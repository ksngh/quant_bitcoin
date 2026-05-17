# Indicator: Average True Range (ATR)

# Source Requirement

Owner assigned ATR implementation with the following mechanical requirements.

## Purpose

Measure market volatility mechanically for future consumers such as breakout buffers, trendline break validation, stop-loss distance, position sizing, displacement candle detection, pattern size normalization, and volatility filtering.

## Required Inputs

- `symbol`
- `timestamp`
- `high`
- `low`
- `close`
- previous candle `close` as `previous_close` when available

## Default Parameters

```yaml
period: 14
smoothing_method: "RMA"
require_full_window: true
reject_missing_price: true
low_volatility_threshold_percent: 1.0
high_volatility_threshold_percent: 4.0
```

## True Range

```text
true_range = max(
    high - low,
    abs(high - previous_close),
    abs(low - previous_close)
)
```

For the first candle, when `previous_close` is unavailable:

```text
true_range = high - low
```

## ATR

ATR is the smoothed average of true range. Default:

```text
ATR14 = RMA(true_range, 14)
```

Supported smoothing methods:

- `SMA`
- `EMA`
- `RMA`

### SMA

```text
ATR = mean(true_range, period)
```

### EMA

```text
multiplier = 2 / (period + 1)
ATR[i] = true_range[i] * multiplier + ATR[i-1] * (1 - multiplier)
```

### RMA

```text
ATR[i] = (ATR[i-1] * (period - 1) + true_range[i]) / period
```

The initial RMA value is the SMA of the first full `period` true range values.

## Normalized ATR

```text
normalized_atr = atr / close
normalized_atr_percent = normalized_atr * 100
```

If `close <= 0`, normalized values are `null`; ATR itself may still be valid when the high, low, and previous close inputs are valid.

## Volatility Status

- `HIGH` when `normalized_atr_percent >= high_volatility_threshold_percent`
- `LOW` when `normalized_atr_percent <= low_volatility_threshold_percent`
- `NORMAL` otherwise
- `UNKNOWN` when normalized ATR percent is unavailable or ATR is invalid/not ready

## Output Schema

```json
{
  "symbol": "BTCUSDT",
  "timestamp": "2026-05-16T10:00:00Z",
  "period": 14,
  "true_range": 850.0,
  "atr": 620.5,
  "close": 65000.0,
  "normalized_atr": 0.00955,
  "normalized_atr_percent": 0.955,
  "smoothing_method": "RMA",
  "volatility_status": "LOW",
  "is_valid": true
}
```

## Edge Cases

- Not enough candles with `require_full_window = true`: `is_valid = false`, `volatility_status = UNKNOWN`.
- Missing `high`, `low`, or `close`: `is_valid = false` for that row.
- Missing previous close on the first candle: use `high - low`.
- Missing previous close after the first candle: `is_valid = false`.
- `high < low`: `is_valid = false`.
- Negative true range should never occur; if it does, `is_valid = false`.

# Implementation Notes

- Implemented as a pure pandas-based indicator under `quant_bitcoin.indicators`.
- The implementation returns one output row per candle and also provides a latest-row snapshot helper for consumers that need the owner-provided single-object schema.
- No market data fetching, exchange API calls, order placement, risk management, live trading, database, dashboard, scheduler, or framework wiring belongs in this indicator task.
