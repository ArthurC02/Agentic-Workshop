"""Probe this exact app on an OS-selected free port, terminating only our child."""
import json
import socket
import subprocess
import sys
import time
import urllib.request

from smart_ticket.main import app

with socket.socket() as socket_probe:
    socket_probe.bind(('127.0.0.1', 0))
    port = socket_probe.getsockname()[1]
process = subprocess.Popen(
    [sys.executable, '-X', 'utf8', '-m', 'uvicorn', 'smart_ticket.main:app',
     '--app-dir', 'src', '--host', '127.0.0.1', '--port', str(port)],
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
try:
    for attempt in range(100):
        if process.poll() is not None:
            raise RuntimeError('Our Uvicorn process exited before probe completed')
        try:
            with urllib.request.urlopen(f'http://127.0.0.1:{port}/health', timeout=1) as response:
                assert response.status == 200 and json.load(response) == {'status': 'ok'}
            with urllib.request.urlopen(f'http://127.0.0.1:{port}/openapi.json', timeout=1) as response:
                schema = json.load(response)
                assert schema['info']['version'] == app.version
                assert schema['info']['title'] == app.title
                assert schema['paths'] == app.openapi()['paths']
            break
        except OSError:
            time.sleep(0.1)
    else:
        raise RuntimeError('Uvicorn startup exceeded 10 seconds')
finally:
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5)
print(json.dumps({'python': sys.version.split()[0], 'app_version': app.version,
                  'app_title': app.title, 'openapi_paths': len(schema['paths']),
                  'http_health': 'PASS', 'http_openapi': 'PASS'}))
