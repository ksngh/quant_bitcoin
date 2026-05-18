# Task 058: Pattern Backtest All Implemented Pattern Selection

# Goal

Extend the existing Task 057 pattern-selection seam so the PostgreSQL-backed pattern backtest CLI and the supporting pattern strategy backtest workflow can explicitly select and backtest every already-implemented pattern that has both:

1. an existing detector, and
2. an existing risk/exit planner compatible with the shared Task 054/055 exit simulation workflow.

The target pattern identifiers are:

- `FAIR_VALUE_GAP`
- `TRENDLINE_BREAK`
- `ORDER_BLOCK`
- `CUP_AND_HANDLE`
- `DIAMOND`
- `ADAM_AND_EVE`

Each target pattern may be wired only if it can be safely connected to the existing backtest workflow without shared contract redesign.

# Source Requirement

Owner request, translated and cleaned:

Extend `quant-bitcoin-pattern-backtest` and the supporting pattern strategy backtest configuration so `--pattern` can explicitly select any supported already-implemented pattern, while keeping `FAIR_VALUE_GAP` as the default. Each supported pattern must reuse its existing detector, existing risk/exit planner, and the existing `simulate_pattern_exit` API. Unsupported or not-yet-wireable pattern names must fail before the provider or backtest runner executes.

This task follows Task 057, which made the Fair Value Gap default explicit and introduced an FVG-only pattern-selection seam.

# Dependencies

This task depends on completed and verified behavior from:

- Task 040 through Task 045 pattern detector implementations.
- Task 048 through Task 053 pattern-specific risk/exit plan implementations.
- Task 054 Pattern Exit Simulation Integration.
- Task 055 Pattern Strategy Backtest.
- Task 056 Pattern PostgreSQL Backtest CLI.
- Task 057 Pattern Backtest CLI Clarity and Pattern Selection.

# Extracted Roles

- Owner role: CLI/backtest orchestration for historical PostgreSQL-backed pattern strategy backtests over stored completed candles.
- Supporting roles:
  - Existing pattern detector modules under `quant_bitcoin/patterns/` identify completed-candle pattern events.
  - Existing pattern-specific risk/exit planner modules under `quant_bitcoin/patterns/` convert supported events into shared `RiskExitPlan` objects and optional soft-invalidation metadata.
  - Existing `simulate_pattern_exit` logic evaluates stops, targets, invalidation, time stops, break-even behavior, trailing stops, and partial exits.
  - Existing PostgreSQL candle provider loads already-stored candles into the standard candle schema.
  - README/status documentation explains safe historical-simulation usage.
  - Tests verify parser help, validation, JSON strategy metadata, selected pattern propagation, deterministic supported-pattern behavior, and safety boundaries.
- Forbidden roles:
  - Live trading.
  - Real Binance order execution.
  - Paper-trader order placement.
  - API-key, `.env`, signed exchange-client, account endpoint, or order endpoint handling.
  - New pattern algorithm design.
  - Shared candle schema, pattern event contract, risk/exit contract, exit simulation contract, PostgreSQL schema, or backtest persistence redesign.
  - Scheduler, dashboard, FastAPI, Streamlit, Docker, machine learning, futures, leverage, or portfolio optimization.

# Responsibility Boundary

This task may refine the focused pattern-selection registry and route selected supported pattern identifiers to existing detector and risk/exit planner pairs. It must preserve the Task 054/055 backtest and exit-simulation contracts.

If any target pattern event model cannot be adapted to the existing Task 054/055 workflow without changing shared contracts, the implementation must leave that pattern unsupported, fail clearly during validation, and document the reason in `STATUS.md` or the task completion summary. It must not silently redesign a shared contract or silently fall back to `FAIR_VALUE_GAP`.

# Relevant Context To Read Before Implementation

- `AGENTS.md`
- `STATUS.md`
- `docs/03_ARCHITECTURE_RULES.md`
- `docs/04_DATA_CONTRACT.md`
- `docs/05_TEST_STRATEGY.md`
- `docs/10_CODEX_COMMAND_GUIDE.md`
- `reviews/CODEX_SELF_REVIEW.md`
- `tasks/040_PATTERN_DETECTION_ENGINE.md`
- `tasks/041_TRENDLINE_BREAK_PATTERN_ENGINE.md`
- `tasks/042_ORDER_BLOCK_PATTERN_ENGINE.md`
- `tasks/043_CUP_AND_HANDLE_PATTERN_ENGINE.md`
- `tasks/044_DIAMOND_PATTERN_ENGINE.md`
- `tasks/045_ADAM_AND_EVE_PATTERN_ENGINE.md`
- `tasks/048_TRENDLINE_BREAK_RISK_EXIT_PLAN.md`
- `tasks/049_ORDER_BLOCK_RISK_EXIT_PLAN.md`
- `tasks/050_FAIR_VALUE_GAP_RISK_EXIT_PLAN.md`
- `tasks/051_CUP_AND_HANDLE_RISK_EXIT_PLAN.md`
- `tasks/052_DIAMOND_RISK_EXIT_PLAN.md`
- `tasks/053_ADAM_AND_EVE_RISK_EXIT_PLAN.md`
- `tasks/054_PATTERN_EXIT_SIMULATION_INTEGRATION.md`
- `tasks/055_PATTERN_STRATEGY_BACKTEST.md`
- `tasks/056_PATTERN_POSTGRES_BACKTEST_CLI.md`
- `tasks/057_PATTERN_BACKTEST_CLI_CLARITY_AND_PATTERN_SELECTION.md`
- `quant_bitcoin/backtesting/pattern_strategy.py`
- `quant_bitcoin/backtesting/pattern_postgres_runner_cli.py`
- `quant_bitcoin/patterns/`
- `tests/backtesting/test_pattern_strategy_backtest.py`
- `tests/backtesting/test_pattern_postgres_runner_cli.py`
- `README.md`

# Scope

- Add all safely wireable already-implemented patterns to the pattern-selection registry.
- Keep `FAIR_VALUE_GAP` as the default selected pattern.
- Allow one selected pattern per CLI run unless the implementation explicitly defines and tests deterministic multi-pattern behavior.
- If multiple `--pattern` values are allowed, define deterministic same-candle priority order and test it.
- If multi-pattern behavior is not implemented, explicitly reject multiple pattern values with a clear error before provider or backtest execution.
- Add deterministic strategy names for each supported single-pattern run, for example:
  - `FAIR_VALUE_GAP_PATTERN_STRATEGY`
  - `TRENDLINE_BREAK_PATTERN_STRATEGY`
  - `ORDER_BLOCK_PATTERN_STRATEGY`
  - `CUP_AND_HANDLE_PATTERN_STRATEGY`
  - `DIAMOND_PATTERN_STRATEGY`
  - `ADAM_AND_EVE_PATTERN_STRATEGY`
- Keep JSON selected pattern identifiers stable and explicit.
- Keep candle input limited to the standard candle schema.
- Keep PostgreSQL usage limited to loading existing stored candles through the existing provider.
- Update README examples for the expanded supported-pattern selection behavior.
- Update `STATUS.md` when project state changes.

# Out of Scope

- Live trading.
- Real Binance order execution.
- Paper-trader order placement.
- API keys.
- `.env` file requirements.
- Signed exchange clients.
- Binance order/account endpoints.
- New pattern algorithms.
- Shared candle schema redesign.
- Shared pattern event contract redesign.
- Shared risk/exit contract redesign.
- Exit simulation contract redesign.
- PostgreSQL schema changes.
- Backtest persistence changes.
- Scheduler.
- Dashboard.
- FastAPI.
- Streamlit.
- Docker.
- Machine learning.
- Futures.
- Leverage.
- Portfolio optimization.

# Requirements

- Introduce or refine a focused pattern registry that maps each supported pattern identifier to:
  - detector function,
  - risk/exit planner function,
  - config object/defaults,
  - deterministic strategy name, and
  - soft invalidation behavior, if applicable.
- Reuse existing pattern detector modules under `quant_bitcoin/patterns/`.
- Reuse existing pattern-specific risk/exit planners under `quant_bitcoin/patterns/`.
- Reuse `simulate_pattern_exit`; do not duplicate exit simulation logic.
- Do not silently fall back to `FAIR_VALUE_GAP` if an unsupported pattern is requested.
- Preserve caller candle data immutability.
- Preserve ascending timestamp validation and standard candle schema validation.
- Preserve one-open-position-at-a-time behavior unless a deterministic tested policy changes it.
- Preserve exit evaluation starting on the candle after entry unless explicitly changed and tested.
- Keep PostgreSQL access limited to loading already-stored candles through the existing provider.
- Keep CLI and tests free of live PostgreSQL, network, exchange, API-key, or `.env` requirements by using existing fakes, mocks, or dependency injection.
- If a target pattern cannot be wired safely without redesigning shared contracts, leave it unsupported, test that it fails before provider/backtest execution, and document the reason in `STATUS.md` or the task completion summary.

# Pattern Registry Expectations

The implementation should make the supported pattern set explicit and deterministic. A registry entry should include enough information for the strategy/backtest workflow to run a selected single pattern without pattern-specific branching scattered across the CLI.

Each supported target should be reviewed for:

- detector availability,
- risk/exit planner availability,
- compatible event status/direction mapping,
- compatible risk plan output,
- compatible soft invalidation metadata, if applicable,
- deterministic event ordering,
- deterministic entry candle and exit-simulation handoff, and
- no need for shared contract redesign.

# Assumptions For Future Implementation

- `FAIR_VALUE_GAP` remains the default and must continue to behave as it did after Task 057.
- One selected pattern per CLI run is the preferred first implementation unless deterministic multi-pattern behavior is intentionally specified and fully tested.
- One open simulated position at a time remains the existing policy unless intentionally changed and fully tested.
- JSON stdout remains sufficient for CLI output.
- Unsupported but implemented detector-only or incompatible detector/planner pairs should not be advertised as supported choices unless the CLI clearly fails them before provider/backtest execution.
- Any not-yet-wireable target pattern should be documented as a known limitation rather than hidden by a fallback default.

# Open Questions Before Implementation

Resolve or document these before coding if the answer is not already clear from reviewed files:

- Which of the target pattern identifiers can be wired safely without changing shared event, risk/exit, or exit simulation contracts?
- Should this task support only one `--pattern` value per run, or explicitly implement deterministic multi-pattern runs?
- If multi-pattern runs are implemented, what is the deterministic same-candle priority order?
- For any target pattern where deterministic synthetic entry construction is difficult, what deterministic no-trade test will prove safe selection and no contract violation?
- Should unsupported target pattern names appear in help as unsupported, or should help list only currently supported choices?

# Status Tracking

## Before Implementation

- [ ] Read `STATUS.md`.
- [ ] Confirm this task matches the current phase and step.
- [ ] Confirm the current active task is recorded or should be updated.
- [ ] Confirm whether any shared contract change is required; stop and report if a redesign is needed.
- [ ] Confirm parallel work is not needed unless independent leaf tasks are explicitly identified.
- [ ] Record assumptions, blockers, not-yet-wireable patterns, or unclear status items before coding.

## After Implementation

- [ ] Update `STATUS.md` if the phase, step, goal, active task, blocker, open question, or completion state changed.
- [ ] Mark checklist items complete only when acceptance criteria and verification are satisfied.
- [ ] Leave uncertain items open and document the uncertainty.
- [ ] Confirm the next step is accurate or explicitly left undecided.

# Acceptance Criteria

- The default CLI invocation still backtests `FAIR_VALUE_GAP`.
- Every safely wireable implemented pattern can be selected via `--pattern`.
- Unsupported or not-yet-wireable patterns fail clearly before provider/backtest execution.
- JSON output has deterministic strategy names and selected pattern identifiers.
- Existing Fair Value Gap behavior and tests continue to pass.
- New tests cover every supported pattern selection path.
- Pattern selection does not mutate caller-provided candle data.
- Backtests continue to validate ascending timestamps and the standard candle schema.
- Backtests continue to use `simulate_pattern_exit` for exit simulation.
- No live trading, exchange order execution, API-key, `.env`, scheduler, dashboard, persistence schema, or Docker behavior is introduced.

# Required Tests

## Unit Tests

- Default selected pattern remains `FAIR_VALUE_GAP`.
- Supported pattern registry includes every safely wireable implemented pattern.
- `validate_pattern_selection()` accepts each supported pattern.
- `validate_pattern_selection()` rejects unsupported names.
- `strategy_name_for_patterns()` returns deterministic names for every supported single-pattern selection.
- `PatternStrategyBacktestConfig` receives and preserves the selected supported pattern.
- Caller-provided candle data remains unmutated after running every supported pattern backtest.
- Unsupported patterns fail before detection, planning, or backtest execution.

## CLI/Parser Tests

- `python -m quant_bitcoin.backtesting.pattern_postgres_runner_cli --help` lists supported pattern choices.
- Help text states that `FAIR_VALUE_GAP` remains the default.
- `--pattern FAIR_VALUE_GAP` works.
- `--pattern TRENDLINE_BREAK` works if supported.
- `--pattern ORDER_BLOCK` works if supported.
- `--pattern CUP_AND_HANDLE` works if supported.
- `--pattern DIAMOND` works if supported.
- `--pattern ADAM_AND_EVE` works if supported.
- Unsupported `--pattern` fails with a clear parser or validation error.
- If multiple `--pattern` values are not supported, multiple values fail clearly before provider/backtest execution.
- CLI fake-provider tests verify selected pattern is passed into `PatternStrategyBacktestConfig`.
- CLI JSON output includes the selected pattern and deterministic strategy name.

## Pattern/Backtest Integration Tests

- For each supported pattern, add at least one synthetic-candle test that proves a deterministic entry path.
- If deterministic synthetic entry construction is not practical for a pattern, add a deterministic no-trade test and document why in the test or task summary.
- Verify each supported pattern reuses its existing detector, risk/exit planner, and `simulate_pattern_exit`.
- Verify selected pattern identifiers in JSON are stable explicit strings.
- Verify candle input still uses only the standard candle schema.
- Verify no unsupported pattern reaches the detector or planner layer.

## Safety Tests

- Verify no exchange order client dependency is instantiated in the CLI or backtest path.
- Verify no paper trader order placement is invoked.
- Verify no API keys, secrets, `.env` files, live-trading toggles, Binance order endpoints, signed exchange requests, or account endpoints are required.
- Verify `--help` does not connect to PostgreSQL, Binance, or any network socket.
- Verify tests use fakes/mocks and do not require live PostgreSQL or network access.

# Documentation Updates

- Update README to show examples for:
  - default Fair Value Gap pattern backtest,
  - at least one explicit non-Fair-Value-Gap pattern selection if implemented, and
  - the list of supported `--pattern` values.
- README must state this is historical simulation over stored candles only.
- README must state it does not place orders or call exchange order/account endpoints.
- Update `STATUS.md` when project state changes.

# Verification

Required verification after implementation:

```bash
pytest tests/backtesting/test_pattern_strategy_backtest.py tests/backtesting/test_pattern_postgres_runner_cli.py -q
pytest
python -m quant_bitcoin.backtesting.pattern_postgres_runner_cli --help
git diff --check
```

# Codex Self-Review Requirement

Before completion of any implementation work under this task, run through `reviews/CODEX_SELF_REVIEW.md` and include the result in the final summary.

For this task-document creation step, perform the same self-review at documentation scope and confirm no application behavior was implemented.

# PR Review Requirement

Use `reviews/REVIEW_CHECKLIST.md` and `docs/06_PR_REVIEW_PROCESS.md` before merge.

Review must be strict about:

- scope expansion beyond historical pattern strategy backtesting,
- unsupported selections silently falling back to `FAIR_VALUE_GAP`,
- multi-pattern behavior without deterministic priority and tests,
- missing parser/help, registry, config propagation, JSON-output, or safety tests,
- duplicated detector, risk/exit planner, or exit simulation logic,
- hidden shared contract redesign,
- data contract violations,
- PostgreSQL schema or persistence changes,
- hardcoded secrets,
- unsafe live trading behavior,
- accidental exchange order/account endpoint calls, and
- unnecessary abstractions.

# Completion Summary Required

- files changed
- implementation summary
- tests added or updated
- tests run
- Codex self-review result
- known limitations
- recommended next task
