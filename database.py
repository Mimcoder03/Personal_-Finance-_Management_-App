import sqlite3
import os

DATABASE_NAME = 'finance_app.db'

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row  # This allows accessing columns by name
    return conn

def create_tables():
    """Creates the necessary tables in the database if they don't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # User table for authentication
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    # Transactions table for income and expenses
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            type TEXT NOT NULL CHECK(type IN ('income', 'expense')),
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Budgets table to set monthly limits
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            month TEXT NOT NULL,
            UNIQUE(user_id, category, month),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()

def backup_database():
    """Creates a backup of the database file."""
    if not os.path.exists(DATABASE_NAME):
        print("No database to back up.")
        return
    backup_file = f"{DATABASE_NAME}.bak"
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        bck = sqlite3.connect(backup_file)
        with bck:
            conn.backup(bck)
        print(f"Database backed up to {backup_file}.")
    except Exception as e:
        print(f"Error backing up database: {e}")
    finally:
        conn.close()
        bck.close()

def restore_database():
    """Restores the database from a backup file."""
    backup_file = f"{DATABASE_NAME}.bak"
    if not os.path.exists(backup_file):
        print("No backup file found to restore.")
        return
    
    try:
        os.remove(DATABASE_NAME)
        conn = sqlite3.connect(DATABASE_NAME)
        bck = sqlite3.connect(backup_file)
        with conn:
            bck.backup(conn)
        print("Database restored from backup.")
    except Exception as e:
        print(f"Error restoring database: {e}")
    finally:
        conn.close()
        bck.close()