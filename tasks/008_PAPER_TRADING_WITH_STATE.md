# Task 008: Paper Trading With State

# Goal

Extend paper trading to maintain local paper-mode state across actions, including balances, positions, and trade history, without calling exchange APIs.

# Source Requirement

`docs/08_ROADMAP.md` Phase 10: Paper Trading With State.

# Extracted Roles

- Owner role: Execution
- Supporting roles: Strategy, Test Designer
- Forbidden roles: Market Data Provider, live exchange client, Binance order client, Risk Management

# Context

Task 005 introduced a minimal in-memory `PaperTrader` that records fake BUY and SELL actions and ignores HOLD. Phase 10 may extend paper mode with local state transitions only. This task must not introduce live trading, real account state, exchange clients, or risk management.

# Scope

- maintain paper cash balance in memory
- maintain paper position quantities by symbol in memory
- maintain paper trade history in memory
- process BUY and SELL signals using local paper state only
- ignore HOLD without changing state
- keep behavior deterministic and covered by tests

# Out of Scope

- live trading
- real exchange APIs
- Binance order execution
- real account state
- real balances
- risk management
- order routing
- fees
- slippage
- database persistence
- dashboard
- scheduler
- machine learning
- futures
- leverage
- portfolio optimization

# Requirements

- Paper trading must never call real exchange order APIs.
- Paper trading must not fetch market data.
- Paper trading must not calculate RSI or other strategy indicators.
- Paper trading must accept signal values from the existing strategy contract.
- Paper state must remain local and in-memory.
- Existing `PaperTrader` behavior should remain backward compatible unless a blocker is recorded in `STATUS.md` before implementation.
- The implementation must not require API keys, secrets, `.env` files, network access, a database, or a scheduler.

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

- BUY updates local paper cash, position, and trade history deterministically.
- SELL updates local paper cash, position, and trade history deterministically.
- HOLD leaves paper state unchanged.
- Invalid state transitions are rejected or handled explicitly with tests.
- Paper trader accepts the existing strategy `Signal` values.
- Paper trader does not fetch data, calculate indicators, call exchange APIs, or place real orders.
- Existing tests continue to pass.

# Required Tests

- Unit Tests: BUY state transition, SELL state transition, HOLD no-op, invalid transition handling.
- Integration Tests: none required unless this task explicitly wires an existing strategy signal into paper state handling.
- Contract Tests: accepts signal values defined by the strategy contract.
- Safety Tests: no external API calls, no exchange order endpoints, no required API keys or `.env` files.

# Review Checklist

- Paper trader does not calculate RSI or embed strategy formulas.
- Paper trader does not fetch candle or market data.
- Paper trader does not use live exchange clients.
- Paper trader does not call Binance order endpoints.
- Paper trader does not introduce risk management, fees, slippage, leverage, futures, or portfolio optimization.
- State remains local and in-memory only.
- Public interfaces remain backward compatible unless a blocker was recorded first.
- No hardcoded secrets or `.env` files.

# Verification

```bash
pytest
```
