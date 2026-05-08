# Task 007: Improved Backtesting

# Goal

Improve the existing basic historical backtest with clearer deterministic result reporting while preserving the current strategy and candle-data boundaries.

# Source Requirement

`docs/08_ROADMAP.md` Phase 9: Improved Backtesting.

# Extracted Roles

- Owner role: Backtest Engine
- Supporting roles: Strategy, Market Data Provider, Test Designer
- Forbidden roles: Live Execution, Binance order client, Risk Management, Optimization

# Context

The initial scope through Task 006 is complete and verified. The current backtester is intentionally simple and long-only. This task may improve result reporting and deterministic test scenarios, but it must not turn the backtester into a live execution system or introduce future-phase risk/optimization features.

# Scope

- improve historical backtest result reporting
- add deterministic backtest scenarios and tests
- preserve use of standard candle data
- preserve strategy ownership by calling strategy signals instead of embedding strategy formulas
- keep simulation local and in-memory only

# Out of Scope

- live trading
- real exchange APIs
- Binance order execution
- risk management
- position sizing rules beyond the existing fixed-quantity simulation unless explicitly documented in this task during implementation assumptions
- fees
- slippage
- portfolio optimization
- dashboard
- database
- scheduler
- machine learning
- futures
- leverage

# Requirements

- Existing `BasicBacktester` behavior must remain backward compatible unless an implementation blocker is recorded in `STATUS.md` before code changes.
- Existing strategy and signal contracts must not be renamed or redesigned.
- Existing standard candle data contract must not be changed.
- Backtest result reporting may be extended with simple deterministic summary values, but advanced performance metrics remain out of scope.
- Backtest code must not fetch market data or call exchange APIs.
- Backtest tests must not call real exchange endpoints.

# Status Tracking

## Before Implementation

- [ ] Read `AGENTS.md`.
- [ ] Read `STATUS.md`.
- [ ] Confirm this task matches the current phase and step.
- [ ] Confirm parallel work is safe before starting any parallel work.
- [ ] Record assumptions or blockers in `STATUS.md` before coding if requirements are unclear.

## After Implementation

- [ ] Update `STATUS.md` if the phase, step, goal, active task, blocker, open question, or completion state changed.
- [ ] Mark checklist items complete only when acceptance criteria and verification are satisfied.
- [ ] Leave uncertain items open and document the uncertainty.
- [ ] Confirm the next step is accurate or explicitly left undecided.

# Acceptance Criteria

- Improved backtest result reporting is deterministic and covered by tests.
- Backtest runs on local historical candle data.
- Backtest continues to reuse strategies without modifying strategy formulas.
- Backtest continues to use the standard candle schema.
- Backtest does not call live exchange APIs or place real orders.
- Existing tests continue to pass.

# Required Tests

- Unit Tests: deterministic result reporting for simple scenarios.
- Integration Tests: run with local candle fixture and simple strategy if result reporting touches end-to-end behavior.
- Contract Tests: input uses standard candle schema and existing strategy signal values.
- Safety Tests: no live exchange calls and no real order execution.

# Review Checklist

- Backtest does not contain RSI or other strategy formulas unless a task explicitly assigns strategy work.
- Backtest does not fetch market data.
- Backtest does not place real or paper orders.
- Backtest does not call Binance order endpoints.
- Backtest does not introduce risk management or optimization.
- Public interfaces remain backward compatible unless a blocker was recorded first.
- No hardcoded secrets or `.env` files.

# Verification

```bash
pytest
```
