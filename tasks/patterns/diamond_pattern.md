# Diamond Pattern Mechanical Definition

## Purpose

Define the Diamond Pattern mechanically.

This module detects a volatility expansion-contraction structure built from confirmed pivots and determines direction only after a breakout or breakdown.

This document defines detection logic only.
It does not define order execution.

## Pattern Type

```text
Diamond Pattern
DIAMOND
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
diamond_pattern:
  minimum_pivot_count: 6
  maximum_pivot_count: 10
  minimum_pattern_duration: 12
  maximum_pattern_duration: 200
  minimum_pattern_height_atr: 1.0
  maximum_pattern_height_atr: 8.0
  breakout_atr_multiplier: 0.2
  minimum_breakout_volume_ratio: 1.5
  weak_breakout_volume_ratio: 1.3
  require_liquidity_pass: true
  require_spread_pass: true
  require_displacement_breakout: false
  minimum_pattern_score: 0.7
  weak_pattern_score: 0.5
  false_breakout_check_window: 3
  default_risk_reward: 2.0
```

## Core Concept

A Diamond Pattern has two phases:

```text
1. Expansion phase: pivot highs rise, pivot lows fall, and range expands.
2. Contraction phase: pivot highs fall, pivot lows rise, and range contracts.
```

The module must not assign bullish or bearish direction before breakout.

Before breakout:

```text
direction = NONE
pattern_status = PENDING
```

After breakout or breakdown:

```text
BULLISH = close breaks above contracting upper boundary with ATR buffer
BEARISH = close breaks below contracting lower boundary with ATR buffer
```

## Pivot Structure

Use confirmed pivots only.

Minimum pivot count:

```text
minimum_pivot_count = 6
```

Recommended pivot count:

```text
6 to 10 pivots
```

The pivot sequence should include at least:

```text
pivot high 1
pivot low 1
pivot high 2
pivot low 2
pivot high 3
pivot low 3
```

The exact high/low order may vary, but the accepted sequence must contain both pivot highs and pivot lows and must show early expansion followed by later contraction.

If fewer than `minimum_pivot_count` confirmed pivots exist:

```text
pattern_status = INVALID
reason = NOT_ENOUGH_PIVOTS
```

Unconfirmed pivots:

```text
ignore pivot
```

## Alternating Pivot Validation

The candidate should alternate between pivot highs and pivot lows often enough to represent a boundary pattern.

Recommended initial rule:

```text
alternating_transition_count >= minimum_pivot_count - 2
```

Where:

```text
alternating_transition_count = count of adjacent selected pivots where pivot_type changes
```

If alternation is weak:

```text
pattern_status = WEAK or INVALID
```

Recommended initial handling:

```text
weak alternation = INVALID
```

## Diamond Center

The diamond center separates expansion and contraction phases.

Possible methods:

```text
middle pivot index
maximum range pivot pair
largest high-low spread point
```

Recommended initial version:

```text
diamond_center = point where local pivot range is maximum
```

For each candidate center, calculate a local pivot range from the nearest confirmed pivot high and nearest confirmed pivot low around the same window:

```text
local_pivot_range = local_pivot_high.price - local_pivot_low.price
```

Select:

```text
diamond_center = pivot index or midpoint index of the maximum local_pivot_range
```

Split selected pivots into:

```text
expansion_pivots = pivots at or before diamond_center
contraction_pivots = pivots at or after diamond_center
```

Both phases must contain at least one pivot high and one pivot low.

## Expansion Phase

Expansion phase must show widening volatility.

Use pivot highs in the expansion phase to calculate:

```text
expansion_high_slope = slope of expansion pivot highs by index
```

Use pivot lows in the expansion phase to calculate:

```text
expansion_low_slope = slope of expansion pivot lows by index
```

Calculate expansion range change:

```text
expansion_range_start = early_expansion_high.price - early_expansion_low.price
expansion_range_end = late_expansion_high.price - late_expansion_low.price
expansion_range_change = expansion_range_end - expansion_range_start
```

Expected signs:

```text
expansion_high_slope > 0
expansion_low_slope < 0
expansion_range_change > 0
```

Equivalent pivot conditions:

```text
later pivot high > earlier pivot high
later pivot low < earlier pivot low
expansion_range_end > expansion_range_start
```

If expansion is not clear:

```text
pattern_status = INVALID
reason = NO_CLEAR_EXPANSION_PHASE
```

## Contraction Phase

Contraction phase must show narrowing volatility.

Use pivot highs in the contraction phase to calculate:

```text
contraction_high_slope = slope of contraction pivot highs by index
```

Use pivot lows in the contraction phase to calculate:

```text
contraction_low_slope = slope of contraction pivot lows by index
```

Calculate contraction range change:

```text
contraction_range_start = early_contraction_high.price - early_contraction_low.price
contraction_range_end = late_contraction_high.price - late_contraction_low.price
contraction_range_change = contraction_range_end - contraction_range_start
```

Expected signs:

```text
contraction_high_slope < 0
contraction_low_slope > 0
contraction_range_change < 0
```

Equivalent pivot conditions:

```text
later pivot high < earlier pivot high
later pivot low > earlier pivot low
contraction_range_end < contraction_range_start
```

If contraction is not clear:

```text
pattern_status = INVALID
reason = NO_CLEAR_CONTRACTION_PHASE
```

## Boundary Construction

Upper boundaries are built from pivot highs.

Lower boundaries are built from pivot lows.

Expansion boundaries:

```text
expanding_upper_boundary = line fitted to expansion pivot highs
expanding_lower_boundary = line fitted to expansion pivot lows
```

Contraction boundaries:

```text
contracting_upper_boundary = line fitted to contraction pivot highs
contracting_lower_boundary = line fitted to contraction pivot lows
```

Recommended initial fitting method:

```text
Use two-point line from earliest and latest confirmed pivots in that phase.
```

Line formula:

```text
slope = (point_2.price - point_1.price) / (point_2.index - point_1.index)
intercept = point_1.price - slope * point_1.index
boundary_value[index] = slope * index + intercept
```

For breakout validation, use latest contraction boundaries:

```text
upper_boundary_value = contracting_upper_boundary.value_at(breakout.index)
lower_boundary_value = contracting_lower_boundary.value_at(breakout.index)
```

Boundary sign expectations:

```text
contracting_upper_boundary.slope < 0
contracting_lower_boundary.slope > 0
```

If a contraction boundary is flat or has the wrong sign:

```text
pattern_status = INVALID
```

## Pattern Duration

```text
pattern_duration = contraction_end_index - expansion_start_index
```

Valid duration:

```text
minimum_pattern_duration <= pattern_duration <= maximum_pattern_duration
```

Default:

```text
minimum_pattern_duration = 12
maximum_pattern_duration = 200
```

## Pattern Height

Pattern height is measured at the widest part of the diamond.

```text
pattern_height = maximum local_pivot_range
pattern_height_atr = pattern_height / ATR[diamond_center_index]
```

Valid range:

```text
minimum_pattern_height_atr <= pattern_height_atr <= maximum_pattern_height_atr
```

Default:

```text
minimum_pattern_height_atr = 1.0
maximum_pattern_height_atr = 8.0
```

If height is too small or too large:

```text
pattern_status = INVALID
```

## Breakout and Breakdown Validation

### Bullish Breakout

```text
close > upper_boundary_value + breakout_atr_multiplier * ATR
```

Direction:

```text
direction = BULLISH
```

Breakout distance:

```text
breakout_distance = close - upper_boundary_value
breakout_distance_atr = breakout_distance / ATR
```

### Bearish Breakdown

```text
close < lower_boundary_value - breakout_atr_multiplier * ATR
```

Direction:

```text
direction = BEARISH
```

Breakout distance:

```text
breakout_distance = lower_boundary_value - close
breakout_distance_atr = breakout_distance / ATR
```

Default:

```text
breakout_atr_multiplier = 0.2
```

If no boundary break exists:

```text
direction = NONE
pattern_status = PENDING
```

If price crosses a boundary but does not exceed the ATR buffer:

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

If volume ratio is missing:

```text
pattern_status = INVALID
```

If volume is weak:

```text
pattern_status = WEAK
```

If volume is below weak threshold:

```text
pattern_status = INVALID
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

Recommended initial version:

```text
require_displacement_breakout = false
```

Bullish breakout displacement:

```text
displacement_direction = BULLISH
displacement_status = VALID
```

Bearish breakdown displacement:

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
displacement_confirmed affects displacement_score only
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
minimum pivot count satisfied
alternating pivot structure valid
clear expansion phase exists
clear contraction phase exists
pattern duration valid
pattern height valid
breakout or breakdown clears ATR buffer
volume_ratio >= minimum_breakout_volume_ratio
pattern_score >= minimum_pattern_score
```

### WEAK

```text
valid diamond structure exists
but volume confirmation is weak
```

or:

```text
pattern_score >= weak_pattern_score
and
pattern_score < minimum_pattern_score
```

### PENDING

```text
valid expansion-contraction structure exists
but breakout or breakdown is missing
```

or:

```text
price crosses a boundary without ATR buffer confirmation
```

### INVALID

```text
liquidity filter fails
spread filter fails
not enough pivots
unconfirmed pivots only
no clear expansion phase
no clear contraction phase
expansion without contraction
contraction without prior expansion
flat or invalid contraction boundary
pattern duration invalid
pattern height invalid
volume ratio missing
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
boundary_quality_score: 0.15
breakout_strength_score: 0.20
volume_confirmation_score: 0.15
liquidity_score: 0.05
displacement_score: 0.03
support_resistance_context_score: 0.02
```

Formula:

```text
pattern_score =
    expansion_quality_score * 0.20
  + contraction_quality_score * 0.20
  + boundary_quality_score * 0.15
  + breakout_strength_score * 0.20
  + volume_confirmation_score * 0.15
  + liquidity_score * 0.05
  + displacement_score * 0.03
  + support_resistance_context_score * 0.02
```

## Score Components

### Expansion Quality Score

```text
if expansion_high_slope > 0 and expansion_low_slope < 0 and expansion_range_change > 0:
    expansion_quality_score = 1.0
else:
    expansion_quality_score = 0.0
```

### Contraction Quality Score

```text
if contraction_high_slope < 0 and contraction_low_slope > 0 and contraction_range_change < 0:
    contraction_quality_score = 1.0
else:
    contraction_quality_score = 0.0
```

### Boundary Quality Score

```text
if contracting_upper_boundary.slope < 0 and contracting_lower_boundary.slope > 0:
    boundary_quality_score = 1.0
else:
    boundary_quality_score = 0.0
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

### Displacement Score

```text
if breakout or breakdown candle displacement direction matches pattern direction:
    displacement_score = 1.0
else:
    displacement_score = 0.0
```

### Support / Resistance Context Score

Bullish:

```text
if breakout occurs above or near resistance zone:
    support_resistance_context_score = 0.7
else:
    support_resistance_context_score = 0.5
```

Bearish:

```text
if breakdown occurs below or near support zone:
    support_resistance_context_score = 0.7
else:
    support_resistance_context_score = 0.5
```

## Entry Reference

This module must not execute orders.

Bullish:

```text
entry_reference = breakout close or next candle open
```

Bearish:

```text
entry_reference = breakdown close or next candle open
```

## Stop Reference

Bullish:

```text
stop_reference = lower contraction boundary value or nearest swing low
```

Bearish:

```text
stop_reference = upper contraction boundary value or nearest swing high
```

If stop reference creates non-positive risk:

```text
pattern_status = INVALID
risk_reward = null
```

## Target Reference

Bullish measured target:

```text
target_reference = breakout_price + pattern_height
```

Bearish measured target:

```text
target_reference = breakout_price - pattern_height
```

Risk-reward fallback:

```text
BULLISH: target_reference = entry_reference + 2 * abs(entry_reference - stop_reference)
BEARISH: target_reference = entry_reference - 2 * abs(entry_reference - stop_reference)
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
  "pattern_type": "DIAMOND",
  "direction": "BULLISH",
  "pattern_status": "VALID",
  "expansion_start_index": 100,
  "diamond_center_index": 132,
  "contraction_end_index": 164,
  "upper_boundary_slope": -18.5,
  "lower_boundary_slope": 16.2,
  "upper_boundary_value": 65200.0,
  "lower_boundary_value": 62600.0,
  "expansion_range_change": 4200.0,
  "contraction_range_change": -3100.0,
  "pattern_height": 5400.0,
  "pattern_height_atr": 4.5,
  "breakout_index": 170,
  "breakout_price": 65600.0,
  "breakout_distance": 400.0,
  "breakout_distance_atr": 0.33,
  "volume_ratio": 1.8,
  "liquidity_pass": true,
  "spread_pass": true,
  "displacement_confirmed": false,
  "pattern_score": 0.81,
  "entry_reference": 65600.0,
  "stop_reference": 62600.0,
  "target_reference": 71000.0,
  "risk_reward": 1.8,
  "reason": "Bullish Diamond breakout detected after valid expansion-contraction structure with ATR buffer and volume confirmation."
}
```

## Output Fields

- `pattern_type`: fixed value `DIAMOND`.
- `direction`: `BULLISH`, `BEARISH`, or `NONE`.
- `pattern_status`: `VALID`, `WEAK`, `INVALID`, or `PENDING`.
- `expansion_start_index`: first selected pivot/candle index of the expansion phase.
- `diamond_center_index`: index where local pivot range is maximum.
- `contraction_end_index`: final selected pivot/candle index of the contraction phase.
- `upper_boundary_slope`: slope of latest contraction upper boundary.
- `lower_boundary_slope`: slope of latest contraction lower boundary.
- `upper_boundary_value`: upper boundary value at breakout index.
- `lower_boundary_value`: lower boundary value at breakout index.
- `expansion_range_change`: expansion range end minus expansion range start.
- `contraction_range_change`: contraction range end minus contraction range start.
- `pattern_height`: maximum local pivot range.
- `pattern_height_atr`: pattern height normalized by ATR.
- `breakout_index`: breakout or breakdown candle index.
- `breakout_price`: close price of breakout or breakdown candle.
- `breakout_distance`: absolute distance from broken boundary.
- `breakout_distance_atr`: breakout distance normalized by ATR.
- `volume_ratio`: volume ratio at breakout or breakdown candle.
- `liquidity_pass`: result from Liquidity module.
- `spread_pass`: result from Bid-Ask Spread module.
- `displacement_confirmed`: true when optional displacement confirmation matches direction.
- `pattern_score`: final score between `0.0` and `1.0`.
- `entry_reference`: reference price for possible entry.
- `stop_reference`: reference price for invalidation.
- `target_reference`: reference price for possible target.
- `risk_reward`: reward-to-risk ratio.
- `reason`: short explanation for detection result.

## Edge Cases

### Not Enough Pivots

If fewer than `minimum_pivot_count` confirmed pivots exist:

```text
pattern_status = INVALID
```

### Unconfirmed Pivots

Unconfirmed pivots are ignored.

### No Clear Expansion Phase

If expansion slopes or range change do not satisfy expected signs:

```text
pattern_status = INVALID
```

### No Clear Contraction Phase

If contraction slopes or range change do not satisfy expected signs:

```text
pattern_status = INVALID
```

### Expansion Without Contraction

If expansion exists but no valid contraction phase follows:

```text
pattern_status = INVALID
```

### Contraction Without Prior Expansion

If contraction exists but no valid earlier expansion phase exists:

```text
pattern_status = INVALID
```

### Flat Upper Boundary

If contraction upper boundary is flat or not downward sloping:

```text
pattern_status = INVALID
```

### Flat Lower Boundary

If contraction lower boundary is flat or not upward sloping:

```text
pattern_status = INVALID
```

### Overlapping Diamond Candidates

If multiple valid candidates overlap:

```text
select highest pattern_score
```

Tie-breakers:

```text
1. stronger breakout volume_ratio
2. larger breakout_distance_atr
3. better expansion and contraction quality
4. cleaner boundary slopes
5. more recent breakout
```

### Pattern Duration Too Short Or Too Long

If pattern duration is outside configured limits:

```text
pattern_status = INVALID
```

### Pattern Height Too Small Or Too Large

If pattern height normalized by ATR is outside configured limits:

```text
pattern_status = INVALID
```

### Breakout Missing

If a valid diamond structure exists but neither boundary is broken:

```text
pattern_status = PENDING
```

### Breakout Without ATR Buffer

If price crosses a boundary but does not exceed ATR buffer:

```text
pattern_status = PENDING
```

### Breakout Without Volume Confirmation

If volume is weak:

```text
pattern_status = WEAK
```

If volume is below weak threshold:

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

### False Breakout

If price breaks a boundary and then closes back inside the contraction boundaries within `false_breakout_check_window` candles:

```text
mark as FALSE_BREAKOUT_CANDIDATE
```

### Conflicting Swing Structure

If Swing Structure conflicts with breakout direction:

```text
reduce score
```

Do not invalidate by default.

### Diamond Inside Major Support Or Resistance Zone

If the diamond forms inside a major support or resistance zone:

```text
record support_resistance_context
adjust support_resistance_context_score
```

## Detection Logic

```text
1. Check liquidity_pass.
2. Check spread_pass.
3. Load confirmed pivot highs and confirmed pivot lows.
4. Build candidate pivot sequences with 6 to 10 pivots.
5. Validate alternating pivot structure.
6. Find diamond_center where local pivot range is maximum.
7. Split pivots into expansion and contraction phases.
8. Validate expansion phase slopes and range change.
9. Validate contraction phase slopes and range change.
10. Build contraction upper and lower boundaries.
11. Validate boundary slopes.
12. Validate pattern duration and pattern height.
13. Evaluate bullish breakout above upper boundary with ATR buffer.
14. Evaluate bearish breakdown below lower boundary with ATR buffer.
15. Apply volume confirmation.
16. Optionally apply displacement confirmation.
17. Calculate score.
18. Define entry, stop, target, and risk/reward references.
19. Return best VALID, WEAK, PENDING, or INVALID result.
```

## Pseudocode

```python
def detect_diamond_pattern(context, config):
    if config.require_liquidity_pass and not context.liquidity.liquidity_pass:
        return invalid_result("liquidity_failed")

    if config.require_spread_pass and not context.spread.spread_pass:
        return invalid_result("spread_failed")

    pivots = merge_and_sort_confirmed_pivots(
        context.confirmed_pivot_highs,
        context.confirmed_pivot_lows,
    )

    if len(pivots) < config.minimum_pivot_count:
        return invalid_result("not_enough_pivots")

    candidates = []

    for pivot_window in rolling_pivot_windows(
        pivots,
        min_size=config.minimum_pivot_count,
        max_size=config.maximum_pivot_count,
    ):
        if not has_valid_alternation(pivot_window, config):
            continue

        center = find_max_local_pivot_range_center(pivot_window)
        expansion, contraction = split_by_center(pivot_window, center)

        if not validate_expansion(expansion):
            continue

        if not validate_contraction(contraction):
            continue

        boundaries = build_contraction_boundaries(contraction)

        if not validate_boundaries(boundaries):
            continue

        breakout_result = evaluate_breakout_or_breakdown(
            boundaries,
            context,
            config,
        )

        candidate = build_diamond_output(
            pivot_window=pivot_window,
            center=center,
            boundaries=boundaries,
            breakout_result=breakout_result,
            context=context,
            config=config,
        )

        candidates.append(candidate)

    return select_best_candidate(candidates)
```

## Final Mechanical Rule

```text
Diamond Pattern:
1. Use confirmed pivots only.
2. Require at least 6 pivots.
3. Require early expansion: pivot highs rise, pivot lows fall, and range expands.
4. Require later contraction: pivot highs fall, pivot lows rise, and range contracts.
5. Set diamond_center to the maximum local pivot range point.
6. Build contraction upper boundary from contraction pivot highs.
7. Build contraction lower boundary from contraction pivot lows.
8. For bullish breakout, require close > upper_boundary_value + 0.2 * ATR.
9. For bearish breakdown, require close < lower_boundary_value - 0.2 * ATR.
10. Require breakout or breakdown volume_ratio >= 1.5 for VALID, or >= 1.3 for WEAK.
11. Require liquidity_pass = true.
12. Require spread_pass = true.
13. Define entry, stop, and target references only; do not execute orders.
```
