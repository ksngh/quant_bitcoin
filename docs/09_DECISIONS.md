# Decision Log

## Decision 0001: Strategy Returns Signal, Not Order

Status:

- accepted

Context:

- Strategies need a clear boundary.
- A strategy can decide market direction, but execution details require separate rules.

Decision:

- Strategy returns Signal, not Order.

Consequences:

- Strategy decides direction only.
- Order quantity and execution belong outside strategy.

## Decision 0002: Use PaperTrader Before LiveTrader

Status:

- accepted

Context:

- Real-money trading must not be introduced before simulated execution is tested.

Decision:

- Use PaperTrader before LiveTrader.

Consequences:

- The system is tested safely before real-money trading.
- Paper trading must not call real exchange order APIs.

## Decision 0003: Use Standard Candle Schema

Status:

- accepted

Context:

- Exchange APIs return provider-specific data.
- Strategy code should remain independent from provider-specific raw fields.

Decision:

- Use the standard candle schema: `timestamp`, `open`, `high`, `low`, `close`, `volume`.

Consequences:

- Strategy does not depend on Binance raw fields.
- Data providers must normalize raw data before returning it.

## Decision 0004: Keep Risk Management Out of First Version

Status:

- accepted

Context:

- The first version should stay focused on data, strategy, backtest, and paper trading.

Decision:

- Keep risk management out of the first version.

Consequences:

- The first version remains small.
- Risk controls will be added after the basic flow works.

## Decision 0005: Keep Live Trading Out of First Implementation Phase

Status:

- accepted

Context:

- Real order execution has safety implications.
- Data, strategy, backtest, and paper trading should be tested first.

Decision:

- Keep live trading out of the first implementation phase.

Consequences:

- Real order execution is added only after the earlier phases are working and reviewed.

## Decision 0006: Use Requirement and Role Extraction Before Implementation Tasks

Status:

- accepted

Context:

- Raw requirements can mix responsibilities across market data, strategy, backtest, and execution.

Decision:

- Use requirement cleanup and role extraction before implementation tasks.

Consequences:

- Tasks have clearer owners, boundaries, out-of-scope items, tests, and review checks.

## Decision 0007: Every Implementation Task Should Define Tests and Review Criteria

Status:

- accepted

Context:

- Future changes need visible verification and review expectations.

Decision:

- Every implementation task should define tests and review criteria.

Consequences:

- Tasks are easier to complete and review.
- Missing tests or review criteria should be treated as incomplete task definition.
