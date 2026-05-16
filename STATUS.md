# Project Status

# Current Phase

Phase 22: PostgreSQL Backtest Result Persistence

# Current Step

Task 022: PostgreSQL backtest result persistence implemented and verified; Task 023 graph read model not started.

# Current Goal

Persist completed PostgreSQL-backed RSI backtest outputs so later graph workflows can read saved summary, simulated trades, and graph-ready time-series points without re-running the backtest.

# Current Active Task

None. Task 022 implementation is complete pending owner review/merge.

# Last Completed Step

Task 022: PostgreSQL Backtest Result Persistence.

Implemented transactional PostgreSQL persistence for completed simulated backtest runs using the accepted Task 021 schema. `quant-bitcoin-postgres-backtest` now persists strategy configuration, run metadata, summary metrics, deterministic simulated trades, and ordered graph-ready points by default, while continuing to print deterministic JSON that includes the saved `backtest_run_id`. Added a `--no-persist` inspection mode for stdout-only runs. Verified on 2026-05-16 with `pytest`, `git diff --check`, and `python -m compileall quant_bitcoin`. This task did not add graph UI, graph read APIs, FastAPI, Streamlit, schedulers, live trading, signed requests, API-key handling, Binance order endpoints, or exchange account API behavior.

# Next Step

Recommended next task: Task 023 Backtest Result Read Model for Graphs. Implement read-only graph result queries against the Task 021/022 persistence schema, keeping strategies and market-data providers unaware of graph read concerns. Local Docker Compose runtime startup verification for Task 014/018 remains deferred to a Docker-capable developer environment.

# Parallel Work Status

Parallel work is not currently recommended.

Reason:
Task 023 should consume the shared persistence contract introduced by Task 022. Additional shared contract changes should remain sequential and explicitly reviewed.

# Phase Checklist

- [x] Step 1.1: Create Codex workflow documentation
- [x] Python project setup complete and verified
- [x] Market data contract complete and verified
- [x] CSV data provider complete and verified
- [x] Parallel work rules reviewed after foundation completion
- [x] RSI strategy complete and verified
- [x] Basic backtest complete and verified
- [x] Paper trader complete and verified
- [x] Binance candle downloader complete and verified
- [x] Next task document selected or created
- [x] Improved backtesting complete and verified
- [x] Paper trading with state task document selected or created
- [x] Paper trading with state complete and verified
- [x] Later risk management task document selected or created
- [x] First concrete risk-management implementation task defined
- [x] Basic paper risk checks complete and verified
- [x] Later live trading safety-gates task document selected or created
- [x] Live trading safety gates defined
- [x] Live trading implementation blocker documented
- [x] Persistence schema design task document selected or created
- [x] Persistence schema design documented
- [x] Codex command consistency guide documented
- [x] Task 014: PostgreSQL Binance Backfill approved for implementation
- [x] Task 014: PostgreSQL Binance Backfill accepted for current cloud workflow with non-Docker verification
- [ ] Task 014: PostgreSQL Binance Backfill optional local Docker runtime startup verified
- [x] Task 015: Binance WebSocket Candle Ingestion approved for implementation
- [x] Task 015: Binance WebSocket Candle Ingestion complete and verified
- [x] Task 017: WebSocket Ingestion Readiness task document selected or created
- [x] Task 017: WebSocket Ingestion Readiness complete and verified
- [x] Task 018: Docker WebSocket Ingestion Service task document selected or created
- [x] Task 018: Docker WebSocket Ingestion Service complete and verified
- [x] Task 019: PostgreSQL Candle Data Provider for Backtesting task document selected or created
- [x] Task 019: PostgreSQL Candle Data Provider for Backtesting approved for implementation
- [x] Task 019: PostgreSQL Candle Data Provider for Backtesting complete and verified
- [x] Task 020: PostgreSQL Backtest Runner task document selected or created
- [x] Task 020: PostgreSQL Backtest Runner approved for implementation
- [x] Task 020: PostgreSQL Backtest Runner complete and verified
- [x] Task 021: Graph-Ready Backtest Persistence Schema task document created
- [x] Task 022: PostgreSQL Backtest Result Persistence task document created
- [x] Task 023: Backtest Result Read Model for Graphs task document created
- [x] Task 021: Graph-Ready Backtest Persistence Schema accepted
- [x] Task 022: PostgreSQL Backtest Result Persistence complete and verified
- [ ] Task 023: Backtest Result Read Model for Graphs approved for implementation

# Open Questions

- Has the project owner explicitly approved live trading and real order execution?
- What credential policy should be used for API keys and secrets?
- Should future live trading use Binance testnet/sandbox first?
- What real-order endpoints, if any, are allowed?
- What kill-switch or disable mechanism is required?
- Should future PostgreSQL implementation use migrations, container init scripts, or another schema-management path? Current Task 014 uses container init SQL plus repository schema initialization; migrations remain a future decision if schema evolution is needed. Task 022 extended the existing init SQL/repository initialization path for graph-ready backtest result tables.
- Docker is not installed in the current cloud environment. Local PostgreSQL and WebSocket ingestor container startup are intentionally skipped here and remain optional local developer verification.

# Blockers

- Live trading implementation is blocked until explicit human approval, credential policy, sandbox/testnet policy, real-order endpoint allowlist, kill-switch design, and safety tests are documented.

# Rules for Next Codex Task

- Read `AGENTS.md` before working.
- Read this `STATUS.md` before starting implementation tasks.
- Use `docs/10_CODEX_COMMAND_GUIDE.md` for consistent command handling and reusable prompt formats.
- Read the assigned task file before coding.
- Do not implement application code unless the assigned task explicitly requires it.
- Do not create trading logic unless the assigned task explicitly requires it.
- Do not mark a phase or step complete unless acceptance criteria and verification are satisfied.
- Update this file when the project phase, step, goal, active task, blocker, open question, or completion state changes.

# Status Update Rule

Codex must update `STATUS.md` whenever project state changes. If state is uncertain, Codex must leave the item open and record the uncertainty under Open Questions or Blockers.
