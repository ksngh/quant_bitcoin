# Requirement Process

# Purpose

This process turns raw requests into scoped implementation tasks that Codex can execute and review without expanding the project beyond the current phase.

# Process

1. Capture raw requirement.
2. Rewrite as clean requirement.
3. Identify the problem and user goal.
4. Extract roles.
5. Identify owner roles, supporting roles, and forbidden roles.
6. Define functional requirements.
7. Define non-functional requirements.
8. Define out-of-scope items.
9. Define acceptance criteria.
10. Define test requirements.
11. Create or update task document.
12. Implement.
13. Perform Codex self-review.
14. Run PR review.
15. Update decisions/docs if needed.

# Requirement Fields

- Raw requirement: the original user request.
- Clean requirement: a concise, implementation-ready version.
- Problem: what gap the request addresses.
- User goal: what the user should be able to do after completion.
- Functional requirements: required behaviors.
- Non-functional requirements: constraints such as safety, local execution, and no live exchange calls.
- Out of scope: behaviors that must not be implemented.
- Acceptance criteria: observable pass/fail conditions.
- Required tests: unit, integration, contract, and safety tests where relevant.

# Example

Raw requirement:

Fetch BTCUSDT 1-minute candle data from Binance.

Clean requirement:

Create a Binance historical candle downloader that fetches BTCUSDT 1-minute candle data and normalizes it to the standard candle schema.

Owner role:

Market Data Provider.

Supporting roles:

Configuration for endpoint and symbol settings, Test Designer for mock response tests.

Forbidden roles:

Strategy, Backtest Engine, Execution.

Out of scope:

Real order execution, API-key trading, risk management, strategy signals, backtest execution.

Acceptance criteria:

- Downloader returns `timestamp`, `open`, `high`, `low`, `close`, `volume`.
- Unit tests use mocked Binance responses.
- No order endpoints are called.
- No real API keys are required for unit tests.
