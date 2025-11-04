import os
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer
import subprocess

def run_celery():
    subprocess.call(["celery", "-A", "your_project", "worker", "--loglevel=info"])

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHTTPRequestHandler)
    print(f"Dummy server running on port {port}")
    server.serve_forever()

# Run Celery and the dummy server in parallel
threading.Thread(target=run_celery).start()
run_server()
