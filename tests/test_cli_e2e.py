from __future__ import annotations
import json
from pathlib import Path
import subprocess
import sys
import unittest


class CliE2ETests(unittest.TestCase):
    def test_cli_outputs_valid_json(self) -> None:
        project_root = Path(__file__).resolve().parents[1]
        csv_path = project_root / "tests" / "fixtures" / "transactions.csv"

        result = subprocess.run(
            [
                sys.executable,
                str(project_root / "cli.py"),
                "--csv",
                str(csv_path),
                "--starting-balance",
                "10000",
                "--weeks",
                "8",
            ],
            check=False,
            capture_output=True,
            text=True,
            cwd=project_root,
        )

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        payload = json.loads(result.stdout)
        for key in ("forecast", "lowest_cash", "status", "runway_weeks", "volatility", "drivers", "actions"):
            self.assertIn(key, payload)


if __name__ == "__main__":
    unittest.main()
