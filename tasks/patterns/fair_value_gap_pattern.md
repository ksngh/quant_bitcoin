# Fair Value Gap Pattern Mechanical Definition

## Purpose

Define the Fair Value Gap Pattern mechanically.

This pattern identifies a three-candle price imbalance where the first and third
candles do not overlap in the impulse direction. The resulting gap is a
potential continuation or reversion reaction zone. This document defines
detection logic only. It does not define order execution, position sizing,
exchange integration, backtesting engine behavior, live order placement, machine
learning, UI visualization, or manual chart drawing.

## Pattern Type

```text
FAIR_VALUE_GAP
FVG
```

Human-readable name:

```text
Fair Value Gap Pattern
```

## Pattern Categories

```text
Price Imbalance
Inefficient Price Delivery
Three-Candle Gap Structure
Continuation or Reversion Zone
```

## Supported Directions

```text
BULLISH
BEARISH
NONE
```

## Required Core Modules

The pattern must reuse snapshots produced by these core modules:

```text
Liquidity: Trading Value / Volume
Bid-Ask Spread
ATR
Volume Ratio
Displacement Candle
Swing Structure
Support / Resistance Zone
```

Optional core modules:

```text
Pivot High / Pivot Low
```

The pattern module must not recalculate these indicators internally except for
simple comparisons against already-provided snapshot fields.

## Required Inputs

```text
symbol
timestamp
OHLCV candles
ATR values
volume ratio values
displacement candle snapshots
swing structure snapshots
support / resistance zones
liquidity status
bid-ask spread status
```

Optional inputs:

```text
confirmed pivot highs
confirmed pivot lows
```

Required candle fields:

```text
open
high
low
close
volume
timestamp
index
```

## Default Parameters

```yaml
fair_value_gap:
  minimum_gap_size_atr_multiplier: 0.1
  maximum_gap_size_atr_multiplier: 2.0
  require_displacement_candle: true
  minimum_volume_ratio: 1.3
  strong_volume_ratio: 1.5
  require_liquidity_pass: true
  require_spread_pass: true
  near_support_resistance_atr_multiplier: 0.5
  broken_atr_buffer_multiplier: 0.2
  stop_atr_buffer_multiplier: 0.2
  minimum_pattern_score: 0.7
  weak_pattern_score: 0.5
  default_entry_reference: ZONE_MID
  default_risk_reward: 2.0
  large_gap_handling: WEAK
```

## Core Definitions

### Three-Candle Window

An FVG is evaluated using exactly three consecutive candles:

```text
candle_1 = candles[i - 2]
candle_2 = candles[i - 1]
candle_3 = candles[i]
middle_candle = candle_2
```

The middle candle is used for displacement and volume confirmation. The pattern
is created at `candle_3.timestamp` only after Candle 3 is closed.

If fewer than three consecutive candles are available:

```text
pattern_status = INVALID
fvg_state = INVALID
direction = NONE
reason = NOT_ENOUGH_CANDLES
```

### Bullish FVG

A bullish FVG exists when Candle 1 high is lower than Candle 3 low:

```text
candle_1.high < candle_3.low
```

Gap size:

```text
gap_size = candle_3.low - candle_1.high
```

Zone boundaries:

```text
zone_low = candle_1.high
zone_high = candle_3.low
zone_mid = (zone_low + zone_high) / 2
```

Preferred displacement confirmation:

```text
displacement_direction = BULLISH
displacement_status = VALID
```

The zone is a potential bullish reaction zone.

### Bearish FVG

A bearish FVG exists when Candle 1 low is higher than Candle 3 high:

```text
candle_1.low > candle_3.high
```

Gap size:

```text
gap_size = candle_1.low - candle_3.high
```

Zone boundaries:

```text
zone_low = candle_3.high
zone_high = candle_1.low
zone_mid = (zone_low + zone_high) / 2
```

Preferred displacement confirmation:

```text
displacement_direction = BEARISH
displacement_status = VALID
```

The zone is a potential bearish reaction zone.

## Detection Sequence

For each closed candle index `i`:

```text
1. Select exactly candle_1, candle_2, and candle_3.
2. Reject the window if required OHLC fields are missing.
3. Require liquidity_pass = true when require_liquidity_pass = true.
4. Require spread_pass = true when require_spread_pass = true.
5. Check bullish structure: candle_1.high < candle_3.low.
6. Check bearish structure: candle_1.low > candle_3.high.
7. If neither structure exists, return direction = NONE and pattern_status = INVALID.
8. Calculate zone_low, zone_high, zone_mid, gap_size, and gap_size_atr.
9. Validate gap size using ATR.
10. Validate Candle 2 with the Displacement Candle snapshot.
11. Confirm volume using Candle 2 Volume Ratio snapshot.
12. Add Swing Structure and Support / Resistance context.
13. Calculate state, fill_ratio, pattern_score, and reference levels.
```

If both bullish and bearish structure appear due to malformed candle data, reject
the window:

```text
pattern_status = INVALID
fvg_state = INVALID
direction = NONE
reason = CONFLICTING_FVG_DIRECTION
```

## Liquidity and Spread Filters

Before validating the pattern:

```text
liquidity_pass = true
spread_pass = true
```

If `require_liquidity_pass = true` and the Liquidity snapshot fails:

```text
pattern_status = INVALID
fvg_state = INVALID
reason = LIQUIDITY_FILTER_FAILED
```

If `require_spread_pass = true` and the Bid-Ask Spread snapshot fails:

```text
pattern_status = INVALID
fvg_state = INVALID
reason = SPREAD_FILTER_FAILED
```

Low liquidity or wide spread can indicate an illiquid price jump rather than a
valid inefficiency. These failures are hard invalidations in the initial version.

## ATR Gap Size Validation

Use the ATR snapshot aligned to Candle 3 unless a project-level consumer
explicitly provides another evaluation timestamp.

```text
gap_size_atr = gap_size / ATR
```

Minimum valid gap:

```text
gap_size >= minimum_gap_size_atr_multiplier * ATR
```

Maximum valid gap:

```text
gap_size <= maximum_gap_size_atr_multiplier * ATR
```

Default thresholds:

```text
minimum_gap_size_atr_multiplier = 0.1
maximum_gap_size_atr_multiplier = 2.0
```

If ATR is missing, non-positive, or invalid:

```text
pattern_status = INVALID
fvg_state = INVALID
reason = ATR_UNAVAILABLE
```

If the gap is too small:

```text
pattern_status = INVALID
fvg_state = INVALID
reason = GAP_TOO_SMALL
```

If the gap is too large and `large_gap_handling = WEAK`:

```text
pattern_status = WEAK
reason includes GAP_TOO_LARGE
```

If the gap is too large and `large_gap_handling = INVALID`:

```text
pattern_status = INVALID
fvg_state = INVALID
reason = GAP_TOO_LARGE
```

## Displacement Validation

The middle candle is validated using the Displacement Candle snapshot aligned to
`candle_2`.

Initial version default:

```text
require_displacement_candle = true
```

Bullish FVG displacement requirement:

```text
candle_2 displacement_direction = BULLISH
candle_2 displacement_status = VALID
```

Bearish FVG displacement requirement:

```text
candle_2 displacement_direction = BEARISH
candle_2 displacement_status = VALID
```

If displacement is required and Candle 2 does not satisfy the directional
requirement:

```text
pattern_status = INVALID
fvg_state = INVALID
reason = DISPLACEMENT_NOT_CONFIRMED
```

If displacement is not required, the FVG can still be detected, but
`displacement_score` is reduced and `pattern_status` cannot be stronger than
`WEAK` unless other project-level rules override this in a future task.

## Volume Confirmation

Use the Volume Ratio snapshot aligned to Candle 2.

Default confirmation:

```text
candle_2.volume_ratio >= minimum_volume_ratio
minimum_volume_ratio = 1.3
```

Strong confirmation:

```text
volume_ratio >= strong_volume_ratio
strong_volume_ratio = 1.5
```

If volume ratio is missing:

```text
volume_confirmation_score = 0.0
reason includes VOLUME_RATIO_UNAVAILABLE
```

If `candle_2.volume_ratio < minimum_volume_ratio`:

```text
pattern_status = WEAK
reason includes VOLUME_CONFIRMATION_FAILED
```

Volume confirmation alone must not override failed liquidity or spread filters.

## FVG State

Allowed values:

```text
FRESH
TOUCHED
PARTIALLY_FILLED
FILLED
BROKEN
INVALID
```

State is evaluated using candles after Candle 3:

```text
later_candles = candles where index > candle_3.index
```

### Fresh

A bullish FVG is fresh when no later candle has returned to the zone:

```text
no later candle has low <= zone_high
```

A bearish FVG is fresh when no later candle has returned to the zone:

```text
no later candle has high >= zone_low
```

### Touched

A bullish FVG is touched when a later candle overlaps the zone:

```text
later_candle.low <= zone_high
and
later_candle.high >= zone_low
```

A bearish FVG is touched when a later candle overlaps the zone:

```text
later_candle.high >= zone_low
and
later_candle.low <= zone_high
```

`TOUCHED` is an event label. The persistent state should be
`PARTIALLY_FILLED`, `FILLED`, or `BROKEN` when the fill-ratio or broken rules are
satisfied.

### Partially Filled

A bullish FVG is partially filled when price enters the gap but does not fully
fill it:

```text
later_candle.low < zone_high
and
later_candle.low > zone_low
```

A bearish FVG is partially filled when price enters the gap but does not fully
fill it:

```text
later_candle.high > zone_low
and
later_candle.high < zone_high
```

### Filled

A bullish FVG is filled when:

```text
later_candle.low <= zone_low
```

A bearish FVG is filled when:

```text
later_candle.high >= zone_high
```

Initial version interpretation:

```text
filled FVG = FILLED
not tradable as fresh imbalance
```

A filled FVG is not automatically `BROKEN`.

### Broken

A bullish FVG is broken when a later close moves below the zone by an ATR buffer:

```text
later_candle.close < zone_low - (broken_atr_buffer_multiplier * ATR)
```

A bearish FVG is broken when a later close moves above the zone by an ATR buffer:

```text
later_candle.close > zone_high + (broken_atr_buffer_multiplier * ATR)
```

Default:

```text
broken_atr_buffer_multiplier = 0.2
```

Broken state takes precedence over fresh, touched, partially filled, and filled.

## Fill Ratio

For bullish FVGs, use the lowest later price that enters the zone:

```text
lowest_price_inside_zone = minimum later low clipped to [zone_low, zone_high]
fill_ratio = (zone_high - lowest_price_inside_zone) / gap_size
```

For bearish FVGs, use the highest later price that enters the zone:

```text
highest_price_inside_zone = maximum later high clipped to [zone_low, zone_high]
fill_ratio = (highest_price_inside_zone - zone_low) / gap_size
```

Clamp:

```text
fill_ratio = max(0.0, min(fill_ratio, 1.0))
```

State mapping before applying the broken rule:

```text
fill_ratio = 0.0 -> FRESH
0.0 < fill_ratio < 1.0 -> PARTIALLY_FILLED
fill_ratio >= 1.0 -> FILLED
```

If a later candle overlaps the zone but the calculated fill ratio remains `0.0`
due to boundary equality, the event may be recorded as `TOUCHED` while the
persistent state remains `FRESH`.

## Swing Structure Context

Use the Swing Structure snapshot aligned to Candle 3 or the latest confirmed
snapshot before Candle 3.

Bullish FVG is stronger when:

```text
market_structure_status = UPTREND
or
market_structure_status = TRANSITION from DOWNTREND to UPTREND
```

Bearish FVG is stronger when:

```text
market_structure_status = DOWNTREND
or
market_structure_status = TRANSITION from UPTREND to DOWNTREND
```

If structure conflicts with FVG direction:

```text
structure_alignment_score is reduced
reason includes CONFLICTING_SWING_STRUCTURE
```

If structure is missing or unknown:

```text
structure_alignment_score = neutral value
reason includes STRUCTURE_CONTEXT_UNAVAILABLE
```

Optional confirmed pivot highs and confirmed pivot lows may be used only as
context already produced by the Pivot High / Pivot Low module. They must not be
used to redefine the three-candle FVG structure.

## Support / Resistance Context

Use Support / Resistance Zone snapshots available at Candle 3 or the latest
confirmed snapshot before Candle 3.

Bullish FVG is stronger when:

```text
FVG zone overlaps a support zone
or
FVG zone is near a support zone
```

Bearish FVG is stronger when:

```text
FVG zone overlaps a resistance zone
or
FVG zone is near a resistance zone
```

Overlap condition:

```text
fvg.zone_low <= sr.zone_high
and
fvg.zone_high >= sr.zone_low
```

Near condition:

```text
distance_to_zone <= near_support_resistance_atr_multiplier * ATR
near_support_resistance_atr_multiplier = 0.5
```

A bullish FVG inside or near major resistance receives reduced context score. A
bearish FVG inside or near major support receives reduced context score. A mixed
support/resistance zone is neutral unless project-level rules classify it as
supportive or conflicting.

## Pattern Status

Allowed values:

```text
VALID
WEAK
INVALID
PENDING
```

Default status mapping:

```text
INVALID: hard validation failed, state invalid, or required data is missing
PENDING: three-candle structure exists but later confirmation data is not closed or available
WEAK: structure exists but non-hard confirmations are weak or conflicting
VALID: structure exists and hard filters, size, displacement, and score pass
```

A fresh or partially filled FVG can be `VALID` or `WEAK`. A filled FVG remains a
valid historical detection but is not tradable as a fresh imbalance. A broken FVG
should not produce fresh-entry references except for historical analysis fields.

## Pattern Scoring

`pattern_score` is normalized from `0.0` to `1.0`.

Required score components:

```text
gap_quality_score
displacement_score
volume_confirmation_score
structure_alignment_score
support_resistance_context_score
liquidity_score
freshness_score
```

Recommended default weights:

```yaml
gap_quality_score: 0.20
displacement_score: 0.20
volume_confirmation_score: 0.15
structure_alignment_score: 0.15
support_resistance_context_score: 0.15
liquidity_score: 0.10
freshness_score: 0.05
```

Weighted score:

```text
pattern_score = sum(component_score * component_weight)
pattern_score = max(0.0, min(pattern_score, 1.0))
```

Component guidance:

```text
gap_quality_score = 1.0 when gap_size_atr is inside preferred range and not too large
                  = 0.0 when gap is below minimum
                  = reduced when gap exceeds maximum and large_gap_handling = WEAK

displacement_score = 1.0 when directional displacement is valid
                   = 0.0 when required displacement fails
                   = reduced when displacement is optional and absent

volume_confirmation_score = 1.0 when volume_ratio >= strong_volume_ratio
                          = 0.7 when minimum_volume_ratio <= volume_ratio < strong_volume_ratio
                          = 0.0 when volume confirmation is missing or below minimum

structure_alignment_score = 1.0 when swing structure aligns
                          = 0.5 when unavailable or neutral
                          = 0.0 when conflicting

support_resistance_context_score = 1.0 when directional S/R context aligns
                                 = 0.5 when unavailable or neutral
                                 = 0.0 when opposing major zone conflicts

liquidity_score = 1.0 when liquidity_pass and spread_pass are true
                = 0.0 when either hard filter fails

freshness_score = 1.0 when FRESH
                = 0.7 when TOUCHED without meaningful fill
                = 0.4 when PARTIALLY_FILLED
                = 0.0 when FILLED, BROKEN, or INVALID
```

Final classification:

```text
if hard validation failed:
    pattern_status = INVALID
else if pattern_score >= minimum_pattern_score:
    pattern_status = VALID
else if pattern_score >= weak_pattern_score:
    pattern_status = WEAK
else:
    pattern_status = INVALID
```

Defaults:

```text
minimum_pattern_score = 0.7
weak_pattern_score = 0.5
```

## Entry, Stop, and Target References

Reference levels are mechanical planning fields only. They are not orders,
position sizing, execution instructions, or live trading decisions.

Default ATR buffer:

```text
atr_buffer = stop_atr_buffer_multiplier * ATR
stop_atr_buffer_multiplier = 0.2
```

### Bullish FVG References

```text
entry_reference = zone_mid or zone_low
stop_reference = zone_low - atr_buffer
target_reference = nearest resistance zone or risk-reward based target
```

If no resistance zone is available:

```text
target_reference = entry_reference + default_risk_reward * (entry_reference - stop_reference)
```

### Bearish FVG References

```text
entry_reference = zone_mid or zone_high
stop_reference = zone_high + atr_buffer
target_reference = nearest support zone or risk-reward based target
```

If no support zone is available:

```text
target_reference = entry_reference - default_risk_reward * (stop_reference - entry_reference)
```

Risk-reward:

```text
risk_reward = abs(target_reference - entry_reference) / abs(entry_reference - stop_reference)
```

If the denominator is zero or any reference is unavailable:

```text
risk_reward = null
```

## Output Schema

```json
{
  "symbol": "BTCUSDT",
  "timestamp": "2026-05-17T00:00:00Z",
  "pattern_type": "FAIR_VALUE_GAP",
  "direction": "BULLISH",
  "pattern_status": "VALID",
  "fvg_state": "FRESH",
  "candle_1_index": 100,
  "candle_2_index": 101,
  "candle_3_index": 102,
  "zone_low": 65000.0,
  "zone_high": 65150.0,
  "zone_mid": 65075.0,
  "gap_size": 150.0,
  "gap_size_atr": 0.25,
  "fill_ratio": 0.0,
  "displacement_confirmed": true,
  "displacement_direction": "BULLISH",
  "volume_ratio": 1.45,
  "liquidity_pass": true,
  "spread_pass": true,
  "structure_context": {
    "market_structure_status": "UPTREND",
    "alignment": "ALIGNED"
  },
  "support_resistance_context": {
    "nearest_zone_type": "SUPPORT",
    "relationship": "NEAR"
  },
  "pattern_score": 0.82,
  "entry_reference": 65075.0,
  "stop_reference": 64900.0,
  "target_reference": 65425.0,
  "risk_reward": 2.0,
  "reason": ["BULLISH_FVG_DETECTED", "DISPLACEMENT_CONFIRMED"]
}
```

## Allowed Values

Direction:

```text
BULLISH
BEARISH
NONE
```

Pattern status:

```text
VALID
WEAK
INVALID
PENDING
```

FVG state:

```text
FRESH
TOUCHED
PARTIALLY_FILLED
FILLED
BROKEN
INVALID
```

## Edge Cases

### Not Enough Candles

If fewer than three consecutive candles are available, return `INVALID` with
`reason = NOT_ENOUGH_CANDLES`.

### Missing OHLC Data

If Candle 1, Candle 2, or Candle 3 is missing required OHLC fields, return
`INVALID` with `reason = MISSING_OHLC_DATA`.

### Gap Size Too Small

If `gap_size < minimum_gap_size_atr_multiplier * ATR`, return `INVALID` with
`reason = GAP_TOO_SMALL`.

### Gap Size Too Large

If `gap_size > maximum_gap_size_atr_multiplier * ATR`, classify as `WEAK` or
`INVALID` according to `large_gap_handling` and include `GAP_TOO_LARGE`.

### Middle Candle Is Not Displacement Candle

If `require_displacement_candle = true`, return `INVALID`. If false, reduce
score and classify no stronger than `WEAK`.

### Volume Confirmation Missing

If Volume Ratio is unavailable, set `volume_confirmation_score = 0.0` and include
`VOLUME_RATIO_UNAVAILABLE`. Do not invalidate unless a future task makes volume a
hard requirement.

### FVG Already Filled

Set `fvg_state = FILLED`, `fill_ratio = 1.0`, and do not treat the zone as a
fresh imbalance.

### FVG Already Broken

Set `fvg_state = BROKEN`, reduce `freshness_score` to `0.0`, and suppress fresh
entry interpretation.

### Overlapping FVGs

Multiple same-direction FVG zones may coexist. Preserve each detected three-candle
window as a separate historical pattern. A future implementation may optionally
merge overlapping zones, but this document does not require merging.

### Opposite-Direction FVGs Nearby

Do not cancel either FVG solely because an opposite-direction FVG is nearby.
Record context in `reason` and reduce score only when swing structure or
support/resistance context conflicts.

### Low Liquidity Market

If liquidity fails, return `INVALID` because the imbalance may be an illiquid
price jump.

### Wide Spread Market

If spread fails, return `INVALID` because the imbalance may not be actionable or
reliably measured.

### Conflicting Swing Structure

Keep the structural FVG detection, but reduce `structure_alignment_score` and
classify as `WEAK` if the final score falls below the valid threshold.

### FVG Formed by Illiquid Price Jump

If liquidity or spread filters fail at creation, return `INVALID` even when the
three-candle price structure exists.

### FVG Inside Major Support Zone

A bullish FVG inside support is supportive. A bearish FVG inside support is
conflicting unless other context marks the support as broken.

### FVG Inside Major Resistance Zone

A bearish FVG inside resistance is supportive. A bullish FVG inside resistance is
conflicting unless other context marks the resistance as broken.
