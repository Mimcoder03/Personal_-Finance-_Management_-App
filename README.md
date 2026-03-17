# Personal Finance Management Application

## 👤 Author: SK Mimraj
### Project ID: UY6758GH

---

## 📝 Overview
The Personal Finance Management Application is a Python-based command-line tool that enables users to efficiently track and manage personal finances. The application supports secure user authentication, income and expense tracking, category-based budgeting with alerts, and automated financial reporting. Data is securely stored using SQLite with backup and restore support.

---
✨ Features:

User Authentication – Secure registration and login system

Transaction Management – Add, view, update, and delete income/expense records

Budget Tracking – Set monthly budgets with automatic limit alerts

Financial Reports – Generate monthly and yearly summaries of income, expenses, and savings

Data Persistence – SQLite database with backup and restore functionality

Unit Testing – Automated tests for authentication, transactions, budgets, and reports

---

Technology Stack:

Language: Python 3.8+

Database: SQLite3

Libraries: sqlite3, hashlib, getpass, datetime, unittest

---

## ⚙️ Installation

1. Install Python 3.x
2. Clone/download this repository
3. Navigate to the directory
4. Run the app: python main.py

---

## 🚀 Usage Instructions

### 1. Getting Started
When you first run the app, you will be prompted to either **Login** or **Register**.
- **Register**: Create a unique username and a secure password.
- **Login**: Enter your credentials to access your personal dashboard.

### 2. Managing Transactions
Once logged in, you can choose from the following menu options:
- **Add Income/Expense**: Enter the category (e.g., Salary, Food), the amount, and an optional description.
- **View Transactions**: See a formatted history of all your financial activities.
- **Update/Delete**: Correct or remove any previous entries using their unique Transaction ID.

### 3. Budgeting & Alerts
- **Set Monthly Budget**: Define how much you want to spend in a specific category (e.g., ₹5000 for "Rent").
- **Exceeding Limits**: The app will automatically notify you if an expense exceeds your set budget or if you reach 90% of your limit.
- **Check Budget Status**: Use this option to see a summary of your spending vs. budget for the current month.

### 4. Financial Reports
- **Monthly Report**: Get a summary of your total income, expenses, and net savings for any given month (YYYY-MM).
- **Yearly Report**: View your annual financial performance.

### 5. Data Safety
- **Backup Data**: Save a copy of your database to `finance_app.db.bak`.
- **Restore Data**: Recover your data from a previous backup if needed.

---

Future Enhancements:

GUI (Tkinter or Web dashboard)

Export reports (PDF/CSV)

Cloud database sync

AI spending insights

---

💻 Author
SK Mimraj - Passionate Python Developer & AI Enthusiast

Support
If you like this project, give it a star ⭐



