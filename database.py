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
            category TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'incomplete'
            )
        """)

        rows = connection.execute("PRAGMA table_info(tasks)").fetchall()
        column_names = []

        for row in rows:
            column_names.append(row[1])

        if "due_date" not in column_names:
            connection.execute("""
                ALTER TABLE tasks ADD COLUMN due_date TEXT
            """)

    finally:
        connection.close()

def add_task(title, category):
    """Add a task to the database."""
    connection = sqlite3.connect(DATABASE_PATH)
    title = title.strip()

    if not title:
        raise ValueError("Enter task name.")

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

def get_tasks():
    """Return all tasks, returning the newest first."""
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    try:
        return connection.execute("""
            SELECT id, title, category, status
            FROM tasks
            ORDER BY id DESC
        """).fetchall()
    finally:
        connection.close()

def update_task(task_id, status):
    """Update the status of a task from incomplete to complete or vice versa."""
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        connection.execute("""
            UPDATE tasks
            SET status = ?
            WHERE id = ?
            """,
            (status, task_id)
        )
        connection.commit()
    finally:
        connection.close()