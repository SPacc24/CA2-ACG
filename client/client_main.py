import sys
import os
from aes_gcm_encrypt import encrypt_gcm
from rsa_key_exchange import encrypt_aes_key
from digital_signature import sign_file

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STORAGE_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "storage", "uploads"))

os.makedirs(STORAGE_DIR, exist_ok=True)

file_path = sys.argv[1]
data = open(file_path, "rb").read()

aes_key, nonce, ciphertext, tag = encrypt_gcm(data)

enc_key = encrypt_aes_key(aes_key, "server_public.pem")
signature = sign_file(data, os.path.join(BASE_DIR, "..", "keys", "client_private.pem"))

with open(os.path.join(STORAGE_DIR, "upload.bin"), "wb") as f:
    f.write(nonce + tag + ciphertext)

with open(os.path.join(STORAGE_DIR, "key.bin"), "wb") as f:
    f.write(enc_key)

with open(os.path.join(STORAGE_DIR, "signature.bin"), "wb") as f:
    f.write(signature)

print("File uploaded securely.")

filename = request.files["file"].filename

with open(f"{UPLOAD_DIR}/{filename}.enc", "wb") as f:
    f.write(ciphertext)

with open(f"{UPLOAD_DIR}/{filename}.sig", "wb") as f:
    f.write(signature)

