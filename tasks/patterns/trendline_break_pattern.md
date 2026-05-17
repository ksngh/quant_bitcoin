# Trendline Break Pattern Mechanical Definition

# Source Requirement

## Purpose

Define the Trendline Break Pattern mechanically.

This module detects when price breaks a valid trendline built from confirmed
pivot points.

This document defines detection logic only. It does not define order execution.

## Pattern Type

```text
TRENDLINE_BREAK
```

Human-readable name:

```text
Trendline Break Pattern
```

## Pattern Categories

```text
Structure Break
Breakout
Breakdown
Trend Reversal
Trend Continuation
```

## Supported Directions

```text
BULLISH
BEARISH
NONE
```

## Required Core Modules

```text
Liquidity: Trading Value / Volume
Bid-Ask Spread
Pivot High / Pivot Low
Swing Structure
ATR
Volume Ratio
Support / Resistance Zone
```

Optional:

```text
Displacement Candle
```

## Required Inputs

```text
symbol
timestamp
OHLCV candles
confirmed pivot highs
confirmed pivot lows
swing structure snapshots
ATR values
volume ratio values
support / resistance zones
liquidity snapshot
bid-ask spread snapshot
```

Optional:

```text
displacement candle snapshot
```

## Default Parameters

```yaml
trendline_break:
  minimum_touch_count: 2
  strong_touch_count: 3
  maximum_pivot_lookback: 50
  minimum_trendline_length: 10
  maximum_trendline_length: 200
  minimum_slope_abs: 0.0
  maximum_slope_abs: null
  maximum_allowed_touch_deviation_atr: 0.5
  breakout_atr_multiplier: 0.2
  minimum_volume_ratio: 1.5
  weak_volume_ratio: 1.3
  require_liquidity_pass: true
  require_spread_pass: true
  require_confirmed_pivots: true
  allow_displacement_bonus: true
  minimum_pattern_score: 0.7
```

## Core Definitions

### Bullish Trendline Break

A bullish trendline break occurs when price closes above a descending resistance
trendline.

Required structure:

```text
1. Use confirmed pivot highs.
2. Build descending trendline from pivot highs.
3. Current close breaks above the trendline.
4. Break distance is greater than ATR buffer.
5. Volume confirms the breakout.
```

Mechanical condition:

```text
trendline_type = DESCENDING_RESISTANCE
close > trendline_value + breakout_atr_multiplier * ATR
volume_ratio >= minimum_volume_ratio
```

### Bearish Trendline Break

A bearish trendline break occurs when price closes below an ascending support
trendline.

Required structure:

```text
1. Use confirmed pivot lows.
2. Build ascending trendline from pivot lows.
3. Current close breaks below the trendline.
4. Break distance is greater than ATR buffer.
5. Volume confirms the breakdown.
```

Mechanical condition:

```text
trendline_type = ASCENDING_SUPPORT
close < trendline_value - breakout_atr_multiplier * ATR
volume_ratio >= minimum_volume_ratio
```

## Trendline Source Pivots

### Bullish Break Source

Use pivot highs.

```text
pivot_type = PIVOT_HIGH
```

The selected pivot highs should generally form lower highs.

```text
latest_pivot_high.price <= previous_pivot_high.price
```

### Bearish Break Source

Use pivot lows.

```text
pivot_type = PIVOT_LOW
```

The selected pivot lows should generally form higher lows.

```text
latest_pivot_low.price >= previous_pivot_low.price
```

## Trendline Construction

### Method 1: Two-point Trendline

Use two confirmed pivots.

```text
point_1 = older pivot
point_2 = newer pivot
```

Trendline slope:

```text
slope = (point_2.price - point_1.price) / (point_2.index - point_1.index)
```

Trendline intercept:

```text
intercept = point_1.price - slope * point_1.index
```

Trendline value at index `i`:

```text
trendline_value[i] = slope * i + intercept
```

### Method 2: Multi-touch Regression Trendline

Use two or more confirmed pivots and fit a linear regression line.

```text
price = slope * index + intercept
```

Recommended for initial module:

```text
Use two-point trendline first.
Allow regression trendline later.
```

## Trendline Type

### Descending Resistance Trendline

```text
source_pivots = PIVOT_HIGH
slope < 0
```

Used for:

```text
BULLISH trendline break
```

### Ascending Support Trendline

```text
source_pivots = PIVOT_LOW
slope > 0
```

Used for:

```text
BEARISH trendline break
```

### Flat Trendline

```text
abs(slope) <= minimum_slope_abs
```

Default handling:

```text
trendline_status = INVALID
```

Flat horizontal zones should be handled by the Support / Resistance Zone module,
not this module.

## Touch Count

A pivot is considered a valid trendline touch when its price is close enough to
the trendline value.

```text
deviation = abs(pivot.price - trendline_value[pivot.index])
```

Valid touch:

```text
deviation <= maximum_allowed_touch_deviation_atr * ATR[pivot.index]
```

Valid trendline:

```text
touch_count >= minimum_touch_count
```

Strong trendline:

```text
touch_count >= strong_touch_count
```

## Trendline Length

Trendline length:

```text
trendline_length = latest_pivot.index - earliest_pivot.index
```

Valid length:

```text
minimum_trendline_length <= trendline_length <= maximum_trendline_length
```

## Break Distance

### Bullish Break Distance

```text
break_distance = close - trendline_value
```

Valid bullish break:

```text
break_distance > breakout_atr_multiplier * ATR
```

### Bearish Break Distance

```text
break_distance = trendline_value - close
```

Valid bearish break:

```text
break_distance > breakout_atr_multiplier * ATR
```

### Break Distance ATR

```text
break_distance_atr = break_distance / ATR
```

Example:

```text
break_distance = 120
ATR = 400
break_distance_atr = 0.3
```

## Volume Confirmation

Strong confirmation:

```text
volume_ratio >= minimum_volume_ratio
```

Weak confirmation:

```text
volume_ratio >= weak_volume_ratio
and
volume_ratio < minimum_volume_ratio
```

No confirmation:

```text
volume_ratio < weak_volume_ratio
```

## Liquidity Filter

If `require_liquidity_pass = true`:

```text
liquidity_pass must be true
```

If not:

```text
pattern_status = INVALID
```

## Spread Filter

If `require_spread_pass = true`:

```text
spread_pass must be true
```

If not:

```text
pattern_status = INVALID
```

## Optional Displacement Confirmation

A bullish break is stronger when:

```text
displacement_direction = BULLISH
displacement_status = VALID
```

A bearish break is stronger when:

```text
displacement_direction = BEARISH
displacement_status = VALID
```

If displacement is not present:

```text
Do not invalidate the pattern.
Only reduce or avoid bonus score.
```

## Pattern Status

Allowed values:

```text
VALID
WEAK
INVALID
PENDING
```

### VALID

```text
liquidity_pass = true
spread_pass = true
valid trendline exists
ATR break condition is satisfied
volume_ratio >= minimum_volume_ratio
pattern_score >= minimum_pattern_score
```

### WEAK

```text
valid trendline exists
ATR break condition is satisfied
volume_ratio >= weak_volume_ratio
volume_ratio < minimum_volume_ratio
```

or:

```text
pattern_score < minimum_pattern_score
but
pattern_score >= 0.5
```

### PENDING

```text
valid trendline exists
but close has not broken the trendline with ATR buffer
```

### INVALID

```text
liquidity filter fails
spread filter fails
not enough pivots
trendline is invalid
ATR is missing
volume ratio is missing
break condition fails
```

## Pattern Score

Score range:

```text
0.0 to 1.0
```

Recommended components:

```text
trendline_quality_score: 0.30
breakout_strength_score: 0.25
volume_confirmation_score: 0.20
liquidity_score: 0.10
structure_alignment_score: 0.10
displacement_score: 0.05
```

Total:

```text
pattern_score =
    trendline_quality_score * 0.30
  + breakout_strength_score * 0.25
  + volume_confirmation_score * 0.20
  + liquidity_score * 0.10
  + structure_alignment_score * 0.10
  + displacement_score * 0.05
```

### Trendline Quality Score

```text
if touch_count >= strong_touch_count:
    trendline_quality_score = 1.0

else if touch_count >= minimum_touch_count:
    trendline_quality_score = 0.7

else:
    trendline_quality_score = 0.0
```

Optional penalty:

```text
if trendline_length < minimum_trendline_length:
    trendline_quality_score = 0.0
```

### Breakout Strength Score

```text
if break_distance_atr >= 0.5:
    breakout_strength_score = 1.0

else if break_distance_atr >= 0.2:
    breakout_strength_score = 0.7

else:
    breakout_strength_score = 0.0
```

### Volume Confirmation Score

```text
if volume_ratio >= 2.0:
    volume_confirmation_score = 1.0

else if volume_ratio >= 1.5:
    volume_confirmation_score = 0.8

else if volume_ratio >= 1.3:
    volume_confirmation_score = 0.5

else:
    volume_confirmation_score = 0.0
```

### Liquidity Score

```text
if liquidity_status = HIGH:
    liquidity_score = 1.0

else if liquidity_status = NORMAL:
    liquidity_score = 0.8

else:
    liquidity_score = 0.0
```

### Structure Alignment Score

For bullish trendline break:

```text
if market_structure_status = DOWNTREND:
    structure_alignment_score = 1.0
```

Reason:

```text
A bullish break above descending resistance can indicate reversal or transition.
```

If market is range:

```text
structure_alignment_score = 0.6
```

For bearish trendline break:

```text
if market_structure_status = UPTREND:
    structure_alignment_score = 1.0
```

Reason:

```text
A bearish break below ascending support can indicate reversal or transition.
```

If market is range:

```text
structure_alignment_score = 0.6
```

### Displacement Score

```text
if breakout candle displacement direction matches pattern direction:
    displacement_score = 1.0

else:
    displacement_score = 0.0
```

## Reference Prices

This module must not execute orders. It only defines reference prices.

### Entry Reference

Bullish:

```text
entry_reference = breakout_close
```

Bearish:

```text
entry_reference = breakdown_close
```

Alternative for either direction:

```text
entry_reference = next_candle_open
```

### Stop Reference

Bullish default:

```text
stop_reference = nearest_recent_pivot_low
```

Bullish alternative:

```text
stop_reference = trendline_value - ATR
```

Bearish default:

```text
stop_reference = nearest_recent_pivot_high
```

Bearish alternative:

```text
stop_reference = trendline_value + ATR
```

### Target Reference

Bullish preferred:

```text
target_reference = nearest_resistance_zone
```

Bullish fallback:

```text
target_reference = entry_reference + 2 * abs(entry_reference - stop_reference)
```

Bearish preferred:

```text
target_reference = nearest_support_zone
```

Bearish fallback:

```text
target_reference = entry_reference - 2 * abs(stop_reference - entry_reference)
```

## Risk Reward

Bullish:

```text
risk = entry_reference - stop_reference
reward = target_reference - entry_reference
risk_reward = reward / risk
```

Bearish:

```text
risk = stop_reference - entry_reference
reward = entry_reference - target_reference
risk_reward = reward / risk
```

If:

```text
risk <= 0
```

Then:

```text
risk_reward = null
pattern_status = INVALID
```

## Output Schema

```json
{
  "symbol": "BTCUSDT",
  "timestamp": "2026-05-16T10:00:00Z",
  "pattern_type": "TRENDLINE_BREAK",
  "direction": "BULLISH",
  "pattern_status": "VALID",
  "trendline_type": "DESCENDING_RESISTANCE",
  "trendline_slope": -25.4,
  "trendline_intercept": 69000.0,
  "touch_count": 3,
  "source_pivot_indices": [120, 145, 171],
  "trendline_value": 64200.0,
  "break_price": 64500.0,
  "break_distance": 300.0,
  "break_distance_atr": 0.375,
  "atr": 800.0,
  "volume_ratio": 1.8,
  "liquidity_pass": true,
  "spread_pass": true,
  "displacement_confirmed": true,
  "pattern_score": 0.83,
  "entry_reference": 64500.0,
  "stop_reference": 63300.0,
  "target_reference": 66900.0,
  "risk_reward": 2.0,
  "reason": "Price closed above descending resistance trendline with ATR buffer and volume confirmation."
}
```

## Output Fields

- `pattern_type`: fixed value `TRENDLINE_BREAK`.
- `direction`: `BULLISH`, `BEARISH`, or `NONE`.
- `pattern_status`: `VALID`, `WEAK`, `INVALID`, or `PENDING`.
- `trendline_type`: `DESCENDING_RESISTANCE`, `ASCENDING_SUPPORT`, or
  `INVALID`.
- `trendline_slope`: slope of the detected trendline.
- `trendline_intercept`: intercept of the detected trendline.
- `touch_count`: number of valid pivot touches on the trendline.
- `source_pivot_indices`: pivot indices used to construct or validate the
  trendline.
- `trendline_value`: trendline price value at the breakout candle index.
- `break_price`: close price of the breakout or breakdown candle.
- `break_distance`: absolute distance between close and trendline value.
- `break_distance_atr`: break distance normalized by ATR.
- `atr`: ATR value at the breakout candle.
- `volume_ratio`: volume ratio at the breakout candle.
- `liquidity_pass`: result from Liquidity module.
- `spread_pass`: result from Bid-Ask Spread module.
- `displacement_confirmed`: true when the breakout candle is a valid
  displacement candle matching the pattern direction; false otherwise.
- `pattern_score`: final score between `0.0` and `1.0`.
- `entry_reference`: reference price for possible entry.
- `stop_reference`: reference price for invalidation.
- `target_reference`: reference price for possible target.
- `risk_reward`: reward-to-risk ratio.
- `reason`: short explanation for detection result.

## Edge Cases

### Not Enough Pivots

If fewer than `minimum_touch_count` pivots exist:

```text
pattern_status = INVALID
```

### Unconfirmed Pivots

If pivots are not confirmed:

```text
ignore pivots
```

### Flat Trendline

If trendline slope is too close to zero:

```text
pattern_status = INVALID
```

Use Support / Resistance Zone module instead.

### Too Steep Trendline

If `maximum_slope_abs` is configured and:

```text
abs(slope) > maximum_slope_abs
```

Then:

```text
pattern_status = INVALID
```

### ATR Missing

If ATR is missing:

```text
pattern_status = INVALID
```

### Volume Ratio Missing

If volume ratio is missing:

```text
pattern_status = INVALID
```

### Liquidity Failure

If liquidity fails:

```text
pattern_status = INVALID
```

### Spread Failure

If spread fails:

```text
pattern_status = INVALID
```

### Break Without ATR Buffer

If close crosses trendline but does not exceed ATR buffer:

```text
pattern_status = PENDING
```

### Break Without Volume

If ATR break is valid but volume is weak:

```text
pattern_status = WEAK
```

### Immediate Re-entry

If price breaks the trendline but returns inside the trendline within a short
window:

```text
mark as FALSE_BREAK_CANDIDATE
```

Optional parameter:

```yaml
false_break_check_window: 3
```

### Multiple Trendlines

If multiple valid trendlines exist:

```text
select the highest score trendline
```

Tie-breakers:

```text
1. higher touch_count
2. longer trendline_length
3. stronger volume_ratio
4. larger break_distance_atr
```

## Detection Logic

```text
1. Check liquidity_pass.
2. Check spread_pass.
3. Load confirmed pivot highs and lows.
4. Build descending resistance trendlines from pivot highs.
5. Build ascending support trendlines from pivot lows.
6. Calculate trendline value at current candle.
7. Check bullish break above descending resistance.
8. Check bearish break below ascending support.
9. Apply ATR buffer.
10. Apply volume confirmation.
11. Optionally apply displacement confirmation.
12. Calculate score.
13. Set pattern status.
14. Return best valid or pending signal.
```

## Pseudocode

```python
def detect_trendline_break(context, config):
    if config.require_liquidity_pass and not context.liquidity.liquidity_pass:
        return invalid_result("liquidity_failed")

    if config.require_spread_pass and not context.spread.spread_pass:
        return invalid_result("spread_failed")

    if context.atr is None:
        return invalid_result("missing_atr")

    if context.volume_ratio is None:
        return invalid_result("missing_volume_ratio")

    bullish_candidates = build_descending_resistance_trendlines(
        context.confirmed_pivot_highs,
        context.atr_series,
        config,
    )

    bearish_candidates = build_ascending_support_trendlines(
        context.confirmed_pivot_lows,
        context.atr_series,
        config,
    )

    candidates = []

    for trendline in bullish_candidates:
        result = evaluate_bullish_break(trendline, context, config)
        candidates.append(result)

    for trendline in bearish_candidates:
        result = evaluate_bearish_break(trendline, context, config)
        candidates.append(result)

    valid_candidates = [
        candidate for candidate in candidates
        if candidate["pattern_status"] in ["VALID", "WEAK", "PENDING"]
    ]

    if not valid_candidates:
        return invalid_result("no_valid_trendline_break")

    return select_best_candidate(valid_candidates)
```

### Bullish Break Evaluation

```python
def evaluate_bullish_break(trendline, context, config):
    current = context.current_candle
    trendline_value = trendline.value_at(current.index)
    break_distance = current.close - trendline_value
    break_distance_atr = break_distance / context.atr

    if break_distance <= 0:
        status = "PENDING"
    elif break_distance_atr < config.breakout_atr_multiplier:
        status = "PENDING"
    elif context.volume_ratio < config.weak_volume_ratio:
        status = "INVALID"
    elif context.volume_ratio < config.minimum_volume_ratio:
        status = "WEAK"
    else:
        status = "VALID"

    score = calculate_pattern_score(
        trendline=trendline,
        direction="BULLISH",
        break_distance_atr=break_distance_atr,
        volume_ratio=context.volume_ratio,
        liquidity=context.liquidity,
        structure=context.swing_structure,
        displacement=context.displacement,
        config=config,
    )

    return build_output(
        context=context,
        trendline=trendline,
        direction="BULLISH",
        status=status,
        break_distance=break_distance,
        break_distance_atr=break_distance_atr,
        score=score,
    )
```

### Bearish Break Evaluation

```python
def evaluate_bearish_break(trendline, context, config):
    current = context.current_candle
    trendline_value = trendline.value_at(current.index)
    break_distance = trendline_value - current.close
    break_distance_atr = break_distance / context.atr

    if break_distance <= 0:
        status = "PENDING"
    elif break_distance_atr < config.breakout_atr_multiplier:
        status = "PENDING"
    elif context.volume_ratio < config.weak_volume_ratio:
        status = "INVALID"
    elif context.volume_ratio < config.minimum_volume_ratio:
        status = "WEAK"
    else:
        status = "VALID"

    score = calculate_pattern_score(
        trendline=trendline,
        direction="BEARISH",
        break_distance_atr=break_distance_atr,
        volume_ratio=context.volume_ratio,
        liquidity=context.liquidity,
        structure=context.swing_structure,
        displacement=context.displacement,
        config=config,
    )

    return build_output(
        context=context,
        trendline=trendline,
        direction="BEARISH",
        status=status,
        break_distance=break_distance,
        break_distance_atr=break_distance_atr,
        score=score,
    )
```

## Domain Model Example

Java-style example supplied by the owner:

```java
public enum TrendlineBreakDirection {
    BULLISH,
    BEARISH,
    NONE
}
```

```java
public enum TrendlineType {
    DESCENDING_RESISTANCE,
    ASCENDING_SUPPORT,
    INVALID
}
```

```java
public enum PatternStatus {
    VALID,
    WEAK,
    INVALID,
    PENDING
}
```

```java
public record TrendlineBreakSignal(
    String symbol,
    Instant timestamp,
    String patternType,
    TrendlineBreakDirection direction,
    PatternStatus patternStatus,
    TrendlineType trendlineType,
    BigDecimal trendlineSlope,
    BigDecimal trendlineIntercept,
    int touchCount,
    List<Integer> sourcePivotIndices,
    BigDecimal trendlineValue,
    BigDecimal breakPrice,
    BigDecimal breakDistance,
    BigDecimal breakDistanceAtr,
    BigDecimal atr,
    BigDecimal volumeRatio,
    boolean liquidityPass,
    boolean spreadPass,
    boolean displacementConfirmed,
    BigDecimal patternScore,
    BigDecimal entryReference,
    BigDecimal stopReference,
    BigDecimal targetReference,
    BigDecimal riskReward,
    String reason
) {
}
```

## Final Mechanical Rule

Bullish Trendline Break:

```text
1. Build descending resistance trendline from confirmed pivot highs.
2. Require touch_count >= 2.
3. Require slope < 0.
4. Calculate trendline_value at current candle.
5. Require close > trendline_value + 0.2 * ATR.
6. Require volume_ratio >= 1.5.
7. Require liquidity_pass = true.
8. Require spread_pass = true.
```

Bearish Trendline Break:

```text
1. Build ascending support trendline from confirmed pivot lows.
2. Require touch_count >= 2.
3. Require slope > 0.
4. Calculate trendline_value at current candle.
5. Require close < trendline_value - 0.2 * ATR.
6. Require volume_ratio >= 1.5.
7. Require liquidity_pass = true.
8. Require spread_pass = true.
```

# Implementation Notes

- This document is a mechanical pattern definition only.
- Do not implement Trendline Break Pattern code from this document unless a later
  explicit implementation task is assigned.
- The pattern may consume previously computed Liquidity, Bid-Ask Spread, Pivot,
  Swing Structure, ATR, Volume Ratio, Support / Resistance Zone, and optional
  Displacement Candle outputs.
- The pattern must not execute orders, call exchange order APIs, read secrets, or
  introduce live trading behavior.
- Future implementation work should create a dedicated task document with
  deterministic tests for bullish, bearish, weak, pending, invalid, missing ATR,
  missing volume ratio, liquidity failure, spread failure, and multiple-trendline
  tie-breaker scenarios.
