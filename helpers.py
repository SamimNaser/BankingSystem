from decimal import Decimal, InvalidOperation


TWO_PLACES = Decimal("0.01")


def cleanup(mydb, cursor):
    cursor.close()
    mydb.close()


def connect_or_report(connection_func):
    try:
        return connection_func()
    except Exception as error:
        print(f"Database connection failed: {error}")
        print("Make sure MySQL is running and your database settings are correct.")
        return None, None


def prompt_non_empty_text(prompt):
    value = input(prompt).strip()
    if not value:
        print("This field cannot be empty.")
        return None
    return value


def prompt_positive_int(prompt):
    raw_value = input(prompt).strip()

    try:
        value = int(raw_value)
    except ValueError:
        print("Invalid input. Please enter a whole number.")
        return None

    if value <= 0:
        print("Value must be greater than zero.")
        return None

    return value


def prompt_amount(prompt, *, allow_zero=False):
    raw_value = input(prompt).strip()

    try:
        amount = Decimal(raw_value).quantize(TWO_PLACES)
    except (InvalidOperation, ValueError):
        print("Invalid amount.")
        return None

    if amount < 0 or (amount == 0 and not allow_zero):
        print("Amount must be greater than zero." if not allow_zero else "Amount cannot be negative.")
        return None

    return amount


def format_currency(amount):
    return f"{Decimal(amount):.2f}"


def format_account_number(account_id):
    return f"ACC{account_id:05d}"


def fetch_account(cursor, account_id):
    query = """
    SELECT id, name, balance, created_at
    FROM accounts
    WHERE id = %s
    """
    cursor.execute(query, (account_id,))
    return cursor.fetchone()


def print_account_details(account):
    print("\n=== Account Details ===")
    print(f"Account ID: {account['id']}")
    print(f"Account Number: {format_account_number(account['id'])}")
    print(f"Account Holder: {account['name']}")
    print(f"Balance: {format_currency(account['balance'])}")

    created_at = account.get("created_at")
    if created_at is not None:
        print(f"Created At: {created_at}")


def record_transaction(
    cursor,
    account_id,
    transaction_type,
    amount,
    *,
    description=None,
    reference_account_id=None,
):
    query = """
    INSERT INTO transactions (account_id, type, amount, description, reference_account_id)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(
        query,
        (account_id, transaction_type, amount, description, reference_account_id),
    )
