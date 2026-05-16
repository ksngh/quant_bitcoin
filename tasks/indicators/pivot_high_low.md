# Indicator: Pivot High / Pivot Low

# Source Requirement

Owner provided the Pivot High / Pivot Low specification on 2026-05-16.

This module detects meaningful local highs and lows from already-provided OHLCV candles for downstream trendline, swing structure, support/resistance, and pattern modules. It must not fetch market data, call exchange APIs, or place orders.

## Required Inputs

- `symbol`
- `timestamp`
- `open`
- `high`
- `low`
- `close`

Optional:

- `volume`
- `atr`

## Default Parameters

```yaml
left_window: 3
right_window: 3
allow_equal_high_low: false
minimum_distance_between_pivots: 3
use_atr_filter: false
minimum_pivot_strength_atr: 0.5
require_full_window: true
```

## Mechanical Rules

A pivot high at index `i` is confirmed when:

```text
high[i] > max(high[i-left_window : i])
and
high[i] > max(high[i+1 : i+right_window+1])
```

A pivot low at index `i` is confirmed when:

```text
low[i] < min(low[i-left_window : i])
and
low[i] < min(low[i+1 : i+right_window+1])
```

If `allow_equal_high_low = true`, use `>=` for pivot highs and `<=` for pivot lows.

A pivot at index `i` is confirmed only after `right_window` candles have closed:

```text
confirmed_index = i + right_window
confirmed_timestamp = timestamp[confirmed_index]
```

The system must not use unconfirmed pivots for backtesting or live trading.

## Pivot Strength

Pivot high strength:

```text
left_max_high = max(high[i-left_window : i])
right_max_high = max(high[i+1 : i+right_window+1])
pivot_high_strength = high[i] - max(left_max_high, right_max_high)
```

Pivot low strength:

```text
left_min_low = min(low[i-left_window : i])
right_min_low = min(low[i+1 : i+right_window+1])
pivot_low_strength = min(left_min_low, right_min_low) - low[i]
```

If `use_atr_filter = true`, the applicable strength must be greater than or equal to:

```text
minimum_pivot_strength_atr * atr[i]
```

## Pivot Types

- `PIVOT_HIGH`
- `PIVOT_LOW`
- `BOTH`
- `NONE`
- `INVALID`
- `UNCONFIRMED`

`BOTH` is allowed for candles that are both local highs and local lows.

## Output Fields

Confirmed event rows include:

- `symbol`
- `pivot_timestamp`
- `confirmed_timestamp`
- `pivot_index`
- `confirmed_index`
- `pivot_type`
- `price` and `strength` for single-type pivots
- `high_price`, `low_price`, `high_strength`, and `low_strength` for `BOTH`
- `left_window`
- `right_window`
- `is_confirmed`

## Edge Cases

- Candles with fewer than `left_window` left neighbors are not pivot events.
- With default `require_full_window = true`, candles with fewer than `right_window` right neighbors are not returned because they are unconfirmed.
- With `require_full_window = false`, incomplete right-window candidates may be returned as `UNCONFIRMED` and `is_confirmed = false`.
- Strict mode rejects equal-high/equal-low ties.
- Equal mode allows equal-high/equal-low ties.
- Consecutive same-type pivots closer than `minimum_distance_between_pivots` keep the stronger pivot: higher price for pivot highs, lower price for pivot lows, and larger combined strength for `BOTH`.
- Missing `high` or `low` is invalid input.
- Zero-range candles can be processed, although ATR filtering may reject them.

# Implementation Notes

- Implemented as a pure pandas-based indicator under `quant_bitcoin.indicators`.
- Output is event-based rather than an all-candle aligned series.
- The implementation validates `symbol`, `timestamp`, `open`, `high`, `low`, and `close` because the owner-provided schema requires `symbol` and the output includes `symbol`.
- No market data fetching, order execution, API-key reads, or live-trading behavior is in scope.
