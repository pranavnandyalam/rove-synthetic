import sqlite3
from pathlib import Path

DB_PATH = Path("flight_data.db")


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        origin TEXT,
        destination TEXT,
        departure_date TEXT,
        miles_available INTEGER,
        rating INTEGER,
        comments TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
        """
    )
    return conn


def insert_feedback(origin: str, destination: str, departure_date: str, miles_available: int, rating: int, comments: str):
    conn = get_conn()
    with conn:
        conn.execute(
            """
        INSERT INTO feedback (origin, destination, departure_date, miles_available, rating, comments)
        VALUES (?, ?, ?, ?, ?, ?)
            """,
            (origin, destination, departure_date, miles_available, rating, comments),
        )
    conn.close()

