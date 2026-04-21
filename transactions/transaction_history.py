from pathlib import Path
import sys
from typing import TypedDict, cast


if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from connect_database import connection
    from helpers import (
        cleanup,
        connect_or_report,
        fetch_account,
        format_currency,
        prompt_positive_int,
    )
else:
    from ..connect_database import connection
    from ..helpers import (
        cleanup,
        connect_or_report,
        fetch_account,
        format_currency,
        prompt_positive_int,
    )


class AccountRow(TypedDict):
    id: int
    name: str
    balance: object
    created_at: object


class TransactionRow(TypedDict):
    type: str
    amount: object
    description: str | None
    reference_account_id: int | None
    date: object


def transaction_history():
    mydb, cursor = connect_or_report(connection)
    if mydb is None or cursor is None:
        return

    account_id = prompt_positive_int("Enter Account ID: ")
    if account_id is None:
        cleanup(mydb, cursor)
        return

    account = cast(AccountRow | None, fetch_account(cursor, account_id))
    if account is None:
        print("Account not found")
        cleanup(mydb, cursor)
        return

    cursor.execute(
        """
        SELECT type, amount, description, reference_account_id, date
        FROM transactions
        WHERE account_id = %s
        ORDER BY date DESC, id DESC
        """,
        (account_id,),
    )
    transactions = cast(list[TransactionRow], cursor.fetchall())

    print(f"\n=== Transaction History for Account {account_id} ===")
    print(f"Account Holder: {account['name']}")
    print(f"Current Balance: {format_currency(account['balance'])}")

    if not transactions:
        print("No transactions found for this account.")
        cleanup(mydb, cursor)
        return

    for index, transaction in enumerate(transactions, start=1):
        reference = ""
        if transaction["reference_account_id"] is not None:
            reference = f" | Related Account: {transaction['reference_account_id']}"

        description = ""
        if transaction["description"]:
            description = f" | Note: {transaction['description']}"

        print(
            f"{index}. {transaction['date']} | {transaction['type']} | "
            f"{format_currency(transaction['amount'])}{reference}{description}"
        )

    cleanup(mydb, cursor)


if __name__ == "__main__":
    transaction_history()
