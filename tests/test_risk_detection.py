from __future__ import annotations

from datetime import date
from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from models import ForecastPoint, WeeklyAggregate
from skills.risk_detection import detect_risk


class RiskDetectionTests(unittest.TestCase):
    def test_detect_risk_negative(self) -> None:
        forecast = [
            ForecastPoint(week_start=date(2026, 1, 12), cash_balance=100.0),
            ForecastPoint(week_start=date(2026, 1, 19), cash_balance=-50.0),
        ]
        weekly = [
            WeeklyAggregate(
                week_start=date(2026, 1, 5),
                inflow=500.0,
                outflow=600.0,
                net=-100.0,
                end_balance=900.0,
            )
        ]

        risk = detect_risk(forecast, weekly)
        self.assertEqual(risk.status, "NEGATIVE")
        self.assertEqual(risk.runway_weeks, 2)


if __name__ == "__main__":
    unittest.main()
