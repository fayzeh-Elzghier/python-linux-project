from utils import (
    file_exists, validate_date, validate_time,
    normalize_days, time_to_minutes, generate_id
)
from logger import log
from backup import backup_data
import os
import re

DATA_DIR = "data"
DOCTORS_FILE = os.path.join(DATA_DIR, "doctors.txt")
PATIENTS_FILE = os.path.join(DATA_DIR, "patients.txt")
APPOINTMENTS_FILE = os.path.join(DATA_DIR, "appointments.txt")

def read_lines(path):
    if not file_exists(path):
        return []
    with open(path) as f:
        return [ln.rstrip("\n") for ln in f if ln.strip()]

def append_line(path, line):
    with open(path, "a") as f:
        f.write(line + "\n")

def book_appointment():
    os.makedirs(DATA_DIR, exist_ok=True)
    print("..........................")
    print("Book new appointment ")
    print("...........................")

    patient_id = input("Enter the patient ID (e.g. p001): ").strip()
    patients = read_lines(PATIENTS_FILE)
    if not any(re.match(rf"{re.escape(patient_id)}\|", p) for p in patients):
        print("The id you entered does not exist")
        return

    specialty = input("Enter specialty you want: ").strip()
    doctors = read_lines(DOCTORS_FILE)
    matched = [d for d in doctors if re.search(rf"\|{re.escape(specialty)}\|", d)]
    if not matched:
        print("No available doctors in this specialty.")
        return

    print("List of available doctors in this specialty:")
    for d in matched:
        print(d)

    doctor_id = input("Enter the doctor ID (e.g. D001): ").strip()
    # Only allow doctor IDs from the matched specialty list
    matched_ids = [d.split("|")[0] for d in matched]
    if doctor_id not in matched_ids:
        print("This doctor ID is not available in the selected specialty.")
        return
    doctor_line = next((d for d in matched if d.startswith(f"{doctor_id}|")), None)

    parts = doctor_line.split("|")
    available_days_raw = parts[3]
    start_time = parts[4]
    end_time = parts[5]

    date_input = input("enter the date if this form (YYYY-MM-DD): ").strip()
    if not validate_date(date_input):
        print("wrong expression ! (date invalid)")
        return

    user_day = input("Enter the day of the week (e.g. Sun, Mon, ...): ").strip().upper()
    valid_days = {"SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"}
    if user_day not in valid_days:
        print("Invalid day entered!")
        return

    ok, normalized = normalize_days(available_days_raw)
    if not ok:
        print("doctor's schedule data is invalid.")
        return
    doctor_days = [d.strip().upper() for d in normalized.split(",")]
    if user_day not in doctor_days:
        print(f"the doctor is not avalible is this day {user_day}")
        return

    time_input = input("Enter time as (HH:MM): ").strip()
    if not validate_time(time_input):
        print("wrong expression ! (time invalid)")
        return

    t_min = time_to_minutes(time_input)
    start_min = time_to_minutes(start_time)
    end_min = time_to_minutes(end_time)
    if t_min < start_min or t_min > end_min:
        print(f"Time outside the doctor's working hours ({start_time} - {end_time})")
        return

    appointments = read_lines(APPOINTMENTS_FILE)
    if any(f"|{doctor_id}|{date_input}|{time_input}|" in a for a in appointments):
        print("this appointment is booked in advance")
        return

    new_aid = generate_id(APPOINTMENTS_FILE, "A", width=3)
    append_line(APPOINTMENTS_FILE, f"{new_aid}|{patient_id}|{doctor_id}|{date_input}|{time_input}|Confirmed")
    # Logging
    log("BOOK_APPOINTMENT", f"{new_aid}|{patient_id}|{doctor_id}|{date_input}|{time_input}")
    # Auto backup
    backup_data()
    print(f"Ur appointment booked is done successfully with appointment ID {new_aid}")

if __name__ == "__main__":
    book_appointment()
