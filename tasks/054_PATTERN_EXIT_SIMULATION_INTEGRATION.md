# Task 054: Pattern Exit Simulation Integration

# Goal

Implement deterministic candle-by-candle exit simulation for pattern risk/exit plans after Tasks 047-053 are complete.

This task turns planned stop-loss, take-profit, soft invalidation, time-stop, break-even, trailing-stop, and partial-exit metadata into backtestable exit decisions. It still must not implement live trading or real exchange order execution.

# Source Requirement

Use:

- `tasks/patterns/risk_exit_management.md`
- Task 047 shared risk/exit contract.
- Task 048 through Task 053 pattern-specific planners.

# Clean Requirement

Add a pure simulation layer that can evaluate completed candles after a planned pattern entry and produce deterministic exit events/results for backtesting and analysis.

# Dependencies

- Task 047 must be completed and verified.
- Pattern-specific planner tasks needed by the target simulation scenario must be completed first.

# Scope

- Add a pure backtesting or pattern-analysis module for exit simulation.
- Support stop-loss, TP1/TP2/TP3, time stop, soft invalidation, break-even move, trailing stop, and partial exits as represented by the Task 047 contract.
- Add deterministic tests using synthetic candles.
- Update `STATUS.md` if project state changes.

# Out of Scope

- Live trading.
- Real Binance order execution.
- Exchange order endpoints.
- Paper order placement unless a later task explicitly assigns paper-trader integration.
- Database persistence.
- Scheduler, dashboard, FastAPI, Streamlit, Docker, ML, futures, leverage, portfolio optimization.
- Changing pattern detection algorithms.

# Requirements

- Evaluate only completed candles in timestamp order.
- Do not mutate caller-provided candle data.
- Apply deterministic precedence rules when multiple exit conditions occur in the same candle; document and test the precedence.
- Support long and short plans.
- Handle partial exits by recording fill ratio/quantity ratio metadata without creating real orders.
- Support break-even stop movement after configured favorable movement.
- Support trailing-stop movement after configured activation.
- Support time stops such as no reaction within N candles or no 1R movement within N candles.
- Support soft invalidation rules, such as close back inside diamond range or close below neckline/trendline/FVG midpoint failure, when the plan provides enough metadata.
- Return analysis/backtest result records, not exchange orders.

# Acceptance Criteria

- Exit simulation is deterministic and tested for long and short plans.
- Stop-loss, take-profit, time-stop, break-even, trailing-stop, and partial-exit behavior are covered by tests.
- Same-candle precedence is documented and tested.
- No exchange client, live trading, or real order execution behavior is introduced.

# Required Tests

## Unit Tests

- Long hard stop hit.
- Short hard stop hit.
- TP1/TP2/TP3 hit sequencing.
- Same-candle stop/TP precedence.
- Time stop before target.
- Soft invalidation exit.
- Break-even stop movement.
- Trailing stop movement.
- Partial-exit recording.

## Integration Tests

- Optional integration test using one completed pattern-specific planner output after the relevant planner task is complete.

## Safety Tests

- Confirm no real order execution or exchange endpoint calls are introduced.

# Verification

Default:

```bash
pytest tests/patterns/test_pattern_exit_simulation.py
pytest
```

# Codex Self-Review Requirement

Before completion, run through `reviews/CODEX_SELF_REVIEW.md` and include the result in the final summary.
