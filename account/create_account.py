from ..connect_database import connection
from ..helpers import (
    cleanup,
    format_account_number,
    format_currency,
    prompt_amount,
    prompt_non_empty_text,
    record_transaction,
)

def create_account():
    mydb, cursor = connection()

    name = prompt_non_empty_text("Enter account holder name: ")
    if name is None:
        cleanup(mydb, cursor)
        return

    balance = prompt_amount("Enter initial balance: ", allow_zero=True)
    if balance is None:
        cleanup(mydb, cursor)
        return

    query = """
    INSERT INTO accounts (name, balance)
    VALUES (%s, %s)
    """

    cursor.execute(query, (name, balance))
    account_id = cursor.lastrowid

    if balance > 0:
        record_transaction(
            cursor,
            account_id,
            "opening_balance",
            balance,
            description="Initial account balance",
        )

    mydb.commit()

    print("Account created successfully")
    print(f"Account Number: {format_account_number(account_id)}")
    print(f"Opening Balance: {format_currency(balance)}")

    cleanup(mydb, cursor)
