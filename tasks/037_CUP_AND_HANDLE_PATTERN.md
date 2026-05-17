# Task 037: Cup and Handle Pattern Mechanical Definition

# Goal

Create a concise Markdown technical specification for mechanically detecting the Cup and Handle Pattern.

This task is documentation-only. It must not implement pattern detection code, trading execution, exchange integration, backtesting engine changes, live order placement, machine learning, UI visualization, or manual chart drawing.

# Source Requirement

## Task Request

Create a mechanical design document for the Cup and Handle Pattern.

This task must produce a pattern definition document that can later be used by an AI coding agent or developer to implement the module.

The next document after this task must be:

```text
Cup and Handle Pattern Mechanical Definition
```

This task does not include implementation.

## Task Purpose

Define the work required to mechanically detect the Cup and Handle Pattern using previously defined core indicator modules.

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
Cup and Handle Pattern
```

## Pattern Category

```text
Continuation Pattern
Bullish Breakout Pattern
Rounded Base Pattern
Accumulation Pattern
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

The document must define how to detect a Cup and Handle Pattern mechanically.

The initial version should focus on bullish Cup and Handle.

Supported direction:

```text
BULLISH
```

Optional future extension:

```text
BEARISH_INVERTED
```

## Cup and Handle Concept

A bullish Cup and Handle Pattern consists of:

```text
prior uptrend
left rim
rounded cup bottom
right rim
handle pullback
neckline or rim resistance
breakout above neckline
volume confirmation
```

## Mechanical Requirements

The pattern document must define:

```text
how to confirm prior uptrend
how to identify left rim using pivot high
how to identify cup bottom using pivot low
how to identify right rim using pivot high
how to validate rim similarity
how to validate cup depth
how to validate cup duration
how to reject V-shaped cups
how to identify handle pullback
how to validate handle depth
how to validate handle duration
how to define neckline
how to validate neckline breakout
how to apply ATR breakout buffer
how to apply volume confirmation
how to apply liquidity and spread filters
how to score the pattern
how to define entry, stop, and target references
```

## Prior Trend Requirements

The pattern document must define prior uptrend using Swing Structure.

Acceptable prior uptrend conditions:

```text
market_structure_status = UPTREND
```

or:

```text
recent swing labels contain HH and HL
```

The document should reject a Cup and Handle candidate if there is no prior upward structure.

## Cup Structure Requirements

The document must define the cup using three main pivot points:

```text
left_rim = pivot high
cup_bottom = pivot low
right_rim = pivot high
```

Required order:

```text
left_rim.index < cup_bottom.index < right_rim.index
```

## Rim Similarity Requirements

The left rim and right rim should be near the same price level.

Mechanical condition:

```text
abs(left_rim.price - right_rim.price) / left_rim.price <= maximum_rim_difference_rate
```

Default:

```text
maximum_rim_difference_rate = 0.05
```

## Cup Depth Requirements

Cup depth:

```text
cup_depth = min(left_rim.price, right_rim.price) - cup_bottom.price
```

Cup depth rate:

```text
cup_depth_rate = cup_depth / min(left_rim.price, right_rim.price)
```

The document must define valid cup depth range.

Default:

```text
minimum_cup_depth_rate = 0.10
maximum_cup_depth_rate = 0.40
```

If cup is too shallow:

```text
pattern_status = INVALID
```

If cup is too deep:

```text
pattern_status = INVALID
```

## Cup Duration Requirements

Cup duration:

```text
cup_duration = right_rim.index - left_rim.index
```

Default:

```text
minimum_cup_duration = 20
maximum_cup_duration = 200
```

The document must reject cups that are too short or too long.

## Cup Roundness Requirements

The document must define how to distinguish a rounded cup from a V-shaped recovery.

Recommended mechanical checks:

```text
bottom_zone_duration
left_decline_duration
right_recovery_duration
slope balance
multiple candles near cup bottom
```

The document should require the cup bottom to persist for more than one candle or one pivot area.

Example condition:

```text
bottom_zone_duration >= minimum_bottom_zone_duration
```

Default:

```text
minimum_bottom_zone_duration = 3
```

## Handle Requirements

The handle occurs after the right rim.

Required structure:

```text
right_rim.index < handle_low.index < breakout.index
```

Handle should be a shallow pullback.

Handle depth:

```text
handle_depth = right_rim.price - handle_low.price
```

Handle depth relative to cup depth:

```text
handle_depth_ratio = handle_depth / cup_depth
```

Default valid range:

```text
handle_depth_ratio <= 0.35
```

If handle is too deep:

```text
pattern_status = INVALID
```

## Handle Duration Requirements

```text
handle_duration = breakout.index - right_rim.index
```

Default:

```text
minimum_handle_duration = 3
maximum_handle_duration = 40
```

## Neckline Requirements

The neckline should be based on the rim resistance zone.

Recommended neckline:

```text
neckline = max(left_rim.price, right_rim.price)
```

Alternative:

```text
neckline = resistance_zone.center_price
```

Recommended initial version:

```text
neckline = max(left_rim.price, right_rim.price)
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
left_rim_index
cup_bottom_index
right_rim_index
handle_low_index
breakout_index
left_rim_price
cup_bottom_price
right_rim_price
handle_low_price
neckline
cup_depth
cup_depth_rate
cup_duration
handle_depth
handle_depth_ratio
handle_duration
breakout_price
breakout_distance_atr
volume_ratio
liquidity_pass
spread_pass
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
prior_trend_score
cup_shape_score
rim_similarity_score
handle_quality_score
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

For bullish Cup and Handle:

```text
entry_reference = breakout close or next candle open
stop_reference = handle low or neckline retest failure level
target_reference = neckline + cup_depth
```

Alternative target:

```text
target_reference = entry_reference + 2 * abs(entry_reference - stop_reference)
```

## Edge Cases to Define

The pattern document must handle:

```text
no prior uptrend
not enough pivots
left rim missing
cup bottom missing
right rim missing
rim prices too different
cup too shallow
cup too deep
cup duration too short
cup duration too long
V-shaped recovery
handle missing
handle too deep
handle too long
breakout missing
breakout without ATR buffer
breakout without volume confirmation
low liquidity market
wide spread market
overlapping cup candidates
multiple possible handles
false breakout
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
Cup and Handle Pattern Mechanical Definition
```

It must be written as a concise Markdown technical specification.

It must reuse the previously defined core indicator modules.

It must not include actual implementation code beyond pseudocode-level logic.

It must not include a final summary section.

# Extracted Roles

- Owner role: Pattern mechanical definition for Cup and Handle detection.
- Supporting roles:
  - Pivot High / Pivot Low, as the source for left rim, cup bottom, right rim, and handle low.
  - Swing Structure, as prior uptrend and swing-label context input.
  - ATR, as breakout-buffer, volatility, and normalized-distance input.
  - Volume Ratio, as breakout confirmation input.
  - Support / Resistance Zone, as neckline/resistance context and target reference input.
  - Liquidity: Trading Value / Volume, as the required tradability filter.
  - Bid-Ask Spread, as the required execution-quality filter.
  - Displacement Candle, as optional bullish breakout confirmation.
- Forbidden roles:
  - Execution, because this task must not place, simulate, or route orders.
  - Exchange integration, because this task must not call real exchange APIs.
  - Risk management and position sizing, because this task only defines reference levels.
  - Backtesting engine, live trading, database, dashboard, scheduler, FastAPI, Streamlit, Docker, machine learning, futures, leverage, portfolio optimization, and manual chart drawing.

# Context

Task 037 creates the numbered task document for the Cup and Handle Pattern definition phase. The implementation-independent mechanical definition should be stored under `tasks/patterns/cup_and_handle_pattern.md`.

# Scope

- Create the Cup and Handle Pattern mechanical definition document.
- Keep the work documentation-only.
- Reuse previously defined core indicator modules by reference.
- Define deterministic inputs, pivot-based cup structure, prior-trend validation, cup validation, handle validation, breakout validation, scoring, outputs, risk reference levels, and edge-case handling.

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

- Define bullish Cup and Handle detection.
- Use Swing Structure to require a prior uptrend or recent HH/HL structure.
- Use confirmed pivot highs for left and right rims.
- Use a confirmed pivot low for the cup bottom.
- Require `left_rim.index < cup_bottom.index < right_rim.index`.
- Define rim similarity using `maximum_rim_difference_rate = 0.05` by default.
- Define cup depth and cup depth rate with defaults `minimum_cup_depth_rate = 0.10` and `maximum_cup_depth_rate = 0.40`.
- Define cup duration with defaults `minimum_cup_duration = 20` and `maximum_cup_duration = 200`.
- Define cup roundness rules to reject V-shaped recoveries.
- Define handle low, handle depth, handle depth ratio, and handle duration.
- Use default `handle_depth_ratio <= 0.35`.
- Use default handle duration bounds `minimum_handle_duration = 3` and `maximum_handle_duration = 40`.
- Define neckline using `neckline = max(left_rim.price, right_rim.price)` for the initial version.
- Validate bullish breakout using `close > neckline + breakout_atr_multiplier * ATR` with default `breakout_atr_multiplier = 0.2`.
- Validate breakout volume using default `minimum_breakout_volume_ratio = 1.5`.
- Require `liquidity_pass = true` and `spread_pass = true` before validation.
- Define optional breakout displacement confirmation with `require_displacement_breakout = false` by default.
- Define allowed direction values `BULLISH` and `NONE`, with optional future `BEARISH_INVERTED`.
- Define allowed status values `VALID`, `WEAK`, `INVALID`, and `PENDING`.
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

- `tasks/037_CUP_AND_HANDLE_PATTERN.md` exists as the numbered Task 037 definition.
- The mechanical definition deliverable exists under `tasks/patterns/cup_and_handle_pattern.md`.
- The mechanical definition is Markdown and is limited to documentation/pseudocode-level logic.
- The mechanical definition covers all required core modules, optional modules, input data, bullish detection, prior uptrend, cup structure, rim similarity, cup depth, cup duration, cup roundness, handle pullback, neckline, breakout, liquidity/spread requirements, output schema, score components, risk references, edge cases, and non-goals.
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
