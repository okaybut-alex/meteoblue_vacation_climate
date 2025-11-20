from fastapi import FastAPI

app = FastAPI(title="Travel Weather Advisor API")

@app.get("/")
def health():
    return {"status": "ok"}

from fastapi import FastAPI, HTTPException
from typing import Any, Dict
from app.meteoblue_client import get_climate_for_city

app = FastAPI(
    title="meteoblue Vacation Climate API",
    version="0.1.0",
    description="Prototype API to explore long-term climate data for travel planning."
)


@app.get("/", tags=["health"])
def health() -> Dict[str, str]:
    """
    Einfacher Healthcheck – gut für Screenshots und zum Testen.
    """
    return {"status": "ok"}


@app.get("/climate/{city_name}", tags=["climate"])
def climate_for_city(city_name: str) -> Dict[str, Any]:
    """
    Liefert die Climate-Daten (meteoblue modelclimate-day) für eine konfigurierte Stadt.
    """
    try:
        data = get_climate_for_city(city_name)
    except ValueError as e:
        # City nicht in CITY_COORDS konfiguriert
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        # Fehler von meteoblue
        raise HTTPException(status_code=502, detail=str(e))

    return data