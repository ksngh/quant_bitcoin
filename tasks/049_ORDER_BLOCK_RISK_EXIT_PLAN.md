# Task 049: Order Block Risk / Exit Plan

# Goal

Implement Order Block pattern-specific stop-loss, take-profit, and exit-plan calculation using the shared contract from Task 047.

# Source Requirement

Use:

- `tasks/patterns/risk_exit_management.md`
- `tasks/042_ORDER_BLOCK_PATTERN_ENGINE.md`
- `tasks/patterns/order_block_pattern.md`

# Clean Requirement

For bullish and bearish Order Block events, build risk plans around the order-block zone boundary, configurable ATR buffer, preferred zone entry reference, R-multiple targets, previous liquidity/structure targets when available, and no-reaction time-stop metadata.

# Dependency

- Task 047 must be completed and verified first.

# Scope

- Add Order Block-specific planner code in the pattern module or a focused companion module.
- Reuse `OrderBlockEvent` fields including `direction`, `zone_low`, `zone_high`, `zone_mid`, `atr`-derived values where available, `entry_reference`, `stop_reference`, and `target_reference`.
- Add deterministic unit tests.
- Update `STATUS.md` if project state changes.

# Out of Scope

- Changing Order Block detection logic.
- Adding new institutional-order inference beyond the existing detector.
- Implementing other patterns.
- Backtest-runner integration.
- Paper or live order placement.
- Exchange API calls.

# Requirements

- Bullish default stop: `order_block_low - ATR(14) * buffer_multiplier`.
- Bearish default stop: `order_block_high + ATR(14) * buffer_multiplier`.
- Default buffer multiplier should be `0.2`; allow conservative config such as `0.5`.
- Represent preferred entry modes for zone entry, at minimum zone midpoint and optional 61.8% zone reference when deterministic.
- Do not force entry at the upper bullish zone edge by default if midpoint/discount entry is configured.
- Include no-reaction time-stop metadata for N candles after OB entry.
- Targets should include R multiples and previous liquidity / market-structure target when available through existing event target data or caller-supplied structural targets.
- Apply the shared minimum profit filter.

# Acceptance Criteria

- Bullish and bearish Order Block plans produce deterministic stops and targets.
- Buffer multiplier configuration changes stop distance predictably.
- Zone midpoint entry behavior is represented and tested.
- No-reaction time-stop metadata is represented without executing trades.
- No detector behavior or exchange behavior is changed.

# Required Tests

## Unit Tests

- Bullish zone-low stop with 0.2 ATR buffer.
- Bullish conservative stop with 0.5 ATR buffer.
- Bearish mirrored zone-high stop.
- Zone midpoint or configured entry reference affects risk per unit.
- Minimum profit filter skip case.

## Safety Tests

- Confirm no real order execution or exchange endpoint calls are introduced.

# Verification

Default:

```bash
pytest tests/patterns/test_order_block_risk_exit.py
pytest
```

# Codex Self-Review Requirement

Before completion, run through `reviews/CODEX_SELF_REVIEW.md` and include the result in the final summary.
