from database import create_tables, backup_database, restore_database
from user_manager import UserManager
from transaction_manager import TransactionManager
from budget_manager import BudgetManager
from report_generator import ReportGenerator

def show_main_menu():
    """Displays the main menu options."""
    print("\n--- Personal Finance Management App ---")
    print("1. Add Income")
    print("2. Add Expense")
    print("3. View Transactions")
    print("4. Update a Transaction")
    print("5. Delete a Transaction")
    print("6. Set Monthly Budget")
    print("7. Check Budget Status (Current Month)")
    print("8. Generate Monthly Report")
    print("9. Generate Yearly Report")
    print("10. Back up Data")
    print("11. Restore Data")
    print("12. Logout")
    print("13. Exit")

def main():
    """Main function to run the application."""
    create_tables()
    user_manager = UserManager()
    current_user_id = None

    while True:
        if not current_user_id:
            print("\nWelcome! Please choose an option:")
            print("1. Login")
            print("2. Register")
            print("3. Exit")
            
            choice = input("> ").strip()
            if choice == '1':
                current_user_id = user_manager.login_user()
            elif choice == '2':
                user_manager.register_user()
            elif choice == '3':
                print("Exiting... Thank you.")
                break
            else:
                print("Invalid choice. Please try again.")
        else:
            transaction_manager = TransactionManager(current_user_id)
            budget_manager = BudgetManager(current_user_id)
            report_generator = ReportGenerator(current_user_id)
            
            show_main_menu()
            choice = input("> ").strip()

            if choice == '1':
                transaction_manager.add_transaction('income')
            elif choice == '2':
                transaction_manager.add_transaction('expense')
            elif choice == '3':
                transaction_manager.view_transactions()
            elif choice == '4':
                transaction_manager.update_transaction()
            elif choice == '5':
                transaction_manager.delete_transaction()
            elif choice == '6':
                budget_manager.set_budget()
            elif choice == '7':
                budget_manager.check_budget_status()
            elif choice == '8':
                report_generator.get_financial_summary('monthly')
            elif choice == '9':
                report_generator.get_financial_summary('yearly')
            elif choice == '10':
                backup_database()
            elif choice == '11':
                restore_database()
            elif choice == '12':
                print("Logged out successfully.")
                current_user_id = None
            elif choice == '13':
                print("Exiting... Thank you.")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

