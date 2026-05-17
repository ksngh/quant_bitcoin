# Indicator: Swing Structure

# Source Requirement

Owner approved a mechanical Swing Structure indicator on 2026-05-16. The indicator consumes confirmed pivot points and classifies same-type pivot movement into:

- `HH`: higher high
- `HL`: higher low
- `LH`: lower high
- `LL`: lower low

It is used to detect trend direction, trend continuation, trend weakening, and structural breaks.

## Required Inputs

- `symbol`
- `timestamp` / `confirmed_timestamp`
- confirmed pivot points only

Each pivot point includes:

- `pivot_timestamp`
- `confirmed_timestamp`
- `pivot_index`
- `confirmed_index`
- `pivot_type`
- `price`

Allowed pivot types:

- `PIVOT_HIGH`
- `PIVOT_LOW`

Unconfirmed pivots must not be used:

```python
if pivot.is_confirmed == false:
    ignore pivot
```

## Default Parameters

```yaml
minimum_price_change_rate: 0.0
minimum_price_change_atr_multiplier: null
use_atr_threshold: false
ignore_equal_price: true
structure_window: 20
```

Recommended initial configuration:

```yaml
swing_structure:
  minimum_price_change_rate: 0.001
  minimum_price_change_atr_multiplier: null
  use_atr_threshold: false
  ignore_equal_price: true
  structure_window: 20
```

## Core Rules

For pivot highs:

```text
current high > previous pivot high = HH
current high < previous pivot high = LH
```

For pivot lows:

```text
current low > previous pivot low = HL
current low < previous pivot low = LL
```

For equal pivot highs:

```text
current high == previous pivot high = EQUAL_HIGH
```

For equal pivot lows:

```text
current low == previous pivot low = EQUAL_LOW
```

If `ignore_equal_price = true`, equal highs/lows are labeled `EQUAL_OR_NOISE`.

## Thresholded Definition

Small differences may be noise:

```text
change_rate = abs(current_price - previous_price) / previous_price
```

Valid structure change:

```text
change_rate >= minimum_price_change_rate
```

If the threshold is not met:

```text
swing_label = EQUAL_OR_NOISE
```

## ATR-based Definition

Optional ATR-based threshold:

```text
minimum_change = atr * minimum_price_change_atr_multiplier
```

Valid structure change:

```text
abs(current_price - previous_price) >= minimum_change
```

If ATR thresholding is enabled and ATR is missing for the pivot, the swing label is `UNKNOWN`.

## Swing Labels

Allowed labels:

- `HH`
- `HL`
- `LH`
- `LL`
- `EQUAL_HIGH`
- `EQUAL_LOW`
- `EQUAL_OR_NOISE`
- `UNKNOWN`

First pivot high and first pivot low have no previous same-type pivot, so their swing label is `UNKNOWN`.

Missing pivot price behavior:

```text
swing_label = UNKNOWN
market_structure_status = UNKNOWN
```

## Market Structure Status

Allowed statuses:

- `UPTREND`
- `DOWNTREND`
- `RANGE`
- `TRANSITION`
- `UNKNOWN`

Mechanical uptrend condition:

```text
last_high_label == HH
and
last_low_label == HL
```

Mechanical downtrend condition:

```text
last_high_label == LH
and
last_low_label == LL
```

Mechanical range condition:

```text
not UPTREND
and
not DOWNTREND
```

Transition condition:

```text
previous_status == UPTREND
and latest_low_label == LL
```

or:

```text
previous_status == DOWNTREND
and latest_high_label == HH
```

## Output Schema

```json
{
  "symbol": "BTCUSDT",
  "timestamp": "2026-05-16T10:00:00Z",
  "pivot_timestamp": "2026-05-16T09:45:00Z",
  "pivot_type": "PIVOT_HIGH",
  "pivot_price": 65000.0,
  "previous_same_type_pivot_price": 64200.0,
  "swing_label": "HH",
  "change_rate": 0.01246,
  "market_structure_status": "UPTREND"
}
```

## Output Fields

- `symbol`: market symbol.
- `timestamp`: evaluation timestamp, normally current pivot `confirmed_timestamp`.
- `pivot_timestamp`: current pivot timestamp.
- `pivot_type`: `PIVOT_HIGH` or `PIVOT_LOW`.
- `pivot_price`: current pivot price.
- `previous_same_type_pivot_price`: previous pivot price of the same type.
- `swing_label`: one supported swing label.
- `change_rate`: absolute price change rate versus previous same-type pivot.
- `market_structure_status`: one supported market structure status.

# Implementation Notes

- Implemented by `tasks/029_IMPLEMENT_SWING_STRUCTURE.md`.
- Scope is limited to pure deterministic structure classification from already-provided pivot data.
- The implementation must not fetch market data, read API keys or environment secrets, call exchange APIs, place orders, or make live-trading decisions.
