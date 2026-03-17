from database import get_db_connection
from datetime import datetime
from utils import get_numeric_input, get_non_empty_input, get_date_input

class BudgetManager:
    def __init__(self, user_id):
        self.user_id = user_id
    
    def set_budget(self):
        """Sets or updates a monthly budget for a category."""
        category = get_non_empty_input("Enter category to set budget for: ")
        month = get_date_input("Enter month (MM-YYYY): ", format="%m-%Y", error_msg="Invalid month. Please use MM-YYYY format.")
        if month is None: return
        amount = get_numeric_input("Enter budget amount: ", error_msg="Invalid amount. Please enter a number.")
        if amount is None:
            return

        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR REPLACE INTO budgets (user_id, category, month, amount) VALUES (?, ?, ?, ?)",
                (self.user_id, category, month, amount)
            )
            conn.commit()
            print(f"Budget of ₹{amount} set for '{category}' in {month}.")
        except Exception as e:
            print(f"Error setting budget: {e}")
        finally:
            conn.close()

    def check_budget_status(self):
        """Checks and reports on budget status for the current month."""
        current_month = datetime.now().strftime("%m-%Y")
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get total expenses per category for the current month
        cursor.execute("""
            SELECT category, SUM(amount) AS total_expense
            FROM transactions
            WHERE user_id = ? AND type = 'expense' AND date LIKE ?
            GROUP BY category
        """, (self.user_id, f'%-{current_month}'))
        expenses_by_category = {row['category']: row['total_expense'] for row in cursor.fetchall()}
        
        # Get all budgets for the current month
        cursor.execute("SELECT category, amount FROM budgets WHERE user_id = ? AND month = ?", (self.user_id, current_month))
        budgets = cursor.fetchall()
        
        conn.close()

        if not budgets:
            print("No budgets set for the current month.")
            return

        print(f"\n--- Budget Status for {current_month} ---")
        for budget in budgets:
            category = budget['category']
            budget_amount = budget['amount']
            spent_amount = expenses_by_category.get(category, 0)
            
            remaining = budget_amount - spent_amount
            status = "✅ On Track" if remaining >= 0 else "❌ Exceeded"
            
            print(f"Category: {category:<10} | Budget: ₹{budget_amount:,.2f} | Spent: ₹{spent_amount:,.2f} | Remaining: ₹{remaining:,.2f} | Status: {status}")
        print("-------------------------------------------\n")

    def check_and_notify_budget(self, category):
        """Checks if the budget for a given category has been exceeded for the current month."""
        current_month = datetime.now().strftime("%m-%Y")
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get total expense for category
        cursor.execute("""
            SELECT SUM(amount) AS total_expense
            FROM transactions
            WHERE user_id = ? AND type = 'expense' AND category = ? AND date LIKE ?
        """, (self.user_id, category, f'%-{current_month}'))
        total_expense = cursor.fetchone()['total_expense'] or 0
        
        # Get budget for category
        cursor.execute("SELECT amount FROM budgets WHERE user_id = ? AND category = ? AND month = ?", 
                       (self.user_id, category, current_month))
        budget_row = cursor.fetchone()
        
        conn.close()
        
        if budget_row:
            budget_amount = budget_row['amount']
            if total_expense > budget_amount:
                print(f"\n⚠️  ALERT: You have exceeded your budget for '{category}'!")
                print(f"Budget: ₹{budget_amount:,.2f} | Total Spent: ₹{total_expense:,.2f} | Over by: ₹{total_expense - budget_amount:,.2f}")
            elif total_expense >= budget_amount * 0.9:
                print(f"\n⚠️  WARNING: You have reached 90% of your budget for '{category}'.")
                print(f"Budget: ₹{budget_amount:,.2f} | Total Spent: ₹{total_expense:,.2f}")