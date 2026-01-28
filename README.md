# CA2-ACG: Secure File Transfer System

A practical implementation of end-to-end encrypted file transfer with digital signatures, demonstrating real-world cryptographic security patterns.

## Overview

This project implements a complete secure file transfer system combining:
- **AES-GCM** for encrypted file storage
- **RSA** for secure key distribution
- **Digital Signatures** for authenticity and non-repudiation
- **SHA-256** for integrity verification

## Quick Start

### Prerequisites
- Python 3.8+
- Required packages: `flask`, `pycryptodome`, `cryptography`

Install dependencies:
```bash
pip install flask pycryptodome cryptography
```

### Setup
```bash
# Generate cryptographic keys
python keys/keygen.py

# Run the web application
python app.py
```

Visit `http://localhost:5000` to access the web interface.

## Project Structure

```
CA2-ACG/
├── app.py                    # Flask web application
├── README.md
├── client/
│   ├── aes_gcm_encrypt.py   # File encryption
│   ├── rsa_key_exchange.py  # Key wrapping
│   ├── digital_signature.py # Signature generation
│   └── hash_utils.py        # Hashing
├── server/
│   ├── aes_gcm_decrypt.py   # File decryption
│   ├── server_rsa_key_exchange.py # Key unwrapping
│   ├── digital_signature.py # Signature verification
│   └── hash_utils.py        # Hashing
├── keys/
│   └── keygen.py            # Create RSA/ECDSA keys
└── website/
    ├── services/
    │   └── db.py            # Database & authentication
    ├── templates/
    │   ├── login.html
    │   └── upload.html
    └── static/
        └── js/
            ├── login.js
            └── upload.js
```

## How It Works

### File Upload
1. User selects file in web UI
2. **Client-side** (browser simulation):
   - Generate random AES-256 key + nonce
   - Encrypt file with AES-GCM
   - Wrap AES key with server's RSA public key
   - Sign with client's private key
3. **Server-side**:
   - Decrypt AES key using server's private RSA key
   - Decrypt file using recovered AES key
   - Verify signature with client's public key
   - Store encrypted artifacts

### File Download
1. Admin navigates to `/files`
2. Server decrypts selected file
3. Verifies integrity (hash) and authenticity (signature)
4. File sent to client

## Security Features

| Feature | Implementation |
|---------|-----------------|
| Confidentiality | AES-256-GCM encryption |
| Integrity | AES-GCM authentication tag + SHA-256 hash |
| Authenticity | RSA/ECDSA digital signatures |
| Key Exchange | RSA encrypted key distribution |
| Access Control | Session-based authentication & role-based access |

## API Routes

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Login page |
| `/login` | POST | Authenticate user |
| `/upload` | GET/POST | Upload encrypted file |
| `/files` | GET | View uploaded files (admin only) |
| `/files/download/<id>` | GET | Download decrypted file (admin only) |
| `/logout` | GET | End session |

## Configuration

The following settings are configured in `app.py`:
- **Port**: `5000` (Flask default)
- **Template Folder**: `website/templates/`
- **Static Folder**: `website/static/`
- **Database**: SQLite at `website/services/database.db` (auto-created on first run)

Default credentials (initialized automatically):
- Admin user: `admin` / `axxxxxxx`
- User: `hehe` / `yxxxxxxx`
- User: `acg` / `wxxxxx`

## References

- [AES-GCM](https://en.wikipedia.org/wiki/Galois/Counter_Mode)
- [RSA Encryption](https://en.wikipedia.org/wiki/RSA_(cryptosystem))
- [Digital Signatures](https://en.wikipedia.org/wiki/Digital_signature)
- [Flask Security](https://flask.palletsprojects.com/security/)
