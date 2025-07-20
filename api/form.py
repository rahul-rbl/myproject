from http.server import BaseHTTPRequestHandler
import json
import os
from .utils import decrypt_message, send_to_telegram

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        raw_data = self.rfile.read(content_length)
        
        try:
            # Verify request signature
            if os.environ.get('REQUEST_SECRET') != self.headers.get('X-Auth-Key'):
                raise PermissionError("Invalid authentication")
                
            data = json.loads(raw_data)
            decrypted = decrypt_message(data['encrypted'])
            send_to_telegram(decrypted.decode())
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode())
            
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
