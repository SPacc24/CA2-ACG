from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes

def encrypt_aes_key(aes_key, public_key_path):
    print(f"\n--- RSA Key Exchange (Client Side) ---")

    with open(public_key_path, "rb") as key_file:
        # load server public key
        public_key = serialization.load_pem_public_key(key_file.read())
    
    print(f"[LOG] Server Public Key loaded from: {public_key_path}")

    # encrypt aes key using RSA-OAEP
    encrypted_key = public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    print(f"[SUCCESS] AES Key has been encrypted with RSA-OAEP.")
    print(f"[LOG] Encrypted AES Key (first 16 bytes): {encrypted_key[:16].hex()}...")
        
    return encrypted_key
