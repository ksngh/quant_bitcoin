# Task 004: Basic Backtest

## Goal

Implement the simplest useful backtest loop.

## Source Requirement

- `requirements/000_INITIAL_SCOPE.md`

## Extracted Roles

- Owner role: Backtest Engine
- Supporting roles: Strategy, Market Data Provider, Test Designer, Reviewer
- Forbidden roles: Execution for live orders

## Context

Backtesting should reuse the strategy and historical candle data without live exchange interaction.

## Scope

- iterate through historical candle data
- call strategy
- simulate trades
- return basic result

## Out of Scope

- live trading
- Binance real orders
- advanced performance metrics
- fees
- slippage
- optimization

## Requirements

- Reuse the existing strategy interface.
- Use normalized candle data.
- Keep results simple and easy to inspect.

## Acceptance Criteria

- backtest can run on local data
- strategy is reused without modification
- no real exchange calls

## Verification

- Run relevant tests.

## Required Tests

### Unit Tests

- simple backtest result behavior

### Integration Tests

- backtest can run on local historical data
- strategy is reused without modification

### Contract Tests

- backtest consumes normalized candle data

### Safety Tests

- no real exchange calls
- no real order placement

## Review Checklist

- Backtest does not implement live trading.
- Backtest does not call Binance real order APIs.
- Strategy rules are not modified to fit the backtest.

## Completion Summary Required

- files changed
- implementation summary
- tests added or updated
- tests run
- known limitations
- recommended next task
