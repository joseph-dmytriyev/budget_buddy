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
    def __init_(self, db : Database, user_id = int):
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

    def get_monthly_expensed(self, month: int, year: int):
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

    def get_monthly_transaction_total(self, transaction_type : str, month: int, year: int):
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
            ''', (transaction_type, self.user_id, month, year))
            result = cursor.fetchone()
            return result[0] if result[0] is not None else 0            
        except mysql.connector.Error as error:
            messagebox.showerror("Erreur", f"Erreur lors de l'éxécution de la requête ; {error}")
        finally:
            cursor.close()


    
