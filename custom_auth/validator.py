import re

def is_valid_min_length(value: str, length: int) -> bool:

    if len(value) < length:
        return False

    return True

def is_valid_max_length(value: str, length: int) -> bool:

    if len(value) > length:
        return False

    return True

def is_valid_alpha_numeric(value: str) -> bool:

    return re.search('^[0-9a-zA-Z-_]+$', value)

