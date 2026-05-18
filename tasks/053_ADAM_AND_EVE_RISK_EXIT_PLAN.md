# Task 053: Adam And Eve Risk / Exit Plan

# Goal

Implement Adam and Eve pattern-specific stop-loss, take-profit, neckline soft-exit, and exit-plan calculation using the shared contract from Task 047.

# Source Requirement

Use:

- `tasks/patterns/risk_exit_management.md`
- `tasks/045_ADAM_AND_EVE_PATTERN_ENGINE.md`
- `tasks/patterns/adam_and_eve_pattern.md`

# Clean Requirement

For Adam and Eve events, build risk plans around Eve low as the practical default structural stop, optional wider Adam/Eve low stop, neckline re-entry soft invalidation, ATR buffer, R-multiple targets, and measured target using pattern height.

# Dependency

- Task 047 must be completed and verified first.

# Scope

- Add Adam and Eve-specific planner code in the pattern module or a focused companion module.
- Reuse `AdamAndEveEvent` fields including `eve_low_price`, `adam_low_price`, `neckline`, `pattern_height`, `breakout_price`, `breakout_index`, `atr`, `entry_reference`, `stop_reference`, and `target_reference`.
- Add deterministic unit tests.
- Update `STATUS.md` if project state changes.

# Out of Scope

- Changing Adam and Eve detection logic.
- Implementing other patterns.
- Backtest-runner integration.
- Paper or live order placement.
- Exchange API calls.

# Requirements

- Long default stop: `eve_low - ATR(14) * buffer_multiplier`.
- Optional wider stop mode: `min(adam_low, eve_low) - ATR(14) * buffer_multiplier`.
- Default buffer multiplier should be configurable; recommended range is `0.3` to `0.6`.
- Include soft invalidation metadata for close below neckline after breakout.
- Include measured target: `neckline + pattern_height` for long plans.
- Include 1R/2R/3R targets and allow nearest structure target when supplied.
- Apply the shared minimum profit filter.
- If bearish/inverse Adam and Eve is not supported by the current detector, document that limitation and do not fabricate mirrored behavior.

# Acceptance Criteria

- Long Adam and Eve plans produce deterministic Eve-low stops and measured targets.
- Wider Adam/Eve stop mode is optional and tested.
- Neckline soft-exit metadata is represented.
- Unsupported inverse direction is handled explicitly.
- No detector behavior or exchange behavior is changed.

# Required Tests

## Unit Tests

- Eve-low stop with ATR buffer.
- Wider min Adam/Eve stop mode.
- Measured target equals neckline plus pattern height.
- Neckline soft-exit metadata is present.
- Minimum profit filter skip case.

## Safety Tests

- Confirm no real order execution or exchange endpoint calls are introduced.

# Verification

Default:

```bash
pytest tests/patterns/test_adam_and_eve_risk_exit.py
pytest
```

# Codex Self-Review Requirement

Before completion, run through `reviews/CODEX_SELF_REVIEW.md` and include the result in the final summary.
