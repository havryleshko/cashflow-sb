# CashFlow AI MVP — System Design Document

## CashFlow AI MVP  
## Date 2026-01-23  

---

## 1. Purpose

Provide small service-based business owners with info into of cash flow for the next 8–12 weeks.  

**Primary job:**  
> “Will I run out of cash? If yes, when, why, and what can I do about it?”

**Constraints:**
- Deterministic core for reliability  
- LLM only for explanation, not calculations  
- CLI / notebook interface for MVP  
- No SaaS hosting required for initial validation

---

## 2. Scope

**In Scope (v1):**
- Input: historical transactions + starting balance  
- Output: cash forecast, lowest balance, status, runway, volatility, drivers, concrete actions  
- Modular skills pipeline  
- Human-readable report generation (LLM)

**Out of Scope:**
- Full P&L / balance sheets  
- Charts / dashboards (optional)  
- Automated bank integrations  
- End-to-end autonomous agents  


## 3. Users / ICP

**Primary Users:**  
- Service-based small business owners (consultants, agencies, freelancers)  

**Pain Points:**  
- Cash unpredictability  
- Late invoices  
- Expense spikes  

**User Goals:**
1. Know if and when cash will run out  
2. Understand top drivers of risk  
3. Receive actionable recommendations  

---

## 4. Inputs & Outputs

**Inputs:**
| Name | Type | Notes |
|------|------|-------|
| Transactions | CSV / table | Date, Amount, optional category |
| Starting balance | Number | Initial cash on hand |

**Outputs (structured JSON):**
```json
{
  "forecast": [
    {"week":"2026-03-02","cash_balance":12500},
    ...
  ],
  "lowest_cash": {"amount":-3200,"date":"2026-04-13"},
  "status": "AT_RISK",
  "runway_weeks": 6,
  "volatility": "HIGH",
  "drivers": [
    "Invoices paid late ~12 days",
    "Expense spike week 5"
  ],
  "actions": [
    "Invoice clients earlier",
    "Delay £1,500 expenses",
    "Maintain £5,000 buffer"
  ]
}

## SKILLS (refer to Anthropic documentation for guidance)

1. **Data Normalization**  
   - **Purpose:** Clean and standardize raw transaction data for downstream processing.  
   - **Input:** Raw CSV or table of transactions (date, amount, optional category).  
   - **Output:** Cleaned transactions with inflow/outflow labeled, dates normalized, duplicates removed.  

2. **Cash Aggregation**  
   - **Purpose:** Convert cleaned transactions into weekly cash movement.  
   - **Input:** Cleaned transactions + starting cash balance.  
   - **Output:** Weekly inflows, outflows, net cash per week, cumulative balances.  

3. **Forecast Simulation**  
   - **Purpose:** Project cash forward 8–12 weeks under multiple scenarios.  
   - **Input:** Weekly net cash data.  
   - **Output:** Baseline, conservative, and stress forecasts; lowest projected balance.  

4. **Risk Detection**  
   - **Purpose:** Assess financial risk based on forecasted cash balances.  
   - **Input:** Forecast output.  
   - **Output:** Status (SAFE / AT_RISK / NEGATIVE), runway in weeks, volatility indicator (LOW / MEDIUM / HIGH).  

5. **Driver Identification**  
   - **Purpose:** Identify main factors driving cash flow risk.  
   - **Input:** Historical transactions + forecast data.  
   - **Output:** Top 1–3 drivers (e.g., late invoices, expense spikes, revenue irregularities).  

6. **Action Recommendation**  
   - **Purpose:** Turn detected risks and drivers into concrete actions for the user.  
   - **Input:** Drivers + risk status.  
   - **Output:** 3 actionable steps (e.g., invoice earlier, delay expenses, maintain cash buffer).  

7. **Report / Explanation**  
   - **Purpose:** Summarize results in human-readable form.  
   - **Input:** Structured outputs from all previous skills.  
   - **Output:** Plain English report including forecast summary, risk status, top drivers, and recommended actions.  

**Notes:**  
- Skills 1–6 are deterministic.  
- Skill 7 uses LLM **only** for explanation and reporting.  
- Each skill maps directly to required outputs and is modular for future expansion.


## SKILLS architecture

[ USER INPUT ]
CSV of transactions + starting balance
        │
        ▼
[ ORCHESTRATOR / CLI ]
Coordinates all modules, calls each skill in order
        │
        ▼
[ SKILLS LAYER ]
  ┌─────────────────────────────┐
  │ 1. Data Normalization       │ --> cleans raw data
  │ 2. Cash Aggregation         │ --> sums weekly inflows/outflows
  │ 3. Forecast Simulation      │ --> projects cash for 8–12 weeks
  │ 4. Risk Detection           │ --> flags at-risk weeks, runway, volatility
  │ 5. Driver Identification    │ --> identifies top causes of cash issues
  │ 6. Action Recommendation    │ --> produces actionable steps
  │ 7. Report / Explanation (LLM) │ --> creates human-readable report
  └─────────────────────────────┘
        │
        ▼
[ OUTPUTS ]
  - JSON: structured data for programmatic use
  - Human-readable report: plain English summary + actions


## Execution Flow


Load Input
Parse CSV, read starting balance
Normalize Transactions (Skill 1)
Aggregate Weekly Cash (Skill 2)
Simulate Forecast (Skill 3)
Detect Risk (Skill 4)
Identify Drivers (Skill 5)
Recommend Actions (Skill 6)
Generate Report (Skill 7, LLM)
Return Outputs (structured + human-readable)

## Technical Considerations
Language: Python
Execution: CLI / Jupyter Notebook
ML/LLM: LLM only for explanation/report
Testing: Unit tests for each skill
Extensibility: Skills are modular, orchestrator is thin
Validation: Manual processing for first users, later automation possible

## Success metrics


| Metric                         | Target                                   |
| ------------------------------ | ---------------------------------------- |
| Forecast accuracy (8–12 weeks) | ±10–15%                                  |
| Action usefulness              | 80% of users confirm recommendations     |
| Delivery time                  | < 5 seconds per dataset                  |
| Adoption                       | Initial 5–10 users validate CLI workflow |



## Optional post-MVP plan just not to forget it

Add optional categories & known future events
Add visualization & dashboards
Optional integration with banks / accounting software
Transition to agent-orchestrated skill calls
Extend forecasting beyond 12 weeks

## repo structure

cashflow-sb/
├── skills/
│   ├── normalize_data.py
│   ├── aggregate_cash.py
│   ├── forecast_simulation.py
│   ├── risk_detection.py
│   ├── pattern_insights.py
│   ├── recommendations.py
│   └── report_writer.py
│
├── orchestrator.py
├── cli.py
├── prompts/
│   └── report_prompt.txt
├── tests/
└── README.md
