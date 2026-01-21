from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15
from Cryptodome.Hash import SHA256
import os

def sign(data, private_key_path):
    with open(private_key_path, "rb") as f:
        key = RSA.import_key(f.read())

    h = SHA256.new(data)
    return pkcs1_15.new(key).sign(h)
