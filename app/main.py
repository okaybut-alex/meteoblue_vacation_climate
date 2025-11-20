from fastapi import FastAPI

app = FastAPI(title="Travel Weather Advisor API")

@app.get("/")
def health():
    return {"status": "ok"}

from fastapi import FastAPI, HTTPException
from typing import Any, Dict
from app.meteoblue_client import get_climate_for_city
from app.scoring import comfort_index

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
@app.get("/recommendation/city/{city_name}", tags=["recommendation"])
def best_time_for_city(city_name: str) -> Dict[str, Any]:
    """
    Returns the best months to visit a city based on monthly climate normals.
    
    Uses:
    - temperature_mean_daily_max  (°C, ideal around 24°C)
    - precipitation_mean          (mm, less is better)
    - sunshine_days               (days/month, more is better)
    """

    try:
        raw = get_climate_for_city(city_name)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))

    climate = raw.get("data_modelclimate")
    if not climate:
        raise HTTPException(status_code=500, detail="No modelclimate data found in response")

    # Monate (1..12)
    months = climate.get("month")

    # Temperatur: daily max (beste Proxy für “Sommergefühl”)
    temps = climate.get("temperature_mean_daily_max")

    # Niederschlag
    precs = climate.get("precipitation_mean")

    # Sonnentage (ist alles, was wir haben)
    suns = climate.get("sunshine_days")

    if not (months and temps and precs and suns):
        raise HTTPException(status_code=500, detail="Climate fields missing in meteoblue response")

    month_scores = []

    for i, month in enumerate(months):
        temp = temps[i]
        precip = precs[i]
        sunshine_days = suns[i]  # 0..31

        # Machen wir daraus einen Stundenwert (notwendig für sunshine_score)
        sunshine_hours = sunshine_days * 5  # pragmatische Heuristik: 5h pro sunshine_day

        score = comfort_index(temp, precip, sunshine_hours)

        month_scores.append({
            "month": month,
            "temp": temp,
            "precip": precip,
            "sunshine_days": sunshine_days,
            "score": score
        })

    # Top 3 Monate
    top = sorted(month_scores, key=lambda x: x["score"], reverse=True)[:3]

    return {
        "city": city_name,
        "best_months": top
    }