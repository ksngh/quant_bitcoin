# Project Status

# Current Phase

Phase 11: Later Risk Management

# Current Step

Task 010: Basic Paper Risk Checks

# Current Goal

Implement deterministic paper-only risk checks for proposed paper trades without exchange APIs or state mutation.

# Current Active Task

Task 010: Basic Paper Risk Checks.

# Last Completed Step

Task 009: Risk Management Task Definition.

Verified on 2026-05-08 with `pytest`: 84 passed.

# Next Step

Read `tasks/010_BASIC_RISK_CHECKS.md`, define the test cases, implement only basic paper risk checks, run verification, and perform Codex self-review.

# Parallel Work Status

Parallel work is allowed only for independent leaf tasks.

Reason:
The documentation workflow, Python project setup, market data contract, CSV provider, RSI strategy, basic backtest, paper trader, Binance candle downloader, improved backtesting, paper trading with state, and risk-management task definition have been verified. Shared contract changes must still not be parallelized.

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
- [ ] Basic paper risk checks complete and verified

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
