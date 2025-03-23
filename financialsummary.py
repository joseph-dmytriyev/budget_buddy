import os
import mysql.connector
from dotenv import load_dotenv
from database import Database
from tkinter import messagebox
from userconnection import User

load_dotenv()
passw = os.getenv("PASSWORD")

class FinancialReport:
    def __init__(self, db: Database, user_id: int):
        self.db = db
        self.user_id = user_id

    def get_monthly_income(self, month: int, year: int):
        """ Get the user income for the selected month """

        if month < 1 or month > 12:
            raise ValueError("Le mois doit être entre 1 et 12.")
        if year < 2020: 
            raise ValueError("L'année doit être un nombre positif supèrieur à 2019.")

        try:
            cursor = self.db.get_cursor()
            cursor.execute('''
                SELECT SUM(montant) AS total_recettes
                FROM transaction
                WHERE type = 'depot'
                    AND id_compte IN (SELECT id FROM compte WHERE id_utilisateur = %s)
                    AND MONTH(date) = %s 
                    AND YEAR(date) = %s;
            ''', (self.user_id, month, year))

            result = cursor.fetchone()
            total_income = result[0] if result[0] is not None else 0  
            
            return total_income

        except mysql.connector.Error as error:
            print(f"Erreur lors de l'exécution de la requête : {error}")
            return None
        finally:
            cursor.close()  

    def get_monthly_expenses(self, month: int, year: int):
        """ Get the user expenses for the selected month """

        if month < 1 or month > 12:
            raise ValueError("Le mois doit être entre 1 et 12.")
        if year < 2020: 
            raise ValueError("L'année doit être un nombre positif supèrieur à 2019.")

        try:
            cursor = self.db.get_cursor()
            cursor.execute('''
                SELECT SUM(montant) AS total_expenses
                FROM transaction
                WHERE (type = 'retrait' OR type = 'transfert')
                    AND id_compte IN (SELECT id FROM compte WHERE id_utilisateur = %s)
                    AND MONTH(date) = %s 
                    AND YEAR(date) = %s;
            ''', (self.user_id, month, year))

            result = cursor.fetchone()
            total_expenses = result[0] if result[0] is not None else 0  
            
            return total_expenses

        except mysql.connector.Error as error:
            print(f"Erreur lors de l'exécution de la requête : {error}")
            return None
        finally:
            cursor.close()

    def get_monthly_balance(self, total_income, total_expenses):
        """ Calculate the user balance for the selected month """

        balance = total_income - total_expenses            
        return balance

    def financial_report_message(self, entry_month, entry_year):
        """ Return the message """
        try:

            month = int(entry_month.get())
            year = int(entry_year.get())
            
            total_income = self.get_monthly_income(month, year)
            total_expenses = self.get_monthly_expenses(month, year)

            if total_income is not None and total_expenses is not None:

                balance = self.get_monthly_balance(total_income, total_expenses)
                messagebox.showinfo("Rapport financier", f"Pour {month}/{year}\nLes recettes sont : {total_income}\nLes dépenses sont : {total_expenses}\nLe solde est : {balance}" )

        except ValueError as error:
            messagebox.showerror("Erreur de saisie", f"Erreur de saisie : {str(error)}")



