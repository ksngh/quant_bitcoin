# Task 051: Cup And Handle Risk / Exit Plan

# Goal

Implement Cup and Handle pattern-specific stop-loss, take-profit, neckline soft-exit, and exit-plan calculation using the shared contract from Task 047.

# Source Requirement

Use:

- `tasks/patterns/risk_exit_management.md`
- `tasks/043_CUP_AND_HANDLE_PATTERN_ENGINE.md`
- `tasks/patterns/cup_and_handle_pattern.md`

# Clean Requirement

For Cup and Handle events, build risk plans around handle low, neckline re-entry invalidation, breakout candle, ATR buffer, R-multiple targets, and measured move target (`neckline + cup_depth` for long patterns).

# Dependency

- Task 047 must be completed and verified first.

# Scope

- Add Cup and Handle-specific planner code in the pattern module or a focused companion module.
- Reuse `CupAndHandleEvent` fields including `handle_low_price`, `neckline`, `cup_depth`, `breakout_price`, `breakout_index`, `atr`, `entry_reference`, `stop_reference`, and `target_reference`.
- Add deterministic unit tests.
- Update `STATUS.md` if project state changes.

# Out of Scope

- Changing Cup and Handle detection logic.
- Implementing new volume/momentum filters unless already available through event fields.
- Implementing other patterns.
- Backtest-runner integration.
- Paper or live order placement.
- Exchange API calls.

# Requirements

- Long default stop: `handle_low - ATR(14) * buffer_multiplier`.
- Default buffer multiplier should be configurable; recommended range is `0.3` to `0.6` because the structure is larger.
- Include a fast soft-exit rule for close below neckline after breakout.
- Include a wider hard-stop rule at handle low with ATR buffer.
- Include measured target: `neckline + cup_depth` for long plans.
- Include 1R/2R/3R targets and allow nearest structure target when supplied.
- Apply the shared minimum profit filter.
- If bearish/inverse Cup and Handle is not supported by the current detector, document that limitation and do not fabricate mirrored behavior.

# Acceptance Criteria

- Long Cup and Handle plans produce deterministic handle-low stops and measured targets.
- Neckline soft-exit metadata is represented.
- Wider stop and measured target behavior are tested.
- Unsupported inverse direction is handled explicitly.
- No detector behavior or exchange behavior is changed.

# Required Tests

## Unit Tests

- Long handle-low stop with configured ATR buffer.
- Measured target equals neckline plus cup depth.
- Neckline soft-exit metadata is present.
- Minimum profit filter skip case.
- Unsupported direction handling if applicable.

## Safety Tests

- Confirm no real order execution or exchange endpoint calls are introduced.

# Verification

Default:

```bash
pytest tests/patterns/test_cup_and_handle_risk_exit.py
pytest
```

# Codex Self-Review Requirement

Before completion, run through `reviews/CODEX_SELF_REVIEW.md` and include the result in the final summary.
