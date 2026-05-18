# Task 047: Pattern Risk / Exit Plan Contract

# Goal

Create the shared, pure-Python contract for pattern-based stop-loss, take-profit, time-stop, break-even, trailing-stop, and partial-exit planning.

This is the required first task before pattern-specific implementations. It establishes the reusable contract only; it must not integrate with live trading, exchange APIs, paper order placement, or the backtest runner.

# Source Requirement

Use the owner-provided source notes saved in:

- `tasks/patterns/risk_exit_management.md`

# Clean Requirement

Add a deterministic planning layer that can represent:

- Entry price.
- Direction (`LONG` / `SHORT`).
- Structural stop and ATR buffer.
- Final stop price.
- Risk per unit.
- R-multiple take-profit levels.
- Optional structural targets and measured targets.
- Minimum profit / minimum R:R filter outcome.
- Time-stop settings.
- Break-even movement condition.
- Trailing-stop settings.
- Partial-exit ratios.
- Skip / invalid-plan reasons.

# Extracted Roles

- Owner role: Shared risk/exit plan contract for pattern strategies.
- Supporting roles:
  - Existing pattern event objects as future inputs.
  - ATR indicator output or existing event `atr` fields as volatility input.
  - Future pattern-specific planner tasks as contract consumers.
- Forbidden roles:
  - Live trading.
  - Real Binance order execution.
  - Exchange order API calls.
  - Backtest-runner integration.
  - Paper order placement.
  - Pattern detection algorithm changes.

# Responsibility Boundary

This task is responsible for reusable data models and calculation helpers only. Pattern-specific tasks must supply their own structural invalidation price, structural targets, and measured targets.

This task must stop for owner guidance if implementing the contract would require renaming or redesigning existing public pattern event contracts.

# Relevant Context To Read Before Implementation

- `AGENTS.md`
- `STATUS.md`
- `docs/03_ARCHITECTURE_RULES.md`
- `docs/04_DATA_CONTRACT.md`
- `docs/05_TEST_STRATEGY.md`
- `docs/10_CODEX_COMMAND_GUIDE.md`
- `reviews/CODEX_SELF_REVIEW.md`
- `tasks/patterns/risk_exit_management.md`
- `quant_bitcoin/indicators/atr.py`
- `quant_bitcoin/patterns/__init__.py`
- `quant_bitcoin/patterns/fair_value_gap.py`
- `quant_bitcoin/patterns/trendline_break.py`
- `quant_bitcoin/patterns/order_block.py`
- `quant_bitcoin/patterns/cup_and_handle.py`
- `quant_bitcoin/patterns/diamond.py`
- `quant_bitcoin/patterns/adam_and_eve.py`

# Scope

- Add a pure module under `quant_bitcoin/patterns/` for risk/exit planning, for example `quant_bitcoin/patterns/risk_exit.py`.
- Add exports in `quant_bitcoin/patterns/__init__.py` only if needed.
- Add deterministic unit tests under `tests/patterns/`.
- Update `STATUS.md` during implementation if project state changes.

# Out of Scope

- Implementing pattern-specific stop formulas.
- Changing existing pattern detector algorithms.
- Changing existing pattern event field names or meanings unless explicitly approved.
- Integrating with `quant_bitcoin/backtesting/`.
- Integrating with `quant_bitcoin/execution/`.
- Creating paper orders or real orders.
- Calling exchange APIs.
- Adding live trading, dashboard, scheduler, FastAPI, Streamlit, Docker, ML, futures, leverage, database schema changes, or portfolio optimization.
- Hardcoding secrets or committing `.env` files.

# Requirements

## Direction And Stop Calculation

- Support long and short plans.
- Long formula:
  - `buffer = atr * buffer_multiplier`
  - `stop_price = structural_stop - buffer`
  - `risk_per_unit = entry_price - stop_price`
- Short formula:
  - `buffer = atr * buffer_multiplier`
  - `stop_price = structural_stop + buffer`
  - `risk_per_unit = stop_price - entry_price`
- Reject or mark invalid plans when ATR, entry, stop, or risk values are missing, non-finite, negative where invalid, or produce non-positive risk.

## R-Multiple Targets

- Calculate long R targets as `entry_price + risk * multiple`.
- Calculate short R targets as `entry_price - risk * multiple`.
- Default multiples should be 1R, 2R, and 3R unless config overrides them.

## Structural And Measured Targets

- Allow optional caller-supplied structural targets and measured targets.
- Do not implement structural-target detection in this task.
- Provide deterministic combination behavior that can be reused by pattern-specific tasks.
- Preserve enough metadata to explain whether each target came from R multiple, structure, measured move, or a combined rule.

## Minimum Profit Filter

- Support a default minimum first-target threshold of `0.8R`.
- Support optional stricter configuration such as `1.2R`.
- Mark the plan skipped or invalid when the first actionable target is below the configured minimum.

## Time Stop, Break-Even, Trailing Stop, Partial Exit

- Represent these settings in the plan contract.
- This task may implement configuration validation and plan serialization-friendly data only.
- Do not implement candle-by-candle exit simulation in this task.

# Acceptance Criteria

- A reusable pattern risk/exit planning contract exists.
- Long and short stop calculations are deterministic and tested.
- R-multiple targets are deterministic and tested.
- Minimum profit filtering is deterministic and tested.
- Time-stop, break-even, trailing-stop, and partial-exit settings can be represented without exchange behavior.
- No live trading or real order execution behavior is added.

# Required Tests

## Unit Tests

- Long stop with ATR buffer.
- Short stop with ATR buffer.
- 1R/2R/3R targets for long and short.
- Minimum first-target threshold pass and skip cases.
- Invalid non-positive risk handling.
- Invalid ATR / missing value handling.
- Partial-exit ratio validation.

## Integration Tests

- Not required for this contract-only task.

## Contract Tests

- Verify exported public objects are importable if exports are added.

## Safety Tests

- Confirm no exchange client, order endpoint, API key, `.env`, or live-trading flag is introduced.

# Verification

Default:

```bash
pytest tests/patterns/test_risk_exit.py
pytest
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
