from __future__ import annotations
from statistics import mean, pstdev
from typing import Iterable
from models import ForecastPoint, RiskAssessment, VolatilityLevel, WeeklyAggregate


def _volatility_level(nets: list[float]) -> VolatilityLevel:
    if len(nets) < 2:
        return "LOW"

    avg = mean(nets)
    std = pstdev(nets)
    if abs(avg) < 1e-6:
        if std < 100:
            return "LOW"
        if std < 500:
            return "MEDIUM"
        return "HIGH"

    ratio = std / abs(avg)
    if ratio < 0.25:
        return "LOW"
    if ratio < 0.75:
        return "MEDIUM"
    return "HIGH"


def detect_risk(
    forecast_points: Iterable[ForecastPoint],
    weekly_aggregates: Iterable[WeeklyAggregate],
) -> RiskAssessment:
    forecast = list(forecast_points)
    weekly = list(weekly_aggregates)

    if not forecast:
        return RiskAssessment(status="SAFE", runway_weeks=0, volatility="LOW")

    lowest_balance = min(point.cash_balance for point in forecast)
    runway_weeks = len(forecast)
    for idx, point in enumerate(forecast, start=1):
        if point.cash_balance < 0:
            runway_weeks = idx
            break

    avg_outflow = mean([item.outflow for item in weekly]) if weekly else 0.0
    nets = [item.net for item in weekly] if weekly else []

    if lowest_balance < 0:
        status = "NEGATIVE"
    elif runway_weeks <= 4 or (avg_outflow > 0 and lowest_balance < avg_outflow):
        status = "AT_RISK"
    else:
        status = "SAFE"

    volatility = _volatility_level(nets)
    return RiskAssessment(status=status, runway_weeks=runway_weeks, volatility=volatility)
