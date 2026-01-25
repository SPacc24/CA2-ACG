from flask import Flask, request, render_template, redirect, session, url_for, send_from_directory
from website.services.db import verify_user

# === CLIENT SIDE CRYPTO (simulated) ===
from client.aes_gcm_encrypt import encrypt_gcm
from client.rsa_key_exchange import encrypt_aes_key
from client.digital_signature import sign_file

# === SERVER SIDE CRYPTO ===
from server.server_rsa_key_exchange import decrypt_aes_key
from server.aes_gcm_decrypt import decrypt_gcm
from server.digital_signature import verify_file

import os

# ====== Users DB Init ===============
from website.services.db import init_db

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

UPLOAD_DIR = "storage/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

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

    if request.method == "GET":
        return render_template("upload.html")

    file_bytes = request.files["file"].read()
    aad = session["user"].encode()

    aes_key, nonce, ciphertext_with_tag = encrypt_gcm(
        file_bytes,
        aad
    )

    encrypted_aes_key = encrypt_aes_key(
        aes_key,
        "keys/server_public_key.pem"
    )

    signature = sign_file(
        file_bytes,
        "keys/client_private_key.pem"
    )


    decrypted_aes_key = decrypt_aes_key(
        encrypted_aes_key,
        "keys/server_private_key.pem"
    )

    plaintext = decrypt_gcm(
        decrypted_aes_key,
        nonce,
        ciphertext_with_tag,
        aad
    )

    verify_file(
        plaintext,
        signature,
        "keys/client_public_key.pem"
    )


    # 💾 Store encrypted artefacts
    with open("storage/uploads/file.enc", "wb") as f:
        f.write(ciphertext_with_tag)

    with open("storage/uploads/file.sig", "wb") as f:
        f.write(signature)

    return "✅ File uploaded, encrypted, and verified successfully"

@app.route("/files")
def files():
    if "user" not in session:
        return redirect("/")

    # Only allow admin user
    if session["user"] != "admin":
        return "❌ Access denied", 403

    files = os.listdir(UPLOAD_DIR)

    file_info = []
    for f in files:
        path = os.path.join(UPLOAD_DIR, f)
        file_info.append({
            "name": f,
            "size": os.path.getsize(path)
        })

    return render_template(
        "files.html",
        files=file_info
    )

@app.route("/files/download/<filename>")
def download_file(filename):
    if "user" not in session:
        return redirect("/")

    if session["user"] != "admin":
        return "❌ Access denied", 403

    return send_from_directory(
        UPLOAD_DIR,
        filename,
        as_attachment=True
    )

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


# ===============================
# Run
# ===============================
if __name__ == "__main__":
    app.run(debug=True)
