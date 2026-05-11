import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "users.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)

    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        ("admin", "SecurePass123")
    )

    connection.commit()
    connection.close()


if __name__ == "__main__":
    init_database()
    print(f"Database initialized at: {DB_PATH}")
