# Task 034: Trendline Break Pattern Mechanical Definition

# Goal

Create a concise Markdown technical specification for mechanically detecting the Trendline Break Pattern.

This task is documentation-only. It must not implement pattern detection code, trading execution, exchange integration, backtesting engine changes, live order placement, machine learning, or UI visualization.

# Source Requirement

## Task Purpose

Create a mechanical specification for detecting the Trendline Break Pattern.

This task does not include implementation.

The output of this task should be a design document that defines how the pattern can be detected using previously defined core indicator modules.

## Target Pattern

```text
Trendline Break Pattern
```

## Pattern Category

```text
Structure Break
Breakout / Breakdown
Trend Reversal or Trend Continuation
```

## Required Core Indicator Modules

This pattern must reuse the following core modules:

```text
Pivot High / Pivot Low
Swing Structure
ATR
Volume Ratio
Support / Resistance Zone
Liquidity: Trading Value / Volume
Bid-Ask Spread
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
swing structure labels
ATR values
volume ratio values
support / resistance zones
liquidity status
bid-ask spread status
```

## Main Detection Objective

The document must define how to detect when price breaks a mechanically generated trendline.

The pattern should support both directions:

```text
Bullish Trendline Break
Bearish Trendline Break
```

## Bullish Trendline Break Concept

A bullish trendline break occurs when price breaks above a descending resistance trendline.

General structure:

```text
1. Market forms lower highs.
2. A descending trendline is built from pivot highs.
3. Price closes above the trendline.
4. Breakout is validated by ATR buffer and volume confirmation.
```

## Bearish Trendline Break Concept

A bearish trendline break occurs when price breaks below an ascending support trendline.

General structure:

```text
1. Market forms higher lows.
2. An ascending trendline is built from pivot lows.
3. Price closes below the trendline.
4. Breakdown is validated by ATR buffer and volume confirmation.
```

## Mechanical Requirements

The pattern document must define:

```text
1. How to select pivot points for trendline construction
2. How many pivot touches are required
3. How to calculate the trendline value at the current candle
4. How to validate a bullish breakout
5. How to validate a bearish breakdown
6. How to apply ATR buffer
7. How to apply volume confirmation
8. How to reject weak or invalid trendlines
9. How to score the pattern
10. How to define entry, stop, and target references
```

## Trendline Construction Requirements

The document must define trendline construction using confirmed pivots only.

For bullish trendline break:

```text
Use pivot highs to construct descending resistance trendline.
```

For bearish trendline break:

```text
Use pivot lows to construct ascending support trendline.
```

The document must specify:

```text
minimum_touch_count
maximum_pivot_lookback
minimum_trendline_length
maximum_allowed_deviation
trendline_slope requirement
```

## Break Validation Requirements

The document must define breakout and breakdown validation.

Bullish break:

```text
close > trendline_value + atr_multiplier * ATR
```

Bearish break:

```text
close < trendline_value - atr_multiplier * ATR
```

Default ATR buffer:

```text
atr_multiplier = 0.2
```

## Volume Confirmation Requirements

The document must define when volume confirms the break.

Default:

```text
volume_ratio >= 1.5
```

Optional weak confirmation:

```text
volume_ratio >= 1.3
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

The document may optionally define a stronger trendline break when the breakout candle is also a displacement candle.

Bullish strong break:

```text
breakout candle is bullish displacement candle
```

Bearish strong break:

```text
breakdown candle is bearish displacement candle
```

## Pattern Output Requirements

The pattern document must define an output schema containing at least:

```text
symbol
timestamp
pattern_type
direction
trendline_type
trendline_slope
touch_count
break_price
trendline_value
break_distance
break_distance_atr
volume_ratio
liquidity_pass
spread_pass
pattern_score
pattern_status
entry_reference
stop_reference
target_reference
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
trendline_quality_score
breakout_strength_score
volume_confirmation_score
liquidity_score
structure_alignment_score
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

For bullish break:

```text
entry_reference = breakout close or next candle open
stop_reference = nearest swing low or broken trendline retest zone
target_reference = nearest resistance zone or risk-reward based target
```

For bearish break:

```text
entry_reference = breakdown close or next candle open
stop_reference = nearest swing high or broken trendline retest zone
target_reference = nearest support zone or risk-reward based target
```

## Edge Cases to Define

The pattern document must handle:

```text
not enough pivot points
unconfirmed pivots
flat trendline
too steep trendline
trendline with only two weak touches
breakout without ATR buffer
breakout without volume confirmation
low liquidity market
wide spread market
price immediately returning inside the trendline
multiple overlapping trendlines
conflicting swing structure
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
```

## Expected Deliverable

The next document should be:

```text
Trendline Break Pattern Mechanical Definition
```

It must be written as a concise Markdown technical specification.

It must reuse the previously defined core indicator modules.

It must not include actual implementation code beyond pseudocode-level logic.

It must not include a final summary section.

# Extracted Roles

- Owner role: Pattern mechanical definition for Trendline Break detection.
- Supporting roles:
  - Pivot High / Pivot Low, as the confirmed pivot source for trendline construction.
  - Swing Structure, as context for lower-high and higher-low alignment.
  - ATR, as the breakout or breakdown buffer and normalized distance input.
  - Volume Ratio, as break confirmation input.
  - Support / Resistance Zone, as contextual target and retest-zone reference input.
  - Liquidity: Trading Value / Volume, as the required tradability filter.
  - Bid-Ask Spread, as the required execution-quality filter.
  - Displacement Candle, as optional stronger-break confirmation.
- Forbidden roles:
  - Execution, because this task must not place, simulate, or route orders.
  - Exchange integration, because this task must not call real exchange APIs.
  - Risk management and position sizing, because this task only defines reference levels.
  - Backtesting engine, live trading, database, dashboard, scheduler, FastAPI, Streamlit, Docker, machine learning, futures, leverage, and portfolio optimization.

# Context

Task 034 restores the missing numbered task document for the Trendline Break Pattern definition phase. The implementation-independent mechanical definition should be stored under `tasks/patterns/trendline_break_pattern.md`.

# Scope

- Create or update the Trendline Break Pattern mechanical definition document.
- Keep the work documentation-only.
- Reuse previously defined core indicator modules by reference.
- Define deterministic inputs, validation rules, scoring, outputs, risk reference levels, and edge-case handling.

# Out of Scope

- Application code implementation.
- Real or paper order execution.
- Exchange API integration.
- Position sizing implementation.
- Backtesting engine implementation.
- Live order placement.
- Machine learning model.
- UI visualization.
- New shared contract redesigns unless a future task explicitly requests them.

# Requirements

- Define bullish and bearish Trendline Break detection.
- Use confirmed pivots only for trendline construction.
- Define pivot selection, touch count, trendline value calculation, ATR buffer, volume confirmation, liquidity and spread gates, invalid-trendline rejection, score calculation, output schema, and risk reference levels.
- Require `liquidity_pass = true` and `spread_pass = true` before pattern validation.
- Use default ATR buffer `atr_multiplier = 0.2`.
- Use default volume confirmation `volume_ratio >= 1.5` and weak confirmation `volume_ratio >= 1.3`.
- Define allowed direction values: `BULLISH`, `BEARISH`, `NONE`.
- Define allowed status values: `VALID`, `WEAK`, `INVALID`, `PENDING`.
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

- `tasks/034_TRENDLINE_BREAK_PATTERN.md` exists as the numbered Task 034 definition.
- The mechanical definition deliverable exists under `tasks/patterns/trendline_break_pattern.md`.
- The mechanical definition is Markdown and is limited to documentation/pseudocode-level logic.
- The mechanical definition covers all required core modules, input data, bullish and bearish detection, trendline construction, break validation, volume confirmation, liquidity/spread requirements, optional displacement confirmation, output schema, score components, risk references, edge cases, and non-goals.
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
