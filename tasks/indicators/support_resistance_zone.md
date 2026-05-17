# Indicator: Support / Resistance Zone

# Source Requirement

Owner provided the Support / Resistance Zone specification on 2026-05-17.

The indicator detects price zones where the market has reacted multiple times.
Zones are built mechanically from confirmed pivot highs and pivot lows and are
intended for future consumers such as breakout detection, neckline validation,
order-block context, liquidity zones, pattern validation, stop-loss placement,
and target placement.

# Required Inputs

- `symbol`
- evaluation `timestamp`
- confirmed pivot points
- `atr`

Each pivot point includes:

- `pivot_timestamp`
- `confirmed_timestamp`
- `pivot_index`
- `pivot_type`
- `price`

Allowed pivot types:

- `PIVOT_HIGH`
- `PIVOT_LOW`

# Default Parameters

```yaml
support_resistance_zone:
  zone_width_atr_multiplier: 0.5
  minimum_touch_count: 2
  strong_touch_count: 3
  lookback_pivot_count: 50
  merge_overlapping_zones: true
  use_atr_zone_width: true
  fallback_zone_width_rate: 0.003
  breakout_atr_multiplier: 0.2
  maximum_zone_width_rate: 0.02
  require_confirmed_pivots: true
```

# Mechanical Rules

Support zones are clusters of pivot lows within a defined price range.
Resistance zones are clusters of pivot highs within a defined price range.
Overlapping support and resistance zones may be merged into a `MIXED` reaction
zone.

When ATR is available and ATR width is enabled:

```text
zone_width = atr * zone_width_atr_multiplier
```

When ATR is unavailable:

```text
zone_width = reference_price * fallback_zone_width_rate
```

For a candidate pivot price:

```text
zone_low = pivot_price - zone_width
zone_high = pivot_price + zone_width
```

A touch is counted when another same-type pivot price falls inside the candidate
zone:

```text
zone_low <= pivot_price <= zone_high
```

A valid zone requires:

```text
touch_count >= minimum_touch_count
```

A strong zone requires:

```text
touch_count >= strong_touch_count
```

Very wide zones are invalid when:

```text
zone_width / center_price > maximum_zone_width_rate
```

Broken support:

```text
close < zone_low - atr * breakout_atr_multiplier
```

Broken resistance:

```text
close > zone_high + atr * breakout_atr_multiplier
```

# Output Schema

Each zone emits:

- `symbol`
- `timestamp`
- `zone_type`: `SUPPORT`, `RESISTANCE`, or `MIXED`
- `zone_status`: `VALID`, `WEAK`, `STRONG`, `BROKEN`, `FLIPPED`, or `INVALID`
- `zone_low`
- `zone_high`
- `center_price`
- `touch_count`
- `pivot_indices`
- `first_touch_timestamp`
- `last_touch_timestamp`
- `zone_width`
- `atr`
- `is_broken`
- `is_valid`

# Edge Cases

- No pivot points returns an empty zone list.
- Zones with fewer than `minimum_touch_count` are not emitted.
- Missing ATR uses percentage fallback width.
- Overlapping same-type zones are merged when enabled.
- Overlapping support and resistance zones become `MIXED` when merging is
  enabled.
- Broken-zone checks require an ATR value for the breakout buffer.
- Zones wider than `maximum_zone_width_rate` relative to center price are marked
  invalid.

# Implementation Notes

- Implemented by Task 032 as a pure deterministic indicator.
- The implementation consumes already-provided pivot rows only.
- The implementation must not fetch market data, read API keys, call exchange
  APIs, place orders, or add live-trading behavior.
