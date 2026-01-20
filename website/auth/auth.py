from flask import Flask, request, jsonify
from werkzeug.security import check_password_hash
from website.services.db import get_db


app = Flask(__name__)

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute("SELECT * FROM users WHERE username=%s", (data["username"],))
    user = cur.fetchone()

    if not user or not check_password_hash(user["password"], data["password"]):
        return jsonify(success=False, message="Invalid credentials")

    return jsonify(success=True, message="Login successful")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
