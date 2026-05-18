# Task 056: Pattern PostgreSQL Backtest CLI

# Goal

Add a runnable command-line workflow for executing the existing pattern strategy backtest against 1-minute candle data already stored in PostgreSQL.

The command should be exposed as `quant-bitcoin-pattern-backtest`, load standard completed `1m` candles through the existing PostgreSQL candle data provider, delegate simulation to the existing pattern strategy backtest implementation, and print a deterministic backtest summary suitable for local verification.

# Source Requirement

Owner request, translated and cleaned:

1. Make pattern backtesting executable through a new command such as `quant-bitcoin-pattern-backtest`.
2. Enable the command to backtest from 1-minute candle data stored in the database.
3. Integrate with the PostgreSQL candle data provider.
4. Reuse the existing pattern strategy backtest.
5. Add tests for the database-backed 1-minute retrieval flow and CLI help.

# Clean Requirement

Create a small CLI entrypoint that reads already-persisted PostgreSQL `1m` candles as the standard candle schema, runs the existing pure historical pattern strategy backtest over those candles, and prints a safe, deterministic result without introducing live trading, order execution, new schema design, scheduler behavior, or dashboard behavior.

# Dependencies

This task depends on completed and verified behavior from:

- Task 019 PostgreSQL Candle Data Provider for Backtesting.
- Task 020 PostgreSQL Backtest Runner for established CLI/provider wiring conventions.
- Task 055 Pattern Strategy Backtest for the existing pattern backtest engine/workflow to reuse.
- Existing project script entrypoint configuration in `pyproject.toml`.

# Extracted Roles

- Owner role: CLI orchestration for database-backed pattern strategy backtests.
- Supporting roles:
  - `PostgresCandleDataProvider` loads persisted candles and normalizes them to the standard candle schema.
  - The existing pattern strategy backtest workflow performs pattern detection, risk/exit planning, and simulated exits.
  - CLI parsing validates user inputs and prints a deterministic result summary.
  - Tests use fakes/mocks to prove wiring without requiring a live PostgreSQL server.
- Forbidden roles:
  - Live trading.
  - Real Binance order execution.
  - Exchange order API calls.
  - Binance historical fetching or WebSocket ingestion.
  - New database schema redesign.
  - Scheduler, dashboard, FastAPI, Streamlit, Docker, machine learning, futures, leverage, or portfolio optimization.
  - Strategy logic directly reading PostgreSQL, environment secrets, `.env` files, or exchange clients.

# Responsibility Boundary

This task is responsible for adding an executable wrapper around already-implemented components. It must not redesign the candle data contract, pattern event contract, risk/exit plan contract, exit simulation contract, pattern strategy result model, or database schema.

If the existing pattern strategy result model is insufficient for the desired CLI output, keep the CLI output limited to the available result fields and document any future enhancement rather than changing shared contracts in this task.

# Relevant Context To Read Before Implementation

- `AGENTS.md`
- `STATUS.md`
- `docs/03_ARCHITECTURE_RULES.md`
- `docs/04_DATA_CONTRACT.md`
- `docs/05_TEST_STRATEGY.md`
- `docs/10_CODEX_COMMAND_GUIDE.md`
- `reviews/CODEX_SELF_REVIEW.md`
- `tasks/019_POSTGRES_CANDLE_DATA_PROVIDER.md`
- `tasks/020_POSTGRES_BACKTEST_RUNNER.md`
- `tasks/055_PATTERN_STRATEGY_BACKTEST.md`
- `quant_bitcoin/market_data/postgres_provider.py`
- `quant_bitcoin/backtesting/postgres_runner_cli.py`
- `quant_bitcoin/backtesting/pattern_strategy.py`
- Existing CLI tests and backtesting tests under `tests/`.

# Scope

- Add a `quant-bitcoin-pattern-backtest` project script entrypoint.
- Add a CLI module for PostgreSQL-backed pattern strategy backtests.
- Use `PostgresCandleDataProvider.from_database_url` or an equivalent dependency-injected provider factory.
- Default the candle interval to `1m` and keep the flow explicitly oriented around completed 1-minute candles.
- Accept database connection and candle query options consistent with existing project CLI conventions where practical, such as source, symbol, interval, start time, and end time.
- Run the existing pattern strategy backtest implementation from Task 055 instead of duplicating pattern simulation logic.
- Print a deterministic JSON-style summary of the run using available pattern strategy backtest result fields.
- Add tests for CLI help and database-backed 1-minute candle retrieval wiring with fakes/mocks.
- Add safety-oriented tests or assertions proving no live trading, order execution, Binance order endpoint, API key, or `.env` dependency is introduced.
- Update `STATUS.md` if the project phase, step, goal, active task, open questions, blockers, or completion state changes.

# Out of Scope

- Live trading.
- Real Binance order execution.
- Exchange account/order endpoints.
- Paper trader integration.
- Fetching candles from Binance.
- WebSocket ingestion.
- Dashboard or scheduler behavior.
- New database schema redesign or migrations.
- Persisting pattern backtest results unless it can be done through an existing compatible persistence contract without schema changes; if compatibility is unclear, leave persistence out of this task.
- Adding new pattern algorithms, risk rules, indicators, or shared contracts.
- Changing Task 055 strategy semantics, including supported pattern set, one-position behavior, entry timing, exit timing, or duplicate-event handling, unless separately approved.
- Tests that require a live PostgreSQL server, Docker, Binance network access, or external services during default `pytest`.

# Requirements

- The project exposes an executable command named `quant-bitcoin-pattern-backtest`.
- `quant-bitcoin-pattern-backtest --help` succeeds without connecting to PostgreSQL.
- The CLI loads candles through the PostgreSQL candle provider boundary, not by writing raw SQL in strategy or backtest code.
- The default interval is `1m`.
- If an interval option is exposed, the task must either:
  - reject non-`1m` intervals with a clear error because this task is scoped to 1-minute candle data, or
  - document that only `1m` is supported by default and add tests proving the provider is called with `1m` when no override is supplied.
- Loaded candles must retain the standard candle schema expected by the existing pattern strategy backtest: `timestamp`, `open`, `high`, `low`, `close`, and `volume`.
- The CLI must reuse the existing pattern strategy backtest workflow from Task 055 and must not duplicate pattern detection, risk/exit planning, or exit simulation logic.
- The CLI must not create or call live trading clients, signed exchange clients, order-placement functions, account endpoints, paper-trader placement, or Binance order APIs.
- The CLI must not require API keys, secrets, `.env` files, Docker, or network access for `--help` or ordinary unit tests.
- Empty candle results should produce a deterministic, user-readable outcome without crashing from unrelated downstream assumptions.
- CLI argument parsing should follow existing project conventions from `quant-bitcoin-postgres-backtest` where practical.

# Assumptions For First Implementation

- The first CLI can use the Task 055 default pattern strategy configuration unless the owner assigns explicit CLI options for pattern selection or risk/exit tuning.
- JSON printed to stdout is sufficient for the initial runnable workflow.
- Result persistence is not required for this task unless the existing persistence contract can safely store the result without schema changes.
- Default verification should use dependency injection, fakes, or mocks rather than a real PostgreSQL service.

# Open Questions Before Implementation

Resolve or document these before coding if the answer is not already clear from reviewed files:

- Should the CLI expose pattern configuration options in the first implementation, or should it use Task 055 defaults only?
- Should non-`1m` intervals be rejected, hidden, or allowed as an advanced override while still defaulting to `1m`?
- Should the command persist results in an existing backtest result table, or print-only until a pattern-specific persistence task is approved?
- What exact result summary fields should be printed if the Task 055 result model differs from the RSI backtest CLI output model?

# Status Tracking

## Before Implementation

- [ ] Read `STATUS.md`.
- [ ] Confirm this task matches the current phase and step.
- [ ] Confirm the current active task is recorded or should be updated.
- [ ] Confirm no shared contract or schema changes are required.
- [ ] Confirm parallel work is not needed unless independent leaf tasks are explicitly identified.
- [ ] Record assumptions, blockers, or unclear status items before coding.

## After Implementation

- [ ] Update `STATUS.md` if the phase, step, goal, active task, blocker, open question, or completion state changed.
- [ ] Mark checklist items complete only when acceptance criteria and verification are satisfied.
- [ ] Leave uncertain items open and document the uncertainty.
- [ ] Confirm the next step is accurate or explicitly left undecided.

# Acceptance Criteria

- `quant-bitcoin-pattern-backtest --help` runs successfully.
- The command is registered as a project script entrypoint.
- The CLI defaults to loading PostgreSQL-backed `1m` candles through the existing PostgreSQL candle data provider.
- The database-backed 1-minute candle retrieval flow is covered by tests using fakes/mocks or skipped optional integration setup.
- The existing pattern strategy backtest implementation is reused rather than reimplemented.
- The CLI output is deterministic for tested inputs.
- No live trading API calls, Binance order execution calls, signed exchange clients, API keys, `.env` requirements, scheduler behavior, or dashboard behavior are introduced.
- Existing tests continue to pass.

# Required Tests

## Unit Tests

- `build_parser()` or equivalent supports `--help` without connecting to PostgreSQL.
- `main()` wires default interval `1m` into the PostgreSQL provider factory.
- `main()` passes standard candles returned by the provider into the existing pattern strategy backtest workflow.
- Empty provider results produce deterministic CLI output or a documented clean error path.
- Dependency injection allows tests to use fake provider/backtest factories without a live database.

## Integration Tests

- A fake or mocked PostgreSQL provider flow verifies source, symbol, interval, start time, and end time options are forwarded correctly.
- A CLI-level test runs the command entrypoint path or `main(["--help"])` equivalent and confirms success.
- Optional real PostgreSQL integration tests may be added only if they are skipped when no test database URL is configured.

## Contract Tests

- Verify the provider output passed to the pattern backtest contains only the standard candle consumer columns where practical.
- Verify the CLI imports and calls the existing Task 055 pattern backtest API rather than defining an incompatible duplicate simulation path.
- Verify command registration points to the intended CLI module.

## Safety Tests

- Verify no exchange order client dependency is instantiated in the CLI path.
- Verify no paper trader order placement is invoked.
- Verify no API keys, secrets, `.env` files, live-trading toggles, Binance order endpoints, or signed exchange requests are required by the CLI or tests.

# Verification

Default verification for the future implementation:

```bash
pytest
quant-bitcoin-pattern-backtest --help
```

Recommended targeted verification after implementation:

```bash
pytest tests/backtesting -q
python -m quant_bitcoin.backtesting.pattern_postgres_runner_cli --help
```

Documentation/task creation verification:

```bash
git diff --check
```

# Codex Self-Review Requirement

Before completion of any implementation work under this task, run through `reviews/CODEX_SELF_REVIEW.md` and include the result in the final summary.

For this task-document creation step, perform the same self-review at documentation scope and confirm no application behavior was implemented.

# PR Review Requirement

Use `reviews/REVIEW_CHECKLIST.md` and `docs/06_PR_REVIEW_PROCESS.md` before merge.

Review must be strict about:

- Scope expansion beyond a PostgreSQL-backed pattern backtest CLI.
- Missing CLI help or provider-wiring tests.
- Missing database-backed `1m` retrieval-flow coverage.
- Duplicating pattern strategy backtest logic instead of reusing Task 055 behavior.
- Hidden shared contract or schema changes.
- Architecture boundary violations between CLI, provider, strategy, backtest, persistence, and execution roles.
- Hardcoded secrets.
- Unsafe live trading behavior.
- Accidental exchange order calls.
- Unnecessary abstractions.

# Completion Summary Required

- files changed
- implementation summary
- tests added or updated
- tests run
- Codex self-review result
- known limitations
- recommended next task
