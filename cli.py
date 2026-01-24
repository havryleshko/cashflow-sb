from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
from orchestrator import run_cashflow_analysis


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Cashflow forecast CLI")
    parser.add_argument("csv_path", help="Path to transactions CSV")
    parser.add_argument("starting_balance", type=float, help="Starting cash balance")
    parser.add_argument("--weeks", type=int, default=12, help="Forecast weeks (default: 12)")
    parser.add_argument(
        "--report-out",
        help="Optional path to save the report text",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output, report = run_cashflow_analysis(
        csv_path=Path(args.csv_path),
        starting_balance=args.starting_balance,
        forecast_weeks=args.weeks,
    )

    print(json.dumps(output, indent=2))

    if args.report_out:
        Path(args.report_out).write_text(report, encoding="utf-8")
    else:
        sys.stderr.write("\n--- Cashflow Report ---\n")
        sys.stderr.write(report + "\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
