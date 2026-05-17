# Indicator: Volume Ratio

# Source Requirement

Owner provided the Volume Ratio specification on 2026-05-17 as the next indicator task.

# Purpose

Measure whether current trading volume is higher or lower than normal recent volume.

Volume Ratio is used for breakout confirmation, breakdown confirmation, displacement candle validation, order block validation, FVG validation, pattern completion confirmation, and abnormal volume detection.

# Required Inputs

- `symbol`
- `timestamp`
- `volume`

Optional future inputs, not implemented by the initial isolated indicator task unless separately assigned:

- `trading_value`
- `quote_volume`

# Default Parameters

```yaml
window: 20
minimum_volume_ratio_for_confirmation: 1.5
high_volume_ratio_threshold: 2.0
low_volume_ratio_threshold: 0.5
require_full_window: true
reject_zero_average_volume: true
```

# Derived Values

```text
average_volume = mean(volume, window)
volume_ratio = current_volume / average_volume
```

The baseline window includes the current candle, matching the owner-provided pseudocode that selects the most recent `window` candles and uses `current = candles[-1]`.

# Mechanical Definition

Current volume is considered increased when:

```text
volume_ratio >= minimum_volume_ratio_for_confirmation
```

Default:

```text
minimum_volume_ratio_for_confirmation = 1.5
```

# Volume Status

```text
if volume_ratio >= high_volume_ratio_threshold:
    volume_status = HIGH
else if volume_ratio >= minimum_volume_ratio_for_confirmation:
    volume_status = INCREASED
else if volume_ratio <= low_volume_ratio_threshold:
    volume_status = LOW
else:
    volume_status = NORMAL
```

# Output Schema

```json
{
  "symbol": "BTCUSDT",
  "timestamp": "2026-05-16T10:00:00Z",
  "volume": 3000.0,
  "average_volume": 1800.0,
  "volume_ratio": 1.6667,
  "minimum_volume_ratio_for_confirmation": 1.5,
  "volume_confirmation": true,
  "volume_status": "INCREASED",
  "is_valid": true
}
```

# Output Fields

- `symbol`: market symbol.
- `timestamp`: current candle timestamp.
- `volume`: current candle volume.
- `average_volume`: rolling average volume over `window`.
- `volume_ratio`: current volume divided by average volume.
- `minimum_volume_ratio_for_confirmation`: minimum ratio required to confirm volume expansion.
- `volume_confirmation`: `true` when current volume is high enough for confirmation.
- `volume_status`: one of `HIGH`, `INCREASED`, `NORMAL`, `LOW`, or `INVALID`.
- `is_valid`: whether the calculation is valid.

# Edge Cases

## Not enough candles

If `require_full_window = true` and candle count is less than `window`:

```text
is_valid = false
volume_status = INVALID
volume_confirmation = false
```

## Missing volume

If current volume or any volume in the active window is missing:

```text
is_valid = false
volume_status = INVALID
volume_confirmation = false
```

## Zero average volume

If `average_volume == 0`:

```text
is_valid = false
volume_status = INVALID
volume_confirmation = false
```

## Zero current volume

If current volume is zero and the average volume is non-zero:

```text
volume_ratio = 0
volume_status = LOW
volume_confirmation = false
```

## Abnormal one-candle volume spike

Optional robust mode may use:

```text
average_volume = median(volume, window)
```

Mean remains the default initial configuration.

# Optional Trading Value Ratio

A future task may calculate trading-value ratio from `quote_volume` or `trading_value`. The initial Volume Ratio implementation remains limited to base `volume`.

# Recommended Initial Configuration

```yaml
volume_ratio:
  window: 20
  minimum_volume_ratio_for_confirmation: 1.5
  high_volume_ratio_threshold: 2.0
  low_volume_ratio_threshold: 0.5
  require_full_window: true
  reject_zero_average_volume: true
```

# Final Mechanical Rule

```text
average_volume = mean(volume, 20)
volume_ratio = current_volume / average_volume
volume_confirmation = volume_ratio >= 1.5
```

# Implementation Notes

- Implemented only by the assigned Task 031 implementation task.
- The initial implementation is pure and deterministic from already-provided candle data.
- No market-data fetching, exchange API calls, order placement, API-key reads, or live-trading decisions are allowed.
