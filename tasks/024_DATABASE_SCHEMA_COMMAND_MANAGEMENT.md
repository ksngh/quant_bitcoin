# Task 024: Database Schema Command Management

# Goal

Move PostgreSQL schema ownership to version-controlled database command files under `db/`, remove duplicated DDL ownership from application code, and define a repeatable startup/update path for DDL and DML commands.

# Source Requirement

Project owner request on 2026-05-16:

- DDL must not be duplicated between application code and database files.
- Prefer managing database schema from the `db/` side.
- First check whether other database-related commands are duplicated.
- Ensure DDL and DML are executed when the database is first started.
- Database commands must be version controlled because future differences between the current DB state and desired state require explicit commands.
- Write this task document first before implementation.

# Clean Requirement

Create a single source of truth for PostgreSQL database DDL/DML command management in version-controlled `db/` files. Application code may execute database command files for local initialization, but it must not own a separate duplicated schema string. The implementation task must audit existing duplicated database commands, define and apply a clear file layout for initial DDL/DML and future change commands, update callers/tests/docs accordingly, and preserve all existing behavior without adding unrelated services or trading behavior.

# Extracted Roles

- Owner role: Database Schema / Command Management
- Supporting roles: Persistence, Docker Compose local startup, CLI initialization, Test Designer, Documentation
- Forbidden roles: Live Trading, Real Binance order execution, Exchange account APIs, Dashboard, FastAPI, Streamlit, Scheduler, Risk Management, Portfolio Optimization, Machine Learning

# Context

The project currently creates PostgreSQL tables in two places:

1. `db/init/001_market_data.sql`, mounted into the PostgreSQL container through Docker Compose for first-time database initialization.
2. `SCHEMA_SQL` in `quant_bitcoin/persistence/postgres.py`, executed by repository `initialize_schema()` methods.

This duplication means fresh Docker databases and application-triggered schema initialization can drift if one definition changes without the other. Task 024 should consolidate schema command ownership under `db/` and keep application code as a command-file executor or consumer, not as the schema authority.

The current database command audit found these duplicate DDL owners:

- `db/init/001_market_data.sql` contains `CREATE TABLE` / `CREATE INDEX` statements for `candles`, `ingestion_checkpoints`, `strategy_configs`, `backtest_runs`, `backtest_results`, `backtest_trades`, and `backtest_graph_points`.
- `quant_bitcoin/persistence/postgres.py` contains a duplicated `SCHEMA_SQL` string with the same table/index DDL.
- Tests import and assert against `SCHEMA_SQL`, so tests will need to be updated to validate the DB command files instead.

The audit also found DML command strings in application code for runtime behavior, such as candle upserts, checkpoint upserts, and backtest result inserts. Those runtime DML statements are not schema-initialization commands by default, but Task 024 should explicitly decide and document which DML belongs under `db/` initialization/change-command management and which DML remains application-owned runtime persistence logic.

# Scope

- Audit current database command duplication across `db/`, `quant_bitcoin/`, `tests/`, docs, and task files.
- Make `db/` the source of truth for schema DDL and initialization DML command files.
- Replace application-owned duplicated DDL constants with loading/executing version-controlled SQL files from `db/`.
- Ensure first-time Docker PostgreSQL startup executes the managed DDL/DML files.
- Define a version-controlled database command layout for:
  - initial schema DDL,
  - optional initial/reference DML,
  - future explicit change commands when the desired schema differs from an existing database state.
- Update repository `initialize_schema()` behavior to use DB command files without duplicating DDL text in Python.
- Update tests so ordinary tests verify command-file discovery/content without requiring real PostgreSQL, Docker, Binance, or external network access.
- Update docs to explain where DB commands live, how first startup runs them, and how future schema/data changes should be added.
- Update `STATUS.md` during implementation if phase, step, goal, active task, blocker, open question, or completion state changes.

# Out of Scope

- Changing the accepted table schema unless required only to remove duplication.
- Adding a full migration framework unless explicitly justified and kept minimal for this task.
- Redesigning repositories or changing public persistence behavior beyond schema initialization command loading.
- Changing backtest algorithms, strategy behavior, candle data contracts, or read-model payload shapes.
- Drawing graphs, dashboards, FastAPI, Streamlit, schedulers, daemon behavior, or Docker service redesign beyond DB command startup wiring.
- Live trading, real Binance order execution, exchange account APIs, API keys, signed requests, tracked `.env` files, futures, leverage, risk management, portfolio optimization, or machine learning.

# Requirements

- Read `AGENTS.md`, `STATUS.md`, `docs/10_CODEX_COMMAND_GUIDE.md`, this task file, relevant persistence docs/tasks, and `reviews/CODEX_SELF_REVIEW.md` before coding.
- Do not start implementation until this task document is approved for implementation.
- Preserve the current accepted PostgreSQL schema unless a concrete mismatch is found and documented.
- Remove DDL duplication: schema DDL must be stored in version-controlled DB command files, not hardcoded separately in Python.
- Python repository initialization may read DB command files, but it must not maintain an independent duplicated schema string.
- First-time database startup via Docker Compose must execute the managed DDL and any managed initial/reference DML.
- Future database state changes must be represented by explicit version-controlled DB command files.
- The implementation must document whether runtime persistence SQL DML remains in application code or moves to DB command files, and why.
- Ordinary tests must not require real PostgreSQL, Docker, Binance, or external network access.
- No live trading, signed requests, exchange account APIs, order endpoints, API-key handling, or tracked `.env` behavior may be added.

# Proposed DB Command Layout

The implementation task should validate or refine this layout before editing code:

```text
db/
  init/
    001_schema.sql          # first-start schema DDL, executed by Docker init
    002_seed_data.sql       # optional first-start/reference DML if needed
  changes/
    024_001_<description>.sql  # explicit future update command files
```

Guidance:

- `db/init/` is for first-time database creation through Docker's `/docker-entrypoint-initdb.d` behavior.
- `db/changes/` is for explicit version-controlled commands that describe how to move an already-existing database from an older desired state to a newer one.
- If no seed/reference DML is currently needed, create no-op or documented placeholder behavior only if useful; do not invent business data.
- File names should be ordered and stable so execution order is deterministic.

# Implementation Notes

- Existing `db/init/001_market_data.sql` may be renamed or split if the task chooses, but Docker Compose must still mount the command directory and execute the intended files on a fresh volume.
- `PostgresCandleRepository.initialize_schema()` and `PostgresBacktestResultRepository.initialize_schema()` should likely call shared SQL-file loading/execution logic rather than `connection.execute(SCHEMA_SQL)`.
- Tests that currently assert against `SCHEMA_SQL` should be changed to assert against the version-controlled SQL command files or a loaded DB command bundle.
- If application code needs a constant for tests or execution, it should be derived from DB command files at runtime/test time rather than manually copied.
- The implementation should consider whether multiple SQL statements are executed correctly by the selected psycopg execution path and test this with fakes where practical.

# Status Tracking

## Before Implementation

- [ ] Read `AGENTS.md`.
- [ ] Read `STATUS.md`.
- [ ] Read `docs/10_CODEX_COMMAND_GUIDE.md`.
- [ ] Read `reviews/CODEX_SELF_REVIEW.md`.
- [ ] Read this task file.
- [ ] Audit duplicated DB DDL/DML command ownership.
- [ ] Confirm this task is DB command management only and does not change trading behavior.
- [ ] Confirm no live trading, exchange order execution, graph UI, API service, or scheduler behavior is requested.

## After Implementation

- [ ] Update `STATUS.md` if active task, current step, next step, or completion state changes.
- [ ] Mark checklist items complete only after acceptance criteria and verification pass.
- [ ] Leave uncertain items open and document the uncertainty.
- [ ] Confirm the next step is accurate or explicitly left undecided.

# Acceptance Criteria

- The repository has a documented audit of current duplicated DB command ownership.
- PostgreSQL schema DDL is managed from version-controlled files under `db/`.
- Application code no longer owns a separate duplicated schema DDL string.
- Repository schema initialization executes the managed DB command files or otherwise delegates to the DB command source of truth.
- Docker first-time PostgreSQL startup executes the managed DDL and any managed initial/reference DML files.
- Future DB state changes have a documented version-controlled command-file location and naming convention.
- Tests are updated to validate the DB command files and initialization wiring without requiring real PostgreSQL, Docker, Binance, or external network access.
- Documentation explains where DB commands live, how fresh startup works, how application initialization works, and how future DB changes should be added.
- Existing persistence, backfill, ingestion, backtest write, and backtest read behavior remains compatible with the accepted schema.
- No graph UI, dashboard, FastAPI, Streamlit, scheduler, live trading, exchange account API, API-key, signed-request, tracked `.env`, or order endpoint behavior is added.

# Required Tests

## Unit Tests

- DB command loader returns deterministic SQL command files in execution order.
- Repository `initialize_schema()` executes DB command-file SQL instead of a hardcoded duplicated schema string.
- DDL definitions used by tests are loaded from `db/` command files.
- Current table names, key constraints, and indexes are still present in managed DB command files.
- Future-change command directory behavior is explicit when no change files exist.

## Integration Tests

- Optional PostgreSQL integration tests may verify fresh schema initialization against a dedicated test database.
- Optional integration tests must be skipped unless a dedicated test database URL such as `QUANT_BITCOIN_TEST_DATABASE_URL` is configured.
- Docker startup verification remains optional in environments without Docker, but Docker Compose command-file mounting must be testable or documented.

## Contract Tests

- Standard candle persistence contract remains unchanged.
- Backtest result persistence schema remains compatible with Task 021/022 accepted tables.
- Backtest graph read model remains compatible with Task 023 read queries.
- Runtime persistence DML still writes the same rows and does not move into first-start seed files unless explicitly documented and tested.

## Safety Tests

- No real Binance network calls.
- No exchange account API calls.
- No order endpoint calls.
- No API-key, signed-request, tracked `.env`, or live-trading behavior.
- Ordinary tests must not open external network connections.

# Review Checklist

- Scope respected.
- Requirement matched.
- DB command source of truth is under `db/`.
- Duplicate schema DDL ownership removed.
- First-start DDL/DML execution path documented and preserved.
- Future DB change command path documented.
- No accepted schema regression.
- No runtime persistence regression.
- No hardcoded secrets.
- No tracked `.env` files.
- No real order execution.
- No exchange order endpoint calls.
- No scheduler, dashboard, FastAPI, or Streamlit added.
- No unnecessary migration framework or abstractions.

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
