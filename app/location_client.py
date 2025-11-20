import requests
from typing import Dict
from app.config import METEOBLUE_API_KEY

BASE_URL = "https://www.meteoblue.com/en/server/search/query3"


def search_location(query: str) -> Dict:
    """
    Lookup for a location using the meteoblue Location Search API.
    Returns basic info including lat, lon, elevation (asl).
    """
    params = {
        "query": query,
        "format": "json",
        "apikey": METEOBLUE_API_KEY,
    }

    resp = requests.get(BASE_URL, params=params, timeout=10)

    if resp.status_code != 200:
        raise RuntimeError(f"meteoblue Location API error {resp.status_code}: {resp.text[:200]}")

    data = resp.json()

    results = data.get("results", [])
    if not results:
        raise ValueError(f"No location found for '{query}'")

    loc = results[0]

    return {
        "name": loc.get("name"),
        "country": loc.get("country"),
        "lat": loc.get("lat"),
        "lon": loc.get("lon"),
        "asl": loc.get("asl", 0),
    }