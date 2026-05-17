# Fair Value Gap Pattern Mechanical Definition

## Purpose

Define the Fair Value Gap pattern mechanically.

This module detects bullish and bearish price imbalance zones using a three-candle structure.

This document defines detection logic only.
It does not define order execution.

## Pattern Type

```text
Fair Value Gap
FVG
```

## Pattern Categories

```text
Price Imbalance
Inefficient Price Delivery
Three-Candle Gap Structure
Continuation Zone
Reversion Zone
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
ATR
Volume Ratio
Displacement Candle
Swing Structure
Support / Resistance Zone
```

Optional:

```text
Pivot High / Pivot Low
```

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
liquidity snapshot
bid-ask spread snapshot
```

## Default Parameters

```yaml
minimum_gap_size_atr_multiplier: 0.1
maximum_gap_size_atr_multiplier: 2.0
require_displacement_candle: true
minimum_volume_ratio: 1.3
strong_volume_ratio: 1.5
break_buffer_atr_multiplier: 0.2
fill_threshold: 1.0
partial_fill_threshold: 0.01
require_liquidity_pass: true
require_spread_pass: true
minimum_pattern_score: 0.7
```

## Three-Candle Structure

The module evaluates three consecutive candles.

```text
candle_1 = candles[i - 2]
candle_2 = candles[i - 1]
candle_3 = candles[i]
```

The middle candle is used for displacement validation.

```text
middle_candle = candle_2
```

## Bullish FVG Definition

A bullish FVG exists when:

```text
candle_1.high < candle_3.low
```

Gap size:

```text
gap_size = candle_3.low - candle_1.high
```

Zone:

```text
zone_low = candle_1.high
zone_high = candle_3.low
```

Zone mid:

```text
zone_mid = (zone_low + zone_high) / 2
```

Expected displacement:

```text
candle_2 displacement_direction = BULLISH
```

## Bearish FVG Definition

A bearish FVG exists when:

```text
candle_1.low > candle_3.high
```

Gap size:

```text
gap_size = candle_1.low - candle_3.high
```

Zone:

```text
zone_low = candle_3.high
zone_high = candle_1.low
```

Zone mid:

```text
zone_mid = (zone_low + zone_high) / 2
```

Expected displacement:

```text
candle_2 displacement_direction = BEARISH
```

## Gap Size ATR

```text
gap_size_atr = gap_size / ATR
```

Valid gap size:

```text
gap_size_atr >= minimum_gap_size_atr_multiplier
and
gap_size_atr <= maximum_gap_size_atr_multiplier
```

Default:

```text
minimum_gap_size_atr_multiplier = 0.1
maximum_gap_size_atr_multiplier = 2.0
```

If gap is too small:

```text
pattern_status = INVALID
```

If gap is too large:

```text
pattern_status = WEAK
```

Recommended initial handling:

```text
gap_size_atr > maximum_gap_size_atr_multiplier = WEAK
not INVALID
```

Reason:

```text
Large FVG may represent extreme imbalance but may also have poor risk reference.
```

## Displacement Validation

If `require_displacement_candle = true`, the middle candle must be a valid displacement candle.

### Bullish FVG Displacement

```text
candle_2.displacement_direction = BULLISH
candle_2.displacement_status = VALID
```

### Bearish FVG Displacement

```text
candle_2.displacement_direction = BEARISH
candle_2.displacement_status = VALID
```

If displacement is missing and required:

```text
pattern_status = INVALID
```

If displacement is missing but not required:

```text
displacement_confirmed = false
```

and:

```text
reduce displacement_score
```

## Volume Confirmation

Use the volume ratio of the middle candle.

```text
volume_ratio = candle_2.volume_ratio
```

Strong confirmation:

```text
volume_ratio >= strong_volume_ratio
```

Default:

```text
strong_volume_ratio = 1.5
```

Valid confirmation:

```text
volume_ratio >= minimum_volume_ratio
```

Default:

```text
minimum_volume_ratio = 1.3
```

If:

```text
volume_ratio < minimum_volume_ratio
```

Then:

```text
pattern_status = WEAK
```

If volume ratio is missing:

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

## Fresh State

An FVG is fresh when price has not returned to the zone after creation.

### Bullish FVG Fresh

```text
no later candle has low <= zone_high
```

### Bearish FVG Fresh

```text
no later candle has high >= zone_low
```

## Touched State

### Bullish FVG Touched

```text
later_candle.low <= zone_high
and
later_candle.high >= zone_low
```

### Bearish FVG Touched

```text
later_candle.high >= zone_low
and
later_candle.low <= zone_high
```

## Partially Filled State

### Bullish FVG Partially Filled

```text
later_candle.low < zone_high
and
later_candle.low > zone_low
```

### Bearish FVG Partially Filled

```text
later_candle.high > zone_low
and
later_candle.high < zone_high
```

## Filled State

### Bullish FVG Filled

```text
later_candle.low <= zone_low
```

### Bearish FVG Filled

```text
later_candle.high >= zone_high
```

## Broken State

### Bullish FVG Broken

```text
close < zone_low - break_buffer_atr_multiplier * ATR
```

### Bearish FVG Broken

```text
close > zone_high + break_buffer_atr_multiplier * ATR
```

Default:

```text
break_buffer_atr_multiplier = 0.2
```

## Fill Ratio

### Bullish Fill Ratio

Use the lowest price after FVG creation.

```text
fill_ratio = (zone_high - lowest_price_after_creation) / gap_size
```

Clamp:

```text
fill_ratio = max(0.0, min(fill_ratio, 1.0))
```

### Bearish Fill Ratio

Use the highest price after FVG creation.

```text
fill_ratio = (highest_price_after_creation - zone_low) / gap_size
```

Clamp:

```text
fill_ratio = max(0.0, min(fill_ratio, 1.0))
```

## Fill Ratio State Mapping

```text
fill_ratio = 0.0:
    fvg_state = FRESH

0.0 < fill_ratio < 1.0:
    fvg_state = PARTIALLY_FILLED

fill_ratio >= 1.0:
    fvg_state = FILLED
```

If broken condition is satisfied:

```text
fvg_state = BROKEN
```

## Structure Context

### Bullish Structure Alignment

Bullish FVG is aligned when:

```text
market_structure_status = UPTREND
or
market_structure_status = TRANSITION
```

Optional stricter condition:

```text
latest swing label includes HH or HL
```

### Bearish Structure Alignment

Bearish FVG is aligned when:

```text
market_structure_status = DOWNTREND
or
market_structure_status = TRANSITION
```

Optional stricter condition:

```text
latest swing label includes LH or LL
```

If structure conflicts:

```text
reduce structure_alignment_score
```

Do not invalidate by default.

## Support / Resistance Context

### Bullish FVG Context

Bullish FVG is stronger when:

```text
FVG zone overlaps support zone
or
distance_to_nearest_support <= 0.5 * ATR
```

### Bearish FVG Context

Bearish FVG is stronger when:

```text
FVG zone overlaps resistance zone
or
distance_to_nearest_resistance <= 0.5 * ATR
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
three-candle FVG exists
gap_size_atr >= minimum_gap_size_atr_multiplier
gap_size_atr <= maximum_gap_size_atr_multiplier
displacement requirement satisfied
volume_ratio >= minimum_volume_ratio
fvg_state is not FILLED
fvg_state is not BROKEN
pattern_score >= minimum_pattern_score
```

### WEAK

```text
three-candle FVG exists
but volume_ratio is weak
```

or:

```text
gap_size_atr > maximum_gap_size_atr_multiplier
```

or:

```text
pattern_score >= 0.5
and
pattern_score < minimum_pattern_score
```

### PENDING

```text
FVG exists
fvg_state = FRESH
price has not returned to the zone
```

### INVALID

```text
liquidity filter fails
spread filter fails
not enough candles
OHLC data missing
no valid FVG structure
gap size too small
required displacement missing
volume ratio missing
FVG is filled
FVG is broken
```

## Pattern Score

Score range:

```text
0.0 to 1.0
```

Recommended components:

```text
gap_quality_score: 0.20
displacement_score: 0.25
volume_confirmation_score: 0.15
structure_alignment_score: 0.15
support_resistance_context_score: 0.10
liquidity_score: 0.10
freshness_score: 0.05
```

Formula:

```text
pattern_score =
    gap_quality_score * 0.20
  + displacement_score * 0.25
  + volume_confirmation_score * 0.15
  + structure_alignment_score * 0.15
  + support_resistance_context_score * 0.10
  + liquidity_score * 0.10
  + freshness_score * 0.05
```

## Gap Quality Score

```text
if 0.2 <= gap_size_atr <= 1.0:
    gap_quality_score = 1.0

else if 0.1 <= gap_size_atr < 0.2:
    gap_quality_score = 0.6

else if 1.0 < gap_size_atr <= 2.0:
    gap_quality_score = 0.7

else:
    gap_quality_score = 0.0
```

## Displacement Score

```text
if displacement_confirmed = true:
    displacement_score = 1.0

else if require_displacement_candle = false:
    displacement_score = 0.4

else:
    displacement_score = 0.0
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

## Structure Alignment Score

```text
if FVG direction aligns with market_structure_status:
    structure_alignment_score = 1.0

else if market_structure_status = TRANSITION:
    structure_alignment_score = 0.7

else if market_structure_status = RANGE:
    structure_alignment_score = 0.5

else:
    structure_alignment_score = 0.2
```

## Support / Resistance Context Score

### Bullish FVG

```text
if FVG overlaps support zone:
    support_resistance_context_score = 1.0

else if FVG is near support zone within 0.5 * ATR:
    support_resistance_context_score = 0.7

else:
    support_resistance_context_score = 0.5
```

### Bearish FVG

```text
if FVG overlaps resistance zone:
    support_resistance_context_score = 1.0

else if FVG is near resistance zone within 0.5 * ATR:
    support_resistance_context_score = 0.7

else:
    support_resistance_context_score = 0.5
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

## Freshness Score

```text
if fvg_state = FRESH:
    freshness_score = 1.0

else if fvg_state = TOUCHED:
    freshness_score = 0.8

else if fvg_state = PARTIALLY_FILLED:
    freshness_score = 0.5

else:
    freshness_score = 0.0
```

## Entry Reference

This module must not execute orders.

It only defines reference prices.

### Bullish Entry Reference

Supported values:

```text
zone_high
zone_mid
zone_low
```

Recommended default:

```text
entry_reference = zone_mid
```

### Bearish Entry Reference

Supported values:

```text
zone_low
zone_mid
zone_high
```

Recommended default:

```text
entry_reference = zone_mid
```

## Stop Reference

### Bullish Stop Reference

```text
stop_reference = zone_low - break_buffer_atr_multiplier * ATR
```

### Bearish Stop Reference

```text
stop_reference = zone_high + break_buffer_atr_multiplier * ATR
```

## Target Reference

### Bullish Target Reference

Preferred:

```text
target_reference = nearest_resistance_zone
```

Fallback:

```text
target_reference = entry_reference + 2 * abs(entry_reference - stop_reference)
```

### Bearish Target Reference

Preferred:

```text
target_reference = nearest_support_zone
```

Fallback:

```text
target_reference = entry_reference - 2 * abs(stop_reference - entry_reference)
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
  "pattern_type": "FAIR_VALUE_GAP",
  "direction": "BULLISH",
  "pattern_status": "VALID",
  "fvg_state": "FRESH",
  "candle_1_index": 120,
  "candle_2_index": 121,
  "candle_3_index": 122,
  "zone_low": 64200.0,
  "zone_high": 64500.0,
  "zone_mid": 64350.0,
  "gap_size": 300.0,
  "gap_size_atr": 0.375,
  "fill_ratio": 0.0,
  "displacement_confirmed": true,
  "displacement_direction": "BULLISH",
  "volume_ratio": 1.7,
  "liquidity_pass": true,
  "spread_pass": true,
  "structure_context": "UPTREND",
  "support_resistance_context": "NEAR_SUPPORT",
  "pattern_score": 0.82,
  "entry_reference": 64350.0,
  "stop_reference": 64140.0,
  "target_reference": 64770.0,
  "risk_reward": 2.0,
  "reason": "Bullish FVG detected with valid three-candle imbalance, bullish displacement, and volume confirmation."
}
```

## Output Fields

### pattern_type

Fixed value:

```text
FAIR_VALUE_GAP
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

### fvg_state

One of:

```text
FRESH
TOUCHED
PARTIALLY_FILLED
FILLED
BROKEN
INVALID
```

### candle_1_index

Index of the first candle in the three-candle structure.

### candle_2_index

Index of the middle candle.

### candle_3_index

Index of the third candle.

### zone_low

Lower boundary of the FVG zone.

### zone_high

Upper boundary of the FVG zone.

### zone_mid

Middle price of the FVG zone.

```text
zone_mid = (zone_low + zone_high) / 2
```

### gap_size

Absolute size of the FVG zone.

```text
gap_size = zone_high - zone_low
```

### gap_size_atr

Gap size normalized by ATR.

```text
gap_size_atr = gap_size / ATR
```

### fill_ratio

How much of the FVG has been filled.

```text
0.0 = not filled
1.0 = fully filled
```

### displacement_confirmed

Boolean value.

```text
true = middle candle is valid displacement candle
false = middle candle is not valid displacement candle
```

### displacement_direction

One of:

```text
BULLISH
BEARISH
NONE
INVALID
```

### volume_ratio

Volume ratio of the middle candle.

### liquidity_pass

Result from Liquidity module.

### spread_pass

Result from Bid-Ask Spread module.

### structure_context

Market structure status at FVG creation.

### support_resistance_context

Possible values:

```text
OVERLAPS_SUPPORT
OVERLAPS_RESISTANCE
NEAR_SUPPORT
NEAR_RESISTANCE
NONE
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

### Not enough candles

If fewer than three candles exist:

```text
pattern_status = INVALID
```

### Missing OHLC data

If required high or low values are missing:

```text
pattern_status = INVALID
```

### No FVG structure

If neither condition is true:

```text
candle_1.high < candle_3.low
candle_1.low > candle_3.high
```

Then:

```text
pattern_status = INVALID
```

### Gap too small

If:

```text
gap_size_atr < minimum_gap_size_atr_multiplier
```

Then:

```text
pattern_status = INVALID
```

### Gap too large

If:

```text
gap_size_atr > maximum_gap_size_atr_multiplier
```

Then:

```text
pattern_status = WEAK
```

### Missing displacement

If `require_displacement_candle = true` and middle candle is not displacement:

```text
pattern_status = INVALID
```

### Missing volume ratio

If volume ratio is missing:

```text
pattern_status = INVALID
```

### FVG already filled

If:

```text
fvg_state = FILLED
```

Then:

```text
pattern_status = INVALID
```

### FVG broken

If:

```text
fvg_state = BROKEN
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

### Overlapping FVGs

If multiple FVGs overlap:

```text
keep all initially
```

Optional later rule:

```text
merge overlapping FVGs of same direction
```

Tie-break priority:

```text
1. higher pattern_score
2. fresher FVG
3. larger volume_ratio
4. better structure alignment
```

## Detection Logic

```text
1. Check liquidity_pass.
2. Check spread_pass.
3. Iterate candles from index 2.
4. Assign candle_1, candle_2, candle_3.
5. Check bullish FVG condition.
6. Check bearish FVG condition.
7. Calculate zone boundaries.
8. Calculate gap_size and gap_size_atr.
9. Validate gap size.
10. Validate middle candle displacement.
11. Validate volume ratio.
12. Determine FVG state.
13. Check structure context.
14. Check support / resistance context.
15. Calculate pattern score.
16. Set pattern status.
17. Return valid, weak, or pending FVG signals.
```

## Pseudocode

```python
def detect_fvg_patterns(context, config):
    if config.require_liquidity_pass and not context.liquidity.liquidity_pass:
        return []

    if config.require_spread_pass and not context.spread.spread_pass:
        return []

    signals = []

    candles = context.candles

    for i in range(2, len(candles)):
        candle_1 = candles[i - 2]
        candle_2 = candles[i - 1]
        candle_3 = candles[i]

        bullish_signal = evaluate_bullish_fvg(
            candle_1,
            candle_2,
            candle_3,
            context,
            config
        )

        bearish_signal = evaluate_bearish_fvg(
            candle_1,
            candle_2,
            candle_3,
            context,
            config
        )

        if bullish_signal is not None:
            signals.append(bullish_signal)

        if bearish_signal is not None:
            signals.append(bearish_signal)

    return signals
```

## Bullish FVG Evaluation

```python
def evaluate_bullish_fvg(candle_1, candle_2, candle_3, context, config):
    if candle_1.high >= candle_3.low:
        return None

    zone_low = candle_1.high
    zone_high = candle_3.low
    gap_size = zone_high - zone_low

    atr = context.atr_at(candle_3.index)

    if atr is None:
        return invalid_fvg("missing_atr")

    gap_size_atr = gap_size / atr

    if gap_size_atr < config.minimum_gap_size_atr_multiplier:
        return invalid_fvg("gap_too_small")

    displacement = context.displacement_at(candle_2.index)

    displacement_confirmed = (
        displacement is not None
        and displacement["displacement_direction"] == "BULLISH"
        and displacement["displacement_status"] == "VALID"
    )

    if config.require_displacement_candle and not displacement_confirmed:
        return invalid_fvg("missing_bullish_displacement")

    volume_ratio = context.volume_ratio_at(candle_2.index)

    if volume_ratio is None:
        return invalid_fvg("missing_volume_ratio")

    fvg_state, fill_ratio = classify_bullish_fvg_state(
        zone_low,
        zone_high,
        context.candles_after(candle_3.index),
        atr,
        config
    )

    if fvg_state in ["FILLED", "BROKEN"]:
        return invalid_fvg("fvg_already_filled_or_broken")

    score = calculate_fvg_score(
        direction="BULLISH",
        gap_size_atr=gap_size_atr,
        displacement_confirmed=displacement_confirmed,
        volume_ratio=volume_ratio,
        fvg_state=fvg_state,
        context=context,
        config=config
    )

    status = classify_fvg_status(
        score=score,
        gap_size_atr=gap_size_atr,
        volume_ratio=volume_ratio,
        fvg_state=fvg_state,
        config=config
    )

    return build_fvg_output(
        direction="BULLISH",
        status=status,
        fvg_state=fvg_state,
        candle_1=candle_1,
        candle_2=candle_2,
        candle_3=candle_3,
        zone_low=zone_low,
        zone_high=zone_high,
        gap_size=gap_size,
        gap_size_atr=gap_size_atr,
        fill_ratio=fill_ratio,
        displacement_confirmed=displacement_confirmed,
        volume_ratio=volume_ratio,
        score=score,
        context=context,
        config=config
    )
```

## Bearish FVG Evaluation

```python
def evaluate_bearish_fvg(candle_1, candle_2, candle_3, context, config):
    if candle_1.low <= candle_3.high:
        return None

    zone_low = candle_3.high
    zone_high = candle_1.low
    gap_size = zone_high - zone_low

    atr = context.atr_at(candle_3.index)

    if atr is None:
        return invalid_fvg("missing_atr")

    gap_size_atr = gap_size / atr

    if gap_size_atr < config.minimum_gap_size_atr_multiplier:
        return invalid_fvg("gap_too_small")

    displacement = context.displacement_at(candle_2.index)

    displacement_confirmed = (
        displacement is not None
        and displacement["displacement_direction"] == "BEARISH"
        and displacement["displacement_status"] == "VALID"
    )

    if config.require_displacement_candle and not displacement_confirmed:
        return invalid_fvg("missing_bearish_displacement")

    volume_ratio = context.volume_ratio_at(candle_2.index)

    if volume_ratio is None:
        return invalid_fvg("missing_volume_ratio")

    fvg_state, fill_ratio = classify_bearish_fvg_state(
        zone_low,
        zone_high,
        context.candles_after(candle_3.index),
        atr,
        config
    )

    if fvg_state in ["FILLED", "BROKEN"]:
        return invalid_fvg("fvg_already_filled_or_broken")

    score = calculate_fvg_score(
        direction="BEARISH",
        gap_size_atr=gap_size_atr,
        displacement_confirmed=displacement_confirmed,
        volume_ratio=volume_ratio,
        fvg_state=fvg_state,
        context=context,
        config=config
    )

    status = classify_fvg_status(
        score=score,
        gap_size_atr=gap_size_atr,
        volume_ratio=volume_ratio,
        fvg_state=fvg_state,
        config=config
    )

    return build_fvg_output(
        direction="BEARISH",
        status=status,
        fvg_state=fvg_state,
        candle_1=candle_1,
        candle_2=candle_2,
        candle_3=candle_3,
        zone_low=zone_low,
        zone_high=zone_high,
        gap_size=gap_size,
        gap_size_atr=gap_size_atr,
        fill_ratio=fill_ratio,
        displacement_confirmed=displacement_confirmed,
        volume_ratio=volume_ratio,
        score=score,
        context=context,
        config=config
    )
```

## Java-style Domain Model Example

```java
public enum FvgDirection {
    BULLISH,
    BEARISH,
    NONE
}
```

```java
public enum FvgState {
    FRESH,
    TOUCHED,
    PARTIALLY_FILLED,
    FILLED,
    BROKEN,
    INVALID
}
```

```java
public enum FvgStatus {
    VALID,
    WEAK,
    INVALID,
    PENDING
}
```

```java
public record FairValueGapSignal(
    String symbol,
    Instant timestamp,
    String patternType,
    FvgDirection direction,
    FvgStatus patternStatus,
    FvgState fvgState,
    int candle1Index,
    int candle2Index,
    int candle3Index,
    BigDecimal zoneLow,
    BigDecimal zoneHigh,
    BigDecimal zoneMid,
    BigDecimal gapSize,
    BigDecimal gapSizeAtr,
    BigDecimal fillRatio,
    boolean displacementConfirmed,
    DisplacementDirection displacementDirection,
    BigDecimal volumeRatio,
    boolean liquidityPass,
    boolean spreadPass,
    String structureContext,
    String supportResistanceContext,
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
fair_value_gap:
  minimum_gap_size_atr_multiplier: 0.1
  maximum_gap_size_atr_multiplier: 2.0
  require_displacement_candle: true
  minimum_volume_ratio: 1.3
  strong_volume_ratio: 1.5
  break_buffer_atr_multiplier: 0.2
  fill_threshold: 1.0
  partial_fill_threshold: 0.01
  require_liquidity_pass: true
  require_spread_pass: true
  minimum_pattern_score: 0.7
```

## Final Mechanical Rule

```text
Bullish FVG:
1. Use three consecutive candles.
2. Require candle_1.high < candle_3.low.
3. zone_low = candle_1.high.
4. zone_high = candle_3.low.
5. Require gap_size >= 0.1 * ATR.
6. Require candle_2 to be bullish displacement candle.
7. Require candle_2.volume_ratio >= 1.3.
8. Require liquidity_pass = true.
9. Require spread_pass = true.

Bearish FVG:
1. Use three consecutive candles.
2. Require candle_1.low > candle_3.high.
3. zone_low = candle_3.high.
4. zone_high = candle_1.low.
5. Require gap_size >= 0.1 * ATR.
6. Require candle_2 to be bearish displacement candle.
7. Require candle_2.volume_ratio >= 1.3.
8. Require liquidity_pass = true.
9. Require spread_pass = true.
```
