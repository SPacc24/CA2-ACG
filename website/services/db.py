import sqlite3
import hashlib
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "../../users.db")


def get_db():
    return sqlite3.connect(DB_PATH)


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


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

    # demo user (only if not exists)
    c.execute("SELECT * FROM users WHERE username=?", ("admin",))
    if not c.fetchone():
        c.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            ("admin", hash_password("admin123"))
        )

    conn.commit()
    conn.close()


def verify_user(username, password):
    conn = get_db()
    c = conn.cursor()

    hashed = hash_password(password)
    c.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, hashed)
    )

    user = c.fetchone()
    conn.close()

    return user is not None
