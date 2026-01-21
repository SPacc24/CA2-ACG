from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KEYS_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "keys"))

def decrypt_key(encrypted_key, server_priv_filename):
    priv_path = os.path.join(KEYS_DIR, server_priv_filename)

    with open(priv_path, "rb") as f:
        priv = RSA.import_key(f.read())

    cipher = PKCS1_OAEP.new(priv)
    return cipher.decrypt(encrypted_key)
