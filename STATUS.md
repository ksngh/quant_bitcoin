# Project Status

# Current Phase

Phase 14: PostgreSQL Backfill Persistence

# Current Step

Task 014: PostgreSQL Binance Backfill is not implemented and is awaiting explicit human approval.

# Current Goal

Review and approve the Task 014 implementation scope before adding PostgreSQL, Docker Compose, or Binance historical candle persistence.

# Current Active Task

None currently assigned.

# Last Completed Step

Task 016: Codex Command Consistency.

This was documentation-only work and did not implement Task 014 or Task 015.

Verified on 2026-05-11 with `git diff --check`.

# Next Step

Review `tasks/014_POSTGRES_BINANCE_BACKFILL.md` and provide explicit human approval before implementing PostgreSQL, Docker Compose, or Binance historical candle persistence.

# Parallel Work Status

Parallel work is not currently recommended.

Reason:
The next work touches shared persistence contracts and local infrastructure. Schema, database, backfill, and WebSocket work should proceed sequentially through assigned task documents.

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
- [ ] Task 014: PostgreSQL Binance Backfill approved for implementation
- [ ] Task 014: PostgreSQL Binance Backfill complete and verified
- [ ] Task 015: Binance WebSocket Candle Ingestion approved for implementation
- [ ] Task 015: Binance WebSocket Candle Ingestion complete and verified

# Open Questions

- Has the project owner explicitly approved live trading and real order execution?
- What credential policy should be used for API keys and secrets?
- Should future live trading use Binance testnet/sandbox first?
- What real-order endpoints, if any, are allowed?
- What kill-switch or disable mechanism is required?
- Has the project owner explicitly approved implementing Task 014: PostgreSQL Binance Backfill?
- Should future PostgreSQL implementation use migrations, container init scripts, or another schema-management path?

# Blockers

- Live trading implementation is blocked until explicit human approval, credential policy, sandbox/testnet policy, real-order endpoint allowlist, kill-switch design, and safety tests are documented.
- PostgreSQL, Docker Compose, Binance backfill, and WebSocket ingestion implementation are blocked until the corresponding assigned task is explicitly approved.

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
