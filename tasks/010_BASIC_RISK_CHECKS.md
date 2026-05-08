# Task 010: Basic Paper Risk Checks

# Goal

Implement the first explicit risk-management component for paper-mode actions only: deterministic pre-trade checks that approve or reject proposed paper trades before paper state changes.

# Source Requirement

`docs/08_ROADMAP.md` Phase 11: Later Risk Management.

# Extracted Roles

- Owner role: Risk Management
- Supporting roles: Execution, Test Designer
- Forbidden roles: Strategy, Market Data Provider, Live Execution, Binance order client

# Context

Task 009 defined that risk-management requirements must be documented before code is written. Existing paper trading is local and in-memory. The first risk-management implementation must remain paper-only and must not introduce live exchange behavior, real account state, or order routing.

# Input Contract

The risk checker receives a proposed paper action with:

- `symbol`: non-blank symbol string
- `signal`: existing strategy `Signal` value
- `quantity`: positive numeric proposed quantity
- `price`: positive numeric proposed price
- `cash_balance`: non-negative numeric paper cash balance
- `current_position`: non-negative numeric paper position for the symbol

# Output Behavior

The risk checker returns a deterministic decision object with:

- `approved`: `True` or `False`
- `reason`: short machine-readable reason string

Initial expected reasons:

- `approved`
- `hold_no_trade`
- `insufficient_cash`
- `insufficient_position`
- `invalid_input`

# Scope

- add a small paper-only risk check component
- approve HOLD as no-trade or explicitly report `hold_no_trade`
- reject BUY when proposed notional exceeds paper cash
- reject SELL when proposed quantity exceeds current paper position
- validate proposed action inputs
- add deterministic tests for approval and rejection paths

# Out of Scope

- live trading
- real exchange APIs
- Binance order execution
- order routing
- real account state
- portfolio-level risk
- stop loss
- take profit
- position sizing formulas
- leverage
- futures
- margin
- fees
- slippage
- portfolio optimization
- dashboard
- database
- scheduler
- machine learning
- changing strategy behavior
- fetching market data

# Requirements

- Risk checks must be pure/local and deterministic.
- Risk checks must not mutate paper trader state.
- Risk checks must not fetch market data.
- Risk checks must not calculate RSI or other strategy indicators.
- Risk checks must not place real or paper orders.
- Risk checks must not call exchange APIs or Binance order endpoints.
- Risk checks must not require API keys, secrets, `.env` files, network access, database access, or scheduler setup.
- Integration with `PaperTrader` is optional for this task and may be deferred unless kept small and explicitly tested.

# Status Tracking

## Before Implementation

- [ ] Read `AGENTS.md`.
- [ ] Read `STATUS.md`.
- [ ] Confirm this task matches the current phase and step.
- [ ] Confirm parallel work is safe before starting any parallel work.
- [ ] Record assumptions, blockers, or unclear items in `STATUS.md` before coding if needed.

## After Implementation

- [ ] Update `STATUS.md` if the phase, step, goal, active task, blocker, open question, or completion state changed.
- [ ] Mark checklist items complete only when acceptance criteria and verification are satisfied.
- [ ] Leave uncertain items open and document the uncertainty.
- [ ] Confirm the next step is accurate or explicitly left undecided.

# Acceptance Criteria

- BUY with sufficient paper cash is approved.
- BUY with insufficient paper cash is rejected.
- SELL with sufficient paper position is approved.
- SELL with insufficient paper position is rejected.
- HOLD is handled deterministically without requiring a trade.
- Invalid inputs are rejected or reported explicitly.
- Risk checks do not mutate paper trader state.
- Risk checks do not call live exchange APIs or place real orders.
- Existing tests continue to pass.

# Required Tests

- Unit Tests: BUY approval/rejection, SELL approval/rejection, HOLD handling, invalid input handling.
- Integration Tests: optional small test with `PaperTrader` only if integration is implemented.
- Contract Tests: accepts existing strategy `Signal` values.
- Safety Tests: no network calls, no exchange order endpoints, no API keys or `.env` requirements, no mutation of paper state.

# Review Checklist

- Risk component owns only risk decisions.
- Risk component does not generate strategy signals.
- Risk component does not fetch market data.
- Risk component does not execute real or paper trades.
- Risk component does not call Binance or exchange order endpoints.
- Risk component does not introduce live trading flags or defaults.
- Risk component does not introduce leverage, futures, portfolio optimization, database, dashboard, scheduler, or ML.
- Public strategy, market data, backtest, and paper trader contracts are not renamed or redesigned.
- No hardcoded secrets or `.env` files.

# Verification

```bash
pytest
```
