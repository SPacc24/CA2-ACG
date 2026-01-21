from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KEYS_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "keys"))

def decrypt_key(enc_key):
    private_key_path = os.path.join(KEYS_DIR, "server_private.pem")

    with open(private_key_path, "rb") as f:
        key = RSA.import_key(f.read())

    cipher = PKCS1_OAEP.new(key)
    return cipher.decrypt(enc_key)
