# Trendline Break Pattern Mechanical Definition

## Purpose

Define a deterministic, implementation-ready specification for detecting a
Trendline Break Pattern from already-provided market data and previously defined
core indicator outputs.

This is a pattern definition only. It does not define order execution,
position sizing, exchange integration, live trading, backtesting engine changes,
machine learning, or UI visualization.

## Pattern Classification

- Pattern type: `TRENDLINE_BREAK_PATTERN`
- Category: Structure Break; Breakout / Breakdown; Trend Reversal or Trend
  Continuation
- Supported directions:
  - `BULLISH`: price breaks above a descending resistance trendline.
  - `BEARISH`: price breaks below an ascending support trendline.
  - `NONE`: no actionable trendline break is detected.

## Required Core Modules

The detector must consume outputs from these existing core modules and must not
recalculate their internal logic inside the pattern module:

- Pivot High / Pivot Low
- Swing Structure
- ATR
- Volume Ratio
- Support / Resistance Zone
- Liquidity: Trading Value / Volume
- Bid-Ask Spread

Optional strengthening input:

- Displacement Candle

## Required Inputs

For each evaluated candle, the pattern detector requires:

- OHLCV candles: `symbol`, `timestamp`, `open`, `high`, `low`, `close`,
  `volume`.
- Confirmed pivot highs from the Pivot High / Pivot Low module.
- Confirmed pivot lows from the Pivot High / Pivot Low module.
- Swing structure labels from the Swing Structure module.
- ATR value aligned to the evaluated candle.
- Volume ratio value aligned to the evaluated candle.
- Support / resistance zones available at the evaluated candle.
- Liquidity status aligned to the evaluated candle.
- Bid-ask spread status aligned to the evaluated candle.
- Optional displacement candle direction/status aligned to the evaluated candle.

Only pivots with `is_confirmed = true` may be used. Unconfirmed pivot candidates
must be ignored.

## Default Parameters

```yaml
trendline_break_pattern:
  minimum_touch_count: 2
  strong_touch_count: 3
  maximum_pivot_lookback: 50
  minimum_trendline_length: 10
  maximum_allowed_deviation_atr: 0.5
  atr_multiplier: 0.2
  volume_confirmation_threshold: 1.5
  weak_volume_confirmation_threshold: 1.3
  minimum_abs_slope_atr_per_candle: 0.02
  maximum_abs_slope_atr_per_candle: 2.0
  retest_lookahead_candles: 3
  invalidation_close_back_inside_atr: 0.0
  prefer_most_recent_trendline: true
```

Parameter meanings:

- `minimum_touch_count`: minimum confirmed pivot touches required to construct a
  candidate trendline.
- `strong_touch_count`: touch count at or above which the trendline receives a
  stronger quality score.
- `maximum_pivot_lookback`: maximum number of most recent same-type confirmed
  pivots to evaluate.
- `minimum_trendline_length`: minimum candle-index distance between the first
  and last anchor pivots.
- `maximum_allowed_deviation_atr`: maximum distance from the trendline for
  additional pivot touches, expressed in ATR units.
- `atr_multiplier`: ATR buffer required beyond the trendline for a valid break.
- `volume_confirmation_threshold`: default volume ratio required for full
  confirmation.
- `weak_volume_confirmation_threshold`: lower volume ratio that can classify the
  pattern as `WEAK` when all other checks pass.
- `minimum_abs_slope_atr_per_candle`: rejects nearly flat lines.
- `maximum_abs_slope_atr_per_candle`: rejects trendlines that are too steep.
- `retest_lookahead_candles`: optional post-break monitoring window for detecting
  immediate failure back inside the trendline.
- `invalidation_close_back_inside_atr`: close back inside the unbuffered
  trendline by more than this ATR amount marks an immediate failure.

## Trendline Construction

### Pivot Selection

Bullish trendline break candidates use confirmed pivot highs only:

```text
trendline_type = DESCENDING_RESISTANCE
anchor_source = confirmed pivot highs
required swing context = lower highs preferred
```

Bearish trendline break candidates use confirmed pivot lows only:

```text
trendline_type = ASCENDING_SUPPORT
anchor_source = confirmed pivot lows
required swing context = higher lows preferred
```

For each direction:

1. Select same-type confirmed pivots whose `confirmed_index` is less than or
   equal to the evaluated candle index.
2. Limit the candidate set to the most recent `maximum_pivot_lookback` pivots.
3. Ignore pivots that occur after the evaluated candle or are not confirmed by
   the evaluated candle.
4. Build candidate lines from ordered pivot pairs where the later anchor occurs
   after the earlier anchor.
5. Retain only candidate lines where the index distance between first and last
   anchor is at least `minimum_trendline_length`.

### Anchor Pair Rules

For a bullish break, the anchor pair must form a descending resistance line:

```text
second_pivot_high.price < first_pivot_high.price
trendline_slope < 0
```

For a bearish break, the anchor pair must form an ascending support line:

```text
second_pivot_low.price > first_pivot_low.price
trendline_slope > 0
```

### Trendline Formula

Use candle index as the x-axis and price as the y-axis.

For anchors `(x1, y1)` and `(x2, y2)`:

```text
trendline_slope = (y2 - y1) / (x2 - x1)
trendline_value(index) = y1 + trendline_slope * (index - x1)
```

At the evaluated candle:

```text
current_trendline_value = trendline_value(current_index)
```

### Touch Count

A pivot is a trendline touch when its price is close enough to the candidate
trendline value at that pivot's index.

For bullish resistance lines:

```text
pivot_touch = abs(pivot_high.price - trendline_value(pivot_high.index)) <= maximum_allowed_deviation_atr * ATR_at_pivot
```

For bearish support lines:

```text
pivot_touch = abs(pivot_low.price - trendline_value(pivot_low.index)) <= maximum_allowed_deviation_atr * ATR_at_pivot
```

If ATR is unavailable at a historical pivot, use the evaluated candle ATR only
for candidate scoring and classify the trendline as no better than `WEAK`.

A candidate trendline is eligible only when:

```text
touch_count >= minimum_touch_count
```

### Trendline Rejection Rules

Reject the candidate as `INVALID` when any of the following is true:

- Fewer than `minimum_touch_count` confirmed touches exist.
- Any anchor pivot is unconfirmed.
- `x2 <= x1`.
- `x2 - x1 < minimum_trendline_length`.
- Bullish candidate slope is not negative.
- Bearish candidate slope is not positive.
- Normalized absolute slope is below `minimum_abs_slope_atr_per_candle`.
- Normalized absolute slope is above `maximum_abs_slope_atr_per_candle`.
- Touch deviation exceeds `maximum_allowed_deviation_atr` for required touches.
- The line is built from only two weak touches and both touches have low pivot
  strength or conflicting swing labels.
- Liquidity or spread gating fails.

Normalized slope:

```text
normalized_abs_slope = abs(trendline_slope) / ATR_current
```

If `ATR_current <= 0` or missing, the pattern cannot be validated and must be
`INVALID`.

### Multiple Overlapping Trendlines

When multiple candidate lines pass construction rules:

1. Prefer the candidate with the largest `touch_count`.
2. If tied, prefer the candidate with the smallest average touch deviation.
3. If tied, prefer the candidate whose most recent anchor is closest to the
   evaluated candle.
4. If still tied and `prefer_most_recent_trendline = true`, choose the most
   recent candidate.

Only one selected trendline per direction should be emitted for a given symbol
and timestamp unless a future task explicitly defines multi-line output.

## Pre-Validation Filters

Before validating a break:

```text
liquidity_pass = true
spread_pass = true
```

If either check fails:

```text
pattern_status = INVALID
pattern_score = 0.0
reason = "liquidity_or_spread_filter_failed"
```

The pattern module must not fetch order-book data, calculate liquidity from raw
exchange data, or call exchange APIs. It must only consume already-provided
liquidity and spread outputs.

## Break Validation

### Bullish Trendline Break

A bullish break is validated when all required conditions are true:

```text
trendline_type = DESCENDING_RESISTANCE
close > trendline_value + atr_multiplier * ATR
volume_ratio >= weak_volume_confirmation_threshold
liquidity_pass = true
spread_pass = true
```

Full confirmation requires:

```text
close > trendline_value + atr_multiplier * ATR
volume_ratio >= volume_confirmation_threshold
```

Break metrics:

```text
break_price = close
break_distance = close - trendline_value
break_distance_atr = break_distance / ATR
```

### Bearish Trendline Break

A bearish break is validated when all required conditions are true:

```text
trendline_type = ASCENDING_SUPPORT
close < trendline_value - atr_multiplier * ATR
volume_ratio >= weak_volume_confirmation_threshold
liquidity_pass = true
spread_pass = true
```

Full confirmation requires:

```text
close < trendline_value - atr_multiplier * ATR
volume_ratio >= volume_confirmation_threshold
```

Break metrics:

```text
break_price = close
break_distance = trendline_value - close
break_distance_atr = break_distance / ATR
```

### Pending Break

A candidate is `PENDING` when a valid trendline exists and price is near the
trendline but has not closed beyond the ATR buffer.

Bullish pending condition:

```text
close > trendline_value
and close <= trendline_value + atr_multiplier * ATR
```

Bearish pending condition:

```text
close < trendline_value
and close >= trendline_value - atr_multiplier * ATR
```

### Weak Break

A candidate is `WEAK` when price passes the ATR buffer and all liquidity/spread
checks pass, but volume only reaches the weak confirmation threshold:

```text
weak_volume_confirmation_threshold <= volume_ratio < volume_confirmation_threshold
```

A candidate is also `WEAK` when the break is valid but the trendline has only
`minimum_touch_count` touches and no support/resistance context.

### Immediate Failure Back Inside

If post-break evaluation is available, a previously valid or weak break becomes
`INVALID` when price closes back inside the unbuffered trendline within
`retest_lookahead_candles`.

Bullish failure:

```text
future_close <= future_trendline_value - invalidation_close_back_inside_atr * ATR_future
```

Bearish failure:

```text
future_close >= future_trendline_value + invalidation_close_back_inside_atr * ATR_future
```

If future candles are unavailable, do not mark immediate failure; leave the
initial break status unchanged.

## Volume Confirmation

Use the Volume Ratio module output aligned to the evaluated candle.

```text
full_volume_confirmation = volume_ratio >= 1.5
weak_volume_confirmation = volume_ratio >= 1.3
```

Volume status impact:

- `volume_ratio >= 1.5`: eligible for `VALID`.
- `1.3 <= volume_ratio < 1.5`: eligible for `WEAK`.
- `volume_ratio < 1.3`: breakout or breakdown is `INVALID` unless it remains
  only a `PENDING` setup that has not broken the ATR buffer.
- Missing or invalid volume ratio: `INVALID` for completed breaks.

## Optional Displacement Candle Strengthening

When the Displacement Candle module output is available, it may improve score
but must not replace ATR and volume validation.

Bullish strong break:

```text
breakout candle is bullish displacement candle
```

Bearish strong break:

```text
breakdown candle is bearish displacement candle
```

If displacement output is unavailable, set `displacement_score = 0.0` and do not
penalize the required validation components.

## Swing Structure Alignment

Swing Structure labels are used as context, not as a replacement for trendline
construction.

Bullish trendline break alignment is strongest when recent pivot highs include
`LH` labels before the break and the break occurs after a downtrend or pullback
sequence.

Bearish trendline break alignment is strongest when recent pivot lows include
`HL` labels before the break and the break occurs after an uptrend or bounce
sequence.

Conflicting structure lowers score or invalidates weak lines:

- Bullish line with recent `HH` dominance receives reduced structure score.
- Bearish line with recent `LL` dominance receives reduced structure score.
- If the only valid trendline has two touches and structure conflicts, mark the
  candidate `INVALID`.

## Support / Resistance Context

Support / Resistance Zone output is used for target references and optional
context scoring.

Bullish break context is stronger when:

- The descending resistance trendline break occurs near or through a resistance
  zone.
- The nearest upper resistance zone provides a clear target reference.
- A broken resistance zone can act as a retest reference.

Bearish break context is stronger when:

- The ascending support trendline break occurs near or through a support zone.
- The nearest lower support zone provides a clear target reference.
- A broken support zone can act as a retest reference.

If zones are unavailable, the pattern may still be detected, but
`support_resistance_context_score = 0.0` and target reference must fall back to a
risk-reward based reference.

## Pattern Status Rules

Allowed statuses:

- `VALID`
- `WEAK`
- `INVALID`
- `PENDING`

Status assignment order:

1. If required inputs are missing or invalid, status is `INVALID`.
2. If `liquidity_pass = false` or `spread_pass = false`, status is `INVALID`.
3. If no eligible trendline exists, status is `INVALID` or `PENDING` only when
   there are enough pivots forming a near-eligible setup.
4. If a trendline exists but price has not crossed the unbuffered line, status is
   `PENDING`.
5. If price crosses the unbuffered line but not the ATR buffer, status is
   `PENDING`.
6. If price crosses the ATR buffer but volume ratio is below `1.3`, status is
   `INVALID`.
7. If price crosses the ATR buffer and `1.3 <= volume_ratio < 1.5`, status is
   `WEAK`.
8. If price crosses the ATR buffer and `volume_ratio >= 1.5`, status is `VALID`.
9. If immediate failure back inside is detected, status is `INVALID`.

## Pattern Scoring

The final `pattern_score` must be clipped to the range `0.0` to `1.0`.

Required components:

```text
pattern_score =
    0.25 * trendline_quality_score
  + 0.25 * breakout_strength_score
  + 0.20 * volume_confirmation_score
  + 0.15 * liquidity_score
  + 0.15 * structure_alignment_score
```

Optional implementation may reserve part of the structure component for
additional context:

```text
structure_alignment_score =
    0.60 * swing_structure_score
  + 0.25 * support_resistance_context_score
  + 0.15 * displacement_score
```

### Component Definitions

`trendline_quality_score`:

- `1.0`: at least `strong_touch_count` touches, acceptable slope, low average
  deviation.
- `0.7`: exactly `minimum_touch_count` touches, acceptable slope, acceptable
  deviation.
- `0.4`: eligible but weak historical ATR quality or marginal slope.
- `0.0`: rejected trendline.

`breakout_strength_score`:

```text
breakout_strength_score = min(break_distance_atr / 1.0, 1.0)
```

A break exactly at the default ATR buffer can be valid but should score lower
than a break with larger displacement beyond the trendline.

`volume_confirmation_score`:

- `1.0`: `volume_ratio >= 2.0`.
- `0.8`: `1.5 <= volume_ratio < 2.0`.
- `0.5`: `1.3 <= volume_ratio < 1.5`.
- `0.0`: `volume_ratio < 1.3` or invalid volume ratio.

`liquidity_score`:

- `1.0`: liquidity passes and spread status is tight or acceptable.
- `0.7`: liquidity passes and spread passes, but one status is only normal or
  acceptable rather than strong.
- `0.0`: liquidity fails or spread fails.

`structure_alignment_score`:

- `1.0`: swing labels strongly align with the expected lower-high or higher-low
  sequence.
- `0.7`: mixed but not conflicting structure.
- `0.3`: weak or sparse structure context.
- `0.0`: conflicting structure.

`support_resistance_context_score`:

- `1.0`: break interacts with a relevant zone and a clear target zone exists.
- `0.5`: relevant zone exists but target context is weak.
- `0.0`: no relevant zone context.

`displacement_score`:

- `1.0`: breakout/breakdown candle is a matching displacement candle.
- `0.0`: no matching displacement candle or displacement output unavailable.

Status-to-score constraints:

- `INVALID`: `pattern_score = 0.0`.
- `PENDING`: `pattern_score <= 0.49`.
- `WEAK`: `0.40 <= pattern_score <= 0.69`.
- `VALID`: `pattern_score >= 0.70` after clipping and constraints.

## Entry, Stop, and Target References

These are reference levels only. They must not trigger real order placement,
position sizing, or exchange calls.

### Bullish Break References

```text
entry_reference = breakout close or next candle open
stop_reference = nearest swing low or broken trendline retest zone
target_reference = nearest resistance zone or risk-reward based target
```

Mechanical selection:

1. `entry_reference`: use breakout candle close by default; optionally use next
   candle open if the consuming strategy requires confirmation.
2. `stop_reference`: choose the nearest confirmed swing low below the break
   price. If no swing low is available, use the broken trendline value or
   retest zone minus `atr_multiplier * ATR`.
3. `target_reference`: choose the nearest valid resistance zone above the break
   price. If unavailable, use `entry_reference + 2 * abs(entry_reference - stop_reference)`.

### Bearish Break References

```text
entry_reference = breakdown close or next candle open
stop_reference = nearest swing high or broken trendline retest zone
target_reference = nearest support zone or risk-reward based target
```

Mechanical selection:

1. `entry_reference`: use breakdown candle close by default; optionally use next
   candle open if the consuming strategy requires confirmation.
2. `stop_reference`: choose the nearest confirmed swing high above the break
   price. If no swing high is available, use the broken trendline value or
   retest zone plus `atr_multiplier * ATR`.
3. `target_reference`: choose the nearest valid support zone below the break
   price. If unavailable, use `entry_reference - 2 * abs(stop_reference - entry_reference)`.

## Output Schema

Each evaluation emits one pattern result per selected direction or a single
`NONE` result when no candidate exists.

```json
{
  "symbol": "BTCUSDT",
  "timestamp": "2026-05-17T10:00:00Z",
  "pattern_type": "TRENDLINE_BREAK_PATTERN",
  "direction": "BULLISH",
  "trendline_type": "DESCENDING_RESISTANCE",
  "trendline_slope": -42.5,
  "touch_count": 3,
  "break_price": 67500.0,
  "trendline_value": 67100.0,
  "break_distance": 400.0,
  "break_distance_atr": 0.8,
  "volume_ratio": 1.65,
  "liquidity_pass": true,
  "spread_pass": true,
  "pattern_score": 0.82,
  "pattern_status": "VALID",
  "entry_reference": 67500.0,
  "stop_reference": 66200.0,
  "target_reference": 70100.0,
  "reason": "bullish_break_confirmed_with_atr_buffer_and_volume"
}
```

Required fields:

- `symbol`
- `timestamp`
- `pattern_type`
- `direction`: `BULLISH`, `BEARISH`, or `NONE`
- `trendline_type`: `DESCENDING_RESISTANCE`, `ASCENDING_SUPPORT`, or `NONE`
- `trendline_slope`
- `touch_count`
- `break_price`
- `trendline_value`
- `break_distance`
- `break_distance_atr`
- `volume_ratio`
- `liquidity_pass`
- `spread_pass`
- `pattern_score`
- `pattern_status`: `VALID`, `WEAK`, `INVALID`, or `PENDING`
- `entry_reference`
- `stop_reference`
- `target_reference`
- `reason`

## Pseudocode-Level Logic

```text
for each evaluated candle:
    read OHLCV, ATR, volume ratio, liquidity status, spread status

    if liquidity_pass is false or spread_pass is false:
        emit INVALID with score 0.0
        stop evaluation for completed breaks

    bullish_line = build descending resistance from confirmed pivot highs
    bearish_line = build ascending support from confirmed pivot lows

    bullish_result = evaluate bullish break if bullish_line exists
    bearish_result = evaluate bearish break if bearish_line exists

    if both directions are valid at the same timestamp:
        choose the higher pattern_score
        if scores are tied, prefer the direction aligned with swing structure

    emit selected result
```

## Edge Case Handling

### Not Enough Pivot Points

If fewer than `minimum_touch_count` confirmed same-type pivots exist, no valid
trendline can be constructed. Emit `PENDING` only if one confirmed pivot exists
and future pivots could complete the setup; otherwise emit `INVALID` or `NONE`.

### Unconfirmed Pivots

Unconfirmed pivots must be ignored. A trendline built from any unconfirmed pivot
is invalid.

### Flat Trendline

If normalized absolute slope is below `minimum_abs_slope_atr_per_candle`, reject
the trendline as too flat. Flat horizontal support/resistance belongs to the
Support / Resistance Zone module, not this pattern.

### Too Steep Trendline

If normalized absolute slope is above `maximum_abs_slope_atr_per_candle`, reject
the trendline as unstable or overfit.

### Trendline With Only Two Weak Touches

A two-touch line is eligible only if slope, deviation, pivot strength, and swing
structure alignment pass. If any of these are weak or conflicting, mark the
candidate `INVALID`.

### Breakout Without ATR Buffer

A close through the unbuffered trendline but not beyond the ATR buffer is
`PENDING`, not `VALID`.

### Breakout Without Volume Confirmation

A completed break with `volume_ratio < 1.3` is `INVALID`. A completed break with
`1.3 <= volume_ratio < 1.5` is `WEAK`.

### Low Liquidity Market

If `liquidity_pass = false`, pattern status is `INVALID` regardless of price,
trendline quality, volume, or structure.

### Wide Spread Market

If `spread_pass = false`, pattern status is `INVALID` regardless of price,
trendline quality, volume, or structure.

### Price Immediately Returning Inside the Trendline

If post-break candles are available and price closes back inside the unbuffered
trendline within `retest_lookahead_candles`, invalidate the break. If future
candles are not available, do not use future information in backtests or live
simulation.

### Multiple Overlapping Trendlines

Select one trendline using touch count, average deviation, recency, and swing
alignment. Do not emit multiple overlapping trendlines unless a future task
explicitly changes the output contract.

### Conflicting Swing Structure

Conflicting swing structure reduces score. If the line has only two touches and
swing structure conflicts with the expected lower-high or higher-low setup,
reject the candidate.

## Non-Goals

This specification does not include:

- Actual trading execution.
- Exchange API integration.
- Position sizing implementation.
- Backtesting engine implementation.
- Live order placement.
- Machine learning models.
- UI visualization.
- Fetching candles, liquidity data, spread data, or order-book data.
