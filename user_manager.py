import hashlib, sqlite3
from database import get_db_connection
from utils import get_non_empty_input

class UserManager:
    def __init__(self):
        pass

    def _hash_password(self, password):
        """Hashes a password for secure storage."""
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self):
        """Registers a new user."""
        username = get_non_empty_input("Enter a new username: ")
        password = get_non_empty_input("Enter a password: ", is_password=True)

        hashed_password = self._hash_password(password)
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            print(f"User '{username}' registered successfully.")
            return True
        except sqlite3.IntegrityError:
            print(f"Error: Username '{username}' already exists. Please choose a different one.")
            return False
        finally:
            conn.close()

    def login_user(self):
        """Authenticates a user."""
        username = get_non_empty_input("Enter your username: ")
        password = get_non_empty_input("Enter your password: ", is_password=True)
        hashed_password = self._hash_password(password)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, hashed_password))
        user_row = cursor.fetchone()
        conn.close()

        if user_row:
            print(f"User '{username}' logged in successfully.")
            return user_row['id']
        else:
            print("Invalid username or password.")
            return None
    