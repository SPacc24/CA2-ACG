from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes

def decrypt_aes_key(encrypted_key, private_key_path):

    print(f"\n--- RSA Key Exchange (Server Side) ---")

    # load server private key 
    with open(private_key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None
        )

    print(f"[LOG] Server Private Key loaded. Attempting decryption...")

    # decrypt aes key using RSA-OAEP
    decrypted_aes_key = private_key.decrypt(
        encrypted_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    print(f"[SUCCESS] AES Key has been decrypted with RSA-OAEP.")
    print(f"[SUCCESS] RSA Decryption successful. Session AES key recovered.")
    # We print a snippet of the hex just to prove it matches the client's original key
    print(f"[LOG] Recovered AES Key (first 16 bytes): {decrypted_aes_key[:16].hex()}...")

    return decrypted_aes_key    
