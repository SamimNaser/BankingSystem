from pathlib import Path
import sys


if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from banking_system.account.create_account import create_account
from banking_system.account.view_account import view_account
from banking_system.account.delete_account import delete_account
from banking_system.administrator import administrator
from banking_system.connect_database import connection
from banking_system.helpers import cleanup
from banking_system.transactions.deposit import deposit
from banking_system.transactions.transaction_history import transaction_history
from banking_system.transactions.transfer import transfer
from banking_system.transactions.withdraw import withdraw


def initialize_application():
    try:
        mydb, cursor = connection()
    except Exception as error:
        print(f"Startup failed: {error}")
        print("Make sure MySQL is running and the database settings are correct.")
        return False

    mydb.commit()
    cleanup(mydb, cursor)
    return True

def menu():
    if not initialize_application():
        return

    while True:
        print("\n=== Banking System ===")
        print("1. Create Account")
        print("2. View Account")
        print("3. Deposit")
        print("4. Withdraw")
        print("5. Transfer Money")
        print("6. Transaction History")
        print("7. Delete Account")
        print("8. Administrator")
        print("9. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            create_account()
        elif choice == "2":
            view_account()
        elif choice == "3":
            deposit()
        elif choice == "4":
            withdraw()
        elif choice == "5":
            transfer()
        elif choice == "6":
            transaction_history()
        elif choice == "7":
            delete_account()
        elif choice == "8":
            administrator()
        elif choice == "9":
            print("Exiting...")
            break
        else:
            print("Invalid choice, try again")

if __name__ == "__main__":
    menu()
