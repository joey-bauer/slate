import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent / "data" / "slate.db"

def initialize_database():
    """Create slate's task table if it does not already exist."""
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)

    try:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            category TEXT NOT NULL
            )
        """)

    finally:
        connection.close()

def add_task(title, category):
    """Add a task to the database."""
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        connection.execute(
            """
            INSERT INTO tasks (title, category)
            VALUES (?, ?)
            """,
            (title, category)
        )
        connection.commit()
    finally:
        connection.close()
