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


def transfer():
    mydb, cursor = connect_or_report(connection)
    if mydb is None or cursor is None:
        return

    sender_id = prompt_positive_int("Enter sender account ID: ")
    if sender_id is None:
        cleanup(mydb, cursor)
        return

    receiver_id = prompt_positive_int("Enter receiver account ID: ")
    if receiver_id is None:
        cleanup(mydb, cursor)
        return

    if sender_id == receiver_id:
        print("Sender and receiver account IDs must be different.")
        cleanup(mydb, cursor)
        return

    amount = prompt_amount("Enter transfer amount: ")
    if amount is None:
        cleanup(mydb, cursor)
        return

    sender = cast(AccountRow | None, fetch_account(cursor, sender_id))
    receiver = cast(AccountRow | None, fetch_account(cursor, receiver_id))

    if sender is None:
        print("Sender account not found.")
        cleanup(mydb, cursor)
        return

    if receiver is None:
        print("Receiver account not found.")
        cleanup(mydb, cursor)
        return

    if amount > sender["balance"]:
        print("Insufficient balance in sender account.")
        cleanup(mydb, cursor)
        return

    sender_new_balance = sender["balance"] - amount
    receiver_new_balance = receiver["balance"] + amount

    cursor.execute(
        """
        UPDATE accounts
        SET balance = %s
        WHERE id = %s
        """,
        (sender_new_balance, sender_id),
    )
    cursor.execute(
        """
        UPDATE accounts
        SET balance = %s
        WHERE id = %s
        """,
        (receiver_new_balance, receiver_id),
    )

    record_transaction(
        cursor,
        sender_id,
        "transfer_out",
        amount,
        description=f"Transferred to account {receiver_id}",
        reference_account_id=receiver_id,
    )
    record_transaction(
        cursor,
        receiver_id,
        "transfer_in",
        amount,
        description=f"Received from account {sender_id}",
        reference_account_id=sender_id,
    )
    mydb.commit()

    sender["balance"] = sender_new_balance
    receiver["balance"] = receiver_new_balance

    print("Transfer successful.")
    print(f"Transferred Amount: {format_currency(amount)}")
    print("\nSender account after transfer:")
    print_account_details(sender)
    print("\nReceiver account after transfer:")
    print_account_details(receiver)

    cleanup(mydb, cursor)


if __name__ == "__main__":
    transfer()
