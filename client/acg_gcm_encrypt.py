from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes

def encrypt(data):
    key = get_random_bytes(32)
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return key, cipher.nonce, ciphertext, tag
