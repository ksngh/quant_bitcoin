# Task 055: Pattern Strategy Backtest

# Goal

Define and implement a backtestable strategy workflow that turns historical minute candles into pattern-based entry signals and exits those simulated positions using configured stop-loss and take-profit rules.

The first implementation should connect existing completed pieces only: candle data, indicator calculation, pattern detection, pattern risk/exit planning, and deterministic exit simulation. It must remain a pure backtesting feature and must not introduce live trading or real exchange order execution.

# Source Requirement

Owner request, translated and cleaned:

1. Load all minute candles for the target backtest period.
2. During backtesting, calculate required indicators for those candles.
3. Use the calculated indicators to detect/create each pattern and buy at the appropriate timing.
4. Sell in the simulation according to the configured stop-loss line or take-profit line.

# Clean Requirement

Create a pattern strategy backtest integration that evaluates completed minute candles in timestamp order, detects configured technical patterns from indicator-enriched candle history, opens simulated long or short positions from valid pattern plans, and closes those simulated positions through the existing deterministic exit simulator when stop-loss, take-profit, invalidation, time-stop, break-even, or trailing-stop rules are triggered.

# Dependencies

This task depends on the completed and verified behavior from:

- Task 019 PostgreSQL Candle Data Provider for Backtesting, if database-backed candles are used.
- Task 020 PostgreSQL Backtest Runner, if the existing runner is the selected integration point.
- Tasks 027-033 implemented indicator modules, where relevant to the selected patterns.
- Tasks 040-045 pattern detection engines.
- Task 047 Pattern Risk / Exit Plan Contract.
- Tasks 048-053 pattern-specific risk/exit planners.
- Task 054 Pattern Exit Simulation Integration.

# Extracted Roles

- Owner role: Pattern strategy backtest orchestration.
- Supporting roles:
  - Candle data provider supplies standard completed candles.
  - Indicator modules calculate reusable indicator values.
  - Pattern detectors emit deterministic pattern events.
  - Pattern risk/exit planners convert pattern events into entry, stop-loss, and take-profit plans.
  - Pattern exit simulator closes simulated positions deterministically.
  - Existing backtest runner or a new pure helper coordinates the simulation.
- Forbidden roles:
  - Live trading.
  - Real Binance order execution.
  - Exchange order API calls.
  - Paper order placement unless explicitly assigned by a later task.
  - Strategy code fetching market data.
  - Strategy code reading API keys or environment secrets.
  - Dashboard, scheduler, FastAPI, Streamlit, Docker, ML, futures, leverage, or portfolio optimization.

# Responsibility Boundary

This task is responsible for wiring already-defined pure components into a historical backtest workflow for pattern entries and planned exits.

This task must not redesign public candle, signal, pattern event, risk/exit plan, exit simulation, or backtest result contracts. If the implementation requires a shared contract change, stop and ask the owner to approve a separate contract task first.

# Relevant Context To Read Before Implementation

- `AGENTS.md`
- `STATUS.md`
- `docs/03_ARCHITECTURE_RULES.md`
- `docs/04_DATA_CONTRACT.md`
- `docs/05_TEST_STRATEGY.md`
- `docs/10_CODEX_COMMAND_GUIDE.md`
- `reviews/CODEX_SELF_REVIEW.md`
- `tasks/020_POSTGRES_BACKTEST_RUNNER.md`
- `tasks/040_PATTERN_DETECTION_ENGINE.md`
- `tasks/047_PATTERN_RISK_EXIT_PLAN_CONTRACT.md`
- `tasks/048_TRENDLINE_BREAK_RISK_EXIT_PLAN.md`
- `tasks/049_ORDER_BLOCK_RISK_EXIT_PLAN.md`
- `tasks/050_FAIR_VALUE_GAP_RISK_EXIT_PLAN.md`
- `tasks/051_CUP_AND_HANDLE_RISK_EXIT_PLAN.md`
- `tasks/052_DIAMOND_RISK_EXIT_PLAN.md`
- `tasks/053_ADAM_AND_EVE_RISK_EXIT_PLAN.md`
- `tasks/054_PATTERN_EXIT_SIMULATION_INTEGRATION.md`
- Existing indicator and pattern modules under `quant_bitcoin/`.
- Existing backtest tests under `tests/`.

# Scope

- Add or update a pure backtesting integration for pattern-based strategies.
- Support historical completed minute candles using the existing standard candle schema.
- Calculate only the indicators required by the selected pattern detectors/planners.
- Detect configured patterns over candle history without duplicate entries for the same pattern event.
- Create simulated entries only from valid pattern risk/exit plans that satisfy the planner filters.
- Close simulated positions with the Task 054 exit simulator.
- Return or record backtest results that include pattern identity, entry timing, entry price, exit timing, exit price, exit reason, and realized simulated outcome.
- Add deterministic tests with in-memory synthetic candles and/or local fixtures.
- Update `STATUS.md` if the project phase, step, goal, active task, open questions, blockers, or completion state changes.

# Out of Scope

- Live trading.
- Real Binance order execution.
- Exchange order endpoints.
- Paper trader integration.
- Real-time WebSocket strategy execution.
- New pattern algorithms.
- New risk/exit planning rules beyond using existing planners.
- Database schema changes unless explicitly approved in a separate task.
- Dashboard, scheduler, FastAPI, Streamlit, Docker, machine learning, futures, leverage, portfolio optimization.
- Fetching candles from Binance during deterministic tests.
- Reading API keys, `.env` files, or credentials.

# Requirements

- Evaluate completed candles in ascending `timestamp` order.
- Require the standard candle schema: `timestamp`, `open`, `high`, `low`, `close`, `volume`.
- Do not mutate caller-provided candle data.
- Indicator calculation must happen before the pattern detector or planner that needs those values.
- Pattern detection must use completed candles only; do not look ahead beyond the candle currently available to the backtest step.
- Each pattern event must be entered at most once per backtest run unless a future task explicitly defines re-entry behavior.
- Entry timing must be deterministic and documented in code/tests; if an event is confirmed on candle N, execution should not assume information from candles after N.
- Exit handling must delegate stop-loss, take-profit, invalidation, time-stop, break-even, trailing-stop, and partial-exit behavior to the existing exit simulator rather than duplicating its logic.
- When multiple patterns are configured, the first implementation must define deterministic ordering or reject ambiguous same-candle entries with a clear reason.
- The implementation must expose enough result metadata for later graph/reporting work without requiring a dashboard.
- No exchange clients, order endpoint URLs, API-key reads, or real order objects may be introduced.

# Open Questions Before Implementation

Resolve or document these before coding if the answer is not already clear from reviewed files:

- Which pattern or set of patterns should be included in the first implementation batch?
- Should the first batch allow only one open simulated position at a time, or multiple independent pattern positions?
- Should same-candle entry and exit be allowed, or should exit evaluation begin on the candle after entry?
- Should long and short entries both be enabled by default, or should the first batch be long-only?
- Which existing backtest result model should be reused, and is it sufficient for pattern metadata without a contract change?
- Should data come from PostgreSQL, CSV/local fixtures, or an in-memory DataFrame in the first implementation?

# Status Tracking

## Before Implementation

- [ ] Read `STATUS.md`.
- [ ] Confirm this task matches the current phase and step.
- [ ] Confirm the current active task is recorded or should be updated.
- [ ] Confirm no shared contract changes are required.
- [ ] Confirm parallel work is not needed unless independent leaf tasks are explicitly identified.
- [ ] Record assumptions, blockers, or unclear status items before coding.

## After Implementation

- [ ] Update `STATUS.md` if the phase, step, goal, active task, blocker, open question, or completion state changed.
- [ ] Mark checklist items complete only when acceptance criteria and verification are satisfied.
- [ ] Leave uncertain items open and document the uncertainty.
- [ ] Confirm the next step is accurate or explicitly left undecided.

# Acceptance Criteria

- A pattern strategy backtest workflow exists and is callable from tests without external services.
- The workflow accepts standard completed minute candles and processes them in deterministic timestamp order.
- Required indicators are calculated before their consuming pattern logic.
- At least one configured pattern can produce a simulated entry from synthetic historical candles.
- Simulated exits use the existing pattern exit simulator and cover stop-loss and take-profit outcomes.
- Duplicate entries for the same pattern event are prevented.
- Result records include pattern metadata, entry metadata, exit metadata, exit reason, and simulated PnL or R-multiple where supported by the existing contracts.
- Tests prove no exchange clients, live order execution, API keys, or `.env` dependencies are introduced.
- Existing test suite continues to pass.

# Required Tests

## Unit Tests

- No trade is opened when no configured pattern is detected.
- A valid configured pattern opens exactly one simulated position.
- Duplicate detections of the same stable pattern event do not create duplicate entries.
- A stop-loss exit is recorded through the exit simulator.
- A take-profit exit is recorded through the exit simulator.
- Indicator warmup/insufficient history produces deterministic no-trade behavior.
- Caller-provided candle data is not mutated.
- Same-candle multiple-pattern behavior follows the documented deterministic rule.

## Integration Tests

- Run the pattern strategy backtest over synthetic minute candles from an in-memory DataFrame or local fixture.
- If the existing PostgreSQL backtest runner is integrated, test with mocks/fakes and do not require a live database for default verification.

## Contract Tests

- Verify the workflow requires and uses only the standard candle schema.
- Verify returned results expose pattern, entry, exit, and outcome metadata without depending on Binance-specific raw fields.
- Verify the implementation reuses existing pattern event, risk/exit plan, and exit simulation contracts rather than redefining incompatible duplicates.

## Safety Tests

- Verify no real exchange order endpoints are called.
- Verify no exchange order client dependency is introduced in the strategy/backtest path.
- Verify no API keys, `.env` files, or live-trading toggles are required.
- Verify paper trader placement is not invoked.

# Verification

Default verification for the future implementation:

```bash
pytest
```

Recommended targeted verification after implementation:

```bash
pytest tests/patterns
pytest tests/backtest*
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
- Missing deterministic tests for entries and exits.
- Duplicate exit simulation logic instead of reusing Task 054 behavior.
- Shared contract changes hidden inside an integration task.
- Architecture boundary violations between data provider, strategy, backtest, and execution roles.
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
