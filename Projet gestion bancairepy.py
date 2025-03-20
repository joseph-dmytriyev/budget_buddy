import customtkinter as ctk
import mysql.connector
import random



try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="godsAvou1r",
        database="finance"
    )
except mysql.connector.Error as err:
    print(f"Erreur de connexion à la base de données: {err}")
    exit()

# Configuration de la fenêtre principale
ctk.set_appearance_mode("dark")  
ctk.set_default_color_theme("blue")


class FinanceApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Application Bancaire")
        self.geometry("600x500")
        self.resizable(False, False)
        self.page_accueil()
        
   

    def generate_unique_reference(self):
    
        while True:
            reference = random.randint(10**9, 10**10 - 1) % (10**6)

            cursor = db.cursor()
            cursor.execute("SELECT reference FROM transaction WHERE reference = %s", (reference,))
            if not cursor.fetchone():  # Vérifie si la référence existe déjà
                cursor.close()
                return reference
            cursor.close()


    def get_user(self):
        cursor = db.cursor()
        cursor.execute("SELECT id, nom, prenom FROM utilisateur")
        users = cursor.fetchall()
        cursor.close()
        return users

    def get_account(self, user_id):
        cursor = db.cursor()
        cursor.execute("SELECT id, nom, numero, montant FROM compte WHERE id_utilisateur = %s", (user_id,))
        compte = cursor.fetchone()
        cursor.close()
        return compte

    def page_accueil(self):
        for widget in self.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self, text="💳 Bienvenue dans votre Banque", font=("Arial", 24, "bold")).pack(pady=20)

        users = self.get_user()
        frame_users = ctk.CTkFrame(self)
        frame_users.pack(pady=20, padx=20, fill="both", expand=True)

        for user_id, nom, prenom in users:
            button = ctk.CTkButton(
                frame_users,
                text=f"👤 {prenom} {nom}",
                height=80,
                width=80,
                corner_radius=40,
                fg_color="blue",
                hover_color="darkblue",
                font=("Arial", 16, "bold"),
                command=lambda u=user_id: self.page_compte(u)
            )
            button.pack(pady=10, padx=10, anchor="center")

    def page_compte(self, user_id):
        for widget in self.winfo_children():
            widget.destroy()

        account = self.get_account(user_id)
        if account:
            compte_id, nom, numero, montant = account
            ctk.CTkLabel(self, text=f"Compte de {nom}", font=("Arial", 22, "bold")).pack(pady=20)

            frame_info = ctk.CTkFrame(self)
            frame_info.pack(pady=20, padx=20, fill="both", expand=True)

            ctk.CTkLabel(frame_info, text=f"Numéro de compte : {numero}", font=("Arial", 18)).pack(pady=10)
            ctk.CTkLabel(frame_info, text=f"💰 Solde : {montant} €", font=("Arial", 18, "bold"), text_color="green").pack(pady=10)

            frame_buttons = ctk.CTkFrame(self)
            frame_buttons.pack(pady=20, padx=20, fill="both", expand=True)

            # Centrer les boutons dans la grille
            frame_buttons.grid_columnconfigure(0, weight=1)
            frame_buttons.grid_columnconfigure(1, weight=1)
            frame_buttons.grid_rowconfigure(0, weight=1)
            frame_buttons.grid_rowconfigure(1, weight=1)

            ctk.CTkButton(
                frame_buttons,
                text="➕ Déposer",
                command=lambda: self.transaction(compte_id, "depot"),
                height=40,
                fg_color="blue",
                hover_color="darkblue",
                font=("Arial", 16, "bold")
            ).grid(row=0, column=0, padx=10, pady=10, sticky="ew")

            ctk.CTkButton(
                frame_buttons,
                text="➖ Retirer",
                command=lambda: self.transaction(compte_id, "retrait"),
                height=40,
                fg_color="blue",
                hover_color="darkblue",
                font=("Arial", 16, "bold")
            ).grid(row=0, column=1, padx=10, pady=10, sticky="ew")

            ctk.CTkButton(
                frame_buttons,
                text="🔄 Transférer",
                command=lambda: self.transaction(compte_id, "virement"),
                height=40,
                fg_color="blue",
                hover_color="darkblue",
                font=("Arial", 16, "bold")
            ).grid(row=1, column=0, padx=10, pady=10, sticky="ew")

            ctk.CTkButton(
                frame_buttons,
                text="📜 Historique",
                command=lambda: self.afficher_historique(compte_id),
                height=40,
                fg_color="blue",
                hover_color="darkblue",
                font=("Arial", 16, "bold")
            ).grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        else:
            ctk.CTkLabel(self, text="Aucun compte trouvé", font=("Arial", 18, "bold"), text_color="red").pack(pady=20)

        ctk.CTkButton(
            self,
            text="↩ Retour",
            command=self.page_accueil,
            height=40,
            fg_color="blue",
            hover_color="darkblue",
            font=("Arial", 16, "bold")
        ).pack(pady=20)

    def transaction(self, compte_id, type_operation):
        montant_input = ctk.CTkInputDialog(title="Montant", text="Entrez le montant :").get_input()
        if not montant_input or not montant_input.isdigit():
            return
        montant = float(montant_input)
        if montant <= 0:
            return
    
        cursor = db.cursor()
        reference = self.generate_unique_reference()
    
        try:
            if type_operation == "depot":
                cursor.execute("UPDATE compte SET montant = montant + %s WHERE id = %s", (montant, compte_id))
                cursor.execute("INSERT INTO transaction (reference, description, montant, date, type, id_compte) VALUES (%s, %s, %s, NOW(), %s, %s)",
                               (reference, "Dépôt d'argent", montant, "dépot", compte_id))
            elif type_operation == "retrait":
                cursor.execute("SELECT montant FROM compte WHERE id = %s", (compte_id,))
                solde_actuel = cursor.fetchone()[0]
                if montant > solde_actuel:
                    ctk.CTkMessagebox.show_error("Erreur", "Solde insuffisant")
                    return
                cursor.execute("UPDATE compte SET montant = montant - %s WHERE id = %s", (montant, compte_id))
                cursor.execute("INSERT INTO transaction (reference, description, montant, date, type, id_compte) VALUES (%s, %s, %s, NOW(), %s, %s)",
                               (reference, "Retrait d'argent", montant, "retrait", compte_id))
            elif type_operation == "virement":
                compte_dest_input = ctk.CTkInputDialog(title="Virement", text="Entrez l'ID du compte destinataire :").get_input()
                if not compte_dest_input or not compte_dest_input.isdigit():
                    ctk.CTkMessagebox.show_error("Erreur", "ID de compte destinataire invalide")
                    return
                compte_dest = int(compte_dest_input)
                cursor.execute("SELECT montant FROM compte WHERE id = %s", (compte_id,))
                solde_actuel = cursor.fetchone()[0]
                if montant > solde_actuel:
                    ctk.CTkMessagebox.show_error("Erreur", "Solde insuffisant")
                    return
                cursor.execute("UPDATE compte SET montant = montant - %s WHERE id = %s", (montant, compte_id))
                cursor.execute("UPDATE compte SET montant = montant + %s WHERE id = %s", (montant, compte_dest))
                cursor.execute("INSERT INTO transaction (reference, description, montant, date, type, id_compte) VALUES (%s, %s, %s, NOW(), %s, %s)",
                               (reference, "Virement vers compte " + str(compte_dest), montant, "virement", compte_id))
    
            db.commit()
        except Exception as e:
            print(f"Erreur lors de la transaction : {e}")
        finally:
            cursor.close()
    
        self.page_compte(compte_id)
    
    
            

    def afficher_historique(self, compte_id):
        # Supprimer les widgets existants
        for widget in self.winfo_children():
            widget.destroy()
    
        try:
            # Connexion à la base de données et exécution de la requête
            cursor = db.cursor()
            cursor.execute("SELECT type, montant, date FROM transaction WHERE id_compte = %s ORDER BY date DESC", (compte_id,))
            transactions = cursor.fetchall()
            cursor.close()
    
            # Vérifier les transactions récupérées
            print("Transactions récupérées :", transactions)
    
        except Exception as e:
            print(f"Erreur lors de la récupération des transactions : {e}")
            transactions = []
    
        # Créer le label pour l'historique des transactions
        ctk.CTkLabel(self, text="Historique des Transactions", font=("Arial", 22, "bold")).pack(pady=20)
    
        # Créer un cadre pour l'historique des transactions
        frame_historique = ctk.CTkFrame(self)
        frame_historique.pack(pady=20, padx=20, fill="both", expand=True)
    
        # Afficher les transactions
        if transactions:
            for type_transaction, montant, date in transactions:
                ctk.CTkLabel(frame_historique, text=f"{date} - {type_transaction} : {montant} €", font=("Arial", 18)).pack(pady=5, anchor="w")
        else:
            ctk.CTkLabel(frame_historique, text="Aucune transaction trouvée", font=("Arial", 18, "bold"), text_color="red").pack(pady=20)
    
        # Créer le bouton de retour
        ctk.CTkButton(
            self,
            text="↩ Retour",
            command=lambda: self.page_compte(compte_id),
            height=40,
            fg_color="blue",
            hover_color="darkblue",
            font=("Arial", 16, "bold")
        ).pack(pady=20)


                    

if __name__ == "__main__":
    app = FinanceApp()
    app.mainloop()
