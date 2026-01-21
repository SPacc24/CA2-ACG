from Cryptodome.Cipher import AES

def decrypt(key, nonce, tag, ciphertext):
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)
