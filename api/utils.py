import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import requests

def decrypt_message(encrypted_data):
    # Get keys from environment
    SECRET_KEY = os.environ['SECRET_KEY'].encode()
    INIT_VECTOR = os.environ['INIT_VECTOR'].encode()
    
    # Decode base64
    encrypted_bytes = base64.b64decode(encrypted_data)
    
    # Setup cipher
    backend = default_backend()
    cipher = Cipher(algorithms.AES(SECRET_KEY), modes.CBC(INIT_VECTOR), backend=backend)
    decryptor = cipher.decryptor()
    
    # Decrypt and unpad
    decrypted_padded = decryptor.update(encrypted_bytes) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    return unpadder.update(decrypted_padded) + unpadder.finalize()

def send_to_telegram(message):
    bot_token = os.environ['TELEGRAM_BOT_TOKEN']
    chat_id = os.environ['TELEGRAM_CHAT_ID']
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload, timeout=10)
