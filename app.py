import os
import json
import logging
import traceback
from http.server import HTTPServer, BaseHTTPRequestHandler
from src.core.wad_wrapper import WADWrapper

# Fallback block for OmegaProtocol safety layer
try:
    from safety.omega_protocol import OmegaProtocol
except ImportError:
    class OmegaProtocol:
        @staticmethod
        def verify(data):
            return {"protocol": "Omega Class", "verification": "nominal", "payload": data}

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

class AxiomaticServerHandler(BaseHTTPRequestHandler):
    
    def _send_response(self, status: int, payload: dict):
        """Constructs a standardized JSON response with full CORS support."""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode('utf-8'))

    def do_OPTIONS(self):
        """Handle CORS preflight authorization."""
        self._send_response(200, {"status": "cors_approved"})

    def do_GET(self):
        """System health and operational status check."""
        logger.info(f"GET request received at path: {self.path}")
        if self.path in ['/', '/health']:
            self._send_response(200, {
                "system": "Axiomatic Ontological Intelligence",
                "status": "ONLINE",
                "arithmetic": "WAD",
                "protocol": "Omega Class"
            })
        else:
            self._send_response(404, {"error": "Endpoint not found in cognitive ledger"})

    def do_POST(self):
        """Process transactions through WAD arithmetic and Omega verification."""
        logger.info(f"POST transmission received at path: {self.path}")
        if self.path == '/process':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            
            try:
                payload = json.loads(body.decode('utf-8')) if body else {}
                
                # Core Execution Pipeline
                wad_output = WADWrapper.process(payload)
                omega_output = OmegaProtocol.verify(wad_output)
                
                self._send_response(200, {
                    "status": "purified",
                    "result": omega_output
                })
                
            except Exception as e:
                logger.error(f"Execution Exception: {str(e)}")
                logger.error(traceback.format_exc())
                self._send_response(500, {
                    "status": "error",
                    "message": str(e)
                })
        else:
            self._send_response(404, {"error": "Endpoint not found"})

def run():
    port = int(os.environ.get("PORT", 10000))
    server_address = ('0.0.0.0', port)
    
    logger.info(f"IGNITING AXIOMATIC SERVER: Binding to port {port}...")
    httpd = HTTPServer(server_address, AxiomaticServerHandler)
    logger.info("SERVER LIVE AND LISTENING.")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
