"""Wage-level normalization."""

import re

_LEVELS = {"1": "Level I", "I": "Level I", "2": "Level II", "II": "Level II", "3": "Level III", "III": "Level III", "4": "Level IV", "IV": "Level IV"}


def normalize_wage_level(value: object) -> str | None:
    if value is None:
        return None
    text = " ".join(str(value).strip().upper().replace("_", " ").split())
    if not text or text in {"N/A", "NA", "NONE", "NULL"}:
        return None
    match = re.fullmatch(r"(?:WAGE\s+)?LEVEL\s+([IV1-4]+)", text)
    token = match.group(1) if match else text
    return _LEVELS.get(token, str(value).strip())
