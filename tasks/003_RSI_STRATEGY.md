# Task 003: RSI Strategy

## Goal

Implement an RSI-based strategy.

## Source Requirement

- `requirements/000_INITIAL_SCOPE.md`

## Extracted Roles

- Owner role: Strategy
- Supporting roles: Test Designer, Reviewer
- Forbidden roles: Market Data Provider, Backtest Engine, Execution

## Context

This is the first technical-analysis strategy. It should prove the strategy boundary without execution behavior.

## Scope

- Signal enum with BUY / SELL / HOLD
- RSI calculation
- RSI strategy using configurable window, buy threshold, and sell threshold

## Out of Scope

- order execution
- quantity calculation
- risk management
- Binance API
- database
- live trading

## Requirements

- Return BUY when RSI <= buy threshold.
- Return SELL when RSI >= sell threshold.
- Return HOLD otherwise.
- Strategy must not fetch data.
- Strategy must not place orders.

## Acceptance Criteria

- BUY test
- SELL test
- HOLD test
- no external API calls
- no order execution

## Verification

- Run relevant tests.

## Required Tests

### Unit Tests

- BUY
- SELL
- HOLD

### Integration Tests

- not required unless a strategy interface already exists

### Contract Tests

- strategy consumes normalized candle data

### Safety Tests

- no external API calls
- no order execution

## Review Checklist

- Strategy does not fetch data.
- Strategy does not place orders.
- Strategy does not decide quantity.
- Strategy does not read API keys.

## Completion Summary Required

- files changed
- implementation summary
- tests added or updated
- tests run
- known limitations
- recommended next task
