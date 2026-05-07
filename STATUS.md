# Project Status

# Current Phase

Phase 8: Binance Candle Downloader

# Current Step

Task 006: Binance Candle Downloader

# Current Goal

Fetch Binance historical candle data and normalize it to the standard candle schema without order execution.

# Current Active Task

Task 006: Binance Candle Downloader.

# Last Completed Step

Task 005: Paper Trader.

Verified on 2026-05-07 with `pytest`: 46 passed.

# Next Step

Read `tasks/006_BINANCE_CANDLE_DOWNLOADER.md`, define the test cases, implement the Binance historical candle downloader, run verification, and perform Codex self-review.

# Parallel Work Status

Parallel work is allowed only for independent leaf tasks.

Reason:
The documentation workflow, Python project setup, market data contract, CSV provider, RSI strategy, basic backtest, and paper trader have been verified. Shared contract changes must still not be parallelized.

# Phase Checklist

- [x] Step 1.1: Create Codex workflow documentation
- [x] Python project setup complete and verified
- [x] Market data contract complete and verified
- [x] CSV data provider complete and verified
- [x] Parallel work rules reviewed after foundation completion
- [x] RSI strategy complete and verified
- [x] Basic backtest complete and verified
- [x] Paper trader complete and verified
- [ ] Binance candle downloader complete and verified

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
