from __future__ import annotations

from datetime import date
from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from models import WeeklyAggregate
from skills.forecast_simulation import simulate_forecast


class ForecastSimulationTests(unittest.TestCase):
    def test_simulate_forecast_projects_weeks(self) -> None:
        weekly = [
            WeeklyAggregate(
                week_start=date(2026, 1, 5),
                inflow=1000.0,
                outflow=500.0,
                net=500.0,
                end_balance=1500.0,
            )
        ]

        forecast = simulate_forecast(weekly, weeks=4)
        self.assertEqual(len(forecast), 4)
        self.assertGreaterEqual(forecast[0].cash_balance, 1500.0)


if __name__ == "__main__":
    unittest.main()
