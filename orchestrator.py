from __future__ import annotations
import csv
from datetime import date
from pathlib import Path
from typing import Iterable, List, Tuple

from models import (
    FinalOutputDict,
    ForecastPoint,
    ForecastPointDict,
    LowestCashDict,
    RiskAssessment,
    Transaction,
    WeeklyAggregate,
)
from skills.aggregate_cash import aggregate_weekly
from skills.forecast_simulation import simulate_forecast
from skills.normalize_data import normalize_transactions
from skills.pattern_insights import identify_drivers
from skills.recommendations import recommend_actions
from skills.report_writer import generate_report
from skills.risk_detection import detect_risk


def load_csv_rows(csv_path: str | Path) -> List[dict]:
    path = Path(csv_path)
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return list(reader)


def _format_forecast(forecast: Iterable[ForecastPoint]) -> List[ForecastPointDict]:
    return [
        {"week": point.week_start.isoformat(), "cash_balance": round(point.cash_balance, 2)}
        for point in forecast
    ]


def _lowest_cash(forecast: Iterable[ForecastPoint]) -> LowestCashDict:
    forecast_list = list(forecast)
    if not forecast_list:
        return {"amount": 0.0, "date": date.today().isoformat()}
    lowest = min(forecast_list, key=lambda point: point.cash_balance)
    return {"amount": round(lowest.cash_balance, 2), "date": lowest.week_start.isoformat()}


def build_final_output(
    forecast: Iterable[ForecastPoint],
    risk: RiskAssessment,
    drivers: List[str],
    actions: List[str],
) -> FinalOutputDict:
    return {
        "forecast": _format_forecast(forecast),
        "lowest_cash": _lowest_cash(forecast),
        "status": risk.status,
        "runway_weeks": risk.runway_weeks,
        "volatility": risk.volatility,
        "drivers": drivers,
        "actions": actions,
    }


def run_cashflow_analysis(
    csv_path: str | Path,
    starting_balance: float,
    forecast_weeks: int = 12,
    report_prompt_path: str | Path = "prompts/report_prompt.txt",
) -> Tuple[FinalOutputDict, str]:
    raw_rows = load_csv_rows(csv_path)
    normalized = normalize_transactions(raw_rows)
    weekly = aggregate_weekly(normalized, starting_balance)
    forecast = simulate_forecast(weekly, forecast_weeks, starting_balance=starting_balance)
    risk = detect_risk(forecast, weekly)
    drivers = identify_drivers(normalized, weekly, forecast)
    actions = recommend_actions(risk.status, drivers)
    final_output = build_final_output(forecast, risk, drivers, actions)
    report = generate_report(final_output, report_prompt_path)
    return final_output, report


__all__ = [
    "Transaction",
    "WeeklyAggregate",
    "ForecastPoint",
    "RiskAssessment",
    "FinalOutputDict",
    "run_cashflow_analysis",
]
