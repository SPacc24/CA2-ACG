import hashlib

def sha256_bytes(data: bytes) -> str:
    """
    Hash raw bytes using SHA-256
    """
    sha = hashlib.sha256()
    sha.update(data)
    return sha.hexdigest()


def sha256_file(file_path: str) -> str:
    """
    Hash a file using SHA-256
    """
    sha = hashlib.sha256()

    with open(file_path, "rb") as f:
        while chunk := f.read(4096):
            sha.update(chunk)

    return sha.hexdigest()
