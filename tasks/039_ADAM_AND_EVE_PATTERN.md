# Task 039: Adam and Eve Pattern Mechanical Definition

# Goal

Create a concise Markdown technical specification for mechanically detecting the Adam and Eve Pattern.

This task is documentation-only. It must not implement pattern detection code, trading execution, exchange integration, backtesting engine changes, live order placement, machine learning, UI visualization, or manual chart drawing.

# Source Requirement

## Task Request

Create a mechanical design document for the Adam and Eve Pattern.

This task must produce a pattern definition document that can later be used by an AI coding agent or developer to implement the module.

The next document after this task must be:

```text
Adam and Eve Pattern Mechanical Definition
```

This task does not include implementation.

## Task Purpose

Define the work required to mechanically detect the Adam and Eve Pattern using previously defined core indicator modules.

The final pattern document should specify:

```text
input data
required core modules
mechanical pattern structure
validation rules
scoring rules
edge cases
output schema
entry, stop, and target references
```

## Target Pattern

```text
Adam and Eve Pattern
```

## Pattern Category

```text
Double Bottom Pattern
Bullish Reversal Pattern
Bottom Formation Pattern
Accumulation Pattern
Neckline Breakout Pattern
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
```

Optional:

```text
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
liquidity status
bid-ask spread status
```

Optional:

```text
displacement candle snapshots
```

## Main Detection Objective

The document must define how to detect a bullish Adam and Eve Pattern mechanically.

The initial version should focus on bullish Adam and Eve.

Supported directions:

```text
BULLISH
NONE
```

Optional future extension:

```text
BEARISH_INVERTED
```

## Adam and Eve Concept

A bullish Adam and Eve Pattern consists of two bottom structures:

```text
Adam bottom
Eve bottom
neckline
breakout
```

Adam bottom:

```text
sharp V-shaped first low
fast decline and fast recovery
narrow bottom duration
high local volatility
```

Eve bottom:

```text
rounded second low
wider bottom duration
smoother recovery
lower local volatility than Adam
```

The pattern is confirmed when price breaks above the neckline.

## Mechanical Requirements

The pattern document must define:

```text
how to confirm prior downtrend
how to identify Adam low using pivot low
how to identify Eve low using pivot low
how to validate similarity between Adam low and Eve low
how to distinguish sharp Adam bottom from rounded Eve bottom
how to define neckline using pivot high between two bottoms
how to validate neckline breakout
how to apply ATR breakout buffer
how to apply volume confirmation
how to apply liquidity and spread filters
how to optionally use displacement candle confirmation
how to score the pattern
how to define entry, stop, and target references
```

## Prior Trend Requirements

The pattern document must define prior downtrend using Swing Structure.

Acceptable prior downtrend conditions:

```text
market_structure_status = DOWNTREND
```

or:

```text
recent swing labels contain LH and LL
```

The document should reject an Adam and Eve candidate if there is no prior downward structure.

## Adam and Eve Structure Requirements

The document must define the pattern using three main pivot points:

```text
adam_low = first pivot low
neckline_pivot = pivot high between Adam and Eve
eve_low = second pivot low
```

Required order:

```text
adam_low.index < neckline_pivot.index < eve_low.index
```

Breakout must occur after Eve low:

```text
breakout.index > eve_low.index
```

## Bottom Similarity Requirements

Adam low and Eve low should be near the same price level.

Mechanical condition:

```text
abs(adam_low.price - eve_low.price) / adam_low.price <= maximum_bottom_difference_rate
```

Default:

```text
maximum_bottom_difference_rate = 0.05
```

If bottoms are too different:

```text
pattern_status = INVALID
```

## Adam Bottom Requirements

Adam bottom should be sharp.

The document must define Adam sharpness using:

```text
adam_bottom_duration
adam_decline_slope
adam_recovery_slope
adam_local_range_atr
```

Adam bottom should satisfy:

```text
adam_bottom_duration <= maximum_adam_bottom_duration
```

Default:

```text
maximum_adam_bottom_duration = 5
```

Adam should have a strong local range:

```text
adam_local_range_atr >= minimum_adam_range_atr
```

Default:

```text
minimum_adam_range_atr = 1.0
```

## Eve Bottom Requirements

Eve bottom should be rounded and wider than Adam.

The document must define Eve roundness using:

```text
eve_bottom_duration
eve_bottom_zone_duration
eve_decline_slope
eve_recovery_slope
eve_local_range_atr
```

Eve bottom should satisfy:

```text
eve_bottom_duration >= minimum_eve_bottom_duration
```

Default:

```text
minimum_eve_bottom_duration = 5
```

Eve bottom zone duration should satisfy:

```text
eve_bottom_zone_duration >= minimum_eve_bottom_zone_duration
```

Default:

```text
minimum_eve_bottom_zone_duration = 3
```

## Adam vs Eve Shape Difference Requirements

The document must define how Adam and Eve differ mechanically.

Adam should be sharper than Eve:

```text
adam_bottom_duration < eve_bottom_duration
```

Eve should be wider than Adam:

```text
eve_bottom_zone_duration > adam_bottom_zone_duration
```

Recommended condition:

```text
eve_bottom_duration / adam_bottom_duration >= minimum_eve_to_adam_duration_ratio
```

Default:

```text
minimum_eve_to_adam_duration_ratio = 1.5
```

## Neckline Requirements

The neckline should be based on the pivot high between Adam low and Eve low.

Recommended neckline:

```text
neckline = neckline_pivot.price
```

Alternative:

```text
neckline = resistance_zone.center_price
```

Use resistance zone only when a valid resistance zone overlaps the neckline pivot area.

Recommended initial version:

```text
neckline = neckline_pivot.price
```

## Breakout Requirements

Bullish breakout occurs when:

```text
close > neckline + breakout_atr_multiplier * ATR
```

Default:

```text
breakout_atr_multiplier = 0.2
```

Breakout should also satisfy:

```text
volume_ratio >= minimum_breakout_volume_ratio
```

Default:

```text
minimum_breakout_volume_ratio = 1.5
```

Weak breakout volume:

```text
volume_ratio >= weak_breakout_volume_ratio
```

Default:

```text
weak_breakout_volume_ratio = 1.3
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

## Optional Displacement Candle Requirement

The breakout candle may optionally be required to be a bullish displacement candle.

Recommended initial version:

```text
require_displacement_breakout = false
```

If true:

```text
breakout candle displacement_direction = BULLISH
breakout candle displacement_status = VALID
```

## Pattern Output Requirements

The pattern document must define an output schema containing at least:

```text
symbol
timestamp
pattern_type
direction
pattern_status
adam_low_index
neckline_pivot_index
eve_low_index
breakout_index
adam_low_price
neckline
eve_low_price
bottom_difference_rate
adam_bottom_duration
eve_bottom_duration
adam_local_range_atr
eve_local_range_atr
eve_to_adam_duration_ratio
breakout_price
breakout_distance
breakout_distance_atr
volume_ratio
liquidity_pass
spread_pass
displacement_confirmed
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
NONE
```

Optional future value:

```text
BEARISH_INVERTED
```

## Pattern Status Values

Allowed values:

```text
VALID
WEAK
INVALID
PENDING
```

## Pattern Score Requirements

The document must define a score from `0.0` to `1.0`.

The score should include:

```text
prior_downtrend_score
bottom_similarity_score
adam_sharpness_score
eve_roundness_score
neckline_quality_score
breakout_strength_score
volume_confirmation_score
liquidity_score
```

Optional:

```text
support_resistance_context_score
displacement_score
```

## Risk Reference Requirements

The document must define reference levels, not actual order execution.

Required:

```text
entry_reference
stop_reference
target_reference
```

For bullish Adam and Eve:

```text
entry_reference = breakout close or next candle open
stop_reference = min(adam_low.price, eve_low.price) - ATR buffer
target_reference = neckline + pattern_height
```

Pattern height:

```text
pattern_height = neckline - min(adam_low.price, eve_low.price)
```

Alternative target:

```text
target_reference = entry_reference + 2 * abs(entry_reference - stop_reference)
```

## Edge Cases to Define

The pattern document must handle:

```text
no prior downtrend
not enough pivots
Adam low missing
Eve low missing
neckline pivot missing
bottom prices too different
Adam bottom not sharp
Eve bottom not rounded
Eve bottom not wider than Adam
neckline too low
neckline too high
breakout missing
breakout without ATR buffer
breakout without volume confirmation
low liquidity market
wide spread market
overlapping Adam and Eve candidates
multiple possible neckline pivots
multiple possible Eve lows
false breakout
pattern formed inside major resistance zone
pattern formed below major support zone
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
Adam and Eve Pattern Mechanical Definition
```

It must be written as a concise Markdown technical specification.

It must reuse the previously defined core indicator modules.

It must not include actual implementation code beyond pseudocode-level logic.

It must not include a final summary section.

# Extracted Roles

- Owner role: Pattern mechanical definition for Adam and Eve detection.
- Supporting roles:
  - Pivot High / Pivot Low, as the source for Adam low, neckline pivot, and Eve low.
  - Swing Structure, as prior downtrend and swing-label context input.
  - ATR, as breakout-buffer, local-range, stop-reference, and volatility normalization input.
  - Volume Ratio, as breakout confirmation input.
  - Support / Resistance Zone, as neckline context, support/resistance context, and target reference input.
  - Liquidity: Trading Value / Volume, as the required tradability filter.
  - Bid-Ask Spread, as the required execution-quality filter.
  - Displacement Candle, as optional bullish breakout confirmation.
- Forbidden roles:
  - Execution, because this task must not place, simulate, or route orders.
  - Exchange integration, because this task must not call real exchange APIs.
  - Risk management and position sizing, because this task only defines reference levels.
  - Backtesting engine, live trading, database, dashboard, scheduler, FastAPI, Streamlit, Docker, machine learning, futures, leverage, portfolio optimization, and manual chart drawing.

# Context

Task 039 creates the numbered task document for the Adam and Eve Pattern definition phase. The implementation-independent mechanical definition should be stored under `tasks/patterns/adam_and_eve_pattern.md`.

# Scope

- Create the Adam and Eve Pattern mechanical definition document.
- Keep the work documentation-only.
- Reuse previously defined core indicator modules by reference.
- Define deterministic inputs, prior-downtrend validation, Adam/Eve pivot structure, bottom similarity, Adam sharpness, Eve roundness, neckline, breakout validation, scoring, outputs, risk reference levels, and edge-case handling.

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
- Bearish inverted implementation beyond an optional future direction value.
- New shared contract redesigns unless a future task explicitly requests them.

# Requirements

- Define bullish Adam and Eve detection.
- Use Swing Structure to require a prior downtrend or recent LH/LL structure.
- Use confirmed pivot lows for Adam low and Eve low.
- Use a confirmed pivot high between them as the neckline pivot.
- Require `adam_low.index < neckline_pivot.index < eve_low.index`.
- Require breakout after Eve low.
- Define bottom similarity using `maximum_bottom_difference_rate = 0.05` by default.
- Use default pattern duration bounds `minimum_pattern_duration = 20` and `maximum_pattern_duration = 200`.
- Define Adam sharpness using bottom duration, local range ATR, and decline/recovery slopes.
- Use defaults `maximum_adam_bottom_duration = 5` and `minimum_adam_range_atr = 1.0`.
- Define Eve roundness using a bottom zone, bottom-zone duration, and Eve bottom duration.
- Use defaults `minimum_eve_bottom_duration = 5`, `minimum_eve_bottom_zone_duration = 3`, and `bottom_zone_atr_multiplier = 0.5`.
- Define shape difference with `minimum_eve_to_adam_duration_ratio = 1.5` by default.
- Define neckline using `neckline = neckline_pivot.price` for the initial version, with resistance-zone neckline as an alternative.
- Define pattern height using `minimum_pattern_height_atr = 1.0` and `maximum_pattern_height_atr = 8.0`.
- Validate bullish breakout using `close > neckline + breakout_atr_multiplier * ATR` with default `breakout_atr_multiplier = 0.2`.
- Validate breakout volume using default `minimum_breakout_volume_ratio = 1.5` and weak threshold `weak_breakout_volume_ratio = 1.3`.
- Require `liquidity_pass = true` and `spread_pass = true` before validation.
- Define optional breakout displacement confirmation with `require_displacement_breakout = false` by default.
- Define allowed direction values `BULLISH` and `NONE`, with optional future `BEARISH_INVERTED`.
- Define allowed status values `VALID`, `WEAK`, `INVALID`, and `PENDING`.
- Define score components from `0.0` to `1.0` using the owner-provided component weights.
- Define entry, stop, target, and risk-reward references without order execution.
- Include the owner-provided output schema, output fields, edge cases, detection logic, pseudocode, domain-model example, recommended initial configuration, and final mechanical rule.
- Avoid implementation code beyond documentation and pseudocode-level logic.

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

- `tasks/039_ADAM_AND_EVE_PATTERN.md` exists as the numbered Task 039 definition.
- The mechanical definition deliverable exists under `tasks/patterns/adam_and_eve_pattern.md`.
- The mechanical definition is Markdown and is limited to documentation/pseudocode-level logic.
- The mechanical definition covers all required core modules, optional modules, input data, supported directions, prior downtrend, Adam/Eve structure, bottom similarity, Adam sharpness, Eve roundness, shape difference, neckline, pattern height, breakout, liquidity/spread requirements, output schema, score components, risk references, edge cases, detection logic, pseudocode, recommended initial configuration, final mechanical rule, and non-goals.
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
