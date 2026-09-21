from pathlib import Path

from openpyxl import Workbook

from jollux_immigration_data import ingest_perm, ingest_pwd

FIXTURES = Path(__file__).parent / "fixtures"


def as_xlsx(csv_path: Path, output: Path) -> Path:
    import csv
    workbook = Workbook()
    sheet = workbook.active
    with csv_path.open(encoding="utf-8", newline="") as handle:
        for row in csv.reader(handle):
            sheet.append(row)
    workbook.save(output)
    return output


def test_pwd_csv_filters_and_normalizes():
    records = list(ingest_pwd(FIXTURES / "pwd.csv"))
    assert len(records) == 1
    assert records[0]["case_number"] == "P-100"
    assert records[0]["employer_normalized"] == "example analytics"
    assert records[0]["worksite_location"] == "Austin, TX"
    assert records[0]["wage_level"] == "Level II"


def test_pwd_xlsx_uses_same_pipeline(tmp_path):
    source = as_xlsx(FIXTURES / "pwd.csv", tmp_path / "pwd.xlsx")
    assert list(ingest_pwd(source))[0]["case_number"] == "P-100"


def test_perm_csv_and_xlsx(tmp_path):
    csv_records = list(ingest_perm(FIXTURES / "perm.csv"))
    source = as_xlsx(FIXTURES / "perm.csv", tmp_path / "perm.xlsx")
    xlsx_records = list(ingest_perm(source))
    assert csv_records == xlsx_records
    assert csv_records[0]["recruitment_start_date"] == "2026-01-01"
    assert csv_records[1]["worksite_state"] == "WA"


def test_missing_required_column_is_clear(tmp_path):
    path = tmp_path / "bad.csv"
    path.write_text("CASE_NUMBER,CASE_STATUS\nX,Certified\n", encoding="utf-8")
    try:
        list(ingest_perm(path))
    except ValueError as error:
        assert "Missing required columns" in str(error)
        assert "EMP_BUSINESS_NAME" in str(error)
    else:
        raise AssertionError("Expected schema validation to fail")
