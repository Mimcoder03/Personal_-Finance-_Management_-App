
"""
unit_tests.py

Comprehensive unit tests for the Personal Finance Management App.
"""

import unittest
from unittest.mock import patch, MagicMock
import sqlite3
import io
from datetime import datetime

# Import core modules
import database
from user_manager import UserManager
from transaction_manager import TransactionManager
from budget_manager import BudgetManager
from report_generator import ReportGenerator

class ConnectionWrapper:
    """Delegates to a real sqlite3.Connection but ignores close()."""
    def __init__(self, conn):
        self._conn = conn
    def __getattr__(self, name):
        return getattr(self._conn, name)
    def close(self):
        # Ignore close() during tests
        pass

def get_test_db_connection():
    """Returns a fresh in-memory connection wrapper with tables created."""
    conn = sqlite3.connect(':memory:')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)")
    cursor.execute("""
        CREATE TABLE transactions (
            id INTEGER PRIMARY KEY, 
            user_id INTEGER, 
            type TEXT, 
            category TEXT, 
            amount REAL, 
            date TEXT, 
            description TEXT
        )
    """)
    cursor.execute("CREATE TABLE budgets (id INTEGER PRIMARY KEY, user_id INTEGER, category TEXT, amount REAL, month TEXT, UNIQUE(user_id, category, month))")
    conn.commit()
    return ConnectionWrapper(conn)

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.wrapper = get_test_db_connection()
        self.conn = self.wrapper._conn
        
        self.patchers = [
            patch('user_manager.get_db_connection', return_value=self.wrapper),
            patch('transaction_manager.get_db_connection', return_value=self.wrapper),
            patch('budget_manager.get_db_connection', return_value=self.wrapper),
            patch('report_generator.get_db_connection', return_value=self.wrapper),
            patch('database.get_db_connection', return_value=self.wrapper)
        ]
        for p in self.patchers:
            p.start()

    def tearDown(self):
        patch.stopall()
        # Real close of the underlying connection
        self.conn.close()

class TestUserManager(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.um = UserManager()

    @patch('builtins.input', return_value='testuser')
    @patch('getpass.getpass', return_value='pass123')
    def test_register_user_success(self, mock_getpass, mock_input):
        result = self.um.register_user()
        self.assertTrue(result)
        
        row = self.conn.execute("SELECT * FROM users WHERE username = 'testuser'").fetchone()
        self.assertIsNotNone(row)

    @patch('builtins.input', side_effect=['testuser', 'testuser'])
    @patch('getpass.getpass', return_value='pass123')
    def test_register_user_duplicate(self, mock_getpass, mock_input):
        self.um.register_user()
        result = self.um.register_user()
        self.assertFalse(result)

    @patch('builtins.input', return_value='testuser')
    @patch('getpass.getpass', return_value='pass123')
    def test_login_user_success(self, mock_getpass, mock_input):
        hp = self.um._hash_password('pass123')
        self.conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('testuser', hp))
        self.conn.commit()
        
        uid = self.um.login_user()
        self.assertEqual(uid, 1)

class TestTransactionManager(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.tm = TransactionManager(user_id=1)

    @patch('builtins.input', side_effect=['Food', '10.5', 'Lunch'])
    def test_add_transaction(self, mock_input):
        self.tm.add_transaction('expense')
        row = self.conn.execute("SELECT * FROM transactions WHERE user_id = 1").fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row['amount'], 10.5)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_view_transactions(self, mock_stdout):
        self.conn.execute("INSERT INTO transactions (user_id, type, category, amount, date, description) VALUES (1, 'expense', 'Food', 5.0, '2023-10-27', 'Coffee')")
        self.conn.commit()
        
        self.tm.view_transactions()
        output = mock_stdout.getvalue()
        self.assertIn('Coffee', output)

    @patch('builtins.input', side_effect=['1', 'Groceries', '15.0', 'Weekly'])
    def test_update_transaction(self, mock_input):
        self.conn.execute("INSERT INTO transactions (id, user_id, type, category, amount, date, description) VALUES (1, 1, 'expense', 'Food', 5.0, '2023-10-27', 'Coffee')")
        self.conn.commit()
        
        self.tm.update_transaction()
        row = self.conn.execute("SELECT category FROM transactions WHERE id = 1").fetchone()
        self.assertEqual(row['category'], 'Groceries')

    @patch('builtins.input', side_effect=['1'])
    def test_delete_transaction(self, mock_input):
        self.conn.execute("INSERT INTO transactions (id, user_id, type, category, amount, date, description) VALUES (1, 1, 'expense', 'Food', 5.0, '2023-10-27', 'Coffee')")
        self.conn.commit()
        
        self.tm.delete_transaction()
        row = self.conn.execute("SELECT * FROM transactions WHERE id = 1").fetchone()
        self.assertIsNone(row)

class TestBudgetManager(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.bm = BudgetManager(user_id=1)

    @patch('builtins.input', side_effect=['Food', '2023-10', '500'])
    def test_set_budget(self, mock_input):
        self.bm.set_budget()
        row = self.conn.execute("SELECT amount FROM budgets WHERE user_id = 1 AND category = 'Food'").fetchone()
        self.assertEqual(row['amount'], 500.0)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_check_budget_status(self, mock_stdout):
        cm = datetime.now().strftime("%Y-%m")
        self.conn.execute("INSERT INTO budgets (user_id, category, month, amount) VALUES (1, 'Food', ?, 500.0)", (cm,))
        self.conn.execute("INSERT INTO transactions (user_id, type, category, amount, date, description) VALUES (1, 'expense', 'Food', 200.0, ?, 'Lunch')", (f"{cm}-01",))
        self.conn.commit()
        
        self.bm.check_budget_status()
        output = mock_stdout.getvalue()
        self.assertIn('On Track', output)

class TestReportGenerator(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.rg = ReportGenerator(user_id=1)

    @patch('builtins.input', side_effect=['2023-10'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_get_financial_summary_monthly(self, mock_stdout, mock_input):
        self.conn.execute("INSERT INTO transactions (user_id, type, category, amount, date, description) VALUES (1, 'income', 'Salary', 1000.0, '2023-10-01', 'S')")
        self.conn.execute("INSERT INTO transactions (user_id, type, category, amount, date, description) VALUES (1, 'expense', 'Rent', 400.0, '2023-10-05', 'R')")
        self.conn.commit()
        
        self.rg.get_financial_summary('monthly')
        output = mock_stdout.getvalue()
        self.assertIn('Income:  ₹1,000.00', output)
        self.assertIn('Expenses: ₹400.00', output)

if __name__ == '__main__':
    unittest.main()






