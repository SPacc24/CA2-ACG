# Member 3 - Client Side
# This file signs a file using RSA digital signature

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from hash import hash_file

def sign_file(file_path):
    # Hash the file using SHA-256
    file_hash = hash_file(file_path)

    # Load client's private key
    with open("client_private_key.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None
        )

    # Sign the file hash using private key
    signature = private_key.sign(
        file_hash,
        padding.PKCS1v15(),
        hashes.SHA256()
    )

    # Return the digital signature
    return signature
