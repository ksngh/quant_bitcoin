# Task 004: Basic Backtest

# Goal

Run a basic historical simulation using candle data and a strategy.

# Source Requirement

`requirements/000_INITIAL_SCOPE.md`

# Extracted Roles

- Owner role: Backtest Engine
- Supporting roles: Strategy, Market Data Provider, Test Designer
- Forbidden roles: Live Execution, Binance order client

# Scope

- iterate through historical candle data
- call strategy
- simulate trades
- return basic result

# Out of Scope

- live trading
- Binance real orders
- advanced performance metrics
- fees
- slippage
- optimization


# Implementation Assumption

The task does not define position sizing or portfolio accounting rules. The first
implementation uses a long-only, fixed-quantity simulation: BUY opens one
position when flat and cash is sufficient, SELL closes the open position, and
HOLD or duplicate signals do not create trades. Fees, slippage, optimization,
and advanced metrics remain out of scope.

# Acceptance Criteria

- Backtest runs on local historical data.
- Backtest reuses strategy without modifying it.
- Backtest returns a basic result.
- Backtest does not call live exchange APIs.

# Required Tests

- Unit Tests: result calculation for simple scenarios.
- Integration Tests: run with local candle fixture and simple strategy.
- Contract Tests: input uses standard candle schema.
- Safety Tests: no live exchange calls and no real order execution.

# Review Checklist

- Backtest does not contain strategy formulas unless explicitly assigned.
- Backtest does not place real orders.
