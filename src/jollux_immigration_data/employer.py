"""Employer matching helpers that preserve the original source name."""

from __future__ import annotations

import re
import unicodedata
from collections import defaultdict
from collections.abc import Iterable

_SUFFIXES = {"co", "company", "corp", "corporation", "inc", "incorporated", "limited", "llc", "llp", "lp", "ltd", "na", "plc"}


def normalize_employer(value: str) -> str:
    text = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    text = text.casefold().replace("&", " and ")
    parts = re.sub(r"[^a-z0-9]+", " ", text).split()
    while parts and parts[-1] in _SUFFIXES:
        parts.pop()
    return " ".join(parts)


def employer_collision_report(names: Iterable[str]) -> dict[str, list[str]]:
    """Return normalized keys that map to multiple distinct source names."""
    grouped: dict[str, set[str]] = defaultdict(set)
    for name in names:
        if name and (key := normalize_employer(name)):
            grouped[key].add(name.strip())
    return {key: sorted(values) for key, values in sorted(grouped.items()) if len(values) > 1}
