import customtkinter as ctk
from userconnection import User
from database import Database
from tkinter import messagebox
from projet_gestion_bancaire import FinanceApp, AdminPage


class FinanceApplogin(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Budget Buddy")
        self.geometry("600x500")
        self.resizable(False, False)
        self.user_id = None
        self.admin_id = None
        self.db_instance = Database()
        self.user_instance = User(self.db_instance)
        self.admin_instance = User(self.db_instance)
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True)

        self.login_page()

    def login_page(self):
        """ui login page"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.main_frame, text="BUDGET BUDDY\nCONNEXION", font=("Arial", 24, "bold")).pack(pady=25)

        ctk.CTkLabel(self.main_frame, text="Email").pack(pady=5)
        self.email_entry = ctk.CTkEntry(self.main_frame)
        self.email_entry.pack(pady=10)

        ctk.CTkLabel(self.main_frame, text='Mot de passe').pack(pady=5)
        self.password_entry = ctk.CTkEntry(self.main_frame, show="*")
        self.password_entry.pack(pady=10)

        ctk.CTkButton(self.main_frame, text="VALIDER", command=self.perform_login).pack(pady=20)

        ctk.CTkLabel(self.main_frame, text="Nouvel utilisateur ?").pack(pady=10)
        ctk.CTkButton(self.main_frame, text="S'INSCRIRE", command=self.register_page).pack(pady=10)

        admin_link = ctk.CTkLabel(self.main_frame, text="Admin connexion", text_color="white", cursor="hand2")
        admin_link.pack(pady=10)
        admin_link.bind("<Button-1>", lambda e: self.admin_page())

    def show_account_page(self, user_id):
        """Show user account page"""
        try:
            if hasattr(self, 'main_frame') and self.main_frame.winfo_exists():
                for widget in self.main_frame.winfo_children():
                    widget.destroy()
                finance_app = FinanceApp(self.main_frame, user_id)
                finance_app.pack(fill="both", expand=True)
            else:
                raise AttributeError("self.main_frame n'existe pas ou a été détruit.")
        except AttributeError as error:
            print(f"Erreur : {error}")
            messagebox.showerror("Erreur", "Une erreur est survenue. Veuillez réessayer.")

            self.main_frame = ctk.CTkFrame(self, fg_color="white")
            self.main_frame.pack(fill="both", expand=True)
            self.show_account_page(self.user_id)
            
    def show_admin_page(self, admin_id):
        """ Show admin page """
        try:
            if hasattr(self, 'main_frame') and self.main_frame.winfo_exists():
                for widget in self.main_frame.winfo_children():
                    widget.destroy()
                admin_page = AdminPage(self.main_frame, self, admin_id) 
                admin_page.pack(fill="both", expand=True)
            else:
                raise AttributeError("self.main_frame n'existe pas ou a été détruit.")
        except AttributeError as error:
            print(f"Erreur : {error}")
            messagebox.showerror("Erreur", "Une erreur est survenue. Veuillez réessayer.")
            self.main_frame = ctk.CTkFrame(self, fg_color="white")
            self.main_frame.pack(fill="both", expand=True)
            self.show_admin_page(admin_id)
    
    def disable_admin_mode(self):
        """ Disable admin mode """
        self.admin_mode = False
        self.admin_id = None
        self.login_page()

    def perform_login(self):
        """Execute login user method if all conditions are ok"""
        email = self.email_entry.get()
        password = self.password_entry.get()
        user_id = self.user_instance.login_user(email, password)

        if user_id:
            self.user_id = user_id
            if hasattr(self, 'main_frame') and self.main_frame.winfo_exists():
                self.show_account_page(self.user_id)
            else:
                print("Erreur : self.main_frame n'existe pas ou a été détruit.")
        else:
            messagebox.showerror("Erreur", "Identifiants invalides.")

    def register_page(self):
        """Ui register page"""
        for widget in self.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self, text = "Créer un compte", font=("Arial", 24, "bold")).pack(pady=25)
        
        ctk.CTkLabel(self, text = "Nom").pack(pady=5)
        self.name_entry = ctk.CTkEntry(self)
        self.name_entry.pack(pady = 5)

        ctk.CTkLabel(self, text="Prénom").pack(pady=5)
        self.surname_entry = ctk.CTkEntry(self)
        self.surname_entry.pack(pady= 5)

        ctk.CTkLabel(self, text="Email").pack(pady=5)
        self.register_email_entry = ctk.CTkEntry(self)
        self.register_email_entry.pack(pady= 5)

        ctk.CTkLabel(self, text= "Mot de passe").pack(pady=5)
        self.register_password_entry = ctk.CTkEntry(self, show="*")
        self.register_password_entry.pack(pady=5)

        ctk.CTkButton(self, text="S'INSCRIRE", command=self.create_account).pack(pady=15)

        back_link = ctk.CTkLabel(self, text="Retour à la page de connexion", text_color="white", cursor="hand2")
        back_link.pack(pady=10)
        back_link.bind("<Button-1>", lambda e: self.login_page())

    def create_account(self):
        """To register the new user in database"""
        nom = self.name_entry.get()
        prenom = self.surname_entry.get()
        email = self.register_email_entry.get()
        motdepasse = self.register_password_entry.get()

        registration_success = self.user_instance.register_user(nom, prenom, email, motdepasse)
        if registration_success:
            messagebox.showinfo("Succès", "Vous êtes enregistré !")
            self.login_page()

    def admin_page(self):
        """Ui admin """
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.main_frame, text="ADMIN CONNEXION", font=("Arial", 24, "bold")).pack(pady=25)

        ctk.CTkLabel(self.main_frame, text="Email").pack(pady=5) 
        self.admin_email_entry = ctk.CTkEntry(self.main_frame)
        self.admin_email_entry.pack(pady=10) 

        ctk.CTkLabel(self.main_frame, text= "Mot de passe").pack(pady=5)
        self.admin_password_entry = ctk.CTkEntry(self.main_frame, show="*")
        self.admin_password_entry.pack(pady = 10) 

        ctk.CTkButton(self.main_frame, text = "SE CONNECTER", command=self.perform_admin_login).pack(pady=10)
        
    def perform_admin_login(self):
        """Perform admin login when all conditions are ok"""
        email = self.admin_email_entry.get()
        motdepasse = self.admin_password_entry.get()
        admin_id = self.admin_instance.admin_login(email, motdepasse)

        if admin_id:
            self.admin_id = admin_id
            if hasattr(self, 'main_frame') and self.main_frame.winfo_exists():
                self.show_admin_page(self.admin_id)
            else: 
                print("Erreur : self.main_frame n'existe pas ou a été détruit.")
        else:
            messagebox.showerror("Erreur", "Identifiants invalides.")

if __name__ == "__main__":
    app = FinanceApplogin()
    app.mainloop()