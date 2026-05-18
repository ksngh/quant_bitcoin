# Task 052: Diamond Risk / Exit Plan

# Goal

Implement Diamond pattern-specific stop-loss, soft invalidation, take-profit, time-stop, and exit-plan calculation using the shared contract from Task 047.

# Source Requirement

Use:

- `tasks/patterns/risk_exit_management.md`
- `tasks/044_DIAMOND_PATTERN_ENGINE.md`
- `tasks/patterns/diamond_pattern.md`

# Clean Requirement

For Diamond breakout events, build risk plans around diamond boundary breakout close, close-back-inside soft invalidation, last internal pivot hard stop when available, ATR buffer, 1R time-stop, R-multiple targets, and measured target using diamond height.

# Dependency

- Task 047 must be completed and verified first.

# Scope

- Add Diamond-specific planner code in the pattern module or a focused companion module.
- Reuse `DiamondEvent` fields including `direction`, `breakout_price`, `breakout_index`, boundary values, `source_pivot_indices`, `pattern_height`, `atr`, `entry_reference`, `stop_reference`, and `target_reference`.
- Add deterministic unit tests.
- Update `STATUS.md` if project state changes.

# Out of Scope

- Changing Diamond detection logic.
- Adding persistent fake-breakout lifecycle tracking.
- Implementing other patterns.
- Backtest-runner integration.
- Paper or live order placement.
- Exchange API calls.

# Requirements

- Long default hard stop should use last internal pivot low minus ATR buffer when deterministically available.
- Bearish default hard stop should use last internal pivot high plus ATR buffer when deterministically available.
- If internal pivot price cannot be reconstructed from current event/candles, use existing event `stop_reference` as a documented fallback or stop for owner approval if ambiguous.
- Default buffer multiplier should be `0.2`; support recommended configurable range `0.2` to `0.5`.
- Include soft invalidation metadata for close back inside diamond range.
- Include time-stop metadata: if price does not move 1R within N candles, exit.
- Include measured target: breakout price plus/minus diamond height by direction.
- Include 1R/2R/3R targets and apply the shared minimum profit filter.

# Acceptance Criteria

- Bullish and bearish Diamond plans produce deterministic hard stops and measured targets.
- Soft re-entry invalidation metadata is represented.
- 1R-within-N-candles time-stop metadata is represented.
- Ambiguous missing internal pivot prices are handled explicitly.
- No detector behavior or exchange behavior is changed.

# Required Tests

## Unit Tests

- Bullish hard stop from last internal pivot low with ATR buffer.
- Bearish hard stop from last internal pivot high with ATR buffer.
- Measured target uses diamond height by direction.
- Soft invalidation metadata for close back inside range.
- 1R time-stop metadata and minimum profit filter skip case.

## Safety Tests

- Confirm no real order execution or exchange endpoint calls are introduced.

# Verification

Default:

```bash
pytest tests/patterns/test_diamond_risk_exit.py
pytest
```

# Codex Self-Review Requirement

Before completion, run through `reviews/CODEX_SELF_REVIEW.md` and include the result in the final summary.
