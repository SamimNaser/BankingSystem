from ..connect_database import connection
from ..helpers import cleanup, fetch_account, print_account_details, prompt_positive_int

def delete_account():
    mydb, cursor = connection()

    account_id = prompt_positive_int("Enter Account ID: ")
    if account_id is None:
        cleanup(mydb, cursor)
        return

    account = fetch_account(cursor, account_id)
    if not account:
        print("Account not found")
        cleanup(mydb, cursor)
        return

    print_account_details(account)
    confirmation = input("Delete this account permanently? (yes/no): ").strip().lower()
    if confirmation not in {"yes", "y"}:
        print("Account deletion cancelled.")
        cleanup(mydb, cursor)
        return

    delete_tx_query = """
    DELETE FROM transactions
    WHERE account_id = %s OR reference_account_id = %s
    """
    cursor.execute(delete_tx_query, (account_id, account_id))

    delete_acc_query = "DELETE FROM accounts WHERE id = %s"
    cursor.execute(delete_acc_query, (account_id,))

    mydb.commit()

    print("Account deleted successfully")

    cleanup(mydb, cursor)
