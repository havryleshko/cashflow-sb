from __future__ import annotations
from typing import List
from models import RiskStatus

def _unique_actions(actions: List[str]) -> List[str]:
    seen = set()
    unique = []
    for action in actions:
        if action not in seen:
            seen.add(action)
            unique.append(action)
    return unique


def recommend_actions(status: RiskStatus, drivers: List[str]) -> List[str]:
    actions: List[str] = []

    if status in {"NEGATIVE", "AT_RISK"}:
        actions.extend(
            [
                "Invoice clients earlier and follow up on late payments",
                "Delay or reduce non-essential expenses in the next 4 weeks",
                "Maintain a cash buffer equal to at least 4 weeks of outflows",
            ]
        )
    else:
        actions.extend(
            [
                "Keep invoicing promptly to maintain steady inflows",
                "Review expenses monthly to avoid unexpected spikes",
                "Maintain a cash buffer equal to at least 4 weeks of outflows",
            ]
        )

    for driver in drivers:
        if "Expense spike" in driver:
            actions.append("Audit large expenses and reschedule discretionary spend")
        if "Revenue irregularity" in driver:
            actions.append("Smooth revenue timing with retainer or milestone billing")
        if "Projected cash decline" in driver:
            actions.append("Prepare a short-term cash plan for the forecast period")

    actions = _unique_actions(actions)
    if len(actions) < 3:
        actions.append("Monitor cash weekly to catch early warning signals")

    return actions[:3]
