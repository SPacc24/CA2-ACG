import os
from aes_gcm_decrypt import decrypt_gcm
from server_rsa_key_exchange import decrypt_aes_key
from digital_signature import verify_file

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STORAGE_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "storage", "uploads"))
KEYS_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "keys"))

# Load files
with open(os.path.join(STORAGE_DIR, "upload.bin"), "rb") as f:
    enc = f.read()

nonce = enc[:16]
tag = enc[16:32]
ciphertext = enc[32:]

with open(os.path.join(STORAGE_DIR, "key.bin"), "rb") as f:
    enc_key = f.read()

with open(os.path.join(STORAGE_DIR, "signature.bin"), "rb") as f:
    signature = f.read()

# Decrypt AES key
aes_key = decrypt_aes_key(enc_key)

# Decrypt file
plaintext = decrypt_gcm(aes_key, nonce, tag, ciphertext)

# Verify signature
client_pub = os.path.join(KEYS_DIR, "client_public.pem")
verify_file(plaintext, signature, client_pub)

# Store decrypted file
with open(os.path.join(STORAGE_DIR, "decrypted.txt"), "wb") as f:
    f.write(plaintext)

filename = request.files["file"].filename

with open(f"{UPLOAD_DIR}/{filename}.enc", "wb") as f:
    f.write(ciphertext)

with open(f"{UPLOAD_DIR}/{filename}.sig", "wb") as f:
    f.write(signature)

print("File decrypted and verified successfully.")
