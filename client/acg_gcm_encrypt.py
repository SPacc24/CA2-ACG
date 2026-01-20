# To install: python -m pip install cryptography
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag
import os

def encrypt_gcm(data, aad):
    # 1. Generate a random 256-bit key
    # In a real app, you'd load this from a secure vault
    key = AESGCM.generate_key(bit_length=256)
    aesgcm = AESGCM(key)
    
    # 2. Generate a 96-bit (12-byte) Nonce
    # This is the "starting point" for the internal counter
    nonce = os.urandom(12)
    
    # 3. Encrypt and Authenticate
    # The library handles the CTR incrementing and GMAC tag creation
    ciphertext_with_tag = aesgcm.encrypt(nonce, data, aad)
    
    return key, nonce, ciphertext_with_tag

# Example Usage
secret_message = b"Standard CTR is good, but GCM is better!"
header_data = b"User-ID-123" # AAD: Authenticated but not encrypted

key, nonce, encrypted = encrypt_gcm(secret_message, header_data)

print(f"Nonce (Hex): {nonce.hex()}")
print(f"Encrypted (Hex): {encrypted.hex()}")

#Decryption
def decrypt_gcm(key, nonce, ciphertext_with_tag, aad):
    aesgcm = AESGCM(key)
    
    try:
        # The library automatically splits the last 16 bytes (the tag)
        # and verifies the integrity before decrypting.
        plaintext = aesgcm.decrypt(nonce, ciphertext_with_tag, aad)
        return plaintext.decode('utf-8')
    except InvalidTag:
        # This happens if the Key, Nonce, Ciphertext, or AAD are wrong/tampered with
        print("ALERT: Integrity check failed! The data has been altered or the key is wrong.")
        return None

# --- Testing the failure ---
# If we change just one letter in the header (AAD), GCM will detect it:
wrong_header = b"User-ID-999" 
result = decrypt_gcm(key, nonce, encrypted, wrong_header)
print(result)