from Cryptodome.Hash import SHA256

def sha256(data):
    return SHA256.new(data).digest()
