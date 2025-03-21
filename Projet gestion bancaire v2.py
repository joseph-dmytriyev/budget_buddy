import customtkinter as ctk
import mysql.connector
import random
import CTkMessagebox



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



class AdminPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="white")  

        ctk.CTkLabel(self, text="Mode Administrateur", font=("Arial", 22, "bold"), text_color="red").pack(pady=20)

        
        self.frame_account = ctk.CTkScrollableFrame(self, width=500, height=300, fg_color="white")
        self.frame_account.pack(pady=20, padx=20, fill="both", expand=True)

        self.load_account()  

        
        ctk.CTkButton(
            self,
            text="🚪 Déconnexion Admin",
            command=self.controller.disable_admin_mode,
            height=40,
            fg_color="red",
            hover_color="darkred",
            text_color="white",
            font=("Arial", 16, "bold")
        ).pack(pady=20)

    def load_account(self):
        
        try:
            
            for widget in self.frame_account.winfo_children():
                widget.destroy()

            
            cursor = db.cursor()
            cursor.execute("SELECT id, nom, numero, montant FROM compte")
            account = cursor.fetchall()
            cursor.close()

            for compte_id, nom, numero, montant in account:
                text = f"{nom} (N°{numero}) - Solde: {montant} €"
                frame_account = ctk.CTkFrame(self.frame_account, fg_color="lightgray", corner_radius=10)
                frame_account.pack(pady=5, padx=10, fill="x")

                ctk.CTkLabel(frame_account, text=text, font=("Arial", 16, "bold"), text_color="black").pack(side="left", padx=10)

                
                button_frame = ctk.CTkScrollableFrame(frame_account, width=450, height=50, fg_color="white", orientation="horizontal")
                button_frame.pack(pady=10, padx=10, fill="x")

                
                ctk.CTkButton(button_frame, text="💵 Dépôt", fg_color="green", hover_color="darkgreen",command=lambda id=compte_id: self.perform_transaction(id, "depot")).pack(side="left", padx=2)
                ctk.CTkButton(button_frame, text="💸 Retrait", fg_color="blue", hover_color="darkblue",command=lambda id=compte_id: self.perform_transaction(id, "retrait")).pack(side="left", padx=2)
                ctk.CTkButton(button_frame, text="🔄 Virement", fg_color="orange", hover_color="darkorange",command=lambda id=compte_id: self.perform_transaction(id, "virement")).pack(side="left", padx=2)
                ctk.CTkButton(button_frame, text="📜 Historique", fg_color="purple", hover_color="darkpurple",command=lambda id=compte_id: self.controller.afficher_historique(id)).pack(side="left", padx=2)

        except Exception as e:
            print(f"Erreur lors du chargement des comptes : {e}")

    def perform_transaction(self, compte_id, type_operator):
        
        self.controller.transaction(compte_id, type_operator)
        self.load_account()  








class FinanceApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.admin_mode = False
        self.home_page()  
        self.title("Application Bancaire")
        self.geometry("600x500")
        self.resizable(False, False)
        self.home_page()
        
   

   
    def enable_admin_mode(self):
        
        self.admin_mode = True
        self.show_admin_page()

    def disable_admin_mode(self):
        
        self.admin_mode = False
        self.home_page()

    def show_admin_page(self):
        
        if self.admin_mode:
            for widget in self.winfo_children():
                widget.destroy()
            admin_page = AdminPage(self, self)
            admin_page.pack(fill="both", expand=True)

     
    def generate_unique_reference(self):
     
         while True:
             reference = random.randint(10**6, 10**7 - 1)

             cursor = db.cursor()
             cursor.execute("SELECT reference FROM transaction WHERE reference = %s", (reference,))
             if not cursor.fetchone():  
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

    def home_page(self):
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
        
        ctk.CTkButton(self, text="🔑 Mode Admin", command=self.enable_admin_mode,
              height=40, fg_color="red", hover_color="darkred",
              font=("Arial", 16, "bold")).pack(pady=10)


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
            command=self.home_page,
            height=40,
            fg_color="blue",
            hover_color="darkblue",
            font=("Arial", 16, "bold")
        ).pack(pady=20)

    def transaction(self, compte_id, type_operator):
        montant_input = ctk.CTkInputDialog(title="Montant", text="Entrez le montant :").get_input()
        if not montant_input or not montant_input.isdigit():
            return
        montant = float(montant_input)
        if montant <= 0:
            return
    
        cursor = db.cursor()
        reference = self.generate_unique_reference()
    
        try:
            if type_operator == "depot":
                cursor.execute("UPDATE compte SET montant = montant + %s WHERE id = %s", (montant, compte_id))
                cursor.execute("INSERT INTO transaction (reference, description, montant, date, type, id_compte) VALUES (%s, %s, %s, NOW(), %s, %s)",
                               (reference, "Dépôt d'argent", montant, "dépot", compte_id))
            elif type_operator == "retrait":
                cursor.execute("SELECT montant FROM compte WHERE id = %s", (compte_id,))
                solde_actuel = cursor.fetchone()[0]
                if montant > solde_actuel:
                    CTkMessagebox.show_error("Erreur", "Solde insuffisant")
                    return
                cursor.execute("UPDATE compte SET montant = montant - %s WHERE id = %s", (montant, compte_id))
                cursor.execute("INSERT INTO transaction (reference, description, montant, date, type, id_compte) VALUES (%s, %s, %s, NOW(), %s, %s)",
                               (reference, "Retrait d'argent", montant, "retrait", compte_id))
            elif type_operator == "virement":
                compte_dest_input = ctk.CTkInputDialog(title="Virement", text="Entrez l'ID du compte destinataire :").get_input()
                if not compte_dest_input or not compte_dest_input.isdigit():
                    CTkMessagebox.show_error("Erreur", "ID de compte destinataire invalide")
                    return
                compte_dest = int(compte_dest_input)
                cursor.execute("SELECT montant FROM compte WHERE id = %s", (compte_id,))
                solde_actuel = cursor.fetchone()[0]
                if montant > solde_actuel:
                    CTkMessagebox.show_error("Erreur", "Solde insuffisant")
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
    
        if self.admin_mode:
           self.show_admin_page()
        else:
           self.page_compte(compte_id)
    
    
            

    def afficher_historique(self, compte_id):
        
        for widget in self.winfo_children():
            widget.destroy()
    
        try:
            
            cursor = db.cursor()
            cursor.execute("SELECT reference, type, montant, date FROM transaction WHERE id_compte = %s ORDER BY date DESC", (compte_id,))
            transactions = cursor.fetchall()
            cursor.close()
    
            # Vérification
            print("Transactions récupérées :", transactions)
    
        except Exception as e:
            print(f"Erreur lors de la récupération des transactions : {e}")
            transactions = []
    
        # label historique 
        ctk.CTkLabel(self, text="Historique des Transactions", font=("Arial", 22, "bold")).pack(pady=20)
    
        #  cadre historique 
        frame_historique = ctk.CTkScrollableFrame(self, width=500, height=300)
        frame_historique.pack(pady=20, padx=20, fill="both", expand=True)
    
        # Affiche transactions
        if transactions:
            for reference, type_transaction, montant, date in transactions:
                ctk.CTkLabel(frame_historique, text=f"{date} - Réf: {reference} - {type_transaction} : {montant} €",
                         font=("Arial", 18)).pack(pady=5, anchor="w")
        else:
            ctk.CTkLabel(frame_historique, text="Aucune transaction trouvée", font=("Arial", 18, "bold"), text_color="red").pack(pady=20)
    
        
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
