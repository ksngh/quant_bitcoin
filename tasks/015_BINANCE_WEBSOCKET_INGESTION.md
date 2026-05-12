# Task 015: Binance WebSocket Candle Ingestion

# Goal

Implement continuous Binance public WebSocket candle ingestion after PostgreSQL candle persistence and historical backfill are accepted for the current workflow.

# Source Requirement

User request on 2026-05-09:

- Write a document for implementing functionality that continuously receives data through WebSocket.

Task 017 readiness clarification on 2026-05-12 refined this task before implementation.

# Extracted Roles

- Owner role: Market Data Provider
- Supporting roles: Persistence, Configuration, Test Designer, Architect
- Forbidden roles: Strategy, Backtest Engine, Execution, Live Trading, Binance order client implementation

# Context

Historical backfill and continuous ingestion are separate responsibilities. Task 014 is accepted for the current cloud workflow based on non-Docker verification, and Docker Compose PostgreSQL startup remains optional local developer verification. WebSocket ingestion must remain market-data-only and must not trigger strategy execution, paper trades, or live orders.

Task 015 implementation must not begin until the project owner explicitly approves this task for implementation after Task 017 readiness clarification is complete.

# Startup Catch-Up Decision

Task 015 must not implement an automatic historical gap-fill loop.

Startup catch-up behavior for the first implementation is:

- Operators must run or have already run Task 014 historical backfill for the target stream before starting WebSocket ingestion when historical completeness is required.
- WebSocket ingestion may read the latest stored candle/checkpoint to record status or avoid duplicate writes, but it must not fetch historical REST pages itself in Task 015.
- If a gap is detected between the latest stored candle and the current WebSocket stream, Task 015 may log or expose that status through checkpoint metadata, but automated bounded gap fill is a future task.
- Closed WebSocket candles are persisted with duplicate-safe writes, so overlapping candles after restart must not create duplicate rows.

# Dependency And Runtime Approach

Task 015 may add the `websockets` Python package to `pyproject.toml` if needed for a real Binance public WebSocket client.

Implementation should keep the runtime small and testable:

- Prefer `asyncio` plus an injectable async message source/client boundary.
- Keep message parsing and candle mapping in pure functions where practical.
- Tests must use mocked async message sources and must not open real network connections.
- No scheduler, daemon supervisor, FastAPI app, Streamlit app, dashboard, Docker change, or production process manager may be introduced by Task 015.

# Allowed Implementation Files For Task 015

Task 015 implementation should be limited to these areas unless a concrete issue requires a narrowly justified status/task update:

- `quant_bitcoin/market_data/binance_websocket.py`
- `quant_bitcoin/market_data/__init__.py`
- `quant_bitcoin/persistence/` only if a small checkpoint-mode constant or repository method is required for WebSocket ingestion status
- `tests/market_data/test_binance_websocket.py`
- `tests/persistence/test_postgres_persistence.py` only if persistence checkpoint behavior changes
- `pyproject.toml` only for an approved WebSocket dependency
- `README.md` only for usage or safety documentation directly related to Task 015
- `STATUS.md`
- `tasks/015_BINANCE_WEBSOCKET_INGESTION.md`

# Scope

- Connect to Binance public WebSocket market-data streams.
- Subscribe to the configured symbol and interval kline stream.
- Detect closed 1-minute candles.
- Persist closed candles using the accepted PostgreSQL candle schema.
- Use duplicate-safe writes based on the accepted uniqueness rule: `source + symbol + interval + open_time`.
- Reconnect after transient failures using behavior defined in code and covered by mocked tests.
- Record or expose basic ingestion checkpoint/status metadata if it can be done within the accepted Task 013/014 persistence contract.
- Keep WebSocket ingestion separate from strategy, backtest, risk, and execution modules.

# Out of Scope

- Historical backfill or automated bounded REST gap fill.
- Live trading.
- Real Binance order endpoints.
- Signed requests.
- API keys or secrets.
- `.env` files.
- Strategy signal generation.
- Backtest execution.
- Paper-trading orchestration.
- Risk behavior changes.
- Dashboard or alerting UI.
- Full production scheduler or process supervisor.
- Docker changes.
- FastAPI.
- Streamlit.
- Futures, leverage, or portfolio optimization.
- Machine learning.

# Requirements

- WebSocket ingestion must use Binance public market-data streams only.
- The first target symbol is `BTCUSDT`.
- The first target interval is `1m`.
- Only closed candles may be persisted as finalized candle rows.
- Open/in-progress kline messages must be ignored or tracked only as non-final status; they must not be written as finalized `candles` rows.
- Persisted candles must follow the accepted Task 013/014 candle schema.
- Duplicate-safe writes must use the accepted candle uniqueness rule: `source + symbol + interval + open_time`.
- Reconnection behavior must be defined and tested with mocks.
- Startup catch-up must require Task 014 backfill when historical completeness is needed; Task 015 must not implement historical REST gap fill.
- Ordinary tests must mock network and WebSocket behavior.
- Ordinary tests must not require real Binance WebSocket availability.
- Safety checks must verify no API keys, signed requests, live-trading flags, or Binance order endpoints are introduced.
- The implementation must not call order endpoints or require API keys.

# Status Tracking

## Before Implementation

- [ ] Read `AGENTS.md`.
- [ ] Read `STATUS.md`.
- [ ] Read `docs/10_CODEX_COMMAND_GUIDE.md`.
- [ ] Read `tasks/013_PERSISTENCE_SCHEMA_DESIGN.md`.
- [ ] Read `tasks/014_POSTGRES_BINANCE_BACKFILL.md`.
- [ ] Read `tasks/017_WEBSOCKET_INGESTION_READINESS.md`.
- [ ] Confirm Task 017 readiness clarification is complete.
- [ ] Confirm persistence schema and historical backfill are accepted for the current workflow.
- [ ] Confirm explicit human approval to implement WebSocket ingestion.
- [ ] Confirm no live-trading approval is implied by this task.

## After Implementation

- [ ] Update `STATUS.md` if active task, next step, or blocker changes.
- [ ] Mark checklist items complete only after acceptance criteria and verification pass.
- [ ] Leave uncertain items open and document the uncertainty.

# Acceptance Criteria

- WebSocket client receives mocked Binance kline messages.
- Closed 1-minute candle messages are mapped to the Task 013/014 candle schema and persisted.
- Open/in-progress kline messages are not persisted as finalized candle rows.
- Duplicate closed-candle messages do not create duplicate rows because writes use `source + symbol + interval + open_time`.
- Reconnect behavior is tested with mocked failures.
- Startup catch-up behavior requires Task 014 backfill when historical completeness is needed and does not implement historical REST gap fill.
- Ordinary tests do not require real Binance WebSocket availability.
- Safety tests or static checks verify no API keys, signed requests, live-trading flags, or Binance order endpoints are introduced.
- No live-trading, signed request, API-key handling, or order execution behavior is added.

# Required Tests

## Unit Tests

- WebSocket kline message parsing.
- Closed-candle detection.
- Mapping closed kline messages to the accepted persisted candle schema.
- Duplicate-safe persistence call behavior.
- Reconnect policy behavior with mocked failures.
- Startup catch-up decision behavior: Task 014 backfill is required or status is exposed; no REST gap-fill calls are made by WebSocket ingestion.

## Integration Tests

- Optional local persistence integration test if PostgreSQL test support exists.
- No ordinary test should require a real PostgreSQL server by default.
- No ordinary test should require the real Binance WebSocket service by default.

## Contract Tests

- Persisted WebSocket candles match the accepted candle schema from Task 013/014.
- Duplicate identity remains `source + symbol + interval + open_time`.

## Safety Tests

- Verify no Binance order endpoint is called.
- Verify no API keys, secrets, `.env` files, signed requests, or live-trading flags are introduced.
- Verify strategy, backtest, risk, and execution modules are not required by WebSocket ingestion.

# Review Checklist

- Scope respected.
- Requirement matched.
- Role ownership respected.
- Architecture boundaries respected.
- Data contract respected.
- Task 013/014 persistence schema preserved.
- Duplicate-safe uniqueness rule preserved.
- WebSocket ingestion remains market-data-only.
- No hardcoded secrets.
- No real order execution.
- No strategy, backtest, risk, or execution behavior changes.
- No historical REST gap fill added in Task 015.
- No scheduler, dashboard, FastAPI, Streamlit, Docker, futures, leverage, portfolio optimization, or machine learning added.

# Verification

Default:

```bash
pytest
```

Additional verification:

```bash
git diff --check
python -m compileall quant_bitcoin
rg -n "apiKey|APIKEY|signature|ENABLE_LIVE_TRADING|/order|SECRET|PRIVATE" quant_bitcoin tests README.md pyproject.toml
```

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
- recommended next prompt
