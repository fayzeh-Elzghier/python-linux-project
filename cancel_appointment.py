from utils import file_exists
from logger import log
from backup import backup_data
import os

DATA_DIR = "data"
APPOINTMENTS_FILE = os.path.join(DATA_DIR, "appointments.txt")
TEMP_FILE = os.path.join(DATA_DIR, "temp_appointments.txt")

def read_lines(path):
    if not file_exists(path):
        return []
    with open(path) as f:
        return [ln.rstrip("\n") for ln in f if ln.strip()]

def overwrite_lines(path, lines):
    with open(path, "w") as f:
        for ln in lines:
            f.write(ln + "\n")

def cancel_appointment():
    print("...........................")
    print("Cancel Appointment ")
    print("..........................")
    pid = input("Enter patient ID: ").strip()
    appointments = read_lines(APPOINTMENTS_FILE)
    matches = [a for a in appointments if f"|{pid}|" in a]
    if not matches:
        print("there is no appointments found for this patients ID")
        return

    print("----------------------------")
    print("Ur appointments:")
    print("..........................")
    for a in matches:
        parts = a.split("|")
        aid = parts[0]
        date = parts[3]
        time1 = parts[4]
        status = parts[5]
        print(f"The appointment id : {aid} Date : {date} At time : {time1} Status : {status}")
        print("........................................")

    appo_id = input("Enter appointment ID u want to cancel (e.g. A002): ").strip()
    found = False
    new_lines = []
    for ln in appointments:
        parts = ln.split("|")
        cur_id = parts[0]
        cur_pid = parts[1]
        if cur_id == appo_id and cur_pid == pid:
            found = True
            if parts[5] != "Cancelled":
                parts[5] = "Cancelled"
            new_lines.append("|".join(parts))
        else:
            new_lines.append(ln)

    if not found:
        print("this appointment not found or dose not belong to u @.@")
        return

    overwrite_lines(APPOINTMENTS_FILE, new_lines)

    # Logging
    log("CANCEL_APPOINTMENT", f"{appo_id}|{pid}")
    # Auto backup
    backup_data()

    print("Appointment has been cancelled sucessfully :)")

if __name__ == "__main__":
    cancel_appointment()
