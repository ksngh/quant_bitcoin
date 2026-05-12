# Task 017: WebSocket Ingestion Readiness Clarification

# Goal

Clarify Task 015 Binance WebSocket Candle Ingestion before implementation so startup catch-up behavior, dependency/runtime choices, allowed files, tests, and safety boundaries are explicit.

# Source Requirement

User request on 2026-05-12:

- Before approving Task 015 implementation, refine the WebSocket ingestion task so startup catch-up behavior, dependency/runtime choices, allowed files, tests, and safety boundaries are explicit.
- Create a new task document under `tasks/`.
- Update `STATUS.md` only if project state changes.
- Do not modify application code.
- Do not start Task 015 implementation.

# Extracted Roles

- Owner role: Architect / Task Designer
- Supporting roles: Market Data Provider, Persistence, Configuration, Test Designer
- Forbidden roles: Strategy, Backtest Engine, Execution, Live Trading, Binance order client implementation

# Context

Task 014 is accepted for the current cloud workflow based on completed non-Docker verification. Docker Compose PostgreSQL startup is intentionally skipped in this cloud environment and remains optional local developer verification.

Task 015 exists as the next candidate implementation task, but it should not begin until its startup catch-up behavior, WebSocket dependency/runtime approach, allowed files, test expectations, and safety boundaries are clarified. Task 015 must remain market-data-only and must not trigger strategy execution, paper trades, or live orders.

# Scope

- Review `tasks/015_BINANCE_WEBSOCKET_INGESTION.md`.
- Update `tasks/015_BINANCE_WEBSOCKET_INGESTION.md` to clarify readiness items before implementation.
- Update `STATUS.md` if active task, next step, blocker, or approval state changes.
- Preserve Task 013 and Task 014 persistence schema decisions.
- Preserve duplicate-safe candle uniqueness: `source + symbol + interval + open_time`.
- Fix clear documentation defects in Task 015, including the `der execution` typo if still present.

# Out of Scope

- Task 015 implementation.
- Application code changes.
- Live trading.
- Real Binance order execution.
- Signed requests.
- API keys or secrets.
- `.env` files.
- Strategy behavior.
- Backtest behavior.
- Paper trading behavior.
- Risk behavior.
- Dashboard.
- Scheduler.
- FastAPI.
- Streamlit.
- Futures.
- Leverage.
- Portfolio optimization.
- Machine learning.

# Required Clarifications For Task 015

Task 015 must clearly state the following before implementation begins:

- Startup catch-up behavior for WebSocket ingestion:
  - whether startup requires running Task 014 backfill first, or
  - whether WebSocket ingestion may run a bounded historical gap fill before opening the stream.
- Allowed WebSocket dependency and runtime approach, including whether an async dependency may be added and where it should be declared.
- Allowed files or modules for Task 015 implementation and tests.
- The persistence contract remains the accepted Task 013/014 candle schema.
- Duplicate-safe writes use `source + symbol + interval + open_time`.
- Ordinary tests must mock network and WebSocket behavior.
- Ordinary tests must not require real Binance availability.
- Safety checks must guard against API keys, signed requests, live-trading flags, and Binance order endpoints.
- Task 015 implementation must not begin during Task 017.

# Acceptance Criteria

- [ ] `tasks/015_BINANCE_WEBSOCKET_INGESTION.md` clarifies startup catch-up behavior before implementation.
- [ ] `tasks/015_BINANCE_WEBSOCKET_INGESTION.md` clarifies any WebSocket dependency/runtime approach before implementation.
- [ ] `tasks/015_BINANCE_WEBSOCKET_INGESTION.md` lists allowed implementation and test file areas for Task 015.
- [ ] `tasks/015_BINANCE_WEBSOCKET_INGESTION.md` requires preserving the Task 013/014 persistence schema and duplicate-safe candle uniqueness rule.
- [ ] `tasks/015_BINANCE_WEBSOCKET_INGESTION.md` requires ordinary tests to mock network/WebSocket behavior and avoid real Binance availability.
- [ ] `tasks/015_BINANCE_WEBSOCKET_INGESTION.md` requires safety checks against API keys, signed requests, live-trading flags, and Binance order endpoints.
- [ ] `tasks/015_BINANCE_WEBSOCKET_INGESTION.md` explicitly says Task 015 implementation must not begin during Task 017.
- [ ] No application code is changed.
- [ ] `STATUS.md` is updated if project state changes.

# Verification

```bash
git diff --check
```

# Codex Self-Review Requirement

Before completion, run through `reviews/CODEX_SELF_REVIEW.md` and include the result in the final summary.

# Completion Summary Required

- files changed
- documentation summary
- checks run
- Codex self-review result
- known limitations
- recommended next task
- recommended next prompt
