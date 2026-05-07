# Task 002: CSV Data Provider

# Goal

Load candle data from local CSV files and return the standard candle schema.

# Source Requirement

`requirements/000_INITIAL_SCOPE.md`

# Extracted Roles

- Owner role: Market Data Provider
- Supporting roles: Test Designer
- Forbidden roles: Strategy, Backtest Engine, Execution

# Scope

- read candle data from CSV
- normalize columns
- sort by timestamp
- return standard candle schema

# Out of Scope

- Binance API
- live trading
- strategy logic
- execution

# Acceptance Criteria

- Returned data includes `timestamp`, `open`, `high`, `low`, `close`, `volume`.
- Rows are sorted ascending by `timestamp`.
- Numeric fields are converted correctly.
- Missing required columns are rejected or handled explicitly.

# Required Tests

- Unit Tests: CSV loading and numeric conversion.
- Integration Tests: load sample local CSV fixture.
- Contract Tests: output matches standard schema.
- Safety Tests: no external API calls.

# Review Checklist

- Provider does not generate signals.
- Provider does not execute orders.
- Provider does not decide quantity.
