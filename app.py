import os
import json
import logging
import traceback
from http.server import HTTPServer, BaseHTTPRequestHandler

# Import your core logic modules
from src.core.wad_wrapper import wad_wrapper
from safety.omega_protocol import OmegaProtocol 

# Configure logging for maximum observability
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ComplianceServerHandler(BaseHTTPRequestHandler):
    
    def _send_json_response(self, status_code, data):
        """Constructs and sends a bulletproof JSON payload."""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        # Robust CORS headers to guarantee front-end connectivity
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        # The HTTP response body must be a valid bytestring
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def do_OPTIONS(self):
        """Intercept and approve CORS pre-flight checks instantly."""
        self._send_json_response(200, {"status": "ok"})

    def do_GET(self):
        """System health and state verification endpoint."""
        logger.info(f"GET request intercepted at path: {self.path}")
        if self.path == '/health' or self.path == '/':
            self._send_json_response(200, {
                "status": "100_PERCENT_ACTIVE", 
                "system": "Axiomatic Ontological Intelligence",
                "protocol": "Omega Class",
                "math_engine": "WAD_Arithmetic"
            })
        else:
            self._send_json_response(404, {"error": "Path unfound in cognitive ledger"})

    def do_POST(self):
        """Core processing pipeline for WAD logic and Omega purification."""
        logger.info(f"POST transmission received at: {self.path}")
        if self.path == '/process':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            
            # Wrapping critical execution logic in try/except blocks is a vital zero-dependency best practice
            try:
                payload = json.loads(body.decode('utf-8')) if body else {}
                logger.info(f"Input payload successfully parsed.")
                
                # --- WAD Arithmetic & Safety Execution ---
                logger.info("Routing payload through WADWrapper...")
                wad_result = WADWrapper.process(payload)
                
                logger.info("Executing OmegaProtocol purification sequence...")
                verified_state = OmegaProtocol.verify(wad_result)
                
                response_payload = {
                    "status": "purified",
                    "result": verified_state
                }
                
                logger.info("Execution flawless. Returning verified state to front-end.")
                self._send_json_response(200, response_payload)
                
            except Exception as e:
                # Capture and log the exact point of failure without crashing the server
                logger.error(f"Logic Execution Anomaly: {str(e)}")
                logger.error(traceback.format_exc())
                self._send_json_response(500, {
                    "status": "error",
                    "message": "Internal Logic Exception", 
                    "details": str(e)
                })
        else:
            self._send_json_response(404, {"error": "Endpoint not recognized by system"})

def run():
    # Dynamic port binding for seamless cloud deployment compatibility
    port = int(os.environ.get("PORT", 10000))
    server_address = ('0.0.0.0', port)
    
    logger.info(f"INITIATING BOOT SEQUENCE: Axiomatic Server binding to port {port}...")
    
    httpd = HTTPServer(server_address, ComplianceServerHandler)
    logger.info("SERVER IS LIVE. Awaiting deterministic input. LET'S GOOOO!")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
