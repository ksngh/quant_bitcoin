# Data Contract

## Standard Candle Schema

All market data providers must return candle data with these fields:

- `timestamp`: candle open time.
- `open`: price at the start of the candle.
- `high`: highest traded price during the candle.
- `low`: lowest traded price during the candle.
- `close`: price at the end of the candle.
- `volume`: traded volume during the candle.

## Rules

- `timestamp` must represent the candle open time.
- `open`, `high`, `low`, `close`, and `volume` must be numeric.
- Rows must be sorted ascending by `timestamp`.
- Data providers must normalize exchange-specific raw data before strategy code sees it.
- Strategy code must not depend on Binance-specific raw response fields.
- The first implementation may use a pandas DataFrame.
- Do not define a complex custom data model yet unless a future task asks for it.
