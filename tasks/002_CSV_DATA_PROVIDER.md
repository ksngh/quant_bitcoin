# Task 002: CSV Data Provider

## Goal

Implement a local candle data provider.

## Source Requirement

- `requirements/000_INITIAL_SCOPE.md`

## Extracted Roles

- Owner role: Market Data Provider
- Supporting roles: Test Designer, Reviewer
- Forbidden roles: Strategy, Backtest Engine, Execution

## Context

Local candle data is needed before backtesting and strategy work can be exercised safely.

## Scope

- read candle data from CSV
- normalize columns
- sort by timestamp
- return standard candle schema

## Out of Scope

- Binance API
- live trading
- strategy logic
- execution

## Requirements

- Follow `docs/02_DATA_CONTRACT.md`.
- Return only the standard candle schema.
- Keep provider behavior focused on data loading and normalization.

## Acceptance Criteria

- provider returns standard candle data
- tests cover valid CSV data
- tests cover missing required columns if reasonable

## Verification

- Run relevant tests.

## Required Tests

### Unit Tests

- valid CSV data returns standard candle data
- missing required columns are rejected or handled if reasonable

### Integration Tests

- local CSV provider can load sample local data if sample data is added in scope

### Contract Tests

- output contains `timestamp`, `open`, `high`, `low`, `close`, `volume`
- rows are sorted by timestamp ascending

### Safety Tests

- no external API calls

## Review Checklist

- CSV provider does not implement strategy logic.
- CSV provider does not implement execution.
- Output follows `docs/04_DATA_CONTRACT.md`.

## Completion Summary Required

- files changed
- implementation summary
- tests added or updated
- tests run
- known limitations
- recommended next task
