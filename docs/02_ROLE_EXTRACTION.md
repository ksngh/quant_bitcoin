# Role Extraction Guide

# Role Types

- Product role: defines the user goal, scope, and non-goals.
- System role: owns a system behavior or module responsibility.
- Quality role: defines tests, safety checks, and review criteria.
- Owner role: the only role allowed to own the main behavior.
- Supporting role: a role that may assist without owning the behavior.
- Forbidden role: a role that must not participate in the behavior.

# Extraction Checklist

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

# Example: RSI Strategy

- Raw requirement: Implement RSI strategy.
- Clean requirement: Create strategy logic that calculates RSI and returns BUY, SELL, or HOLD.
- Owner role: Strategy.
- Supporting roles: Test Designer.
- Forbidden roles: Market Data Provider, Execution, Configuration for secrets.
- Inputs: standard candle data, RSI window, buy threshold, sell threshold.
- Outputs: BUY / SELL / HOLD signal and optional reason.
- Acceptance criteria: returns all three signal types under deterministic test data.
- Required tests: BUY, SELL, HOLD, no external API calls, no order execution.
- PR review checks: strategy does not fetch data, place orders, decide quantity, or read API keys.

# Example: Binance Candle Downloader

- Raw requirement: Fetch Binance candles.
- Clean requirement: Fetch historical candles and normalize them to the standard candle schema.
- Owner role: Market Data Provider.
- Supporting roles: Configuration, Test Designer.
- Forbidden roles: Strategy, Backtest Engine, Execution.
- Inputs: symbol, interval, start/end time.
- Outputs: normalized candle rows.
- Acceptance criteria: produces standard schema from mocked Binance responses.
- Required tests: mock response normalization, no order endpoint calls, no real API keys.
- PR review checks: downloader does not generate signals, execute orders, or calculate quantities.

# Example: Basic Backtest

- Raw requirement: Run basic backtest.
- Clean requirement: Iterate through historical candles, call a strategy, simulate trades, and return a basic result.
- Owner role: Backtest Engine.
- Supporting roles: Strategy, Market Data Provider, Test Designer.
- Forbidden roles: Live Execution, Binance order client.
- Inputs: standard candle data, strategy instance, initial cash or simple starting state if required by task.
- Outputs: basic backtest result.
- Acceptance criteria: runs on local historical data and returns deterministic result.
- Required tests: local historical data run, strategy reuse, no live exchange calls.
- PR review checks: backtest does not place real orders or modify strategy internals.

# Example: Paper Trader

- Raw requirement: Add paper trader.
- Clean requirement: Record fake BUY and SELL actions from signals and ignore HOLD.
- Owner role: Execution.
- Supporting roles: Test Designer.
- Forbidden roles: Strategy, Market Data Provider, live exchange client.
- Inputs: symbol, signal, quantity.
- Outputs: fake trade record or no action for HOLD.
- Acceptance criteria: BUY and SELL record fake trades; HOLD records none.
- Required tests: BUY fake trade, SELL fake trade, HOLD no trade, no external API calls.
- PR review checks: paper trader never calls exchange order APIs and does not calculate RSI.
