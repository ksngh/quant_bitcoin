# Order Block Pattern Mechanical Definition

# Source Requirement

## Purpose

Define the Order Block Pattern mechanically.

This pattern identifies a supply or demand zone created by the last opposing
candle before a valid displacement candle. The output is a technical detection
specification only. It does not define order execution, position sizing, live
trading, exchange integration, or backtesting engine behavior.

## Pattern Type

```text
ORDER_BLOCK
```

Human-readable name:

```text
Order Block Pattern
```

## Pattern Categories

```text
Supply / Demand Zone
Institutional Imbalance Zone
Structure-Based Reversal or Continuation Zone
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
Pivot High / Pivot Low
Swing Structure
ATR
Volume Ratio
Support / Resistance Zone
Displacement Candle
```

The pattern module must not recalculate these indicators internally except for
simple comparisons against already-provided snapshot fields.

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
displacement candle snapshots
liquidity status
bid-ask spread status
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
order_block:
  source_search_lookback: 5
  allow_single_candle_order_block: true
  allow_multi_candle_order_block: true
  maximum_source_cluster_size: 3
  zone_definition: FULL_RANGE
  allow_body_only_zone: true
  allow_wick_adjusted_zone: true
  require_displacement: true
  minimum_displacement_body_ratio: 0.6
  minimum_displacement_atr_multiplier: 1.5
  minimum_volume_ratio: 1.5
  weak_volume_ratio: 1.3
  close_extreme_threshold: 0.25
  require_liquidity_pass: true
  require_spread_pass: true
  require_structure_confirmation: false
  minimum_zone_size_atr_multiplier: 0.1
  maximum_zone_size_atr_multiplier: 2.0
  mitigation_threshold: 0.5
  broken_atr_buffer_multiplier: 0.2
  stop_atr_buffer_multiplier: 0.2
  minimum_pattern_score: 0.7
  weak_pattern_score: 0.5
  default_entry_reference: ZONE_MID
  default_risk_reward: 2.0
```

## Core Definitions

### Bullish Order Block

A bullish order block is the last bearish candle, or last bearish candle cluster,
before a valid bullish displacement candle.

Required mechanical structure:

```text
1. A bearish source candle or bearish source cluster exists before displacement.
2. A later displacement snapshot has displacement_direction = BULLISH.
3. The displacement snapshot has displacement_status = VALID.
4. The displacement range satisfies the ATR minimum move rule.
5. The displacement candle volume ratio satisfies the volume rule.
6. Liquidity and spread filters pass.
7. The source candle range defines a bullish demand zone.
```

Primary source candle rule:

```text
source_candle = last candle before bullish displacement where close < open
```

### Bearish Order Block

A bearish order block is the last bullish candle, or last bullish candle cluster,
before a valid bearish displacement candle.

Required mechanical structure:

```text
1. A bullish source candle or bullish source cluster exists before displacement.
2. A later displacement snapshot has displacement_direction = BEARISH.
3. The displacement snapshot has displacement_status = VALID.
4. The displacement range satisfies the ATR minimum move rule.
5. The displacement candle volume ratio satisfies the volume rule.
6. Liquidity and spread filters pass.
7. The source candle range defines a bearish supply zone.
```

Primary source candle rule:

```text
source_candle = last candle before bearish displacement where close > open
```

## Displacement Candle Requirement

The pattern is created only after a valid displacement candle exists after the
source candle.

Bullish displacement:

```text
displacement_direction = BULLISH
displacement_status = VALID
```

Bearish displacement:

```text
displacement_direction = BEARISH
displacement_status = VALID
```

A displacement candle is acceptable only when the Displacement Candle snapshot
and dependent ATR / Volume Ratio snapshots satisfy:

```text
body_ratio >= minimum_displacement_body_ratio
candle_range >= minimum_displacement_atr_multiplier * ATR
volume_ratio >= weak_volume_ratio
close near directional extreme
```

Strong displacement volume confirmation:

```text
volume_ratio >= minimum_volume_ratio
```

Weak displacement volume confirmation:

```text
weak_volume_ratio <= volume_ratio < minimum_volume_ratio
```

Directional close-location rule:

```text
candle_range = high - low
```

Bullish:

```text
(high - close) / candle_range <= close_extreme_threshold
```

Bearish:

```text
(close - low) / candle_range <= close_extreme_threshold
```

If `candle_range <= 0`, the displacement is invalid for this pattern.

## Source Candle Selection

### Single-Candle Order Block

Single-candle order blocks are allowed by default.

Bullish:

```text
source candle = nearest candle before displacement where close < open
```

Bearish:

```text
source candle = nearest candle before displacement where close > open
```

Search window:

```text
displacement_index - source_search_lookback <= source_index < displacement_index
```

If no valid source candle exists inside the search window:

```text
pattern_status = INVALID
order_block_state = INVALID
reason = SOURCE_CANDLE_NOT_FOUND
```

### Multi-Candle Order Block

Multi-candle order blocks are allowed, but the first version should prefer the
single nearest opposing candle for deterministic behavior.

A multi-candle cluster may be used when consecutive candles immediately before
displacement have the opposing direction.

Bullish cluster:

```text
all cluster candles have close < open
cluster ends at source_candle_index
cluster_size <= maximum_source_cluster_size
```

Bearish cluster:

```text
all cluster candles have close > open
cluster ends at source_candle_index
cluster_size <= maximum_source_cluster_size
```

When `zone_definition = FULL_RANGE`, cluster boundaries are:

```text
zone_low = minimum low across source cluster
zone_high = maximum high across source cluster
```

If multiple candidate clusters exist, select the candidate closest to the
displacement candle.

## Zone Definitions

Supported values:

```text
FULL_RANGE
BODY_ONLY
WICK_ADJUSTED
```

Recommended initial version:

```text
zone_definition = FULL_RANGE
```

### Full Range Zone

Bullish and bearish full range zones use the same boundaries:

```text
zone_low = source_candle.low
zone_high = source_candle.high
```

For multi-candle source clusters:

```text
zone_low = minimum source_cluster.low
zone_high = maximum source_cluster.high
```

### Body-Only Zone

Bullish body-only zone:

```text
zone_low = source_candle.low
zone_high = source_candle.open
```

Bearish body-only zone:

```text
zone_low = source_candle.close
zone_high = source_candle.high
```

### Wick-Adjusted Zone

Wick-adjusted zones are optional and must be deterministic.

Bullish wick-adjusted zone:

```text
zone_low = source_candle.low
zone_high = max(source_candle.open, source_candle.close)
```

Bearish wick-adjusted zone:

```text
zone_low = min(source_candle.open, source_candle.close)
zone_high = source_candle.high
```

### Derived Zone Values

```text
zone_mid = (zone_low + zone_high) / 2
zone_size = zone_high - zone_low
zone_size_atr = zone_size / ATR
```

Invalid zone boundaries:

```text
zone_high <= zone_low
ATR <= 0
```

## Zone Size Validation

The zone must not be too small or too large relative to ATR.

```text
zone_size >= minimum_zone_size_atr_multiplier * ATR
zone_size <= maximum_zone_size_atr_multiplier * ATR
```

Default:

```text
minimum_zone_size_atr_multiplier = 0.1
maximum_zone_size_atr_multiplier = 2.0
```

If zone size validation fails:

```text
pattern_status = INVALID
order_block_state = INVALID
reason = ZONE_TOO_SMALL or ZONE_TOO_LARGE
```

## Liquidity and Spread Filters

Before validating the pattern:

```text
liquidity_pass = true
spread_pass = true
```

If liquidity fails and `require_liquidity_pass = true`:

```text
pattern_status = INVALID
order_block_state = INVALID
reason = LIQUIDITY_FILTER_FAILED
```

If spread fails and `require_spread_pass = true`:

```text
pattern_status = INVALID
order_block_state = INVALID
reason = SPREAD_FILTER_FAILED
```

## Volume Confirmation

Volume confirmation uses the Volume Ratio snapshot for the displacement candle.

Strong confirmation:

```text
volume_ratio >= minimum_volume_ratio
```

Default:

```text
minimum_volume_ratio = 1.5
```

Weak confirmation:

```text
volume_ratio >= weak_volume_ratio
and
volume_ratio < minimum_volume_ratio
```

Default:

```text
weak_volume_ratio = 1.3
```

No confirmation:

```text
volume_ratio < weak_volume_ratio
```

If displacement is otherwise valid but volume is weak:

```text
pattern_status = WEAK
```

If volume has no confirmation:

```text
pattern_status = INVALID
reason = VOLUME_CONFIRMATION_FAILED
```

## ATR Usage

ATR must be used for:

```text
displacement validation
zone size validation
broken zone validation
stop reference calculation
```

Minimum displacement move:

```text
displacement_range >= minimum_displacement_atr_multiplier * ATR
```

Default:

```text
minimum_displacement_atr_multiplier = 1.5
```

Displacement range ATR:

```text
displacement_range_atr = displacement_range / ATR
```

Broken-zone ATR buffer:

```text
broken_buffer = broken_atr_buffer_multiplier * ATR
```

Stop ATR buffer:

```text
stop_buffer = stop_atr_buffer_multiplier * ATR
```

If ATR is missing, non-positive, or invalid:

```text
pattern_status = INVALID
order_block_state = INVALID
reason = ATR_INVALID
```

## Swing Structure Confirmation

Structure confirmation is optional by default but should be reported for every
candidate.

Supported structure events:

```text
BOS
CHoCH
MSS
```

Bullish structure confirmation is true when either condition is met:

```text
displacement_close > nearest_previous_confirmed_pivot_high.price
```

or:

```text
previous market_structure_status = DOWNTREND
and current market_structure_status in [TRANSITION, UPTREND]
```

Bearish structure confirmation is true when either condition is met:

```text
displacement_close < nearest_previous_confirmed_pivot_low.price
```

or:

```text
previous market_structure_status = UPTREND
and current market_structure_status in [TRANSITION, DOWNTREND]
```

Event classification:

```text
BOS = break in direction of the prior trend
CHoCH = break against the prior trend
MSS = transition from UPTREND to TRANSITION/DOWNTREND or DOWNTREND to TRANSITION/UPTREND
```

If `require_structure_confirmation = true` and no structure confirmation exists:

```text
pattern_status = INVALID
reason = STRUCTURE_NOT_CONFIRMED
```

If structure confirmation is not required, missing or conflicting structure only
reduces the structure score.

## Support / Resistance Context

Use the Support / Resistance Zone snapshots to classify location context.

Bullish order block context:

```text
SUPPORT zone overlap = favorable
MIXED zone overlap = neutral/favorable
RESISTANCE zone overlap = unfavorable unless broken/flipped support
```

Bearish order block context:

```text
RESISTANCE zone overlap = favorable
MIXED zone overlap = neutral/favorable
SUPPORT zone overlap = unfavorable unless broken/flipped resistance
```

Zone overlap is true when:

```text
order_block.zone_low <= sr_zone.zone_high
and
order_block.zone_high >= sr_zone.zone_low
```

Context output values:

```text
FAVORABLE_SUPPORT
FAVORABLE_RESISTANCE
MIXED_CONTEXT
CONFLICTING_SUPPORT
CONFLICTING_RESISTANCE
NO_CONTEXT
```

Major support or resistance zones do not automatically invalidate the pattern.
They affect score unless they directly conflict with direction and the configured
future implementation elects to require context alignment.

## Order Block State

Allowed values:

```text
FRESH
TOUCHED
MITIGATED
BROKEN
INVALID
```

State is evaluated after the displacement candle using subsequent candles only.
The displacement candle itself creates the order block and is not counted as a
return to the zone unless a future implementation explicitly enables immediate
return handling.

### FRESH

An order block is fresh when price has not returned to the zone after creation.

```text
no subsequent candle satisfies the touched rule
```

### TOUCHED

Bullish touched rule:

```text
low <= zone_high
and
close >= zone_low
```

Bearish touched rule:

```text
high >= zone_low
and
close <= zone_high
```

### MITIGATED

An order block is mitigated when price enters the zone by at least the configured
percentage.

Default:

```text
mitigation_threshold = 0.5
```

Bullish mitigation depth:

```text
mitigation_depth = (zone_high - lowest_low_after_touch) / zone_size
```

Bearish mitigation depth:

```text
mitigation_depth = (highest_high_after_touch - zone_low) / zone_size
```

Mitigated:

```text
mitigation_depth >= mitigation_threshold
```

Clamp `mitigation_depth` to the range `0.0` through `1.0` for scoring and output
interpretation.

### BROKEN

Bullish broken rule:

```text
close < zone_low - broken_atr_buffer_multiplier * ATR
```

Bearish broken rule:

```text
close > zone_high + broken_atr_buffer_multiplier * ATR
```

A broken zone is not valid for new bullish or bearish order block references.

### INVALID

An order block is invalid when any required validation fails:

```text
source candle is invalid
displacement is missing
displacement is invalid
liquidity filter fails
spread filter fails
zone is broken
zone is too large
zone is too small
ATR is invalid
volume confirmation fails
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
source candle exists
displacement_status = VALID
displacement_direction matches order block direction
ATR displacement rule passes
volume_ratio >= minimum_volume_ratio
zone size is valid
order_block_state in [FRESH, TOUCHED, MITIGATED]
pattern_score >= minimum_pattern_score
```

### WEAK

```text
all required hard filters pass
and volume_ratio >= weak_volume_ratio
and volume_ratio < minimum_volume_ratio
```

or:

```text
all required hard filters pass
and weak_pattern_score <= pattern_score < minimum_pattern_score
```

### PENDING

```text
source candle candidate exists
but no valid displacement candle has occurred yet
```

PENDING candidates are optional for watchlist-style consumers and must not be
reported as valid order blocks.

### INVALID

```text
required source candle missing
required displacement missing
required displacement invalid
liquidity_pass = false
spread_pass = false
ATR invalid
volume ratio invalid or below weak threshold
zone size invalid
order_block_state in [BROKEN, INVALID]
required structure confirmation missing
```

## Scoring

Score range:

```text
0.0 to 1.0
```

Recommended components:

```text
displacement_score: 0.25
volume_confirmation_score: 0.15
structure_confirmation_score: 0.15
zone_quality_score: 0.15
liquidity_score: 0.10
support_resistance_context_score: 0.10
freshness_score: 0.10
```

Total:

```text
pattern_score =
    displacement_score * 0.25
  + volume_confirmation_score * 0.15
  + structure_confirmation_score * 0.15
  + zone_quality_score * 0.15
  + liquidity_score * 0.10
  + support_resistance_context_score * 0.10
  + freshness_score * 0.10
```

### Displacement Score

```text
if displacement_range_atr >= 2.0 and body_ratio >= 0.7:
    displacement_score = 1.0
elif displacement_range_atr >= 1.5 and body_ratio >= 0.6:
    displacement_score = 0.8
else:
    displacement_score = 0.0
```

### Volume Confirmation Score

```text
if volume_ratio >= 2.0:
    volume_confirmation_score = 1.0
elif volume_ratio >= 1.5:
    volume_confirmation_score = 0.8
elif volume_ratio >= 1.3:
    volume_confirmation_score = 0.5
else:
    volume_confirmation_score = 0.0
```

### Structure Confirmation Score

```text
if structure_confirmed = true:
    structure_confirmation_score = 1.0
elif structure is neutral or unavailable and not required:
    structure_confirmation_score = 0.5
else:
    structure_confirmation_score = 0.0
```

### Zone Quality Score

```text
if 0.25 <= zone_size_atr <= 1.0:
    zone_quality_score = 1.0
elif minimum_zone_size_atr_multiplier <= zone_size_atr <= maximum_zone_size_atr_multiplier:
    zone_quality_score = 0.7
else:
    zone_quality_score = 0.0
```

### Liquidity Score

```text
if liquidity_status = HIGH and spread_status = TIGHT:
    liquidity_score = 1.0
elif liquidity_pass = true and spread_pass = true:
    liquidity_score = 0.8
else:
    liquidity_score = 0.0
```

### Support / Resistance Context Score

```text
if context is favorable for direction:
    support_resistance_context_score = 1.0
elif context is MIXED_CONTEXT or NO_CONTEXT:
    support_resistance_context_score = 0.6
else:
    support_resistance_context_score = 0.2
```

### Freshness Score

```text
if order_block_state = FRESH:
    freshness_score = 1.0
elif order_block_state = TOUCHED:
    freshness_score = 0.7
elif order_block_state = MITIGATED:
    freshness_score = 0.4
else:
    freshness_score = 0.0
```

## Entry, Stop, and Target References

These fields are reference levels only. They must not place orders, size
positions, or call execution components.

Supported entry reference modes:

```text
ZONE_HIGH
ZONE_MID
ZONE_LOW
```

Bullish references:

```text
entry_reference = zone_high, zone_mid, or zone_low
stop_reference = zone_low - stop_atr_buffer_multiplier * ATR
target_reference = nearest resistance zone or risk-reward based target
```

Bearish references:

```text
entry_reference = zone_low, zone_mid, or zone_high
stop_reference = zone_high + stop_atr_buffer_multiplier * ATR
target_reference = nearest support zone or risk-reward based target
```

If no suitable support or resistance target exists, use a risk-reward reference.

Bullish risk-reward target:

```text
risk = entry_reference - stop_reference
target_reference = entry_reference + default_risk_reward * risk
```

Bearish risk-reward target:

```text
risk = stop_reference - entry_reference
target_reference = entry_reference - default_risk_reward * risk
```

Risk-reward output:

```text
risk_reward = abs(target_reference - entry_reference) / abs(entry_reference - stop_reference)
```

If risk is zero or negative:

```text
risk_reward = null
pattern_status = INVALID
reason = INVALID_RISK_REFERENCE
```

## Detection Flow

Pseudocode-level logic:

```text
for each valid displacement snapshot:
    if liquidity/spread filters fail:
        emit INVALID candidate or skip according to consumer policy

    determine direction from displacement_direction
    locate nearest opposing source candle before displacement
    optionally expand to opposing source cluster
    build zone using configured zone_definition
    validate ATR, displacement_range_atr, volume_ratio, and zone_size_atr
    evaluate structure confirmation from pivots and swing snapshots
    classify support/resistance context
    classify current order_block_state from candles after displacement
    compute entry, stop, target references
    compute pattern_score
    assign VALID, WEAK, INVALID, or PENDING status
    emit output schema
```

## Output Schema

Each detected candidate must include at least:

```text
symbol
timestamp
pattern_type
direction
pattern_status
order_block_state
source_candle_index
source_candle_timestamp
displacement_candle_index
displacement_candle_timestamp
zone_low
zone_high
zone_mid
zone_size
zone_size_atr
displacement_direction
displacement_range_atr
volume_ratio
liquidity_pass
spread_pass
structure_confirmed
support_resistance_context
pattern_score
entry_reference
stop_reference
target_reference
risk_reward
reason
```

Additional recommended fields:

```text
source_mode
source_cluster_start_index
source_cluster_end_index
zone_definition
body_ratio
liquidity_status
spread_status
structure_event
mitigation_depth
nearest_support_zone_id
nearest_resistance_zone_id
```

Allowed `direction` values:

```text
BULLISH
BEARISH
NONE
```

Allowed `pattern_status` values:

```text
VALID
WEAK
INVALID
PENDING
```

Allowed `order_block_state` values:

```text
FRESH
TOUCHED
MITIGATED
BROKEN
INVALID
```

## Edge Cases

### No Displacement Candle

```text
pattern_status = PENDING if a source candidate exists
pattern_status = INVALID if no source candidate exists
reason = DISPLACEMENT_MISSING
```

### Displacement Candle Without Volume Confirmation

```text
volume_ratio < weak_volume_ratio -> INVALID
weak_volume_ratio <= volume_ratio < minimum_volume_ratio -> WEAK
```

### Source Candle Not Found

```text
pattern_status = INVALID
order_block_state = INVALID
reason = SOURCE_CANDLE_NOT_FOUND
```

### Multiple Source Candles

Use the nearest valid opposing candle before displacement for the initial
single-candle version. If multi-candle mode is enabled, combine consecutive
opposing candles up to `maximum_source_cluster_size`.

### Overlapping Order Blocks

Overlapping zones of the same direction may both be emitted. Consumers may merge
or rank them later, but this pattern definition should rank by:

```text
higher pattern_score
then newer displacement_candle_timestamp
then smaller zone_size_atr
```

Opposite-direction overlaps are not merged by this pattern definition and should
be reported as separate candidates with context noted in `reason` if needed.

### Order Block Too Large

```text
zone_size_atr > maximum_zone_size_atr_multiplier -> INVALID
reason = ZONE_TOO_LARGE
```

### Order Block Too Small

```text
zone_size_atr < minimum_zone_size_atr_multiplier -> INVALID
reason = ZONE_TOO_SMALL
```

### Order Block Already Mitigated

If mitigation has occurred but the zone is not broken:

```text
order_block_state = MITIGATED
pattern_status may be VALID or WEAK depending on score
freshness_score is reduced
```

### Order Block Already Broken

```text
order_block_state = BROKEN
pattern_status = INVALID
reason = ZONE_BROKEN
```

### Price Returns to Zone Immediately

If the first candle after displacement touches the zone:

```text
order_block_state = TOUCHED or MITIGATED according to depth
freshness_score is reduced
```

The displacement candle itself is not treated as a return to the zone.

### Low Liquidity Market

```text
liquidity_pass = false -> INVALID
reason = LIQUIDITY_FILTER_FAILED
```

### Wide Spread Market

```text
spread_pass = false -> INVALID
reason = SPREAD_FILTER_FAILED
```

### Conflicting Swing Structure

If structure confirmation conflicts with direction and structure confirmation is
required:

```text
pattern_status = INVALID
reason = STRUCTURE_CONFLICT
```

If structure confirmation is optional:

```text
structure_confirmation_score = 0.0
pattern may remain WEAK or VALID only if total score and hard filters pass
```

### Order Block Inside Major Support Zone

Bullish order block inside support is favorable. Bearish order block inside
support is conflicting unless that support is already broken or flipped.

### Order Block Inside Major Resistance Zone

Bearish order block inside resistance is favorable. Bullish order block inside
resistance is conflicting unless that resistance is already broken or flipped.

## Non-Goals

This document does not include:

```text
actual trading execution
exchange API integration
position sizing implementation
backtesting engine implementation
live order placement
machine learning model
UI visualization
manual chart drawing
```
