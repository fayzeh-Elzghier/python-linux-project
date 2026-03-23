# admin.py
from utils import (
    validate_time, normalize_days, time_to_minutes,
    validate_date, log_action, file_exists, backup_files, generate_id
)

import os
DATA_DIR = "data"
DOCTORS_FILE = os.path.join(DATA_DIR, "doctors.txt")
APPOINTMENTS_FILE = os.path.join(DATA_DIR, "appointments.txt")

def admin_menu():
    while True:
        print("\n--- Admin Menu ---")
        print("1. Add Doctor")
        print("2. View Doctor Schedule")
        print("3. Backup Data")
        print("4. Back to Main Menu")
        choice = input("Choose: ").strip()

        if choice == "1":
            add_doctor()
        elif choice == "2":
            view_doctor_schedule()
        elif choice == "3":
            backup_files()
        elif choice == "4":
            break
        else:
            # Wrong menu choice → print error and return to menu immediately
            print("Invalid choice!")

def add_doctor():
    # Ask for name then validate immediately
    name = input("Enter doctor name: ").strip()
    if not name:
        print("Invalid name! It cannot be empty.")
        return

    # Ask for specialty then validate immediately
    specialty = input("Enter specialty: ").strip()
    if not specialty:
        print("Invalid specialty! It cannot be empty.")
        return

    # Ask for days then validate immediately
    days_in = input("Enter available days (comma-separated, e.g. Mon,Wed,Fri): ").strip()
    ok_days, days_norm = normalize_days(days_in)
    if not ok_days:
        print("Invalid days! Use only: MON,TUE,WED,THU,FRI,SAT,SUN (comma-separated).")
        return

    # Ask for start time then validate immediately
    start = input("Enter start time (HH:MM 24h): ").strip()
    if not validate_time(start):
        print("Invalid time format for start! Expected HH:MM (24h).")
        return

    # Ask for end time then validate immediately
    end = input("Enter end time (HH:MM 24h): ").strip()
    if not validate_time(end):
        print("Invalid time format for end! Expected HH:MM (24h).")
        return

    # Validate time range right away
    if time_to_minutes(start) >= time_to_minutes(end):
        print("Time range error! Start time must be earlier than end time.")
        return

    # Everything is valid → save record
    did = generate_id(DOCTORS_FILE, "D")
    with open(DOCTORS_FILE, "a") as f:
        f.write(f"{did}|{name}|{specialty}|{days_norm}|{start}|{end}\n")
    log_action(f"Doctor added: {did} - {name}")
    print("Doctor added successfully!")

def view_doctor_schedule():
    # Ask for Doctor ID and fail fast if empty
    did = input("Enter Doctor ID (e.g., D001): ").strip()
    if not did:
        print("Invalid Doctor ID! It cannot be empty.")
        return


    # Check if doctor exists in doctors file
    if not file_exists(DOCTORS_FILE):
        print("No doctors file found!")
        return
    doctor_found = False
    with open(DOCTORS_FILE) as f:
        for line in f:
            if line.split("|")[0] == did:
                doctor_found = True
                break
    if not doctor_found:
        print("Doctor ID not found in doctors file!")
        return

    # If appointments file missing → fail fast
    if not file_exists(APPOINTMENTS_FILE):
        print("No appointments file found!")
        return

    # Scan appointments and print matches immediately
    found = False
    with open(APPOINTMENTS_FILE) as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) != 6:
                # Bad line format → print error and continue scanning
                print("Corrupted line detected in appointments file. Skipping it.")
                continue
            aid, pid, doc_id, date, time, status = parts
            if doc_id == did:
                print(f"{aid} | Patient: {pid} | {date} {time} | {status}")
                found = True

    if not found:
        print("No appointments for this doctor.")
