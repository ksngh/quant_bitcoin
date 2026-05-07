# Purpose

PR review verifies that a task is complete, scoped, tested, safe, and consistent with architecture.

# Review Steps

1. Read requirement file.
2. Read task file.
3. Inspect changed files.
4. Check task scope.
5. Check role ownership.
6. Check architecture boundaries.
7. Check tests.
8. Check safety.
9. Check docs/decision updates.
10. Approve, request changes, or create follow-up task.

# Required PR Summary

- Requirement
- Task
- What changed
- What did not change
- Tests run
- Codex self-review result
- Safety notes
- Known limitations
- Follow-up tasks

# Review Decision Types

- Approve
- Request changes
- Follow-up task

# Strict Trading Review Areas

- API keys are not hardcoded.
- `.env` files are not committed.
- Live order execution is absent unless explicitly requested by the task.
- Exchange order endpoints are not called by market data, strategy, backtest, or paper trading code.
- Paper trading does not use live exchange clients.
- Binance candle downloader uses historical data endpoints only and does not use order endpoints.
