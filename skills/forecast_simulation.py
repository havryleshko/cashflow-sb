from __future__ import annotations
from datetime import date, timedelta
from statistics import mean
from typing import Iterable, List
from models import ForecastPoint, WeeklyAggregate


def _next_week_start(week_start: date) -> date:
    return week_start + timedelta(days=7)


def simulate_forecast(
    weekly_aggregates: Iterable[WeeklyAggregate],
    weeks: int = 12,
    starting_balance: float = 0.0,
) -> List[ForecastPoint]:
    aggregates = list(weekly_aggregates)
    if aggregates:
        recent_net = [item.net for item in aggregates[-8:]]
        baseline_net = mean(recent_net) if recent_net else 0.0
        last_balance = aggregates[-1].end_balance
        last_week = aggregates[-1].week_start
    else:
        baseline_net = 0.0
        last_balance = starting_balance
        last_week = date.today()

    forecast: List[ForecastPoint] = []
    balance = last_balance
    week_start = _next_week_start(last_week)

    for _ in range(weeks):
        balance += baseline_net
        forecast.append(
            ForecastPoint(week_start=week_start, cash_balance=round(balance, 2))
        )
        week_start = _next_week_start(week_start)

    return forecast
