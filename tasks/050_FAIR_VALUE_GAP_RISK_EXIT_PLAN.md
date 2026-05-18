# Task 050: Fair Value Gap Risk / Exit Plan

# Goal

Implement Fair Value Gap pattern-specific stop-loss, take-profit, reaction-failure, and exit-plan calculation using the shared contract from Task 047.

# Source Requirement

Use:

- `tasks/patterns/risk_exit_management.md`
- `tasks/040_PATTERN_DETECTION_ENGINE.md`
- `tasks/patterns/fair_value_gap_pattern.md`

# Clean Requirement

For bullish and bearish FVG events, build risk plans around the FVG boundary, ATR buffer, FVG midpoint reaction rule, R-multiple targets, FVG/structure/liquidity targets when available, and time-based failure metadata.

# Dependency

- Task 047 must be completed and verified first.

# Scope

- Add FVG-specific planner code in `quant_bitcoin/patterns/fair_value_gap.py` or a focused companion module.
- Reuse `PatternEvent` fields including `direction`, `zone_low`, `zone_high`, `zone_mid`, `gap_size_atr`, `entry_reference`, `stop_reference`, and `target_reference`.
- Add deterministic unit tests.
- Update `STATUS.md` if project state changes.

# Out of Scope

- Changing FVG detection logic.
- Implementing liquidity detection if unavailable.
- Implementing other patterns.
- Backtest-runner integration.
- Paper or live order placement.
- Exchange API calls.

# Requirements

- Bullish default stop: `fvg_low - ATR(14) * buffer_multiplier`.
- Bearish default stop: `fvg_high + ATR(14) * buffer_multiplier`.
- Default buffer multiplier should be `0.2`; support recommended configurable range `0.1` to `0.3`.
- Include a reaction-failure time-stop rule: if price enters the FVG and does not close beyond the FVG midpoint in the favorable direction within N candles, exit.
- Represent the reaction-failure rule as plan metadata; candle-by-candle execution may be deferred to the exit simulation task.
- Targets should include FVG opposite boundary, previous swing/liquidity target when available, and R multiples.
- Apply the shared minimum profit filter.

# Acceptance Criteria

- Bullish and bearish FVG plans produce deterministic stops and targets.
- Midpoint reaction-failure metadata is represented.
- FVG boundary target behavior is deterministic.
- Missing liquidity targets are handled as optional, not fabricated.
- No detector behavior or exchange behavior is changed.

# Required Tests

## Unit Tests

- Bullish FVG low stop with ATR buffer.
- Bearish FVG high stop with ATR buffer.
- FVG midpoint reaction rule metadata for long and short.
- TP includes R multiple and FVG/structure candidate where available.
- Minimum profit filter skip case.

## Safety Tests

- Confirm no real order execution or exchange endpoint calls are introduced.

# Verification

Default:

```bash
pytest tests/patterns/test_fair_value_gap_risk_exit.py
pytest
```

# Codex Self-Review Requirement

Before completion, run through `reviews/CODEX_SELF_REVIEW.md` and include the result in the final summary.
