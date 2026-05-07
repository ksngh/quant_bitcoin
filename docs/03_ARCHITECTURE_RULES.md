# Architecture Rules

These boundaries apply to future implementation tasks.

## Market Data

Allowed:

- load local candle data
- later fetch Binance historical candles
- normalize external data into standard candle schema

Forbidden:

- generate trading signals
- execute trades
- decide quantity
- perform risk management

## Strategy

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

## Backtest

Allowed:

- simulate historical strategy execution
- use historical candle data
- produce simple backtest results

Forbidden:

- call live exchange order APIs
- place real orders

## Execution

Allowed:

- paper trading first
- later live execution only when explicitly requested

Forbidden:

- calculate RSI or other strategy indicators
- define strategy rules
- fetch market data

## App Layer

Allowed:

- wire components together
- run a use case

Forbidden:

- contain indicator formulas
- parse raw Binance responses directly
- contain real order logic directly

## Configuration

Allowed:

- hold local settings
- later read environment variables

Forbidden:

- hardcode secrets
- contain business logic

## Tests

Allowed:

- verify behavior for the assigned task
- verify architecture boundaries
- verify data contracts
- verify safety rules

Forbidden:

- require real API keys for unit tests
- call real order endpoints
- depend on unrelated future features

## Review

Allowed:

- check requirement match
- check role ownership
- check architecture boundaries
- check safety and tests

Forbidden:

- approve scope expansion without a task update
- ignore missing tests for changed behavior
