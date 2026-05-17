# Task 032: Implement Support / Resistance Zone

# Goal

Implement deterministic Support / Resistance Zone detection from already-provided candle data and/or owner-approved pivot points.

This task must identify price zones only. It must not fetch market data, place orders, call exchange APIs, or make live-trading decisions.

# Source Requirement

Owner listed Support / Resistance Zone as one of the remaining indicators to add on 2026-05-16.

The owner provided detailed formulas, default parameters, output schema, and edge-case behavior on 2026-05-17. The saved indicator source document is `tasks/indicators/support_resistance_zone.md`.

# Clean Requirement

Add a pure zone-detection module that groups owner-approved pivot highs and lows or candle levels into support and resistance zones using owner-approved clustering/tolerance rules.

# Extracted Roles

- Owner role: Price zone indicator calculation.
- Supporting roles:
  - Pivot High / Pivot Low indicator, as an upstream dependency if approved.
  - Swing Structure, as a possible future consumer or context provider only if assigned.
  - Strategy, only as a future consumer of zones.
  - Test Designer, for deterministic clustering and edge-case tests.
  - Documentation, for assumptions and output field descriptions.
- Forbidden roles:
  - Market Data Provider, because this task must not fetch candle data.
  - Execution, because this task must not place or simulate orders.
  - Live Trading, because this task must not call real exchange order APIs.
  - Risk Management, Database, dashboard, scheduler, FastAPI, Streamlit, machine learning, futures, leverage, or portfolio optimization.

# Dependencies

- Prefer completing Task 028: Pivot High / Pivot Low before this task.
- ATR may optionally provide a zone-width tolerance only if Task 030 is complete and the owner explicitly approves ATR-based zones.
- If dependencies are incomplete, implementation must stop unless the owner provides a self-contained zone definition.

# Scope

- Add pure Support / Resistance Zone calculation using owner-approved input and tolerance rules.
- Add deterministic output for each zone, including at minimum zone type, lower bound, upper bound, representative price, and touch count if approved.
- Add tests for support zones, resistance zones, merged nearby levels, isolated levels, insufficient data, and invalid input.
- Update package exports only if needed.
- Update `STATUS.md` during implementation if project state changes.

# Out of Scope

- Pivot detection changes beyond consuming approved pivot output.
- Trade entry/exit signals from zones.
- Breakout, retest, or pattern validation logic unless explicitly assigned.
- Fetching market data or calling exchange APIs.
- Backtesting wiring, paper trading wiring, execution, risk management, persistence, dashboards, schedulers, Docker, FastAPI, Streamlit, machine learning, futures, leverage, or portfolio optimization.

# Requirements

- Read `AGENTS.md`, `STATUS.md`, `docs/10_CODEX_COMMAND_GUIDE.md`, `tasks/025_INDICATOR_DOCUMENT_INTAKE_PROCESS.md`, `tasks/028_IMPLEMENT_PIVOT_HIGH_LOW.md`, this task file, and `reviews/CODEX_SELF_REVIEW.md` before coding.
- Confirm owner-approved zone construction rules before implementation.
- Confirm whether zones are built from pivot highs/lows, candle highs/lows, closes, or another input.
- Confirm tolerance method, such as fixed percent, fixed price amount, ATR multiple, or another method.
- Keep the implementation pure and deterministic.
- Do not add network calls, exchange clients, API-key reads, environment-secret reads, order placement, or live-trading toggles.

# Open Questions Before Implementation

- What qualifies as a support zone versus a resistance zone?
- What input levels should zones use?
- What tolerance or clustering method should merge nearby levels?
- What minimum touch count is required for a valid zone?
- Should zones expire after time or after price breaks them?
- Should overlapping support and resistance zones be allowed?

# Status Tracking

## Before Implementation

- [x] Read required project files and this task.
- [x] Confirm required dependencies are complete or owner supplied a self-contained input contract.
- [x] Confirm owner-approved zone construction rules and parameters.
- [x] Confirm implementation is limited to Support / Resistance Zone only.

## After Implementation

- [x] Add or update deterministic tests.
- [x] Run required verification.
- [x] Complete Codex self-review.
- [x] Update `STATUS.md` if active task, current step, next step, or completion state changed.

# Acceptance Criteria

- Support / Resistance Zone calculation is deterministic for fixed input and fixed parameters.
- Zone construction and merge rules match owner-approved requirements.
- Insufficient-data and ambiguous-zone behavior is explicit and tested.
- Output includes stable zone fields for future strategy consumption.
- Tests cover support, resistance, merge, no-zone, insufficient-data, and invalid-input cases.
- No market-data fetching, exchange API calls, order endpoint calls, API-key reads, live trading behavior, or execution wiring is added.

# Required Tests

## Unit Tests

- Detects a support zone from repeated lows according to owner-approved rules.
- Detects a resistance zone from repeated highs according to owner-approved rules.
- Merges nearby levels according to tolerance.
- Leaves isolated levels unzoned or single-touch according to owner-approved behavior.
- Handles insufficient data deterministically.
- Rejects malformed pivot or candle input.

## Integration Tests

- Optional test with Task 028 pivot output may be added if Task 028 is complete.
- Optional ATR-tolerance test may be added only if Task 030 is complete and owner-approved.

## Contract Tests

- Output field names and zone type values remain stable.

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
