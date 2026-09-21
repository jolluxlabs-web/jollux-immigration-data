"""Transparent recruitment timing statistics."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from datetime import date
from statistics import median
from typing import Any


def calendar_days(start: str | None, end: str | None, *, maximum: int = 366) -> int | None:
    if not start or not end:
        return None
    try:
        duration = (date.fromisoformat(end) - date.fromisoformat(start)).days
    except ValueError:
        return None
    return duration if 0 <= duration <= maximum else None


def recruitment_statistics(records: Iterable[Mapping[str, Any]], *, maximum: int = 366) -> dict[str, int | float | None]:
    values: list[int] = []
    total = 0
    for record in records:
        total += 1
        value = calendar_days(record.get("recruitment_start_date"), record.get("received_date"), maximum=maximum)
        if value is not None:
            values.append(value)
    return {
        "total_records": total,
        "included_records": len(values),
        "excluded_records": total - len(values),
        "minimum_days": min(values) if values else None,
        "maximum_days": max(values) if values else None,
        "median_days": median(values) if values else None,
    }
