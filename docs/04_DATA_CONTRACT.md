# Candle Data Contract

# Standard Candle Schema

The standard candle schema has exactly these required fields:

| Field | Meaning |
| --- | --- |
| `timestamp` | Candle open time. |
| `open` | First traded price in the candle interval. |
| `high` | Highest traded price in the candle interval. |
| `low` | Lowest traded price in the candle interval. |
| `close` | Last traded price in the candle interval. |
| `volume` | Traded volume in the candle interval. |

# Rules

- `timestamp` must represent the candle open time.
- `open`, `high`, `low`, `close`, and `volume` must be numeric.
- Rows must be sorted ascending by `timestamp`.
- Data providers must normalize exchange-specific raw data before strategy code sees it.
- Strategy code must not depend on Binance-specific raw response fields.
- The first implementation may use a pandas `DataFrame`.
- Do not define a complex custom data model yet unless a future task asks for it.

# Review Checks

- Any provider returning candle data must return the standard schema.
- Strategy tests should use standard candle fields only.
- Binance downloader tests must prove raw Binance fields are normalized before strategy code receives data.
