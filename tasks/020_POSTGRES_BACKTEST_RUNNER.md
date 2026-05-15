# Task 020: PostgreSQL Backtest Runner

# Goal

Add a small, explicit workflow for running the existing RSI backtest against candles already stored in PostgreSQL.

# Source Requirement

User request on 2026-05-15:

- Select or create the next project task explicitly after Task 019.
- If local PostgreSQL backtesting needs real data first, run the accepted Binance PostgreSQL backfill workflow.

# Extracted Roles

- Owner role: Backtest Engine
- Supporting roles: Market Data Provider, Persistence, Strategy, Documentation, Test Designer
- Forbidden roles: Live Trading, Real Binance order execution, Exchange account APIs, Scheduler, Dashboard, FastAPI, Streamlit, Risk Management, Portfolio Optimization

# Context

Task 019 added a PostgreSQL-backed candle data provider that reads closed rows from the accepted `candles` table, maps `open_time` to the standard `timestamp` field, and returns only `timestamp`, `open`, `high`, `low`, `close`, and `volume` for existing backtests.

The next useful project step is to make the PostgreSQL-backed backtest workflow runnable and repeatable without changing the existing backtest contract. This task should wire together existing components only:

- `PostgresCandleRepository`
- `PostgresCandleDataProvider`
- `RsiStrategy`
- `BasicBacktester`

For local runs with real data, PostgreSQL must already contain candles. The accepted Task 014 Binance PostgreSQL backfill workflow remains the approved way to store historical Binance candles before running this backtest workflow.

# Scope

- Add a small CLI or script entrypoint for running an RSI backtest from PostgreSQL-stored candles.
- Accept configuration for database URL, source, symbol, interval, optional start/end time, starting cash, trade quantity, and RSI parameters.
- Load candles with `PostgresCandleDataProvider`.
- Run the existing `BasicBacktester` with the existing `RsiStrategy`.
- Print a deterministic machine-readable summary suitable for local inspection, such as JSON.
- Add tests with mocked/fake repository/provider behavior so ordinary tests do not require real PostgreSQL, Docker, or Binance network access.
- Update README usage documentation for the runnable PostgreSQL backtest workflow.
- Update `STATUS.md` during implementation if phase, step, goal, active task, or completion state changes.

# Out of Scope

- Live trading.
- Real Binance order execution.
- Exchange account APIs.
- API keys, signed requests, or tracked `.env` files.
- Strategy algorithm changes.
- Backtest engine public contract changes.
- New signal contracts.
- Database schema changes or migration-framework adoption.
- Running a scheduler or daemon.
- Dashboard, FastAPI, or Streamlit.
- Risk management, portfolio optimization, futures, leverage, or machine learning.
- Ordinary tests that require real PostgreSQL, Docker, real Binance availability, or external network access.

# Requirements

- Read `AGENTS.md`, `STATUS.md`, `docs/10_CODEX_COMMAND_GUIDE.md`, `docs/04_DATA_CONTRACT.md`, `tasks/014_POSTGRES_BINANCE_BACKFILL.md`, `tasks/019_POSTGRES_CANDLE_DATA_PROVIDER.md`, this task file, and `reviews/CODEX_SELF_REVIEW.md` before coding.
- Keep implementation limited to runnable wiring around existing market-data, strategy, and backtest components.
- Preserve the standard candle data contract.
- Preserve the existing `BasicBacktester.run(candles, strategy)` public contract.
- Do not make strategy code fetch data or know about PostgreSQL.
- Do not make market-data code generate signals or choose quantities.
- Do not add live trading flags or order-execution behavior.
- Do not call Binance endpoints from the backtest runner.
- Document that local real-data runs require existing PostgreSQL candles and can use Task 014 backfill first.
- Ordinary tests must mock persistence/provider behavior and must not require real PostgreSQL or Docker.

# Status Tracking

## Before Implementation

- [ ] Read `AGENTS.md`.
- [ ] Read `STATUS.md`.
- [ ] Read `docs/10_CODEX_COMMAND_GUIDE.md`.
- [ ] Read `docs/04_DATA_CONTRACT.md`.
- [ ] Read `tasks/014_POSTGRES_BINANCE_BACKFILL.md`.
- [ ] Read `tasks/019_POSTGRES_CANDLE_DATA_PROVIDER.md`.
- [ ] Read `reviews/CODEX_SELF_REVIEW.md`.
- [ ] Read this task file.
- [ ] Confirm the task is runnable backtest wiring only.
- [ ] Confirm PostgreSQL candles are read-only inputs for this workflow.
- [ ] Confirm no live trading, order execution, scheduler, or dashboard behavior is requested.

## After Implementation

- [ ] Update `STATUS.md` if active task, current step, next step, or completion state changes.
- [ ] Mark checklist items complete only after acceptance criteria and verification pass.
- [ ] Leave uncertain items open and document the uncertainty.
- [ ] Confirm the next step is accurate or explicitly left undecided.

# Acceptance Criteria

- A runnable PostgreSQL-backed RSI backtest entrypoint exists.
- The runner loads candle data through `PostgresCandleDataProvider`.
- The runner uses the existing `RsiStrategy` and `BasicBacktester` without changing their public contracts.
- The runner supports database URL, source, symbol, interval, optional start/end time, starting cash, trade quantity, and RSI parameter configuration.
- The runner prints deterministic JSON or another documented machine-readable summary.
- README documents how to populate PostgreSQL first with the accepted Task 014 backfill workflow before running against real local data.
- Tests cover CLI/script argument parsing and component wiring with mocked/fake persistence/provider behavior.
- Tests cover empty-candle or insufficient-data behavior if the runner defines a user-facing result for it.
- Ordinary tests do not require real PostgreSQL, Docker, Binance, or external network access.
- No live-trading, signed request, API-key, `.env`, exchange account API, or order endpoint behavior is added.

# Required Tests

## Unit Tests

- CLI/script default arguments are parsed as documented.
- Optional start/end times are parsed using the same open-time semantics as Task 019.
- Runner wires `PostgresCandleDataProvider`, `RsiStrategy`, and `BasicBacktester` with configured values.
- Runner serializes a deterministic summary payload.

## Integration Tests

- Optional PostgreSQL integration is not required for ordinary tests.
- If an optional local PostgreSQL integration test is added, it must be skipped unless a dedicated test database URL such as `QUANT_BITCOIN_TEST_DATABASE_URL` is configured.

## Contract Tests

- Runner does not change the standard candle schema.
- Runner does not change `BasicBacktester.run(candles, strategy)`.
- Runner consumes provider-loaded candles without CSV.

## Safety Tests

- No real Binance network calls.
- No exchange account API calls.
- No order endpoint calls.
- No API-key, signed-request, tracked `.env`, or live-trading behavior.
- Ordinary tests must not open external network connections.

# Review Checklist

- Scope respected.
- Requirement matched.
- Role ownership respected.
- Architecture boundaries respected.
- Existing standard candle data contract preserved.
- Existing backtest engine public contract preserved.
- No hardcoded secrets.
- No tracked `.env` files.
- No real order execution.
- No exchange order endpoint calls.
- No scheduler, dashboard, FastAPI, or Streamlit added.
- No unnecessary abstractions.

# Verification

```bash
pytest
git diff --check
python -m compileall quant_bitcoin
```

# Codex Self-Review Requirement

Before completion, run through `reviews/CODEX_SELF_REVIEW.md` and include the result in the final summary.

# PR Review Requirement

Use `reviews/REVIEW_CHECKLIST.md` and `docs/06_PR_REVIEW_PROCESS.md` before merge.

# Completion Summary Required

- files changed
- implementation summary
- tests added or updated
- tests run
- Codex self-review result
- known limitations
- recommended next task
