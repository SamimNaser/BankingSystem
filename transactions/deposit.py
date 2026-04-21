from pathlib import Path
import sys
from decimal import Decimal
from typing import TypedDict, cast


if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from connect_database import connection
    from helpers import (
        cleanup,
        connect_or_report,
        fetch_account,
        format_currency,
        print_account_details,
        prompt_amount,
        prompt_positive_int,
        record_transaction,
    )
else:
    from ..connect_database import connection
    from ..helpers import (
        cleanup,
        connect_or_report,
        fetch_account,
        format_currency,
        print_account_details,
        prompt_amount,
        prompt_positive_int,
        record_transaction,
    )


class AccountRow(TypedDict):
    id: int
    name: str
    balance: Decimal
    created_at: object


def deposit():
    mydb, cursor = connect_or_report(connection)
    if mydb is None or cursor is None:
        return

    account_id = prompt_positive_int("Enter Account ID: ")
    if account_id is None:
        cleanup(mydb, cursor)
        return

    amount = prompt_amount("Enter deposit amount: ")
    if amount is None:
        cleanup(mydb, cursor)
        return

    account = cast(AccountRow | None, fetch_account(cursor, account_id))
    if account is None:
        print("Account not found")
        cleanup(mydb, cursor)
        return

    new_balance = account["balance"] + amount

    cursor.execute(
        """
        UPDATE accounts
        SET balance = %s
        WHERE id = %s
        """,
        (new_balance, account_id),
    )
    record_transaction(
        cursor,
        account_id,
        "deposit",
        amount,
        description="Cash deposit",
    )
    mydb.commit()

    account["balance"] = new_balance
    print("Deposit successful.")
    print(f"Deposited Amount: {format_currency(amount)}")
    print_account_details(account)

    cleanup(mydb, cursor)


if __name__ == "__main__":
    deposit()
