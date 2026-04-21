# Banking System

A simple command-line banking system built with Python and MySQL.

## Features

- Create bank accounts with an opening balance
- View account details
- Deposit and withdraw money
- Transfer money between accounts
- View transaction history
- Delete accounts
- Administrator view to list all accounts and balances in a table

## Requirements

- Python 3
- MySQL Server
- `mysql-connector-python`

## Installation

1. Clone the repository:

```bash
git clone <your-repository-url>
cd banking_system
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set your database configuration:

```bash
export BANKING_DB_HOST=localhost
export BANKING_DB_USER=root
export BANKING_DB_PASSWORD=your_mysql_password
export BANKING_DB_NAME=banking_db
```

On Windows Command Prompt:

```cmd
set BANKING_DB_HOST=localhost
set BANKING_DB_USER=root
set BANKING_DB_PASSWORD=your_mysql_password
set BANKING_DB_NAME=banking_db
```

## Run the Project

```bash
python3 main.py
```

## Menu Options

1. Create Account
2. View Account
3. Deposit
4. Withdraw
5. Transfer Money
6. Transaction History
7. Delete Account
8. Administrator
9. Exit

## Administrator Access

The administrator feature is implemented in `administrator.py`.

- Default security code: `1234`
- After choosing `Administrator` from the menu, the system asks for the security code
- If the code is correct, all bank accounts and balances are shown in table format

You can change the code by editing this variable in `administrator.py`:

```python
ADMIN_SECURITY_CODE = "1234"
```

## Notes

- The database and tables are created automatically if they do not already exist.
- Make sure MySQL is running before starting the application.
