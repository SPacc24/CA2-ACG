from flask import Flask, request, render_template, redirect, session, url_for
from website.services.db import verify_user

# === CLIENT SIDE CRYPTO (simulated) ===
from client.acg_gcm_encrypt import encrypt
from client.rsa_key_exchange import encrypt_key
from client.digital_signature import sign

# === SERVER SIDE CRYPTO ===
from server.server_rsa_key_exchange import decrypt_key
from server.aes_gcm_decrypt import decrypt
from server.digital_signature import verify

import os

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

    # 🔐 CLIENT SIDE
    aes_key, nonce, ciphertext, tag = encrypt(file_bytes)

    encrypted_aes_key = encrypt_key(
        aes_key,"server_public.pem")
    

    signature = sign(
        file_bytes,
        "keys/client_private.pem"
    )

    # 🔓 SERVER SIDE
   # print("AES key match:", aes_key == decrypted_aes_key)

    decrypted_aes_key = decrypt_key(
        encrypted_aes_key,
        "server_private.pem"
    )

    plaintext = decrypt(
        decrypted_aes_key,
        nonce,
        ciphertext,
        tag
    )

    verify(
        plaintext,
        signature,
        "keys/client_public.pem"
    )

    # 💾 Store encrypted artefacts
    with open("storage/uploads/file.enc", "wb") as f:
        f.write(ciphertext)

    with open("storage/uploads/file.sig", "wb") as f:
        f.write(signature)

    return "✅ File uploaded, encrypted, and verified successfully"


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


# ===============================
# Run
# ===============================
if __name__ == "__main__":
    app.run(debug=True)
