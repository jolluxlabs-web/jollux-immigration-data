from datetime import date, datetime

from jollux_immigration_data.dates import excel_date
from jollux_immigration_data.employer import employer_collision_report, normalize_employer
from jollux_immigration_data.location import normalize_location, normalize_state
from jollux_immigration_data.wage import normalize_wage_level


def test_employer_normalization_and_collisions():
    assert normalize_employer("Café Data & Research, Inc.") == "cafe data and research"
    assert employer_collision_report(["Example, Inc.", "Example LLC", "Different Co."]) == {
        "example": ["Example LLC", "Example, Inc."]
    }


def test_location_and_wage_level_normalization():
    assert normalize_state("New York") == "NY"
    assert normalize_state("ca") == "CA"
    assert normalize_location("  New York ", "New York") == "New York, NY"
    assert normalize_wage_level("Wage Level IV") == "Level IV"
    assert normalize_wage_level(2) == "Level II"
    assert normalize_wage_level("N/A") is None


def test_excel_date_conversion():
    assert excel_date(1) == "1899-12-31"
    assert excel_date(date(2026, 3, 4)) == "2026-03-04"
    assert excel_date(datetime(2026, 3, 4, 12, 30)) == "2026-03-04"
    assert excel_date("03/04/2026") == "2026-03-04"
