# Task 031: Implement Volume Ratio

# Goal

Implement deterministic Volume Ratio calculation from already-provided candle volume data.

This task must calculate relative volume only. It must not fetch market data, place orders, call exchange APIs, or make live-trading decisions.

# Source Requirement

Owner listed Volume Ratio as one of the remaining indicators to add on 2026-05-16.

Detailed formulas, default parameters, output schema, and edge-case behavior are not yet fully specified in an owner-provided indicator document. Before implementation, the owner must confirm the exact baseline average, window, and zero-volume behavior.

# Clean Requirement

Add a pure candle-based Volume Ratio indicator that compares current volume against an owner-approved historical volume baseline.

# Extracted Roles

- Owner role: Volume indicator calculation.
- Supporting roles:
  - Strategy, only as a future consumer of volume ratio values.
  - Liquidity filter, only as a conceptual related filter; do not couple unless assigned.
  - Test Designer, for deterministic window and edge-case tests.
  - Documentation, for assumptions and output field descriptions.
- Forbidden roles:
  - Market Data Provider, because this task must not fetch candle data.
  - Execution, because this task must not place or simulate orders.
  - Live Trading, because this task must not call real exchange order APIs.
  - Risk Management, Database, dashboard, scheduler, FastAPI, Streamlit, machine learning, futures, leverage, or portfolio optimization.

# Scope

- Add a pure Volume Ratio calculation from provided candles containing `volume`.
- Add configurable baseline window after owner confirmation.
- Add output fields such as current volume, average volume, and volume ratio after owner confirmation.
- Add deterministic tests for normal, high-volume, low-volume, insufficient-data, and zero-baseline cases.
- Update package exports only if needed.
- Update `STATUS.md` during implementation if project state changes.

# Out of Scope

- Liquidity trading value implementation unless explicitly assigned.
- Signal generation, pattern validation, backtesting wiring, paper trading wiring, execution, or risk management.
- Fetching market data or calling exchange APIs.
- Database, dashboards, schedulers, Docker, FastAPI, Streamlit, machine learning, futures, leverage, or portfolio optimization.

# Requirements

- Read `AGENTS.md`, `STATUS.md`, `docs/10_CODEX_COMMAND_GUIDE.md`, `tasks/025_INDICATOR_DOCUMENT_INTAKE_PROCESS.md`, this task file, and `reviews/CODEX_SELF_REVIEW.md` before coding.
- Confirm owner-approved formula before implementation.
- Confirm whether the current candle is included or excluded from the average baseline.
- Confirm zero average volume and missing volume behavior.
- Keep the implementation pure and deterministic.
- Do not add network calls, exchange clients, API-key reads, environment-secret reads, order placement, or live-trading toggles.

# Open Questions Before Implementation

- Should `volume_ratio = current_volume / average_volume`?
- What is the default window?
- Should the baseline include or exclude the current candle?
- Should the baseline use mean, median, EMA, or another method?
- What should happen when average volume is zero?
- Should quote volume be supported, or only base volume?

# Status Tracking

## Before Implementation

- [ ] Read required project files and this task.
- [ ] Confirm owner-approved formula and parameters.
- [ ] Confirm implementation is limited to Volume Ratio only.

## After Implementation

- [ ] Add or update deterministic tests.
- [ ] Run required verification.
- [ ] Complete Codex self-review.
- [ ] Update `STATUS.md` if active task, current step, next step, or completion state changed.

# Acceptance Criteria

- Volume Ratio calculation is deterministic for fixed candle input and fixed parameters.
- Baseline average behavior is owner-approved and documented.
- Insufficient-data and zero-baseline behavior is explicit and tested.
- Missing or non-numeric volume is rejected or handled exactly as documented.
- Tests cover normal, elevated-volume, low-volume, insufficient-data, zero-baseline, invalid-parameter, and invalid-input cases.
- No market-data fetching, exchange API calls, order endpoint calls, API-key reads, live trading behavior, or execution wiring is added.

# Required Tests

## Unit Tests

- Calculates expected volume ratio for a deterministic fixture.
- Handles insufficient baseline window deterministically.
- Handles zero average volume according to owner-approved behavior.
- Rejects missing `volume` column.
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
