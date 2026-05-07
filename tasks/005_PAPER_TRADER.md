# Task 005: Paper Trader

## Goal

Implement fake execution.

## Source Requirement

- `requirements/000_INITIAL_SCOPE.md`

## Extracted Roles

- Owner role: Execution
- Supporting roles: Strategy, Test Designer, Reviewer
- Forbidden roles: Market Data Provider, Backtest Engine, Live order execution

## Context

Paper trading records simulated trades and must never place real orders.

## Scope

- receive symbol, signal, and quantity
- record fake BUY and SELL actions
- ignore HOLD

## Out of Scope

- real exchange API
- Binance order execution
- risk management
- strategy logic

## Requirements

- Treat BUY and SELL as fake actions.
- HOLD must not create a trade.
- Do not call external order APIs.

## Acceptance Criteria

- BUY creates fake buy record
- SELL creates fake sell record
- HOLD creates no trade
- no external API calls

## Verification

- Run relevant tests.

## Required Tests

### Unit Tests

- BUY creates fake buy record
- SELL creates fake sell record
- HOLD creates no trade

### Integration Tests

- not required unless integrated with strategy in scope

### Contract Tests

- signal input is handled as defined by strategy contract

### Safety Tests

- no external API calls
- no Binance order execution

## Review Checklist

- Paper trader does not call real exchange APIs.
- Paper trader does not calculate indicators.
- Paper trader does not define strategy rules.

## Completion Summary Required

- files changed
- implementation summary
- tests added or updated
- tests run
- known limitations
- recommended next task
