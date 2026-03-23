# core/io.py
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
DOCTORS_FILE = os.path.join(DATA_DIR, "doctors.txt")
PATIENTS_FILE = os.path.join(DATA_DIR, "patients.txt")
APPOINTMENTS_FILE = os.path.join(DATA_DIR, "appointments.txt")

def ensure_data_files():
    os.makedirs(DATA_DIR, exist_ok=True)
    for fp in (DOCTORS_FILE, PATIENTS_FILE, APPOINTMENTS_FILE):
        if not os.path.exists(fp):
            open(fp, "w", encoding="utf-8").close()

def load_lines(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return [ln.rstrip("\n") for ln in f if ln.strip()]

def append_line(path, line):
    with open(path, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def overwrite_lines(path, lines):
    with open(path, "w", encoding="utf-8") as f:
        for ln in lines:
            f.write(ln + "\n")
