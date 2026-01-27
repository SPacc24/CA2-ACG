from flask import (
    Flask, request, render_template,
    redirect, session, url_for, send_file
)
import io

from website.services.db import (
    verify_user,
    init_db,
    save_file,
    get_all_files,
    get_file_by_id
)

# === CLIENT SIDE CRYPTO (simulated) ===
from client.aes_gcm_encrypt import encrypt_gcm
from client.rsa_key_exchange import encrypt_aes_key
from client.digital_signature import sign_file

# === SERVER SIDE CRYPTO ===
from server.server_rsa_key_exchange import decrypt_aes_key
from server.aes_gcm_decrypt import decrypt_gcm
from server.digital_signature import verify_file

# ===============================
# Database Init
# ===============================
init_db()

# ===============================
# Flask App Setup
# ===============================
app = Flask(
    __name__,
    template_folder="website/templates",
    static_folder="website/static"
)

app.secret_key = "ca2-secret"

# ===============================
# Routes
# ===============================

@app.route("/")
def home():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    if verify_user(username, password):
        session["user"] = username
        return redirect(url_for("upload"))

    return "❌ Login failed", 401


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if "user" not in session:
        return redirect("/")

    if request.method == "POST":
        uploaded_file = request.files["file"]
        file_bytes = uploaded_file.read()

        # ===============================
        # 🔐 CLIENT SIDE
        # ===============================
        aes_key, nonce, ciphertext = encrypt_gcm(
            file_bytes,
            aad=b"file-upload"
        )

        encrypted_aes_key = encrypt_aes_key(
            aes_key,
            "keys/server_public_key.pem"
        )

        signature = sign_file(
            file_bytes,
            "keys/client_private_key.pem"
        )

        # ===============================
        # 🔓 SERVER SIDE
        # ===============================
        decrypted_aes_key = decrypt_aes_key(
            encrypted_aes_key,
            "keys/server_private_key.pem"
        )

        plaintext = decrypt_gcm(
            decrypted_aes_key,
            nonce,
            ciphertext,
            aad=b"file-upload"
        )

        verify_file(
            plaintext,
            signature,
            "keys/client_public_key.pem"
        )

        # ===============================
        # 💾 STORE DECRYPTED FILE IN SQL
        # ===============================
        save_file(
            filename=uploaded_file.filename,
            filedata=plaintext,
            uploaded_by=session["user"]
        )

    files = get_all_files()
    return render_template("upload.html", files=files)


@app.route("/files")
def files():
    if "user" not in session:
        return redirect("/")

    if session["user"] != "admin":
        return "❌ Access denied", 403

    files = get_all_files()
    return render_template("upload.html", files=files)


@app.route("/files/download/<int:file_id>")
def download_file(file_id):
    if "user" not in session:
        return redirect("/")

    if session["user"] != "admin":
        return "❌ Access denied", 403

    file = get_file_by_id(file_id)
    if not file:
        return "File not found", 404

    return send_file(
        io.BytesIO(file["filedata"]),
        download_name=file["filename"],
        as_attachment=True
    )

@app.route("/files/view/<int:file_id>")
def view_file(file_id):
    if "user" not in session:
        return redirect("/")

    if session["user"] != "admin":
        return "❌ Access denied", 403

    file = get_file_by_id(file_id)
    if not file:
        return "File not found", 404

    return send_file(
        io.BytesIO(file["filedata"]),
        download_name=file["filename"],
        mimetype="application/octet-stream"
    )

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


# ===============================
# Runs
# ===============================
if __name__ == "__main__":
    app.run(debug=True)
