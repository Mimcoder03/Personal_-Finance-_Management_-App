from datetime import datetime

class User:
    """Represents a user of the application."""
    def __init__(self, user_id, username):
        self.id = user_id
        self.username = username

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"

class Transaction:
    """Represents a financial transaction (income or expense)."""
    def __init__(self, transaction_id, user_id, type, category, amount, date, description):
        self.id = transaction_id
        self.user_id = user_id
        self.type = type
        self.category = category
        self.amount = amount
        self.date = datetime.strptime(date, "%Y-%m-%d") if isinstance(date, str) else date
        self.description = description

    def __repr__(self):
        return f"<Transaction(id={self.id}, type='{self.type}', category='{self.category}', amount={self.amount})>"

class Budget:
    """Represents a monthly budget for a specific category."""
    def __init__(self, budget_id, user_id, category, amount, month):
        self.id = budget_id
        self.user_id = user_id
        self.category = category
        self.amount = amount
        self.month = datetime.strptime(month, "%Y-%m") if isinstance(month, str) else month

    def __repr__(self):
        return f"<Budget(id={self.id}, category='{self.category}', amount={self.amount}, month='{self.month.strftime('%Y-%m')}')>"