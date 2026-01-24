from __future__ import annotations

from datetime import date
from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from models import ForecastPoint, Transaction, WeeklyAggregate
from skills.pattern_insights import identify_drivers


class PatternInsightsTests(unittest.TestCase):
    def test_identify_drivers_detects_spike(self) -> None:
        transactions = [
            Transaction(date=date(2026, 1, 1), amount=-100.0, is_inflow=False),
        ]
        weekly = [
            WeeklyAggregate(
                week_start=date(2026, 1, 5),
                inflow=1000.0,
                outflow=200.0,
                net=800.0,
                end_balance=1800.0,
            ),
            WeeklyAggregate(
                week_start=date(2026, 1, 12),
                inflow=1000.0,
                outflow=1200.0,
                net=-200.0,
                end_balance=1600.0,
            ),
        ]
        forecast = [
            ForecastPoint(week_start=date(2026, 1, 19), cash_balance=1500.0),
            ForecastPoint(week_start=date(2026, 1, 26), cash_balance=1400.0),
        ]

        drivers = identify_drivers(transactions, weekly, forecast)
        self.assertTrue(any("Expense spike" in item for item in drivers))


if __name__ == "__main__":
    unittest.main()
