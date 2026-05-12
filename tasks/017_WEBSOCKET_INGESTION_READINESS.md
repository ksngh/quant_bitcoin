# Task 017: WebSocket Ingestion Readiness

# Goal

Add a small market-data-only readiness check for Binance WebSocket candle ingestion so operators and tests can validate startup configuration before opening a public WebSocket connection.

# Source Requirement

User request on 2026-05-12:

- Implement the next explicitly approved market-data readiness or operations task.
- Do not add live trading or order execution.
- Mock external network behavior in ordinary tests.
- Create the missing `tasks/017_WEBSOCKET_INGESTION_READINESS.md` task document, then implement it.

# Extracted Roles

- Owner role: Market Data Operations
- Supporting roles: Market Data Provider, Persistence, Test Designer
- Forbidden roles: Strategy, Backtest Engine, Execution, Risk Management, Live Trading, Binance order client

# Context

Task 015 implemented public Binance WebSocket kline ingestion for closed candle persistence. This task adds preflight readiness validation only. It must not open network connections, connect to PostgreSQL, place orders, calculate signals, decide quantity, or perform historical backfill.

# Scope

- Add a readiness helper for Binance WebSocket candle ingestion configuration.
- Validate symbol, interval, WebSocket stream URL, reconnect delay, and reconnect limit.
- Report a reminder that historical startup catch-up remains a Task 014 backfill responsibility.
- Keep the helper deterministic and unit-testable without external network or database access.
- Export the readiness helper and result types from the market data package.
- Add tests for valid readiness, invalid configuration reporting, and order-endpoint safety.
- Update `STATUS.md` for the active task and completion state.

# Out of Scope

- Live trading.
- Real Binance order execution.
- Exchange account APIs.
- API keys, signed requests, or `.env` files.
- Opening real WebSocket connections in tests.
- Connecting to PostgreSQL in tests.
- Historical backfill execution.
- Scheduler, dashboard, FastAPI, Streamlit, Docker changes, or database migrations.
- Strategy, signal, quantity, portfolio, futures, leverage, or risk-management behavior.

# Requirements

- Read `AGENTS.md`, `STATUS.md`, `docs/10_CODEX_COMMAND_GUIDE.md`, this task file, and `reviews/CODEX_SELF_REVIEW.md` before coding.
- Read relevant existing WebSocket ingestion and persistence code before changing code.
- Keep changes limited to this task.
- The readiness helper must not perform external network I/O.
- The readiness helper must not instantiate an exchange order client or call exchange order endpoints.
- The readiness helper must return structured check results instead of requiring callers to parse exception text for normal invalid configuration.
- Invalid configuration must be represented as a not-ready report.
- A configured order endpoint or signed request data must be represented as a failed readiness check.
- Ordinary tests must mock or avoid external network behavior.

# Status Tracking

## Before Implementation

- [x] Read `AGENTS.md`.
- [x] Read `STATUS.md`.
- [x] Read `docs/10_CODEX_COMMAND_GUIDE.md`.
- [x] Read `reviews/CODEX_SELF_REVIEW.md`.
- [x] Read this task file.
- [x] Confirm the task is market-data readiness/operations only.
- [x] Confirm no live trading or order execution is requested.

## After Implementation

- [x] Update `STATUS.md` if active task, current step, next step, or completion state changes.
- [x] Mark checklist items complete only after acceptance criteria and verification pass.
- [x] Leave uncertain items open and document the uncertainty.

# Acceptance Criteria

- A public API exists to check Binance WebSocket ingestion readiness without opening a network connection.
- The readiness report includes normalized symbol, interval, candidate stream URL when safe to build, per-check pass/fail results, and an overall ready flag.
- Valid default `BTCUSDT` `1m` configuration returns ready.
- Unsupported intervals, blank symbols, negative reconnect delays, and negative reconnect limits return not-ready reports.
- Order endpoint or signed-request configuration returns a not-ready report and does not perform network I/O.
- The helper documents or reports that startup historical gap catch-up must be handled by Task 014 backfill when completeness is required.
- Tests cover readiness success, invalid configuration aggregation, and order-endpoint safety.
- Verification passes with `pytest`, `git diff --check`, and `python -m compileall quant_bitcoin`.

# Required Tests

## Unit Tests

- Readiness success for default public WebSocket configuration.
- Readiness failure for invalid symbol, interval, reconnect delay, and reconnect limit.
- Readiness failure for order endpoint or signed request configuration.

## Integration Tests

- None required.

## Contract Tests

- Readiness helper uses existing WebSocket URL construction and interval validation semantics.

## Safety Tests

- Tests must not call real network endpoints.
- Tests must verify readiness does not allow order endpoint or signed request configuration.

# Review Checklist

- Scope respected.
- Requirement matched.
- Role ownership respected.
- Architecture boundaries respected.
- Market-data readiness stays separate from strategy, backtesting, execution, and risk.
- No hardcoded secrets.
- No `.env` files.
- No real order execution.
- No exchange order endpoint calls.
- No unnecessary abstractions.

# Verification

```bash
pytest
git diff --check
python -m compileall quant_bitcoin
```
