# Purpose

Testing verifies requirements, architecture boundaries, data contracts, and safety.

# Test Levels

- Unit tests
- Integration tests
- Contract tests
- Safety tests
- Regression tests

# Required Tests by Area

## Market Data

- returns `timestamp`, `open`, `high`, `low`, `close`, `volume`
- sorts rows by `timestamp` ascending
- converts numeric fields correctly
- rejects or handles missing required columns
- normalizes Binance raw response before strategy sees it

## Strategy

- BUY signal
- SELL signal
- HOLD signal
- no external API calls
- no order execution
- no quantity decision

## Backtest

- runs on local historical data
- reuses strategy without modifying it
- does not call live exchange APIs
- returns basic result

## Paper Trader

- BUY records fake trade
- SELL records fake trade
- HOLD records no trade
- no external API calls

## Binance Candle Downloader

- normalizes mock Binance response
- returns standard candle schema
- does not call order endpoints
- does not require real API keys for unit tests

# Verification Commands

Default:

```bash
pytest
```

If configured later:

```bash
ruff check .
mypy .
```
