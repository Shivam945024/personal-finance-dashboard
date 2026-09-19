import sqlite3
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "finance.db"


def get_connection():
    DATA_DIR.mkdir(exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_date TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            transaction_type TEXT NOT NULL,
            amount REAL NOT NULL,
            payment_method TEXT,
            notes TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL UNIQUE,
            amount REAL NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def add_transaction(
    transaction_date,
    description,
    category,
    transaction_type,
    amount,
    payment_method,
    notes
):
    connection = get_connection()

    connection.execute(
        """
        INSERT INTO transactions
        (
            transaction_date,
            description,
            category,
            transaction_type,
            amount,
            payment_method,
            notes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            transaction_date,
            description,
            category,
            transaction_type,
            amount,
            payment_method,
            notes
        )
    )

    connection.commit()
    connection.close()


def get_transactions():
    connection = get_connection()

    query = """
        SELECT
            id,
            transaction_date,
            description,
            category,
            transaction_type,
            amount,
            payment_method,
            notes
        FROM transactions
        ORDER BY transaction_date DESC, id DESC
    """

    data = connection.execute(query).fetchall()
    connection.close()

    return [dict(row) for row in data]


def delete_transaction(transaction_id):
    connection = get_connection()

    connection.execute(
        "DELETE FROM transactions WHERE id = ?",
        (transaction_id,)
    )

    connection.commit()
    connection.close()


def save_budget(category, amount):
    connection = get_connection()

    connection.execute(
        """
        INSERT INTO budgets(category, amount)
        VALUES (?, ?)
        ON CONFLICT(category)
        DO UPDATE SET amount = excluded.amount
        """,
        (category, amount)
    )

    connection.commit()
    connection.close()


def get_budgets():
    connection = get_connection()

    data = connection.execute(
        "SELECT category, amount FROM budgets ORDER BY category"
    ).fetchall()

    connection.close()

    return [dict(row) for row in data]


def delete_budget(category):
    connection = get_connection()

    connection.execute(
        "DELETE FROM budgets WHERE category = ?",
        (category,)
    )

    connection.commit()
    connection.close()
