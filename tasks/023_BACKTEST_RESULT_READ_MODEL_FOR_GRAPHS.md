# Task 023: Backtest Result Read Model for Graphs

# Goal

Add a read-only application-layer interface for loading persisted backtest results in a graph-friendly shape after backtest result persistence exists.

# Source Requirement

User request on 2026-05-16:

- Backtest results should be saved to the database.
- Later, the database will be read to draw graphs.
- Define the immediate next tasks according to `AGENTS.md` before implementation.

# Extracted Roles

- Owner role: Backtest Result Query/Read Model
- Supporting roles: Persistence, Backtest Engine consumer, Test Designer, Documentation
- Forbidden roles: Dashboard, FastAPI, Streamlit, Scheduler, Live Trading, Real Binance order execution, Exchange account APIs, Risk Management, Portfolio Optimization, Machine Learning

# Context

Task 021 should define the graph-ready persistence schema. Task 022 should implement writes from `quant-bitcoin-postgres-backtest`. This task should add a small read path that future graphing code can consume without coupling graph code directly to write internals or re-running backtests.

This task is not a graph UI task. It should provide data retrieval and shape only.

# Scope

- Add a read-only repository/service method for loading one persisted backtest run by id.
- Return run metadata, strategy parameters, summary metrics, simulated trades, and graph-ready time-series points in deterministic order.
- Add a lightweight list/query method for recent runs or runs filtered by symbol/interval/time range if needed for selecting graph inputs.
- Document the returned shape for future graphing work.
- Add tests with fake/mocked persistence so ordinary tests do not require real PostgreSQL, Docker, Binance, or external network access.
- Update `STATUS.md` during implementation if phase, step, goal, active task, blocker, open question, or completion state changes.

# Out of Scope

- Drawing graphs.
- Dashboard, FastAPI, Streamlit, scheduler, or daemon behavior.
- Writing backtest results; that belongs to Task 022.
- Changing the backtest engine, strategy algorithms, or candle data contract.
- Live trading, real Binance order execution, exchange account APIs, API keys, signed requests, tracked `.env` files, futures, leverage, risk management, portfolio optimization, or machine learning.

# Requirements

- Read `AGENTS.md`, `STATUS.md`, `docs/10_CODEX_COMMAND_GUIDE.md`, `tasks/021_GRAPH_READY_BACKTEST_PERSISTENCE_SCHEMA.md`, `tasks/022_POSTGRES_BACKTEST_RESULT_PERSISTENCE.md`, this task file, and `reviews/CODEX_SELF_REVIEW.md` before coding.
- Do not start this task until Task 022 is complete and accepted.
- Keep implementation read-only.
- Return graph points in ascending timestamp order.
- Return trades in deterministic sequence order.
- Keep graph consumer data independent of live trading, exchange account APIs, and order endpoints.
- Ordinary tests must not require real PostgreSQL, Docker, Binance, or external network access.

# Status Tracking

## Before Implementation

- [x] Read `AGENTS.md`.
- [x] Read `STATUS.md`.
- [x] Read `docs/10_CODEX_COMMAND_GUIDE.md`.
- [x] Read `tasks/021_GRAPH_READY_BACKTEST_PERSISTENCE_SCHEMA.md`.
- [x] Read `tasks/022_POSTGRES_BACKTEST_RESULT_PERSISTENCE.md`.
- [x] Read `reviews/CODEX_SELF_REVIEW.md`.
- [x] Read this task file.
- [x] Confirm Task 022 is complete and accepted.
- [x] Confirm this task is read-only and does not implement a graph UI.

## After Implementation

- [x] Update `STATUS.md` if active task, current step, next step, or completion state changes.
- [x] Mark checklist items complete only after acceptance criteria and verification pass.
- [x] Leave uncertain items open and document the uncertainty.
- [x] Confirm the next step is accurate or explicitly left undecided.

# Acceptance Criteria

- A read-only path exists for loading a persisted backtest run by id.
- Returned data includes run metadata, strategy parameters, summary metrics, simulated trades, and graph-ready time-series points.
- Graph points are returned in ascending timestamp order.
- Trades are returned in deterministic sequence order.
- Documentation explains how future graphing code should consume the read model.
- Ordinary tests do not require real PostgreSQL, Docker, Binance, or external network access.
- No graph UI, dashboard, FastAPI, Streamlit, scheduler, live trading, exchange account API, API-key, signed-request, tracked `.env`, or order endpoint behavior is added.

# Required Tests

## Unit Tests

- Load backtest run by id returns deterministic metadata, summary, trades, and graph points.
- Trades are ordered by sequence.
- Graph points are ordered by timestamp/sequence according to the accepted schema.
- Missing run behavior is explicit and documented.

## Integration Tests

- Optional PostgreSQL integration tests may verify read behavior against fixture rows.
- Optional integration tests must be skipped unless a dedicated test database URL such as `QUANT_BITCOIN_TEST_DATABASE_URL` is configured.

## Contract Tests

- Read model does not mutate persisted rows.
- Read model does not require re-running a backtest.
- Read model does not call market-data providers or strategy code.

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
- Read-only behavior preserved.
- No graph UI added.
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
