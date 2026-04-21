from pathlib import Path
import sys


if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from banking_system.connect_database import connection
from banking_system.helpers import cleanup


def create_tables():
    mydb, cursor = connection()
    mydb.commit()
    print("Database and tables are ready.")
    cleanup(mydb, cursor)


if __name__ == "__main__":
    create_tables()
