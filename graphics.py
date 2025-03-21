import matplotlib.pyplot as plt
import os
import mysql.connector
from tkinter import messagebox
from dotenv import load_dotenv
from datetime import datetime
from database import Database
from userconnection import User

load_dotenv()
pasw = os.getenv("PASSWORD")

class Graphics:
    def __init__(self, db : Database, user_id : int):
        self.db = db
        self.user_id = user_id

    def get_monthly_income(self, month: int, year: int):
        "To get the user income for the selected month"
        try:
            cursor = self.db.get_cursor()
            cursor.execute('''
            SELECT SUM(montant) AS total_income
                FROM transaction
                WHERE type = 'depot'
                AND user_id = %s
                AND MONTH(date) = %s
                AND YEAR(date) = %s;
                ''', (self.user_id, month, year))
            result = cursor.fetchone()
            return result[0] if result[0] is not None else 0
        except mysql.connector.Error as error:
            messagebox.showerror("Erreur", f"Erreur lors de l'execution de la requête : {error}")
            return None
        finally:
            cursor.close()

    def get_monthly_expenses(self, month: int, year: int):
        """To get the monthly expenses for the selected month"""
        try:
            cursor = self.db.get_cursor()
            cursor.execute('''
            SELECT SUM(montant) AS total_expenses
                FROM transaction
                WHERE(type = 'retrait' OR type = 'transfert')
                AND user_id = %s
                AND MONTH(date) = %s
                AND YEAR(date) = %s; 
            ''', (self.user_id, month, year))
            result = cursor.fetchone()
            return result[0] if result[0] is not None else 0
        except mysql.connector.Error as error :
            messagebox.showerror("Erreur", f"Erreur lors de l'execution de la requête : {error}")
            return None
        finally:
            cursor.close()

    def get_monthly_transaction_total(self, trans_type : str, month: int, year: int):
        """ To get the total amount of transaction for a specific type"""
        try:
            cursor = self.db.get_cursor()
            cursor.execute('''
                SELECT SUM(montant) AS total_amount
                    FROM transaction
                    WHERE type = %s
                    AND user_id = %s
                    AND MONTH(date) = %s
                    AND YEAR(date) = %s;     
            ''', (trans_type, self.user_id, month, year))
            result = cursor.fetchone()
            return result[0] if result[0] is not None else 0            
        except mysql.connector.Error as error:
            messagebox.showerror("Erreur", f"Erreur lors de l'éxécution de la requête ; {error}")
            return None
        finally:
            cursor.close()

    def plot_yearly_financials(self):
        """Plot the balances, expenses and income for the current year"""
       
        current_year = datetime.now().year
        months = list(range(1,13))
        incomes = []
        expenses = []
        balances =[]

        for month in months:
            total_income = self.get_monthly_income(month, current_year)
            total_expenses = self.get_monthly_expenses(month, current_year)
            monthly_balance = total_income - total_expenses

            incomes.append(total_income)
            expenses.append(total_expenses)
            balances.append(monthly_balance)

        plt.figure(figsize=(10,6))
        plt.plot(months, incomes, label='Recettes', color='green', marker='o')
        plt.plot(months, expenses, label='Dépenses', color='red', marker='o')
        plt.plot(months, balances, label="Solde", color='blue', marker='o')
        plt.title(f"Aperçu financier des recettes, dépenses et solde pour {current_year}")
        plt.xlabel('Mois')
        plt.ylabel('Montant')
        plt.xticks(months, ['Janv', 'Févr', 'Mars', 'Avr', 'Mai', 'Juin', 'Juill', 'Août', 'Sept', 'Oct', 'Nov', 'Déc'])
        plt.legend()
        plt.grid()
        plt.tight_layout()
        plt.show()

    def plot_monthly_distribution(self):
        """ Plot the distribution of transactions for the current month"""

        current_month = datetime.now().month
        current_year = datetime.now().year

        transaction_types = ['depot', 'retrait', 'transfert']
        amounts = []

        for trans_type in transaction_types:
            total_amount = self.get_monthly_transaction_total(trans_type, current_month, current_year)
            amounts.append(total_amount)
        
        plt.figure(figsize=(8,8))
        plt.pie(amounts, labels=transaction_types, autopct='%1.1f%%', startangle=140, pctdistance=0.85 )
        plt.title(f'Distribution des transactions pour {datetime.now().strftime("%B %Y")}')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()

    
