# Cup and Handle Pattern Mechanical Definition

## Purpose

Define the Cup and Handle Pattern mechanically.

This module detects a bullish continuation breakout setup consisting of a prior uptrend, a rounded cup, a shallow handle, and a neckline breakout with volume confirmation.

This document defines detection logic only.
It does not define order execution.

## Pattern Type

```text
CUP_AND_HANDLE
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

Optional inputs:

```text
displacement candle snapshots
```

## Default Parameters

```yaml
cup_and_handle:
  maximum_rim_difference_rate: 0.05
  minimum_cup_depth_rate: 0.10
  maximum_cup_depth_rate: 0.40
  minimum_cup_duration: 20
  maximum_cup_duration: 200
  minimum_bottom_zone_duration: 3
  bottom_zone_atr_multiplier: 0.5
  maximum_slope_imbalance_rate: 0.60
  maximum_handle_depth_ratio: 0.35
  minimum_handle_duration: 3
  maximum_handle_duration: 40
  breakout_atr_multiplier: 0.2
  minimum_breakout_volume_ratio: 1.5
  weak_breakout_volume_ratio: 1.3
  require_liquidity_pass: true
  require_spread_pass: true
  require_displacement_breakout: false
  minimum_pattern_score: 0.7
  weak_pattern_score: 0.5
  default_entry_reference: BREAKOUT_CLOSE
  default_risk_reward: 2.0
```

## Prior Uptrend Requirement

A bullish Cup and Handle candidate requires prior upward structure before the left rim.

Acceptable conditions:

```text
market_structure_status = UPTREND
```

or:

```text
recent swing labels before left_rim contain HH and HL
```

If no prior upward structure exists:

```text
pattern_status = INVALID
reason = NO_PRIOR_UPTREND
```

## Cup Structure

The cup is defined by three confirmed pivots:

```text
left_rim = confirmed pivot high
cup_bottom = confirmed pivot low
right_rim = confirmed pivot high
```

Required order:

```text
left_rim.index < cup_bottom.index < right_rim.index
```

The module must ignore unconfirmed pivots.

## Rim Similarity

The left and right rims should be near the same price level.

```text
rim_difference_rate = abs(left_rim.price - right_rim.price) / left_rim.price
```

Valid condition:

```text
rim_difference_rate <= maximum_rim_difference_rate
```

Default:

```text
maximum_rim_difference_rate = 0.05
```

If rims are too different:

```text
pattern_status = INVALID
reason = RIM_PRICES_TOO_DIFFERENT
```

## Cup Depth

```text
rim_reference_price = min(left_rim.price, right_rim.price)
cup_depth = rim_reference_price - cup_bottom.price
cup_depth_rate = cup_depth / rim_reference_price
```

Valid range:

```text
minimum_cup_depth_rate <= cup_depth_rate <= maximum_cup_depth_rate
```

Default:

```text
minimum_cup_depth_rate = 0.10
maximum_cup_depth_rate = 0.40
```

If the cup is too shallow or too deep:

```text
pattern_status = INVALID
```

## Cup Duration

```text
cup_duration = right_rim.index - left_rim.index
```

Valid range:

```text
minimum_cup_duration <= cup_duration <= maximum_cup_duration
```

Default:

```text
minimum_cup_duration = 20
maximum_cup_duration = 200
```

If the cup duration is outside the valid range:

```text
pattern_status = INVALID
```

## Cup Roundness

The pattern should reject sharp V-shaped recoveries.

### Bottom Zone Duration

Define bottom zone as candles near the cup bottom:

```text
abs(candle.close - cup_bottom.price) <= bottom_zone_atr_multiplier * ATR
```

Bottom zone duration:

```text
bottom_zone_duration = count of candles satisfying bottom zone condition between left_rim and right_rim
```

Valid condition:

```text
bottom_zone_duration >= minimum_bottom_zone_duration
```

Default:

```text
minimum_bottom_zone_duration = 3
bottom_zone_atr_multiplier = 0.5
```

### Decline and Recovery Durations

```text
left_decline_duration = cup_bottom.index - left_rim.index
right_recovery_duration = right_rim.index - cup_bottom.index
```

Both durations must be positive.

### Slope Balance

```text
slope_imbalance_rate = abs(left_decline_duration - right_recovery_duration) / cup_duration
```

Recommended valid condition:

```text
slope_imbalance_rate <= maximum_slope_imbalance_rate
```

Default:

```text
maximum_slope_imbalance_rate = 0.60
```

If bottom duration is too short or slope balance fails:

```text
pattern_status = INVALID
reason = V_SHAPED_RECOVERY
```

## Handle Structure

The handle occurs after the right rim and before breakout.

```text
right_rim.index < handle_low.index < breakout.index
```

The handle low should be selected from confirmed pivot lows after the right rim, or from the lowest candle low in the handle window when no confirmed pivot low exists yet.

If no handle low exists:

```text
pattern_status = INVALID
reason = HANDLE_MISSING
```

## Handle Depth

```text
handle_depth = right_rim.price - handle_low.price
handle_depth_ratio = handle_depth / cup_depth
```

Valid condition:

```text
handle_depth_ratio <= maximum_handle_depth_ratio
```

Default:

```text
maximum_handle_depth_ratio = 0.35
```

If the handle is too deep:

```text
pattern_status = INVALID
reason = HANDLE_TOO_DEEP
```

## Handle Duration

```text
handle_duration = breakout.index - right_rim.index
```

Valid range:

```text
minimum_handle_duration <= handle_duration <= maximum_handle_duration
```

Default:

```text
minimum_handle_duration = 3
maximum_handle_duration = 40
```

If handle duration is too short or too long:

```text
pattern_status = INVALID
```

## Neckline

Recommended initial neckline:

```text
neckline = max(left_rim.price, right_rim.price)
```

Alternative context from Support / Resistance Zone:

```text
neckline = resistance_zone.center_price
```

Use the pivot-based neckline for the initial version. Use resistance zone context only for scoring and target/reference context unless a future task explicitly changes the neckline rule.

## Breakout Validation

Bullish breakout occurs when the breakout candle closes above the neckline by an ATR buffer.

```text
breakout_price = breakout.close
breakout_distance = breakout.close - neckline
breakout_distance_atr = breakout_distance / ATR
```

Valid breakout:

```text
breakout.close > neckline + breakout_atr_multiplier * ATR
```

Default:

```text
breakout_atr_multiplier = 0.2
```

If price is below the neckline or does not clear the ATR buffer:

```text
pattern_status = PENDING
```

## Volume Confirmation

Use the breakout candle volume ratio.

Strong confirmation:

```text
volume_ratio >= minimum_breakout_volume_ratio
```

Default:

```text
minimum_breakout_volume_ratio = 1.5
```

Weak confirmation:

```text
weak_breakout_volume_ratio <= volume_ratio < minimum_breakout_volume_ratio
```

Default:

```text
weak_breakout_volume_ratio = 1.3
```

If volume ratio is missing:

```text
pattern_status = INVALID
```

If breakout exists but volume is weak:

```text
pattern_status = WEAK
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

## Optional Displacement Breakout

Recommended initial setting:

```text
require_displacement_breakout = false
```

If enabled, breakout candle must satisfy:

```text
breakout.displacement_direction = BULLISH
breakout.displacement_status = VALID
```

If disabled, displacement confirmation should only affect `displacement_score`.

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
prior uptrend confirmed
valid cup pivots exist
rim similarity valid
cup depth valid
cup duration valid
cup roundness valid
handle valid
breakout clears neckline with ATR buffer
volume_ratio >= minimum_breakout_volume_ratio
pattern_score >= minimum_pattern_score
```

### WEAK

```text
valid cup and handle exists
breakout clears neckline with ATR buffer
volume_ratio >= weak_breakout_volume_ratio
volume_ratio < minimum_breakout_volume_ratio
```

or:

```text
pattern_score >= weak_pattern_score
and
pattern_score < minimum_pattern_score
```

### PENDING

```text
valid cup and handle exists
but breakout is missing
```

or:

```text
breakout does not clear ATR buffer yet
```

### INVALID

```text
liquidity filter fails
spread filter fails
no prior uptrend
not enough pivots
missing left rim
missing cup bottom
missing right rim
rim prices too different
cup too shallow
cup too deep
cup duration invalid
V-shaped recovery
handle missing
handle too deep
handle duration invalid
volume ratio missing
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
liquidity_score: 0.05
support_resistance_context_score: 0.03
displacement_score: 0.02
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
  + liquidity_score * 0.05
  + support_resistance_context_score * 0.03
  + displacement_score * 0.02
```

## Score Components

### Prior Trend Score

```text
if market_structure_status = UPTREND:
    prior_trend_score = 1.0
else if recent swing labels contain HH and HL:
    prior_trend_score = 0.8
else:
    prior_trend_score = 0.0
```

### Cup Shape Score

```text
if cup_depth_rate is within default range and bottom_zone_duration >= minimum_bottom_zone_duration:
    cup_shape_score = 1.0
else if cup_depth_rate is valid but roundness is marginal:
    cup_shape_score = 0.6
else:
    cup_shape_score = 0.0
```

### Rim Similarity Score

```text
if rim_difference_rate <= 0.02:
    rim_similarity_score = 1.0
else if rim_difference_rate <= maximum_rim_difference_rate:
    rim_similarity_score = 0.7
else:
    rim_similarity_score = 0.0
```

### Handle Quality Score

```text
if handle_depth_ratio <= 0.20 and handle duration is valid:
    handle_quality_score = 1.0
else if handle_depth_ratio <= maximum_handle_depth_ratio and handle duration is valid:
    handle_quality_score = 0.7
else:
    handle_quality_score = 0.0
```

### Breakout Strength Score

```text
if breakout_distance_atr >= 0.5:
    breakout_strength_score = 1.0
else if breakout_distance_atr >= breakout_atr_multiplier:
    breakout_strength_score = 0.7
else:
    breakout_strength_score = 0.0
```

### Volume Confirmation Score

```text
if volume_ratio >= 2.0:
    volume_confirmation_score = 1.0
else if volume_ratio >= minimum_breakout_volume_ratio:
    volume_confirmation_score = 0.8
else if volume_ratio >= weak_breakout_volume_ratio:
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

### Support / Resistance Context Score

```text
if neckline overlaps resistance zone:
    support_resistance_context_score = 1.0
else if neckline is near resistance zone within 0.5 * ATR:
    support_resistance_context_score = 0.7
else:
    support_resistance_context_score = 0.5
```

### Displacement Score

```text
if breakout candle is bullish displacement candle:
    displacement_score = 1.0
else:
    displacement_score = 0.0
```

## Entry Reference

This module must not execute orders.

Supported bullish entry references:

```text
breakout close
next candle open
neckline retest
```

Recommended default:

```text
entry_reference = breakout close
```

## Stop Reference

Supported bullish stop references:

```text
handle_low
neckline - breakout_atr_multiplier * ATR
```

Recommended default:

```text
stop_reference = handle_low
```

If neckline retest failure is used:

```text
stop_reference = neckline - breakout_atr_multiplier * ATR
```

## Target Reference

Primary measured-move target:

```text
target_reference = neckline + cup_depth
```

Alternative risk-reward target:

```text
target_reference = entry_reference + 2 * abs(entry_reference - stop_reference)
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
  "cup_bottom_price": 52000.0,
  "right_rim_price": 64800.0,
  "handle_low_price": 61000.0,
  "neckline": 65000.0,
  "cup_depth": 12800.0,
  "cup_depth_rate": 0.1975,
  "cup_duration": 70,
  "handle_depth": 3800.0,
  "handle_depth_ratio": 0.2969,
  "handle_duration": 20,
  "breakout_price": 65400.0,
  "breakout_distance_atr": 0.5,
  "volume_ratio": 1.8,
  "liquidity_pass": true,
  "spread_pass": true,
  "pattern_score": 0.84,
  "entry_reference": 65400.0,
  "stop_reference": 61000.0,
  "target_reference": 77800.0,
  "risk_reward": 2.82,
  "reason": "Bullish Cup and Handle detected with prior uptrend, rounded cup, valid handle, ATR breakout, and volume confirmation."
}
```

## Output Fields

- `pattern_type`: fixed value `CUP_AND_HANDLE`.
- `direction`: `BULLISH` or `NONE`; `BEARISH_INVERTED` is reserved for a future task.
- `pattern_status`: `VALID`, `WEAK`, `INVALID`, or `PENDING`.
- `left_rim_index`: candle index of the left rim pivot high.
- `cup_bottom_index`: candle index of the cup bottom pivot low.
- `right_rim_index`: candle index of the right rim pivot high.
- `handle_low_index`: candle index of the handle low.
- `breakout_index`: candle index of the breakout candle.
- `left_rim_price`: price of the left rim pivot high.
- `cup_bottom_price`: price of the cup bottom pivot low.
- `right_rim_price`: price of the right rim pivot high.
- `handle_low_price`: price of the handle low.
- `neckline`: rim resistance level used for breakout validation.
- `cup_depth`: distance from rim reference to cup bottom.
- `cup_depth_rate`: cup depth normalized by rim reference price.
- `cup_duration`: number of candles from left rim to right rim.
- `handle_depth`: distance from right rim to handle low.
- `handle_depth_ratio`: handle depth divided by cup depth.
- `handle_duration`: number of candles from right rim to breakout.
- `breakout_price`: close price of the breakout candle.
- `breakout_distance_atr`: breakout distance normalized by ATR.
- `volume_ratio`: breakout candle volume ratio.
- `liquidity_pass`: result from Liquidity module.
- `spread_pass`: result from Bid-Ask Spread module.
- `pattern_score`: final score between `0.0` and `1.0`.
- `entry_reference`: reference price for possible entry.
- `stop_reference`: reference price for invalidation.
- `target_reference`: reference price for possible target.
- `risk_reward`: reward-to-risk ratio.
- `reason`: short explanation for detection result.

## Edge Cases

### No Prior Uptrend

If prior uptrend is not confirmed:

```text
pattern_status = INVALID
```

### Not Enough Pivots

If there are not enough confirmed pivot highs and lows to form left rim, cup bottom, and right rim:

```text
pattern_status = INVALID
```

### Missing Rim or Bottom

If left rim, cup bottom, or right rim is missing:

```text
pattern_status = INVALID
```

### Rim Prices Too Different

If `rim_difference_rate > maximum_rim_difference_rate`:

```text
pattern_status = INVALID
```

### Cup Too Shallow or Too Deep

If cup depth is outside the valid range:

```text
pattern_status = INVALID
```

### Cup Duration Invalid

If cup duration is too short or too long:

```text
pattern_status = INVALID
```

### V-Shaped Recovery

If bottom zone duration is too short or slope balance fails:

```text
pattern_status = INVALID
```

### Handle Missing

If no valid handle low exists after the right rim:

```text
pattern_status = INVALID
```

### Handle Too Deep

If `handle_depth_ratio > maximum_handle_depth_ratio`:

```text
pattern_status = INVALID
```

### Handle Too Long or Too Short

If handle duration is outside the valid range:

```text
pattern_status = INVALID
```

### Breakout Missing

If a valid cup and handle exists but price has not broken the neckline:

```text
pattern_status = PENDING
```

### Breakout Without ATR Buffer

If close is above neckline but does not exceed the ATR buffer:

```text
pattern_status = PENDING
```

### Breakout Without Volume Confirmation

If breakout exists but volume is below strong confirmation and above weak confirmation:

```text
pattern_status = WEAK
```

If volume is below weak confirmation:

```text
pattern_status = INVALID
```

### Low Liquidity

If liquidity fails:

```text
pattern_status = INVALID
```

### Wide Spread

If spread fails:

```text
pattern_status = INVALID
```

### Overlapping Cup Candidates

If multiple valid cup candidates overlap:

```text
select highest pattern_score candidate
```

Tie-break priority:

```text
1. higher pattern_score
2. better rim similarity
3. stronger breakout volume_ratio
4. longer valid cup duration within range
5. shallower valid handle_depth_ratio
```

### Multiple Possible Handles

If multiple handle lows exist after the right rim:

```text
select the handle with the highest handle_quality_score that still produces a valid breakout
```

### False Breakout

If price breaks the neckline and then closes back below the neckline within a short confirmation window:

```text
mark as FALSE_BREAKOUT_CANDIDATE
```

Recommended optional parameter:

```yaml
false_breakout_check_window: 3
```

## Detection Logic

```text
1. Check liquidity_pass.
2. Check spread_pass.
3. Confirm prior uptrend using Swing Structure.
4. Load confirmed pivot highs and lows.
5. Select left_rim pivot high, cup_bottom pivot low, and right_rim pivot high in required order.
6. Validate rim similarity.
7. Validate cup depth.
8. Validate cup duration.
9. Validate cup roundness and reject V-shaped recoveries.
10. Identify handle low after right rim.
11. Validate handle depth and duration.
12. Define neckline as max(left_rim.price, right_rim.price).
13. Check bullish breakout above neckline with ATR buffer.
14. Validate breakout volume ratio.
15. Optionally evaluate breakout displacement candle.
16. Calculate pattern score.
17. Define entry, stop, target, and risk/reward references.
18. Return VALID, WEAK, PENDING, or INVALID pattern output.
```

## Pseudocode

```python
def detect_cup_and_handle(context, config):
    if config.require_liquidity_pass and not context.liquidity.liquidity_pass:
        return invalid_result("liquidity_failed")

    if config.require_spread_pass and not context.spread.spread_pass:
        return invalid_result("spread_failed")

    if not has_prior_uptrend(context.swing_structure):
        return invalid_result("no_prior_uptrend")

    candidates = []

    for left_rim in context.confirmed_pivot_highs:
        for cup_bottom in context.confirmed_pivot_lows_after(left_rim.index):
            for right_rim in context.confirmed_pivot_highs_after(cup_bottom.index):
                if not valid_pivot_order(left_rim, cup_bottom, right_rim):
                    continue

                cup = build_cup_candidate(left_rim, cup_bottom, right_rim, context, config)

                if not cup.is_valid:
                    continue

                handle = find_best_handle(cup, context, config)

                if handle is None:
                    candidates.append(pending_result(cup, "handle_missing"))
                    continue

                breakout = find_breakout(cup, handle, context, config)

                result = evaluate_candidate(cup, handle, breakout, context, config)
                candidates.append(result)

    return select_best_candidate(candidates)
```

## Final Mechanical Rule

```text
Bullish Cup and Handle:
1. Require prior uptrend by Swing Structure or recent HH/HL labels.
2. Use confirmed pivot high as left_rim.
3. Use confirmed pivot low as cup_bottom.
4. Use confirmed pivot high as right_rim.
5. Require left_rim.index < cup_bottom.index < right_rim.index.
6. Require rim_difference_rate <= 0.05.
7. Require 0.10 <= cup_depth_rate <= 0.40.
8. Require 20 <= cup_duration <= 200.
9. Require bottom_zone_duration >= 3 to reject V-shaped recoveries.
10. Identify handle_low after right_rim and before breakout.
11. Require handle_depth_ratio <= 0.35.
12. Require 3 <= handle_duration <= 40.
13. Set neckline = max(left_rim.price, right_rim.price).
14. Require breakout close > neckline + 0.2 * ATR.
15. Require breakout volume_ratio >= 1.5 for VALID, or >= 1.3 for WEAK.
16. Require liquidity_pass = true.
17. Require spread_pass = true.
18. Define entry, stop, and target references only; do not execute orders.
```
