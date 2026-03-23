# view_appointments.py
from utils import file_exists
import os

DATA_DIR = "data"
APPOINTMENTS_FILE = os.path.join(DATA_DIR, "appointments.txt")
DOCTORS_FILE = os.path.join(DATA_DIR, "doctors.txt")

def read_lines(path):
    if not file_exists(path):
        return []
    with open(path) as f:
        return [ln.rstrip("\n") for ln in f if ln.strip()]

def view_appointments():
    print(".............................")
    print("view my appointment ")
    print("............................")
    pid = input("Enter the patient ID's: ").strip()
    appointments = [a for a in read_lines(APPOINTMENTS_FILE) if f"|{pid}|" in a]
    if not appointments:
        print("there is no patient with this ID or no appointments")
        return

    doctors = {d.split("|")[0]: d.split("|")[1] for d in read_lines(DOCTORS_FILE)}
    print("list of ur appointments :")
    print("..........................")
    for line in appointments:
        aid = line.split("|")[0]
        doctor_id = line.split("|")[2]
        date = line.split("|")[3]
        time1 = line.split("|")[4]
        status = line.split("|")[5]
        doctor_name = doctors.get(doctor_id, "Unknown")
        print(f"The appointment id : {aid}")
        print(f"with : {doctor_name}")
        print(f"Date : {date}")
        print(f"At time : {time1}")
        print(f"Status : {status}")
        print("........................................")

if __name__ == "__main__":
    view_appointments()
