# Task 003: RSI Strategy

# Goal

Implement an RSI strategy that returns BUY, SELL, or HOLD.

# Source Requirement

`requirements/000_INITIAL_SCOPE.md`

# Extracted Roles

- Owner role: Strategy
- Supporting roles: Test Designer
- Forbidden roles: Market Data Provider, Execution, Configuration for secrets

# Scope

- Signal enum with BUY / SELL / HOLD
- RSI calculation
- RSI strategy using configurable window, buy threshold, and sell threshold

# Out of Scope

- order execution
- quantity calculation
- risk management
- Binance API
- database
- live trading

# Acceptance Criteria

- Strategy returns BUY when RSI crosses or is below the buy condition defined in the task.
- Strategy returns SELL when RSI crosses or is above the sell condition defined in the task.
- Strategy returns HOLD when neither condition is met.
- Strategy uses standard candle data only.

# Required Tests

- Unit Tests: BUY, SELL, HOLD.
- Integration Tests: none required unless wired into backtest later.
- Contract Tests: consumes standard candle schema.
- Safety Tests: no external API calls, no order execution.

# Review Checklist

- Strategy does not fetch data.
- Strategy does not call Binance.
- Strategy does not place orders.
- Strategy does not decide quantity.
