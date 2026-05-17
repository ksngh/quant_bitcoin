# Task 035: Order Block Pattern Mechanical Definition

# Goal

Create a concise Markdown technical specification for mechanically detecting the Order Block Pattern.

This task is documentation-only. It must not implement pattern detection code, trading execution, exchange integration, backtesting engine changes, live order placement, machine learning, UI visualization, or manual chart drawing.

# Source Requirement

## Task Purpose

Create a mechanical specification for detecting the Order Block Pattern.

This task does not include implementation.

The output of this task should be a design document that defines how an Order Block can be detected using previously defined core indicator modules.

## Target Pattern

```text
Order Block
```

## Pattern Category

```text
Supply / Demand Zone
Institutional Imbalance Zone
Structure-Based Reversal or Continuation Zone
```

## Required Core Indicator Modules

This pattern must reuse the following core modules:

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

## Required Input Data

The pattern document must define how to use the following inputs:

```text
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

## Main Detection Objective

The document must define how to detect bullish and bearish order blocks mechanically.

The pattern should support both directions:

```text
Bullish Order Block
Bearish Order Block
```

## Bullish Order Block Concept

A bullish order block is the last bearish candle before a strong bullish displacement move.

General structure:

```text
1. Market forms a bearish candle or bearish candle cluster.
2. A strong bullish displacement candle appears after it.
3. The displacement move breaks structure or moves strongly away from the zone.
4. The last bearish candle before displacement becomes a bullish order block zone.
5. Later price may return to this zone and react upward.
```

## Bearish Order Block Concept

A bearish order block is the last bullish candle before a strong bearish displacement move.

General structure:

```text
1. Market forms a bullish candle or bullish candle cluster.
2. A strong bearish displacement candle appears after it.
3. The displacement move breaks structure or moves strongly away from the zone.
4. The last bullish candle before displacement becomes a bearish order block zone.
5. Later price may return to this zone and react downward.
```

## Mechanical Requirements

The pattern document must define:

```text
1. How to identify displacement candles
2. How to locate the source candle before displacement
3. How to define the order block zone
4. How to validate bullish order blocks
5. How to validate bearish order blocks
6. How to use swing structure confirmation
7. How to use support / resistance context
8. How to apply ATR-based minimum move validation
9. How to apply volume confirmation
10. How to classify fresh, mitigated, invalidated, and broken order blocks
11. How to score the order block
12. How to define entry, stop, and target references
```

## Order Block Source Candle Requirements

The document must define source candles as follows.

For bullish order block:

```text
source candle = last bearish candle before bullish displacement
```

For bearish order block:

```text
source candle = last bullish candle before bearish displacement
```

The document must define whether to allow:

```text
single-candle order block
multi-candle order block
candle body zone
full candle range zone
wick-adjusted zone
```

## Displacement Requirements

The document must require displacement after the source candle.

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

The displacement should satisfy:

```text
body_ratio >= configured threshold
candle_range >= ATR multiplier threshold
volume_ratio >= configured threshold
close near directional extreme
```

## Structure Confirmation Requirements

The document must define optional or required structure confirmation.

For bullish order block:

```text
displacement should break a previous pivot high
or shift market structure from bearish to bullish
```

For bearish order block:

```text
displacement should break a previous pivot low
or shift market structure from bullish to bearish
```

Supported structure events:

```text
Break of Structure, BOS
Change of Character, CHoCH
Market Structure Shift, MSS
```

The document should avoid subjective terminology unless mechanically defined.

## Order Block Zone Requirements

The document must define the order block zone boundaries.

Supported zone definitions:

```text
Full range zone
Body-only zone
Wick-adjusted zone
```

Recommended initial version:

```text
Full range zone
```

Bullish order block full range:

```text
zone_low = source_candle.low
zone_high = source_candle.high
```

Bearish order block full range:

```text
zone_low = source_candle.low
zone_high = source_candle.high
```

Optional body-only version:

Bullish:

```text
zone_low = source_candle.low
zone_high = source_candle.open
```

Bearish:

```text
zone_low = source_candle.close
zone_high = source_candle.high
```

## Zone State Requirements

The document must define order block states.

Allowed values:

```text
FRESH
TOUCHED
MITIGATED
BROKEN
INVALID
```

## Fresh Order Block

An order block is fresh when price has not returned to the zone after displacement.

```text
price has not touched zone after order block creation
```

## Touched Order Block

An order block is touched when price returns to the zone.

Bullish:

```text
low <= zone_high
and
close >= zone_low
```

Bearish:

```text
high >= zone_low
and
close <= zone_high
```

## Mitigated Order Block

An order block is mitigated when price enters the zone by a configured percentage.

Example:

```text
mitigation_depth >= configured threshold
```

Default:

```text
mitigation_threshold = 0.5
```

Meaning:

```text
price filled at least 50% of the order block zone
```

## Broken Order Block

Bullish order block is broken when:

```text
close < zone_low - ATR buffer
```

Bearish order block is broken when:

```text
close > zone_high + ATR buffer
```

## Invalid Order Block

An order block is invalid when:

```text
source candle is invalid
displacement is missing
liquidity filter fails
spread filter fails
zone is broken
zone is too large
zone is too small
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

## Volume Confirmation Requirements

The displacement candle should satisfy:

```text
volume_ratio >= minimum_volume_ratio
```

Default:

```text
minimum_volume_ratio = 1.5
```

Optional weak confirmation:

```text
volume_ratio >= 1.3
```

## ATR Requirements

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

## Zone Size Requirements

The document must reject zones that are too large or too small.

Zone size:

```text
zone_size = zone_high - zone_low
```

Minimum zone size:

```text
zone_size >= minimum_zone_size_atr_multiplier * ATR
```

Maximum zone size:

```text
zone_size <= maximum_zone_size_atr_multiplier * ATR
```

Default:

```text
minimum_zone_size_atr_multiplier = 0.1
maximum_zone_size_atr_multiplier = 2.0
```

## Pattern Output Requirements

The pattern document must define an output schema containing at least:

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

## Order Block State Values

Allowed values:

```text
FRESH
TOUCHED
MITIGATED
BROKEN
INVALID
```

## Pattern Score Requirements

The document must define a score from `0.0` to `1.0`.

The score should include:

```text
displacement_score
volume_confirmation_score
structure_confirmation_score
zone_quality_score
liquidity_score
support_resistance_context_score
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

For bullish order block:

```text
entry_reference = zone_high, zone_mid, or zone_low
stop_reference = zone_low - ATR buffer
target_reference = nearest resistance zone or risk-reward based target
```

For bearish order block:

```text
entry_reference = zone_low, zone_mid, or zone_high
stop_reference = zone_high + ATR buffer
target_reference = nearest support zone or risk-reward based target
```

## Edge Cases to Define

The pattern document must handle:

```text
no displacement candle
displacement candle without volume confirmation
source candle not found
multiple source candles
overlapping order blocks
order block too large
order block too small
order block already mitigated
order block already broken
price returns to zone immediately
low liquidity market
wide spread market
conflicting swing structure
order block inside major support zone
order block inside major resistance zone
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
Order Block Pattern Mechanical Definition
```

It must be written as a concise Markdown technical specification.

It must reuse the previously defined core indicator modules.

It must not include actual implementation code beyond pseudocode-level logic.

It must not include a final summary section.

# Extracted Roles

- Owner role: Pattern mechanical definition for Order Block detection.
- Supporting roles:
  - Displacement Candle, as the required impulse candle source.
  - Pivot High / Pivot Low, as structure-break reference points.
  - Swing Structure, as BOS, CHoCH, MSS, and directional context input.
  - ATR, as displacement, zone-size, broken-zone, and stop-reference input.
  - Volume Ratio, as displacement volume-confirmation input.
  - Support / Resistance Zone, as contextual target and zone-overlap input.
  - Liquidity: Trading Value / Volume, as the required tradability filter.
  - Bid-Ask Spread, as the required execution-quality filter.
- Forbidden roles:
  - Execution, because this task must not place, simulate, or route orders.
  - Exchange integration, because this task must not call real exchange APIs.
  - Risk management and position sizing, because this task only defines reference levels.
  - Backtesting engine, live trading, database, dashboard, scheduler, FastAPI, Streamlit, Docker, machine learning, futures, leverage, portfolio optimization, and manual chart drawing.

# Context

Task 035 restores the missing numbered task document for the Order Block Pattern definition phase. The implementation-independent mechanical definition should be stored under `tasks/patterns/order_block_pattern.md`.

# Scope

- Create or update the Order Block Pattern mechanical definition document.
- Keep the work documentation-only.
- Reuse previously defined core indicator modules by reference.
- Define deterministic inputs, source-candle selection, displacement validation, zone rules, state classification, scoring, outputs, risk reference levels, and edge-case handling.

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

- Define bullish and bearish Order Block detection.
- Require a valid displacement candle after the source candle.
- Define source candle selection for bullish and bearish order blocks.
- Define full-range, body-only, and wick-adjusted zone options, with full-range as the recommended initial version.
- Define order block states: `FRESH`, `TOUCHED`, `MITIGATED`, `BROKEN`, `INVALID`.
- Require `liquidity_pass = true` and `spread_pass = true` before pattern validation.
- Use default volume confirmation `minimum_volume_ratio = 1.5` and weak confirmation `volume_ratio >= 1.3`.
- Use ATR for displacement validation, zone size validation, broken-zone validation, and stop reference calculation.
- Use default minimum displacement move `minimum_displacement_atr_multiplier = 1.5`.
- Use default zone-size bounds `minimum_zone_size_atr_multiplier = 0.1` and `maximum_zone_size_atr_multiplier = 2.0`.
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

- `tasks/035_ORDER_BLOCK_PATTERN.md` exists as the numbered Task 035 definition.
- The mechanical definition deliverable exists under `tasks/patterns/order_block_pattern.md`.
- The mechanical definition is Markdown and is limited to documentation/pseudocode-level logic.
- The mechanical definition covers all required core modules, input data, bullish and bearish detection, source-candle selection, displacement requirements, structure confirmation, zone definitions, zone states, liquidity/spread requirements, volume and ATR requirements, zone size bounds, output schema, score components, risk references, edge cases, and non-goals.
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
