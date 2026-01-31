from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag


def decrypt_gcm(key, nonce, ciphertext_with_tag, aad):

    print(f"\n--- AES-GCM Decryption (Server Side) ---")
    
    aesgcm = AESGCM(key)

    try:
        plaintext = aesgcm.decrypt(
            nonce,
            ciphertext_with_tag,
            aad
        )

        # ADDED LOG LINE:
        print("[SUCCESS] AES-GCM authentication tag verified. File decrypted successfully.")
        
        return plaintext

    except InvalidTag:
        raise Exception("AES-GCM decryption failed: integrity check failed")