# Roadmap

# Phase 1: Codex Working Documents

- Goal: establish requirement, task, test, self-review, and PR review workflow.
- Features: docs, templates, role map, review checklist.
- Out of scope: application code and trading logic.
- Exit criteria: all workflow documents exist and define safety rules.

# Phase 2: Python Project Setup

- Goal: create a minimal importable Python package with runnable tests.
- Features: package structure, test runner configuration, minimal README update if needed.
- Out of scope: trading logic, Binance integration, live trading, risk management.
- Exit criteria: package imports and tests run.

# Phase 3: Market Data Contract

- Goal: define the standard candle schema.
- Features: `timestamp`, `open`, `high`, `low`, `close`, `volume` contract.
- Out of scope: Binance API, strategy, backtest, execution.
- Exit criteria: contract is documented and covered by contract tests when implemented.

# Phase 4: CSV/Local Data Provider

- Goal: load local candle data.
- Features: read CSV, normalize columns, sort by timestamp, return standard schema.
- Out of scope: Binance API, strategy logic, execution.
- Exit criteria: provider passes unit and contract tests.

# Phase 5: RSI Strategy

- Goal: generate BUY / SELL / HOLD from RSI.
- Features: signal enum, RSI calculation, configurable thresholds.
- Out of scope: quantity decisions, order execution, Binance API, database.
- Exit criteria: BUY, SELL, HOLD, and safety tests pass.

# Phase 6: Basic Backtest

- Goal: simulate strategy execution over historical data.
- Features: iterate candles, call strategy, simulate simple trades, return basic result.
- Out of scope: live trading, order APIs, fees, slippage, optimization.
- Exit criteria: deterministic local backtest test passes.

# Phase 7: Paper Trader

- Goal: record fake trades from signals.
- Features: fake BUY and SELL records, HOLD ignored.
- Out of scope: real exchange APIs, risk management, strategy logic.
- Exit criteria: paper trader tests prove no external API calls.

# Phase 8: Binance Historical Candle Downloader

- Goal: collect historical Binance candles.
- Features: minute-level candle fetching, normalization to standard schema.
- Out of scope: order placement, live trading, risk management.
- Exit criteria: mock Binance response tests pass and no order endpoints are used.

# Phase 9: Improved Backtesting

- Goal: improve historical simulation after the basic version works.
- Features: better result reporting and deterministic scenarios.
- Out of scope: portfolio optimization, live trading, advanced risk management unless assigned.
- Exit criteria: expanded backtest tests pass without changing strategy responsibilities.

# Phase 10: Paper Trading With State

- Goal: maintain paper trading state across actions.
- Features: positions, balances, and trade history for paper mode only.
- Out of scope: live exchange order execution and real account state.
- Exit criteria: state transitions are tested without external calls.

# Phase 11: Later Risk Management

- Goal: add explicit risk controls in a future phase.
- Features: to be defined by future requirement.
- Out of scope: first-version implementation.
- Exit criteria: future task defines ownership, tests, and review criteria.

# Phase 12: Later Live Trading

- Goal: add live trading only after explicit approval and risk controls.
- Features: to be defined by future requirement.
- Out of scope: all current first-version work.
- Exit criteria: future task explicitly permits live order execution and defines safety gates.
