# Task 033: Implement Displacement Candle

# Goal

Implement deterministic Displacement Candle detection from already-provided candle data.

This task must identify unusually strong candles only. It must not fetch market data, place orders, call exchange APIs, or make live-trading decisions.

# Source Requirement

Owner listed Displacement Candle as one of the remaining indicators to add on 2026-05-16.

Detailed formulas, default parameters, output schema, and edge-case behavior are not yet fully specified in an owner-provided indicator document. Before implementation, the owner must confirm whether displacement is based on candle body, range, ATR multiple, volume ratio, close location, or a combination.

# Clean Requirement

Add a pure candle-based detector that labels bullish, bearish, or non-displacement candles according to owner-approved body/range/volatility/volume rules.

# Extracted Roles

- Owner role: Candle pattern / momentum indicator calculation.
- Supporting roles:
  - ATR indicator, only if owner approves ATR-based displacement thresholds.
  - Volume Ratio indicator, only if owner approves volume-confirmed displacement.
  - Strategy, only as a future consumer of displacement labels.
  - Test Designer, for deterministic candle-pattern tests.
  - Documentation, for assumptions and output field descriptions.
- Forbidden roles:
  - Market Data Provider, because this task must not fetch candle data.
  - Execution, because this task must not place or simulate orders.
  - Live Trading, because this task must not call real exchange order APIs.
  - Risk Management, Database, dashboard, scheduler, FastAPI, Streamlit, machine learning, futures, leverage, or portfolio optimization.

# Dependencies

- ATR may optionally be consumed only if Task 030 is complete and owner approves ATR-based thresholds.
- Volume Ratio may optionally be consumed only if Task 031 is complete and owner approves volume confirmation.
- If optional dependencies are incomplete, implementation must use only a self-contained owner-approved candle formula or stop and report the dependency.

# Scope

- Add pure Displacement Candle detection from provided candles.
- Add owner-approved configuration for body size, range size, ATR multiple, close-location, and/or volume confirmation.
- Add deterministic output such as displacement flag, direction, body size, range size, and threshold values after owner confirmation.
- Add tests for bullish displacement, bearish displacement, normal candles, edge thresholds, insufficient dependency data, and invalid input.
- Update package exports only if needed.
- Update `STATUS.md` during implementation if project state changes.

# Out of Scope

- Strategy entries, order blocks, fair value gaps, pattern validation, or trading signals unless explicitly assigned.
- ATR or Volume Ratio implementation unless assigned by their own tasks.
- Fetching market data or calling exchange APIs.
- Backtesting wiring, paper trading wiring, execution, risk management, persistence, dashboards, schedulers, Docker, FastAPI, Streamlit, machine learning, futures, leverage, or portfolio optimization.

# Requirements

- Read `AGENTS.md`, `STATUS.md`, `docs/10_CODEX_COMMAND_GUIDE.md`, `tasks/025_INDICATOR_DOCUMENT_INTAKE_PROCESS.md`, this task file, and `reviews/CODEX_SELF_REVIEW.md` before coding.
- Confirm owner-approved displacement formula before implementation.
- Confirm whether bullish/bearish direction is based on `close > open` and `close < open` or another rule.
- Confirm whether thresholds are inclusive or strict.
- Confirm dependency behavior if ATR or Volume Ratio values are unavailable.
- Keep the implementation pure and deterministic.
- Do not add network calls, exchange clients, API-key reads, environment-secret reads, order placement, or live-trading toggles.

# Open Questions Before Implementation

- Is displacement based on body size, full range, ATR multiple, volume ratio, or all of these?
- What are the default thresholds?
- Should the candle close near its high/low to count as displacement?
- Should wick size disqualify a displacement candle?
- Should bullish and bearish displacement use symmetric rules?
- Should the output include a displacement score or only a boolean/direction?

# Status Tracking

## Before Implementation

- [ ] Read required project files and this task.
- [ ] Confirm owner-approved displacement formula and parameters.
- [ ] Confirm optional ATR or Volume Ratio dependencies are complete if required.
- [ ] Confirm implementation is limited to Displacement Candle only.

## After Implementation

- [ ] Add or update deterministic tests.
- [ ] Run required verification.
- [ ] Complete Codex self-review.
- [ ] Update `STATUS.md` if active task, current step, next step, or completion state changed.

# Acceptance Criteria

- Displacement Candle detection is deterministic for fixed candle input and fixed parameters.
- Direction and threshold behavior match owner-approved rules.
- Optional ATR or Volume Ratio dependency behavior is explicit and tested if used.
- Missing, non-numeric, or malformed candle fields are rejected or handled exactly as documented.
- Tests cover bullish, bearish, non-displacement, threshold boundary, insufficient-data, invalid-parameter, and invalid-input cases.
- No market-data fetching, exchange API calls, order endpoint calls, API-key reads, live trading behavior, or execution wiring is added.

# Required Tests

## Unit Tests

- Detects bullish displacement according to owner-approved rules.
- Detects bearish displacement according to owner-approved rules.
- Does not mark ordinary candles as displacement.
- Covers threshold equality or strictness according to owner-approved behavior.
- Handles unavailable optional ATR/Volume Ratio data according to owner-approved behavior.
- Rejects missing required candle columns.
- Rejects invalid threshold parameters.

## Integration Tests

- Optional ATR/Volume Ratio integration tests may be added only if those dependency tasks are complete and owner-approved.

## Contract Tests

- Output field names, direction values, and status values remain stable.

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
