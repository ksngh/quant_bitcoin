# Project Status

# Current Phase

Phase 12: Later Live Trading

# Current Step

Task 011: Live Trading Safety Gates

# Current Goal

Define live-trading safety gates before any live order execution code is implemented.

# Current Active Task

Task 011: Live Trading Safety Gates.

# Last Completed Step

Task 010: Basic Paper Risk Checks.

Verified on 2026-05-08 with `pytest`: 113 passed.

# Next Step

Read `tasks/011_LIVE_TRADING_SAFETY_GATES.md`, define the future live-trading safety gates and next safe task or blocker, run verification, and perform Codex self-review without implementing application code.

# Parallel Work Status

Parallel work is allowed only for independent leaf tasks.

Reason:
The documentation workflow, Python project setup, market data contract, CSV provider, RSI strategy, basic backtest, paper trader, Binance candle downloader, improved backtesting, paper trading with state, risk-management task definition, and basic paper risk checks have been verified. Shared contract changes must still not be parallelized.

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
- [ ] Live trading safety gates defined

# Open Questions

None currently recorded.

# Blockers

None currently recorded.

# Rules for Next Codex Task

- Read `AGENTS.md` before working.
- Read this `STATUS.md` before starting implementation tasks.
- Read the assigned task file before coding.
- Do not implement application code unless the assigned task explicitly requires it.
- Do not create trading logic unless the assigned task explicitly requires it.
- Do not mark a phase or step complete unless acceptance criteria and verification are satisfied.
- Update this file when the project phase, step, goal, active task, blocker, or completion state changes.

# Status Update Rule

Codex must update `STATUS.md` whenever project state changes. If state is uncertain, Codex must leave the item open and record the uncertainty under Open Questions or Blockers.
