from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes

def encrypt_aes_key(aes_key, public_key_path):
    with open(public_key_path, "rb") as key_file:
        # load server public key
        public_key = serialization.load_pem_public_key(key_file.read())
    # encrypt aes key using RSA-OAEP
    return public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
