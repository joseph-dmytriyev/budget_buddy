import os
import mysql.connector
import hashlib
import secrets
from dotenv import load_dotenv
from database import Database
from tkinter import messagebox
import re

load_dotenv()
passw = os.getenv("PASSWORD")
pepper = os.getenv("PEPPER")

class User:
    def __init__(self, db: Database):
        self.db = db
        self.user_id = None
        self.admin_id = None

    def hash_password(self, password, salt):
        """To hash the user password."""
        return hashlib.sha256((password + salt + pepper).encode()).hexdigest()
    
    def generate_salt(self):
        "generate random salt"
        return secrets.token_hex(16)
    
    def validate_password(self, motdepasse):
        """To validate the password before hashing and registering in the database."""
        if (len(motdepasse) < 10 or 
            not any(character.isupper() for character in motdepasse) 
            or not any(character.islower() for character in motdepasse)
            or not any(character.isdigit() for character in motdepasse)
            or not any(character in '?,.;/:§!%&*()-+|@' for character in motdepasse)):
            return False
        return True    

    def validate_email(self, email):
        """Validate the email format."""
        email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
        return re.match(email_regex, email) is not None
    
    def register_user(self, nom, prenom, email, motdepasse):
        """To register a new user."""
        
        if not self.validate_email(email):
            messagebox.showerror("Erreur", "L'adresse e-mail fournie n'est pas valide.")
            return False

        if not self.validate_password(motdepasse):
            messagebox.showerror("Erreur", "Le mot de passe doit contenir au moins 10 caractères, une majuscule, une minuscule, un chiffre et un caractère spécial.")
            return False
        
        salt = self.generate_salt() 
        hashed_password = self.hash_password(motdepasse, salt)
        cursor = self.db.get_cursor()

        try:
            cursor.execute("INSERT INTO utilisateur (nom, prenom, email, motdepasse, salt) VALUES (%s, %s, %s, %s, %s)", 
                            (nom, prenom, email, hashed_password, salt))
            self.db.db.commit()
            messagebox.showinfo("Succès", "Utilisateur enregistré avec succès!")
            return True
        except mysql.connector.Error as error:
            messagebox.showerror("Erreur", f"Erreur d'inscription : {error}")
            return False
        finally:
            cursor.close()

    def login_user(self, email, motdepasse):
        """To log in an existing user."""

        cursor = self.db.get_cursor()

        try:
            cursor.execute("SELECT id, nom, prenom, motdepasse, salt FROM utilisateur WHERE email = %s", (email,))
            result = cursor.fetchone()

            if result:
                self.user_id, nom, prenom, stored_password, salt = result
                hashed_password = self.hash_password(motdepasse, salt)

                if stored_password == hashed_password:
                    messagebox.showinfo("Bonjour", f"Bienvenue {prenom} {nom}!")
                    return True
                else:
                    messagebox.showerror("Erreur", "Le mot de passe est incorrect.")
                    return False
            else:
                messagebox.showerror("Erreur", "Cet e-mail n'est pas enregistré.")
                return False

        except mysql.connector.Error as error:
            messagebox.showerror("Erreur", f"Erreur lors de la connexion {error}")
        finally:
            cursor.close()

    def admin_login(self, email, motdepasse):
        """To log in as an admin."""
        cursor = self.db.get_cursor()

        try:
            cursor.execute("SELECT id, nom, prenom, motdepasse, salt FROM banquier WHERE email = %s", (email,))
            result = cursor.fetchone()

            if result:
                self.admin_id, nom, prenom, stored_password, salt = result
                hashed_password = self.hash_password(motdepasse, salt)
                
                if stored_password == hashed_password:
                    messagebox.showinfo("Bonjour", f"Bienvenue {prenom} {nom}!")
                    return True
                else:
                    messagebox.showerror("Erreur", "Le mot de passe est incorrect.")
                    return False
            else:
                messagebox.showerror("Erreur", "Cet e-mail d'administrateur n'est pas enregistré.")
                return False

        except mysql.connector.Error as error:
            messagebox.showerror("Erreur", f"Erreur lors de la connexion admin {error}")
        finally:
            cursor.close()