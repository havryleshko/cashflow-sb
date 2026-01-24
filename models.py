from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import List, Literal, Optional, TypedDict

RiskStatus = Literal["SAFE", "AT_RISK", "NEGATIVE"]
VolatilityLevel = Literal["LOW", "MEDIUM", "HIGH"]


@dataclass(frozen=True)
class Transaction:
    date: date
    amount: float
    is_inflow: bool
    category: Optional[str] = None


@dataclass(frozen=True)
class WeeklyAggregate:
    week_start: date
    inflow: float
    outflow: float
    net: float
    end_balance: float


@dataclass(frozen=True)
class ForecastPoint:
    week_start: date
    cash_balance: float


@dataclass(frozen=True)
class RiskAssessment:
    status: RiskStatus
    runway_weeks: int
    volatility: VolatilityLevel


class ForecastPointDict(TypedDict):
    week: str
    cash_balance: float


class LowestCashDict(TypedDict):
    amount: float
    date: str


class FinalOutputDict(TypedDict):
    forecast: List[ForecastPointDict]
    lowest_cash: LowestCashDict
    status: RiskStatus
    runway_weeks: int
    volatility: VolatilityLevel
    drivers: List[str]
    actions: List[str]
