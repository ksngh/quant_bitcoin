# Task 031: Implement Volume Ratio

# Goal

Implement deterministic Volume Ratio calculation from already-provided candle volume data.

This task must calculate relative volume only. It must not fetch market data, place orders, call exchange APIs, or make live-trading decisions.

# Source Requirement

Owner listed Volume Ratio as one of the remaining indicators to add on 2026-05-16.

The owner provided the detailed Volume Ratio specification on 2026-05-17. The approved formula is `volume_ratio = current_volume / average_volume`, where `average_volume` defaults to the mean of the most recent 20 volume values including the current candle. The owner-approved specification is saved in `tasks/indicators/volume_ratio.md`.

# Clean Requirement

Add a pure candle-based Volume Ratio indicator that compares current volume against the owner-approved recent average volume baseline.

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
- Add configurable baseline window with the default owner-approved 20-candle window.
- Add output fields for current volume, average volume, volume ratio, confirmation flag, status, and validity.
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
- Use the owner-approved formula saved in `tasks/indicators/volume_ratio.md`.
- Include the current candle in the average baseline, matching the owner-provided pseudocode.
- Apply the documented missing-volume, insufficient-window, zero-average-volume, and zero-current-volume behavior.
- Keep the implementation pure and deterministic.
- Do not add network calls, exchange clients, API-key reads, environment-secret reads, order placement, or live-trading toggles.

# Resolved Questions Before Implementation

- `volume_ratio = current_volume / average_volume`.
- The default window is 20.
- The baseline includes the current candle.
- The default baseline uses mean; optional median mode may be supported for robust spike handling.
- If average volume is zero, the row is invalid with `volume_status = INVALID` and `volume_confirmation = false`.
- Initial implementation supports base `volume` only; quote-volume or trading-value ratio remains future scope.

# Status Tracking

## Before Implementation

- [x] Read required project files and this task.
- [x] Confirm owner-approved formula and parameters.
- [x] Confirm implementation is limited to Volume Ratio only.

## After Implementation

- [x] Add or update deterministic tests.
- [x] Run required verification.
- [x] Complete Codex self-review.
- [x] Update `STATUS.md` if active task, current step, next step, or completion state changed.

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
