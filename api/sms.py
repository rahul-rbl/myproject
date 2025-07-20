from http.server import BaseHTTPRequestHandler
import json
import os
from .utils import decrypt_message, send_to_telegram

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # 1. Validate request
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                return self.send_error(400, "Empty request")
                
            # 2. Verify security header
            if os.environ.get('REQUEST_SECRET') != self.headers.get('X-Auth-Key'):
                return self.send_error(401, "Unauthorized")
                
            # 3. Process request
            raw_data = self.rfile.read(content_length)
            data = json.loads(raw_data)
            
            # 4. Decrypt message
            decrypted = decrypt_message(data['encrypted'])
            
            # 5. Send to Telegram
            send_to_telegram(decrypted.decode())
            
            # 6. Respond with success
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "success",
                "message": "SMS forwarded to Telegram"
            }).encode())
            
        except Exception as e:
            self.send_error(500, f"Server error: {str(e)}")
