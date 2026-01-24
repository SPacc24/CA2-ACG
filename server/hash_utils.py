# Member 3 - Server Side
# This file handles SHA-256 hashing of received files

from cryptography.hazmat.primitives import hashes

def hash_file(file_path):
    # Create SHA-256 hash object
    digest = hashes.Hash(hashes.SHA256())

    # Read file and update hash
    with open(file_path, "rb") as file:
        digest.update(file.read())

    # Return final hash value
    return digest.finalize()
