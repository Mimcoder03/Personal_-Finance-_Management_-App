import sqlite3

DATABASE_NAME = 'finance_app.db'

def inspect_db():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    print("Database State after Migration:")
    
    # Check transactions
    cursor.execute("SELECT date FROM transactions LIMIT 5")
    print("\nSample Transaction Dates:")
    for row in cursor.fetchall():
        print(f"- {row[0]}")
        
    # Check budgets
    cursor.execute("SELECT month FROM budgets LIMIT 5")
    print("\nSample Budget Months:")
    for row in cursor.fetchall():
        print(f"- {row[0]}")
        
    conn.close()

if __name__ == "__main__":
    inspect_db()
