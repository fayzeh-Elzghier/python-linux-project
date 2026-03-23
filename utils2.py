# ---------- filesystem helpers ----------
def file_exists(path: str) -> bool:
    try:
        with open(path, 'r'):
            pass
        return True
    except (FileNotFoundError, OSError):
        return False
# utils.py

import re
import time

# ---------- validation ----------
def validate_time(t: str) -> bool:
    # HH:MM in 24-hour format
    if not re.fullmatch(r'(?:[01]\d|2[0-3]):[0-5]\d', t.strip()):
        return False
    hh, mm = map(int, t.strip().split(':'))
    return 0 <= hh <= 23 and 0 <= mm <= 59

def validate_date(s: str) -> bool:
    # Format YYYY-MM-DD + simple date validation (without libraries)
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', s or ""):
        return False
    y, m, d = map(int, s.split("-"))
    if not (1 <= m <= 12 and 1 <= d <= 31):
        return False
    # Check number of days in each month
    if m in {4, 6, 9, 11} and d > 30:
        return False
    if m == 2:
        # Leap year
        is_leap = (y % 4 == 0 and (y % 100 != 0 or y % 400 == 0))
        if d > (29 if is_leap else 28):
            return False
    return True

def normalize_days(days_str: str):
    """
    Returns (is_valid, normalized_str)
    Allowed days: MON,TUE,WED,THU,FRI,SAT,SUN
    """
    allowed = {'MON','TUE','WED','THU','FRI','SAT','SUN'}
    items = [d.strip().upper() for d in (days_str or "").split(',') if d.strip()]
    if not items or any(d not in allowed for d in items):
        return False, None
    # Remove duplicates while preserving order
    seen = set()
    norm = []
    for d in items:
        if d not in seen:
            seen.add(d)
            norm.append(d)
    return True, ','.join(norm)

def time_to_minutes(t: str) -> int:
    hh, mm = map(int, t.split(':'))
    return hh * 60 + mm


# ---------- filesystem helpers ----------
def file_exists(path: str) -> bool:
    try:
        with open(path, 'r'):
            pass
        return True
    except (FileNotFoundError, OSError):
        return False

def log_action(action_type: str, details: str, log_file: str = "system.log") -> None:
    # Writes a timestamped log entry: [YYYY-MM-DD HH:MM:SS] ACTION_TYPE: details
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a") as f:
        f.write(f"[{ts}] {action_type}: {details}\n")

def backup_data(dest_dir: str = "backups") -> None:
    # Create backup folder if it doesn't exist
    try:
        with open(f"{dest_dir}/.test", 'w') as f:
            f.write("")
    except FileNotFoundError:
        # Try to create subfolders if needed
        for i in range(10):
            try:
                with open(f"{dest_dir}/temp_dir_creation", 'w') as f:
                    f.write("")
                break
            except FileNotFoundError:
                continue
    # Find the next available backup number
    backup_counter = 1
    while True:
        backup_folder = f"{dest_dir}/backup_{backup_counter:03d}"
        if not file_exists(f"{backup_folder}/.exists"):
            break
        backup_counter += 1
    # Create the backup folder
    try:
        with open(f"{backup_folder}/.exists", 'w') as f:
            f.write("")
    except FileNotFoundError:
        pass
    candidates = ["doctors.txt", "patients.txt", "appointments.txt", "system.log"]
    copied_any = False
    for fname in candidates:
        if file_exists(fname):
            # Manually copy the file
            try:
                with open(fname, 'r') as src:
                    content = src.read()
                with open(f"{backup_folder}/{fname}", 'w') as dst:
                    dst.write(content)
                copied_any = True
            except (FileNotFoundError, OSError):
                continue
    if copied_any:
        log_action("BACKUP", f"Backup created at {backup_folder}")
        print(f"Backup created at: {backup_folder}")
    else:
        print("No data files found to backup.")

backup_files = backup_data

# ---------- IDs ----------
def generate_id(filepath: str, prefix: str, width: int = 3) -> str:
    """
    Generates an ID like D001, P007 ...
    Uses the last line in the file if it exists, otherwise starts from 001
    """
    last_num = 0
    if file_exists(filepath):
        with open(filepath) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                first_field = line.split("|", 1)[0]
                m = re.match(rf'{re.escape(prefix)}(\d+)$', first_field.strip())
                if m:
                    try:
                        last_num = max(last_num, int(m.group(1)))
                    except ValueError:
                        pass
    new_num = last_num + 1
    return f"{prefix}{new_num:0{width}d}"