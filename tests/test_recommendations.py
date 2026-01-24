from __future__ import annotations

from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from skills.recommendations import recommend_actions


class RecommendationsTests(unittest.TestCase):
    def test_recommend_actions_returns_three(self) -> None:
        actions = recommend_actions("AT_RISK", ["Expense spike week of 2026-01-12"])
        self.assertEqual(len(actions), 3)


if __name__ == "__main__":
    unittest.main()
