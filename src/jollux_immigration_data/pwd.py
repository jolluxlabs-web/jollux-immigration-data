"""PWD disclosure ingestion."""

from __future__ import annotations

from collections.abc import Iterator
from itertools import chain
from pathlib import Path
from typing import Any

from .dates import excel_date
from .employer import normalize_employer
from .location import normalize_location, normalize_state
from .tabular import iter_rows, require_columns
from .wage import normalize_wage_level

REQUIRED_COLUMNS = {
    "CASE_NUMBER", "CASE_STATUS", "RECEIVED_DATE", "VISA_CLASS", "EMPLOYER_LEGAL_BUSINESS_NAME",
    "JOB_TITLE", "PRIMARY_WORKSITE_CITY", "PRIMARY_WORKSITE_STATE", "PWD_SOC_TITLE", "PWD_WAGE_RATE",
    "PWD_UNIT_OF_PAY", "PWD_OES_WAGE_LEVEL", "PREVAIL_WAGE_DETERM_DATE", "PWD_WAGE_EXPIRATION_DATE",
}


def ingest_pwd(path: str | Path) -> Iterator[dict[str, Any]]:
    rows = iter_rows(path)
    try:
        first = next(rows)
    except StopIteration:
        return
    require_columns(first, REQUIRED_COLUMNS)
    seen: set[str] = set()
    for row in chain((first,), rows):
        case_number = str(row.get("CASE_NUMBER") or "").strip()
        status = str(row.get("CASE_STATUS") or "").strip()
        visa_class = str(row.get("VISA_CLASS") or "").strip()
        employer = str(row.get("EMPLOYER_LEGAL_BUSINESS_NAME") or "").strip()
        expiration = excel_date(row.get("PWD_WAGE_EXPIRATION_DATE"))
        if not case_number or case_number in seen or visa_class.upper() != "PERM" or status.casefold() == "withdrawn" or not employer or not expiration:
            continue
        seen.add(case_number)
        city = row.get("PRIMARY_WORKSITE_CITY")
        state = row.get("PRIMARY_WORKSITE_STATE")
        yield {
            "case_number": case_number,
            "case_status": status or None,
            "received_date": excel_date(row.get("RECEIVED_DATE")),
            "employer_name": employer,
            "employer_normalized": normalize_employer(employer),
            "job_title": row.get("JOB_TITLE"),
            "worksite_city": city,
            "worksite_state": normalize_state(str(state) if state else None),
            "worksite_location": normalize_location(str(city) if city else None, str(state) if state else None),
            "soc_title": row.get("PWD_SOC_TITLE"),
            "wage_rate": row.get("PWD_WAGE_RATE"),
            "wage_unit": row.get("PWD_UNIT_OF_PAY"),
            "wage_level": normalize_wage_level(row.get("PWD_OES_WAGE_LEVEL")),
            "determination_date": excel_date(row.get("PREVAIL_WAGE_DETERM_DATE")),
            "wage_expiration_date": expiration,
        }
