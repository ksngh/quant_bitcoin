# Role Extraction

Role extraction makes requirements easier to scope before implementation.

## Role Types

Product role:

- Defines user goal, requirement value, and acceptance criteria.

System role:

- Owns a runtime responsibility such as market data, strategy, backtest, execution, or configuration.

Quality role:

- Defines required tests, safety checks, and review criteria.

Owner role:

- The primary role responsible for the requested behavior.

Supporting role:

- A role that provides input, validation, or integration support without owning the behavior.

Forbidden role:

- A role that must not be changed or given responsibility for the requirement.

## Extraction Checklist

For each requirement, Codex should identify:

- raw requirement
- clean requirement
- owner role
- supporting roles
- forbidden roles
- inputs
- outputs
- acceptance criteria
- required tests
- PR review checks

## Example: RSI Strategy

Raw requirement:

- Add RSI trading signals.

Clean requirement:

- Implement an RSI strategy that returns BUY, SELL, or HOLD from normalized candle data.

Owner role:

- Strategy

Supporting roles:

- Test Designer
- Reviewer

Forbidden roles:

- Market Data Provider
- Execution
- Configuration, except for local strategy parameters if needed

Inputs:

- normalized candle data with close prices
- RSI window
- buy threshold
- sell threshold

Outputs:

- BUY, SELL, or HOLD
- optional signal reason

Acceptance criteria:

- BUY is returned when RSI is below or equal to the buy threshold.
- SELL is returned when RSI is above or equal to the sell threshold.
- HOLD is returned otherwise.

Required tests:

- BUY case
- SELL case
- HOLD case
- no external API calls
- no order execution

PR review checks:

- Strategy does not fetch data.
- Strategy does not place orders.
- Strategy does not decide quantity.

## Example: Binance Candle Downloader

Raw requirement:

- Fetch Binance candles.

Clean requirement:

- Implement a historical candle downloader that fetches Binance candle data and normalizes it to the standard candle schema.

Owner role:

- Market Data Provider

Supporting roles:

- Configuration, if local settings are needed
- Test Designer
- Reviewer

Forbidden roles:

- Strategy
- Backtest Engine
- Execution

Inputs:

- symbol
- interval
- start/end range if required

Outputs:

- normalized candle data

Acceptance criteria:

- Historical candles are fetched or mocked in tests.
- Output uses `timestamp`, `open`, `high`, `low`, `close`, `volume`.
- No order endpoint is used.

Required tests:

- mock response normalization
- schema contract test
- safety test for no order endpoint

PR review checks:

- Binance raw fields do not reach strategy code.
- API keys are not hardcoded.
- No order execution was added.

## Example: Basic Backtest

Raw requirement:

- Backtest a strategy.

Clean requirement:

- Implement a simple backtest loop that runs a strategy over historical candle data and returns a basic result.

Owner role:

- Backtest Engine

Supporting roles:

- Strategy
- Market Data Provider
- Test Designer
- Reviewer

Forbidden roles:

- Execution for live orders
- Configuration, except local test settings if needed

Inputs:

- historical candle data
- strategy instance or function

Outputs:

- basic backtest result

Acceptance criteria:

- Backtest runs on local historical data.
- Strategy is reused without modification.
- No live exchange API is called.

Required tests:

- local-data backtest test
- strategy reuse test
- safety test for no real exchange calls

PR review checks:

- Backtest does not place real orders.
- Backtest does not change strategy rules.

## Example: Paper Trader

Raw requirement:

- Add paper trading.

Clean requirement:

- Implement fake execution that records BUY and SELL actions and ignores HOLD.

Owner role:

- Execution

Supporting roles:

- Strategy for signal input
- Test Designer
- Reviewer

Forbidden roles:

- Market Data Provider
- Strategy rule owner
- Live order execution

Inputs:

- symbol
- signal
- quantity

Outputs:

- fake trade record for BUY or SELL
- no trade for HOLD

Acceptance criteria:

- BUY creates a fake buy record.
- SELL creates a fake sell record.
- HOLD creates no trade.
- No external API calls occur.

Required tests:

- BUY fake trade
- SELL fake trade
- HOLD no trade
- no external API calls

PR review checks:

- Paper trader does not call exchange order APIs.
- Paper trader does not calculate indicators.
