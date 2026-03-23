from utils import file_exists, generate_id
from logger import log
from backup import backup_data
import os

DATA_DIR = "data"
PATIENTS_FILE = os.path.join(DATA_DIR, "patients.txt")

def read_lines(path):
    if not file_exists(path):
        return []
    with open(path) as f:
        return [ln.rstrip("\n") for ln in f if ln.strip()]

def append_line(path, line):
    with open(path, "a") as f:
        f.write(line + "\n")

def register_patient():
    os.makedirs(DATA_DIR, exist_ok=True)
    print(".....................")
    print("Register new patient")
    print(".....................")

    name = input("Enter name: ").strip()
    phone = input("Enter phone number (10 digits): ").strip()

    if len(phone) != 10 or not phone.isdigit():
        print(":( Invalid phone number (must be 10 digits and numeric)")
        return

    new_id = generate_id(PATIENTS_FILE, "p", width=3)
    append_line(PATIENTS_FILE, f"{new_id}|{name}|{phone}")

    # Logging
    log("REGISTER_PATIENT", f"{new_id}|{name}|{phone}")
    # Auto backup
    backup_data()

    print(f"Register new patient done successfully. New patient id is: {new_id}")

if __name__ == "__main__":
    register_patient()
