# Project Status

# Current Phase

Phase 9: Improved Backtesting

# Current Step

Task 007: Improved Backtesting

# Current Goal

Improve historical backtest result reporting with deterministic scenarios while preserving strategy and candle-data boundaries.

# Current Active Task

Task 007: Improved Backtesting.

# Last Completed Step

Task 006: Binance Candle Downloader.

Verified on 2026-05-07 with `pytest`: 66 passed.

# Next Step

Read `tasks/007_IMPROVED_BACKTESTING.md`, define the test cases, implement only the improved backtesting changes, run verification, and perform Codex self-review.

# Parallel Work Status

Parallel work is allowed only for independent leaf tasks.

Reason:
The documentation workflow, Python project setup, market data contract, CSV provider, RSI strategy, basic backtest, paper trader, and Binance candle downloader have been verified. Shared contract changes must still not be parallelized.

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
- [ ] Improved backtesting complete and verified

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
