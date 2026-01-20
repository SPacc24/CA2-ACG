import sqlite3
import hashlib
import os
import json
from http.server import BaseHTTPRequestHandler

DB_PATH = "auth/users.db"

def hash_password(password: str, salt: str) -> str:
    return hashlib.sha256((password + salt).encode()).hexdigest()


class AuthHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        if self.path == "/login":
            self.handle_login()
        elif self.path == "/logout":
            self.handle_logout()
        else:
            self.send_error(404)

    def handle_login(self):
        content_length = int(self.headers["Content-Length"])
        body = self.rfile.read(content_length)
        data = json.loads(body)

        username = data.get("username")
        password = data.get("password")

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        cur.execute(
            "SELECT password_hash, salt FROM users WHERE username=?",
            (username,)
        )
        row = cur.fetchone()
        conn.close()

        if not row:
            self.respond(401, "Invalid username or password")
            return

        stored_hash, salt = row
        if hash_password(password, salt) != stored_hash:
            self.respond(401, "Invalid username or password")
            return

        # VERY SIMPLE session (acceptable for CA)
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Set-Cookie", "session=authenticated; HttpOnly")
        self.end_headers()
        self.wfile.write(json.dumps({"message": "Login successful"}).encode())

    def handle_logout(self):
        self.send_response(200)
        self.send_header("Set-Cookie", "session=; Max-Age=0")
        self.end_headers()

    def respond(self, code, message):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"message": message}).encode())
