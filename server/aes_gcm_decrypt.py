from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag


def decrypt_gcm(key, nonce, ciphertext_with_tag, aad):
    aesgcm = AESGCM(key)

    try:
        plaintext = aesgcm.decrypt(
            nonce,
            ciphertext_with_tag,
            aad
        )
        return plaintext

    except InvalidTag:
        raise Exception("AES-GCM decryption failed: integrity check failed")