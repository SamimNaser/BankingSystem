from pathlib import Path
import sys
from typing import TypedDict, cast


if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from connect_database import connection
    from helpers import (
        cleanup,
        connect_or_report,
        format_account_number,
        format_currency,
    )
else:
    from .connect_database import connection
    from .helpers import (
        cleanup,
        connect_or_report,
        format_account_number,
        format_currency,
    )


ADMIN_SECURITY_CODE = "1234"


class AccountSummary(TypedDict):
    id: int
    name: str
    balance: object


def _print_accounts_table(accounts: list[AccountSummary]):
    headers = ("ID", "Account Number", "Account Holder", "Balance")
    rows = [
        (
            str(account["id"]),
            format_account_number(account["id"]),
            account["name"],
            format_currency(account["balance"]),
        )
        for account in accounts
    ]

    column_widths = [
        max(len(header), *(len(row[index]) for row in rows))
        for index, header in enumerate(headers)
    ]

    divider = "+-" + "-+-".join("-" * width for width in column_widths) + "-+"
    header_row = "| " + " | ".join(
        header.ljust(column_widths[index]) for index, header in enumerate(headers)
    ) + " |"

    print(divider)
    print(header_row)
    print(divider)

    for row in rows:
        print(
            "| "
            + " | ".join(
                value.ljust(column_widths[index]) for index, value in enumerate(row)
            )
            + " |"
        )

    print(divider)


def administrator():
    entered_code = input("Enter administrator security code: ").strip()
    if entered_code != ADMIN_SECURITY_CODE:
        print("Invalid security code.")
        return

    mydb, cursor = connect_or_report(connection)
    if mydb is None or cursor is None:
        return

    cursor.execute(
        """
        SELECT id, name, balance
        FROM accounts
        ORDER BY id ASC
        """
    )
    accounts = cast(list[AccountSummary], cursor.fetchall())

    print("\n=== Administrator Account Overview ===")

    if not accounts:
        print("No bank accounts found.")
        cleanup(mydb, cursor)
        return

    _print_accounts_table(accounts)
    cleanup(mydb, cursor)


if __name__ == "__main__":
    administrator()
