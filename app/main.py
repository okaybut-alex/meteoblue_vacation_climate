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

MONTH_NAMES = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December",
}


@app.get("/", tags=["health"])
def health() -> Dict[str, str]:
    """
    simple healthcheck
    """
    return {"status": "ok"}


@app.get("/climate/{city_name}", tags=["climate"])
def climate_for_city(city_name: str) -> Dict[str, Any]:
    """
    delivers climate (meteoblue modelclimate-day) for the selected city.
    """
    try:
        data = get_climate_for_city(city_name)
    except ValueError as e:
        # if city not configured
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        # error from meteoblue
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

    months = climate.get("month")
    temps = climate.get("temperature_mean_daily_max")
    precs = climate.get("precipitation_mean")
    suns = climate.get("sunshine_days")

    if not (months and temps and precs and suns):
        raise HTTPException(status_code=500, detail="Climate fields missing in meteoblue response")

    month_scores = []

    for i, month in enumerate(months):
        temp = temps[i]
        precip = precs[i]
        sunshine_days = suns[i]

        # einfache Heuristik: ca. 5h Sonne pro "sunshine day"
        sunshine_hours = sunshine_days * 5.0

        score = comfort_index(temp, precip, sunshine_hours)

        month_scores.append({
            "month": month,
            "month_name": MONTH_NAMES.get(month, str(month)),
            "temp": temp,
            "precip": precip,
            "sunshine_days": sunshine_days,
            "score": score
        })

    if not month_scores:
        raise HTTPException(status_code=500, detail="No usable climate data for scoring")

    top = sorted(month_scores, key=lambda x: x["score"], reverse=True)[:3]

    best = top[0]
    best_month_name = best["month_name"]

    summary = (
        f"The best month to visit {city_name} based on the climate comfort index "
        f"is {best_month_name}."
    )

    return {
        "city": city_name,
        "summary": summary,
        "best_months": top
    }