# Roadmap

## Phase 1: Codex Working Documents

Goal:

- establish working documents for requirements, roles, tasks, tests, reviews, and decisions

Features:

- `AGENTS.md`
- `docs/`
- `requirements/`
- `roles/`
- `tasks/`
- `tests/`
- `reviews/`

Out of scope:

- application code
- trading logic
- dependency installation

Exit criteria:

- requested documentation structure exists
- future tasks have clear templates and boundaries

## Phase 2: Python Project Setup

Goal:

- create the minimal Python project structure later

Features:

- package structure
- test folder
- minimal project metadata
- optional README if needed

Out of scope:

- trading logic
- Binance integration
- live trading

Exit criteria:

- package can be imported
- tests can run
- no trading logic exists

## Phase 3: Market Data Contract

Goal:

- define the standard candle data contract in code later

Features:

- standard candle schema
- validation expectations
- provider interface

Out of scope:

- Binance API
- strategy
- execution

Exit criteria:

- contract is defined
- tests verify expected schema if code is implemented

## Phase 4: CSV/local Data Provider

Goal:

- load local candle data for testing and backtesting

Features:

- CSV loading
- schema normalization
- timestamp sorting
- basic validation

Out of scope:

- Binance API
- strategy logic
- execution

Exit criteria:

- provider returns standard candle data
- valid and invalid CSV cases are tested

## Phase 5: RSI Strategy

Goal:

- create the first technical-analysis strategy

Features:

- Signal enum
- RSI calculation
- BUY / SELL / HOLD signal

Out of scope:

- order quantity
- execution
- risk management

Exit criteria:

- BUY, SELL, and HOLD are tested
- strategy makes no external API calls

## Phase 6: Basic Backtest

Goal:

- simulate a strategy on historical data

Features:

- simple historical loop
- strategy calls
- simple trade simulation
- basic result summary

Out of scope:

- live trading
- advanced analytics
- fees
- slippage
- optimization

Exit criteria:

- backtest runs on local historical data
- no live exchange calls occur

## Phase 7: Paper Trader

Goal:

- simulate execution without real orders

Features:

- fake BUY records
- fake SELL records
- HOLD creates no trade

Out of scope:

- real exchange API
- Binance order execution
- risk management

Exit criteria:

- BUY, SELL, and HOLD behavior is tested
- no external order API is called

## Phase 8: Binance Historical Candle Downloader

Goal:

- fetch historical minute-level candle data from Binance

Features:

- historical candle fetch
- minute-level interval support
- standard schema normalization

Out of scope:

- placing orders
- live trading
- strategy logic

Exit criteria:

- mocked or fetched historical candles normalize correctly
- no order endpoint is used

## Phase 9: Improved Backtesting

Goal:

- improve backtest usefulness after the basic loop works

Features:

- to be defined later

Out of scope:

- live trading
- real order execution

Exit criteria:

- to be defined in a future task

## Phase 10: Paper Trading With State

Goal:

- add fake balance and fake positions after simple paper trading works

Features:

- to be defined later

Out of scope:

- real balances
- real positions
- real exchange order execution

Exit criteria:

- to be defined in a future task

## Phase 11: Later Risk Management

Goal:

- add risk controls only after the basic trading flow exists

Features:

- to be defined later

Out of scope:

- all risk management implementation for now

Exit criteria:

- to be defined in a future task

## Phase 12: Later Live Trading

Goal:

- add live trading only after paper trading and safety rules are proven

Features:

- to be defined later

Out of scope:

- all real order execution for now

Exit criteria:

- to be defined in a future task
