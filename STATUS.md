# Project Status

# Current Phase

Phase 21: Graph-Ready Backtest Persistence Planning

# Current Step

Task 021: Graph-ready backtest persistence schema documented and accepted; Task 022 implementation not started.

# Current Goal

Prepare the accepted graph-ready backtest persistence contract for Task 022 PostgreSQL result writes and Task 023 graph read models.

# Current Active Task

None. Task 021 is completed as documentation/design only. No DB schema or write implementation has been added.

# Last Completed Step

Task 021: Graph-Ready Backtest Persistence Schema.

Documented and accepted a graph-ready PostgreSQL backtest persistence schema for `strategy_configs`, `backtest_runs`, `backtest_results`, `backtest_trades`, and first-class `backtest_graph_points`. The accepted design preserves the standard candle contract and existing `BasicBacktester.run(candles, strategy)` public boundary, keeps the existing CLI stdout JSON behavior for now, and requires later graphing workflows to read persisted summary/trade/graph-point rows without re-running the backtest. Verified on 2026-05-16 with `git diff --check`. This documentation-only task does not add migrations, SQL files, repository classes, graph UI, API services, schedulers, live trading, signed requests, API-key handling, Binance network calls, or exchange order endpoint behavior.

# Next Step

Recommended next task: Task 022 PostgreSQL Backtest Result Persistence. Implement DB writes only against the accepted Task 021 schema, keep stdout JSON behavior unless Task 022 explicitly changes it, and defer graph-read APIs/models to Task 023. If PostgreSQL candles need to exist before local backtesting, run the accepted Task 014 PostgreSQL Binance backfill first. Local Docker Compose runtime startup verification for Task 018 remains deferred to a Docker-capable developer environment.

# Parallel Work Status

Parallel work is not currently recommended.

Reason:
Task 021 design is complete. Tasks 022-023 intentionally touch shared persistence contracts and should proceed sequentially: write implementation next, read model third.

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
- [ ] Task 022: PostgreSQL Backtest Result Persistence approved for implementation
- [ ] Task 023: Backtest Result Read Model for Graphs approved for implementation

# Open Questions

- Has the project owner explicitly approved live trading and real order execution?
- What credential policy should be used for API keys and secrets?
- Should future live trading use Binance testnet/sandbox first?
- What real-order endpoints, if any, are allowed?
- What kill-switch or disable mechanism is required?
- Should future PostgreSQL implementation use migrations, container init scripts, or another schema-management path? Current Task 014 uses container init SQL plus repository schema initialization; migrations remain a future decision if schema evolution is needed. Task 021 accepted the graph-ready backtest persistence schema; Task 022 should choose the minimal implementation path for creating/writing those tables.
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
