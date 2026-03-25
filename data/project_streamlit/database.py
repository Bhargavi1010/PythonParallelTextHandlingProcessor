import sqlite3

DB_NAME = "results.db"

def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT,
            score INTEGER,
            sentiment TEXT
        )
    """)

    conn.commit()
    conn.close()

def insert_data(data):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.executemany("""
        INSERT INTO results (text, score, sentiment)
        VALUES (?, ?, ?)
    """, [(d["Text"], d["Score"], d["Sentiment"]) for d in data])

    conn.commit()
    conn.close()

def fetch_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT text, score, sentiment FROM results")
    rows = cursor.fetchall()

    conn.close()
    return rows

def clear_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM results")

    conn.commit()
    conn.close()