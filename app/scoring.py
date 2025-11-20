def temp_score(t: float) -> float:
    """
    Idealtemperatur ~24°C, je weiter weg, desto schlechter.
    10–32°C = ok, darunter/darüber 0 Punkte.
    """
    if t < 10 or t > 32:
        return 0.0
    ideal = 24.0
    return max(0.0, 10.0 - abs(t - ideal))  # 0..10


def precip_score(p: float) -> float:
    """
    0 mm = 10 Punkte, 100+ mm = 0.
    Linearer Abfall dazwischen.
    """
    if p <= 0:
        return 10.0
    if p >= 100:
        return 0.0
    return 10.0 * (1.0 - (p / 100.0))


def sunshine_score(h: float) -> float:
    """
    0 Stunden = 0, 10+ Stunden = 10.
    """
    if h <= 0:
        return 0.0
    if h >= 10:
        return 10.0
    return h  # 0..10


def comfort_index(temp: float, precip: float, sunshine: float) -> float:
    """
    Kombiniert Temperatur, Niederschlag und Sonnenscheindauer.

    Rückgabe: 0..10 (höher = besser)
    """
    scores = [
        temp_score(temp),
        precip_score(precip),
        sunshine_score(sunshine),
    ]
    return round(sum(scores) / len(scores), 2)