# Task 012: Live Trading Implementation Blocker

# Goal

Block live-trading implementation until explicit human approval, credential policy, exchange-sandbox policy, and real-order safety requirements are documented.

# Source Requirement

`docs/08_ROADMAP.md` Phase 12: Later Live Trading.

# Extracted Roles

- Owner role: Architect
- Supporting roles: Risk Management, Execution, Configuration, Test Designer
- Forbidden roles: Strategy, Market Data Provider, Binance order client implementation

# Context

Task 011 defined live-trading safety gates before any live order execution code. The project still does not have explicit approval to implement real exchange order execution, a credential policy, a testnet/sandbox policy, or a complete real-order safety checklist. Therefore live-trading implementation must remain blocked.

# Live Trading Safety Gates

Any future task that implements live trading must satisfy all gates below before code is written:

1. Explicit human approval for live trading in the assigned task prompt.
2. A documented credential policy that forbids committing API keys, secrets, or `.env` files.
3. Live trading disabled by default in all configuration.
4. No `ENABLE_LIVE_TRADING=true` default or equivalent permissive default.
5. A testnet/sandbox-first policy or a documented reason if unavailable.
6. A real-order endpoint allowlist documented before implementation.
7. A kill-switch or explicit disable mechanism documented before implementation.
8. Risk checks must run before any live order request.
9. Tests must prove no real order endpoint is called unless a controlled test path explicitly enables it with mocks.
10. PR review must explicitly check API keys, `.env` files, signed requests, order endpoints, and unsafe defaults.

# Current Decision

Live trading implementation is blocked.

Reason:
The project has not yet received explicit human approval for real order execution and does not yet have a credential policy, sandbox policy, real-order endpoint allowlist, or kill-switch design.

# Scope

- document the live-trading implementation blocker
- document the safety gates required before live trading can be considered
- update `STATUS.md` to record the blocker and stop further live-trading implementation

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
- `STATUS.md` must clearly record that live-trading implementation is blocked.
- The blocker must explain what approval or documentation is needed to unblock future live-trading work.

# Status Tracking

## Before Implementation

- [ ] Read `AGENTS.md`.
- [ ] Read `STATUS.md`.
- [ ] Read `tasks/011_LIVE_TRADING_SAFETY_GATES.md`.
- [ ] Confirm this task matches the current phase and step.

## After Implementation

- [ ] Update `STATUS.md` with the live-trading blocker.
- [ ] Mark checklist items complete only when acceptance criteria and verification are satisfied.
- [ ] Leave uncertain items open and document the uncertainty.
- [ ] Confirm the next step is blocked or explicitly left undecided.

# Acceptance Criteria

- Live-trading safety gates are documented.
- Live-trading implementation is explicitly blocked.
- The blocker states what is required to unblock live-trading implementation.
- No application code is changed.
- Existing tests continue to pass.

# Required Tests

- Unit Tests: none required because this is a documentation/blocker task.
- Integration Tests: none required.
- Contract Tests: none required.
- Safety Tests: verify no application code, live-trading configuration, API-key handling, signed-request behavior, or order-execution behavior changed.

# Review Checklist

- No application code was implemented.
- No live trading was introduced.
- No real exchange API usage was introduced.
- No Binance order execution was introduced.
- No signed requests were introduced.
- No API key or `.env` handling was introduced.
- No `ENABLE_LIVE_TRADING=true` default was introduced.
- `STATUS.md` clearly records the blocker.

# Verification

```bash
pytest
```
