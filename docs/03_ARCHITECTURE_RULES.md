# Architecture Rules

# Market Data

Allowed:

- load local candle data
- later fetch Binance historical candles
- normalize external data into standard candle schema

Forbidden:

- generate trading signals
- execute trades
- decide quantity
- perform risk management

# Strategy

Allowed:

- calculate indicators needed by the strategy
- generate BUY / SELL / HOLD
- optionally return a signal reason

Forbidden:

- fetch data
- call Binance
- place orders
- decide quantity
- read API keys
- write files or database records
- send notifications

# Backtest

Allowed:

- simulate historical strategy execution
- use historical candle data
- produce simple backtest results

Forbidden:

- call live exchange order APIs
- place real orders

# Execution

Allowed:

- paper trading first
- later live execution only when explicitly requested

Forbidden:

- calculate RSI or other strategy indicators
- define strategy rules
- fetch market data

# App Layer

Allowed:

- wire components together
- run a use case

Forbidden:

- contain indicator formulas
- parse raw Binance responses directly
- contain real order logic directly

# Configuration

Allowed:

- hold local settings
- later read environment variables

Forbidden:

- hardcode secrets
- contain business logic

# Tests

Allowed:

- verify behavior with local fixtures and mocks
- verify standard candle schema
- verify no unsafe exchange order calls

Forbidden:

- call real exchange order endpoints
- require real API keys for unit tests
- depend on live market availability for deterministic tests

# Review

PR review must reject changes that cross owner boundaries, add forbidden responsibilities, skip required tests, or introduce live trading behavior outside an explicit future task.
