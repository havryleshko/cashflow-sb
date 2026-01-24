from __future__ import annotations
from datetime import datetime
from typing import Iterable, List, Optional
from models import Transaction


_DATE_FORMATS = ("%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y")


def _parse_date(value: str) -> datetime.date:
    value = value.strip()
    for fmt in _DATE_FORMATS:
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue
    raise ValueError(f"Unsupported date format: {value}")


def _parse_amount(value: str) -> float:
    cleaned = value.strip().replace(",", "")
    if cleaned.startswith("(") and cleaned.endswith(")"):
        cleaned = "-" + cleaned[1:-1]
    cleaned = cleaned.replace("$", "").replace("£", "").replace("€", "")
    return float(cleaned)


def _get_field(row: dict, field_names: Iterable[str]) -> Optional[str]:
    lowered = {str(key).strip().lower(): key for key in row.keys()}
    for field in field_names:
        key = lowered.get(field)
        if key is not None:
            value = row.get(key)
            if value is not None:
                return str(value)
    return None


def normalize_transactions(raw_rows: Iterable[dict]) -> List[Transaction]:
    normalized: List[Transaction] = []
    seen = set()

    for row in raw_rows:
        date_value = _get_field(row, ("date", "transaction_date"))
        amount_value = _get_field(row, ("amount", "value", "total"))

        if not date_value or not amount_value:
            continue

        category_value = _get_field(row, ("category", "type", "label"))
        parsed_date = _parse_date(date_value)
        parsed_amount = _parse_amount(amount_value)
        is_inflow = parsed_amount >= 0

        signature = (parsed_date, parsed_amount, category_value or "")
        if signature in seen:
            continue
        seen.add(signature)

        normalized.append(
            Transaction(
                date=parsed_date,
                amount=parsed_amount,
                is_inflow=is_inflow,
                category=category_value,
            )
        )

    return sorted(normalized, key=lambda item: item.date)
