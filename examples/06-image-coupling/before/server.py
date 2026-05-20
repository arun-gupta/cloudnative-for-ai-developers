"""Coupled inference server -- source URL and credentials baked into the image.

The weights source URL and the credentials to fetch them are hardcoded constants.
Change the bucket, rotate the key, or switch from S3 to GCS:
you edit this file and rebuild the image.

In a real deployment these values end up in a Dockerfile as ENV instructions,
or in a .env file COPYed into the image. Either way they travel with the image:
cached in your registry, your CI system, and on every node that ever pulled it.
"""
import http.server
import socketserver
import shutil
import os
import time

# Source URL baked in. Change the bucket -> edit here -> rebuild the image.
WEIGHTS_SOURCE = os.path.join(os.path.dirname(__file__), "weights.txt")

# Credentials baked in. Rotate the key -> edit here -> rebuild the image.
# In a real image these show up in `docker history` and in the registry cache.
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

WEIGHTS_PATH = "/tmp/weights.txt"
PORT = 8080


def download_weights():
    print(f"[startup] Connecting to {WEIGHTS_SOURCE}")
    print(f"[startup] Using key: {AWS_ACCESS_KEY_ID} (hardcoded in this file)")
    start = time.time()
    shutil.copy(WEIGHTS_SOURCE, WEIGHTS_PATH)
    elapsed = time.time() - start
    print(f"[startup] Weights staged in {elapsed:.3f}s -> {WEIGHTS_PATH}")


def load_weights():
    with open(WEIGHTS_PATH) as f:
        return f.read().strip()


class InferenceHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"ok")
        elif self.path == "/predict":
            self.send_response(200)
            self.end_headers()
            response = f"prediction using model: [{self.server.model_weights[:60]}...]\n"
            self.wfile.write(response.encode())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        print(f"[request] {format % args}")


if __name__ == "__main__":
    download_weights()
    model_weights = load_weights()
    print(f"[startup] Model loaded. Preview: {model_weights[:60]}...")
    print(f"[startup] To change the source or rotate the key, edit this file and rebuild.")

    with socketserver.TCPServer(("", PORT), InferenceHandler) as httpd:
        httpd.model_weights = model_weights
        print(f"[ready] Inference server listening on port {PORT}")
        print(f"[ready]   GET /health  -> liveness check")
        print(f"[ready]   GET /predict -> simulated inference")
        httpd.serve_forever()
