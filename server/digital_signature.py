# Member 3 - Server Side
# This file verifies RSA digital signatures

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.utils import Prehashed
from server.hash_utils import hash_bytes,hash_file

def verify_file(file_bytes, signature, client_public_key_path):

    print(f"\n--- Digital Signature Verification (Server Side) ---")

    # Hash the file bytes
    file_hash = hash_bytes(file_bytes)

    # Load client's public key
    with open(client_public_key_path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read()
        )

    # Verify the digital signature
    try:
        public_key.verify(
            signature,
            file_hash,
            padding.PKCS1v15(),
            # Wrap SHA-256 has in Prehashed() to match the client
            Prehashed(hashes.SHA256())
        )

        print("[SUCCESS] Digital Signature Verified: The file author is authentic.")

        return True  # Signature is valid
    except InvalidSignature:
        print("[CRITICAL] Signature Mismatch. The file may have been tampered with or is not from the claimed sender.")
        return False  # Signature is invalid
