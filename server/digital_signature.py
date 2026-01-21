from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15
from Cryptodome.Hash import SHA256

def verify(data, signature, public_key_path):
    with open(public_key_path, "rb") as f:
        key = RSA.import_key(f.read())

    h = SHA256.new(data)
    pkcs1_15.new(key).verify(h, signature)
