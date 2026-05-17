# Adam and Eve Pattern Mechanical Definition

## Purpose

Define the Adam and Eve Pattern mechanically.

This module detects a bullish double-bottom reversal structure with a sharp first bottom, a rounded second bottom, and a neckline breakout.

This document defines detection logic only.
It does not define order execution.

## Pattern Type

```text
Adam and Eve Pattern
```

## Pattern Categories

```text
Double Bottom Pattern
Reversal Pattern
Bottom Formation Pattern
Accumulation Pattern
Neckline Breakout Pattern
```

## Supported Directions

Initial supported direction:

```text
BULLISH
NONE
```

Optional future extension:

```text
BEARISH_INVERTED
```

The initial version must not emit `BEARISH_INVERTED` as a valid implemented direction unless a future implementation task explicitly adds inverted bearish detection.

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
minimum_pattern_duration: 10
maximum_pattern_duration: 160
maximum_bottom_difference_rate: 0.05
maximum_bottom_difference_atr: 1.0
maximum_adam_bottom_duration: 5
minimum_adam_decline_slope_atr: 0.5
minimum_adam_recovery_slope_atr: 0.5
minimum_adam_range_atr: 1.0
minimum_eve_bottom_duration: 5
minimum_eve_bottom_zone_duration: 3
maximum_eve_slope_atr: 0.6
minimum_eve_to_adam_duration_ratio: 1.5
eckline_touch_deviation_atr: 0.5
breakout_atr_multiplier: 0.2
minimum_breakout_volume_ratio: 1.5
weak_breakout_volume_ratio: 1.3
require_liquidity_pass: true
require_spread_pass: true
require_displacement_breakout: false
minimum_pattern_score: 0.7
```

## Core Structure

A bullish Adam and Eve Pattern consists of four structural parts:

```text
Adam bottom
Eve bottom
neckline
bullish breakout
```

Adam bottom:

```text
sharp V-shaped first low
fast decline into the low
fast recovery away from the low
narrow bottom duration
high local volatility
```

Eve bottom:

```text
rounded second low
wider bottom duration
longer bottom-zone residence
smoother recovery
lower local volatility than Adam
```

The pattern is confirmed only when price breaks above the neckline after the Eve low.

## Required Pivot Structure

Use confirmed pivots only.

Required pivot points:

```text
adam_low = first confirmed pivot low
neckline_pivot = confirmed pivot high between Adam and Eve
eve_low = second confirmed pivot low
```

Required ordering:

```text
adam_low.index < neckline_pivot.index < eve_low.index
```

Breakout ordering:

```text
breakout.index > eve_low.index
```

Reject the candidate when any required pivot is missing or when the required ordering is violated.

## Prior Downtrend Requirement

The candidate must appear after a prior downward structure.

Acceptable prior downtrend condition:

```text
market_structure_status = DOWNTREND
```

Alternative acceptable condition:

```text
recent swing labels before adam_low contain at least one LH and at least one LL
```

The prior trend window should end before `adam_low.index`.

Reject the candidate when no prior downtrend evidence exists.

## Candidate Selection

Candidate selection should scan confirmed pivot lows in chronological order.

For each ordered pair of pivot lows:

```text
adam_low.index < eve_low.index
```

Find the highest confirmed pivot high between them:

```text
neckline_pivot = max(pivot_high.price where adam_low.index < pivot_high.index < eve_low.index)
```

If no confirmed pivot high exists between the lows, reject the candidate.

The candidate duration is:

```text
pattern_duration = eve_low.index - adam_low.index
```

Accept only if:

```text
minimum_pattern_duration <= pattern_duration <= maximum_pattern_duration
```

## Bottom Similarity

Adam low and Eve low should be near the same price level.

Rate-based condition:

```text
bottom_difference_rate = abs(adam_low.price - eve_low.price) / adam_low.price
bottom_difference_rate <= maximum_bottom_difference_rate
```

ATR-based condition:

```text
bottom_difference_atr = abs(adam_low.price - eve_low.price) / ATR_at_eve_low
bottom_difference_atr <= maximum_bottom_difference_atr
```

A candidate is structurally stronger when both conditions pass.

A candidate is invalid when neither condition passes.

## Adam Bottom Definition

Adam bottom measures the sharpness of the first low.

Define Adam left reference as the most recent local swing high or local candle high before `adam_low` inside the Adam inspection window.

Define Adam right reference as the first recovery high or neckline-side pivot after `adam_low` and before `neckline_pivot`.

Adam bottom duration:

```text
adam_bottom_duration = adam_right_reference.index - adam_left_reference.index
```

Adam decline slope:

```text
adam_decline_slope_atr = (adam_left_reference.price - adam_low.price) / max(1, adam_low.index - adam_left_reference.index) / ATR_at_adam_low
```

Adam recovery slope:

```text
adam_recovery_slope_atr = (adam_right_reference.price - adam_low.price) / max(1, adam_right_reference.index - adam_low.index) / ATR_at_adam_low
```

Adam local range:

```text
adam_range_atr = (adam_left_reference.price - adam_low.price) / ATR_at_adam_low
```

Adam sharpness is valid when:

```text
adam_bottom_duration <= maximum_adam_bottom_duration
adam_decline_slope_atr >= minimum_adam_decline_slope_atr
adam_recovery_slope_atr >= minimum_adam_recovery_slope_atr
adam_range_atr >= minimum_adam_range_atr
```

If a clean Adam right reference cannot be selected, use the highest candle high between `adam_low.index` and `neckline_pivot.index`.

## Eve Bottom Definition

Eve bottom measures the roundness of the second low.

Define Eve left reference as the neckline-side decline reference before `eve_low`.

Define Eve right reference as the recovery reference after `eve_low` and before breakout.

Eve bottom duration:

```text
eve_bottom_duration = eve_right_reference.index - eve_left_reference.index
```

Define the Eve bottom zone around the Eve low:

```text
eve_bottom_zone_low = eve_low.price
eve_bottom_zone_high = eve_low.price + neckline_touch_deviation_atr * ATR_at_eve_low
```

Eve bottom-zone duration:

```text
eve_bottom_zone_duration = count(candles where eve_bottom_zone_low <= low_or_close <= eve_bottom_zone_high)
```

Eve decline slope:

```text
eve_decline_slope_atr = (eve_left_reference.price - eve_low.price) / max(1, eve_low.index - eve_left_reference.index) / ATR_at_eve_low
```

Eve recovery slope:

```text
eve_recovery_slope_atr = (eve_right_reference.price - eve_low.price) / max(1, eve_right_reference.index - eve_low.index) / ATR_at_eve_low
```

Eve roundness is valid when:

```text
eve_bottom_duration >= minimum_eve_bottom_duration
eve_bottom_zone_duration >= minimum_eve_bottom_zone_duration
eve_decline_slope_atr <= maximum_eve_slope_atr
eve_recovery_slope_atr <= maximum_eve_slope_atr
```

If the Eve recovery reference is not available yet, the candidate status should be `PENDING` rather than `VALID`.

## Adam Versus Eve Shape Difference

The Eve structure must be wider or smoother than the Adam structure.

Duration condition:

```text
eve_to_adam_duration_ratio = eve_bottom_duration / max(1, adam_bottom_duration)
eve_to_adam_duration_ratio >= minimum_eve_to_adam_duration_ratio
```

Volatility comparison:

```text
eve_range_atr <= adam_range_atr
```

At least the duration condition must pass.

The volatility comparison is a scoring component and may downgrade the candidate to `WEAK` when it fails.

## Neckline Definition

The initial version uses a horizontal neckline:

```text
neckline = neckline_pivot.price
```

The neckline must be above both lows:

```text
neckline > adam_low.price
neckline > eve_low.price
```

Neckline height from the average bottom:

```text
average_bottom_price = (adam_low.price + eve_low.price) / 2
pattern_height = neckline - average_bottom_price
pattern_height_atr = pattern_height / ATR_at_eve_low
```

Reject a candidate when `pattern_height <= 0`.

## Bullish Breakout Definition

A bullish breakout can only be evaluated after `eve_low.index`.

Breakout threshold:

```text
breakout_threshold = neckline + breakout_atr_multiplier * ATR_at_breakout
```

Bullish breakout condition:

```text
breakout.close > breakout_threshold
```

The first candle after the Eve low that satisfies the condition is the breakout candle.

If no candle satisfies the breakout condition, the candidate status is `PENDING` when all structure requirements pass.

## Volume Confirmation

Use the Volume Ratio module at the breakout candle.

Strong volume confirmation:

```text
breakout_volume_ratio >= minimum_breakout_volume_ratio
```

Weak volume confirmation:

```text
weak_breakout_volume_ratio <= breakout_volume_ratio < minimum_breakout_volume_ratio
```

Invalid or missing volume confirmation:

```text
breakout_volume_ratio < weak_breakout_volume_ratio
```

A candidate with weak volume can be `WEAK` if all mandatory structure and filter requirements pass.

A candidate with missing volume data should be `PENDING` if breakout has not been confirmed by another required mechanism.

## Optional Displacement Breakout

When `require_displacement_breakout = false`, displacement candle data is optional and contributes only to score.

When `require_displacement_breakout = true`, the breakout candle must also satisfy:

```text
displacement_direction = BULLISH
displacement_status in [VALID, STRONG]
```

If required displacement data is missing, the candidate cannot be `VALID`.

## Liquidity Filter

When `require_liquidity_pass = true`, require:

```text
liquidity_pass = true
```

The liquidity snapshot should correspond to the breakout candle or the latest available snapshot before breakout.

If liquidity fails, status must be `INVALID`.

If liquidity data is missing, status should be `PENDING` unless the implementation explicitly treats missing required filter data as invalid.

## Spread Filter

When `require_spread_pass = true`, require:

```text
spread_pass = true
```

The bid-ask spread snapshot should correspond to the breakout candle or the latest available snapshot before breakout.

If spread fails, status must be `INVALID`.

If spread data is missing, status should be `PENDING` unless the implementation explicitly treats missing required filter data as invalid.

## Support And Resistance Context

Use Support / Resistance Zone data as context.

Positive evidence:

```text
adam_low or eve_low occurs inside or near a support zone
neckline aligns with or is below a resistance zone that gets broken
breakout closes above the neckline resistance zone
```

Negative evidence:

```text
breakout occurs directly into a nearby stronger resistance zone without clearing it
bottom lows occur far from any support context
```

Support / Resistance Zone context should affect score and diagnostics.
It should not replace required pivot, prior trend, breakout, liquidity, or spread validation.

## Pattern Status

Allowed status values:

```text
VALID
WEAK
INVALID
PENDING
```

## VALID

A candidate is `VALID` when all conditions pass:

```text
prior downtrend exists
required pivot ordering is valid
bottom similarity passes
Adam sharpness passes
Eve roundness passes
Eve-to-Adam duration ratio passes
neckline is valid
bullish breakout is confirmed
breakout volume is strong
liquidity filter passes
spread filter passes
required displacement confirmation passes when enabled
pattern_score >= minimum_pattern_score
```

## WEAK

A candidate is `WEAK` when mandatory structural requirements pass, but one or more quality conditions are marginal:

```text
breakout volume is weak but not invalid
support/resistance context is neutral or mildly negative
Eve range is not lower than Adam range
pattern_score is below minimum_pattern_score but above an implementation-defined weak threshold
```

A `WEAK` candidate must still satisfy liquidity and spread filters when those filters are required.

## PENDING

A candidate is `PENDING` when the structure is forming but confirmation data is not complete:

```text
Adam and Eve structure is present
neckline is defined
breakout has not occurred yet
or required breakout candle data is missing
or required filter snapshots are missing and missing data is not treated as invalid
```

## INVALID

A candidate is `INVALID` when any mandatory rule fails:

```text
prior downtrend missing
required pivots missing
pivot ordering invalid
bottom similarity invalid
Adam sharpness invalid
Eve roundness invalid
Eve-to-Adam duration invalid
neckline invalid
liquidity filter fails
spread filter fails
required displacement confirmation fails
```

## Pattern Score

Pattern score must be a normalized value from `0.0` to `1.0`.

Suggested components:

```text
prior_trend_score
bottom_similarity_score
adam_sharpness_score
eve_roundness_score
shape_difference_score
neckline_quality_score
breakout_strength_score
volume_confirmation_score
liquidity_score
support_resistance_score
displacement_score
```

Suggested default weights:

```yaml
prior_trend_score: 0.10
bottom_similarity_score: 0.15
adam_sharpness_score: 0.12
eve_roundness_score: 0.12
shape_difference_score: 0.10
neckline_quality_score: 0.08
breakout_strength_score: 0.12
volume_confirmation_score: 0.10
liquidity_score: 0.04
support_resistance_score: 0.04
displacement_score: 0.03
```

Weights should sum to `1.0`.

## Prior Trend Score

Score high when the pre-pattern structure is clearly bearish:

```text
1.0 = DOWNTREND with recent LH and LL labels
0.7 = DOWNTREND without complete recent labels
0.5 = recent LH and LL labels but neutral current status
0.0 = no prior downtrend evidence
```

## Bottom Similarity Score

Score high when Adam and Eve lows are close:

```text
bottom_similarity_score = 1.0 - min(1.0, bottom_difference_rate / maximum_bottom_difference_rate)
```

If ATR-based similarity is stronger than rate-based similarity, use the higher of the two normalized similarity scores.

## Adam Sharpness Score

Score high when Adam is narrow, fast, and volatile:

```text
duration_component = 1.0 - min(1.0, adam_bottom_duration / maximum_adam_bottom_duration)
decline_component = min(1.0, adam_decline_slope_atr / minimum_adam_decline_slope_atr)
recovery_component = min(1.0, adam_recovery_slope_atr / minimum_adam_recovery_slope_atr)
range_component = min(1.0, adam_range_atr / minimum_adam_range_atr)
adam_sharpness_score = average(duration_component, decline_component, recovery_component, range_component)
```

## Eve Roundness Score

Score high when Eve is wider and smoother:

```text
duration_component = min(1.0, eve_bottom_duration / minimum_eve_bottom_duration)
zone_component = min(1.0, eve_bottom_zone_duration / minimum_eve_bottom_zone_duration)
decline_smoothness_component = 1.0 - min(1.0, eve_decline_slope_atr / maximum_eve_slope_atr)
recovery_smoothness_component = 1.0 - min(1.0, eve_recovery_slope_atr / maximum_eve_slope_atr)
eve_roundness_score = average(duration_component, zone_component, decline_smoothness_component, recovery_smoothness_component)
```

## Shape Difference Score

Score high when Eve is materially wider than Adam:

```text
shape_difference_score = min(1.0, eve_to_adam_duration_ratio / minimum_eve_to_adam_duration_ratio)
```

Add a positive diagnostic flag when:

```text
eve_range_atr <= adam_range_atr
```

## Neckline Quality Score

Score high when the neckline is clear and materially above both lows:

```text
neckline_quality_score = min(1.0, pattern_height_atr / 1.0)
```

Reduce score when the neckline pivot is ambiguous, when multiple similar highs compete for neckline selection, or when nearby resistance remains uncleared.

## Breakout Strength Score

Score high when breakout closes far above the neckline threshold:

```text
breakout_distance_atr = (breakout.close - neckline) / ATR_at_breakout
breakout_strength_score = min(1.0, breakout_distance_atr / max(breakout_atr_multiplier, 0.01))
```

## Volume Confirmation Score

```text
1.0 = breakout_volume_ratio >= minimum_breakout_volume_ratio
0.5 = weak_breakout_volume_ratio <= breakout_volume_ratio < minimum_breakout_volume_ratio
0.0 = breakout_volume_ratio < weak_breakout_volume_ratio or missing required volume
```

## Liquidity Score

```text
1.0 = liquidity_pass = true
0.0 = liquidity_pass = false or missing when required
```

## Support Resistance Score

```text
1.0 = bottoms align with support and breakout clears neckline resistance
0.7 = one support/resistance context condition is favorable
0.5 = neutral context
0.0 = breakout is blocked by nearby stronger resistance
```

## Displacement Score

When displacement confirmation is optional:

```text
1.0 = bullish displacement confirms breakout
0.5 = displacement data missing
0.0 = displacement contradicts breakout
```

When displacement confirmation is required:

```text
1.0 = required bullish displacement passes
0.0 = required bullish displacement fails or is missing
```

## Entry Reference

This document defines reference levels only.
It does not place orders.

Bullish entry reference:

```text
entry_reference = breakout.close
```

Alternative pullback reference:

```text
pullback_entry_reference = neckline
```

A future implementation may expose both references without deciding position size or executing trades.

## Stop Reference

Conservative stop reference:

```text
stop_reference = min(adam_low.price, eve_low.price) - breakout_atr_multiplier * ATR_at_breakout
```

Eve-only stop reference:

```text
eve_stop_reference = eve_low.price - breakout_atr_multiplier * ATR_at_breakout
```

The stop reference is a level for downstream analysis only.
It is not an order instruction.

## Target Reference

Measured-move target:

```text
target_reference = neckline + pattern_height
```

Risk-reward reference:

```text
risk = entry_reference - stop_reference
reward = target_reference - entry_reference
risk_reward_ratio = reward / risk
```

If `risk <= 0`, risk-reward is invalid and should be returned as `null` or marked invalid by implementation.

## Output Schema

A detector should return one record per evaluated candidate.

```yaml
pattern_type: ADAM_AND_EVE
direction: BULLISH | NONE
pattern_status: VALID | WEAK | INVALID | PENDING
symbol: string
timeframe: string | null
adam_low_index: integer
adam_low_timestamp: datetime
adam_low_price: float
neckline_index: integer
neckline_timestamp: datetime
neckline_price: float
eve_low_index: integer
eve_low_timestamp: datetime
eve_low_price: float
breakout_index: integer | null
breakout_timestamp: datetime | null
breakout_close: float | null
pattern_duration: integer
adam_bottom_duration: integer | null
eve_bottom_duration: integer | null
eve_bottom_zone_duration: integer | null
bottom_difference_rate: float
bottom_difference_atr: float | null
eve_to_adam_duration_ratio: float | null
pattern_height: float
pattern_height_atr: float | null
breakout_threshold: float | null
breakout_distance_atr: float | null
breakout_volume_ratio: float | null
liquidity_pass: boolean | null
spread_pass: boolean | null
displacement_confirmed: boolean | null
support_resistance_context: string | null
pattern_score: float
score_components: object
entry_reference: float | null
pullback_entry_reference: float | null
stop_reference: float | null
eve_stop_reference: float | null
target_reference: float | null
risk_reward_ratio: float | null
invalid_reasons: list[string]
warnings: list[string]
```

## Output Field Rules

### pattern_type

Always:

```text
ADAM_AND_EVE
```

### direction

Use:

```text
BULLISH
```

when bullish breakout is confirmed.

Use:

```text
NONE
```

when the structure is pending or invalid without a confirmed breakout.

### pattern_status

Must be one of:

```text
VALID
WEAK
INVALID
PENDING
```

### invalid_reasons

Include deterministic reason codes such as:

```text
MISSING_PRIOR_DOWNTREND
MISSING_ADAM_LOW
MISSING_NECKLINE_PIVOT
MISSING_EVE_LOW
INVALID_PIVOT_ORDER
PATTERN_DURATION_TOO_SHORT
PATTERN_DURATION_TOO_LONG
BOTTOM_SIMILARITY_FAILED
ADAM_SHARPNESS_FAILED
EVE_ROUNDNESS_FAILED
SHAPE_DIFFERENCE_FAILED
INVALID_NECKLINE
BREAKOUT_NOT_CONFIRMED
BREAKOUT_VOLUME_TOO_LOW
LIQUIDITY_FAILED
SPREAD_FAILED
DISPLACEMENT_REQUIRED_FAILED
```

### warnings

Include non-fatal diagnostics such as:

```text
WEAK_BREAKOUT_VOLUME
NEUTRAL_SUPPORT_RESISTANCE_CONTEXT
EVE_RANGE_NOT_LOWER_THAN_ADAM_RANGE
MISSING_OPTIONAL_DISPLACEMENT_DATA
AMBIGUOUS_NECKLINE
```

## Edge Cases

### Missing Candles

If required OHLCV candles are missing inside the candidate window, return `INVALID` or skip the candidate.

### Missing Pivots

If required confirmed pivot lows or the neckline pivot high are missing, return `INVALID`.

### Unconfirmed Pivots

Do not use unconfirmed pivots.

A candidate based on unconfirmed pivots must remain outside the detector output or be returned as `PENDING` only if the implementation explicitly supports provisional diagnostics.

### Equal Bottoms

Equal Adam and Eve low prices are valid if all other rules pass.

### Eve Below Adam

Eve low may be slightly below Adam low only within the bottom similarity tolerance.

If Eve low is far below Adam low, reject the candidate.

### Eve Above Adam

Eve low may be slightly above Adam low within the bottom similarity tolerance.

A higher Eve low can be positive context when prior downtrend and breakout conditions pass.

### Multiple Neckline Pivots

If multiple pivot highs exist between the lows, select the highest pivot high as the default neckline.

If two or more highs are within `neckline_touch_deviation_atr` of each other, keep the selected highest neckline and add warning:

```text
AMBIGUOUS_NECKLINE
```

### Breakout Gap

If price gaps above the neckline threshold and closes above it, the breakout is valid.

Use the breakout candle close as `entry_reference`.

### Intrabar Breakout Without Close Confirmation

If high exceeds the neckline threshold but close does not, do not confirm breakout.

Return `PENDING` when the structure remains valid.

### Failed Breakout

If breakout closes above the threshold but volume is too low, return `INVALID` or `WEAK` according to the volume thresholds.

If price later closes back below the neckline, this document does not define failure tracking beyond initial detection.

### Low Liquidity Or Wide Spread

If required liquidity or spread filters fail, return `INVALID` regardless of structure quality.

### Missing ATR

If ATR is missing for required threshold calculations, return `PENDING` when the pattern is otherwise structurally valid and the missing ATR may arrive later.

If ATR cannot be computed for the window, return `INVALID`.

### Zero Or Negative Prices

Reject candidates with zero or negative prices.

### Overlapping Candidates

If multiple candidates share the same Eve low and neckline, keep the highest-scoring candidate.

If candidates overlap but have different pivot anchors, output each candidate unless a future task defines deduplication rules.

## Pseudocode

```text
for each symbol and timeframe:
    load candles, confirmed pivots, swing structure, ATR, volume ratio, liquidity, spread

    for each ordered pair of confirmed pivot lows:
        assign adam_low and eve_low
        validate adam_low.index < eve_low.index
        validate pattern duration
        validate prior downtrend before adam_low

        select highest confirmed pivot high between adam_low and eve_low as neckline_pivot
        validate adam_low.index < neckline_pivot.index < eve_low.index
        calculate neckline and pattern height
        validate bottom similarity
        calculate Adam sharpness metrics
        calculate Eve roundness metrics
        validate Eve-to-Adam shape difference

        search candles after eve_low for close > neckline + breakout ATR buffer
        if breakout not found:
            return PENDING candidate if structure is valid

        validate breakout volume
        validate liquidity and spread filters
        validate required displacement if enabled
        calculate score components and pattern_score
        assign VALID, WEAK, INVALID, or PENDING
        return candidate output
```

## Non-Goals

This document does not define:

```text
application code implementation
real order execution
paper order execution
position sizing
portfolio allocation
risk management policy
exchange API integration
live trading
backtesting engine changes
machine learning
UI visualization
manual chart drawing
bearish inverted Adam and Eve implementation
```
