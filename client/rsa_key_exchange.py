from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KEYS_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "keys"))

def encrypt_key(aes_key, server_pub):
    pub_path = os.path.join(KEYS_DIR, server_pub)
    with open(pub_path, "rb") as f:
        pub = RSA.import_key(f.read())

    cipher = PKCS1_OAEP.new(pub)
    return cipher.encrypt(aes_key)
