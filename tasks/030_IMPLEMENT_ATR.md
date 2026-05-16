# Task 030: Implement ATR

# Goal

Implement deterministic Average True Range (ATR) calculation from already-provided candle data.

This task must calculate volatility only. It must not fetch market data, place orders, call exchange APIs, or make live-trading decisions.

# Source Requirement

Owner listed ATR as one of the remaining indicators to add on 2026-05-16.

Detailed owner-specific output schema and edge-case behavior are not yet fully specified in an owner-provided indicator document. The common ATR formula may be used only after the owner confirms the intended smoothing method and warm-up behavior.

# Clean Requirement

Add a pure candle-based ATR indicator that calculates true range and rolling or smoothed average true range using owner-approved parameters.

# Extracted Roles

- Owner role: Volatility indicator calculation.
- Supporting roles:
  - Strategy, only as a future consumer of ATR values.
  - Test Designer, for deterministic numeric tests.
  - Documentation, for formula and warm-up assumptions.
- Forbidden roles:
  - Market Data Provider, because this task must not fetch candle data.
  - Execution, because this task must not place or simulate orders.
  - Live Trading, because this task must not call real exchange order APIs.
  - Risk Management, unless a later task explicitly consumes ATR for risk controls.
  - Database, dashboard, scheduler, FastAPI, Streamlit, machine learning, futures, leverage, or portfolio optimization.

# Scope

- Add a pure ATR calculation from provided candles containing at least `high`, `low`, and `close`.
- Add configurable ATR window, expected default `14` if owner approves.
- Add owner-approved smoothing behavior, such as simple moving average, Wilder smoothing, or another explicit method.
- Add deterministic tests for true range and ATR values.
- Update package exports only if needed.
- Update `STATUS.md` during implementation if project state changes.

# Out of Scope

- Position sizing, stop-loss logic, risk management, or execution decisions.
- Strategy signal generation or pattern validation.
- Fetching market data or calling exchange APIs.
- Database, dashboards, schedulers, Docker, FastAPI, Streamlit, machine learning, futures, leverage, or portfolio optimization.

# Requirements

- Read `AGENTS.md`, `STATUS.md`, `docs/10_CODEX_COMMAND_GUIDE.md`, `tasks/025_INDICATOR_DOCUMENT_INTAKE_PROCESS.md`, this task file, and `reviews/CODEX_SELF_REVIEW.md` before coding.
- Confirm the ATR smoothing method before implementation.
- Confirm default window and warm-up behavior before implementation.
- True range must be based on current high/low and previous close according to the owner-approved formula.
- Keep the implementation pure and deterministic.
- Do not add network calls, exchange clients, API-key reads, environment-secret reads, order placement, or live-trading toggles.

# Open Questions Before Implementation

- Should ATR use simple rolling average or Wilder smoothing?
- What is the default window?
- Should the first candle true range use `high - low` because no previous close exists?
- Should insufficient warm-up rows be `NaN`, `None`, omitted, or invalid result objects?
- Should output include both `true_range` and `atr`, or only `atr`?

# Status Tracking

## Before Implementation

- [ ] Read required project files and this task.
- [ ] Confirm owner-approved ATR formula, smoothing method, and parameters.
- [ ] Confirm implementation is limited to ATR only.

## After Implementation

- [ ] Add or update deterministic tests.
- [ ] Run required verification.
- [ ] Complete Codex self-review.
- [ ] Update `STATUS.md` if active task, current step, next step, or completion state changed.

# Acceptance Criteria

- ATR calculation is deterministic for fixed candle input and fixed parameters.
- True range is calculated exactly by the owner-approved formula.
- Warm-up behavior is explicit and tested.
- Missing or non-numeric required candle fields are rejected or handled exactly as documented.
- Tests cover true range, ATR values, warm-up rows, invalid parameters, and invalid input.
- No market-data fetching, exchange API calls, order endpoint calls, API-key reads, live trading behavior, risk-control behavior, or execution wiring is added.

# Required Tests

## Unit Tests

- Calculates true range for candles with previous close above/below current range.
- Calculates ATR for a deterministic fixture using the owner-approved smoothing method.
- Handles first candle and warm-up rows deterministically.
- Rejects missing `high`, `low`, or `close` columns.
- Rejects invalid window values.

## Integration Tests

- Not required for the first isolated implementation.

## Contract Tests

- Output field names and numeric tolerance expectations remain stable.

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
