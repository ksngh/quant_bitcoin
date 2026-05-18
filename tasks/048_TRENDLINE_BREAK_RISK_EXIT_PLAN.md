# Task 048: Trendline Break Risk / Exit Plan

# Goal

Implement Trendline Break pattern-specific stop-loss, take-profit, and exit-plan calculation using the shared contract from Task 047.

# Source Requirement

Use:

- `tasks/patterns/risk_exit_management.md`
- `tasks/041_TRENDLINE_BREAK_PATTERN_ENGINE.md`
- `tasks/patterns/trendline_break_pattern.md`

# Clean Requirement

For Trendline Break events, build a long/short risk plan that uses the broken trendline structure, breakout candle, optional retest pivot, ATR buffer, R-multiple targets, nearest prior swing target when available, and a follow-through time-stop setting.

# Dependency

- Task 047 must be completed and verified first.

# Scope

- Add Trendline Break-specific planner code in the pattern module or a focused companion module.
- Reuse the shared risk/exit contract from Task 047.
- Reuse existing `TrendlineBreakEvent` fields where possible, including `direction`, `end_index`, `break_price`, `atr`, `entry_reference`, `stop_reference`, and `target_reference`.
- Use candle lows/highs and available pivot indices only as needed to compute breakout-candle and structural references.
- Add deterministic unit tests.
- Update `STATUS.md` if project state changes.

# Out of Scope

- Changing Trendline Break detection logic.
- Adding retest detection if current events/candles cannot support it deterministically; document or defer retest-specific behavior instead.
- Implementing other patterns.
- Backtest-runner integration.
- Paper or live order placement.
- Exchange API calls.

# Requirements

- Default long structural stop should use the lower of breakout-candle low and retest pivot low when a deterministic retest pivot is available.
- If retest pivot is unavailable, use the breakout-candle low or existing event `stop_reference` as the documented fallback.
- Apply default ATR buffer multiplier `0.2`, with configurable range guidance `0.2` to `0.4`.
- Support bearish/short symmetry using breakout-candle high / retest pivot high and ATR buffer above the structural stop.
- Include a soft invalidation setting for close re-entering the broken trendline side when it can be evaluated by a future exit simulator.
- Include a time-stop setting for follow-through failure within configurable N candles.
- Targets should include 1R/2R/3R and nearest prior swing high/low or existing `target_reference` when available.
- Apply the shared minimum profit filter.

# Acceptance Criteria

- Trendline Break risk plans can be generated for valid bullish and bearish events.
- ATR-buffered hard stops match the mechanical formula.
- Missing optional retest data is handled deterministically and documented in test expectations.
- Soft invalidation and time-stop metadata are represented without executing trades.
- No detector behavior or exchange behavior is changed.

# Required Tests

## Unit Tests

- Bullish stop uses min breakout low and retest pivot low when both are supplied.
- Bullish fallback stop uses breakout low or event stop reference when retest is unavailable.
- Bearish stop uses the mirrored high-side formula.
- R targets and structural target metadata are present.
- Minimum target filter can skip a poor R:R plan.

## Safety Tests

- Confirm no real order execution or exchange endpoint calls are introduced.

# Verification

Default:

```bash
pytest tests/patterns/test_trendline_break_risk_exit.py
pytest
```

# Codex Self-Review Requirement

Before completion, run through `reviews/CODEX_SELF_REVIEW.md` and include the result in the final summary.
