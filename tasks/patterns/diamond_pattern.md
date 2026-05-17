# Diamond Pattern Mechanical Definition

## Purpose

Define the Diamond Pattern mechanically.

This module detects a volatility expansion-contraction structure and validates directional breakout or breakdown from the contraction boundary.

This document defines detection logic only.
It does not define order execution.

## Pattern Type

```text
Diamond Pattern
```

## Pattern Categories

```text
Volatility Expansion-Contraction Pattern
Breakout Pattern
Breakdown Pattern
Potential Reversal Pattern
Potential Continuation Pattern
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
displacement candle snapshots
```

## Default Parameters

```yaml
minimum_pivot_count: 6
maximum_pivot_count: 10
minimum_pattern_duration: 20
maximum_pattern_duration: 200
minimum_expansion_range_change_atr: 1.0
minimum_contraction_range_change_rate: 0.20
minimum_pattern_height_atr: 1.0
maximum_pattern_height_atr: 8.0
maximum_boundary_touch_deviation_atr: 0.5
breakout_atr_multiplier: 0.2
minimum_breakout_volume_ratio: 1.5
weak_breakout_volume_ratio: 1.3
require_liquidity_pass: true
require_spread_pass: true
require_displacement_breakout: false
minimum_pattern_score: 0.7
```

## Core Structure

A Diamond Pattern consists of two phases:

```text
expansion phase
contraction phase
```

Expansion phase:

```text
pivot highs rise
pivot lows fall
local range expands
```

Contraction phase:

```text
pivot highs fall
pivot lows rise
local range contracts
```

The trade direction is not determined during pattern formation.

Direction is determined only after breakout or breakdown:

```text
break above contracting upper boundary = BULLISH
break below contracting lower boundary = BEARISH
no break = NONE
```

## Required Pivot Structure

Use confirmed pivots only.

Minimum requirement:

```text
pivot_count >= minimum_pivot_count
```

Default:

```text
minimum_pivot_count = 6
```

Recommended pivot sequence:

```text
P1 = pivot high or pivot low
P2 = opposite pivot
P3 = pivot high or pivot low
P4 = opposite pivot
P5 = pivot high or pivot low
P6 = opposite pivot
```

The exact first pivot type may vary.

The selected pivot sequence must include:

```text
at least 3 pivot highs
at least 3 pivot lows
```

## Pattern Duration

```text
pattern_duration = last_pattern_pivot.index - first_pattern_pivot.index
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

If duration is outside valid range:

```text
pattern_status = INVALID
```

## Local Range Definition

For a given segment of pivots:

```text
local_range = local_high - local_low
```

Where:

```text
local_high = highest pivot high in segment
local_low = lowest pivot low in segment
```

## Diamond Center

The diamond center is the point where the pivot-based local range is maximum.

Mechanical definition:

```text
diamond_center = pivot area where local_range is maximum
```

Recommended method:

```text
1. Build rolling pivot windows.
2. For each window, calculate local_range.
3. Select the pivot index where local_range is maximum.
```

Alternative simple method:

```text
diamond_center = middle pivot of selected pivot sequence
```

Recommended initial version:

```text
diamond_center = maximum local range point
```

## Phase Split

After determining `diamond_center`, split selected pivots into:

```text
expansion_pivots = pivots from pattern_start to diamond_center
contraction_pivots = pivots from diamond_center to pattern_end
```

Required:

```text
expansion_pivots contains at least 2 pivot highs and 2 pivot lows
contraction_pivots contains at least 2 pivot highs and 2 pivot lows
```

If not:

```text
pattern_status = INVALID
```

## Expansion Phase Definition

Expansion phase must show widening price range.

### Expansion High Condition

Pivot highs should rise.

```text
latest_expansion_high.price > earliest_expansion_high.price
```

Expansion high slope:

```text
expansion_high_slope = linear_regression_slope(expansion_pivot_high_prices over pivot indices)
```

Valid:

```text
expansion_high_slope > 0
```

### Expansion Low Condition

Pivot lows should fall.

```text
latest_expansion_low.price < earliest_expansion_low.price
```

Expansion low slope:

```text
expansion_low_slope = linear_regression_slope(expansion_pivot_low_prices over pivot indices)
```

Valid:

```text
expansion_low_slope < 0
```

### Expansion Range Change

```text
expansion_start_range = range near expansion start
expansion_end_range = range near diamond center
expansion_range_change = expansion_end_range - expansion_start_range
```

Valid:

```text
expansion_range_change > 0
```

ATR-normalized expansion:

```text
expansion_range_change_atr = expansion_range_change / ATR
```

Required:

```text
expansion_range_change_atr >= minimum_expansion_range_change_atr
```

Default:

```text
minimum_expansion_range_change_atr = 1.0
```

## Contraction Phase Definition

Contraction phase must show narrowing price range.

### Contraction High Condition

Pivot highs should fall.

```text
latest_contraction_high.price < earliest_contraction_high.price
```

Contraction high slope:

```text
contraction_high_slope = linear_regression_slope(contraction_pivot_high_prices over pivot indices)
```

Valid:

```text
contraction_high_slope < 0
```

### Contraction Low Condition

Pivot lows should rise.

```text
latest_contraction_low.price > earliest_contraction_low.price
```

Contraction low slope:

```text
contraction_low_slope = linear_regression_slope(contraction_pivot_low_prices over pivot indices)
```

Valid:

```text
contraction_low_slope > 0
```

### Contraction Range Change

```text
contraction_start_range = range near diamond center
contraction_end_range = range near contraction end
contraction_range_change = contraction_start_range - contraction_end_range
```

Valid:

```text
contraction_range_change > 0
```

Contraction range change rate:

```text
contraction_range_change_rate = contraction_range_change / contraction_start_range
```

Required:

```text
contraction_range_change_rate >= minimum_contraction_range_change_rate
```

Default:

```text
minimum_contraction_range_change_rate = 0.20
```

## Pattern Height

Pattern height is the maximum vertical range of the diamond.

```text
pattern_height = highest_pivot_high.price - lowest_pivot_low.price
```

Pattern height ATR:

```text
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

## Boundary Construction

Use contraction phase pivots for breakout boundaries.

### Upper Boundary

The upper boundary is built from contraction pivot highs.

```text
upper_boundary = trendline built from contraction pivot highs
```

Expected slope:

```text
upper_boundary_slope < 0
```

### Lower Boundary

The lower boundary is built from contraction pivot lows.

```text
lower_boundary = trendline built from contraction pivot lows
```

Expected slope:

```text
lower_boundary_slope > 0
```

## Boundary Value

At current candle index:

```text
upper_boundary_value = upper_boundary_slope * current_index + upper_boundary_intercept
lower_boundary_value = lower_boundary_slope * current_index + lower_boundary_intercept
```

## Boundary Touch Validation

Each contraction pivot should be close enough to its boundary.

Deviation:

```text
deviation = abs(pivot.price - boundary_value_at_pivot_index)
```

Valid touch:

```text
deviation <= maximum_boundary_touch_deviation_atr * ATR
```

Default:

```text
maximum_boundary_touch_deviation_atr = 0.5
```

Required:

```text
upper_boundary_touch_count >= 2
lower_boundary_touch_count >= 2
```

## Bullish Breakout Definition

A bullish breakout occurs when price closes above the contracting upper boundary.

```text
close > upper_boundary_value + breakout_atr_multiplier * ATR
```

Default:

```text
breakout_atr_multiplier = 0.2
```

Breakout distance:

```text
breakout_distance = close - upper_boundary_value
breakout_distance_atr = breakout_distance / ATR
```

If price is above upper boundary but does not exceed ATR buffer:

```text
pattern_status = PENDING
```

## Bearish Breakdown Definition

A bearish breakdown occurs when price closes below the contracting lower boundary.

```text
close < lower_boundary_value - breakout_atr_multiplier * ATR
```

Default:

```text
breakout_atr_multiplier = 0.2
```

Breakout distance:

```text
breakout_distance = lower_boundary_value - close
breakout_distance_atr = breakout_distance / ATR
```

If price is below lower boundary but does not exceed ATR buffer:

```text
pattern_status = PENDING
```

## Volume Confirmation

Use the breakout or breakdown candle volume ratio.

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

If:

```text
volume_ratio < weak_breakout_volume_ratio
```

Then:

```text
pattern_status = INVALID
```

## Optional Displacement Breakout

If `require_displacement_breakout = true`, breakout candle must satisfy:

For bullish breakout:

```text
displacement_direction = BULLISH
displacement_status = VALID
```

For bearish breakdown:

```text
displacement_direction = BEARISH
displacement_status = VALID
```

If required and not satisfied:

```text
pattern_status = INVALID
```

If not required:

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
minimum pivot count satisfied
pattern duration valid
expansion phase valid
contraction phase valid
pattern height valid
upper and lower boundaries valid
breakout or breakdown exceeds ATR buffer
volume_ratio >= minimum_breakout_volume_ratio
pattern_score >= minimum_pattern_score
```

## WEAK

```text
core diamond structure exists
but one or more non-critical conditions are weak
```

Examples:

```text
volume_ratio is between weak threshold and strong threshold
pattern_height_atr > maximum_pattern_height_atr
pattern_score >= 0.5 and pattern_score < minimum_pattern_score
```

## PENDING

```text
diamond structure is valid
but no directional breakout or breakdown has occurred
```

or:

```text
price crossed boundary but did not exceed ATR buffer
```

## INVALID

```text
liquidity filter fails
spread filter fails
not enough pivots
unconfirmed pivots
pattern duration invalid
no expansion phase
no contraction phase
pattern height too small
boundary construction fails
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
expansion_quality_score: 0.20
contraction_quality_score: 0.20
boundary_quality_score: 0.20
breakout_strength_score: 0.15
volume_confirmation_score: 0.10
liquidity_score: 0.10
displacement_score: 0.05
```

Formula:

```text
pattern_score =
    expansion_quality_score * 0.20
  + contraction_quality_score * 0.20
  + boundary_quality_score * 0.20
  + breakout_strength_score * 0.15
  + volume_confirmation_score * 0.10
  + liquidity_score * 0.10
  + displacement_score * 0.05
```

## Expansion Quality Score

```text
if expansion_high_slope > 0
and expansion_low_slope < 0
and expansion_range_change_atr >= 1.5:
    expansion_quality_score = 1.0

else if expansion_high_slope > 0
and expansion_low_slope < 0
and expansion_range_change_atr >= 1.0:
    expansion_quality_score = 0.7

else:
    expansion_quality_score = 0.0
```

## Contraction Quality Score

```text
if contraction_high_slope < 0
and contraction_low_slope > 0
and contraction_range_change_rate >= 0.35:
    contraction_quality_score = 1.0

else if contraction_high_slope < 0
and contraction_low_slope > 0
and contraction_range_change_rate >= 0.20:
    contraction_quality_score = 0.7

else:
    contraction_quality_score = 0.0
```

## Boundary Quality Score

```text
if upper_boundary_touch_count >= 3
and lower_boundary_touch_count >= 3:
    boundary_quality_score = 1.0

else if upper_boundary_touch_count >= 2
and lower_boundary_touch_count >= 2:
    boundary_quality_score = 0.7

else:
    boundary_quality_score = 0.0
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

If no breakout or breakdown has occurred:

```text
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

## Displacement Score

```text
if displacement breakout is confirmed:
    displacement_score = 1.0

else:
    displacement_score = 0.0
```

If `require_displacement_breakout = false`, absence of displacement does not invalidate the pattern.

## Entry Reference

This module must not execute orders.

It only defines reference prices.

### Bullish Entry Reference

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
entry_reference = upper_boundary retest area
```

### Bearish Entry Reference

Recommended:

```text
entry_reference = breakdown_close
```

Alternative:

```text
entry_reference = next_candle_open
```

Retest-based alternative:

```text
entry_reference = lower_boundary retest area
```

## Stop Reference

### Bullish Stop Reference

Recommended:

```text
stop_reference = lower_boundary_value - breakout_atr_multiplier * ATR
```

Alternative:

```text
stop_reference = nearest_recent_pivot_low
```

### Bearish Stop Reference

Recommended:

```text
stop_reference = upper_boundary_value + breakout_atr_multiplier * ATR
```

Alternative:

```text
stop_reference = nearest_recent_pivot_high
```

## Target Reference

### Bullish Target Reference

Classic measured target:

```text
target_reference = breakout_price + pattern_height
```

Risk-reward fallback:

```text
target_reference = entry_reference + 2 * abs(entry_reference - stop_reference)
```

If nearest resistance zone exists before classic target:

```text
target_reference = nearest_resistance_zone
```

### Bearish Target Reference

Classic measured target:

```text
target_reference = breakdown_price - pattern_height
```

Risk-reward fallback:

```text
target_reference = entry_reference - 2 * abs(stop_reference - entry_reference)
```

If nearest support zone exists before classic target:

```text
target_reference = nearest_support_zone
```

## Risk Reward

### Bullish

```text
risk = entry_reference - stop_reference
reward = target_reference - entry_reference
risk_reward = reward / risk
```

### Bearish

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
  "pattern_type": "DIAMOND_PATTERN",
  "direction": "BULLISH",
  "pattern_status": "VALID",
  "expansion_start_index": 100,
  "diamond_center_index": 140,
  "contraction_end_index": 175,
  "upper_boundary_slope": -22.4,
  "lower_boundary_slope": 18.7,
  "upper_boundary_value": 64600.0,
  "lower_boundary_value": 63100.0,
  "expansion_high_slope": 31.5,
  "expansion_low_slope": -28.2,
  "contraction_high_slope": -22.4,
  "contraction_low_slope": 18.7,
  "expansion_range_change": 2400.0,
  "expansion_range_change_atr": 3.0,
  "contraction_range_change": 1800.0,
  "contraction_range_change_rate": 0.42,
  "pattern_height": 5200.0,
  "pattern_height_atr": 6.5,
  "breakout_index": 180,
  "breakout_price": 64900.0,
  "breakout_distance": 300.0,
  "breakout_distance_atr": 0.375,
  "volume_ratio": 1.8,
  "liquidity_pass": true,
  "spread_pass": true,
  "displacement_confirmed": false,
  "pattern_score": 0.81,
  "entry_reference": 64900.0,
  "stop_reference": 62940.0,
  "target_reference": 70100.0,
  "risk_reward": 2.65,
  "reason": "Bullish Diamond Pattern detected after valid expansion-contraction structure and breakout above upper boundary."
}
```

## Output Fields

### pattern_type

Fixed value:

```text
DIAMOND_PATTERN
```

### direction

One of:

```text
BULLISH
BEARISH
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

### expansion_start_index

Index where the expansion phase begins.

### diamond_center_index

Index around the maximum local range.

### contraction_end_index

Index where the contraction phase ends.

### upper_boundary_slope

Slope of the contraction upper boundary.

### lower_boundary_slope

Slope of the contraction lower boundary.

### upper_boundary_value

Upper boundary value at the breakout evaluation candle.

### lower_boundary_value

Lower boundary value at the breakout evaluation candle.

### expansion_high_slope

Slope of pivot highs during expansion phase.

### expansion_low_slope

Slope of pivot lows during expansion phase.

### contraction_high_slope

Slope of pivot highs during contraction phase.

### contraction_low_slope

Slope of pivot lows during contraction phase.

### expansion_range_change

Increase in local range during expansion phase.

### expansion_range_change_atr

Expansion range change normalized by ATR.

### contraction_range_change

Decrease in local range during contraction phase.

### contraction_range_change_rate

Contraction range decrease divided by contraction start range.

### pattern_height

Maximum vertical height of the diamond.

### pattern_height_atr

Pattern height normalized by ATR.

### breakout_index

Index of breakout or breakdown candle.

### breakout_price

Close price of breakout or breakdown candle.

### breakout_distance

Distance between close and broken boundary.

### breakout_distance_atr

Breakout distance normalized by ATR.

### volume_ratio

Volume ratio of breakout or breakdown candle.

### liquidity_pass

Result from Liquidity module.

### spread_pass

Result from Bid-Ask Spread module.

### displacement_confirmed

Boolean value.

```text
true = breakout candle is valid displacement candle in breakout direction
false = breakout candle is not displacement candle
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

### Not enough pivots

If:

```text
pivot_count < minimum_pivot_count
```

Then:

```text
pattern_status = INVALID
```

### Unconfirmed pivots

If pivots are not confirmed:

```text
ignore pivots
```

### No expansion phase

If expansion high slope and expansion low slope do not diverge:

```text
pattern_status = INVALID
```

Required:

```text
expansion_high_slope > 0
expansion_low_slope < 0
```

### No contraction phase

If contraction high slope and contraction low slope do not converge:

```text
pattern_status = INVALID
```

Required:

```text
contraction_high_slope < 0
contraction_low_slope > 0
```

### Expansion without contraction

If expansion is valid but contraction is not valid:

```text
pattern_status = INVALID
```

### Contraction without prior expansion

If contraction is valid but prior expansion is missing:

```text
pattern_status = INVALID
```

### Pattern duration too short

If:

```text
pattern_duration < minimum_pattern_duration
```

Then:

```text
pattern_status = INVALID
```

### Pattern duration too long

If:

```text
pattern_duration > maximum_pattern_duration
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

### Boundary construction fails

If upper or lower boundary cannot be built:

```text
pattern_status = INVALID
```

### Breakout missing

If no breakout or breakdown occurs:

```text
pattern_status = PENDING
direction = NONE
```

### Breakout without ATR buffer

If price crosses boundary but does not exceed ATR buffer:

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

### Multiple diamond candidates

If multiple candidates exist:

```text
select highest pattern_score
```

Tie-breakers:

```text
1. better contraction quality
2. higher breakout volume_ratio
3. larger breakout_distance_atr
4. more balanced boundary touches
5. more recent breakout
```

### False breakout

Optional post-break check:

```yaml
false_break_check_window: 3
```

Bullish false breakout candidate:

```text
price closes back below upper_boundary within false_break_check_window
```

Bearish false breakout candidate:

```text
price closes back above lower_boundary within false_break_check_window
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
4. Build alternating pivot sequence candidates.
5. Require minimum pivot count.
6. Find diamond center by maximum local range.
7. Split pivots into expansion and contraction phases.
8. Validate expansion phase.
9. Validate contraction phase.
10. Calculate pattern height.
11. Validate pattern duration.
12. Build contraction upper boundary from pivot highs.
13. Build contraction lower boundary from pivot lows.
14. Check bullish breakout above upper boundary.
15. Check bearish breakdown below lower boundary.
16. Apply ATR breakout buffer.
17. Apply volume confirmation.
18. Optionally check displacement breakout.
19. Calculate pattern score.
20. Set pattern status.
21. Return best valid, weak, or pending signal.
```

## Pseudocode

```python
def detect_diamond_pattern(context, config):
    if config.require_liquidity_pass and not context.liquidity.liquidity_pass:
        return invalid_result("liquidity_failed")

    if config.require_spread_pass and not context.spread.spread_pass:
        return invalid_result("spread_failed")

    pivots = merge_and_sort_pivots(
        context.confirmed_pivot_highs,
        context.confirmed_pivot_lows
    )

    candidates = build_diamond_candidates(
        pivots,
        config
    )

    evaluated_candidates = []

    for candidate in candidates:
        evaluated = evaluate_diamond_candidate(
            candidate,
            context,
            config
        )

        if evaluated["pattern_status"] in ["VALID", "WEAK", "PENDING"]:
            evaluated_candidates.append(evaluated)

    if not evaluated_candidates:
        return invalid_result("no_valid_diamond_pattern")

    return select_best_candidate(evaluated_candidates)
```

## Candidate Evaluation

```python
def evaluate_diamond_candidate(candidate, context, config):
    if len(candidate.pivots) < config.minimum_pivot_count:
        return invalid_result("not_enough_pivots")

    duration = candidate.pivots[-1].index - candidate.pivots[0].index

    if duration < config.minimum_pattern_duration:
        return invalid_result("pattern_duration_too_short")

    if duration > config.maximum_pattern_duration:
        return invalid_result("pattern_duration_too_long")

    center = find_diamond_center(candidate.pivots)

    expansion_pivots = get_pivots_before_or_at(candidate.pivots, center)
    contraction_pivots = get_pivots_after_or_at(candidate.pivots, center)

    expansion = evaluate_expansion_phase(
        expansion_pivots,
        context,
        config
    )

    if not expansion["valid"]:
        return invalid_result("invalid_expansion_phase")

    contraction = evaluate_contraction_phase(
        contraction_pivots,
        context,
        config
    )

    if not contraction["valid"]:
        return invalid_result("invalid_contraction_phase")

    boundaries = build_contraction_boundaries(
        contraction_pivots,
        context,
        config
    )

    if not boundaries["valid"]:
        return invalid_result("boundary_construction_failed")

    breakout = evaluate_diamond_breakout(
        boundaries,
        context,
        config
    )

    score = calculate_diamond_score(
        expansion=expansion,
        contraction=contraction,
        boundaries=boundaries,
        breakout=breakout,
        context=context,
        config=config
    )

    status = classify_diamond_status(
        expansion=expansion,
        contraction=contraction,
        boundaries=boundaries,
        breakout=breakout,
        score=score,
        config=config
    )

    return build_diamond_output(
        candidate=candidate,
        center=center,
        expansion=expansion,
        contraction=contraction,
        boundaries=boundaries,
        breakout=breakout,
        score=score,
        status=status,
        context=context,
        config=config
    )
```

## Expansion Phase Evaluation

```python
def evaluate_expansion_phase(expansion_pivots, context, config):
    highs = [p for p in expansion_pivots if p.type == "PIVOT_HIGH"]
    lows = [p for p in expansion_pivots if p.type == "PIVOT_LOW"]

    if len(highs) < 2 or len(lows) < 2:
        return {"valid": False}

    expansion_high_slope = linear_regression_slope(highs)
    expansion_low_slope = linear_regression_slope(lows)

    expansion_start_range = calculate_start_range(expansion_pivots)
    expansion_end_range = calculate_end_range(expansion_pivots)

    expansion_range_change = expansion_end_range - expansion_start_range
    expansion_range_change_atr = expansion_range_change / context.current_atr

    valid = (
        expansion_high_slope > 0
        and expansion_low_slope < 0
        and expansion_range_change_atr >= config.minimum_expansion_range_change_atr
    )

    return {
        "valid": valid,
        "expansion_high_slope": expansion_high_slope,
        "expansion_low_slope": expansion_low_slope,
        "expansion_range_change": expansion_range_change,
        "expansion_range_change_atr": expansion_range_change_atr
    }
```

## Contraction Phase Evaluation

```python
def evaluate_contraction_phase(contraction_pivots, context, config):
    highs = [p for p in contraction_pivots if p.type == "PIVOT_HIGH"]
    lows = [p for p in contraction_pivots if p.type == "PIVOT_LOW"]

    if len(highs) < 2 or len(lows) < 2:
        return {"valid": False}

    contraction_high_slope = linear_regression_slope(highs)
    contraction_low_slope = linear_regression_slope(lows)

    contraction_start_range = calculate_start_range(contraction_pivots)
    contraction_end_range = calculate_end_range(contraction_pivots)

    contraction_range_change = contraction_start_range - contraction_end_range
    contraction_range_change_rate = contraction_range_change / contraction_start_range

    valid = (
        contraction_high_slope < 0
        and contraction_low_slope > 0
        and contraction_range_change_rate >= config.minimum_contraction_range_change_rate
    )

    return {
        "valid": valid,
        "contraction_high_slope": contraction_high_slope,
        "contraction_low_slope": contraction_low_slope,
        "contraction_range_change": contraction_range_change,
        "contraction_range_change_rate": contraction_range_change_rate
    }
```

## Breakout Evaluation

```python
def evaluate_diamond_breakout(boundaries, context, config):
    current = context.current_candle
    atr = context.current_atr
    volume_ratio = context.current_volume_ratio

    upper_value = boundaries["upper_boundary"].value_at(current.index)
    lower_value = boundaries["lower_boundary"].value_at(current.index)

    bullish_break_distance = current.close - upper_value
    bearish_break_distance = lower_value - current.close

    if bullish_break_distance > config.breakout_atr_multiplier * atr:
        direction = "BULLISH"
        breakout_distance = bullish_break_distance
        breakout_distance_atr = breakout_distance / atr

    elif bearish_break_distance > config.breakout_atr_multiplier * atr:
        direction = "BEARISH"
        breakout_distance = bearish_break_distance
        breakout_distance_atr = breakout_distance / atr

    else:
        return {
            "direction": "NONE",
            "status": "PENDING",
            "upper_boundary_value": upper_value,
            "lower_boundary_value": lower_value
        }

    if volume_ratio < config.weak_breakout_volume_ratio:
        status = "INVALID"

    elif volume_ratio < config.minimum_breakout_volume_ratio:
        status = "WEAK"

    else:
        status = "VALID"

    return {
        "direction": direction,
        "status": status,
        "breakout_index": current.index,
        "breakout_price": current.close,
        "breakout_distance": breakout_distance,
        "breakout_distance_atr": breakout_distance_atr,
        "upper_boundary_value": upper_value,
        "lower_boundary_value": lower_value,
        "volume_ratio": volume_ratio
    }
```

## Java-style Domain Model Example

```java
public enum DiamondDirection {
    BULLISH,
    BEARISH,
    NONE
}
```

```java
public enum DiamondPatternStatus {
    VALID,
    WEAK,
    INVALID,
    PENDING
}
```

```java
public record DiamondPatternSignal(
    String symbol,
    Instant timestamp,
    String patternType,
    DiamondDirection direction,
    DiamondPatternStatus patternStatus,
    int expansionStartIndex,
    int diamondCenterIndex,
    int contractionEndIndex,
    BigDecimal upperBoundarySlope,
    BigDecimal lowerBoundarySlope,
    BigDecimal upperBoundaryValue,
    BigDecimal lowerBoundaryValue,
    BigDecimal expansionHighSlope,
    BigDecimal expansionLowSlope,
    BigDecimal contractionHighSlope,
    BigDecimal contractionLowSlope,
    BigDecimal expansionRangeChange,
    BigDecimal expansionRangeChangeAtr,
    BigDecimal contractionRangeChange,
    BigDecimal contractionRangeChangeRate,
    BigDecimal patternHeight,
    BigDecimal patternHeightAtr,
    int breakoutIndex,
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
diamond_pattern:
  minimum_pivot_count: 6
  maximum_pivot_count: 10
  minimum_pattern_duration: 20
  maximum_pattern_duration: 200
  minimum_expansion_range_change_atr: 1.0
  minimum_contraction_range_change_rate: 0.20
  minimum_pattern_height_atr: 1.0
  maximum_pattern_height_atr: 8.0
  maximum_boundary_touch_deviation_atr: 0.5
  breakout_atr_multiplier: 0.2
  minimum_breakout_volume_ratio: 1.5
  weak_breakout_volume_ratio: 1.3
  require_liquidity_pass: true
  require_spread_pass: true
  require_displacement_breakout: false
  minimum_pattern_score: 0.7
```

## Final Mechanical Rule

```text
Diamond Pattern:
1. Use confirmed pivot highs and pivot lows.
2. Require at least 6 pivots.
3. Find diamond center where local pivot range is maximum.
4. Split pivots into expansion phase and contraction phase.
5. Expansion phase requires rising pivot highs and falling pivot lows.
6. Contraction phase requires falling pivot highs and rising pivot lows.
7. Require expansion_range_change_atr >= 1.0.
8. Require contraction_range_change_rate >= 0.20.
9. Build upper boundary from contraction pivot highs.
10. Build lower boundary from contraction pivot lows.
11. Bullish breakout requires close > upper_boundary_value + 0.2 * ATR.
12. Bearish breakdown requires close < lower_boundary_value - 0.2 * ATR.
13. Require breakout volume_ratio >= 1.5.
14. Require liquidity_pass = true.
15. Require spread_pass = true.
```
