# Task 001: Market Data Contract

# Goal

Define the first market data contract for standard candle data.

# Source Requirement

`requirements/000_INITIAL_SCOPE.md`

# Extracted Roles

- Owner role: Architect
- Supporting roles: Market Data Provider, Test Designer
- Forbidden roles: Strategy, Backtest Engine, Execution

# Context

Must follow `docs/04_DATA_CONTRACT.md`.

# Scope

- Define standard candle fields.
- Define validation expectations if implementation requires them.
- Keep the first implementation simple.

# Out of Scope

- Binance API
- strategy
- backtest
- execution
- live trading

# Acceptance Criteria

- Standard schema uses `timestamp`, `open`, `high`, `low`, `close`, `volume`.
- Timestamp represents candle open time.
- Numeric fields are numeric.
- Rows are sorted ascending by timestamp.

# Required Tests

- Unit Tests: schema helper behavior if code is added.
- Integration Tests: none required.
- Contract Tests: standard schema accepted, missing required fields rejected or handled.
- Safety Tests: no exchange API calls.

# Review Checklist

- Contract does not include Binance-specific raw fields.
- No strategy or execution behavior added.
