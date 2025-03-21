import customtkinter as ctk
from userconnection import User
from database import Database
from tkinter import messagebox


class FinanceApplogin(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Application Bancaire")
        self.geometry("600x500")
        self.resizable(False, False)
        self.user_id = None
        self.db_instance = Database()
        self.user_instance = User(self.db_instance)
        self.login_page()

    def login_page(self):
        """ui login page"""
        for widget in self.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self, text = "BUDGET BUDDY\nCONNEXION", font=("Arial", 24, "bold")).pack(pady=25)
        
        ctk.CTkLabel(self, text="Email").pack(pady=5)
        self.email_entry = ctk.CTkEntry(self)
        self.email_entry.pack(pady=10)

        ctk.CTkLabel(self, text='Mot de passe').pack(pady=5)
        self.password_entry = ctk.CTkEntry(self, show="*")
        self.password_entry.pack(pady=10)

        ctk.CTkButton(self, text="VALIDER", command=self.perform_login).pack(pady=20)

        ctk.CTkLabel(self, text="Nouvel utilisateur ?").pack(pady=10)

        ctk.CTkButton(self, text="S'INSCRIRE", command=self.register_page).pack(pady=10)        
    
    
    def perform_login(self):
        """Execute login user method if all conditions are ok"""
        email = self.email_entry.get()
        password = self.password_entry.get()
        self.user_instance.login_user(email, password)
        
        if self.user_instance.user_id:
            self.user_id = self.user_instance.user_id
            # add here method to go to the next step

    def register_page(self):
        pass

if __name__ == "__main__":
    app = FinanceApplogin()
    app.mainloop()