from __future__ import annotations
from datetime import date, timedelta
from typing import Dict, Iterable, List
from models import Transaction, WeeklyAggregate


def _week_start(target_date: date) -> date:
    return target_date - timedelta(days=target_date.weekday())


def _daterange(start_date: date, end_date: date) -> Iterable[date]:
    current = start_date
    while current <= end_date:
        yield current
        current += timedelta(days=7)


def aggregate_weekly(transactions: Iterable[Transaction], starting_balance: float) -> List[WeeklyAggregate]:
    transactions_list = list(transactions)
    if not transactions_list:
        return []

    by_week: Dict[date, Dict[str, float]] = {}
    for tx in transactions_list:
        week = _week_start(tx.date)
        bucket = by_week.setdefault(week, {"inflow": 0.0, "outflow": 0.0})
        if tx.amount >= 0:
            bucket["inflow"] += tx.amount
        else:
            bucket["outflow"] += abs(tx.amount)

    first_week = min(by_week.keys())
    last_week = max(by_week.keys())
    aggregates: List[WeeklyAggregate] = []
    balance = starting_balance

    for week_start in _daterange(first_week, last_week):
        totals = by_week.get(week_start, {"inflow": 0.0, "outflow": 0.0})
        inflow = totals["inflow"]
        outflow = totals["outflow"]
        net = inflow - outflow
        balance += net
        aggregates.append(
            WeeklyAggregate(
                week_start=week_start,
                inflow=round(inflow, 2),
                outflow=round(outflow, 2),
                net=round(net, 2),
                end_balance=round(balance, 2),
            )
        )

    return aggregates
