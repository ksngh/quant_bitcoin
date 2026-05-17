# Adam and Eve Pattern Mechanical Definition

## Purpose

Define the Adam and Eve Pattern mechanically.

This module detects a bullish double-bottom reversal pattern consisting of a sharp first bottom, a rounded second bottom, and a breakout above the neckline.

This document defines detection logic only.
It does not define order execution.

## Pattern Type

```text
Adam and Eve Pattern
```

## Pattern Categories

```text
Double Bottom Pattern
Bullish Reversal Pattern
Bottom Formation Pattern
Accumulation Pattern
Neckline Breakout Pattern
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
maximum_bottom_difference_rate: 0.05
minimum_pattern_duration: 20
maximum_pattern_duration: 200
maximum_adam_bottom_duration: 5
minimum_eve_bottom_duration: 5
minimum_eve_bottom_zone_duration: 3
bottom_zone_atr_multiplier: 0.5
minimum_adam_range_atr: 1.0
minimum_eve_to_adam_duration_ratio: 1.5
minimum_pattern_height_atr: 1.0
maximum_pattern_height_atr: 8.0
breakout_atr_multiplier: 0.2
minimum_breakout_volume_ratio: 1.5
weak_breakout_volume_ratio: 1.3
require_prior_downtrend: true
require_liquidity_pass: true
require_spread_pass: true
require_displacement_breakout: false
minimum_pattern_score: 0.7
```

## Core Structure

A bullish Adam and Eve Pattern consists of:

```text
prior downtrend
Adam low
neckline pivot
Eve low
neckline
breakout
```

Required index order:

```text
adam_low.index < neckline_pivot.index < eve_low.index < breakout.index
```

## Prior Downtrend Definition

If `require_prior_downtrend = true`, the pattern requires bearish structure before the Adam low.

Valid prior downtrend:

```text
market_structure_status = DOWNTREND
```

or:

```text
recent swing labels contain LH and LL
```

Optional stricter rule:

```text
at least one LH and one LL exist before adam_low.index
```

If prior downtrend is required but not found:

```text
pattern_status = INVALID
```

## Pivot Roles

### Adam Low

The Adam low is the first confirmed pivot low.

```text
adam_low.pivot_type = PIVOT_LOW
```

Adam low should be sharp and V-shaped.

### Neckline Pivot

The neckline pivot is a confirmed pivot high between Adam low and Eve low.

```text
neckline_pivot.pivot_type = PIVOT_HIGH
adam_low.index < neckline_pivot.index < eve_low.index
```

### Eve Low

The Eve low is the second confirmed pivot low after the neckline pivot.

```text
eve_low.pivot_type = PIVOT_LOW
neckline_pivot.index < eve_low.index
```

Eve low should be wider and more rounded than Adam low.

### Breakout

The breakout is the candle that closes above the neckline with ATR buffer.

```text
breakout.index > eve_low.index
```

## Pattern Duration

```text
pattern_duration = breakout.index - adam_low.index
```

Valid duration:

```text
minimum_pattern_duration <= pattern_duration <= maximum_pattern_duration
```

Default:

```text
minimum_pattern_duration = 20
maximum_pattern_duration = 200
```

If pattern duration is outside valid range:

```text
pattern_status = INVALID
```

## Bottom Similarity

Adam low and Eve low should be near the same price level.

```text
bottom_difference = abs(adam_low.price - eve_low.price)
bottom_difference_rate = bottom_difference / adam_low.price
```

Valid bottom similarity:

```text
bottom_difference_rate <= maximum_bottom_difference_rate
```

Default:

```text
maximum_bottom_difference_rate = 0.05
```

If bottom prices are too different:

```text
pattern_status = INVALID
```

## Neckline Definition

Recommended initial version:

```text
neckline = neckline_pivot.price
```

Alternative:

```text
neckline = resistance_zone.center_price
```

Use resistance zone only when a valid resistance zone overlaps the neckline pivot area.

Default:

```text
neckline = neckline_pivot.price
```

## Pattern Height

```text
pattern_bottom = min(adam_low.price, eve_low.price)
pattern_height = neckline - pattern_bottom
pattern_height_atr = pattern_height / ATR
```

Valid pattern height:

```text
minimum_pattern_height_atr <= pattern_height_atr <= maximum_pattern_height_atr
```

Default:

```text
minimum_pattern_height_atr = 1.0
maximum_pattern_height_atr = 8.0
```

If pattern height is too small:

```text
pattern_status = INVALID
```

If pattern height is too large:

```text
pattern_status = WEAK
```

## Adam Bottom Definition

Adam bottom should be sharp and short.

Adam bottom is evaluated around `adam_low.index`.

### Adam Bottom Duration

Define Adam bottom local window:

```text
adam_window_start = adam_low.index - adam_left_window
adam_window_end = adam_low.index + adam_right_window
```

Recommended default:

```yaml
adam_left_window: 3
adam_right_window: 3
```

Adam bottom duration:

```text
adam_bottom_duration = adam_window_end - adam_window_start + 1
```

Valid Adam duration:

```text
adam_bottom_duration <= maximum_adam_bottom_duration
```

Default:

```text
maximum_adam_bottom_duration = 5
```

If Adam bottom duration is too long:

```text
adam_sharpness_score is reduced
```

or:

```text
pattern_status = WEAK
```

## Adam Local Range

```text
adam_local_high = max(high from adam_window_start to adam_window_end)
adam_local_low = adam_low.price
adam_local_range = adam_local_high - adam_local_low
adam_local_range_atr = adam_local_range / ATR
```

Valid Adam range:

```text
adam_local_range_atr >= minimum_adam_range_atr
```

Default:

```text
minimum_adam_range_atr = 1.0
```

If Adam local range is too small:

```text
adam_sharpness_score = 0.0
```

## Adam Decline and Recovery Slope

Adam decline slope:

```text
adam_decline_slope = (adam_low.price - pre_adam_high_price) / (adam_low.index - pre_adam_high_index)
```

Adam recovery slope:

```text
adam_recovery_slope = (neckline_pivot.price - adam_low.price) / (neckline_pivot.index - adam_low.index)
```

Sharp Adam preference:

```text
abs(adam_decline_slope) is large
adam_recovery_slope is large
```

Recommended normalized values:

```text
adam_decline_slope_atr = abs(adam_decline_slope) / ATR
adam_recovery_slope_atr = adam_recovery_slope / ATR
```

## Eve Bottom Definition

Eve bottom should be wider and more rounded than Adam.

Eve bottom is evaluated around `eve_low.index`.

## Eve Bottom Zone

Define a bottom zone around `eve_low.price`.

```text
eve_bottom_zone_low = eve_low.price - bottom_zone_atr_multiplier * ATR
eve_bottom_zone_high = eve_low.price + bottom_zone_atr_multiplier * ATR
```

Default:

```text
bottom_zone_atr_multiplier = 0.5
```

A candle is inside Eve bottom zone when:

```text
eve_bottom_zone_low <= candle.low
and
candle.high <= eve_bottom_zone_high
```

Alternative looser rule:

```text
candle.low <= eve_bottom_zone_high
and
candle.high >= eve_bottom_zone_low
```

Recommended initial version:

```text
use looser overlap rule
```

## Eve Bottom Zone Duration

```text
eve_bottom_zone_duration = number of candles overlapping Eve bottom zone
```

Valid Eve roundness:

```text
eve_bottom_zone_duration >= minimum_eve_bottom_zone_duration
```

Default:

```text
minimum_eve_bottom_zone_duration = 3
```

If Eve bottom zone duration is too short:

```text
eve_roundness_score = 0.0
```

or:

```text
pattern_status = INVALID
```

Recommended initial handling:

```text
Eve not rounded = INVALID
```

## Eve Bottom Duration

Define Eve bottom duration as the number of candles from the start of Eve decline to the end of Eve recovery.

Simple approximation:

```text
eve_bottom_duration = breakout.index - neckline_pivot.index
```

More precise approximation:

```text
eve_bottom_duration = eve_recovery_end_index - eve_decline_start_index
```

Recommended initial version:

```text
eve_bottom_duration = breakout.index - neckline_pivot.index
```

Valid Eve duration:

```text
eve_bottom_duration >= minimum_eve_bottom_duration
```

Default:

```text
minimum_eve_bottom_duration = 5
```

## Adam vs Eve Shape Difference

Adam should be sharper than Eve.

```text
eve_to_adam_duration_ratio = eve_bottom_duration / adam_bottom_duration
```

Valid shape difference:

```text
eve_to_adam_duration_ratio >= minimum_eve_to_adam_duration_ratio
```

Default:

```text
minimum_eve_to_adam_duration_ratio = 1.5
```

If Eve is not sufficiently wider than Adam:

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

## Support / Resistance Context

The neckline is stronger when it overlaps a valid resistance zone.

```text
neckline inside resistance_zone
```

or:

```text
distance(neckline, resistance_zone.center_price) <= 0.5 * ATR
```

The bottom area is stronger when Adam and Eve lows overlap a support zone.

```text
adam_low.price inside support_zone
or
eve_low.price inside support_zone
```

Support / resistance context should affect score.

Do not invalidate by default.

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
prior downtrend condition is satisfied
adam low exists
neckline pivot exists
eve low exists
bottom similarity is valid
Adam bottom is sharp enough
Eve bottom is rounded enough
Eve is wider than Adam
pattern height is valid
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
breakout volume ratio is between weak and strong threshold
pattern height is larger than maximum preferred height
Adam sharpness score is weak
pattern_score >= 0.5 and pattern_score < minimum_pattern_score
```

## PENDING

```text
Adam and Eve structure exists
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
prior downtrend missing
not enough pivots
Adam low missing
neckline pivot missing
Eve low missing
bottom similarity invalid
Eve not rounded
Eve not wider than Adam
pattern height too small
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
prior_downtrend_score: 0.15
bottom_similarity_score: 0.15
adam_sharpness_score: 0.15
eve_roundness_score: 0.15
neckline_quality_score: 0.10
breakout_strength_score: 0.15
volume_confirmation_score: 0.10
liquidity_score: 0.05
```

Formula:

```text
pattern_score =
    prior_downtrend_score * 0.15
  + bottom_similarity_score * 0.15
  + adam_sharpness_score * 0.15
  + eve_roundness_score * 0.15
  + neckline_quality_score * 0.10
  + breakout_strength_score * 0.15
  + volume_confirmation_score * 0.10
  + liquidity_score * 0.05
```

## Prior Downtrend Score

```text
if market_structure_status = DOWNTREND:
    prior_downtrend_score = 1.0

else if recent swing labels contain LH and LL:
    prior_downtrend_score = 0.8

else:
    prior_downtrend_score = 0.0
```

## Bottom Similarity Score

```text
if bottom_difference_rate <= 0.02:
    bottom_similarity_score = 1.0

else if bottom_difference_rate <= 0.05:
    bottom_similarity_score = 0.7

else:
    bottom_similarity_score = 0.0
```

## Adam Sharpness Score

```text
if adam_bottom_duration <= maximum_adam_bottom_duration
and adam_local_range_atr >= 1.5:
    adam_sharpness_score = 1.0

else if adam_bottom_duration <= maximum_adam_bottom_duration
and adam_local_range_atr >= 1.0:
    adam_sharpness_score = 0.7

else:
    adam_sharpness_score = 0.0
```

## Eve Roundness Score

```text
if eve_bottom_zone_duration >= minimum_eve_bottom_zone_duration + 2
and eve_to_adam_duration_ratio >= 2.0:
    eve_roundness_score = 1.0

else if eve_bottom_zone_duration >= minimum_eve_bottom_zone_duration
and eve_to_adam_duration_ratio >= 1.5:
    eve_roundness_score = 0.7

else:
    eve_roundness_score = 0.0
```

## Neckline Quality Score

```text
if neckline overlaps resistance zone:
    neckline_quality_score = 1.0

else if neckline is near resistance zone within 0.5 * ATR:
    neckline_quality_score = 0.7

else:
    neckline_quality_score = 0.5
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
stop_reference = min(adam_low.price, eve_low.price) - breakout_atr_multiplier * ATR
```

Alternative:

```text
stop_reference = eve_low.price - breakout_atr_multiplier * ATR
```

Invalid if:

```text
stop_reference >= entry_reference
```

## Target Reference

Classic measured move target:

```text
target_reference = neckline + pattern_height
```

Risk-reward fallback:

```text
target_reference = entry_reference + 2 * abs(entry_reference - stop_reference)
```

If nearest resistance zone exists before classic target:

```text
target_reference = nearest_resistance_zone
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
  "pattern_type": "ADAM_AND_EVE",
  "direction": "BULLISH",
  "pattern_status": "VALID",
  "adam_low_index": 100,
  "neckline_pivot_index": 125,
  "eve_low_index": 155,
  "breakout_index": 170,
  "adam_low_price": 56000.0,
  "neckline": 65000.0,
  "eve_low_price": 56800.0,
  "bottom_difference_rate": 0.0143,
  "adam_bottom_duration": 5,
  "eve_bottom_duration": 45,
  "eve_bottom_zone_duration": 6,
  "adam_local_range_atr": 1.8,
  "eve_local_range_atr": 1.1,
  "eve_to_adam_duration_ratio": 9.0,
  "pattern_height": 9000.0,
  "pattern_height_atr": 6.4,
  "breakout_price": 65400.0,
  "breakout_distance": 400.0,
  "breakout_distance_atr": 0.29,
  "volume_ratio": 1.8,
  "liquidity_pass": true,
  "spread_pass": true,
  "displacement_confirmed": false,
  "pattern_score": 0.82,
  "entry_reference": 65400.0,
  "stop_reference": 55860.0,
  "target_reference": 74000.0,
  "risk_reward": 0.9,
  "reason": "Bullish Adam and Eve detected with similar lows, sharp Adam bottom, rounded Eve bottom, and volume-confirmed neckline breakout."
}
```

## Output Fields

### pattern_type

Fixed value:

```text
ADAM_AND_EVE
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

### adam_low_index

Index of the Adam low pivot.

### neckline_pivot_index

Index of the pivot high between Adam low and Eve low.

### eve_low_index

Index of the Eve low pivot.

### breakout_index

Index of the breakout candle.

### adam_low_price

Price of the Adam low.

### neckline

Neckline price.

### eve_low_price

Price of the Eve low.

### bottom_difference_rate

Difference between Adam and Eve lows normalized by Adam low.

```text
bottom_difference_rate = abs(adam_low.price - eve_low.price) / adam_low.price
```

### adam_bottom_duration

Duration of Adam bottom area.

### eve_bottom_duration

Duration of Eve bottom area.

### eve_bottom_zone_duration

Number of candles overlapping Eve bottom zone.

### adam_local_range_atr

Adam local range normalized by ATR.

### eve_local_range_atr

Eve local range normalized by ATR.

### eve_to_adam_duration_ratio

Eve duration divided by Adam duration.

### pattern_height

Distance from neckline to lower bottom.

### pattern_height_atr

Pattern height normalized by ATR.

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

### No prior downtrend

If `require_prior_downtrend = true` and prior downtrend is missing:

```text
pattern_status = INVALID
```

### Not enough pivots

If valid Adam low, neckline pivot, and Eve low cannot be found:

```text
pattern_status = INVALID
```

### Adam low missing

If no valid first pivot low exists:

```text
pattern_status = INVALID
```

### Neckline pivot missing

If no valid pivot high exists between Adam low and Eve low:

```text
pattern_status = INVALID
```

### Eve low missing

If no valid second pivot low exists after neckline pivot:

```text
pattern_status = INVALID
```

### Bottom prices too different

If:

```text
bottom_difference_rate > maximum_bottom_difference_rate
```

Then:

```text
pattern_status = INVALID
```

### Adam bottom not sharp

If:

```text
adam_sharpness_score = 0.0
```

Then:

```text
pattern_status = WEAK
```

or, if strict mode is enabled:

```text
pattern_status = INVALID
```

### Eve bottom not rounded

If:

```text
eve_bottom_zone_duration < minimum_eve_bottom_zone_duration
```

Then:

```text
pattern_status = INVALID
```

### Eve not wider than Adam

If:

```text
eve_to_adam_duration_ratio < minimum_eve_to_adam_duration_ratio
```

Then:

```text
pattern_status = INVALID
```

### Pattern height too small

If:

```text
pattern_height_atr < minimum_pattern_height_atr
```

Then:

```text
pattern_status = INVALID
```

### Pattern height too large

If:

```text
pattern_height_atr > maximum_pattern_height_atr
```

Then:

```text
pattern_status = WEAK
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

### Multiple candidate patterns

If multiple candidates exist:

```text
select highest pattern_score
```

Tie-breakers:

```text
1. better bottom similarity
2. stronger Eve roundness
3. stronger breakout volume_ratio
4. higher breakout_distance_atr
5. more recent breakout
```

### False breakout

Optional post-break check:

```yaml
false_break_check_window: 3
```

False breakout candidate:

```text
price closes back below neckline within false_break_check_window
```

If detected:

```text
pattern_status = WEAK
```

or:

```text
false_break_candidate = true
```

## Detection Logic

```text
1. Check liquidity_pass.
2. Check spread_pass.
3. Load confirmed pivot highs and pivot lows.
4. Find prior downtrend context.
5. Search pivot sequence: Adam low -> neckline pivot -> Eve low.
6. Validate bottom similarity.
7. Validate Adam sharpness.
8. Validate Eve roundness.
9. Validate Eve wider-than-Adam condition.
10. Calculate neckline.
11. Calculate pattern height.
12. Validate pattern duration.
13. Search breakout candle after Eve low.
14. Apply ATR breakout buffer.
15. Apply volume confirmation.
16. Optionally check displacement breakout.
17. Calculate score.
18. Set pattern status.
19. Return best valid, weak, or pending signal.
```

## Pseudocode

```python
def detect_adam_and_eve(context, config):
    if config.require_liquidity_pass and not context.liquidity.liquidity_pass:
        return invalid_result("liquidity_failed")

    if config.require_spread_pass and not context.spread.spread_pass:
        return invalid_result("spread_failed")

    candidates = []

    pivot_lows = context.confirmed_pivot_lows
    pivot_highs = context.confirmed_pivot_highs

    for adam_low in pivot_lows:
        if config.require_prior_downtrend:
            if not has_prior_downtrend(adam_low, context.swing_structure, config):
                continue

        possible_necklines = [
            pivot for pivot in pivot_highs
            if pivot.index > adam_low.index
        ]

        for neckline_pivot in possible_necklines:
            possible_eve_lows = [
                pivot for pivot in pivot_lows
                if pivot.index > neckline_pivot.index
            ]

            for eve_low in possible_eve_lows:
                candidate = build_adam_and_eve_candidate(
                    adam_low,
                    neckline_pivot,
                    eve_low,
                    context,
                    config
                )

                evaluated = evaluate_adam_and_eve_candidate(
                    candidate,
                    context,
                    config
                )

                if evaluated["pattern_status"] in ["VALID", "WEAK", "PENDING"]:
                    candidates.append(evaluated)

    if not candidates:
        return invalid_result("no_valid_adam_and_eve")

    return select_best_candidate(candidates)
```

## Candidate Validation

```python
def evaluate_adam_and_eve_candidate(candidate, context, config):
    if candidate.bottom_difference_rate > config.maximum_bottom_difference_rate:
        return invalid_result("bottom_difference_too_large")

    if candidate.pattern_height_atr < config.minimum_pattern_height_atr:
        return invalid_result("pattern_height_too_small")

    if candidate.eve_bottom_zone_duration < config.minimum_eve_bottom_zone_duration:
        return invalid_result("eve_not_rounded")

    if candidate.eve_to_adam_duration_ratio < config.minimum_eve_to_adam_duration_ratio:
        return invalid_result("eve_not_wider_than_adam")

    breakout = find_breakout_after_eve(
        candidate,
        context,
        config
    )

    if breakout is None:
        candidate.pattern_status = "PENDING"
        return candidate

    candidate.breakout_index = breakout.index
    candidate.breakout_price = breakout.close
    candidate.breakout_distance = breakout.close - candidate.neckline
    candidate.breakout_distance_atr = candidate.breakout_distance / breakout.atr
    candidate.volume_ratio = breakout.volume_ratio

    score = calculate_adam_and_eve_score(
        candidate,
        context,
        config
    )

    candidate.pattern_score = score
    candidate.pattern_status = classify_pattern_status(
        candidate,
        config
    )

    return candidate
```

## Breakout Detection

```python
def find_breakout_after_eve(candidate, context, config):
    candles = context.candles_after(candidate.eve_low_index)

    for candle in candles:
        atr = context.atr_at(candle.index)
        volume_ratio = context.volume_ratio_at(candle.index)

        if atr is None or volume_ratio is None:
            continue

        breakout_threshold = (
            candidate.neckline
            + config.breakout_atr_multiplier * atr
        )

        if candle.close > breakout_threshold:
            if volume_ratio < config.weak_breakout_volume_ratio:
                return None

            candle.atr = atr
            candle.volume_ratio = volume_ratio
            return candle

    return None
```

## Java-style Domain Model Example

```java
public enum AdamAndEveDirection {
    BULLISH,
    NONE
}
```

```java
public enum AdamAndEveStatus {
    VALID,
    WEAK,
    INVALID,
    PENDING
}
```

```java
public record AdamAndEveSignal(
    String symbol,
    Instant timestamp,
    String patternType,
    AdamAndEveDirection direction,
    AdamAndEveStatus patternStatus,
    int adamLowIndex,
    int necklinePivotIndex,
    int eveLowIndex,
    int breakoutIndex,
    BigDecimal adamLowPrice,
    BigDecimal neckline,
    BigDecimal eveLowPrice,
    BigDecimal bottomDifferenceRate,
    int adamBottomDuration,
    int eveBottomDuration,
    int eveBottomZoneDuration,
    BigDecimal adamLocalRangeAtr,
    BigDecimal eveLocalRangeAtr,
    BigDecimal eveToAdamDurationRatio,
    BigDecimal patternHeight,
    BigDecimal patternHeightAtr,
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
adam_and_eve:
  maximum_bottom_difference_rate: 0.05
  minimum_pattern_duration: 20
  maximum_pattern_duration: 200
  maximum_adam_bottom_duration: 5
  minimum_eve_bottom_duration: 5
  minimum_eve_bottom_zone_duration: 3
  bottom_zone_atr_multiplier: 0.5
  minimum_adam_range_atr: 1.0
  minimum_eve_to_adam_duration_ratio: 1.5
  minimum_pattern_height_atr: 1.0
  maximum_pattern_height_atr: 8.0
  breakout_atr_multiplier: 0.2
  minimum_breakout_volume_ratio: 1.5
  weak_breakout_volume_ratio: 1.3
  require_prior_downtrend: true
  require_liquidity_pass: true
  require_spread_pass: true
  require_displacement_breakout: false
  minimum_pattern_score: 0.7
```

## Final Mechanical Rule

```text
Bullish Adam and Eve:
1. Require prior downtrend.
2. Find Adam low as first pivot low.
3. Find neckline pivot as pivot high after Adam low.
4. Find Eve low as pivot low after neckline pivot.
5. Require bottom_difference_rate <= 0.05.
6. Require Adam bottom to be sharp.
7. Require Eve bottom_zone_duration >= 3.
8. Require eve_to_adam_duration_ratio >= 1.5.
9. Define neckline = neckline_pivot.price.
10. Require pattern_height_atr >= 1.0.
11. Require breakout close > neckline + 0.2 * ATR.
12. Require breakout volume_ratio >= 1.5.
13. Require liquidity_pass = true.
14. Require spread_pass = true.
```
