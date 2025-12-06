import requests
from typing import Dict, Any
from app.config import METEOBLUE_API_KEY
from app.location_client import search_location

BASE_URL = "https://my.meteoblue.com/packages/modelclimate-day"


def get_climate_for_city(city_name: str) -> Dict[str, Any]:
    """
    Uses the Location Search API to get coordinates and then calls
    the meteoblue modelclimate-day API for that location.
    """
    # 1) Location Lookup
    loc = search_location(city_name)

    params = {
        "lat": loc["lat"],
        "lon": loc["lon"],
        "asl": loc["asl"],
        "startdate": "2020-01-01",
        "enddate": "2020-12-31",
        "tz": "Europe/Zurich",
        "name": loc["name"],
        "format": "json",
        "apikey": METEOBLUE_API_KEY,
        # 'package' is implicitly in the URL (modelclimate-day)
    }

    resp = requests.get(BASE_URL, params=params, timeout=20)

    if resp.status_code != 200:
        raise RuntimeError(f"meteoblue Climate API error {resp.status_code}: {resp.text[:200]}")

    return resp.json()