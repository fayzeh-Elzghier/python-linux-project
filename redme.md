

---

# Outpatient Reservation System – Admin Module

## Overview

The **Admin Module** of the Outpatient Reservation System allows system administrators to manage doctor information, monitor schedules, and perform backups.
This module is designed for **command-line interaction** and uses **plain text files** to store and manage data.

---

## Features

### 1. **Add a New Doctor**

* **Purpose:** Register a new doctor into the system.
* **Input Required:**

  * Doctor Name
  * Medical Specialty
  * Available Working Days (comma-separated, e.g., `Mon,Wed,Fri`)
  * Start Time (`HH:MM`, 24-hour format)
  * End Time (`HH:MM`, 24-hour format)
* **Validation Rules:**

  * Name and specialty must not be empty.
  * Days must be valid (MON, TUE, WED, THU, FRI, SAT, SUN).
  * Time must follow the `HH:MM` format.
  * Start time must be earlier than end time.
* **Storage Format:**

  ```
  DoctorID|Name|Specialty|AvailableDays|StartTime|EndTime
  ```

  Example:

  ```
  D001|Dr. Ahmad|Cardiology|MON,WED,FRI|08:00|14:00
  ```
* **Logging:** Every doctor addition is recorded in `system.log`.

---

### 2. **View Doctor Schedule**

* **Purpose:** View all booked appointment slots for a specific doctor.
* **Process:**

  * Admin enters the **Doctor ID**.
  * The system reads `appointments.txt` and displays:

    * Appointment ID
    * Patient ID
    * Date
    * Time
    * Status
* **Usage Example:**

  ```
  A001 | Patient: P005 | 2025-08-18 09:00 | Confirmed
  ```
* **Behavior:**

  * If no appointments exist, a message is shown.
  * If `appointments.txt` is missing, the system alerts the admin.

---

### 3. **Backup Data**

* **Purpose:** Create a manual backup of system data files.
* **Files Included in Backup:**

  * `doctors.txt`
  * `patients.txt`
  * `appointments.txt`
  * `system.log`
* **Backup Process:**

  * A timestamped folder is created in `backups/`.
  * All existing files are copied into this folder.
  * Log entry is added to `system.log`.
* **Example Backup Folder:**

  ```
  backups/20250814_235959/
      doctors.txt
      patients.txt
      appointments.txt
      system.log
  ```

---

## File Dependencies

* **doctors.txt** → Stores doctor information.
* **appointments.txt** → Stores appointment details.
* **system.log** → Tracks system actions.
* **backups/** → Folder where backup data is stored.

---

## Logging

All admin operations are logged in `system.log` with timestamps for tracking and auditing.

Example log entry:

```
[2025-08-14 12:45:22] Doctor added: D004 - Dr. Sara
[2025-08-14 12:47:10] Backup created at backups/20250814_124710
```

---

## Usage Flow (Admin)

1. Select `Admin` role from main menu.
2. Choose an option:

   * `1` → Add Doctor
   * `2` → View Doctor Schedule
   * `3` → Backup Data
   * `4` → Return to Main Menu
3. Follow the prompts and validations.

---


---

# Outpatient Reservation System – Python Version

## Overview

The **Patient Module** of the Outpatient Reservation System allows patients to register, book, view, or cancel appointments.
This system is designed for **command-line interaction** and uses **plain text files** to store and manage data.
All scripts are located in the `out/` folder.

---

## Features

### 1. **Register a New Patient**

* **Purpose:** Register a new patient into the system.

* **Input Required:**

  * Patient Name
  
  * Contact Information

* **Validation Rules:**

  * Name must not be empty.
  * Age must be a positive integer.
  * Contact info must be valid (phone/email).

* **Storage Format:**

  ```
  PatientID|Name|Age|Contact
  ```

  Example:

  ```
  P001|Fayzeh|+970598765432
  ```

* **Script:** `register_patient.py`

---

### 2. **Book an Appointment**

* **Purpose:** Allow a patient to book an appointment with a doctor.

* **Input Required:**

  * Patient ID
  * Doctor ID
  * Date (`YYYY-MM-DD`)
  * Time (`HH:MM`, 24-hour format)

* **Validation Rules:**

  * Patient and doctor IDs must exist.
  * Date must be valid.
  * Time must be within the doctor's working hours.
  * Slot must be available.

* **Storage Format:**

  ```
  AppointmentID|PatientID|DoctorID|Date|Time
  ```

  Example:

  ```
  A001|P001|D003|2025-08-18|09:00
  ```

* **Script:** `book_appointment.py`

---

### 3. **Cancel an Appointment**

* **Purpose:** Allow a patient to cancel an existing appointment.

* **Input Required:**

  * Appointment ID or combination of Patient ID + Date/Time

* **Behavior:**

  * Checks if the appointment exists.
  * Removes the appointment from `appointments.txt`.
  * Logs the cancellation.

* **Script:** `cancel_appointment.py`

---

### 4. **View Appointments**

* **Purpose:** View all scheduled appointments for a patient or a doctor.
* **Input Required:**

  * Patient ID or Doctor ID
* **Output:**

  * Lists appointments with Date, Time, Doctor/Patient Name, and Status.
* **Script:** `view_appointments.py`

---

### 5. **Patient Menu**

* **Purpose:** Main interface for patient operations.

* **Features:**

  * Register as a new patient
  * Book an appointment
  * Cancel an appointment
  * View appointments

* **Script:** `patient_menu.py`

* **Behavior:** Calls the other scripts to perform tasks interactively.

---

## File Dependencies

* **patients.txt** → Stores patient information.
* **doctors.txt** → Stores doctor information.
* **appointments.txt** → Stores appointment details.
* **system.log** → Tracks operations and actions.
* **backups/** → Folder for manual backup data.

---

## Logging

All actions are logged in `system.log` with timestamps.
Example log entry:

```
[2025-08-14 14:10:22] Patient registered: P001 - Fayzeh
[2025-08-14 14:15:10] Appointment booked: A001 - P001 with D003
[2025-08-14 14:18:05] Appointment canceled: A001
```

---

## Usage Flow (Patient)

1. Navigate to the `out/` folder.
2. Run the main menu script:

```bash
python3 patient_menu.py
```

3. Follow the prompts:

   * `1` → Register New Patient
   * `2` → Book Appointment
   * `3` → Cancel Appointment
   * `4` → View Appointments
   * `5` → Exit

4. All inputs are validated, and operations are logged automatically.

---


