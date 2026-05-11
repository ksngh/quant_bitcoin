# Task 013: Persistence Schema Design

# Goal

Review the current project and document the data that should be persisted before any database implementation is added.

# Source Requirement

User request on 2026-05-09:

- Review the current project and design schemas for data that should be stored.
- Include the Binance candle data that should be stored in the database.
- Write the result as documentation before implementation.

# Extracted Roles

- Owner role: Architect
- Supporting roles: Market Data Provider, Backtest Engine, Paper Execution, Strategy, Test Designer
- Forbidden roles: Live Trading, Binance order client implementation, Scheduler, Dashboard

# Context

The project currently has market data, strategy, backtesting, paper trading, risk checks, and a Binance historical candle downloader. Database work is out of scope by default in `AGENTS.md`, so this task is documentation-only. It must define the persistence contract before any PostgreSQL, Docker, migration, backfill, or WebSocket implementation task starts.

# Scope

- Review existing project modules and task history.
- Identify data that should be persisted for future historical data, backtesting, paper trading, and ingestion workflows.
- Design proposed database schemas at documentation level.
- Include Binance candle persistence design.
- Define candle uniqueness and timestamp semantics.
- Define what data should remain outside persistence for now.
- Define test expectations for later implementation tasks.

# Out of Scope

- Creating database migrations.
- Creating Docker Compose files.
- Installing PostgreSQL dependencies.
- Implementing repository classes.
- Implementing Binance backfill persistence.
- Implementing WebSocket ingestion.
- Implementing schedulers.
- Implementing dashboards.
- Implementing live trading or real order execution.
- Storing API keys, secrets, or `.env` files.

# Requirements

- Document a proposed `candles` schema for Binance market data.
- The candle design must include source, symbol, interval, open timestamp, OHLCV values, Binance-specific volume/trade fields, and raw provider payload storage if needed.
- The candle design must include a uniqueness rule equivalent to `source + symbol + interval + open_time`.
- The design must distinguish open time, close time, and ingestion/update timestamps.
- The design must identify additional future tables, such as backtest runs, backtest trades, backtest results, paper sessions, paper trades, paper state snapshots, strategy configurations, and ingestion checkpoints.
- The design must state that paper-trading persistence records simulated state only.
- The design must state that live-trading order data remains blocked until explicit approval and safety gates are satisfied.
- The design must recommend PostgreSQL as the primary database candidate and note SQLite only as a prototype or test fixture option.

# Project Review Summary

Current project modules reviewed for this design:

- `docs/04_DATA_CONTRACT.md` defines the standard candle schema consumed by strategy and backtest code: `timestamp`, `open`, `high`, `low`, `close`, `volume`.
- `quant_bitcoin/market_data/binance_downloader.py` fetches public Binance spot klines from `/api/v3/klines`, normalizes the first six Binance fields to the standard candle schema, supports minute intervals, and rejects order endpoints.
- `quant_bitcoin/market_data/csv_provider.py` loads local CSV candles and normalizes them to the same standard candle schema.
- `quant_bitcoin/strategies/rsi.py` consumes standard candles only and returns `BUY`, `SELL`, or `HOLD`.
- `quant_bitcoin/backtesting/basic.py` simulates in-memory long-only trades and returns `BacktestResult`, `BacktestSummary`, and `BacktestTrade`.
- `quant_bitcoin/execution/paper_trader.py` records simulated paper trades and local paper state only.
- `quant_bitcoin/risk/paper_checks.py` returns deterministic paper risk decisions without mutating state or calling external APIs.

# Persistence Boundary

Persistence must preserve the existing role boundaries:

- Market Data Provider owns stored candle data and ingestion metadata.
- Strategy may store configuration metadata, but strategy code must still consume only the standard candle schema.
- Backtest Engine owns persisted backtest runs, trades, and summary results.
- Paper Execution owns persisted paper sessions, paper trades, and paper state snapshots.
- Risk Management may later persist paper-only risk decisions if a task explicitly asks for it.
- Live Trading, real exchange orders, signed requests, API keys, secrets, and real account state remain blocked.

# Database Recommendation

PostgreSQL is the primary persistence candidate for future implementation tasks.

Reasons:

- It supports durable local and later service-style storage without changing the data model.
- It has strong uniqueness constraints for duplicate-safe candle ingestion.
- It supports transactions for backfill, paper state, and backtest result writes.
- It supports JSON-style metadata fields for strategy configuration, run metadata, provider payloads, and ingestion status.
- It provides a natural path to later analytical indexing or time-series extensions if needed.

SQLite may remain useful only for prototypes, temporary local tests, or lightweight fixtures. It should not be the default target for the planned Binance backfill and WebSocket persistence tasks.

# Proposed Schemas

These are documentation-level schemas, not migrations or SQL.

## `candles`

Owner role: Market Data Provider.

Purpose:
Store normalized market candles with enough provider-specific metadata to resume ingestion, deduplicate data, and reconstruct Binance source rows when needed.

Fields:

| Field | Meaning |
| --- | --- |
| `id` | Internal surrogate identifier. |
| `source` | Data source, for example `binance_spot`. |
| `symbol` | Exchange symbol, for example `BTCUSDT`. |
| `interval` | Candle interval, initially `1m`. |
| `open_time` | Candle open timestamp in UTC. This maps to the standard candle `timestamp`. |
| `close_time` | Candle close timestamp in UTC from provider data. |
| `open` | First traded price in the interval. |
| `high` | Highest traded price in the interval. |
| `low` | Lowest traded price in the interval. |
| `close` | Last traded price in the interval. |
| `volume` | Base asset traded volume. |
| `quote_asset_volume` | Binance quote asset volume. |
| `number_of_trades` | Binance number of trades in the interval. |
| `taker_buy_base_asset_volume` | Binance taker buy base asset volume. |
| `taker_buy_quote_asset_volume` | Binance taker buy quote asset volume. |
| `is_closed` | Whether the candle is finalized. Historical backfill should store only closed candles. |
| `raw_payload` | Optional raw provider payload for audit/debugging. |
| `ingested_at` | Time this row was first ingested. |
| `updated_at` | Time this row was last updated. |

Uniqueness:

- Unique key: `source + symbol + interval + open_time`.
- This is required for idempotent historical backfill and WebSocket duplicate handling.

Timestamp semantics:

- `open_time` is the canonical candle timestamp used by the standard data contract.
- `close_time` is provider close time and must not replace `open_time` in strategy/backtest inputs.
- `ingested_at` records when local persistence first observed the row.
- `updated_at` records later corrections or duplicate-safe updates.

Notes:

- Strategy and backtest code should receive only `timestamp`, `open`, `high`, `low`, `close`, `volume`.
- Provider-specific Binance fields stay inside persistence and market-data boundaries.
- Open WebSocket candles should not be written as finalized `candles` rows unless a later task explicitly defines a separate staging table.

## `ingestion_checkpoints`

Owner role: Market Data Provider.

Purpose:
Track historical backfill and continuous ingestion progress.

Fields:

| Field | Meaning |
| --- | --- |
| `id` | Internal surrogate identifier. |
| `source` | Data source, for example `binance_spot`. |
| `symbol` | Exchange symbol. |
| `interval` | Candle interval. |
| `mode` | Ingestion mode, for example `historical_backfill` or `websocket`. |
| `last_open_time` | Latest finalized candle open time successfully persisted. |
| `last_close_time` | Latest finalized candle close time successfully persisted. |
| `last_event_time` | Latest provider event time observed, if available. |
| `status` | Current state such as `idle`, `running`, `failed`, or `completed`. |
| `error_message` | Last failure message, if any. |
| `metadata` | Optional provider/run metadata. |
| `created_at` | Row creation time. |
| `updated_at` | Last checkpoint update time. |

Uniqueness:

- Recommended unique key: `source + symbol + interval + mode`.

## `strategy_configs`

Owner role: Strategy.

Purpose:
Persist deterministic strategy settings used by backtests or paper sessions.

Fields:

| Field | Meaning |
| --- | --- |
| `id` | Internal surrogate identifier. |
| `strategy_name` | Strategy identifier, for example `RsiStrategy`. |
| `version` | Optional strategy implementation/config version. |
| `parameters` | Config values such as RSI window and thresholds. |
| `created_at` | Config creation time. |

Notes:

- For current RSI behavior, `parameters` should be able to represent `window`, `buy_threshold`, and `sell_threshold`.
- Strategy configs are metadata. Strategy code must not gain persistence responsibilities.

## `backtest_runs`

Owner role: Backtest Engine.

Purpose:
Persist one deterministic backtest execution.

Fields:

| Field | Meaning |
| --- | --- |
| `id` | Internal surrogate identifier. |
| `strategy_config_id` | Reference to the strategy configuration used, if persisted. |
| `source` | Candle source used by the run. |
| `symbol` | Symbol used by the run. |
| `interval` | Candle interval used by the run. |
| `start_time` | First candle open time included. |
| `end_time` | Last candle open time included. |
| `starting_cash` | Starting simulated cash. |
| `trade_quantity` | Fixed trade quantity for current basic backtester. |
| `status` | Run state such as `completed` or `failed`. |
| `metadata` | Optional run metadata. |
| `created_at` | Run creation time. |
| `completed_at` | Run completion time, if completed. |

## `backtest_trades`

Owner role: Backtest Engine.

Purpose:
Persist simulated trades generated during a backtest.

Fields:

| Field | Meaning |
| --- | --- |
| `id` | Internal surrogate identifier. |
| `backtest_run_id` | Owning backtest run. |
| `sequence` | Deterministic trade order within the run. |
| `timestamp` | Candle timestamp that generated the trade. |
| `signal` | `BUY` or `SELL`. |
| `price` | Simulated execution price. |
| `quantity` | Simulated quantity. |
| `cash_after` | Simulated cash after the trade. |
| `position_after` | Simulated position after the trade. |

Uniqueness:

- Recommended unique key: `backtest_run_id + sequence`.

## `backtest_results`

Owner role: Backtest Engine.

Purpose:
Persist deterministic summary output from a completed backtest.

Fields:

| Field | Meaning |
| --- | --- |
| `backtest_run_id` | Owning backtest run and primary identity. |
| `starting_cash` | Starting simulated cash. |
| `ending_cash` | Ending simulated cash. |
| `ending_position` | Ending simulated position. |
| `final_price` | Last candle close price, if available. |
| `final_equity` | Ending equity. |
| `total_return` | Deterministic total return. |
| `trade_count` | Number of simulated trades. |
| `buy_count` | Number of simulated BUY trades. |
| `sell_count` | Number of simulated SELL trades. |
| `created_at` | Result creation time. |

## `paper_sessions`

Owner role: Paper Execution.

Purpose:
Persist one simulated paper-trading session.

Fields:

| Field | Meaning |
| --- | --- |
| `id` | Internal surrogate identifier. |
| `name` | Optional human label. |
| `strategy_config_id` | Reference to strategy configuration, if used. |
| `starting_cash` | Starting simulated cash. |
| `status` | Session state such as `open`, `paused`, or `closed`. |
| `created_at` | Session creation time. |
| `closed_at` | Session close time, if closed. |
| `metadata` | Optional paper-only metadata. |

Notes:

- Paper sessions store simulated state only.
- Paper sessions must not represent real exchange account sessions.

## `paper_trades`

Owner role: Paper Execution.

Purpose:
Persist fake paper trades generated from strategy signals.

Fields:

| Field | Meaning |
| --- | --- |
| `id` | Internal surrogate identifier. |
| `paper_session_id` | Owning paper session. |
| `sequence` | Deterministic trade order within the session. |
| `symbol` | Traded symbol. |
| `signal` | `BUY` or `SELL`. |
| `quantity` | Simulated quantity. |
| `price` | Simulated price, if stateful paper execution is used. |
| `cash_after` | Simulated cash after the trade. |
| `position_after` | Simulated position after the trade. |
| `created_at` | Trade creation time. |

Uniqueness:

- Recommended unique key: `paper_session_id + sequence`.

## `paper_state_snapshots`

Owner role: Paper Execution.

Purpose:
Persist paper cash and positions after key simulated actions.

Fields:

| Field | Meaning |
| --- | --- |
| `id` | Internal surrogate identifier. |
| `paper_session_id` | Owning paper session. |
| `sequence` | Snapshot order within the session. |
| `cash_balance` | Simulated cash balance. |
| `positions` | Simulated positions by symbol. |
| `created_at` | Snapshot creation time. |

Notes:

- `positions` may be represented as structured metadata in the first persistence implementation, unless a later task decides to normalize positions into a separate table.
- This table must never store real exchange balances or real account state.

# Data Not Persisted Yet

The following should remain out of persistence until assigned by future tasks:

- Real exchange orders.
- Real account balances.
- API keys, secrets, signed request payloads, or `.env` values.
- Live-trading sessions.
- Scheduler runtime state beyond ingestion checkpoints.
- Dashboard-specific view state.
- Machine-learning artifacts, futures, leverage, or portfolio optimization data.

# Later Implementation Test Expectations

Future implementation tasks should add tests for:

- Candle mapping from Binance kline payloads to the accepted persistence fields.
- `source + symbol + interval + open_time` uniqueness.
- Idempotent duplicate candle writes.
- Open-time versus close-time handling.
- Closed-candle-only historical persistence.
- Standard candle projection back to `timestamp`, `open`, `high`, `low`, `close`, `volume`.
- Backtest run/trade/result persistence without changing strategy responsibilities.
- Paper session/trade/snapshot persistence with simulated state only.
- Safety checks proving no order endpoint, signed request, API-key handling, or live-trading behavior is introduced.

# Status Tracking

## Before Implementation

- [x] Read `AGENTS.md`.
- [x] Read `STATUS.md`.
- [x] Review current market data, backtesting, strategy, execution, and risk modules.
- [x] Confirm this task is documentation-only.

## After Implementation

- [x] Update `STATUS.md` only if project state, active task, blockers, or next step changes.
- [x] Leave implementation checklist items open until later tasks are approved.

# Acceptance Criteria

- A schema design document exists or this task document contains enough schema detail to guide later implementation.
- Binance candle persistence fields and uniqueness rules are documented.
- Future persistence candidates are listed with ownership boundaries.
- The document clearly forbids live order execution and real exchange order storage in this phase.
- No application code, Docker file, migration, or dependency is added.

# Required Tests

## Unit Tests

- None required because this is a documentation task.

## Integration Tests

- None required.

## Contract Tests

- Later implementation must add tests for candle uniqueness, timestamp normalization, and provider-field mapping.

## Safety Tests

- Verify no application code, live-trading code, real order endpoint, API-key handling, `.env` file, or Docker runtime file is added in this task.

# Review Checklist

- Scope respected.
- Requirement matched.
- Role ownership respected.
- Architecture boundaries respected.
- Data contract documented.
- No hardcoded secrets.
- No real order execution.
- No unnecessary abstractions.

# Verification

Documentation-only verification:

```bash
git diff --check
```

# Completion Summary Required

- files changed
- documentation summary
- tests run
- known limitations
- recommended next task
