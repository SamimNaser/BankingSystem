from ..connect_database import connection
from ..helpers import cleanup, fetch_account, print_account_details, prompt_positive_int

def view_account():
    mydb, cursor = connection()

    account_id = prompt_positive_int("Enter Account ID: ")
    if account_id is None:
        cleanup(mydb, cursor)
        return

    account = fetch_account(cursor, account_id)
    if account:
        print_account_details(account)
    else:
        print("Account not found")

    cleanup(mydb, cursor)
