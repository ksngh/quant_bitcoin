# Task 014: PostgreSQL Binance Backfill

# Goal

Implement PostgreSQL persistence, local Docker Compose startup, and full historical Binance 1-minute candle backfill after Task 013 approves the persistence schema.

# Source Requirement

User request on 2026-05-09:

- Assume PostgreSQL is the target database.
- Write an implementation task document for PostgreSQL + Docker Compose + full Binance 1-minute backfill.
- Do not implement files directly before task documentation and approval.

# Extracted Roles

- Owner role: Market Data Provider
- Supporting roles: Persistence, Configuration, Test Designer, Architect
- Forbidden roles: Strategy, Backtest Engine, Execution, Live Trading, Binance order client implementation

# Context

This task is an implementation task definition, not an implementation approval by itself. PostgreSQL and Docker are out of scope by default in `AGENTS.md`, so implementation must start only after explicit human approval of this task and completion or acceptance of Task 013.

# Scope

- Add local PostgreSQL support for market-data persistence.
- Add Docker Compose for local PostgreSQL startup.
- Add database initialization or migration path for the accepted candle schema.
- Implement a Binance historical 1-minute candle backfill that stores BTCUSDT candles.
- Make the backfill resumable from stored progress or the latest stored candle.
- Use duplicate-safe writes based on the accepted candle uniqueness rule.
- Store only closed candles.
- Handle Binance pagination, retryable errors, and rate-limit responses.
- Keep public market-data fetching separate from strategy and execution code.

# Out of Scope

- WebSocket ingestion.
- Live trading.
- Real Binance order endpoints.
- Signed requests.
- API keys or secrets.
- Strategy changes.
- Backtest behavior changes.
- Paper-trading orchestration.
- Dashboards.
- Production schedulers.
- Futures, leverage, or portfolio optimization.

# Requirements

- PostgreSQL must be the primary persistence target.
- Docker Compose must run PostgreSQL locally with non-secret development defaults or documented environment overrides.
- `.env` files must not be committed.
- The candle table must follow the schema accepted by Task 013.
- Historical backfill must target Binance public market-data endpoints only.
- The first target symbol is `BTCUSDT`.
- The first target interval is `1m`.
- The backfill must support full historical retrieval from Binance's earliest available candle through the latest closed candle.
- The backfill must be restartable without duplicating rows.
- The implementation must not call Binance order endpoints.
- Tests must mock network calls and must not depend on real Binance availability.

# Status Tracking

## Before Implementation

- [x] Read `AGENTS.md`.
- [x] Read `STATUS.md`.
- [x] Read `tasks/013_PERSISTENCE_SCHEMA_DESIGN.md`.
- [x] Confirm Task 013 is accepted.
- [x] Confirm explicit human approval to implement PostgreSQL and Docker Compose.
- [x] Confirm no live-trading approval is implied by this task.

## After Implementation

- [x] Update `STATUS.md` if active task, next step, or blocker changes.
- [x] Mark feasible non-Docker checklist items complete after acceptance criteria and verification pass. Docker runtime startup is intentionally skipped for the current cloud workflow, remains optional local developer verification, and is not marked passed.
- [x] Leave uncertain items open and document the uncertainty.

# Acceptance Criteria

- [ ] Docker Compose can start local PostgreSQL. Intentionally skipped for the current cloud workflow because Docker cannot be installed or run here; remains optional local developer verification and is not marked passed.
- [x] The accepted candle schema is created through the chosen initialization or migration path. Verified by schema contract tests and matching `db/init/001_market_data.sql`/repository schema SQL.
- [x] Binance 1-minute historical backfill can store BTCUSDT candles. Verified with mocked Binance kline responses.
- [x] Re-running the backfill is idempotent for already stored candles. Verified by duplicate-safe repository upsert SQL and optional PostgreSQL integration test coverage when a test database is configured.
- [x] The backfill resumes after interruption. Verified by latest stored candle start-time calculation and checkpoint persistence tests.
- [x] Open/in-progress candles are not persisted as final historical candles. Verified by unit tests.
- [x] Tests prove the implementation uses public market-data endpoints only. Verified by mocked endpoint safety tests and static safety scan.
- [x] No live-trading, signed request, API-key handling, or order execution behavior is added. Verified by tests and static safety scan.

# Required Tests

## Unit Tests

- Binance kline payload to persistence row mapping.
- Backfill pagination start/end calculation.
- Closed-candle filtering.
- Retry/rate-limit handling behavior with mocked responses.

## Integration Tests

- PostgreSQL persistence test using a local test database or containerized database if the test environment allows it.
- Idempotent upsert behavior for duplicate candles.

## Contract Tests

- Stored candle fields match the accepted schema from Task 013.
- Uniqueness rule prevents duplicate `source + symbol + interval + open_time` rows.

## Safety Tests

- Verify no Binance order endpoint is called.
- Verify no API keys, secrets, `.env` files, signed requests, or live-trading flags are introduced.

# Review Checklist

- Scope respected.
- Requirement matched.
- Role ownership respected.
- Architecture boundaries respected.
- Data contract respected.
- Docker is local development support only.
- No hardcoded secrets.
- No real order execution.
- No strategy or execution behavior changes.

# Verification

Default:

```bash
pytest
```

Additional implementation verification should include a documented local Docker Compose startup command, but the command must not be required for ordinary unit tests unless explicitly approved.

Current cloud workflow verification on 2026-05-12:

- `pytest` passed with ordinary tests and one optional PostgreSQL integration test skipped because `QUANT_BITCOIN_TEST_DATABASE_URL` was not configured.
- `git diff --check` passed.
- `python -m compileall quant_bitcoin` passed.
- Static safety scan for API keys, signed requests, live-trading flags, and order endpoints found no unsafe Task 014 behavior; expected safety-rule text may mention forbidden terms.
- Docker runtime startup is intentionally skipped for this cloud workflow because Docker cannot be installed or run in the current environment. This is an environment limitation, not a code failure; Docker Compose startup remains optional local developer verification.

Cloud workflow acceptance note:

Task 014 is accepted for the current cloud workflow based on completed non-Docker verification. Optional Docker Compose PostgreSQL startup verification may still be run later in a Docker-capable local developer environment, but it is not required to proceed with a separately approved next task.

# Codex Self-Review Requirement

Before completion, run through `reviews/CODEX_SELF_REVIEW.md` and include the result in the final summary.

# Completion Summary Required

- files changed
- implementation summary
- tests added or updated
- tests run
- Codex self-review result
- known limitations
- recommended next task
