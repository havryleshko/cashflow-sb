from __future__ import annotations
from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from skills.normalize_data import normalize_transactions


class NormalizeDataTests(unittest.TestCase):
    def test_normalize_transactions_parses_amounts(self) -> None:
        raw_rows = [
            {"Date": "2026-01-01", "Amount": "1000", "Category": "Income"},
            {"date": "2026-01-02", "amount": "-200"},
        ]

        normalized = normalize_transactions(raw_rows)
        self.assertEqual(len(normalized), 2)
        self.assertTrue(normalized[0].is_inflow)
        self.assertFalse(normalized[1].is_inflow)
        self.assertEqual(normalized[1].amount, -200.0)


if __name__ == "__main__":
    unittest.main()
