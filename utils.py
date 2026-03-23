import re
import os
from datetime import datetime

# ---------- validation ----------
def validate_time(t):
    return re.fullmatch(r'(?:[01]\d|2[0-3]):[0-5]\d', (t or "").strip()) is not None

def validate_date(s):
    s = (s or "").strip()
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', s):
        return False
    y, m, d = map(int, s.split("-"))
    try:
        datetime(y, m, d)
        return True
    except ValueError:
        return False

def normalize_days(days_str):
    allowed = {'MON','TUE','WED','THU','FRI','SAT','SUN'}
    items = [d.strip().upper() for d in (days_str or "").split(',') if d.strip()]
    if not items or any(d not in allowed for d in items):
        return False, None
    seen, out = set(), []
    for d in items:
        if d not in seen:
            seen.add(d)
            out.append(d)
    return True, ",".join(out)

def time_to_minutes(t):
    hh, mm = map(int, (t or "0:0").split(':', 1))
    return hh * 60 + mm

# ---------- filesystem helpers ----------
def file_exists(path):
    return os.path.exists(path)

def log_action(msg, log_file="system.log"):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a") as f:
        f.write(f"[{ts}] {msg}\n")

def backup_files(dest_dir="backups"):
    os.makedirs(dest_dir, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = os.path.join(dest_dir, ts)
    os.makedirs(out_dir, exist_ok=True)

    candidates = ["doctors.txt", "patients.txt", "appointments.txt", "system.log"]
    copied_any = False
    for fname in candidates:
        if os.path.isfile(fname):
            with open(fname, "rb") as src, open(os.path.join(out_dir, fname), "wb") as dst:
                dst.write(src.read())
            copied_any = True

    if copied_any:
        log_action(f"Backup created at {out_dir}")
        print(f"Backup created at: {out_dir}")
    else:
        print("No data files found to backup.")

# ---------- IDs ----------
def generate_id(filepath, prefix, width=3):
    last_num = 0
    if os.path.exists(filepath):
        with open(filepath) as f:
            for line in f:
                first = line.strip().split("|", 1)[0]
                m = re.match(rf'{re.escape(prefix)}(\d+)$', first)
                if m:
                    try:
                        n = int(m.group(1))
                        if n > last_num:
                            last_num = n
                    except ValueError:
                        pass
    return f"{prefix}{last_num + 1:0{width}d}"
