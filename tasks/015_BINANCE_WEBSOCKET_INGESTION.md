# Task 015: Binance WebSocket Candle Ingestion

# Goal

Implement continuous Binance WebSocket candle ingestion after PostgreSQL candle persistence and historical backfill are accepted.

# Source Requirement

User request on 2026-05-09:

- Write a document for implementing functionality that continuously receives data through WebSocket.

# Extracted Roles

- Owner role: Market Data Provider
- Supporting roles: Persistence, Configuration, Test Designer, Architect
- Forbidden roles: Strategy, Backtest Engine, Execution, Live Trading, Binance order client implementation

# Context

Historical backfill and continuous ingestion are separate responsibilities. This task should run only after the persistence schema is accepted and the historical PostgreSQL backfill path exists. WebSocket ingestion must remain market-data-only and must not trigger strategy execution, paper trades, or live orders.

# Scope

- Connect to Binance public WebSocket market-data streams.
- Subscribe to the configured symbol and interval kline stream.
- Detect closed 1-minute candles.
- Persist closed candles using the accepted PostgreSQL candle schema.
- Reconnect after transient failures.
- Avoid duplicate writes.
- Record or expose basic ingestion checkpoint/status metadata if accepted by Task 013.
- Keep WebSocket ingestion separate from strategy, backtest, and execution modules.

# Out of Scope

- Historical backfill.
- Live trading.
- Real Binance order endpoints.
- Signed requests.
- API keys or secrets.
- Strategy signal generation.
- Backtest execution.
- Paper-trading orchestration.
- Dashboard or alerting UI.
- Full production scheduler or process supervisor.
- Futures, leverage, or portfolio optimization.

# Requirements

- WebSocket ingestion must use Binance public market-data streams only.
- The first target symbol is `BTCUSDT`.
- The first target interval is `1m`.
- Only closed candles may be persisted as finalized candle rows.
- Duplicate-safe writes must use the accepted candle uniqueness rule.
- Reconnection behavior must be defined and tested with mocks.
- The implementation must define how startup catches up after downtime, either by requiring Task 014 backfill or by running a bounded historical gap fill before opening the stream.
- The implementation must not call order endpoints or require API keys.

# Status Tracking

## Before Implementation

- [x] Read `AGENTS.md`.
- [x] Read `STATUS.md`.
- [x] Read `tasks/013_PERSISTENCE_SCHEMA_DESIGN.md`.
- [x] Read `tasks/014_POSTGRES_BINANCE_BACKFILL.md`.
- [x] Confirm persistence schema and historical backfill are accepted or implemented.
- [x] Confirm explicit human approval to implement WebSocket ingestion.

## After Implementation

- [x] Update `STATUS.md` if active task, next step, or blocker changes.
- [x] Mark checklist items complete only after acceptance criteria and verification pass.
- [x] Leave uncertain items open and document the uncertainty.

# Acceptance Criteria

- WebSocket client receives mocked Binance kline messages.
- Closed 1-minute candle messages are persisted.
- Open/in-progress kline messages are ignored or stored only as non-final status if explicitly designed.
- Duplicate closed-candle messages do not create duplicate rows.
- Reconnect behavior is tested with mocked failures.
- Startup catch-up behavior is documented.
- No live-trading, signed request, API-key handling, or der execution behavior is added.

# Required Tests

## Unit Test

- WebSocket kline message parsing.
- Closed-candle detection.
- Duplicate-safe persistence call behavior.
- Reconnect policy behavior with mocked failures.

## Integration Tests

- Optional local persistence integration test if PostgreSQL test support exists.
- No test should require the real Binance WebSocket service by default.

## Contract Tests

- Persisted WebSocket candles match the accepted candle schema from Task 013.

## Safety Tests

- Verify no Binance order endpoint is called.
- Verify no API keys, secrets, `.env` files, signed requests, or live-trading flags are introduced.

# Review Checklist

- Scope respected.
- Requirement matched.
- Role ownership respected.
- Architecture boundaries respected.
- Data contract respected.
- WebSocket ingestion remains market-data-only.
- No hardcoded secrets.
- No real order execution.
- No strategy, backtest, or execution behavior changes.

# Verification

Default:

```bash
pytest
```

Additional Task 015 verification run on 2026-05-12:

```bash
pytest
git diff --check
python -m compileall quant_bitcoin
rg -n "apiKey|APIKEY|signature|ENABLE_LIVE_TRADING|/order|SECRET|PRIVATE" quant_bitcoin tests README.md pyproject.toml
```

# Startup Catch-Up Decision

WebSocket ingestion does not run historical REST gap fill on startup. When
historical completeness is required after downtime, run the accepted Task 014
PostgreSQL Binance backfill first, then start the WebSocket ingestor. This keeps
continuous ingestion and historical catch-up as separate market-data
responsibilities.

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
