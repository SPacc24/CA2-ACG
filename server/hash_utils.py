""" # Member 3 - Server Side
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
 """
# client/hash_utils.py
# Utility functions for SHA-256 hashing
# i tried to add in reading from bytes based on your code
from cryptography.hazmat.primitives import hashes

def hash_bytes(data: bytes) -> bytes:
    """Hash raw bytes using SHA-256"""
    digest = hashes.Hash(hashes.SHA256())
    digest.update(data)
    return digest.finalize()


def hash_file(file_path: str) -> bytes:
    """Hash a file from disk using SHA-256"""
    with open(file_path, "rb") as f:
        return hash_bytes(f.read())
