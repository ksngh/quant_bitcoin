# Codex Workflow

## Standard Workflow

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
11. Perform PR review.
12. Update decisions/docs if behavior or architecture changed.

## Scope-Control Rules

- If task is about market data, do not implement strategy.
- If task is about strategy, do not implement execution.
- If task is about backtesting, do not implement live trading.
- If task is about paper trading, do not call real exchange APIs.
- If task is about Binance candle downloading, do not implement real order execution.

## Error-Handling Rules

- If a command fails, summarize the error.
- Explain the likely cause.
- Apply the smallest in-scope fix.
- If the fix is out of scope, stop and report it.
