# Codex Workflow

# Standard Workflow

1. Receive raw requirement.
2. Create or update requirement document.
3. Extract roles.
4. Check responsibility boundaries.
5. Create or update task document.
6. Create or update test plan.
7. Implement the task.
8. Run tests.
9. Perform Codex self-review.
10. Prepare PR summary.
11. Open PR.
12. Run Codex PR review.
13. Perform human final review.
14. Update decisions/docs if behavior or architecture changed.

# Scope-Control Rules

- If task is about market data, do not implement strategy.
- If task is about strategy, do not implement execution.
- If task is about backtesting, do not implement live trading.
- If task is about paper trading, do not call real exchange APIs.
- If task is about Binance candle downloading, do not implement real order execution.

# Parallel-Work Rules

- One prompt may include multiple tasks only when they are independent leaf tasks.
- Do not parallelize contract changes.
- Do not parallelize integration work that depends on unfinished modules.
- If the task batch is not parallel-safe, implement only the safe subset and report the blocked work.

# Error-Handling Rules

- If a command fails, summarize the error.
- Explain the likely cause.
- Apply the smallest in-scope fix.
- If the fix is out of scope, stop and report it.
