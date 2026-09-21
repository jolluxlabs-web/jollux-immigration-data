"""U.S. state and territory normalization."""

_STATE_CODES = {
    "ALABAMA": "AL", "ALASKA": "AK", "ARIZONA": "AZ", "ARKANSAS": "AR", "CALIFORNIA": "CA",
    "COLORADO": "CO", "CONNECTICUT": "CT", "DELAWARE": "DE", "FLORIDA": "FL", "GEORGIA": "GA",
    "HAWAII": "HI", "IDAHO": "ID", "ILLINOIS": "IL", "INDIANA": "IN", "IOWA": "IA",
    "KANSAS": "KS", "KENTUCKY": "KY", "LOUISIANA": "LA", "MAINE": "ME", "MARYLAND": "MD",
    "MASSACHUSETTS": "MA", "MICHIGAN": "MI", "MINNESOTA": "MN", "MISSISSIPPI": "MS", "MISSOURI": "MO",
    "MONTANA": "MT", "NEBRASKA": "NE", "NEVADA": "NV", "NEW HAMPSHIRE": "NH", "NEW JERSEY": "NJ",
    "NEW MEXICO": "NM", "NEW YORK": "NY", "NORTH CAROLINA": "NC", "NORTH DAKOTA": "ND", "OHIO": "OH",
    "OKLAHOMA": "OK", "OREGON": "OR", "PENNSYLVANIA": "PA", "RHODE ISLAND": "RI", "SOUTH CAROLINA": "SC",
    "SOUTH DAKOTA": "SD", "TENNESSEE": "TN", "TEXAS": "TX", "UTAH": "UT", "VERMONT": "VT",
    "VIRGINIA": "VA", "WASHINGTON": "WA", "WEST VIRGINIA": "WV", "WISCONSIN": "WI", "WYOMING": "WY",
    "DISTRICT OF COLUMBIA": "DC", "PUERTO RICO": "PR", "GUAM": "GU", "AMERICAN SAMOA": "AS",
    "NORTHERN MARIANA ISLANDS": "MP", "U.S. VIRGIN ISLANDS": "VI", "US VIRGIN ISLANDS": "VI", "VIRGIN ISLANDS": "VI",
}
_CODES = set(_STATE_CODES.values())


def normalize_state(value: str | None) -> str | None:
    if not value or not value.strip():
        return None
    text = " ".join(value.strip().upper().replace(".", "").split())
    return text if text in _CODES else _STATE_CODES.get(text, text)


def normalize_location(city: str | None, state: str | None) -> str | None:
    city_value = " ".join(city.split()) if city else None
    state_value = normalize_state(state)
    return ", ".join(value for value in (city_value, state_value) if value) or None
