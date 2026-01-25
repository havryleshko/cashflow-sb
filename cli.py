from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
from orchestrator import run_cashflow_analysis


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Cashflow forecast CLI")
    parser.add_argument("csv_path", nargs="?", help="Path to transactions CSV")
    parser.add_argument("starting_balance", nargs="?", type=float, help="Starting cash balance")
    parser.add_argument("--csv", dest="csv_path_flag", help="Path to transactions CSV")
    parser.add_argument(
        "--starting-balance",
        dest="starting_balance_flag",
        type=float,
        help="Starting cash balance",
    )
    parser.add_argument("--weeks", type=int, default=12, help="Forecast weeks (default: 12)")
    parser.add_argument(
        "--report-out",
        help="Optional path to save the report text",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    csv_path = args.csv_path_flag or args.csv_path
    starting_balance = (
        args.starting_balance_flag if args.starting_balance_flag is not None else args.starting_balance
    )

    if not csv_path or starting_balance is None:
        raise SystemExit("csv path and starting balance are required")

    output, report = run_cashflow_analysis(
        csv_path=Path(csv_path),
        starting_balance=starting_balance,
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
