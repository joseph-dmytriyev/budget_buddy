import customtkinter as ctk 
from userconnection import User
from database import Database
from tkinter import messagebox

class FinanceAppLogin(ctk.CTk):
    def __intit__(self):
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
        
        ctk.CTkLabel(self, text = "BUDGET BUDDY\nCONNEXION", font=("Arial", 24, "bold")).pack(pady=20)
        ctk.CTkLabel(self, text="Email").pack(pady=5)
        self.email_entry = ctk.CTkEntry(self, show ='*')
        

if __name__ == "__main__":
    app = FinanceAppLogin()
    app.mainloop()