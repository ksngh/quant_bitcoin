# Indicator: Liquidity Trading Value / Volume

# Source Requirement

## 01. Liquidity: Trading Value / Volume

## Purpose

Define whether a market is liquid enough for automated pattern detection and trading.

This module should run before all pattern modules.

## Required Inputs

- symbol
- timestamp
- open
- high
- low
- close
- volume
- quote_volume optional

## Derived Values

### trading_value

If `quote_volume` exists:

```text
trading_value = quote_volume
```

Otherwise:

```text
trading_value = close * volume
```

### average_volume

```text
average_volume = mean(volume, window)
```

Default:

```text
window = 20
```

### average_trading_value

```text
average_trading_value = mean(trading_value, window)
```

Default:

```text
window = 20
```

## Mechanical Definition

A market passes the liquidity filter when:

```text
average_trading_value >= minimum_required_trading_value
```

Optional stricter condition:

```text
average_volume >= minimum_required_volume
```

## Default Parameters

```yaml
window: 20
minimum_required_trading_value: configurable
minimum_required_volume: null
use_quote_volume_if_available: true
require_full_window: true
reject_zero_volume: true
```

## Liquidity Status

```text
if average_trading_value >= minimum_required_trading_value * 5:
    status = HIGH

else if average_trading_value >= minimum_required_trading_value:
    status = NORMAL

else if average_trading_value > 0:
    status = LOW

else:
    status = UNTRADABLE
```

## Output Schema

```json
{
  "symbol": "BTCUSDT",
  "timestamp": "2026-05-16T10:00:00Z",
  "volume": 1250.5,
  "trading_value": 81250000.0,
  "average_volume": 980.2,
  "average_trading_value": 64100000.0,
  "minimum_required_trading_value": 1000000.0,
  "liquidity_pass": true,
  "liquidity_status": "HIGH"
}
```

## Output Fields

### volume

Current candle volume.

### trading_value

Current candle monetary trading value.

### average_volume

Rolling average volume over `window`.

### average_trading_value

Rolling average trading value over `window`.

### minimum_required_trading_value

Minimum threshold required to pass the liquidity filter.

### liquidity_pass

Boolean result.

```text
true = tradable
false = not tradable
```

### liquidity_status

One of:

```text
HIGH
NORMAL
LOW
UNTRADABLE
```

## Edge Cases

### Not enough candles

If `require_full_window = true` and candle count is less than `window`:

```text
liquidity_pass = false
status = UNTRADABLE
```

### Zero volume

If `reject_zero_volume = true` and current volume is zero:

```text
liquidity_pass = false
status = UNTRADABLE
```

### Missing close or volume

If `close` or `volume` is missing:

```text
return invalid result
```

### Abnormal volume spike

Optional robust mode:

```text
average_trading_value = median(trading_value, window)
```

Use this only if volume spikes distort the mean.

## Pseudocode

```python
def calculate_liquidity(candles, config):
    if config.require_full_window and len(candles) < config.window:
        return invalid_liquidity_result("not_enough_candles")

    current = candles[-1]

    if current.close is None or current.volume is None:
        return invalid_liquidity_result("missing_required_value")

    if config.reject_zero_volume and current.volume == 0:
        return {
            "liquidity_pass": False,
            "liquidity_status": "UNTRADABLE"
        }

    trading_values = []

    for candle in candles[-config.window:]:
        if candle.quote_volume is not None and config.use_quote_volume_if_available:
            trading_value = candle.quote_volume
        else:
            trading_value = candle.close * candle.volume

        trading_values.append(trading_value)

    volumes = [candle.volume for candle in candles[-config.window:]]

    average_volume = mean(volumes)
    average_trading_value = mean(trading_values)

    liquidity_pass = average_trading_value >= config.minimum_required_trading_value

    if average_trading_value >= config.minimum_required_trading_value * 5:
        status = "HIGH"
    elif average_trading_value >= config.minimum_required_trading_value:
        status = "NORMAL"
    elif average_trading_value > 0:
        status = "LOW"
    else:
        status = "UNTRADABLE"

    return {
        "symbol": current.symbol,
        "timestamp": current.timestamp,
        "volume": current.volume,
        "trading_value": trading_values[-1],
        "average_volume": average_volume,
        "average_trading_value": average_trading_value,
        "minimum_required_trading_value": config.minimum_required_trading_value,
        "liquidity_pass": liquidity_pass,
        "liquidity_status": status
    }
```

# Implementation Notes

- To be implemented only by a later assigned implementation task.
- No application code is implemented by this intake document.
- Future implementation task should clarify the invalid result schema for missing values and insufficient data.
- Future implementation task should clarify whether `minimum_required_volume` is included in `liquidity_pass` when configured.
- Future implementation task should clarify whether abnormal volume spike robust mode is in scope for the first implementation.
