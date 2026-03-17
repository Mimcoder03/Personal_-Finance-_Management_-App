from database import get_db_connection
from datetime import datetime

class ReportGenerator:
    def __init__(self, user_id):
        self.user_id = user_id
    
    def get_financial_summary(self, period_type):
        """Generates a summary report for a given period (monthly or yearly)."""
        if period_type == 'monthly':
            period = input("Enter month to report (MM-YYYY): ").strip()
            if not period:
                period = datetime.now().strftime("%m-%Y")
            query_filter = f"%-{period}"
        elif period_type == 'yearly':
            period = input("Enter year to report (YYYY): ").strip()
            if not period:
                period = datetime.now().strftime("%Y")
            query_filter = f"%-{period}"
        else:
            print("Invalid period type.")
            return

        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get total income
        cursor.execute("SELECT SUM(amount) FROM transactions WHERE user_id = ? AND type = 'income' AND date LIKE ?",
                       (self.user_id, query_filter))
        total_income = cursor.fetchone()[0] or 0.0

        # Get total expenses
        cursor.execute("SELECT SUM(amount) FROM transactions WHERE user_id = ? AND type = 'expense' AND date LIKE ?",
                       (self.user_id, query_filter))
        total_expense = cursor.fetchone()[0] or 0.0
        
        conn.close()

        savings = total_income - total_expense

        print(f"\n--- Financial Report for {period} ---")
        print(f"Total Income:  ₹{total_income:,.2f}")
        print(f"Total Expenses: ₹{total_expense:,.2f}")
        print(f"Net Savings:   ₹{savings:,.2f}")
        print("--------------------------------------\n")