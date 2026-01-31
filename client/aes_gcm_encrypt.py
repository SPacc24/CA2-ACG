# To install: python -m pip install cryptography
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag
import os

def encrypt_gcm(data, aad):
    
    print(f"\n--- AES-GCM Encryption (Client Side) ---")
    
    # 1. Generate a random 256-bit key
    key = AESGCM.generate_key(bit_length=256)
    aesgcm = AESGCM(key)
    
    # 2. Generate a 96-bit (12-byte) Nonce
    # This is the starting point for the internal counter
    nonce = os.urandom(12)
    
    # 3. Encrypt and Authenticate
    # The library handles the CTR incrementing and GMAC tag creation
    ciphertext_with_tag = aesgcm.encrypt(nonce, data, aad)

    # ADDED LOG LINE:
    print(f"[LOG] Cryptographic integrity check: File has been encrypted with AES-GCM (Nonce: {nonce.hex()[:8]}...)")
    
    return key, nonce, ciphertext_with_tag