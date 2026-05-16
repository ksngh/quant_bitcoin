# Task 029: Implement Swing Structure

# Goal

Implement deterministic Swing Structure classification from already-provided candle data and/or owner-approved pivot points.

This task must classify market structure only. It must not fetch market data, place orders, call exchange APIs, or make live-trading decisions.

# Source Requirement

Owner listed Swing Structure as one of the remaining indicators to add on 2026-05-16.

Detailed formulas, default parameters, output schema, and edge-case behavior are not yet fully specified in an owner-provided indicator document. This task should not be implemented until Pivot High / Pivot Low behavior is approved and available, or until the owner explicitly provides an alternative Swing Structure definition.

# Clean Requirement

Add a pure structure module that consumes confirmed swing pivots and labels structural relationships such as higher high, higher low, lower high, lower low, trend state, or other owner-approved structure fields.

# Extracted Roles

- Owner role: Price structure classification.
- Supporting roles:
  - Pivot High / Pivot Low indicator, as an upstream dependency if approved.
  - Strategy, only as a future consumer of structure labels.
  - Test Designer, for deterministic sequence tests.
  - Documentation, for assumptions and output field descriptions.
- Forbidden roles:
  - Market Data Provider, because this task must not fetch candle data.
  - Execution, because this task must not place or simulate orders.
  - Live Trading, because this task must not call real exchange order APIs.
  - Risk Management, Database, dashboard, scheduler, FastAPI, Streamlit, machine learning, futures, leverage, or portfolio optimization.

# Dependencies

- Prefer completing Task 028: Pivot High / Pivot Low before this task.
- If Task 028 is not complete, implementation must stop unless the owner provides a self-contained Swing Structure input contract.

# Scope

- Add a pure Swing Structure calculation from confirmed pivots and/or candles according to owner-approved rules.
- Add deterministic output for each relevant pivot or candle.
- Add tests for bullish, bearish, neutral/ranging, insufficient-structure, and ambiguous cases.
- Update package exports only if needed.
- Update `STATUS.md` during implementation if project state changes.

# Out of Scope

- Pivot detection changes beyond consuming the approved pivot output.
- Support / Resistance Zone aggregation.
- Trading signal generation, pattern validation, backtesting wiring, paper trading wiring, execution, risk management, or live trading.
- Fetching market data or calling exchange APIs.
- Database, dashboards, schedulers, Docker, FastAPI, Streamlit, machine learning, futures, leverage, or portfolio optimization.

# Requirements

- Read `AGENTS.md`, `STATUS.md`, `docs/10_CODEX_COMMAND_GUIDE.md`, `tasks/025_INDICATOR_DOCUMENT_INTAKE_PROCESS.md`, `tasks/028_IMPLEMENT_PIVOT_HIGH_LOW.md`, this task file, and `reviews/CODEX_SELF_REVIEW.md` before coding.
- Confirm owner-approved structure labels and transition rules before implementation.
- Confirm whether structure is calculated per candle, per pivot event, or as the latest state only.
- Confirm how to handle equal highs/lows, missing pivots, and insufficient confirmed pivots.
- Keep the implementation pure and deterministic.
- Do not add network calls, exchange clients, API-key reads, environment-secret reads, order placement, or live-trading toggles.

# Open Questions Before Implementation

- Which labels are required: `HH`, `HL`, `LH`, `LL`, bullish/bearish/neutral trend, break of structure, change of character, or another set?
- How many confirmed pivots are required before returning a valid structure state?
- Should output align to candles, pivot events, or a single latest snapshot?
- How should equal highs/lows be classified?
- Should internal and external swing structure be separate concepts?

# Status Tracking

## Before Implementation

- [ ] Read required project files and this task.
- [ ] Confirm Task 028 is complete or confirm a self-contained owner-approved input contract.
- [ ] Confirm owner-approved structure labels and transition rules.
- [ ] Confirm implementation is limited to Swing Structure only.

## After Implementation

- [ ] Add or update deterministic tests.
- [ ] Run required verification.
- [ ] Complete Codex self-review.
- [ ] Update `STATUS.md` if active task, current step, next step, or completion state changed.

# Acceptance Criteria

- Swing Structure calculation is deterministic for a fixed input and fixed parameters.
- Output labels match owner-approved structure rules.
- Insufficient or ambiguous structure has explicit documented behavior.
- Tests cover bullish, bearish, neutral/insufficient, equal-level, and invalid-input cases.
- No market-data fetching, exchange API calls, order endpoint calls, API-key reads, live trading behavior, or execution wiring is added.

# Required Tests

## Unit Tests

- Classifies a sequence of higher highs and higher lows as owner-approved bullish structure.
- Classifies a sequence of lower highs and lower lows as owner-approved bearish structure.
- Handles insufficient pivots deterministically.
- Handles equal highs/lows according to owner-approved rules.
- Rejects malformed pivot or candle input.

## Integration Tests

- Optional test with Task 028 pivot output may be added if Task 028 is complete.

## Contract Tests

- Output field names and label values remain stable.

## Safety Tests

- Verify ordinary tests do not require network access, Binance credentials, PostgreSQL, Docker, or exchange API calls.

# Verification

Required:

```bash
pytest
```

Required:

```bash
git diff --check
```

Optional if implementation adds new modules:

```bash
python -m compileall quant_bitcoin
```

# Codex Self-Review Requirement

Before completion, run through `reviews/CODEX_SELF_REVIEW.md` and include the result in the final summary.

# Completion Summary Required

- files changed
- implementation summary
- tests added or updated
- tests run
- Codex self-review result
- known limitations
- recommended next task
