# CA2-ACG: Secure File Transfer with Cryptography

A comprehensive client-server application demonstrating practical implementation of modern cryptographic techniques for secure file transfer, authentication, and data integrity verification.

## 🔐 Features

- **RSA Key Exchange**: Secure asymmetric encryption for AES key distribution
- **AES-GCM Encryption**: Authenticated encryption for file confidentiality
- **Digital Signatures**: ECDSA/RSA-based signatures for non-repudiation and authenticity
- **Hash Utilities**: Cryptographic hashing for data integrity
- **Web Interface**: Flask-based web application with user authentication
- **Client-Server Architecture**: Dual implementations for CLI and web-based file uploads

## 📁 Project Structure

```
CA2-ACG/
├── app.py                          # Flask web application (main entry point)
├── client/                         # Client-side cryptographic operations
│   ├── client_main.py             # CLI client for secure file upload
│   ├── aes_gcm_encrypt.py         # AES-GCM encryption
│   ├── rsa_key_exchange.py        # RSA public key encryption
│   ├── digital_signature.py       # Digital signature generation
│   └── hash_utils.py              # Hashing utilities
├── server/                         # Server-side cryptographic operations
│   ├── server_main.py             # CLI server for file processing
│   ├── aes_gcm_decrypt.py         # AES-GCM decryption
│   ├── server_rsa_key_exchange.py # RSA private key decryption
│   ├── digital_signature.py       # Signature verification
│   └── hash_utils.py              # Hashing utilities
├── keys/                           # Cryptographic key generation
│   └── keygen.py                  # RSA & ECDSA key generation script
├── website/                        # Web interface
│   ├── services/
│   │   └── db.py                  # User authentication database
│   ├── templates/
│   │   ├── login.html             # Login page
│   │   ├── upload.html            # File upload page
│   │   └── files.html             # Files listing page (admin)
│   └── static/
│       └── js/
│           ├── login.js           # Login script
│           └── upload.js          # Upload script
├── storage/
│   └── uploads/                   # Encrypted file storage
│       ├── file.enc               # Encrypted file
│       ├── file.sig               # Digital signature
│       ├── PGP.pptx.enc           # Example encrypted PPTX file
│       ├── PGP.pptx.enc.sig       # Corresponding signature
│       └── ...                    # Additional encrypted files
└── README.md
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Flask
- Cryptography libraries (pycryptodome, cryptography)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd CA2-ACG
   ```

2. **Generate cryptographic keys**
   ```bash
   python keys/keygen.py
   ```
   This generates RSA and ECDSA key pairs for both client and server.

3. **Install dependencies**
   ```bash
   pip install flask pycryptodome cryptography
   ```

## 💻 Usage

### Web Application
Start the Flask web server:
```bash
python app.py
```
Then navigate to `http://localhost:5000` and:
1. Login with your credentials
2. Upload a file - it will be encrypted client-side and verified server-side
3. Admin users can access the files listing to view and download all uploaded files

### CLI Client (File Upload)
Securely upload a file from command line:
```bash
python client/client_main.py <path-to-file>
```

### CLI Server (File Decryption)
Decrypt and verify uploaded files:
```bash
python server/server_main.py
```

## 🔑 Cryptographic Operations

### File Upload Flow

1. **Client-Side Encryption**
   - Generate random AES-256 key and nonce
   - Encrypt file with AES-GCM (provides both confidentiality and authenticity)
   - Encrypt AES key using server's RSA public key
   - Sign file with client's private key

2. **Server-Side Decryption**
   - Decrypt AES key using server's private RSA key
   - Decrypt file using recovered AES key
   - Verify digital signature using client's public key
   - Store encrypted artifacts in storage/uploads/

## 🛡️ Security Highlights

- **Confidentiality**: AES-256 GCM mode encryption
- **Authenticity**: Digital signatures and GCM authentication tag
- **Non-Repudiation**: RSA-based digital signatures
- **Key Security**: RSA-encrypted key distribution
- **Session Management**: Flask session-based authentication

## 📋 API Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Login page |
| `/login` | POST | User authentication |
| `/upload` | GET | Upload form |
| `/upload` | POST | File upload and encryption |
| `/files` | GET | Files listing |
| `/files/download/<filename>` | GET | Download file |
| `/logout` | GET | Logout |

## 📝 File Formats

- **Encrypted Upload**: `nonce (16 bytes) + tag (16 bytes) + ciphertext`
- **Encrypted Key**: RSA-encrypted AES key (variable length)
- **Signature**: Digital signature of original plaintext

## 🔧 Configuration

- **Flask Secret Key**: Set in `app.py` (change for production)
- **Upload Directory**: `storage/uploads/`
- **Key Directory**: `keys/`
- **Port**: 5000 (default Flask)

## ⚠️ Important Security Notes

This project is designed for educational purposes. For production use:
- Use environment variables for sensitive keys
- Implement proper key management and rotation
- Add HTTPS/TLS for transport security
- Implement rate limiting and input validation
- Use secure session management (e.g., Redis)
- Add comprehensive logging and monitoring
- Conduct security audits and penetration testing

## 📚 References

- [AES-GCM Documentation](https://en.wikipedia.org/wiki/Galois/Counter_Mode)
- [RSA Cryptography](https://en.wikipedia.org/wiki/RSA_(cryptosystem))
- [Digital Signatures](https://en.wikipedia.org/wiki/Digital_signature)
- [Flask Security Best Practices](https://flask.palletsprojects.com/en/2.0.x/security/)

## 📄 License

This project is provided for educational purposes.