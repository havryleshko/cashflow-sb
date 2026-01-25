# CashFlow AI MVP

Deterministic cashflow pipeline with an optional OpenAI-generated report.

## Setup

```bash
pip install -r requirements.txt
```

Environment variables:
- `OPENAI_API_KEY` (required for OpenAI report generation)
- `OPENAI_REPORT_MODEL` (optional, defaults to `gpt-4o-mini`)

## CSV schema

Required headers:
- `Date` (supported formats: `YYYY-MM-DD`, `MM/DD/YYYY`, `DD/MM/YYYY`)
- `Amount` (positive for inflow, negative for outflow; currency symbols allowed)

Optional headers:
- `Category`

## CLI usage

```bash
python cli.py --csv path/to/transactions.csv --starting-balance 12000 --weeks 10
```

Report output goes to stderr by default. To save it:

```bash
python cli.py --csv path/to/transactions.csv --starting-balance 12000 --report-out report.txt
```
