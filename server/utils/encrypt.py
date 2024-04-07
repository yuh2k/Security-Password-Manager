import hashlib
import base64

def encrypt(input_string):
    # SHA-256 Hash
    hashed_bytes = hashlib.sha256(input_string.encode('utf-8')).digest()
    # Base64 encrypt
    encoded_string = base64.b64encode(hashed_bytes).decode('utf-8')
    return encoded_string
