import sqlite3
import os

DB_PATH = "./website/services/database.db"

def get_db():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    c = conn.cursor()

    # Users table
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    # Files table (DECRYPTED FILE STORED)
    c.execute("""
    CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        filedata BLOB,
        uploaded_by TEXT
    )
    """)

    # Default admin user
    c.execute("""
    INSERT OR IGNORE INTO users (username, password)
    VALUES ('admin', 'admin123')
    """)

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

def save_file(filename, filedata, uploaded_by):
    conn = get_db()
    c = conn.cursor()

    c.execute("""
        INSERT INTO files (filename, filedata, uploaded_by)
        VALUES (?, ?, ?)
    """, (filename, filedata, uploaded_by))

    conn.commit()
    conn.close()


def get_all_files():
    conn = get_db()
    c = conn.cursor()

    c.execute("SELECT id, filename, uploaded_by FROM files")
    rows = c.fetchall()

    conn.close()
    return rows


def get_file_by_id(file_id):
    conn = get_db()
    c = conn.cursor()

    c.execute("SELECT filename, filedata FROM files WHERE id=?", (file_id,))
    file = c.fetchone()

    conn.close()
    return file
