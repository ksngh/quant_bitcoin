# Task 038: Diamond Pattern Mechanical Definition

# Goal

Create a concise Markdown technical specification for mechanically detecting the Diamond Pattern.

This task is documentation-only. It must not implement pattern detection code, trading execution, exchange integration, backtesting engine changes, live order placement, machine learning, UI visualization, or manual chart drawing.

# Source Requirement

## Task Request

Create a mechanical design document for the Diamond Pattern.

This task must produce a pattern definition document that can later be used by an AI coding agent or developer to implement the module.

The next document after this task must be:

```text
Diamond Pattern Mechanical Definition
```

This task does not include implementation.

## Task Purpose

Define the work required to mechanically detect the Diamond Pattern using previously defined core indicator modules.

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
Diamond Pattern
```

## Pattern Category

```text
Volatility Expansion-Contraction Pattern
Breakout Pattern
Breakdown Pattern
Potential Reversal Pattern
Potential Continuation Pattern
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

The document must define how to detect a Diamond Pattern mechanically.

The pattern should be interpreted as:

```text
volatility expansion followed by volatility contraction
```

The pattern should not assume direction before breakout.

Supported directions:

```text
BULLISH
BEARISH
NONE
```

## Diamond Pattern Concept

A Diamond Pattern consists of two structural phases:

```text
Expansion phase
Contraction phase
```

Expansion phase:

```text
pivot highs rise
pivot lows fall
price range expands
```

Contraction phase:

```text
pivot highs fall
pivot lows rise
price range contracts
```

The trade direction is determined only after price breaks the upper or lower boundary.

## Mechanical Requirements

The pattern document must define:

```text
how to identify expansion phase
how to identify contraction phase
how to select pivot highs and pivot lows
how to validate alternating pivot structure
how to calculate pattern range expansion
how to calculate pattern range contraction
how to build upper boundary
how to build lower boundary
how to validate bullish breakout
how to validate bearish breakdown
how to apply ATR breakout buffer
how to apply volume confirmation
how to apply liquidity and spread filters
how to optionally use displacement candle confirmation
how to score the pattern
how to define entry, stop, and target references
```

## Pivot Structure Requirements

The document must define the Diamond Pattern using confirmed pivots only.

Required pivot sequence should include at least:

```text
pivot high 1
pivot low 1
pivot high 2
pivot low 2
pivot high 3
pivot low 3
```

The exact pivot order may vary, but the structure must show:

```text
early expansion
later contraction
```

Minimum pivot count:

```text
minimum_pivot_count = 6
```

Recommended pivot count:

```text
6 to 10 pivots
```

## Expansion Phase Requirements

The expansion phase must show widening volatility.

Mechanical conditions:

```text
later pivot high > earlier pivot high
later pivot low < earlier pivot low
```

Range expansion condition:

```text
expansion_range_end > expansion_range_start
```

The document must define how to calculate:

```text
expansion_high_slope
expansion_low_slope
expansion_range_change
```

Expected signs:

```text
expansion_high_slope > 0
expansion_low_slope < 0
expansion_range_change > 0
```

## Contraction Phase Requirements

The contraction phase must show narrowing volatility.

Mechanical conditions:

```text
later pivot high < earlier pivot high
later pivot low > earlier pivot low
```

Range contraction condition:

```text
contraction_range_end < contraction_range_start
```

The document must define how to calculate:

```text
contraction_high_slope
contraction_low_slope
contraction_range_change
```

Expected signs:

```text
contraction_high_slope < 0
contraction_low_slope > 0
contraction_range_change < 0
```

## Diamond Center Requirements

The document must define a center point that separates expansion and contraction phases.

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

The document must define how to split pivots into:

```text
expansion_pivots before or near center
contraction_pivots after center
```

## Boundary Requirements

The document must define upper and lower pattern boundaries.

Upper boundary should be built from pivot highs.

Lower boundary should be built from pivot lows.

Expansion boundaries:

```text
expanding upper boundary
expanding lower boundary
```

Contraction boundaries:

```text
contracting upper boundary
contracting lower boundary
```

For breakout validation, use the latest contraction boundaries.

Bullish breakout boundary:

```text
contracting_upper_boundary
```

Bearish breakdown boundary:

```text
contracting_lower_boundary
```

## Breakout Requirements

Bullish breakout occurs when:

```text
close > upper_boundary_value + breakout_atr_multiplier * ATR
```

Bearish breakdown occurs when:

```text
close < lower_boundary_value - breakout_atr_multiplier * ATR
```

Default:

```text
breakout_atr_multiplier = 0.2
```

## Volume Confirmation Requirements

The breakout or breakdown candle should satisfy:

```text
volume_ratio >= minimum_breakout_volume_ratio
```

Default:

```text
minimum_breakout_volume_ratio = 1.5
```

Weak confirmation:

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

The breakout or breakdown candle may optionally be required to be a displacement candle.

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

## Pattern Output Requirements

The pattern document must define an output schema containing at least:

```text
symbol
timestamp
pattern_type
direction
pattern_status
expansion_start_index
diamond_center_index
contraction_end_index
upper_boundary_slope
lower_boundary_slope
upper_boundary_value
lower_boundary_value
expansion_range_change
contraction_range_change
pattern_height
pattern_height_atr
breakout_index
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

## Pattern Score Requirements

The document must define a score from `0.0` to `1.0`.

The score should include:

```text
expansion_quality_score
contraction_quality_score
boundary_quality_score
breakout_strength_score
volume_confirmation_score
liquidity_score
```

Optional:

```text
displacement_score
support_resistance_context_score
```

## Risk Reference Requirements

The document must define reference levels, not actual order execution.

Required:

```text
entry_reference
stop_reference
target_reference
```

For bullish Diamond Pattern:

```text
entry_reference = breakout close or next candle open
stop_reference = lower contraction boundary or nearest swing low
target_reference = breakout price + pattern height
```

For bearish Diamond Pattern:

```text
entry_reference = breakdown close or next candle open
stop_reference = upper contraction boundary or nearest swing high
target_reference = breakdown price - pattern height
```

Alternative target:

```text
target_reference = entry_reference +/- 2 * abs(entry_reference - stop_reference)
```

## Edge Cases to Define

The pattern document must handle:

```text
not enough pivots
unconfirmed pivots
no clear expansion phase
no clear contraction phase
expansion without contraction
contraction without prior expansion
flat upper boundary
flat lower boundary
overlapping diamond candidates
too short pattern duration
too long pattern duration
pattern height too small
pattern height too large
breakout missing
breakout without ATR buffer
breakout without volume confirmation
low liquidity market
wide spread market
false breakout
conflicting swing structure
diamond pattern inside major support zone
diamond pattern inside major resistance zone
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
Diamond Pattern Mechanical Definition
```

It must be written as a concise Markdown technical specification.

It must reuse the previously defined core indicator modules.

It must not include actual implementation code beyond pseudocode-level logic.

It must not include a final summary section.

# Extracted Roles

- Owner role: Pattern mechanical definition for Diamond Pattern detection.
- Supporting roles:
  - Pivot High / Pivot Low, as the confirmed pivot source for expansion, contraction, center, and boundaries.
  - Swing Structure, as context for conflicting structure and optional trend interpretation.
  - ATR, as breakout-buffer, pattern-height normalization, and size-filter input.
  - Volume Ratio, as breakout or breakdown confirmation input.
  - Support / Resistance Zone, as context for major zone overlap and target/reference checks.
  - Liquidity: Trading Value / Volume, as the required tradability filter.
  - Bid-Ask Spread, as the required execution-quality filter.
  - Displacement Candle, as optional breakout/breakdown confirmation.
- Forbidden roles:
  - Execution, because this task must not place, simulate, or route orders.
  - Exchange integration, because this task must not call real exchange APIs.
  - Risk management and position sizing, because this task only defines reference levels.
  - Backtesting engine, live trading, database, dashboard, scheduler, FastAPI, Streamlit, Docker, machine learning, futures, leverage, portfolio optimization, and manual chart drawing.

# Context

Task 038 creates the numbered task document for the Diamond Pattern definition phase. The implementation-independent mechanical definition should be stored under `tasks/patterns/diamond_pattern.md`.

# Scope

- Create the Diamond Pattern mechanical definition document.
- Keep the work documentation-only.
- Reuse previously defined core indicator modules by reference.
- Define deterministic inputs, confirmed-pivot selection, expansion/contraction validation, boundary construction, breakout/breakdown validation, scoring, outputs, risk reference levels, and edge-case handling.

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

- Define Diamond Pattern detection as volatility expansion followed by volatility contraction.
- Use confirmed pivots only.
- Support direction values `BULLISH`, `BEARISH`, and `NONE`.
- Define minimum pivot count `minimum_pivot_count = 6` and recommended pivot count of 6 to 10 pivots.
- Define expansion phase conditions with rising pivot highs, falling pivot lows, and positive range change.
- Define contraction phase conditions with falling pivot highs, rising pivot lows, and negative range change.
- Define `diamond_center` as the point where local pivot range is maximum for the initial version.
- Define upper and lower boundaries from pivot highs and lows.
- Use latest contraction boundaries for breakout/breakdown validation.
- Validate bullish breakout using `close > upper_boundary_value + breakout_atr_multiplier * ATR`.
- Validate bearish breakdown using `close < lower_boundary_value - breakout_atr_multiplier * ATR`.
- Use default `breakout_atr_multiplier = 0.2`.
- Validate breakout or breakdown volume with default `minimum_breakout_volume_ratio = 1.5` and weak threshold `weak_breakout_volume_ratio = 1.3`.
- Require `liquidity_pass = true` and `spread_pass = true` before validation.
- Define optional displacement confirmation with `require_displacement_breakout = false` by default.
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

- `tasks/038_DIAMOND_PATTERN.md` exists as the numbered Task 038 definition.
- The mechanical definition deliverable exists under `tasks/patterns/diamond_pattern.md`.
- The mechanical definition is Markdown and is limited to documentation/pseudocode-level logic.
- The mechanical definition covers all required core modules, optional modules, input data, supported directions, pivot structure, expansion phase, contraction phase, diamond center, boundaries, breakout/breakdown, liquidity/spread requirements, output schema, score components, risk references, edge cases, and non-goals.
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
