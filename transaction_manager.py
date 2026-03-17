import sqlite3
from datetime import datetime
from database import get_db_connection
from models import Transaction
from utils import get_numeric_input, get_non_empty_input

class TransactionManager:
    def __init__(self, user_id):
        self.user_id = user_id

    def add_transaction(self, trans_type):
        """
        Adds a new transaction (income or expense) for the current user.
        """
        category = get_non_empty_input("Enter category (e.g., Food, Rent, Salary): ")
        amount = get_numeric_input(f"Enter {trans_type} amount: ", error_msg="Invalid amount. Please enter a number.")
        if amount is None:
            return

        description = input(f"Enter a brief description (optional): ").strip()
        date = datetime.now().strftime("%d-%m-%Y")

        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO transactions (user_id, type, category, amount, date, description) VALUES (?, ?, ?, ?, ?, ?)",
                (self.user_id, trans_type, category, amount, date, description)
            )
            conn.commit()
            print(f"Added {trans_type} of ₹{amount:.2f} to '{category}'.")
        except Exception as e:
            print(f"Error adding transaction: {e}")
        finally:
            conn.close()

        # Proactive budget notification for expenses
        if trans_type == 'expense':
            from budget_manager import BudgetManager
            bm = BudgetManager(self.user_id)
            bm.check_and_notify_budget(category)

    def view_transactions(self):
        """
        Retrieves and displays all transactions for the current user,
        using the Transaction model for a structured output.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transactions WHERE user_id = ? ORDER BY date DESC", (self.user_id,))
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            print("No transactions found.")
            return

        # Convert database rows into a list of Transaction objects
        transactions = [
            Transaction(
                transaction_id=row['id'],
                user_id=row['user_id'],
                type=row['type'],
                category=row['category'],
                amount=row['amount'],
                date=row['date'],
                description=row['description']
            ) for row in rows
        ]

        print("\n--- Your Transactions ---")
        for t in transactions:
            # Handle date string which might be in old YYYY-MM-DD or new DD-MM-YYYY format during migration
            try:
                date_obj = datetime.strptime(t.date, "%d-%m-%Y")
            except (ValueError, TypeError):
                try:
                    date_obj = datetime.strptime(t.date, "%Y-%m-%d")
                except:
                    date_obj = t.date # Fallback

            print(f"ID: {t.id:<3} | Type: {t.type.capitalize():<7} | "
                  f"Category: {t.category:<10} | Amount: ₹{t.amount:,.2f} | "
                  f"Date: {date_obj.strftime('%d-%m-%Y') if isinstance(date_obj, datetime) else date_obj:<10} | Desc: {t.description}")
        print("-------------------------\n")
    
    def update_transaction(self):
        """
        Updates an existing transaction based on its ID.
        """
        trans_id = get_numeric_input("Enter the ID of the transaction to update: ", type_func=int, error_msg="Invalid ID. Please enter a number.")
        if trans_id is None:
            return

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transactions WHERE id = ? AND user_id = ?", (trans_id, self.user_id))
        transaction_row = cursor.fetchone()
        
        if not transaction_row:
            print("Transaction not found or you do not have permission to update it.")
            conn.close()
            return
        
        # Create a Transaction object from the database row
        transaction = Transaction(
            transaction_id=transaction_row['id'],
            user_id=transaction_row['user_id'],
            type=transaction_row['type'],
            category=transaction_row['category'],
            amount=transaction_row['amount'],
            date=transaction_row['date'],
            description=transaction_row['description']
        )
        
        print(f"Updating transaction ID {transaction.id} ({transaction.type.capitalize()}):")
        print(f"Current Category: {transaction.category}")
        new_category = input("Enter new category (leave blank to keep): ").strip() or transaction.category
        
        print(f"Current Amount: ₹{transaction.amount:,.2f}")
        new_amount = get_numeric_input(f"Enter new amount (leave blank to keep): ", error_msg="Invalid amount. Please enter a number.")
        if new_amount is None:
            new_amount = transaction.amount
        
        print(f"Current Description: {transaction.description}")
        new_description = input("Enter new description (leave blank to keep): ").strip() or transaction.description

        try:
            cursor.execute(
                "UPDATE transactions SET category = ?, amount = ?, description = ? WHERE id = ? AND user_id = ?",
                (new_category, new_amount, new_description, trans_id, self.user_id)
            )
            conn.commit()
            print(f"Transaction {trans_id} updated successfully.")
        except Exception as e:
            print(f"Error updating transaction: {e}")
        finally:
            conn.close()

    def delete_transaction(self):
        """
        Deletes a transaction based on its ID.
        """
        trans_id = get_numeric_input("Enter the ID of the transaction to delete: ", type_func=int, error_msg="Invalid ID. Please enter a number.")
        if trans_id is None:
            return

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM transactions WHERE id = ? AND user_id = ?", (trans_id, self.user_id))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"Transaction {trans_id} deleted successfully.")
        else:
            print("Transaction not found or you do not have permission to delete it.")
        conn.close()