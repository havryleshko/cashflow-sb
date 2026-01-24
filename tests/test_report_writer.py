from __future__ import annotations

from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from skills.report_writer import generate_report


class ReportWriterTests(unittest.TestCase):
    def test_generate_report_fallback_template(self) -> None:
        final_output = {
            "forecast": [],
            "lowest_cash": {"amount": -10.0, "date": "2026-01-19"},
            "status": "AT_RISK",
            "runway_weeks": 3,
            "volatility": "MEDIUM",
            "drivers": ["Expense spike week of 2026-01-12"],
            "actions": ["Delay non-essential expenses"],
        }

        report = generate_report(final_output, "missing_prompt.txt")
        self.assertIn("Status: AT_RISK", report)


if __name__ == "__main__":
    unittest.main()
