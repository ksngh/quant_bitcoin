# Cup and Handle Pattern Mechanical Definition

## Purpose

Define the Cup and Handle Pattern mechanically.

This module detects a bullish continuation pattern formed by a rounded cup, a shallow handle pullback, and a breakout above the neckline.

This document defines detection logic only.
It does not define order execution.

## Pattern Type

```text
Cup and Handle Pattern
```

## Pattern Categories

```text
Continuation Pattern
Bullish Breakout Pattern
Rounded Base Pattern
Accumulation Pattern
```

## Supported Directions

```text
BULLISH
NONE
```

Optional future extension:

```text
BEARISH_INVERTED
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
displacement candle snapshots
```

## Default Parameters

```yaml
minimum_cup_duration: 20
maximum_cup_duration: 200
minimum_handle_duration: 3
maximum_handle_duration: 40
maximum_rim_difference_rate: 0.05
minimum_cup_depth_rate: 0.10
maximum_cup_depth_rate: 0.40
maximum_handle_depth_ratio: 0.35
minimum_bottom_zone_duration: 3
bottom_zone_atr_multiplier: 0.5
breakout_atr_multiplier: 0.2
minimum_breakout_volume_ratio: 1.5
weak_breakout_volume_ratio: 1.3
require_prior_uptrend: true
require_liquidity_pass: true
require_spread_pass: true
require_displacement_breakout: false
minimum_pattern_score: 0.7
```

## Core Structure

A bullish Cup and Handle Pattern consists of:

```text
prior uptrend
left rim
cup bottom
right rim
handle low
neckline
breakout
```

Required index order:

```text
left_rim.index < cup_bottom.index < right_rim.index < handle_low.index < breakout.index
```

## Prior Uptrend Definition

If `require_prior_uptrend = true`, the pattern requires bullish structure before the left rim.

Valid prior uptrend:

```text
market_structure_status = UPTREND
```

or:

```text
recent swing labels contain HH and HL
```

Optional stricter rule:

```text
at least one HH and one HL exist before left_rim.index
```

If prior uptrend is required but not found:

```text
pattern_status = INVALID
```

## Pivot Roles

### Left Rim

The left rim is a confirmed pivot high.

```text
left_rim.pivot_type = PIVOT_HIGH
```

### Cup Bottom

The cup bottom is a confirmed pivot low after the left rim.

```text
cup_bottom.pivot_type = PIVOT_LOW
left_rim.index < cup_bottom.index
```

### Right Rim

The right rim is a confirmed pivot high after the cup bottom.

```text
right_rim.pivot_type = PIVOT_HIGH
cup_bottom.index < right_rim.index
```

### Handle Low

The handle low is a confirmed pivot low after the right rim.

```text
handle_low.pivot_type = PIVOT_LOW
right_rim.index < handle_low.index
```

### Breakout

The breakout is the candle that closes above the neckline with ATR buffer.

```text
breakout.index > handle_low.index
```

## Rim Similarity

Left rim and right rim must be near the same price level.

```text
rim_difference = abs(left_rim.price - right_rim.price)
rim_difference_rate = rim_difference / left_rim.price
```

Valid rim similarity:

```text
rim_difference_rate <= maximum_rim_difference_rate
```

Default:

```text
maximum_rim_difference_rate = 0.05
```

If rim prices are too different:

```text
pattern_status = INVALID
```

## Neckline Definition

Recommended initial version:

```text
neckline = max(left_rim.price, right_rim.price)
```

Alternative:

```text
neckline = resistance_zone.center_price
```

Use resistance zone only when a valid resistance zone overlaps the rim area.

Rim zone match:

```text
left_rim.price is inside resistance zone
or
right_rim.price is inside resistance zone
```

Default:

```text
use neckline = max(left_rim.price, right_rim.price)
```

## Cup Depth

```text
cup_reference_price = min(left_rim.price, right_rim.price)
cup_depth = cup_reference_price - cup_bottom.price
cup_depth_rate = cup_depth / cup_reference_price
```

Valid cup depth:

```text
minimum_cup_depth_rate <= cup_depth_rate <= maximum_cup_depth_rate
```

Default:

```text
minimum_cup_depth_rate = 0.10
maximum_cup_depth_rate = 0.40
```

If cup is too shallow:

```text
pattern_status = INVALID
```

If cup is too deep:

```text
pattern_status = INVALID
```

## Cup Duration

```text
cup_duration = right_rim.index - left_rim.index
```

Valid cup duration:

```text
minimum_cup_duration <= cup_duration <= maximum_cup_duration
```

Default:

```text
minimum_cup_duration = 20
maximum_cup_duration = 200
```

If cup duration is outside valid range:

```text
pattern_status = INVALID
```

## Cup Roundness

The cup should not be a sharp V-shaped recovery.

Use the following mechanical checks:

```text
bottom_zone_duration
left_decline_duration
right_recovery_duration
slope_balance
bottom_stability
```

## Bottom Zone

Define a bottom zone around `cup_bottom.price`.

```text
bottom_zone_low = cup_bottom.price - bottom_zone_atr_multiplier * ATR
bottom_zone_high = cup_bottom.price + bottom_zone_atr_multiplier * ATR
```

Default:

```text
bottom_zone_atr_multiplier = 0.5
```

A candle is inside the bottom zone when:

```text
bottom_zone_low <= candle.low
and
candle.high <= bottom_zone_high
```

Bottom zone duration:

```text
bottom_zone_duration = number of candles near cup_bottom inside bottom zone
```

Valid rounded bottom:

```text
bottom_zone_duration >= minimum_bottom_zone_duration
```

Default:

```text
minimum_bottom_zone_duration = 3
```

If bottom zone duration is too short:

```text
cup_shape_status = V_SHAPED
pattern_status = INVALID or WEAK
```

Recommended initial handling:

```text
V_SHAPED = INVALID
```

## Left Decline Duration

```text
left_decline_duration = cup_bottom.index - left_rim.index
```

## Right Recovery Duration

```text
right_recovery_duration = right_rim.index - cup_bottom.index
```

## Slope Balance

```text
duration_ratio = min(left_decline_duration, right_recovery_duration) / max(left_decline_duration, right_recovery_duration)
```

Valid slope balance:

```text
duration_ratio >= minimum_slope_balance_ratio
```

Recommended default:

```yaml
minimum_slope_balance_ratio: 0.3
```

If one side is too short:

```text
cup_shape_status = UNBALANCED
```

Recommended initial handling:

```text
UNBALANCED = WEAK
```

## Handle Definition

The handle is a shallow pullback after the right rim and before breakout.

Required order:

```text
right_rim.index < handle_low.index < breakout.index
```

Handle depth:

```text
handle_depth = right_rim.price - handle_low.price
```

Handle depth ratio:

```text
handle_depth_ratio = handle_depth / cup_depth
```

Valid handle depth:

```text
handle_depth_ratio <= maximum_handle_depth_ratio
```

Default:

```text
maximum_handle_depth_ratio = 0.35
```

If handle is too deep:

```text
pattern_status = INVALID
```

## Handle Duration

```text
handle_duration = breakout.index - right_rim.index
```

Valid handle duration:

```text
minimum_handle_duration <= handle_duration <= maximum_handle_duration
```

Default:

```text
minimum_handle_duration = 3
maximum_handle_duration = 40
```

If handle duration is outside valid range:

```text
pattern_status = INVALID
```

## Handle Position

The handle should form in the upper part of the cup.

Handle low must not fall below the midpoint of the cup.

```text
cup_midpoint = cup_bottom.price + cup_depth * 0.5
```

Valid handle position:

```text
handle_low.price >= cup_midpoint
```

If handle low is below cup midpoint:

```text
pattern_status = INVALID
```

## Breakout Definition

A bullish breakout occurs when price closes above the neckline with ATR buffer.

```text
breakout_close > neckline + breakout_atr_multiplier * ATR
```

Default:

```text
breakout_atr_multiplier = 0.2
```

Breakout distance:

```text
breakout_distance = breakout_close - neckline
breakout_distance_atr = breakout_distance / ATR
```

If close is above neckline but does not exceed ATR buffer:

```text
pattern_status = PENDING
```

## Volume Confirmation

Breakout candle must satisfy:

```text
volume_ratio >= minimum_breakout_volume_ratio
```

Default:

```text
minimum_breakout_volume_ratio = 1.5
```

Weak volume confirmation:

```text
weak_breakout_volume_ratio <= volume_ratio < minimum_breakout_volume_ratio
```

Default:

```text
weak_breakout_volume_ratio = 1.3
```

If volume ratio is weak:

```text
pattern_status = WEAK
```

If volume ratio is below weak threshold:

```text
pattern_status = INVALID
```

## Optional Displacement Breakout

If `require_displacement_breakout = true`, breakout candle must satisfy:

```text
displacement_direction = BULLISH
displacement_status = VALID
```

If not satisfied:

```text
pattern_status = INVALID
```

If `require_displacement_breakout = false`:

```text
displacement_confirmed = false
```

but the pattern can still be valid.

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

## Pattern Status

Allowed values:

```text
VALID
WEAK
INVALID
PENDING
```

## VALID

```text
liquidity_pass = true
spread_pass = true
prior uptrend condition is satisfied
left rim exists
cup bottom exists
right rim exists
handle low exists
rim similarity is valid
cup depth is valid
cup duration is valid
cup is not V-shaped
handle depth is valid
handle duration is valid
handle position is valid
breakout exceeds ATR buffer
volume_ratio >= minimum_breakout_volume_ratio
pattern_score >= minimum_pattern_score
```

## WEAK

```text
core structure exists
but one or more non-critical quality conditions are weak
```

Examples:

```text
volume_ratio is between weak threshold and strong threshold
cup shape is unbalanced
pattern_score >= 0.5 and pattern_score < minimum_pattern_score
```

## PENDING

```text
cup and handle structure exists
but breakout has not occurred yet
```

or:

```text
close is above neckline but does not exceed ATR buffer
```

## INVALID

```text
liquidity filter fails
spread filter fails
prior uptrend missing
not enough pivots
rim similarity invalid
cup depth invalid
cup duration invalid
V-shaped cup
handle missing
handle too deep
handle duration invalid
handle below cup midpoint
breakout volume missing
breakout volume too low
```

## Pattern Score

Score range:

```text
0.0 to 1.0
```

Recommended components:

```text
prior_trend_score: 0.15
cup_shape_score: 0.20
rim_similarity_score: 0.15
handle_quality_score: 0.15
breakout_strength_score: 0.15
volume_confirmation_score: 0.10
liquidity_score: 0.10
```

Formula:

```text
pattern_score =
    prior_trend_score * 0.15
  + cup_shape_score * 0.20
  + rim_similarity_score * 0.15
  + handle_quality_score * 0.15
  + breakout_strength_score * 0.15
  + volume_confirmation_score * 0.10
  + liquidity_score * 0.10
```

## Prior Trend Score

```text
if market_structure_status = UPTREND:
    prior_trend_score = 1.0

else if recent swing labels contain HH and HL:
    prior_trend_score = 0.8

else:
    prior_trend_score = 0.0
```

## Cup Shape Score

```text
if bottom_zone_duration >= minimum_bottom_zone_duration
and duration_ratio >= 0.5:
    cup_shape_score = 1.0

else if bottom_zone_duration >= minimum_bottom_zone_duration
and duration_ratio >= 0.3:
    cup_shape_score = 0.7

else:
    cup_shape_score = 0.0
```

## Rim Similarity Score

```text
if rim_difference_rate <= 0.02:
    rim_similarity_score = 1.0

else if rim_difference_rate <= 0.05:
    rim_similarity_score = 0.7

else:
    rim_similarity_score = 0.0
```

## Handle Quality Score

```text
if handle_depth_ratio <= 0.25
and handle_low.price >= cup_midpoint:
    handle_quality_score = 1.0

else if handle_depth_ratio <= 0.35
and handle_low.price >= cup_midpoint:
    handle_quality_score = 0.7

else:
    handle_quality_score = 0.0
```

## Breakout Strength Score

```text
if breakout_distance_atr >= 0.5:
    breakout_strength_score = 1.0

else if breakout_distance_atr >= 0.2:
    breakout_strength_score = 0.7

else:
    breakout_strength_score = 0.0
```

## Volume Confirmation Score

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

## Liquidity Score

```text
if liquidity_status = HIGH:
    liquidity_score = 1.0

else if liquidity_status = NORMAL:
    liquidity_score = 0.8

else:
    liquidity_score = 0.0
```

## Entry Reference

This module must not execute orders.

It only defines reference prices.

Recommended:

```text
entry_reference = breakout_close
```

Alternative:

```text
entry_reference = next_candle_open
```

Retest-based alternative:

```text
entry_reference = neckline retest area
```

## Stop Reference

Recommended:

```text
stop_reference = handle_low.price - breakout_atr_multiplier * ATR
```

Alternative:

```text
stop_reference = neckline - ATR
```

Invalid if:

```text
stop_reference >= entry_reference
```

## Target Reference

Classic measured move target:

```text
target_reference = neckline + cup_depth
```

Risk-reward fallback:

```text
target_reference = entry_reference + 2 * abs(entry_reference - stop_reference)
```

If both exist, preferred target:

```text
target_reference = min(classic_target, nearest_resistance_zone)
```

If no resistance zone exists:

```text
target_reference = classic_target
```

## Risk Reward

```text
risk = entry_reference - stop_reference
reward = target_reference - entry_reference
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
  "pattern_type": "CUP_AND_HANDLE",
  "direction": "BULLISH",
  "pattern_status": "VALID",
  "left_rim_index": 100,
  "cup_bottom_index": 135,
  "right_rim_index": 170,
  "handle_low_index": 182,
  "breakout_index": 190,
  "left_rim_price": 65000.0,
  "cup_bottom_price": 56000.0,
  "right_rim_price": 64800.0,
  "handle_low_price": 62000.0,
  "neckline": 65000.0,
  "cup_depth": 8800.0,
  "cup_depth_rate": 0.1354,
  "cup_duration": 70,
  "bottom_zone_duration": 5,
  "duration_ratio": 0.92,
  "handle_depth": 2800.0,
  "handle_depth_ratio": 0.3182,
  "handle_duration": 20,
  "breakout_price": 65400.0,
  "breakout_distance": 400.0,
  "breakout_distance_atr": 0.5,
  "volume_ratio": 1.8,
  "liquidity_pass": true,
  "spread_pass": true,
  "displacement_confirmed": false,
  "pattern_score": 0.84,
  "entry_reference": 65400.0,
  "stop_reference": 61840.0,
  "target_reference": 73800.0,
  "risk_reward": 2.36,
  "reason": "Bullish Cup and Handle detected with valid rim similarity, rounded cup, shallow handle, and volume-confirmed breakout."
}
```

## Output Fields

### pattern_type

Fixed value:

```text
CUP_AND_HANDLE
```

### direction

One of:

```text
BULLISH
NONE
```

### pattern_status

One of:

```text
VALID
WEAK
INVALID
PENDING
```

### left_rim_index

Index of the left rim pivot high.

### cup_bottom_index

Index of the cup bottom pivot low.

### right_rim_index

Index of the right rim pivot high.

### handle_low_index

Index of the handle low pivot.

### breakout_index

Index of the breakout candle.

### left_rim_price

Price of the left rim pivot high.

### cup_bottom_price

Price of the cup bottom pivot low.

### right_rim_price

Price of the right rim pivot high.

### handle_low_price

Price of the handle low pivot.

### neckline

Breakout reference level.

### cup_depth

Distance between cup reference price and cup bottom.

### cup_depth_rate

Cup depth normalized by rim price.

### cup_duration

Number of candles between left rim and right rim.

### bottom_zone_duration

Number of candles near cup bottom zone.

### duration_ratio

Balance between left decline duration and right recovery duration.

### handle_depth

Distance between right rim and handle low.

### handle_depth_ratio

Handle depth divided by cup depth.

### handle_duration

Number of candles between right rim and breakout.

### breakout_price

Close price of breakout candle.

### breakout_distance

Distance between breakout close and neckline.

### breakout_distance_atr

Breakout distance normalized by ATR.

### volume_ratio

Volume ratio of breakout candle.

### liquidity_pass

Result from Liquidity module.

### spread_pass

Result from Bid-Ask Spread module.

### displacement_confirmed

Boolean value.

```text
true = breakout candle is bullish displacement candle
false = breakout candle is not bullish displacement candle
```

### pattern_score

Final score between `0.0` and `1.0`.

### entry_reference

Reference price for possible entry.

### stop_reference

Reference price for invalidation.

### target_reference

Reference price for possible target.

### risk_reward

Reward-to-risk ratio.

### reason

Short explanation for detection result.

## Edge Cases

### No prior uptrend

If `require_prior_uptrend = true` and prior uptrend is missing:

```text
pattern_status = INVALID
```

### Not enough pivots

If valid left rim, cup bottom, right rim, and handle low cannot be found:

```text
pattern_status = INVALID
```

### Rim prices too different

If:

```text
rim_difference_rate > maximum_rim_difference_rate
```

Then:

```text
pattern_status = INVALID
```

### Cup too shallow

If:

```text
cup_depth_rate < minimum_cup_depth_rate
```

Then:

```text
pattern_status = INVALID
```

### Cup too deep

If:

```text
cup_depth_rate > maximum_cup_depth_rate
```

Then:

```text
pattern_status = INVALID
```

### Cup duration invalid

If:

```text
cup_duration < minimum_cup_duration
or
cup_duration > maximum_cup_duration
```

Then:

```text
pattern_status = INVALID
```

### V-shaped cup

If:

```text
bottom_zone_duration < minimum_bottom_zone_duration
```

Then:

```text
pattern_status = INVALID
```

### Handle missing

If no valid handle low exists after right rim:

```text
pattern_status = PENDING
```

### Handle too deep

If:

```text
handle_depth_ratio > maximum_handle_depth_ratio
```

Then:

```text
pattern_status = INVALID
```

### Handle below cup midpoint

If:

```text
handle_low.price < cup_midpoint
```

Then:

```text
pattern_status = INVALID
```

### Breakout missing

If price has not broken neckline:

```text
pattern_status = PENDING
```

### Breakout without ATR buffer

If:

```text
close > neckline
and
close <= neckline + breakout_atr_multiplier * ATR
```

Then:

```text
pattern_status = PENDING
```

### Breakout volume weak

If:

```text
weak_breakout_volume_ratio <= volume_ratio < minimum_breakout_volume_ratio
```

Then:

```text
pattern_status = WEAK
```

### Breakout volume too low

If:

```text
volume_ratio < weak_breakout_volume_ratio
```

Then:

```text
pattern_status = INVALID
```

### Low liquidity

If liquidity fails:

```text
pattern_status = INVALID
```

### Wide spread

If spread fails:

```text
pattern_status = INVALID
```

### Multiple candidate cups

If multiple candidates exist:

```text
select highest pattern_score
```

Tie-breakers:

```text
1. stronger volume_ratio
2. better rim similarity
3. better handle quality
4. more balanced cup duration
5. more recent breakout
```

## Detection Logic

```text
1. Check liquidity_pass.
2. Check spread_pass.
3. Load confirmed pivot highs and pivot lows.
4. Find prior uptrend context.
5. Search pivot sequence: left_rim -> cup_bottom -> right_rim.
6. Validate rim similarity.
7. Validate cup depth.
8. Validate cup duration.
9. Validate cup roundness.
10. Search handle low after right rim.
11. Validate handle depth.
12. Validate handle duration.
13. Validate handle position.
14. Define neckline.
15. Search breakout candle after handle.
16. Apply ATR breakout buffer.
17. Apply volume confirmation.
18. Optionally check displacement breakout.
19. Calculate score.
20. Set pattern status.
21. Return best valid, weak, or pending signal.
```

## Pseudocode

```python
def detect_cup_and_handle(context, config):
    if config.require_liquidity_pass and not context.liquidity.liquidity_pass:
        return invalid_result("liquidity_failed")

    if config.require_spread_pass and not context.spread.spread_pass:
        return invalid_result("spread_failed")

    candidates = []

    pivot_highs = context.confirmed_pivot_highs
    pivot_lows = context.confirmed_pivot_lows

    for left_rim in pivot_highs:
        if config.require_prior_uptrend:
            if not has_prior_uptrend(left_rim, context.swing_structure, config):
                continue

        possible_bottoms = [
            pivot for pivot in pivot_lows
            if pivot.index > left_rim.index
        ]

        for cup_bottom in possible_bottoms:
            possible_right_rims = [
                pivot for pivot in pivot_highs
                if pivot.index > cup_bottom.index
            ]

            for right_rim in possible_right_rims:
                cup = build_cup_candidate(
                    left_rim,
                    cup_bottom,
                    right_rim,
                    context,
                    config
                )

                if not validate_cup(cup, context, config):
                    continue

                handle_candidates = find_handle_candidates(
                    right_rim,
                    cup,
                    context,
                    config
                )

                for handle_low in handle_candidates:
                    pattern = build_pattern_candidate(
                        cup,
                        handle_low,
                        context,
                        config
                    )

                    evaluated = evaluate_cup_and_handle(
                        pattern,
                        context,
                        config
                    )

                    if evaluated["pattern_status"] in ["VALID", "WEAK", "PENDING"]:
                        candidates.append(evaluated)

    if not candidates:
        return invalid_result("no_valid_cup_and_handle")

    return select_best_candidate(candidates)
```

## Cup Validation

```python
def validate_cup(cup, context, config):
    if cup.rim_difference_rate > config.maximum_rim_difference_rate:
        return False

    if cup.cup_depth_rate < config.minimum_cup_depth_rate:
        return False

    if cup.cup_depth_rate > config.maximum_cup_depth_rate:
        return False

    if cup.cup_duration < config.minimum_cup_duration:
        return False

    if cup.cup_duration > config.maximum_cup_duration:
        return False

    if cup.bottom_zone_duration < config.minimum_bottom_zone_duration:
        return False

    return True
```

## Handle Validation

```python
def validate_handle(pattern, context, config):
    if pattern.handle_depth_ratio > config.maximum_handle_depth_ratio:
        return False

    if pattern.handle_duration < config.minimum_handle_duration:
        return False

    if pattern.handle_duration > config.maximum_handle_duration:
        return False

    if pattern.handle_low_price < pattern.cup_midpoint:
        return False

    return True
```

## Breakout Evaluation

```python
def evaluate_breakout(pattern, context, config):
    breakout_candles = context.candles_after(pattern.handle_low_index)

    for candle in breakout_candles:
        atr = context.atr_at(candle.index)
        volume_ratio = context.volume_ratio_at(candle.index)

        if atr is None or volume_ratio is None:
            continue

        breakout_threshold = pattern.neckline + config.breakout_atr_multiplier * atr

        if candle.close > breakout_threshold:
            pattern.breakout_index = candle.index
            pattern.breakout_price = candle.close
            pattern.breakout_distance = candle.close - pattern.neckline
            pattern.breakout_distance_atr = pattern.breakout_distance / atr
            pattern.volume_ratio = volume_ratio
            return pattern

    pattern.pattern_status = "PENDING"
    return pattern
```

## Java-style Domain Model Example

```java
public enum CupAndHandleDirection {
    BULLISH,
    NONE
}
```

```java
public enum CupAndHandleStatus {
    VALID,
    WEAK,
    INVALID,
    PENDING
}
```

```java
public record CupAndHandleSignal(
    String symbol,
    Instant timestamp,
    String patternType,
    CupAndHandleDirection direction,
    CupAndHandleStatus patternStatus,
    int leftRimIndex,
    int cupBottomIndex,
    int rightRimIndex,
    int handleLowIndex,
    int breakoutIndex,
    BigDecimal leftRimPrice,
    BigDecimal cupBottomPrice,
    BigDecimal rightRimPrice,
    BigDecimal handleLowPrice,
    BigDecimal neckline,
    BigDecimal cupDepth,
    BigDecimal cupDepthRate,
    int cupDuration,
    int bottomZoneDuration,
    BigDecimal durationRatio,
    BigDecimal handleDepth,
    BigDecimal handleDepthRatio,
    int handleDuration,
    BigDecimal breakoutPrice,
    BigDecimal breakoutDistance,
    BigDecimal breakoutDistanceAtr,
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

## Recommended Initial Configuration

```yaml
cup_and_handle:
  minimum_cup_duration: 20
  maximum_cup_duration: 200
  minimum_handle_duration: 3
  maximum_handle_duration: 40
  maximum_rim_difference_rate: 0.05
  minimum_cup_depth_rate: 0.10
  maximum_cup_depth_rate: 0.40
  maximum_handle_depth_ratio: 0.35
  minimum_bottom_zone_duration: 3
  bottom_zone_atr_multiplier: 0.5
  minimum_slope_balance_ratio: 0.3
  breakout_atr_multiplier: 0.2
  minimum_breakout_volume_ratio: 1.5
  weak_breakout_volume_ratio: 1.3
  require_prior_uptrend: true
  require_liquidity_pass: true
  require_spread_pass: true
  require_displacement_breakout: false
  minimum_pattern_score: 0.7
```

## Final Mechanical Rule

```text
Bullish Cup and Handle:
1. Require prior uptrend.
2. Find left_rim as pivot high.
3. Find cup_bottom as pivot low after left_rim.
4. Find right_rim as pivot high after cup_bottom.
5. Require rim_difference_rate <= 0.05.
6. Require 0.10 <= cup_depth_rate <= 0.40.
7. Require 20 <= cup_duration <= 200.
8. Require bottom_zone_duration >= 3.
9. Find handle_low after right_rim.
10. Require handle_depth_ratio <= 0.35.
11. Require handle_low.price >= cup_midpoint.
12. Define neckline = max(left_rim.price, right_rim.price).
13. Require breakout close > neckline + 0.2 * ATR.
14. Require breakout volume_ratio >= 1.5.
15. Require liquidity_pass = true.
16. Require spread_pass = true.
```
