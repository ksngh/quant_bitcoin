# Task 011: Live Trading Safety Gates

# Goal

Define live-trading safety gates before any live order execution code is implemented.

# Source Requirement

`docs/08_ROADMAP.md` Phase 12: Later Live Trading.

# Extracted Roles

- Owner role: Architect
- Supporting roles: Risk Management, Execution, Configuration, Test Designer
- Forbidden roles: Strategy, Market Data Provider, Binance order client implementation

# Context

Live trading is explicitly out of scope until a future task explicitly permits real order execution and defines safety gates. The project now has local strategy, backtesting, paper trading, Binance candle downloading, and paper-only risk checks. Before any live execution implementation, this task must define the safety gates, configuration requirements, tests, and review criteria that a later live-trading task must satisfy.

# Scope

- define required safety gates for any future live-trading implementation
- define required configuration defaults for live trading to remain disabled by default
- define required tests before any live order code may be written
- define PR review checks for future live-trading work
- update `STATUS.md` after the next concrete live-trading task is defined or explicitly blocked

# Out of Scope

- implementing live trading
- implementing real Binance order execution
- adding exchange clients
- placing orders
- signing requests
- storing or loading API keys
- creating `.env` files
- enabling live trading by default
- changing strategy behavior
- changing market data behavior
- changing paper trader behavior
- changing risk-check behavior
- adding dashboards
- adding databases
- adding schedulers
- adding FastAPI or Streamlit
- adding Docker
- adding machine learning
- adding futures
- adding leverage
- adding portfolio optimization

# Requirements

- No application code may be implemented in this task.
- No live order execution code may be implemented in this task.
- No real exchange client may be implemented in this task.
- No API key, secret, `.env`, or signed-request behavior may be added in this task.
- The future live-trading task must require live trading to be disabled by default.
- The future live-trading task must require explicit user approval before any real order endpoint can be called.
- The future live-trading task must define safety tests that prove no live order endpoint is called unless explicitly enabled in a controlled test path.
- If live-trading safety requirements are unclear, record open questions in `STATUS.md` instead of implementing code.

# Status Tracking

## Before Implementation

- [ ] Read `AGENTS.md`.
- [ ] Read `STATUS.md`.
- [ ] Read `docs/08_ROADMAP.md` Phase 12.
- [ ] Confirm this task matches the current phase and step.
- [ ] Record assumptions, blockers, or unclear items in `STATUS.md` before coding if needed.

## After Implementation

- [ ] Update `STATUS.md` if the phase, step, goal, active task, blocker, open question, or completion state changed.
- [ ] Mark checklist items complete only when acceptance criteria and verification are satisfied.
- [ ] Leave uncertain items open and document the uncertainty.
- [ ] Confirm the next step is accurate or explicitly left undecided.

# Acceptance Criteria

- A future live-trading implementation task or blocker is defined in a task document or `STATUS.md`.
- Future live-trading safety gates are explicit.
- Future live-trading configuration defaults are explicit and disabled by default.
- Future live-trading test requirements are explicit.
- Future live-trading PR review requirements are explicit.
- No application code is changed.
- Existing tests continue to pass.

# Required Tests

- Unit Tests: none required because this is a documentation/safety-gates task.
- Integration Tests: none required.
- Contract Tests: none required.
- Safety Tests: verify no application code, live-trading configuration, API-key handling, or order-execution behavior changed.

# Review Checklist

- No application code was implemented.
- No live trading was introduced.
- No real exchange API usage was introduced.
- No Binance order execution was introduced.
- No signed requests were introduced.
- No API key or `.env` handling was introduced.
- No `ENABLE_LIVE_TRADING=true` default was introduced.
- Future safety gates are explicit enough to review before live code exists.
- `STATUS.md` accurately points to the next safe step.

# Verification

```bash
pytest
```
