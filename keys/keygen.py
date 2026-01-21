from Cryptodome.PublicKey import RSA
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def gen_keypair(name):
    key = RSA.generate(2048)

    with open(os.path.join(BASE_DIR, f"{name}_private.pem"), "wb") as f:
        f.write(key.export_key())

    with open(os.path.join(BASE_DIR, f"{name}_public.pem"), "wb") as f:
        f.write(key.publickey().export_key())

gen_keypair("server")
gen_keypair("client")

print("Keys generated inside keys/ folder.")
