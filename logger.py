import os
from datetime import datetime

DATA_DIR = "data"
LOG_FILE = os.path.join(DATA_DIR, "system.log")
os.makedirs(DATA_DIR, exist_ok=True)

def log(action: str, details: str):
    """
    Logs an action to system.log with timestamp.
    Format: YYYY-MM-DD HH:MM:SS | ACTION | details
    """
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{ts} | {action} | {details}\n"
    with open(LOG_FILE, "a") as f:
        f.write(line)
