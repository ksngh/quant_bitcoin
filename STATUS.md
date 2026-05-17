# Project Status

# Current Phase

Phase 28: Swing Structure Implementation

# Current Step

Task 029: Swing Structure implemented and ready for review.

# Current Goal

Review the Swing Structure implementation and continue one-indicator-at-a-time work without expanding scope.

# Current Active Task

Task 029: Implement Swing Structure. Owner-provided swing structure formula was saved to `tasks/indicators/swing_structure.md`; implementation and deterministic tests are complete pending review.

# Last Completed Step

Task 028: Pivot High / Pivot Low.

Implemented deterministic confirmed pivot high / pivot low event detection from already-provided candle data. Verified with deterministic tests and compile checks.

Previous completed step: Task 025: WebSocket Unbounded Ingestion Service.

# Next Step

Recommended next task: owner review of Task 029, then explicitly assign the next one-indicator implementation task. Task 030: ATR is a likely next dependency for ATR-thresholded structure and other indicators. Local Docker Compose runtime startup verification for Task 014/018 remains deferred to a Docker-capable developer environment.

# Parallel Work Status

Parallel work is not currently recommended.

Reason:
Tasks 027-033 define multiple indicator implementation plans, but concrete indicator implementation should proceed one indicator at a time unless the owner explicitly approves independent parallel leaf tasks that do not change shared contracts. Pivot-derived tasks may depend on Task 028, and displacement/zone tasks may depend on ATR or Volume Ratio decisions.

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
- [x] Task 023: Backtest Result Read Model for Graphs approved for implementation by owner prompt on 2026-05-16
- [x] Task 023: Backtest Result Read Model for Graphs complete and verified
- [x] Task 024: Database Schema Command Management task document created
- [x] Task 024: Database Schema Command Management approved for implementation by owner prompt on 2026-05-16
- [x] Task 024: Database Schema Command Management complete and verified
- [x] Task 025: WebSocket Unbounded Ingestion Service task document created
- [x] Task 025: WebSocket Unbounded Ingestion Service approved for implementation by owner prompt on 2026-05-16
- [x] Task 025: WebSocket Unbounded Ingestion Service complete and verified
- [x] Task 025: Indicator Document Intake Process task document created
- [x] First owner-provided indicator document saved under `tasks/indicators/`
- [x] Task 027: Bid-Ask Spread implementation task document created
- [x] Task 028: Pivot High / Pivot Low implementation task document created
- [x] Task 029: Swing Structure implementation task document created
- [x] Task 029: Swing Structure complete and verified
- [x] Task 030: ATR implementation task document created
- [x] Task 031: Volume Ratio implementation task document created
- [x] Task 032: Support / Resistance Zone implementation task document created
- [x] Task 033: Displacement Candle implementation task document created

# Open Questions

- Has the project owner explicitly approved live trading and real order execution?
- What credential policy should be used for API keys and secrets?
- Should future live trading use Binance testnet/sandbox first?
- What real-order endpoints, if any, are allowed?
- What kill-switch or disable mechanism is required?
- Task 024 decided the concrete PostgreSQL command-management path: `db/init/001_schema.sql` is the source-of-truth first-start schema DDL, `db/changes/` is reserved for future existing-database state-change SQL, repository initialization executes managed command files, and runtime persistence DML remains application-owned.
- Task 025 defines the indicator document intake process. Future owner-provided indicator documents should be saved under `tasks/indicators/<INDICATOR_KEY>.md`, and concrete indicator code must wait for an explicit indicator-specific implementation task.
- Tasks 027-033 define planned implementation tasks for the remaining indicator/filter modules. Task 028 Pivot High / Pivot Low and Task 029 Swing Structure have owner-provided formulas saved under `tasks/indicators/` and deterministic implementations pending review. Remaining unimplemented indicator tasks still require explicit assignment and owner-approved detailed formulas before coding.
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
