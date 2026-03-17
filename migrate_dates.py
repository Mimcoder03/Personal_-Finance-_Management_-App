import sqlite3
from datetime import datetime

DATABASE_NAME = 'finance_app.db'

def migrate():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    print("Starting date migration...")
    
    # Migrate transactions: YYYY-MM-DD -> DD-MM-YYYY
    cursor.execute("SELECT id, date FROM transactions")
    transactions = cursor.fetchall()
    updated_transactions = 0
    for trans_id, old_date in transactions:
        try:
            # Check if it needs migration
            date_obj = datetime.strptime(old_date, "%Y-%m-%d")
            new_date = date_obj.strftime("%d-%m-%Y")
            cursor.execute("UPDATE transactions SET date = ? WHERE id = ?", (new_date, trans_id))
            updated_transactions += 1
        except (ValueError, TypeError):
            # Already migrated or invalid format
            continue
            
    # Migrate budgets: YYYY-MM -> MM-YYYY
    cursor.execute("SELECT id, month FROM budgets")
    budgets = cursor.fetchall()
    updated_budgets = 0
    for budget_id, old_month in budgets:
        try:
            # Check if it needs migration
            date_obj = datetime.strptime(old_month, "%Y-%m")
            new_month = date_obj.strftime("%m-%Y")
            cursor.execute("UPDATE budgets SET month = ? WHERE id = ?", (new_month, budget_id))
            updated_budgets += 1
        except (ValueError, TypeError):
            # Already migrated or invalid format
            continue
            
    conn.commit()
    conn.close()
    
    print(f"Migration complete.")
    print(f"Transactions updated: {updated_transactions}")
    print(f"Budgets updated: {updated_budgets}")

if __name__ == "__main__":
    migrate()
