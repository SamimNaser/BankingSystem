import os

try:
    import mysql.connector
except ModuleNotFoundError as exc:
    mysql = None
    MYSQL_IMPORT_ERROR = exc
else:
    MYSQL_IMPORT_ERROR = None


DB_CONFIG = {
    "host": os.getenv("BANKING_DB_HOST", "localhost"),
    "user": os.getenv("BANKING_DB_USER", "root"),
    "password": os.getenv("BANKING_DB_PASSWORD", ""),
}
DB_NAME = os.getenv("BANKING_DB_NAME", "banking_db")


def ensure_schema(cursor):
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS accounts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            balance DECIMAL(12,2) DEFAULT 0.00,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS transactions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            account_id INT NOT NULL,
            type VARCHAR(30) NOT NULL,
            amount DECIMAL(12,2) NOT NULL,
            description VARCHAR(255) NULL,
            reference_account_id INT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE
        )
        """
    )

    _ensure_column(
        cursor,
        "accounts",
        "created_at",
        "ALTER TABLE accounts ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
    )
    _ensure_column(
        cursor,
        "transactions",
        "description",
        "ALTER TABLE transactions ADD COLUMN description VARCHAR(255) NULL",
    )
    _ensure_column(
        cursor,
        "transactions",
        "reference_account_id",
        "ALTER TABLE transactions ADD COLUMN reference_account_id INT NULL",
    )


def _ensure_column(cursor, table_name, column_name, alter_statement):
    cursor.execute(f"SHOW COLUMNS FROM {table_name} LIKE %s", (column_name,))
    column = cursor.fetchone()
    if column is None:
        cursor.execute(alter_statement)


def connection():
    if MYSQL_IMPORT_ERROR is not None:
        raise RuntimeError(
            "MySQL connector is not installed. Install it with: "
            "pip install -r requirements.txt"
        ) from MYSQL_IMPORT_ERROR

    mydb = mysql.connector.connect(**DB_CONFIG)
    cursor = mydb.cursor(dictionary=True)

    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    cursor.execute(f"USE {DB_NAME}")
    ensure_schema(cursor)

    return mydb, cursor
