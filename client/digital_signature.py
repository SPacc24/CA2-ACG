# Member 3 - Client Side
# This file generates a digital signature for uploaded files
# Digital signature ensures authenticity, integrity, and non-repudiation

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.utils import Prehashed
from cryptography.hazmat.primitives import hashes
from client.hash_utils import hash_bytes


def sign_file(file_bytes, private_key_path):

    print(f"\n--- Digital Signature Generation (Client Side) ---")
    
    """
    Signs the SHA-256 hash of a file using RSA private key.
    """

    # --------------------------------
    # Step 1: Hash file (Integrity)
    # --------------------------------
    file_hash = hash_bytes(file_bytes)  # SHA-256 digest (bytes)

    # --------------------------------
    # Step 2: Load private key
    # --------------------------------
    with open(private_key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None
        )

    # --------------------------------
    # Step 3: Sign the hash
    # --------------------------------
    signature = private_key.sign(
        file_hash,
        padding.PKCS1v15(),
        Prehashed(hashes.SHA256())
    )

    # ADDED LOG LINE:
    print(f"[LOG] Digital signature generated. Ready for AES-GCM encryption.")

    # --------------------------------
    # Step 4: Return signature + hash
    # --------------------------------
    return signature, file_hash