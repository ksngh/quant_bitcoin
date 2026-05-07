# Requirement Process

This process turns raw requests into scoped implementation tasks.

## Steps

1. Capture raw requirement.
2. Rewrite it as a clean requirement.
3. Identify the problem and user goal.
4. Extract roles.
5. Identify owner roles, supporting roles, and forbidden roles.
6. Define functional requirements.
7. Define non-functional requirements.
8. Define out-of-scope items.
9. Define acceptance criteria.
10. Define test requirements.
11. Create or update the task document.
12. Implement the task.
13. Perform Codex self-review.
14. Perform PR review.
15. Update decisions or docs if behavior or architecture changed.

## Required Output Before Implementation

- clean requirement
- owner role
- supporting roles
- forbidden roles
- scope
- out of scope
- acceptance criteria
- required tests
- review checks
- assumptions, if any

## Example

Raw requirement:

- Fetch BTCUSDT 1-minute candle data from Binance.

Clean requirement:

- Add a Binance historical candle downloader that can fetch BTCUSDT 1-minute candle data and normalize it to the standard candle schema.

Problem:

- Local CSV data is not enough for future backtests that need exchange historical candles.

User goal:

- Obtain normalized minute-level BTCUSDT candle data for strategy and backtest use.

Owner role:

- Market Data Provider

Supporting roles:

- Test Designer
- Reviewer
- Configuration, only if settings are needed

Forbidden roles:

- Strategy
- Backtest Engine
- Execution

Functional requirements:

- Fetch historical BTCUSDT candles.
- Support 1-minute interval.
- Normalize output to `timestamp`, `open`, `high`, `low`, `close`, `volume`.

Non-functional requirements:

- Do not require real API keys for unit tests.
- Do not expose Binance raw response fields to strategy code.

Out of scope:

- placing orders
- live trading
- strategy rules
- risk controls

Acceptance criteria:

- Mock Binance candle response is normalized correctly.
- Output follows the standard candle schema.
- No order endpoint is called.

Required tests:

- contract test for standard candle schema
- unit test with mocked Binance response
- safety test that no order endpoint is used
