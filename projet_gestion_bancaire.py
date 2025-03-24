import customtkinter as ctk
import random
from database import Database
from userconnection import User
from tkinter import messagebox
from UIGraphics import GraphicsPage


db_instance = Database()
user_instance = User(db_instance)

ctk.set_appearance_mode("dark")  
ctk.set_default_color_theme("blue")

class AdminPage(ctk.CTkFrame):
    def __init__(self, parent, controller, admin_id): # change made here : add admin_id
        super().__init__(parent)
        self.admin_mode = True # set admin_mode True
        self.db = Database()
        self.controller = controller  
        self.admin_id = admin_id  # changes made here instantiate admin_id
        self.configure(fg_color="white")
        
       
        
        ctk.CTkLabel(self, text="Mode Administrateur", font=("Arial", 22, "bold"), text_color="red").pack(pady=20)
        self.frame_accounts = ctk.CTkScrollableFrame(self, width=500, height=300, fg_color="white")
        self.frame_accounts.pack(pady=20, padx=20, fill="both", expand=True)

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

        self.init_adminui() # changes here

    def init_adminui(self): # add this method
        """ To show user accounts """
        if self.admin_id:
            self.load_account()
        else: 
            messagebox.showerror("Erreur", "L'utilisateur n'est pas identifié.")

    def load_account(self):
        try:
            for widget in self.frame_accounts.winfo_children():
                widget.destroy()
           
            cursor = self.db.get_cursor()
            cursor.execute("SELECT id, nom, numero, montant FROM compte")
            accounts = cursor.fetchall()
            cursor.close()

            for account_id, name, number, montant in accounts:
                texte = f"{name} (N°{number}) - Solde: {montant} €"
                frame_account = ctk.CTkFrame(self.frame_accounts, fg_color="lightgray", corner_radius=10)
                frame_account.pack(pady=5, padx=10, fill="x")

                ctk.CTkLabel(frame_account, text=texte, font=("Arial", 16, "bold"), text_color="black").pack(side="left", padx=10)
               
                button_frame = ctk.CTkScrollableFrame(frame_account, width=450, height=50, fg_color="white", orientation="horizontal")
                button_frame.pack(pady=10, padx=10, fill="x")
                
                ctk.CTkButton(button_frame, text="💵 Dépôt", fg_color="green", hover_color="darkgreen",command=lambda id=account_id: self.perform_transaction(id, "depot")).pack(side="left", padx=2)
                ctk.CTkButton(button_frame, text="💸 Retrait", fg_color="blue", hover_color="darkblue",command=lambda id=account_id: self.perform_transaction(id, "retrait")).pack(side="left", padx=2)
                ctk.CTkButton(button_frame, text="🔄 Virement", fg_color="orange", hover_color="darkorange",command=lambda id=account_id: self.perform_transaction(id, "virement")).pack(side="left", padx=2)
                ctk.CTkButton(button_frame, text="📜 Historique", fg_color="purple", hover_color="purple",command=lambda id=account_id: self.controller.show_historical(id)).pack(side="left", padx=2)

        except Exception as e:
            print(f"Erreur lors du chargement des comptes : {e}")

    def perform_transaction(self, account_id, type_operation):
        self.controller.transaction(account_id, type_operation)
        self.load_account() 

class FinanceApp(ctk.CTkFrame):
    def __init__(self, parent, user_id = None, logout_callback=None):   # changed this line, add parent, user_id 
        super().__init__(parent) 
        self.admin_mode = False
        self.user_id = user_id # add this line
        self.db = Database()
        self.logout_callback = logout_callback
        self.init_ui() # add this line
        #self.page_accueil()  
        #self.title("Application Bancaire")
        #self.geometry("600x500")
        #self.resizable(False, False)
        #self.page_accueil()
    
    def logout(self):
        """ Déconnecte l'utilisateur et retourne à la page de connexion """
        if self.logout_callback:
            self.logout_callback()  

    def init_ui(self): # add this method
        """to show page account """
        self.pack(fill="both", expand = True)
        if self.user_id:
            self.page_account(self.user_id)
        else:
            messagebox.showerror("Erreur", "L'utilisateur n'est pas identifié.")

    def enable_admin_mode(self):
        self.admin_mode = True
        self.show_admin_page()

    def disable_admin_mode(self):
        self.admin_mode = False
        self.page_accueil()

    def show_admin_page(self):
        if self.admin_mode:
            for widget in self.winfo_children():
                widget.destroy()
            admin_page = AdminPage(self, self)
            admin_page.pack(fill="both", expand=True)
    
    def generate_unique_reference(self):
         while True:
            reference = random.randint(10**9, 10**10 - 1) % (10**6)
            cursor = self.db.get_cursor()
            cursor.execute("SELECT reference FROM transaction WHERE reference = %s", (reference,))
            if not cursor.fetchone():  
                cursor.close()
                return reference
            cursor.close()

    def get_user(self):
        cursor = self.db.get_cursor()
        cursor.execute("SELECT id, nom, prenom FROM utilisateur")
        users = cursor.fetchall()
        cursor.close()
        return users

    def get_account(self, user_id):
        cursor = self.db.get_cursor()
        cursor.execute("SELECT id, nom, numero, montant FROM compte WHERE id_utilisateur = %s", (user_id,))
        account = cursor.fetchone()
        cursor.close()
        return account

    def page_accueil(self):
        for widget in self.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self, text="💳 Bienvenue dans votre Banque", font=("Arial", 24, "bold")).pack(pady=20)

        users = self.get_user()
        frame_users = ctk.CTkFrame(self)
        frame_users.pack(pady=20, padx=20, fill="both", expand=True)

        for user_id, name, first_name in users:
            button = ctk.CTkButton(
                frame_users,
                text=f"👤 {first_name} {name}",
                height=80,
                width=80,
                corner_radius=40,
                fg_color="blue",
                hover_color="darkblue",
                font=("Arial", 16, "bold"),
                command=lambda u=user_id: self.page_account(u)
            )
            button.pack(pady=10, padx=10, anchor="center")
        
        ctk.CTkButton(self, text="🔑 Mode Admin", command=self.enable_admin_mode,
              height=40, fg_color="red", hover_color="darkred",
              font=("Arial", 16, "bold")).pack(pady=10)

    def page_account(self, user_id):
        for widget in self.winfo_children():
            widget.destroy()

        account = self.get_account(user_id)
        if account:
            account_id, name, number, montant = account
            ctk.CTkLabel(self, text=f"Compte de {name}", font=("Arial", 22, "bold")).pack(pady=20)

            frame_info = ctk.CTkFrame(self)
            frame_info.pack(pady=20, padx=20, fill="both", expand=True)

            ctk.CTkLabel(frame_info, text=f"Numéro de compte : {number}", font=("Arial", 18)).pack(pady=10)
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
                command=lambda: self.transaction(account_id, "depot"),
                height=40,
                fg_color="blue",
                hover_color="darkblue",
                font=("Arial", 16, "bold")
            ).grid(row=0, column=0, padx=10, pady=10, sticky="ew")

            ctk.CTkButton(
                frame_buttons,
                text="➖ Retirer",
                command=lambda: self.transaction(account_id, "retrait"),
                height=40,
                fg_color="blue",
                hover_color="darkblue",
                font=("Arial", 16, "bold")
            ).grid(row=0, column=1, padx=10, pady=10, sticky="ew")

            ctk.CTkButton(
                frame_buttons,
                text="🔄 Transférer",
                command=lambda: self.transaction(account_id, "virement"),
                height=40,
                fg_color="blue",
                hover_color="darkblue",
                font=("Arial", 16, "bold")
            ).grid(row=1, column=0, padx=10, pady=10, sticky="ew")

            ctk.CTkButton(
                frame_buttons,
                text="📜 Historique",
                command=lambda: self.show_historical(account_id),
                height=40,
                fg_color="blue",
                hover_color="darkblue",
                font=("Arial", 16, "bold")
            ).grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        else:
            ctk.CTkLabel(self, text="Aucun compte trouvé", font=("Arial", 18, "bold"), text_color="red").pack(pady=20)

        ctk.CTkButton(
            self,
            text="↩ Deconnexion",
            command=self.logout,
            height=40,
            fg_color="blue",
            hover_color="darkblue",
            font=("Arial", 16, "bold")
        ).pack(pady=20)

        ctk.CTkButton(
            self,
            text="📊 Rapport Financier",
            command=lambda: self.show_graphics_page(user_id),  
            height=40,
            fg_color="blue",
            hover_color="darkblue",
            font=("Arial", 16, "bold")
        ).pack(pady=20)

    # command=lambda: self.show_graphics_page(user_id), # command for the display graph button

    def show_graphics_page(self, user_id):
        """To perform the display of GraphicsPage"""
        for widget in self.winfo_children():
            widget.destroy()
        graphics_page = GraphicsPage(self, user_id, self)  
        graphics_page.pack(fill="both", expand=True)        

    def transaction(self, account_id, type_operation):
        montant_input = ctk.CTkInputDialog(title="Montant", text="Entrez le montant :").get_input()
        if not montant_input or not montant_input.isdigit():
            return
        montant = float(montant_input)
        if montant <= 0:
            return
    
        cursor = self.db.get_cursor()
        reference = self.generate_unique_reference()
    
        try:
            if type_operation == "depot":
                cursor.execute("UPDATE compte SET montant = montant + %s WHERE id = %s", (montant, account_id))
                cursor.execute("INSERT INTO transaction (reference, description, montant, date, type, id_compte) VALUES (%s, %s, %s, NOW(), %s, %s)",
                               (reference, "Dépôt d'argent", montant, "dépot", account_id))
            elif type_operation == "retrait":
                cursor.execute("SELECT montant FROM compte WHERE id = %s", (account_id,))
                solde_actuel = cursor.fetchone()[0]
                if montant > solde_actuel:
                    ctk.CTkMessagebox.show_error("Erreur", "Solde insuffisant")
                    return
                cursor.execute("UPDATE compte SET montant = montant - %s WHERE id = %s", (montant, account_id))
                cursor.execute("INSERT INTO transaction (reference, description, montant, date, type, id_compte) VALUES (%s, %s, %s, NOW(), %s, %s)",
                               (reference, "Retrait d'argent", montant, "retrait", account_id))
            elif type_operation == "virement":
                account_dest_input = ctk.CTkInputDialog(title="Virement", text="Entrez l'ID du compte destinataire :").get_input()
                if not account_dest_input or not account_dest_input.isdigit():
                    ctk.CTkMessagebox.show_error("Erreur", "ID de compte destinataire invalide")
                    return
                account_dest = int(account_dest_input)
                cursor.execute("SELECT montant FROM compte WHERE id = %s", (account_id,))
                solde_actuel = cursor.fetchone()[0]
                if montant > solde_actuel:
                    ctk.CTkMessagebox.show_error("Erreur", "Solde insuffisant")
                    return
                cursor.execute("UPDATE compte SET montant = montant - %s WHERE id = %s", (montant, account_id))
                cursor.execute("UPDATE compte SET montant = montant + %s WHERE id = %s", (montant, account_dest))
                cursor.execute("INSERT INTO transaction (reference, description, montant, date, type, id_compte) VALUES (%s, %s, %s, NOW(), %s, %s)",
                               (reference, "Virement vers compte " + str(account_dest), montant, "virement", account_id))
    
            self.db.db.commit()
        except Exception as e:
            print(f"Erreur lors de la transaction : {e}")
        finally:
            cursor.close()
    
        if self.admin_mode:
           self.show_admin_page()
        else:
           self.page_account(account_id)
    
    def filtered(self, value, account_id):
        try:    
            cursor = self.db.db.cursor()
            cursor.execute("SELECT reference, type, montant, date FROM transaction WHERE id_compte = %s AND type = %s ORDER BY date DESC", (account_id, value))
            transactions = cursor.fetchall()
            cursor.close()
    
            # Verification
            print("Transactions récupérées :", transactions)
    
        except Exception as e:
            print(f"Erreur lors de la récupération des transactions : {e}")
            transactions = []
    
        for widget in self.frame_historic.winfo_children():
            widget.destroy()

        # Print transactions
        if transactions:
            for reference, type_transaction, amount, date in transactions:
                ctk.CTkLabel(self.frame_historic, text=f"{date} - Réf: {reference} - {type_transaction} : {amount} €",
                         font=("Arial", 18)).pack(pady=5, anchor="w")
        else:
            ctk.CTkLabel(self.frame_historic, text="Aucune transaction trouvée", font=("Arial", 18, "bold"), text_color="red").pack(pady=20)
            

    def show_historical(self, account_id):
        
        for widget in self.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self, text="Historique des Transactions", font=("Arial", 22, "bold")).pack(pady=20)

        combobox = ctk.CTkComboBox(master = self, values=["dépot", "retrait", "virement"])
        combobox.pack(padx=10, pady=5)
        combobox.set("dépot")
        
        ctk.CTkButton(
            self,
            text="Rechercher",
            command=lambda: self.filtered(combobox.get(), account_id),
            height=40,
            fg_color="blue",
            hover_color="darkblue",
            font=("Arial", 16, "bold")
        ).pack(pady=20)

        self.frame_historic = ctk.CTkScrollableFrame(self, width=400, height=150)
        self.frame_historic.pack(pady=20, padx=20, fill="both", expand=True)
        self.filtered(combobox.get(), account_id)

        ctk.CTkButton(
            self,
            text="↩ Retour",
            command=lambda: self.page_account(account_id),
            height=40,
            fg_color="blue",
            hover_color="darkblue",
            font=("Arial", 16, "bold")
        ).pack(pady=20)
                    
                    
if __name__ == "__main__":
    app = FinanceApp()
    app.mainloop()