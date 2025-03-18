import os
import mysql.connector
import hashlib
from dotenv import load_dotenv
from database import Database
from tkinter import messagebox

load_dotenv()
passw = os.getenv("PASSWORD")

class User:
    def __init__(self, db: Database):
        self.db = db

    def hash_password(self, password):
        """To hash the user password"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def validate_password(self, motdepasse):
        """To validate the password before hash and register in database"""
        if (len(motdepasse) < 10 or 
            not any(character.isupper() for character in motdepasse) 
            or not any (character.islower() for character in motdepasse)
            or not any(character.isdigit() for character in motdepasse)
            or not any (character in '?,.;/:§!%&*()-+|' for character in motdepasse)):
            return False
        return True
    
    def register_user(self, nom, prenom, email, motdepasse):
        """To register a new user"""

        if not self.validate_password(motdepasse):
            messagebox.showerror("Erreur", "Le mot de passe doit contenir au moins 10 caractères, une majuscule, une minuscule, un chiffre et un caractère spécial.")
            return
        hashed_password = self.hash_password(motdepasse)
        cursor = self.db.get_cursor()

        try:
            cursor.execute("INSERT INTO utilisateur (nom, prenom, email, motdepasse) VALUES (%s, %s, %s, %s)", (nom, prenom, email, hashed_password))
            self.db.db.commit()
        except mysql.connector.Error as error:
            raise Exception(f"Erreur d'inscription {error}")
        finally:
            cursor.close()