# Task 036: Fair Value Gap Pattern Mechanical Definition

# Goal

Create a concise Markdown technical specification for mechanically detecting the Fair Value Gap Pattern.

This task is documentation-only. It must not implement pattern detection code, trading execution, exchange integration, backtesting engine changes, live order placement, machine learning, UI visualization, or manual chart drawing.

# Source Requirement

## Task Purpose

Create a mechanical specification for detecting the Fair Value Gap pattern.

This task does not include implementation.

The output of this task should be a design document that defines how an FVG can be detected using previously defined core indicator modules.

## Target Pattern

```text
Fair Value Gap
FVG
```

## Pattern Category

```text
Price Imbalance
Inefficient Price Delivery
Three-Candle Gap Structure
Continuation or Reversion Zone
```

## Required Core Indicator Modules

This pattern must reuse the following core modules:

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

## Required Input Data

The pattern document must define how to use the following inputs:

```text
OHLCV candles
ATR values
volume ratio values
displacement candle snapshots
swing structure snapshots
support / resistance zones
liquidity status
bid-ask spread status
```

Optional:

```text
confirmed pivot highs
confirmed pivot lows
```

## Main Detection Objective

The document must define how to detect bullish and bearish Fair Value Gaps mechanically.

The pattern should support both directions:

```text
Bullish FVG
Bearish FVG
```

## Bullish FVG Concept

A bullish FVG is a three-candle imbalance where the first candle high is lower than the third candle low.

General structure:

```text
1. Candle 1 forms before the impulse.
2. Candle 2 is usually a bullish displacement candle.
3. Candle 3 closes after the impulse.
4. A price gap exists between Candle 1 high and Candle 3 low.
5. The gap becomes a potential bullish reaction zone.
```

Mechanical structure:

```text
candle_1.high < candle_3.low
```

Bullish FVG zone:

```text
zone_low = candle_1.high
zone_high = candle_3.low
```

## Bearish FVG Concept

A bearish FVG is a three-candle imbalance where the first candle low is higher than the third candle high.

General structure:

```text
1. Candle 1 forms before the impulse.
2. Candle 2 is usually a bearish displacement candle.
3. Candle 3 closes after the impulse.
4. A price gap exists between Candle 1 low and Candle 3 high.
5. The gap becomes a potential bearish reaction zone.
```

Mechanical structure:

```text
candle_1.low > candle_3.high
```

Bearish FVG zone:

```text
zone_low = candle_3.high
zone_high = candle_1.low
```

## Mechanical Requirements

The pattern document must define:

```text
1. How to identify the three-candle FVG structure
2. How to define bullish FVG
3. How to define bearish FVG
4. How to define FVG zone boundaries
5. How to validate gap size using ATR
6. How to validate the middle candle using Displacement Candle module
7. How to apply volume confirmation
8. How to classify fresh, touched, partially filled, filled, and invalid FVGs
9. How to use swing structure context
10. How to use support / resistance context
11. How to score the FVG
12. How to define entry, stop, and target references
```

## Three-Candle Structure Requirements

The document must define FVG using exactly three consecutive candles.

```text
candle_1 = candles[i - 2]
candle_2 = candles[i - 1]
candle_3 = candles[i]
```

The middle candle should be used for displacement validation.

```text
middle_candle = candle_2
```

## Bullish FVG Requirements

The document must define bullish FVG as:

```text
candle_1.high < candle_3.low
```

The gap size:

```text
gap_size = candle_3.low - candle_1.high
```

The FVG zone:

```text
zone_low = candle_1.high
zone_high = candle_3.low
```

The middle candle should preferably satisfy:

```text
displacement_direction = BULLISH
displacement_status = VALID
```

## Bearish FVG Requirements

The document must define bearish FVG as:

```text
candle_1.low > candle_3.high
```

The gap size:

```text
gap_size = candle_1.low - candle_3.high
```

The FVG zone:

```text
zone_low = candle_3.high
zone_high = candle_1.low
```

The middle candle should preferably satisfy:

```text
displacement_direction = BEARISH
displacement_status = VALID
```

## Gap Size Requirements

The document must define minimum and maximum gap size.

Gap size must be normalized by ATR.

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
pattern_status = WEAK or INVALID
```

## Displacement Requirements

The document must define whether middle candle displacement is required.

Recommended initial version:

```text
require_displacement_candle = true
```

For bullish FVG:

```text
candle_2 must be bullish displacement candle
```

For bearish FVG:

```text
candle_2 must be bearish displacement candle
```

If displacement is not required:

```text
FVG can still be detected, but pattern score is reduced.
```

## Volume Confirmation Requirements

The document must define volume confirmation using the middle candle.

Default:

```text
candle_2.volume_ratio >= minimum_volume_ratio
```

Recommended:

```text
minimum_volume_ratio = 1.3
```

Strong confirmation:

```text
volume_ratio >= 1.5
```

## Liquidity Requirements

Before validating the pattern, the document must require:

```text
liquidity_pass = true
spread_pass = true
```

If liquidity or spread fails:

```text
pattern_valid = false
```

## FVG State Requirements

The document must define FVG states.

Allowed values:

```text
FRESH
TOUCHED
PARTIALLY_FILLED
FILLED
BROKEN
INVALID
```

## Fresh FVG

An FVG is fresh when price has not returned to the zone after creation.

Bullish:

```text
no later candle has low <= zone_high
```

Bearish:

```text
no later candle has high >= zone_low
```

## Touched FVG

Bullish FVG is touched when:

```text
later_candle.low <= zone_high
and
later_candle.high >= zone_low
```

Bearish FVG is touched when:

```text
later_candle.high >= zone_low
and
later_candle.low <= zone_high
```

## Partially Filled FVG

An FVG is partially filled when price enters the gap but does not fully fill it.

Bullish:

```text
later_candle.low < zone_high
and
later_candle.low > zone_low
```

Bearish:

```text
later_candle.high > zone_low
and
later_candle.high < zone_high
```

## Filled FVG

Bullish FVG is filled when:

```text
later_candle.low <= zone_low
```

Bearish FVG is filled when:

```text
later_candle.high >= zone_high
```

## Broken FVG

The document must define whether filled FVGs are considered broken or still valid.

Recommended initial version:

```text
filled FVG = FILLED
not tradable as fresh imbalance
```

Broken condition may be defined separately:

Bullish FVG broken:

```text
close < zone_low - ATR buffer
```

Bearish FVG broken:

```text
close > zone_high + ATR buffer
```

## Fill Ratio Requirements

The document must define fill ratio.

For bullish FVG:

```text
fill_ratio = (zone_high - lowest_price_inside_zone) / gap_size
```

For bearish FVG:

```text
fill_ratio = (highest_price_inside_zone - zone_low) / gap_size
```

Clamp:

```text
fill_ratio = max(0.0, min(fill_ratio, 1.0))
```

State mapping:

```text
fill_ratio = 0.0 -> FRESH
0.0 < fill_ratio < 1.0 -> PARTIALLY_FILLED
fill_ratio >= 1.0 -> FILLED
```

## Structure Context Requirements

The document must define optional structure alignment.

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

If structure conflicts:

```text
reduce pattern score
```

## Support / Resistance Context Requirements

Bullish FVG is stronger when:

```text
FVG zone overlaps support zone
or
FVG zone is near support zone
```

Bearish FVG is stronger when:

```text
FVG zone overlaps resistance zone
or
FVG zone is near resistance zone
```

Near condition:

```text
distance_to_zone <= 0.5 * ATR
```

## Pattern Output Requirements

The pattern document must define an output schema containing at least:

```text
symbol
timestamp
pattern_type
direction
pattern_status
fvg_state
candle_1_index
candle_2_index
candle_3_index
zone_low
zone_high
zone_mid
gap_size
gap_size_atr
fill_ratio
displacement_confirmed
displacement_direction
volume_ratio
liquidity_pass
spread_pass
structure_context
support_resistance_context
pattern_score
entry_reference
stop_reference
target_reference
risk_reward
reason
```

## Pattern Direction Values

Allowed values:

```text
BULLISH
BEARISH
NONE
```

## Pattern Status Values

Allowed values:

```text
VALID
WEAK
INVALID
PENDING
```

## FVG State Values

Allowed values:

```text
FRESH
TOUCHED
PARTIALLY_FILLED
FILLED
BROKEN
INVALID
```

## Pattern Score Requirements

The document must define a score from `0.0` to `1.0`.

The score should include:

```text
gap_quality_score
displacement_score
volume_confirmation_score
structure_alignment_score
support_resistance_context_score
liquidity_score
freshness_score
```

## Risk Reference Requirements

The document must define reference levels, not actual order execution.

Required:

```text
entry_reference
stop_reference
target_reference
```

For bullish FVG:

```text
entry_reference = zone_mid or zone_low
stop_reference = zone_low - ATR buffer
target_reference = nearest resistance zone or risk-reward based target
```

For bearish FVG:

```text
entry_reference = zone_mid or zone_high
stop_reference = zone_high + ATR buffer
target_reference = nearest support zone or risk-reward based target
```

## Edge Cases to Define

The pattern document must handle:

```text
not enough candles
missing OHLC data
gap size too small
gap size too large
middle candle is not displacement candle
volume confirmation missing
FVG already filled
FVG already broken
overlapping FVGs
opposite-direction FVGs nearby
low liquidity market
wide spread market
conflicting swing structure
FVG formed by illiquid price jump
FVG inside major support zone
FVG inside major resistance zone
```

## Non-Goals

This task does not include:

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

## Expected Deliverable

The next document should be:

```text
Fair Value Gap Pattern Mechanical Definition
```

It must be written as a concise Markdown technical specification.

It must reuse the previously defined core indicator modules.

It must not include actual implementation code beyond pseudocode-level logic.

It must not include a final summary section.

# Extracted Roles

- Owner role: Pattern mechanical definition for Fair Value Gap detection.
- Supporting roles:
  - ATR, as the gap-size, broken-zone, and stop-reference normalization input.
  - Volume Ratio, as middle-candle volume-confirmation input.
  - Displacement Candle, as the preferred or required middle-candle impulse input.
  - Swing Structure, as directional and transition context input.
  - Support / Resistance Zone, as contextual target and overlap input.
  - Liquidity: Trading Value / Volume, as the required tradability filter.
  - Bid-Ask Spread, as the required execution-quality filter.
  - Pivot High / Pivot Low, as optional structure context input.
- Forbidden roles:
  - Execution, because this task must not place, simulate, or route orders.
  - Exchange integration, because this task must not call real exchange APIs.
  - Risk management and position sizing, because this task only defines reference levels.
  - Backtesting engine, live trading, database, dashboard, scheduler, FastAPI, Streamlit, Docker, machine learning, futures, leverage, portfolio optimization, and manual chart drawing.

# Context

Task 036 restores the missing numbered task document for the Fair Value Gap Pattern definition phase. The implementation-independent mechanical definition should be stored under `tasks/patterns/fair_value_gap_pattern.md`.

# Scope

- Create or update the Fair Value Gap Pattern mechanical definition document.
- Keep the work documentation-only.
- Reuse previously defined core indicator modules by reference.
- Define deterministic inputs, three-candle structure rules, gap validation, FVG states, scoring, outputs, risk reference levels, and edge-case handling.

# Out of Scope

- Application code implementation.
- Real or paper order execution.
- Exchange API integration.
- Position sizing implementation.
- Backtesting engine implementation.
- Live order placement.
- Machine learning model.
- UI visualization.
- Manual chart drawing.
- New shared contract redesigns unless a future task explicitly requests them.

# Requirements

- Define bullish and bearish Fair Value Gap detection.
- Use exactly three consecutive candles for the FVG structure.
- Define Candle 2 as the middle candle used for displacement and volume validation.
- Define bullish and bearish gap rules and zone boundaries.
- Use ATR to normalize and validate minimum and maximum gap size.
- Use default gap-size bounds `minimum_gap_size_atr_multiplier = 0.1` and `maximum_gap_size_atr_multiplier = 2.0`.
- Define whether middle-candle displacement is required, with `require_displacement_candle = true` recommended initially.
- Use default middle-candle volume confirmation `minimum_volume_ratio = 1.3` and strong confirmation `volume_ratio >= 1.5`.
- Require `liquidity_pass = true` and `spread_pass = true` before pattern validation.
- Define FVG states: `FRESH`, `TOUCHED`, `PARTIALLY_FILLED`, `FILLED`, `BROKEN`, `INVALID`.
- Define fill ratio and state mapping.
- Define optional swing-structure and support/resistance context handling.
- Define allowed direction values: `BULLISH`, `BEARISH`, `NONE`.
- Define allowed status values: `VALID`, `WEAK`, `INVALID`, `PENDING`.
- Define score components from `0.0` to `1.0`.
- Define entry, stop, and target references without order execution.
- Handle all listed edge cases explicitly.
- Avoid implementation code beyond pseudocode-level logic.
- Do not include a final summary section in the mechanical definition document.

# Status Tracking

## Before Documentation

- [ ] Read `STATUS.md`.
- [ ] Confirm the task matches the current phase and step.
- [ ] Confirm the current active task is recorded or should be updated.
- [ ] Confirm parallel work is allowed before starting any parallel tasks.
- [ ] Record assumptions, blockers, or unclear status items before editing.

## After Documentation

- [ ] Update `STATUS.md` if the phase, step, goal, active task, blocker, open question, or completion state changed.
- [ ] Mark checklist items complete only when acceptance criteria and verification are satisfied.
- [ ] Leave uncertain items open and document the uncertainty.
- [ ] Confirm the next step is accurate or explicitly left undecided.

# Acceptance Criteria

- `tasks/036_FAIR_VALUE_GAP_PATTERN.md` exists as the numbered Task 036 definition.
- The mechanical definition deliverable exists under `tasks/patterns/fair_value_gap_pattern.md`.
- The mechanical definition is Markdown and is limited to documentation/pseudocode-level logic.
- The mechanical definition covers all required core modules, optional modules, input data, bullish and bearish detection, three-candle structure, gap-size validation, displacement requirements, volume confirmation, liquidity/spread requirements, FVG state handling, fill ratio, structure context, support/resistance context, output schema, score components, risk references, edge cases, and non-goals.
- No application code is changed by this task.

# Required Tests

## Unit Tests

- Not required because this is a documentation-only task.

## Integration Tests

- Not required because this is a documentation-only task.

## Contract Tests

- Not required because this task does not change runtime contracts.

## Safety Tests

- Confirm no real trading behavior, exchange order API calls, credentials, or `.env` files are introduced.

# Verification

Required:

```bash
git diff --check
```

Optional:

```bash
git status --short
```

# Codex Self-Review Requirement

Before completion, run through `reviews/CODEX_SELF_REVIEW.md` and include the result in the final summary.

# Completion Summary Required

- files changed
- implementation summary
- tests added or updated
- tests run
- Codex self-review result
- known limitations
- recommended next task
