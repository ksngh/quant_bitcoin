# Task 018: Docker WebSocket Ingestion Service

# Goal

Add local Docker support for running the market-data-only Binance WebSocket ingestion service with PostgreSQL.

# Source Requirement

User request on 2026-05-13:

- Add local Docker support for running the market-data-only WebSocket ingestion service with PostgreSQL.
- Add Dockerfile.
- Extend `docker-compose.yml` with db and websocket-ingestor service.
- Add a small CLI entrypoint for readiness and bounded ingestion.
- Do not add live trading or order execution.
- Do not require real network access in ordinary tests.

# Extracted Roles

- Owner role: Market Data Operations
- Supporting roles: Market Data Provider, Persistence, Test Designer, Local Development Tooling
- Forbidden roles: Strategy, Backtest Engine, Execution, Risk Management, Live Trading, Binance order client

# Context

Task 017 added deterministic readiness checks for Binance public WebSocket candle ingestion. Task 015 added market-data-only WebSocket ingestion into persistence. This task adds local Docker and CLI wiring only so a developer can run the readiness check or a bounded ingestion service against local PostgreSQL.

# Scope

- Add a repository Dockerfile for the Python package.
- Extend `docker-compose.yml` to include an application service for WebSocket ingestion alongside PostgreSQL.
- Preserve the existing PostgreSQL service and schema initialization.
- Add a small Python CLI entrypoint for:
  - readiness checks without network or database access
  - bounded WebSocket ingestion into PostgreSQL
- Add tests for CLI readiness and bounded ingestion wiring with mocked persistence and ingestion behavior.
- Update `STATUS.md` for the active task and completion state.

# Out of Scope

- Live trading.
- Real Binance order execution.
- Exchange account APIs.
- API keys, signed requests, or `.env` files.
- Unbounded scheduler behavior.
- Strategy, signal, quantity, portfolio, futures, leverage, or risk-management behavior.
- Dashboard, FastAPI, or Streamlit.
- Database migrations beyond existing local schema initialization.
- Ordinary tests that require real Binance, Docker, or PostgreSQL availability.

# Requirements

- Read `AGENTS.md`, `STATUS.md`, `docs/10_CODEX_COMMAND_GUIDE.md`, this task file, and `reviews/CODEX_SELF_REVIEW.md` before coding.
- Keep changes limited to this task.
- Docker support must remain local development support only.
- The CLI readiness command must not perform external network I/O or database access.
- The CLI ingestion command must support a bounded `--max-messages` option.
- The Docker Compose application service must use local PostgreSQL and default to bounded ingestion.
- Ordinary tests must mock external network behavior and must not require real Docker or PostgreSQL.
- Do not add live trading flags or order execution behavior.

# Status Tracking

## Before Implementation

- [x] Read `AGENTS.md`.
- [x] Read `STATUS.md`.
- [x] Read `docs/10_CODEX_COMMAND_GUIDE.md`.
- [x] Read `reviews/CODEX_SELF_REVIEW.md`.
- [x] Read this task file.
- [x] Confirm the task is market-data operations/local Docker support only.
- [x] Confirm no live trading or order execution is requested.

## After Implementation

- [x] Update `STATUS.md` if active task, current step, next step, or completion state changes.
- [x] Mark checklist items complete only after acceptance criteria and verification pass.
- [x] Leave uncertain items open and document the uncertainty.

# Acceptance Criteria

- A `Dockerfile` exists for the Python package.
- `docker-compose.yml` includes PostgreSQL and a `websocket-ingestor` service.
- The `websocket-ingestor` service uses the local Compose PostgreSQL database URL.
- The `websocket-ingestor` service defaults to bounded ingestion rather than live order execution or strategy behavior.
- A CLI entrypoint exists for readiness checks.
- A CLI entrypoint exists for bounded ingestion using PostgreSQL persistence.
- CLI tests cover readiness and bounded ingestion wiring without real network, Docker, or PostgreSQL.
- Verification passes with `pytest`, `git diff --check`, and `python -m compileall quant_bitcoin`.

# Required Tests

## Unit Tests

- CLI readiness returns success for valid default readiness.
- CLI readiness returns non-zero for invalid readiness configuration.
- CLI bounded ingestion wires repository initialization and ingestor run with mocked dependencies.

## Integration Tests

- None required for ordinary tests.

## Contract Tests

- Docker Compose YAML includes PostgreSQL and WebSocket ingestor service definitions with the expected local database URL.

## Safety Tests

- Tests must not call real network endpoints.
- Tests must not require real Docker or PostgreSQL.
- No live-trading flags, API keys, signed requests, or order execution behavior.

# Review Checklist

- Scope respected.
- Requirement matched.
- Role ownership respected.
- Architecture boundaries respected.
- Docker remains local development support only.
- CLI remains market-data-only.
- No hardcoded secrets beyond local development database defaults already used by Compose.
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
