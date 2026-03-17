import sqlite3
import sys

DATABASE_NAME = 'finance_app.db'

def inspect_db():
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        
        # List all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        with open('db_inspection_utf8.txt', 'w', encoding='utf-8') as f:
            f.write(f"Tables in {DATABASE_NAME}:\n")
            for table in tables:
                table_name = table[0]
                f.write(f"\n- Table: {table_name}\n")
                
                # Get schema
                cursor.execute(f"PRAGMA table_info({table_name});")
                columns = cursor.fetchall()
                f.write("  Columns:\n")
                for col in columns:
                    f.write(f"    - {col[1]} ({col[2]})\n")
                    
                # Get row count
                cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
                count = cursor.fetchone()[0]
                f.write(f"  Row count: {count}\n")
                
                # Get sample data (up to 5 rows)
                if count > 0:
                    cursor.execute(f"SELECT * FROM {table_name} LIMIT 5;")
                    rows = cursor.fetchall()
                    f.write("  Sample Data:\n")
                    for row in rows:
                        f.write(f"    {row}\n")
        
        conn.close()
    except Exception as e:
        with open('db_inspection_utf8.txt', 'w', encoding='utf-8') as f:
            f.write(f"Error: {e}\n")

if __name__ == "__main__":
    inspect_db()
