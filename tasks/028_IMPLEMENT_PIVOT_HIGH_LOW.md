# Task 028: Implement Pivot High / Pivot Low

# Goal

Implement deterministic Pivot High / Pivot Low detection from already-provided candle data.

This task must identify local swing points only. It must not fetch market data, place orders, call exchange APIs, or make live-trading decisions.

# Source Requirement

Owner listed Pivot High / Pivot Low as one of the remaining indicators to add on 2026-05-16.

Detailed formulas, default parameters, output schema, and edge-case behavior are not yet fully specified in an owner-provided indicator document. Before implementation, the assigned implementer must either use an owner-approved saved indicator document or record explicit assumptions in this task and `STATUS.md`.

# Clean Requirement

Add a pure candle-based indicator that marks each candle as a pivot high, pivot low, both, or neither according to owner-approved left/right lookback parameters.

# Extracted Roles

- Owner role: Price structure indicator calculation.
- Supporting roles:
  - Strategy, only as a future consumer of pivot points.
  - Test Designer, for deterministic window and edge-case tests.
  - Documentation, for assumptions and output field descriptions.
- Forbidden roles:
  - Market Data Provider, because this task must not fetch candle data.
  - Execution, because this task must not place or simulate orders.
  - Live Trading, because this task must not call real exchange order APIs.
  - Risk Management, Database, dashboard, scheduler, FastAPI, Streamlit, machine learning, futures, leverage, or portfolio optimization.

# Context

Pivot points are likely prerequisites for Swing Structure and Support / Resistance Zone tasks. If those downstream tasks need additional pivot contract fields, stop and report the shared contract question instead of silently expanding this task.

# Scope

- Add a pure Pivot High / Pivot Low calculation from provided candles.
- Use existing candle schema where possible: `timestamp`, `open`, `high`, `low`, `close`, `volume`.
- Add explicit configuration for left/right lookback windows after owner confirmation.
- Add deterministic output that includes timestamp, high, low, pivot flags, and pivot price where applicable.
- Add tests for normal pivots, no pivot, insufficient warm-up/cool-down candles, equal-high/equal-low tie behavior, and invalid input.
- Update package exports only if needed.
- Update `STATUS.md` during implementation if project state changes.

# Out of Scope

- Swing trend classification such as higher-high, lower-low, break of structure, or change of character.
- Support / Resistance Zone aggregation.
- ATR, volume ratio, displacement candle, or spread calculations.
- Fetching market data or calling exchange APIs.
- Strategy signal generation, execution, paper trading, risk management, persistence, dashboards, schedulers, FastAPI, Streamlit, Docker, machine learning, futures, leverage, or portfolio optimization.

# Requirements

- Read `AGENTS.md`, `STATUS.md`, `docs/10_CODEX_COMMAND_GUIDE.md`, `tasks/025_INDICATOR_DOCUMENT_INTAKE_PROCESS.md`, this task file, and `reviews/CODEX_SELF_REVIEW.md` before coding.
- Confirm the owner-approved definition of pivot high and pivot low before implementation.
- Confirm whether comparisons are strict (`>`, `<`) or allow ties (`>=`, `<=`).
- Confirm warm-up/cool-down behavior for candles that do not have enough left or right neighbors.
- Keep the implementation pure and deterministic.
- Do not add network calls, exchange clients, API-key reads, environment-secret reads, order placement, or live-trading toggles.

# Open Questions Before Implementation

- What are the default `left_bars` and `right_bars` values?
- Should equal highs/lows count as pivots or invalidate the pivot?
- Should the result be returned as a series aligned to all candles or only as pivot events?
- Should a candle be allowed to be both a pivot high and pivot low?
- Should the implementation require a full right-side confirmation window before marking the latest candle?

# Status Tracking

## Before Implementation

- [ ] Read required project files and this task.
- [ ] Confirm owner-approved pivot formula and parameters.
- [ ] Confirm no shared contract changes are required for downstream Swing Structure or Support / Resistance Zone tasks.
- [ ] Confirm implementation is limited to Pivot High / Pivot Low only.

## After Implementation

- [ ] Add or update deterministic tests.
- [ ] Run required verification.
- [ ] Complete Codex self-review.
- [ ] Update `STATUS.md` if active task, current step, next step, or completion state changed.

# Acceptance Criteria

- Pivot High / Pivot Low calculation is deterministic for a fixed candle input and fixed parameters.
- Output includes stable pivot flags and enough identifying data for downstream structure tasks.
- Insufficient-window candles have explicit documented behavior.
- Tie behavior is implemented exactly as owner-approved.
- Tests cover normal, boundary, insufficient-data, tie, and invalid-input cases.
- No market-data fetching, exchange API calls, order endpoint calls, API-key reads, live trading behavior, or execution wiring is added.

# Required Tests

## Unit Tests

- Detects a pivot high in a simple five-candle sequence.
- Detects a pivot low in a simple five-candle sequence.
- Does not mark non-pivot middle candles.
- Handles insufficient left/right windows deterministically.
- Covers equal-high/equal-low tie behavior after owner confirmation.
- Rejects missing required candle columns.
- Rejects invalid lookback parameters.

## Integration Tests

- Not required for the first isolated implementation.

## Contract Tests

- Output field names and pivot flag semantics remain stable.

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
