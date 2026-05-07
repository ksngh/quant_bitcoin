# Task 005: Paper Trader

# Goal

Record fake trades from signals without calling any exchange order APIs.

# Source Requirement

`requirements/000_INITIAL_SCOPE.md`

# Extracted Roles

- Owner role: Execution
- Supporting roles: Test Designer
- Forbidden roles: Strategy, Market Data Provider, live exchange client

# Scope

- receive symbol, signal, and quantity
- record fake BUY and SELL actions
- ignore HOLD

# Out of Scope

- real exchange API
- Binance order execution
- risk management
- strategy logic

# Acceptance Criteria

- BUY records a fake trade.
- SELL records a fake trade.
- HOLD records no trade.
- No external API is called.

# Required Tests

- Unit Tests: BUY fake trade, SELL fake trade, HOLD no trade.
- Integration Tests: none required unless wired into app later.
- Contract Tests: accepts signal values defined by strategy contract.
- Safety Tests: no external API calls.

# Review Checklist

- Paper trader does not calculate RSI.
- Paper trader does not fetch market data.
- Paper trader does not use live exchange clients.
