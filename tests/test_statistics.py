from jollux_immigration_data import calendar_days, recruitment_statistics


def test_calendar_days_rejects_invalid_or_implausible_values():
    assert calendar_days("2026-01-01", "2026-04-01") == 90
    assert calendar_days("2026-04-01", "2026-01-01") is None
    assert calendar_days("bad", "2026-01-01") is None
    assert calendar_days("2020-01-01", "2026-01-01") is None


def test_recruitment_statistics_reports_coverage():
    result = recruitment_statistics([
        {"recruitment_start_date": "2026-01-01", "received_date": "2026-04-01"},
        {"recruitment_start_date": "2026-02-01", "received_date": "2026-04-11"},
        {"recruitment_start_date": None, "received_date": "2026-04-11"},
    ])
    assert result == {
        "total_records": 3,
        "included_records": 2,
        "excluded_records": 1,
        "minimum_days": 69,
        "maximum_days": 90,
        "median_days": 79.5,
    }
