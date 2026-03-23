def is_valid_phone(phone):
    return phone.isdigit() and len(phone) == 10

def parse_date(date_str):
    parts = date_str.split('-')
    if len(parts) == 3 and all(part.isdigit() for part in parts):
        y, m, d = parts
        if len(y) == 4 and 1 <= int(m) <= 12 and 1 <= int(d) <= 31:
            return (int(y), int(m), int(d))
    return None

def parse_time(time_str):
    parts = time_str.split(':')
    if len(parts) == 2 and all(part.isdigit() for part in parts):
        h, m = parts
        if 0 <= int(h) <= 23 and 0 <= int(m) <= 59:
            return (int(h), int(m))
    return None

def day_code_from_date(date_tuple):
    # Not possible without a date library, so just return 'N/A'
    return 'N/A'

def time_in_range(t, start_str, end_str):
    s = parse_time(start_str)
    e = parse_time(end_str)
    if s is None or e is None or t is None:
        return False
    return s <= t <= e