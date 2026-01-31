from inspect import signature
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

# === CLIENT SIDE CRYPTO (SIMULATED) ===
from client.aes_gcm_encrypt import encrypt_gcm
from client.rsa_key_exchange import encrypt_aes_key
from client.digital_signature import sign_file
from client.hash_utils import hash_bytes

# === SERVER SIDE CRYPTO ===
from server.server_rsa_key_exchange import decrypt_aes_key
from server.aes_gcm_decrypt import decrypt_gcm
from server.digital_signature import verify_file


# ===============================
# Init
# ===============================
init_db()

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

    user = verify_user(username, password)
    if user:
        session["user"] = username
        session["role"] = user["role"]
        return redirect(url_for("upload"))

    return "❌ Login failed", 401


# ===============================
# Upload (ALL USERS)
# ===============================
@app.route("/upload", methods=["GET", "POST"])
def upload():
    if "user" not in session:
        return redirect("/")

    if request.method == "POST":
        uploaded_file = request.files["file"]
        file_bytes = uploaded_file.read()

        # ===============================
        # 🔐 CLIENT SIDE (Simulated)
        # ===============================
        # 1. Sign the file (Authenticity & Integrity)
        signature = sign_file(
            file_bytes,
            "keys/client_private_key.pem"
        )

        signature = signature[0] if isinstance(signature, tuple) else signature

        # 2. Encrypt the file (Confidentiality)
        aes_key, nonce, encrypted_data = encrypt_gcm(
            file_bytes,
            aad=b"file-upload"
        )
        
        # 3. Encrypt the AES key for the server
        encrypted_key = encrypt_aes_key(
            aes_key,
            "keys/server_public_key.pem"
        )

        # 4. Hash the original file for a quick database check
        file_hash = hash_bytes(file_bytes)

        """
        print("\n=== UPLOAD CRYPTO PIPELINE ===")
        print("AES key (hex):", aes_key.hex())
        print("Nonce:", nonce.hex())
        print("Encrypted data (first 32 bytes):", encrypted_data[:32].hex())
        print("Encrypted AES key (RSA, first 64 bytes):", encrypted_key[:64])
        print("File hash:", file_hash.hex())
        print("Digital signature (first 64 bytes):", signature[:64])
        print("================================\n") 
        """
        # ===============================
        # 💾 STORE ONLY ENCRYPTED DATA
        # ===============================
        save_file(
            filename=uploaded_file.filename,
            encrypted_data=encrypted_data,
            nonce=nonce,
            encrypted_key=encrypted_key,
            file_hash=file_hash,
            signature=signature,
            uploaded_by=session["user"]
        )

    files = get_all_files()
    return render_template("upload.html", files=files)


# ===============================
# View Files (ADMIN ONLY)
# ===============================
@app.route("/files")
def files():
    if "user" not in session:
        return redirect("/")

    if session["role"] != "admin":
        return "❌ Access denied", 403
    files = get_all_files()
    return render_template("upload.html", files=files)


# ===============================
# Secure Download (ADMIN ONLY)
# ===============================
@app.route("/files/download/<int:file_id>")
def download_file(file_id):
    if "user" not in session:
        return redirect("/")

    if session["role"] != "admin":
        return "❌ Access denied", 403
    
    file = get_file_by_id(file_id)
    if not file:
        return "File not found", 404

    # ===============================
    # 🔓 SERVER SIDE DECRYPTION
    # ===============================
    aes_key = decrypt_aes_key(
        file["encrypted_key"],
        "keys/server_private_key.pem"
    )
    """
    print("Decrypted AES key (hex):", aes_key.hex())
    """

    plaintext = decrypt_gcm(
        aes_key,
        file["nonce"],
        file["encrypted_data"],
        aad=b"file-upload"
    )

    # ===============================
    # 🧪 INTEGRITY CHECK
    # ===============================
    recalculated_hash = hash_bytes(plaintext)
    stored_hash = file["file_hash"]

    print(f"\n--- Hash Comparison ---")
    print(f"Stored Hash:      {stored_hash.hex()}")
    print(f"Recalculated:     {recalculated_hash.hex()}")

    if recalculated_hash == stored_hash:
        print("Result: MATCH ✅")
    else:
        print("Result: MISMATCH ❌")
    print(f"-----------------------\n")
    # ===============================
    # ✍️ DIGITAL SIGNATURE VERIFICATION
    # ===============================
    verify_file(
        plaintext,
        file["signature"],
        "keys/client_public_key.pem"
    )
    
    print("Digital signature verified successfully")
    print("================================\n")

    # ===============================
    # 📤 SAFE FILE RELEASE
    # ===============================
    return send_file(
        io.BytesIO(plaintext),
        download_name=file["filename"],
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
