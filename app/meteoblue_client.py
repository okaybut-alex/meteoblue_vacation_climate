import requests
from typing import Dict, Any
from app.config import METEOBLUE_API_KEY

# Vorkonfigurierte Städte (kannst du erweitern)
CITY_COORDS = {
    "Basel": {
        "lat": 47.558,
        "lon": 7.573,
        "asl": 279,
        "tz": "Europe/Zurich"
    },
    "Berlin": {
        "lat": 52.52,
        "lon": 13.405,
        "asl": 34,
        "tz": "Europe/Berlin"
    }
    # weitere Städte später nach Bedarf hinzufügen
}

BASE_URL = "https://my.meteoblue.com/packages/modelclimate-day"


def normalize_city_name(city_name: str) -> str:
    """
    Kleine Normalisierung, damit 'basel', 'BASEL' etc. funktionieren.
    """
    name = city_name.strip()
    # simple Variante: first letter upper, Rest lower
    name = name[0].upper() + name[1:].lower() if name else name
    return name


def get_climate_for_city(city_name: str) -> Dict[str, Any]:
    """
    Ruft die meteoblue Climate-API (modelclimate-day) für eine Stadt auf
    und gibt das JSON direkt zurück.
    """
    normalized = normalize_city_name(city_name)

    if normalized not in CITY_COORDS:
        raise ValueError(f"City '{city_name}' is not configured in CITY_COORDS")

    cfg = CITY_COORDS[normalized]

    params = {
        "lat": cfg["lat"],
        "lon": cfg["lon"],
        "asl": cfg["asl"],
        "startdate": "2020-01-01",
        "enddate": "2020-12-31",
        "tz": cfg["tz"],
        "name": normalized,
        "format": "json",
        "apikey": METEOBLUE_API_KEY,
        # modelclimate-day ist über die URL gewählt, kein 'package'-Parameter nötig
    }

    response = requests.get(BASE_URL, params=params, timeout=15)

    if response.status_code != 200:
        # Für Debug könnt ihr hier auch response.text loggen
        raise RuntimeError(
            f"meteoblue API error {response.status_code}: {response.text[:200]}"
        )

    return response.json()