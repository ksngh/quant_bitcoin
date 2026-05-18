# Indicator And Pattern Class Usage

# Purpose

This document lists the primary classes, dataclasses, enums, result/event objects, and public functions for the implemented indicator and pattern modules. It gives high-level usage guidance only. It does not promise APIs that are not present in the current codebase.

# General Usage Rules

- Use completed candle data sorted ascending by `timestamp`.
- Prefer `pandas.DataFrame` inputs for indicator functions.
- Pattern detectors accept either a `pandas.DataFrame` or an iterable of candle dictionaries.
- Required candle columns differ by module; missing required columns raise `ValueError`.
- Public configuration objects are frozen dataclasses with default values.
- Indicator functions generally return DataFrames or latest-row dictionaries.
- Pattern detectors return lists of frozen event dataclass instances.
- Empty input or no detected structure returns an empty frame/list or a null-filled snapshot, depending on the API.
- None of these APIs place orders, fetch exchange data, or perform live trading.

# Indicator Public APIs

## ATR

Module: `quant_bitcoin.indicators.atr`

Classes and enums:

- `AtrConfig`
- `AtrSmoothingMethod`: `SMA`, `EMA`, `RMA`
- `VolatilityStatus`: `LOW`, `NORMAL`, `HIGH`, `UNKNOWN`

Constants:

- `ATR_OUTPUT_COLUMNS`

Functions:

- `calculate_atr(candles, config=None)`
- `calculate_true_range(high, low, previous_close)`
- `classify_volatility(normalized_atr_percent, config=None)`
- `calculate_atr_snapshot(candles, config=None)`

Required input columns for `calculate_atr`:

- `symbol`, `timestamp`, `high`, `low`, `close`

Output style:

- DataFrame with one row per input candle.
- Invalid warm-up or invalid-price rows are included with `is_valid=False`.
- Empty input returns an empty DataFrame with ATR output columns.

Example:

```python
from quant_bitcoin.indicators import AtrConfig, calculate_atr

atr_rows = calculate_atr(
    candles[["symbol", "timestamp", "high", "low", "close"]],
    AtrConfig(period=14),
)
latest_atr = atr_rows.iloc[-1]["atr"] if not atr_rows.empty else None
```

## Volume Ratio

Module: `quant_bitcoin.indicators.volume_ratio`

Classes and enums:

- `VolumeRatioConfig`
- `VolumeAverageMethod`: `MEAN`, `MEDIAN`
- `VolumeStatus`: `HIGH`, `INCREASED`, `NORMAL`, `LOW`, `INVALID`

Constants:

- `REQUIRED_VOLUME_RATIO_COLUMNS`
- `VOLUME_RATIO_OUTPUT_COLUMNS`

Functions:

- `calculate_volume_ratio(candles, config=None)`
- `classify_volume_status(volume_ratio, config=None)`
- `calculate_volume_ratio_snapshot(candles, config=None)`

Required input columns:

- `symbol`, `timestamp`, `volume`

Output style:

- DataFrame with one row per input candle.
- Warm-up rows can be invalid when full windows are required.
- Rows include `volume_ratio`, `volume_confirmation`, `volume_status`, and `is_valid`.

Example:

```python
from quant_bitcoin.indicators import VolumeRatioConfig, calculate_volume_ratio

volume_rows = calculate_volume_ratio(
    candles[["symbol", "timestamp", "volume"]],
    VolumeRatioConfig(window=20),
)
confirmed = bool(volume_rows.iloc[-1]["volume_confirmation"])
```

## Pivot High / Pivot Low

Module: `quant_bitcoin.indicators.pivots`

Classes and enums:

- `PivotConfig`
- `PivotType`: `PIVOT_HIGH`, `PIVOT_LOW`, `BOTH`, `NONE`, `INVALID`, `UNCONFIRMED`

Functions:

- `detect_pivots(candles, config=None)`
- `remove_close_duplicate_pivots(pivots, config)`

Required input columns:

- `symbol`, `timestamp`, `open`, `high`, `low`, `close`

Output style:

- DataFrame of pivot or unconfirmed rows with pivot metadata.
- Confirmed pivots include `is_confirmed=True` and confirmation metadata.

Example:

```python
from quant_bitcoin.indicators import PivotConfig, detect_pivots

pivots = detect_pivots(
    candles[["symbol", "timestamp", "open", "high", "low", "close"]],
    PivotConfig(left_window=3, right_window=3),
)
confirmed = pivots[pivots["is_confirmed"] == True]
```

## Swing Structure

Module: `quant_bitcoin.indicators.swing_structure`

Classes and enums:

- `SwingStructureConfig`
- `SwingLabel`: `HH`, `HL`, `LH`, `LL`, `EQUAL_HIGH`, `EQUAL_LOW`, `EQUAL_OR_NOISE`, `UNKNOWN`
- `MarketStructureStatus`: `UPTREND`, `DOWNTREND`, `RANGE`, `TRANSITION`, `UNKNOWN`

Functions:

- `classify_swing_structure(pivots, config=None)`
- `classify_high(current_high, previous_high, config=None)`
- `classify_low(current_low, previous_low, config=None)`
- `classify_market_status(recent_labels, config=None)`

Expected input shape:

- Pivot rows with pivot type, pivot price, pivot index, timestamp, and confirmation fields.

Output style:

- DataFrame of swing labels and market status derived from the supplied pivot sequence.

Example:

```python
from quant_bitcoin.indicators import classify_swing_structure

swing_rows = classify_swing_structure(confirmed_pivots)
market_status = swing_rows.iloc[-1]["market_structure_status"] if not swing_rows.empty else "UNKNOWN"
```

## Support / Resistance Zone

Module: `quant_bitcoin.indicators.support_resistance_zone`

Classes and enums:

- `SupportResistanceZoneConfig`
- `ZoneType`: `SUPPORT`, `RESISTANCE`, `MIXED`
- `ZoneStatus`: `VALID`, `WEAK`, `STRONG`, `BROKEN`, `FLIPPED`, `INVALID`

Constants:

- `REQUIRED_SUPPORT_RESISTANCE_PIVOT_COLUMNS`
- `SUPPORT_RESISTANCE_ZONE_OUTPUT_COLUMNS`

Functions:

- `detect_support_resistance_zones(pivots, current_close=None, atr=None, timestamp=None, config=None)`
- `merge_overlapping_zones(zones, config=None)`
- `merge_support_resistance_overlaps(zones, config=None)`
- `update_zone_status(zone, current_close, atr, config=None)`

Expected input shape:

- Pivot rows with pivot type, pivot price, pivot index, timestamp, and confirmation metadata.

Output style:

- DataFrame of zone records with boundaries, touch counts, type, status, and source pivots.
- Empty or insufficient pivot input returns an empty zone frame.

Example:

```python
from quant_bitcoin.indicators import SupportResistanceZoneConfig, detect_support_resistance_zones

zones = detect_support_resistance_zones(
    confirmed_pivots,
    current_close=float(candles.iloc[-1]["close"]),
    atr=latest_atr,
    timestamp=candles.iloc[-1]["timestamp"],
    config=SupportResistanceZoneConfig(minimum_touch_count=2),
)
```

## Displacement Candle

Module: `quant_bitcoin.indicators.displacement_candle`

Classes and enums:

- `DisplacementCandleConfig`
- `DisplacementDirection`: `BULLISH`, `BEARISH`, `NONE`, `INVALID`
- `DisplacementStatus`: `VALID`, `WEAK`, `NONE`, `INVALID`

Constants:

- `REQUIRED_DISPLACEMENT_CANDLE_COLUMNS`
- `DISPLACEMENT_CANDLE_OUTPUT_COLUMNS`

Functions:

- `detect_displacement_candles(candles, config=None)`
- `detect_displacement_candle(candle, config=None)`
- `calculate_displacement_candle_snapshot(candles, config=None)`
- `invalid_displacement_result(reason, base=None)`

Expected input columns:

- `symbol`, `timestamp`, `open`, `high`, `low`, `close`
- `atr` when ATR filtering is enabled
- `volume_ratio` when volume filtering is enabled

Output style:

- DataFrame with one displacement result per input candle.
- Single-candle API returns one dictionary.
- Invalid helper returns a dictionary with invalid status and supplied reason.

Example:

```python
from quant_bitcoin.indicators import DisplacementCandleConfig, detect_displacement_candles

indicator_frame = candles.copy()
indicator_frame["atr"] = atr_rows["atr"]
indicator_frame["volume_ratio"] = volume_rows["volume_ratio"]

displacement_rows = detect_displacement_candles(
    indicator_frame[["symbol", "timestamp", "open", "high", "low", "close", "atr", "volume_ratio"]],
    DisplacementCandleConfig(),
)
```

# Pattern Public APIs

## Fair Value Gap

Module: `quant_bitcoin.patterns.fair_value_gap`

Classes and enums:

- `FairValueGapConfig`
- `FairValueGapState`
- `PatternType`
- `PatternDirection`
- `PatternStatus`
- `PatternEvent`

Functions:

- `detect_patterns(candles, symbol=None, timeframe=None, config=None)`
- `detect_fair_value_gaps(candles, symbol=None, timeframe=None, config=None)`
- `filter_new_events(events, seen_event_ids)`

Required input columns:

- `timestamp`, `open`, `high`, `low`, `close`, `volume`
- `symbol` is optional when the caller passes `symbol`; otherwise it is added as `UNKNOWN` when missing.

Output style:

- List of `PatternEvent` objects.
- Empty list when fewer than three candles are supplied or no FVG is found.
- `ValueError` for missing columns, unsorted timestamps, invalid numeric data, or required unavailable filters without explicit pass values.

Example:

```python
from quant_bitcoin.patterns import FairValueGapConfig, detect_fair_value_gaps, filter_new_events

events = detect_fair_value_gaps(
    candles,
    symbol="BTCUSDT",
    timeframe="1h",
    config=FairValueGapConfig(),
)
new_events = filter_new_events(events, seen_event_ids=set())
```

## Trendline Break

Module: `quant_bitcoin.patterns.trendline_break`

Classes and enums:

- `TrendlineBreakConfig`
- `TrendlineBreakDirection`
- `TrendlineBreakStatus`
- `TrendlineType`
- `TrendlineBreakEvent`

Function:

- `detect_trendline_breaks(candles, symbol=None, timeframe=None, config=None)`

Required input columns:

- `timestamp`, `open`, `high`, `low`, `close`, `volume`

Output style:

- List of `TrendlineBreakEvent` objects.
- Empty list for insufficient candles, unavailable ATR/volume context, or no qualifying break.

Example:

```python
from quant_bitcoin.patterns import TrendlineBreakConfig, detect_trendline_breaks

break_events = detect_trendline_breaks(
    candles,
    symbol="BTCUSDT",
    timeframe="1h",
    config=TrendlineBreakConfig(minimum_touch_count=2),
)
```

## Order Block

Module: `quant_bitcoin.patterns.order_block`

Classes and enums:

- `OrderBlockConfig`
- `OrderBlockDirection`
- `OrderBlockStatus`
- `OrderBlockState`
- `OrderBlockZoneDefinition`
- `OrderBlockEvent`

Function:

- `detect_order_blocks(candles, symbol=None, timeframe=None, config=None)`

Required input columns:

- `timestamp`, `open`, `high`, `low`, `close`, `volume`

Output style:

- List of `OrderBlockEvent` objects.
- Events include zone boundaries, source/displacement candle metadata, state, mitigation depth, score, and reference prices.

Example:

```python
from quant_bitcoin.patterns import OrderBlockConfig, OrderBlockZoneDefinition, detect_order_blocks

order_blocks = detect_order_blocks(
    candles,
    symbol="BTCUSDT",
    timeframe="1h",
    config=OrderBlockConfig(zone_definition=OrderBlockZoneDefinition.FULL_RANGE),
)
```

## Cup And Handle

Module: `quant_bitcoin.patterns.cup_and_handle`

Classes and enums:

- `CupAndHandleConfig`
- `CupAndHandleDirection`
- `CupAndHandleStatus`
- `CupAndHandleEvent`

Function:

- `detect_cup_and_handle_patterns(candles, symbol=None, timeframe=None, config=None)`

Required input columns:

- `timestamp`, `open`, `high`, `low`, `close`, `volume`

Output style:

- List of `CupAndHandleEvent` objects.
- Current implementation emits bullish completed breakout events only.

Example:

```python
from quant_bitcoin.patterns import CupAndHandleConfig, detect_cup_and_handle_patterns

cup_events = detect_cup_and_handle_patterns(
    candles,
    symbol="BTCUSDT",
    timeframe="4h",
    config=CupAndHandleConfig(),
)
```

## Diamond

Module: `quant_bitcoin.patterns.diamond`

Classes and enums:

- `DiamondConfig`
- `DiamondDirection`
- `DiamondStatus`
- `DiamondEvent`

Function:

- `detect_diamond_patterns(candles, symbol=None, timeframe=None, config=None)`

Required input columns:

- `timestamp`, `open`, `high`, `low`, `close`, `volume`

Output style:

- List of `DiamondEvent` objects.
- Events include expansion/contraction geometry, boundary lines, breakout metrics, score, and reference prices.

Example:

```python
from quant_bitcoin.patterns import DiamondConfig, detect_diamond_patterns

diamond_events = detect_diamond_patterns(
    candles,
    symbol="BTCUSDT",
    timeframe="4h",
    config=DiamondConfig(),
)
```

## Adam And Eve

Module: `quant_bitcoin.patterns.adam_and_eve`

Classes and enums:

- `AdamAndEveConfig`
- `AdamAndEveDirection`
- `AdamAndEveStatus`
- `AdamAndEveEvent`

Function:

- `detect_adam_and_eve_patterns(candles, symbol=None, timeframe=None, config=None)`

Required input columns:

- `timestamp`, `open`, `high`, `low`, `close`, `volume`

Output style:

- List of `AdamAndEveEvent` objects.
- Current implementation emits bullish completed breakout events only.
- Events include Adam low, neckline, Eve low, bottom similarity, sharpness/roundness metrics, breakout metrics, score, and reference prices.

Example:

```python
from quant_bitcoin.patterns import AdamAndEveConfig, detect_adam_and_eve_patterns

adam_eve_events = detect_adam_and_eve_patterns(
    candles,
    symbol="BTCUSDT",
    timeframe="4h",
    config=AdamAndEveConfig(),
)
```

# Error And Empty-Result Expectations

## Indicators

- Missing required columns raise `ValueError`.
- Invalid configuration values raise `ValueError` during config construction.
- Empty DataFrame input usually returns an empty DataFrame with output columns.
- Snapshot helpers return a dictionary with expected columns set to `None` when no rows exist.
- Warm-up periods usually produce invalid rows rather than exceptions when the input schema itself is valid.

## Patterns

- Missing required candle columns raise `ValueError`.
- Non-numeric OHLCV values raise `ValueError` through pandas numeric conversion.
- Unsorted timestamps raise `ValueError`.
- Too few candles or no qualifying structure returns an empty list.
- Required liquidity or spread filters require explicit pass/fail values; there is no internal liquidity or bid-ask spread module.

# Minimal End-To-End Analysis Sketch

```python
from quant_bitcoin.indicators import calculate_atr, calculate_volume_ratio, detect_pivots
from quant_bitcoin.patterns import detect_fair_value_gaps, detect_trendline_breaks

# candles is a completed-candle DataFrame sorted by timestamp.
atr_rows = calculate_atr(candles[["symbol", "timestamp", "high", "low", "close"]])
volume_rows = calculate_volume_ratio(candles[["symbol", "timestamp", "volume"]])
pivots = detect_pivots(candles[["symbol", "timestamp", "open", "high", "low", "close"]])

fvg_events = detect_fair_value_gaps(candles, symbol="BTCUSDT", timeframe="1h")
trendline_events = detect_trendline_breaks(candles, symbol="BTCUSDT", timeframe="1h")
```

The sketch shows separate indicator and pattern calls. It does not execute trades, size positions, submit orders, or persist events.
