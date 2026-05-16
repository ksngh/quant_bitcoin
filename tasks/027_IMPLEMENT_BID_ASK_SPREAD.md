# Task 027: Implement Bid-Ask Spread

# Goal

Implement a deterministic Bid-Ask Spread calculation module that decides whether the current best bid and best ask are narrow enough for automated trading filters.

This task is indicator/filter calculation only. It must not fetch market data, place orders, call exchange APIs, or make live-trading decisions.

# Source Requirement

Owner provided the Bid-Ask Spread specification on 2026-05-16.

Required inputs:

- `symbol`
- `timestamp`
- `best_bid_price`
- `best_ask_price`

Optional inputs:

- `mid_price`
- `bid_size`
- `ask_size`

Derived values:

```text
mid_price = (best_bid_price + best_ask_price) / 2
spread = best_ask_price - best_bid_price
spread_rate = spread / mid_price
spread_rate_percent = spread_rate * 100
```

Mechanical rule:

```text
spread_pass = spread_rate <= maximum_allowed_spread_rate
```

Default parameters:

```yaml
maximum_allowed_spread_rate: 0.001
require_positive_bid_ask: true
reject_crossed_orderbook: true
reject_zero_mid_price: true
```

Spread status:

```text
if spread_rate <= maximum_allowed_spread_rate * 0.5:
    spread_status = TIGHT
elif spread_rate <= maximum_allowed_spread_rate:
    spread_status = ACCEPTABLE
else:
    spread_status = WIDE
```

Invalid status rules:

```text
missing bid or ask -> INVALID
best_bid_price <= 0 -> INVALID
best_ask_price <= 0 -> INVALID
best_ask_price < best_bid_price -> CROSSED_ORDERBOOK
mid_price <= 0 -> INVALID
```

Expected output fields:

- `symbol`
- `timestamp`
- `best_bid_price`
- `best_ask_price`
- `mid_price`
- `spread`
- `spread_rate`
- `spread_rate_percent`
- `maximum_allowed_spread_rate`
- `spread_pass`
- `spread_status`

Allowed statuses:

- `TIGHT`
- `ACCEPTABLE`
- `WIDE`
- `INVALID`
- `CROSSED_ORDERBOOK`

# Clean Requirement

Add a small application-layer indicator/filter component that accepts an order-book top-of-book snapshot and returns a complete Bid-Ask Spread snapshot with calculated mid price, spread, normalized spread rate, pass/fail flag, and status.

# Extracted Roles

- Owner role: Liquidity / spread filter calculation.
- Supporting roles:
  - Strategy, only as a future consumer of the spread result.
  - Test Designer, for deterministic calculation and edge-case tests.
  - Documentation, for public output field expectations.
- Forbidden roles:
  - Market Data Provider, because this task must not fetch order-book data.
  - Execution, because this task must not place or simulate orders.
  - Live Trading, because this task must not call real exchange order APIs.
  - Risk Management, unless a later task explicitly wires the filter into risk checks.
  - Database, dashboard, scheduler, FastAPI, Streamlit, machine learning, futures, leverage, or portfolio optimization.

# Context

This is the first top-of-book liquidity filter task after the indicator intake workflow. It may introduce a new indicator/filter module if the repository does not already have a suitable location, but must keep the implementation small and isolated.

# Scope

- Add a domain model or dataclass for the top-of-book input if needed.
- Add a config object or dataclass for spread parameters.
- Add a result model or dataclass matching the output fields.
- Add a status enum or equivalent stable constants for the five allowed statuses.
- Add a pure calculation function such as `calculate_bid_ask_spread(...)`.
- Add deterministic unit tests for normal cases, threshold boundaries, and invalid inputs.
- Update package exports only if needed for ordinary imports.
- Update `STATUS.md` during implementation if project state changes.

# Out of Scope

- Fetching order-book data from Binance or any exchange.
- Calling signed endpoints, account endpoints, order endpoints, or WebSocket order APIs.
- Live trading or real Binance order execution.
- Strategy signal generation or pattern validation.
- Wiring the spread filter into paper trading, backtesting, execution, risk checks, or persistence.
- Changing candle data contracts.
- Adding dashboards, schedulers, databases, Docker changes, FastAPI, Streamlit, machine learning, futures, leverage, or portfolio optimization.

# Requirements

- Read `AGENTS.md`, `STATUS.md`, `docs/10_CODEX_COMMAND_GUIDE.md`, `tasks/025_INDICATOR_DOCUMENT_INTAKE_PROCESS.md`, this task file, and `reviews/CODEX_SELF_REVIEW.md` before coding.
- Keep the calculation pure and deterministic.
- Treat missing `best_bid_price` or `best_ask_price` as `spread_pass = False` and `spread_status = INVALID`.
- If `require_positive_bid_ask` is true, non-positive bid or ask must return `INVALID`.
- If `reject_crossed_orderbook` is true, ask below bid must return `CROSSED_ORDERBOOK`.
- If `reject_zero_mid_price` is true, non-positive mid price must return `INVALID`.
- Boundary behavior must be inclusive: `spread_rate <= maximum_allowed_spread_rate` passes.
- Boundary behavior for `TIGHT` must be inclusive: `spread_rate <= maximum_allowed_spread_rate * 0.5` is `TIGHT`.
- Do not add network calls, exchange clients, API-key reads, environment-secret reads, order placement, or live-trading toggles.

# Status Tracking

## Before Implementation

- [ ] Read `AGENTS.md`.
- [ ] Read `STATUS.md`.
- [ ] Read `docs/10_CODEX_COMMAND_GUIDE.md`.
- [ ] Read `tasks/025_INDICATOR_DOCUMENT_INTAKE_PROCESS.md`.
- [ ] Read `reviews/CODEX_SELF_REVIEW.md`.
- [ ] Read this task file.
- [ ] Confirm implementation is limited to Bid-Ask Spread only.
- [ ] Confirm no external market-data fetch or order execution is required.

## After Implementation

- [ ] Add or update deterministic tests.
- [ ] Run required verification.
- [ ] Complete Codex self-review.
- [ ] Update `STATUS.md` if active task, current step, next step, or completion state changed.
- [ ] Leave uncertain items open and document the uncertainty.

# Acceptance Criteria

- Bid-Ask Spread calculation returns all required output fields for valid top-of-book input.
- Default configuration uses `maximum_allowed_spread_rate = 0.001` and all three rejection flags enabled.
- Tight, acceptable, and wide spread statuses are assigned exactly by the owner-provided thresholds.
- Missing bid or ask, non-positive bid or ask, crossed order book, and zero/non-positive mid price are handled deterministically.
- Tests cover threshold equality for `TIGHT`, `ACCEPTABLE`, and `WIDE` behavior.
- No market-data fetching, exchange API calls, order endpoint calls, API-key reads, live trading behavior, or execution wiring is added.

# Required Tests

## Unit Tests

- Valid tight spread example using BTCUSDT values from the source requirement.
- Boundary case where `spread_rate == maximum_allowed_spread_rate * 0.5` returns `TIGHT`.
- Boundary case where `spread_rate == maximum_allowed_spread_rate` returns `ACCEPTABLE` and passes.
- Case where `spread_rate > maximum_allowed_spread_rate` returns `WIDE` and fails.
- Missing bid returns `INVALID` and fails.
- Missing ask returns `INVALID` and fails.
- Zero or negative bid returns `INVALID` and fails when positive bid/ask is required.
- Zero or negative ask returns `INVALID` and fails when positive bid/ask is required.
- Ask below bid returns `CROSSED_ORDERBOOK` and fails when crossed books are rejected.
- Non-positive mid price returns `INVALID` and fails when zero mid price is rejected.

## Integration Tests

- Not required for the first isolated implementation.

## Contract Tests

- Output field names and status values remain stable.
- Public models, if added, can be imported from the documented module path.

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
