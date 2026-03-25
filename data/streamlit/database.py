import sqlite3
from datetime import datetime

DB_NAME = "results.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        score INTEGER,
        sentiment TEXT,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()


def insert_results(data):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for text, score, sentiment in data:
        c.execute(
            "INSERT INTO results (text, score, sentiment, timestamp) VALUES (?, ?, ?, ?)",
            (text, score, sentiment, current_time)
        )

    conn.commit()
    conn.close()


def fetch_results():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT * FROM results ORDER BY timestamp DESC")
    rows = c.fetchall()

    conn.close()
    return rows


def clear_database():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("DELETE FROM results")
    c.execute("DELETE FROM sqlite_sequence WHERE name='results'")

    conn.commit()
    conn.close()