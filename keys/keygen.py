from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import os
## how to run? python keygen.py
## should see: server_private_key.pem and server_public_key.pem

def generate_rsa_keys(name):
    # generate rsa private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    
    public_key = private_key.public_key()

    # filenames
    private_key_file = f"{name}_private_key.pem"
    public_key_file = f"{name}_public_key.pem"

    # save private key to file
    with open(private_key_file, "wb") as private_file:
        private_file.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )
    # save public key
    with open(public_key_file, "wb") as public_file:
        public_file.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )
        )

    print(f"{name.capitalize()} RSA key pair generated.")

if __name__ == "__main__":
    # make sure keys are generated in this folder
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    generate_rsa_keys("server")
    generate_rsa_keys("client")

    print("All keys generated inside keys/ folder.")

## I have put the code for client public key and server private key
## I changed the dir to be under keys folder also