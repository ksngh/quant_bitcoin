# Project Status

# Current Phase

Phase 5: RSI Strategy

# Current Step

Task 003: RSI Strategy

# Current Goal

Implement an RSI strategy that returns BUY, SELL, or HOLD from standard candle data.

# Current Active Task

Task 003: RSI Strategy.

# Last Completed Step

Task 002: CSV Data Provider.

Verified on 2026-05-07 with `pytest`: 9 passed.

# Next Step

Read `tasks/003_RSI_STRATEGY.md`, define the test cases, implement the strategy, run verification, and perform Codex self-review.

# Parallel Work Status

Parallel work is allowed only for independent leaf tasks.

Reason:
The documentation workflow, Python project setup, market data contract, and CSV provider have been verified. Shared contract changes must still not be parallelized.

# Phase Checklist

- [x] Step 1.1: Create Codex workflow documentation
- [x] Python project setup complete and verified
- [x] Market data contract complete and verified
- [x] CSV data provider complete and verified
- [x] Parallel work rules reviewed after foundation completion
- [ ] RSI strategy complete and verified

# Open Questions

- Should the RSI strategy use only the latest RSI value, or require a threshold crossing from the previous RSI value?

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
