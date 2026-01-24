from __future__ import annotations

from datetime import date
from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from models import Transaction
from skills.aggregate_cash import aggregate_weekly


class AggregateCashTests(unittest.TestCase):
    def test_aggregate_weekly_creates_cumulative_balance(self) -> None:
        transactions = [
            Transaction(date=date(2026, 1, 1), amount=500.0, is_inflow=True),
            Transaction(date=date(2026, 1, 2), amount=-200.0, is_inflow=False),
        ]

        weekly = aggregate_weekly(transactions, starting_balance=1000.0)
        self.assertEqual(len(weekly), 1)
        self.assertAlmostEqual(weekly[0].net, 300.0)
        self.assertAlmostEqual(weekly[0].end_balance, 1300.0)


if __name__ == "__main__":
    unittest.main()
