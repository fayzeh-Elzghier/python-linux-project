import os
 
from datetime import datetime

DATA_DIR = "data"
BACKUP_DIR = os.path.join(DATA_DIR, "backups")
os.makedirs(BACKUP_DIR, exist_ok=True)

def backup_data():
    """
    Creates a timestamped backup of all data files.
    """
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest_folder = os.path.join(BACKUP_DIR, ts)
    os.makedirs(dest_folder, exist_ok=True)

    for filename in ["patients.txt", "appointments.txt", "doctors.txt", "system.log"]:
        src = os.path.join(DATA_DIR, filename)
        dst = os.path.join(dest_folder, filename)
        if os.path.exists(src):
            with open(src, "rb") as fsrc:
                content = fsrc.read()
            with open(dst, "wb") as fdst:
                fdst.write(content)

    return dest_folder
