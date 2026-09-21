"""PERM disclosure ingestion."""

from __future__ import annotations

from collections.abc import Iterator
from itertools import chain
from pathlib import Path
from typing import Any

from .dates import excel_date
from .employer import normalize_employer
from .location import normalize_location, normalize_state
from .tabular import iter_rows, require_columns

REQUIRED_COLUMNS = {
    "CASE_NUMBER", "CASE_STATUS", "RECEIVED_DATE", "DECISION_DATE", "EMP_BUSINESS_NAME", "PWD_SOC_TITLE",
    "JOB_TITLE", "JOB_OPP_WAGE_FROM", "JOB_OPP_WAGE_TO", "JOB_OPP_WAGE_PER", "PRIMARY_WORKSITE_CITY",
    "PRIMARY_WORKSITE_STATE", "RECR_INFO_JOB_START_DATE", "RECR_INFO_JOB_END_DATE",
}


def ingest_perm(path: str | Path) -> Iterator[dict[str, Any]]:
    rows = iter_rows(path)
    try:
        first = next(rows)
    except StopIteration:
        return
    require_columns(first, REQUIRED_COLUMNS)
    for row in chain((first,), rows):
        case_number = str(row.get("CASE_NUMBER") or "").strip()
        employer = str(row.get("EMP_BUSINESS_NAME") or "").strip()
        if not case_number or not employer:
            continue
        city = row.get("PRIMARY_WORKSITE_CITY")
        state = row.get("PRIMARY_WORKSITE_STATE")
        yield {
            "case_number": case_number,
            "case_status": row.get("CASE_STATUS"),
            "received_date": excel_date(row.get("RECEIVED_DATE")),
            "decision_date": excel_date(row.get("DECISION_DATE")),
            "employer_name": employer,
            "employer_normalized": normalize_employer(employer),
            "job_title": row.get("JOB_TITLE"),
            "soc_title": row.get("PWD_SOC_TITLE"),
            "wage_from": row.get("JOB_OPP_WAGE_FROM"),
            "wage_to": row.get("JOB_OPP_WAGE_TO"),
            "wage_unit": row.get("JOB_OPP_WAGE_PER"),
            "worksite_city": city,
            "worksite_state": normalize_state(str(state) if state else None),
            "worksite_location": normalize_location(str(city) if city else None, str(state) if state else None),
            "recruitment_start_date": excel_date(row.get("RECR_INFO_JOB_START_DATE")),
            "recruitment_end_date": excel_date(row.get("RECR_INFO_JOB_END_DATE")),
        }
