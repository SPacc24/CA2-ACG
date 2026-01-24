# Member 3 - Server Side
# This file verifies RSA digital signatures

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from hash import hash_file

def verify_file(file_path, signature):
    # Hash the received file using SHA-256
    file_hash = hash_file(file_path)

    # Load client's public key
    with open("client_public_key.pem", "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read()
        )

    # Verify the digital signature
    try:
        public_key.verify(
            signature,
            file_hash,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return True  # Signature is valid
    except:
        return False  # Signature is invalid
