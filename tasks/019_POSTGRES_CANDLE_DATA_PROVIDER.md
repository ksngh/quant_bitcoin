# Task 019: PostgreSQL Candle Data Provider for Backtesting

# Goal

Add a PostgreSQL-backed candle data provider that reads stored rows from the `candles` table and returns the standard candle `DataFrame` consumed by the existing `BasicBacktester`.

# Source Requirement

User request on 2026-05-15:

- The current backtest workflow appears to use CSV files.
- Add a way to run backtests against candles already stored in PostgreSQL.
- Add a provider that reads the PostgreSQL `candles` table and returns the existing standard candle `DataFrame` for `BasicBacktester`.
- Explain how candle contents can be stored in PostgreSQL.

# Extracted Roles

- Owner role: Market Data Provider
- Supporting roles: Persistence, Backtest Engine consumer, Test Designer, Documentation
- Forbidden roles: Strategy, Backtest Engine public contract redesign, Execution, Live Trading, Binance order client, Scheduler, Dashboard

# Context

Task 013 defined the accepted persistence schema for Binance candle storage. Task 014 implemented PostgreSQL persistence and a Binance historical backfill path that stores closed public-market-data candles. The current backtest engine already accepts standard candle data as a pandas `DataFrame`; this task must add a read path from PostgreSQL into that same standard schema without changing strategy behavior or the backtest engine public contract.

The standard candle schema remains:

- `timestamp`
- `open`
- `high`
- `low`
- `close`
- `volume`

For PostgreSQL-backed rows, `timestamp` must map from `candles.open_time`. Provider-specific fields such as `source`, `symbol`, `interval`, `close_time`, Binance volume details, trade counts, raw payloads, and ingestion metadata must stay inside the persistence/market-data boundary and must not leak into strategy inputs.

# Scope

- Add PostgreSQL candle read functionality in `quant_bitcoin/market_data` and/or `quant_bitcoin/persistence`.
- Return candles in the existing standard candle `DataFrame` shape expected by `BasicBacktester`.
- Support filtering by `source`, `symbol`, `interval`, and optional UTC start/end times.
- Sort returned rows ascending by `timestamp`.
- Add tests for provider/repository read behavior using mocked/fake DB access and/or optional PostgreSQL integration.
- Add or update README usage examples if needed to show backtesting from stored PostgreSQL candles.
- Update `STATUS.md` during implementation if phase, step, goal, active task, or completion state changes.

# Out of Scope

- Live trading.
- Real Binance order execution.
- Exchange account APIs.
- API keys, signed requests, or tracked `.env` files.
- Strategy changes.
- Backtest engine public contract changes.
- New signal contracts.
- Dashboard, scheduler, FastAPI, or Streamlit.
- Database redesign or migration-framework adoption.
- Schema changes unless the existing accepted schema is demonstrably insufficient and the task is stopped for owner approval.
- Machine learning, futures, leverage, risk management, or portfolio optimization.

# Requirements

- Read `AGENTS.md`, `STATUS.md`, `docs/10_CODEX_COMMAND_GUIDE.md`, `docs/04_DATA_CONTRACT.md`, `tasks/013_PERSISTENCE_SCHEMA_DESIGN.md`, `tasks/014_POSTGRES_BINANCE_BACKFILL.md`, this task file, and `reviews/CODEX_SELF_REVIEW.md` before coding.
- Keep implementation limited to a PostgreSQL candle read path and any required tests/docs.
- Preserve the standard candle data contract.
- Preserve the existing `BasicBacktester.run(candles, strategy)` contract.
- Do not make strategies depend on PostgreSQL or Binance-specific fields.
- The provider must expose only standard candle columns to backtest/strategy consumers.
- `timestamp` must be derived from `open_time`, not `close_time` or ingestion timestamps.
- Returned rows must be sorted ascending by `timestamp`.
- Optional time filters must be applied against `open_time` semantics.
- The default intended source should remain compatible with the Task 013/014 source value for Binance spot candles.
- Tests must not call real Binance endpoints or any exchange order endpoints.
- Ordinary tests must not require a real PostgreSQL server unless they are explicitly skipped when a test database URL is not configured.

# Status Tracking

## Before Implementation

- [ ] Read `AGENTS.md`.
- [ ] Read `STATUS.md`.
- [ ] Read `docs/10_CODEX_COMMAND_GUIDE.md`.
- [ ] Read `docs/04_DATA_CONTRACT.md`.
- [ ] Read `tasks/013_PERSISTENCE_SCHEMA_DESIGN.md`.
- [ ] Read `tasks/014_POSTGRES_BINANCE_BACKFILL.md`.
- [ ] Read `reviews/CODEX_SELF_REVIEW.md`.
- [ ] Read this task file.
- [ ] Confirm the task is a market-data/persistence read path for backtesting only.
- [ ] Confirm no live trading, order execution, or strategy redesign is requested.
- [ ] Confirm whether README usage documentation should be updated during implementation.

## After Implementation

- [ ] Update `STATUS.md` if active task, current step, next step, or completion state changes.
- [ ] Mark checklist items complete only after acceptance criteria and verification pass.
- [ ] Leave uncertain items open and document the uncertainty.
- [ ] Confirm the next step is accurate or explicitly left undecided.

# Acceptance Criteria

- PostgreSQL `candles` rows can be loaded as a standard candle `DataFrame` with exactly the consumer-facing fields `timestamp`, `open`, `high`, `low`, `close`, and `volume`.
- `timestamp` maps from `candles.open_time`.
- Rows are sorted ascending by `timestamp`.
- The provider can filter by `source`, `symbol`, `interval`, optional start time, and optional end time.
- Provider-loaded candles can be passed to `BasicBacktester.run(...)` without using CSV.
- Tests cover the standard schema mapping and timestamp semantics.
- Tests use mocked/fake DB behavior and/or optional PostgreSQL integration that is skipped when no test database URL is configured.
- Tests do not call Binance endpoints, exchange account APIs, or order endpoints.
- No live-trading, signed request, API-key, `.env`, or real order behavior is added.

# Required Tests

## Unit Tests

- PostgreSQL row/query result maps to standard candle columns only.
- `open_time` maps to `timestamp`.
- Numeric OHLCV values are returned in a form accepted by existing backtest validation.
- Rows are sorted ascending by `timestamp` even if the database/fake input order requires ordering verification.
- Source, symbol, interval, start-time, and end-time filters are passed to the query/repository layer as expected.

## Integration Tests

- Optional PostgreSQL integration test may load fixture `candles` rows and verify the provider returns standard schema rows.
- Optional integration tests must be skipped unless a dedicated test database URL such as `QUANT_BITCOIN_TEST_DATABASE_URL` is configured.

## Contract Tests

- Provider output follows `docs/04_DATA_CONTRACT.md`.
- Provider output can be consumed by `BasicBacktester.run(...)` with a deterministic test strategy.
- Binance-specific persistence columns do not appear in the returned backtest input `DataFrame`.

## Safety Tests

- No real Binance network calls.
- No exchange account API calls.
- No order endpoint calls.
- No API-key, signed-request, `.env`, or live-trading behavior.

# Review Checklist

- Scope respected.
- Requirement matched.
- Role ownership respected.
- Architecture boundaries respected.
- Existing standard candle data contract preserved.
- Existing backtest engine public contract preserved.
- Persistence-specific metadata does not leak into strategy inputs.
- No hardcoded secrets.
- No tracked `.env` files.
- No real order execution.
- No exchange order endpoint calls.
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
