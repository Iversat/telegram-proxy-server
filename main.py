import os
import time
import subprocess
import signal
import sys

USERS_FILE = 'users.enc'
process = None

def get_mtime():
    try:
        return os.path.getmtime(USERS_FILE)
    except Exception:
        return 0

def cleanup(signum, frame):
    if process:
        process.terminate()
    sys.exit(0)

signal.signal(signal.SIGTERM, cleanup)
signal.signal(signal.SIGINT, cleanup)

last_mtime = get_mtime()
process = subprocess.Popen(["python3", "mtprotoproxy.py"])

while True:
    time.sleep(3)
    current_mtime = get_mtime()
    if current_mtime != last_mtime:
        process.terminate()
        process.wait()
        process = subprocess.Popen(["python3", "mtprotoproxy.py"])
        last_mtime = current_mtime