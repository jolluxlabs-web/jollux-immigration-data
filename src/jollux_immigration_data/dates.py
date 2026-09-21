"""Date conversion helpers for DOL disclosure values."""

from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Any


def excel_date(value: Any) -> str | None:
    """Convert an Excel serial or common date value to an ISO date string."""
    if value in (None, ""):
        return None
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return (datetime(1899, 12, 30) + timedelta(days=float(value))).date().isoformat()
    text = str(value).strip()
    if not text:
        return None
    candidate = text.split("T", 1)[0].split(" ", 1)[0]
    for pattern in ("%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y"):
        try:
            return datetime.strptime(candidate, pattern).date().isoformat()
        except ValueError:
            pass
    return candidate
