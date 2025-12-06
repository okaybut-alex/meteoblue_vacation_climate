def temp_score(t: float) -> float:
    """
    ideal temperature ~24°C, the further away, the worse.
    10–32°C = ok, below/above 0 Punkte.
    """
    if t < 10 or t > 32:
        return 0.0
    ideal = 24.0
    return max(0.0, 10.0 - abs(t - ideal))  # 0..10


def precip_score(p: float) -> float:
    """
    0 mm = 10 points, 100+ mm = 0.
    linear decline in between.
    """
    if p <= 0:
        return 10.0
    if p >= 100:
        return 0.0
    return 10.0 * (1.0 - (p / 100.0))


def sunshine_score(h: float) -> float:
    """
    0 hours = 0, 10+ hours = 10.
    """
    if h <= 0:
        return 0.0
    if h >= 10:
        return 10.0
    return h  # 0..10


def comfort_index(temp: float, precip: float, sunshine: float) -> float:
    """
    combines temperature, precipitation and sunshine duration.

    return: 0..10 (higher = better)
    """
    scores = [
        temp_score(temp),
        precip_score(precip),
        sunshine_score(sunshine),
    ]
    return round(sum(scores) / len(scores), 2)