# Task 006: Binance Candle Downloader

# Goal

Fetch Binance historical candle data and normalize it to the standard candle schema.

# Source Requirement

`requirements/000_INITIAL_SCOPE.md`

# Extracted Roles

- Owner role: Market Data Provider
- Supporting roles: Configuration, Test Designer
- Forbidden roles: Strategy, Backtest Engine, Execution

# Scope

- fetch historical candles
- support minute-level candles
- normalize to standard candle schema
- no order execution

# Out of Scope

- live trading
- real order placement
- risk management
- strategy logic

# Acceptance Criteria

- Downloader supports historical candle retrieval.
- Minute-level candles are supported.
- Returned data follows standard candle schema.
- Unit tests do not require real API keys.
- No order endpoint is called.

# Required Tests

- Unit Tests: mock Binance response normalization.
- Integration Tests: optional mocked HTTP integration.
- Contract Tests: output standard candle schema.
- Safety Tests: reject or prove absence of order endpoint usage.

# Review Checklist

- Downloader does not generate signals.
- Downloader does not place orders.
- Downloader does not decide quantity.
