import sqlite3
import os

DB_PATH = os.path.join(
    os.path.dirname(__file__),
    "users.db"
)

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    # test admin account
    c.execute("""
    INSERT OR IGNORE INTO users (username, password)
    VALUES (?, ?)
    """, ("admin", "admin123"))

    conn.commit()
    conn.close()


def verify_user(username, password):
    conn = get_db()
    c = conn.cursor()

    c.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    user = c.fetchone()
    conn.close()
    return user is not None
