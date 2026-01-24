from __future__ import annotations
from statistics import mean, pstdev
from typing import Iterable, List
from models import ForecastPoint, Transaction, WeeklyAggregate


def identify_drivers(
    transactions: Iterable[Transaction],
    weekly_aggregates: Iterable[WeeklyAggregate],
    forecast: Iterable[ForecastPoint],
) -> List[str]:
    drivers: List[str] = []
    weekly = list(weekly_aggregates)
    forecast_list = list(forecast)

    if weekly:
        avg_outflow = mean(item.outflow for item in weekly)
        avg_inflow = mean(item.inflow for item in weekly)
        outflow_std = pstdev([item.outflow for item in weekly]) if len(weekly) > 1 else 0.0
        inflow_std = pstdev([item.inflow for item in weekly]) if len(weekly) > 1 else 0.0

        if avg_outflow > 0 and outflow_std > avg_outflow * 0.5:
            spike_week = max(weekly, key=lambda item: item.outflow)
            drivers.append(f"Expense spike week of {spike_week.week_start.isoformat()}")

        if avg_inflow > 0 and inflow_std > avg_inflow * 0.5:
            drivers.append("Revenue irregularity across recent weeks")

    if forecast_list:
        if forecast_list[-1].cash_balance < forecast_list[0].cash_balance:
            drivers.append("Projected cash decline over forecast period")

    if not drivers:
        drivers.append("Cash flow stable with no major anomalies detected")

    return drivers[:3]
