from __future__ import annotations
from pathlib import Path
from typing import List
from models import FinalOutputDict


def _join_list(items: List[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def _render_template(template: str, data: FinalOutputDict) -> str:
    return template.format(
        status=data["status"],
        runway_weeks=data["runway_weeks"],
        lowest_cash_amount=data["lowest_cash"]["amount"],
        lowest_cash_date=data["lowest_cash"]["date"],
        drivers=_join_list(data["drivers"]),
        actions=_join_list(data["actions"]),
    )


def generate_report(final_output: FinalOutputDict, prompt_path: str | Path) -> str:
    path = Path(prompt_path)
    if path.exists():
        template = path.read_text(encoding="utf-8")
    else:
        template = (
            "Cashflow summary\n"
            "Status: {status}\n"
            "Runway (weeks): {runway_weeks}\n"
            "Lowest cash: {lowest_cash_amount} on {lowest_cash_date}\n\n"
            "Top drivers:\n{drivers}\n\n"
            "Recommended actions:\n{actions}\n"
        )

    return _render_template(template, final_output)
