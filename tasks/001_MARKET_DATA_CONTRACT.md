# Task 001: Market Data Contract

## Goal

Define the market data provider contract.

## Source Requirement

- `requirements/000_INITIAL_SCOPE.md`

## Extracted Roles

- Owner role: Market Data Provider
- Supporting roles: Architect, Test Designer, Reviewer
- Forbidden roles: Strategy, Backtest Engine, Execution

## Context

Strategy and backtest code need a stable candle format before providers are implemented.

## Scope

- standard candle schema
- provider interface
- validation expectations

## Out of Scope

- Binance API
- strategy
- backtest
- execution
- live trading

## Requirements

- Follow `docs/04_DATA_CONTRACT.md`.
- Strategy must receive normalized candle data only.

## Acceptance Criteria

- contract is defined
- tests verify expected schema if code is implemented

## Required Tests

### Unit Tests

- validate required candle fields if code is implemented

### Integration Tests

- not required

### Contract Tests

- standard candle schema is enforced or documented in code

### Safety Tests

- strategy does not receive provider-specific raw fields

## Review Checklist

- Contract follows `docs/04_DATA_CONTRACT.md`.
- No Binance API implementation was added.
- No strategy, backtest, execution, or live trading behavior was added.

## Verification

- Run relevant tests if code is implemented.

## Completion Summary Required

- files changed
- implementation summary
- tests added or updated
- tests run
- known limitations
- recommended next task
