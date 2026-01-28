import sqlite3
import os
import hashlib

DB_PATH = "./website/services/database.db"


# ===============================
# Database Connection
# ===============================
def get_db():
    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.row_factory = sqlite3.Row
    return conn


# ===============================
# Initialize Database
# ===============================
def init_db():
    conn = get_db()
    c = conn.cursor()

    # ===============================
    # Users Table (with roles)
    # ===============================
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL
    )
    """)

    # ===============================
    # Files Table (ENCRYPTED AT REST)
    # ===============================
    c.execute("""
    CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        encrypted_data BLOB NOT NULL,
        nonce BLOB NOT NULL,
        encrypted_key BLOB NOT NULL,
        file_hash BLOB NOT NULL,
        signature BLOB NOT NULL,
        uploaded_by TEXT NOT NULL
    )
    """)

    # ===============================
    # Default Users
    # ===============================
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    c.execute("""
    INSERT OR IGNORE INTO users (username, password_hash, role)
    VALUES (?, ?, ?)
    """, ("admin", hash_password("admin123"), "admin"))

    c.execute("""
    INSERT OR IGNORE INTO users (username, password_hash, role)
    VALUES (?, ?, ?)
    """, ("user1", hash_password("user123"), "user"))

    c.execute("""
    INSERT OR IGNORE INTO users (username, password_hash, role)
    VALUES (?, ?, ?)
    """, ("user2", hash_password("user123"), "user"))

    conn.commit()
    conn.close()


# ===============================
# User Authentication
# ===============================
def verify_user(username, password):
    conn = get_db()
    c = conn.cursor()

    password_hash = hashlib.sha256(password.encode()).hexdigest()

    c.execute("""
        SELECT * FROM users
        WHERE username=? AND password_hash=?
    """, (username, password_hash))

    user = c.fetchone()
    conn.close()
    return user


def get_user_role(username):
    conn = get_db()
    c = conn.cursor()

    c.execute("SELECT role FROM users WHERE username=?", (username,))
    row = c.fetchone()

    conn.close()
    return row["role"] if row else None


# ===============================
# File Operations
# ===============================
def save_file(
    filename,
    encrypted_data,
    nonce,
    encrypted_key,
    file_hash,
    signature,
    uploaded_by
):
    conn = get_db()
    c = conn.cursor()

    c.execute("""
        INSERT INTO files (
            filename,
            encrypted_data,
            nonce,
            encrypted_key,
            file_hash,
            signature,
            uploaded_by
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        filename,
        encrypted_data,
        nonce,
        encrypted_key,
        file_hash,
        signature,
        uploaded_by
    ))

    conn.commit()
    conn.close()


def get_all_files():
    conn = get_db()
    c = conn.cursor()

    c.execute("""
        SELECT id, filename, uploaded_by
        FROM files
    """)

    rows = c.fetchall()
    conn.close()
    return rows


def get_file_by_id(file_id):
    conn = get_db()
    c = conn.cursor()

    c.execute("""
        SELECT *
        FROM files
        WHERE id=?
    """, (file_id,))

    file = c.fetchone()
    conn.close()
    return file
