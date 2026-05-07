# Task 006: Binance Candle Downloader

## Goal

Fetch historical candle data from Binance.

## Source Requirement

- `requirements/000_INITIAL_SCOPE.md`

## Extracted Roles

- Owner role: Market Data Provider
- Supporting roles: Configuration, Test Designer, Reviewer
- Forbidden roles: Strategy, Backtest Engine, Execution

## Context

This task is only for historical candle collection. It must not introduce order execution.

## Scope

- fetch historical candles
- support minute-level candles
- normalize to standard candle schema
- no order execution

## Out of Scope

- live trading
- real order placement
- risk management
- strategy logic

## Requirements

- Binance raw responses must not be passed directly to strategy.
- Output must follow `docs/02_DATA_CONTRACT.md`.
- API keys must not be hardcoded.

## Acceptance Criteria

- historical candles can be fetched or mocked in tests
- output follows standard schema
- no real order endpoint is used

## Verification

- Run relevant tests.

## Required Tests

### Unit Tests

- mocked Binance response is normalized

### Integration Tests

- optional mocked downloader integration if useful

### Contract Tests

- output follows `docs/04_DATA_CONTRACT.md`

### Safety Tests

- no real order endpoint is used
- unit tests do not require real API keys

## Review Checklist

- Binance raw responses are normalized before strategy use.
- No order execution was added.
- API keys are not hardcoded.

## Completion Summary Required

- files changed
- implementation summary
- tests added or updated
- tests run
- known limitations
- recommended next task
