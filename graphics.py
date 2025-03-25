import matplotlib.pyplot as plt
import os
import mysql.connector
from tkinter import messagebox
from dotenv import load_dotenv
from datetime import datetime
from database import Database
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

load_dotenv()
pasw = os.getenv("PASSWORD")

class Graphics:
    def __init__(self, db : Database, user_id : int, parent = None):
        self.db = db
        self.user_id = user_id
        self.parent = parent

    def get_monthly_income(self, month: int, year: int):
        
        try:
            cursor = self.db.get_cursor()
            cursor.execute('''
            SELECT SUM(montant) AS total_income
                FROM transaction
                WHERE type = 'dépot'
                AND id_compte IN (SELECT id FROM compte WHERE id_utilisateur = %s)
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
                WHERE(type = 'retrait' OR type = 'virement')
                AND id_compte IN (SELECT id FROM compte WHERE id_utilisateur = %s)
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
                    AND id_compte IN (SELECT id FROM compte WHERE id_utilisateur = %s)
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

    def plot_monthly_distribution(self):
        """ Plot the distribution of transactions for the current month"""
        for widget in self.parent.graph_frame.winfo_children():            
            widget.destroy()
        current_month = datetime.now().month
        current_year = datetime.now().year

        transaction_types = ['depot', 'retrait', 'virement']
        amounts = []

        for trans_type in transaction_types:
            total_amount = self.get_monthly_transaction_total(trans_type, current_month, current_year)
            amounts.append(total_amount)

        fig, ax = plt.subplots(figsize=(3, 3))
        ax.pie(amounts, labels=transaction_types, autopct='%1.1f%%', startangle=140, pctdistance=0.85)
        ax.set_title(f"Répartition des transactions pour {datetime.now().strftime('%B %Y')}")
        ax.axis('equal')

        if hasattr(self, 'canvas'):        
            self.canvas.get_tk_widget().destroy()
        self.fig = fig
        self.canvas = FigureCanvasTkAgg(fig, master=self.parent.graph_frame)    
        self.canvas.draw()    
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def plot_yearly_financials(self):
        """Plot the balances, expenses and income for the current year"""
        for widget in self.parent.graph_frame.winfo_children():            
            widget.destroy()
        current_year = datetime.now().year
        months = list(range(1, 13))
        incomes = []
        expenses = []
        balances = []

        for month in months:
            total_income = self.get_monthly_income(month, current_year)
            total_expenses = self.get_monthly_expenses(month, current_year)
            monthly_balance = total_income - total_expenses

            incomes.append(total_income)
            expenses.append(total_expenses)
            balances.append(monthly_balance)

        fig, ax = plt.subplots(figsize=(7, 3))
        ax.plot(months, incomes, label='Recettes', color='green', marker='o')
        ax.plot(months, expenses, label='Dépenses', color='red', marker='o')
        ax.plot(months, balances, label="Solde", color='blue', marker='o')
        ax.set_title(f"Aperçu financier des recettes, dépenses et solde pour {current_year}")
        ax.set_xlabel('Mois')
        ax.set_ylabel('Montant')
        ax.set_xticks(months)
        ax.set_xticklabels(['Janv', 'Févr', 'Mars', 'Avr', 'Mai', 'Juin', 'Juill', 'Août', 'Sept', 'Oct', 'Nov', 'Déc'])
        ax.legend()
        ax.grid()

        if hasattr(self, 'canvas'):        
            self.canvas.get_tk_widget().destroy()
        self.fig = fig
        self.canvas = FigureCanvasTkAgg(fig, master=self.parent.graph_frame)    
        self.canvas.draw()    
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
