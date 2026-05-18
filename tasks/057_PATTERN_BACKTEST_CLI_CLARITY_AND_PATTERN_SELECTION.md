# Task 057: Pattern Backtest CLI Clarity and Pattern Selection

# Goal

Clarify the existing pattern backtest CLI so users can see that the current default strategy is the Fair Value Gap pattern strategy, and extend the pattern backtest workflow so the same CLI/backtest shape can support other implemented pattern strategies through explicit pattern selection.

The immediate user-visible CLI changes are:

- CLI description should say: `Run the default Fair Value Gap pattern strategy backtest...` instead of the generic `Run a pattern strategy backtest...` wording.
- Help text must clearly state that the current default behavior is FVG-only.
- JSON output strategy name should change from `PATTERN_STRATEGY` to `FAIR_VALUE_GAP_PATTERN_STRATEGY` for the default FVG run.
- README or status documentation must include a concrete usage example for the pattern backtest CLI.

The extensibility goal is to prepare the command and backtest layer so additional supported patterns can be backtested in the same way without creating separate one-off CLIs for every pattern.

# Source Requirement

Owner request, translated and cleaned:

1. Make the CLI description more explicit.
   - Current: `Run a pattern strategy backtest...`
   - Desired: `Run the default Fair Value Gap pattern strategy backtest...`
2. Make the output strategy name more explicit.
   - Current: `"name": "PATTERN_STRATEGY"`
   - Desired: `"name": "FAIR_VALUE_GAP_PATTERN_STRATEGY"`
3. Show in help text that the current implementation is FVG-only.
4. Add a usage example in README or task/status documentation.
5. Create a task first before implementation.
6. After this task is assigned for implementation, make it possible to backtest other patterns in this same style.

# Clean Requirement

Update the PostgreSQL-backed pattern backtest CLI and its supporting pattern backtest configuration so the default Fair Value Gap behavior is explicit in command help and JSON output, while introducing a small, tested pattern-selection seam for additional already-implemented pattern detector/risk-exit pairs. Keep the default behavior backward-compatible except for clearer names/help text, and do not introduce live trading, new exchange clients, database schema changes, dashboard behavior, or real order execution.

# Dependencies

This task depends on completed and verified behavior from:

- Task 040 through Task 045 pattern detector implementations.
- Task 048 through Task 053 pattern-specific risk/exit plan implementations.
- Task 054 Pattern Exit Simulation Integration.
- Task 055 Pattern Strategy Backtest.
- Task 056 Pattern PostgreSQL Backtest CLI.

# Extracted Roles

- Owner role: CLI/backtest orchestration for historical PostgreSQL-backed pattern strategy backtests.
- Supporting roles:
  - Existing pattern detector modules identify completed-candle pattern events.
  - Existing pattern-specific risk/exit planners convert supported events into shared `RiskExitPlan` objects.
  - Existing exit simulation handles stop-loss, take-profit, invalidation, time-stop, break-even, trailing-stop, and partial-exit behavior.
  - README/status documentation explains safe local usage.
  - Tests verify parser help, JSON strategy metadata, pattern selection, and safety boundaries.
- Forbidden roles:
  - Live trading.
  - Real Binance order execution.
  - Exchange account/order endpoint calls.
  - API-key or `.env` requirements.
  - Binance historical fetching or WebSocket ingestion changes.
  - New database schema design or persistence model changes.
  - Scheduler, dashboard, FastAPI, Streamlit, Docker, machine learning, futures, leverage, or portfolio optimization.
  - Strategy logic directly reading PostgreSQL, environment secrets, `.env` files, exchange clients, or paper-trader placement APIs.

# Responsibility Boundary

This task may adjust the pattern backtest configuration and CLI wiring so selected patterns can be routed to their existing detector and existing risk/exit planner. It must not redesign the shared candle schema, pattern event models, risk/exit plan contracts, exit simulation contract, PostgreSQL candle schema, or backtest persistence schema.

If a pattern's detector output or risk/exit planner cannot be safely adapted to the existing Task 055 backtest result shape without a contract redesign, that pattern must be left unsupported with a clear validation error and a documented follow-up task rather than silently changing shared contracts.

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
- `quant_bitcoin/backtesting/pattern_strategy.py`
- `quant_bitcoin/backtesting/pattern_postgres_runner_cli.py`
- `quant_bitcoin/patterns/`
- `tests/backtesting/test_pattern_strategy_backtest.py`
- `tests/backtesting/test_pattern_postgres_runner_cli.py`
- `README.md`

# Scope

- Update the pattern CLI description to explicitly name the default Fair Value Gap pattern strategy backtest.
- Update CLI help text so users can see that the current default is FVG-only.
- Update JSON output strategy metadata so the default strategy name is `FAIR_VALUE_GAP_PATTERN_STRATEGY`.
- Add or update tests for the exact CLI description/help text and JSON strategy name.
- Add README usage documentation for `quant-bitcoin-pattern-backtest`, including a safe local example with `--start-time` and `--end-time`.
- Introduce an explicit pattern selection interface for the pattern backtest CLI/backtest config, such as a `--pattern` option and/or a focused internal pattern registry.
- Keep the default selected pattern as Fair Value Gap.
- Allow additional pattern names only when they are backed by an existing detector, existing risk/exit planner, deterministic event filtering, and deterministic soft-invalidation behavior compatible with Task 054/055 contracts.
- Reject unsupported or not-yet-wired pattern names with a clear parser or validation error.
- Preserve deterministic ordering when multiple patterns are configured or explicitly reject multi-pattern runs until a deterministic policy is fully tested.
- Keep tests free of live PostgreSQL, network, exchange, API-key, or `.env` requirements by using existing fakes/mocks/dependency injection.
- Update `STATUS.md` only for real project-state changes.

# Out of Scope

- Live trading or real order execution.
- Paper-trader order placement.
- Binance order endpoint integrations.
- API keys, `.env` files, signed clients, account endpoints, or live-trading toggles.
- New pattern algorithms beyond existing implemented detector modules.
- Redesigning pattern event contracts, risk/exit contracts, exit simulation contracts, market data contracts, or database schemas.
- Persisting pattern backtest results to PostgreSQL unless an existing persistence path can be reused without schema changes and is explicitly requested in a later task.
- Dashboard, graph UI, scheduler, FastAPI, Streamlit, Docker, machine learning, futures, leverage, or portfolio optimization.
- Broad CLI redesign unrelated to pattern strategy selection and clearer FVG wording.

# Requirements

- The default CLI parser description must include the phrase `Run the default Fair Value Gap pattern strategy backtest`.
- The CLI help output must mention that the current default behavior is FVG-only.
- The default JSON output must include:

```json
"strategy": {
  "name": "FAIR_VALUE_GAP_PATTERN_STRATEGY"
}
```

- The output should continue to include the selected pattern list and existing entry/exit metadata fields where available.
- The default command invocation with no pattern option must keep using Fair Value Gap.
- If a `--pattern` option is added, its default must be Fair Value Gap and its help text must explain the currently supported pattern choices.
- Pattern identifiers must use stable, explicit names in JSON, for example `FAIR_VALUE_GAP`, `TRENDLINE_BREAK`, `ORDER_BLOCK`, `CUP_AND_HANDLE`, `DIAMOND`, and `ADAM_AND_EVE` if they are supported by this implementation.
- Strategy names must be deterministic and clear; for example, a single FVG run uses `FAIR_VALUE_GAP_PATTERN_STRATEGY`, and any multi-pattern strategy name must be explicitly defined and tested.
- The implementation must reuse existing detector, risk/exit planner, and exit simulation functions rather than duplicating their logic.
- Unsupported pattern selections must fail before running the backtest and must not partially run with a misleading default.
- README documentation must include at least one concrete safe usage example for the default FVG pattern backtest.
- README documentation should state that this is a historical simulation over stored candles and does not place orders or call exchange order endpoints.

# Assumptions For Future Implementation

- The first implementation may keep only `FAIR_VALUE_GAP` enabled if adapting other pattern event models would require a shared contract redesign; however, it must add a clear selection seam and validation path so future pattern support can be added without another CLI.
- If additional patterns are wired in this task, they must be limited to already-implemented detector and risk/exit planner pairs under `quant_bitcoin/patterns/`.
- One open simulated position at a time remains acceptable unless the implementation explicitly documents and tests a different behavior.
- Exit evaluation should continue to start on the candle after entry unless a future task changes the Task 055 backtest policy.
- JSON stdout remains sufficient for the CLI output.

# Open Questions Before Implementation

Resolve or document these before coding if the answer is not already clear from reviewed files:

- Which additional pattern names can be wired safely without changing shared event/risk/exit contracts?
- Should the CLI support one `--pattern` value per run first, or multiple pattern selections in a single run?
- If multiple patterns are supported in one run, what deterministic priority order should be used for same-candle entries?
- Should unsupported but implemented detector-only patterns be hidden from help choices, or shown as unsupported with a clear error?
- Should README document only the default FVG example first, or include examples for every supported pattern selection?

# Status Tracking

## Before Implementation

- [ ] Read `STATUS.md`.
- [ ] Confirm this task matches the current phase and step.
- [ ] Confirm the current active task is recorded or should be updated.
- [ ] Confirm whether any shared contract change is required; stop and report if a redesign is needed.
- [ ] Confirm parallel work is not needed unless independent leaf tasks are explicitly identified.
- [ ] Record assumptions, blockers, or unclear status items before coding.

## After Implementation

- [ ] Update `STATUS.md` if the phase, step, goal, active task, blocker, open question, or completion state changed.
- [ ] Mark checklist items complete only when acceptance criteria and verification are satisfied.
- [ ] Leave uncertain items open and document the uncertainty.
- [ ] Confirm the next step is accurate or explicitly left undecided.

# Acceptance Criteria

- `python -m quant_bitcoin.backtesting.pattern_postgres_runner_cli --help` shows a description containing `Run the default Fair Value Gap pattern strategy backtest`.
- CLI help text clearly states that the current default is FVG-only.
- The default CLI/backtest output strategy name is `FAIR_VALUE_GAP_PATTERN_STRATEGY`.
- Tests verify the default strategy name in `build_output()` or equivalent CLI output.
- Tests verify parser help/description text for the explicit FVG wording.
- README includes a pattern backtest usage example and safety note.
- A tested pattern selection seam exists, with Fair Value Gap as the default.
- Supported pattern selections are deterministic and backed by existing detector/risk-exit/exit-simulation code.
- Unsupported pattern selections fail with a clear error and do not run a misleading default strategy.
- Existing pattern backtest and pattern CLI tests continue to pass.
- No live trading API calls, Binance order execution calls, signed exchange clients, API-key reads, `.env` requirements, scheduler behavior, dashboard behavior, or new persistence schema behavior are introduced.

# Required Tests

## Unit Tests

- Parser/help includes the default Fair Value Gap strategy wording.
- Parser/help states that current default behavior is FVG-only.
- Default output strategy name is `FAIR_VALUE_GAP_PATTERN_STRATEGY`.
- Default selected pattern remains `FAIR_VALUE_GAP`.
- Pattern selection validation accepts every supported pattern and rejects unsupported pattern names.
- Pattern selection passes the selected pattern into `PatternStrategyBacktestConfig` or the equivalent backtest configuration.
- Caller-provided candle data remains unmutated after running pattern backtests.

## Integration Tests

- CLI-level fake-provider test verifies default FVG selection and JSON output without a live database.
- If additional patterns are wired, each supported pattern has at least one synthetic-candle test proving a deterministic entry path or deterministic no-trade path if synthetic entry construction is not practical.
- README example command remains consistent with registered CLI options.

## Contract Tests

- Verify the CLI and backtest path reuse existing detector, risk/exit planner, and `simulate_pattern_exit` APIs rather than duplicating incompatible logic.
- Verify selected pattern identifiers in JSON are stable explicit strings.
- Verify candle input still uses the standard candle schema only.
- Verify unsupported patterns are rejected before the backtest runner is called.

## Safety Tests

- Verify no exchange order client dependency is instantiated in the CLI or pattern backtest path.
- Verify no paper trader order placement is invoked.
- Verify no API keys, secrets, `.env` files, live-trading toggles, Binance order endpoints, signed exchange requests, or account endpoints are required by the CLI or tests.
- Verify `--help` does not connect to PostgreSQL, Binance, or any network socket.

# Verification

Default verification for the future implementation:

```bash
pytest
python -m quant_bitcoin.backtesting.pattern_postgres_runner_cli --help
```

Recommended targeted verification after implementation:

```bash
pytest tests/backtesting/test_pattern_strategy_backtest.py tests/backtesting/test_pattern_postgres_runner_cli.py -q
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

- Scope expansion beyond historical pattern strategy backtesting.
- Requirement mismatch for exact CLI wording and strategy JSON naming.
- Missing parser/help or JSON-output tests.
- Pattern selection that silently falls back to FVG after an unsupported selection.
- Duplicated detector, risk/exit planner, or exit simulation logic.
- Shared contract redesign hidden inside a CLI clarity task.
- Data contract violations.
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
