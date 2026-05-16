# Task 025: WebSocket Unbounded Ingestion Service

# Goal

- WebSocket ingestor CLI/Docker service must not stop after five messages by default.
- Clearly separate bounded smoke-test mode from unbounded long-running mode.

# Clean Requirement

Update the market-data-only WebSocket ingestion CLI and Docker Compose service so local service startup defaults to long-running/unbounded ingestion, while retaining an explicit bounded mode for tests and smoke checks.

# Scope

Allowed files/modules:

- `quant_bitcoin/market_data/websocket_ingestion_cli.py`
- `quant_bitcoin/market_data/binance_websocket.py` only if needed for wording or small support changes
- `docker-compose.yml`
- relevant tests under `tests/market_data/`
- `README.md` and `STATUS.md` for documentation/status updates

Do not add:

- strategy execution
- paper trading
- live trading
- real Binance order execution
- exchange account API calls
- signed requests
- API-key handling
- scheduler
- dashboard
- FastAPI
- Streamlit

# Requirements

- Add `--no-max-messages` or equivalent CLI option so ingestion can pass `max_messages=None` to the ingestor.
- Define how `INGEST_MAX_MESSAGES` unset, empty, and unbounded values behave.
- Docker Compose `websocket-ingestor` defaults must be long-running/unbounded rather than five-message bounded mode.
- Keep bounded smoke-test mode available with `--max-messages <positive integer>` or equivalent.
- Add/update tests for bounded and unbounded modes.
- WebSocket ingestion must remain market-data-only.
- No strategy execution, paper trading, live trading, Binance order endpoint, signed request, or API-key behavior may be added.

# Acceptance Criteria

- CLI default ingestion mode is unbounded when no max-message limit is provided.
- `INGEST_MAX_MESSAGES` unset, empty, `none`, `unbounded`, and `0` are documented/tested as unbounded values, or another explicit policy is implemented and documented.
- Positive integer `INGEST_MAX_MESSAGES` and `--max-messages` still provide bounded smoke-test mode.
- `--no-max-messages` overrides any configured max-message limit.
- Docker Compose no longer defaults to `INGEST_MAX_MESSAGES=5` for the `websocket-ingestor` service.
- Ordinary tests do not require real PostgreSQL, Docker, Binance, or external network.
- Safety boundaries are preserved.

# Required Verification

```bash
pytest
git diff --check
python -m compileall quant_bitcoin
```

# Codex Self-Review Requirement

Before completion, run through `reviews/CODEX_SELF_REVIEW.md` and include the result in the final summary.
