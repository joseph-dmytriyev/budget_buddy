import customtkinter as ctk
from database import Database
from graphics import Graphics
from tkinter import messagebox
from financialsummary import FinancialReport

class GraphicsPage(ctk.CTkFrame):
    def __init__(self, parent, user_id, controller):
        super().__init__(parent)
        self.db = Database()
        self.user_id = user_id
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        """ The graphic ui interface """
        ctk.CTkLabel(self, text="Rapport Financier", font=("Arial", 24, "bold")).pack(pady=20)

        entry_frame = ctk.CTkFrame(self)
        entry_frame.pack(pady=10)

        ctk.CTkLabel(entry_frame, text = "Entrez :").pack(side = "left", padx = 5)

        self.month_entry = ctk.CTkEntry(entry_frame, placeholder_text = "Mois (1-12)")
        self.month_entry.pack(side = "left", padx = 5)

        self.year_entry = ctk.CTkEntry(entry_frame, placeholder_text ="Année (à partir de 2023)")
        self.year_entry.pack(side = "left", padx = 5)

        ctk.CTkButton(entry_frame, text = "Afficher le Rapport Financier", command = self.show_financial_report).pack(side = "left", padx = 5)

        ctk.CTkButton(self, text="Retour au compte", command = self.go_back_to_account).pack(pady = 10) 

    def show_financial_report(self):
        financial_report = FinancialReport(self.db, self.user_id)
        financial_report.financial_report_message(self.month_entry, self.year_entry)

    def go_back_to_account(self):
        """ Go back to the user account """
        self.destroy()  
        self.controller.page_compte(self.user_id)
