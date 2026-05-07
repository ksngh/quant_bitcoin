# Requirement 000: Initial Scope

## Raw Requirement

The project should start as a small Python Bitcoin quant trading application.
It should first support candle data, RSI strategy, basic backtesting, and paper trading.
It should not implement live trading, real order execution, risk management, dashboard, database, scheduler, machine learning, futures, leverage, or portfolio optimization in the first version.

## Clean Requirement

Create a small first-version scope for a Python Bitcoin quantitative trading application focused on candle data, RSI strategy, basic backtesting, and paper trading.

## Problem

- The project needs a safe starting scope before implementation begins.
- Future Codex tasks need clear boundaries to avoid adding advanced trading features too early.

## User Goal

- Build the project gradually with small, reviewable implementation phases.

## Functional Requirements

- Define first-version scope around candle data, RSI strategy, basic backtesting, and paper trading.
- Keep Binance historical candle downloading as a later data task.
- Require paper trading before live trading.

## Non-Functional Requirements

- Keep the first version small.
- Keep implementation tasks scoped and testable.
- Preserve architecture boundaries between data, strategy, backtest, and execution.

## Explicitly Out of Scope

- live trading
- real order execution
- risk management
- dashboard
- database
- scheduler
- machine learning
- futures
- leverage
- portfolio optimization

## Ambiguities

- Exact Python package name is not defined yet.
- Exact test framework setup is not defined yet.

## Assumptions

- The first implementation task will be project setup.
- Unit tests will use `pytest` when the project is configured.

## Acceptance Criteria

- Documentation defines the first-version scope.
- Task tickets exist for project setup, market data, CSV provider, RSI strategy, basic backtest, paper trader, and Binance historical candle downloader.
- Review and self-review checklists exist.

## Extracted Roles

- Owner role: Requirement Owner
- Supporting roles: Architect, Test Designer, Reviewer
- Forbidden roles: Live order execution, risk management implementation

## Required Tests

- Unit tests: not applicable for documentation-only scope
- Integration tests: not applicable for documentation-only scope
- Contract tests: not applicable for documentation-only scope
- Safety tests: future implementation tasks must include safety checks where relevant

## PR Review Checks

- Scope excludes live trading and real orders.
- Tasks are small enough for future implementation.
- Safety rules are visible in `AGENTS.md` and review docs.

## Related Documents

- `AGENTS.md`
- `docs/00_PROJECT_BRIEF.md`
- `docs/08_ROADMAP.md`
- `tasks/000_PROJECT_SETUP.md`
