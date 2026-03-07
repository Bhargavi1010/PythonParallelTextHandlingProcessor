import sqlite3
import time


# CREATE DATABASE
def setup_db():

    conn = sqlite3.connect("project.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reviews(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        review TEXT,
        sentiment TEXT
    )
    """)

    conn.commit()
    conn.close()



# BULK INSERT DATA
def bulk_insert(data):

    conn = sqlite3.connect("project.db")

    cursor = conn.cursor()

    start = time.time()

    cursor.executemany(
        "INSERT INTO reviews (review, sentiment) VALUES (?,?)",
        data
    )

    conn.commit()

    end = time.time()

    conn.close()

    return end - start



# QUERY PERFORMANCE TEST
def query_test():

    conn = sqlite3.connect("project.db")

    cursor = conn.cursor()

    # Query before index
    start = time.time()

    cursor.execute("SELECT * FROM reviews WHERE sentiment='positive'")
    cursor.fetchall()

    end = time.time()

    before = end - start


    # Create index
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_sentiment ON reviews(sentiment)")
    conn.commit()


    # Query after index
    start = time.time()

    cursor.execute("SELECT * FROM reviews WHERE sentiment='positive'")
    cursor.fetchall()

    end = time.time()

    after = end - start

    conn.close()

    return before, after