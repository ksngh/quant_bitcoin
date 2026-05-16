# quant_bitcoin

`quant_bitcoin` is a small Python project for Bitcoin quantitative-trading experiments. The current implementation focuses on offline and paper-only workflows: candle data loading, standard candle normalization, RSI signals, basic historical backtesting, paper trade recording, Binance public historical candle downloading, and basic paper risk checks.

> **Safety status:** live trading and real Binance order execution are intentionally blocked. This project does not place real orders, does not sign exchange requests, and does not store or load API keys.

## Current scope

Implemented components:

- **Market data contract** using the standard candle fields `timestamp`, `open`, `high`, `low`, `close`, and `volume`.
- **CSV candle provider** for loading local CSV files into the standard candle schema.
- **Binance candle downloader** for public historical spot klines only; it normalizes responses to the standard candle schema and rejects order endpoints.
- **RSI strategy** that returns `BUY`, `SELL`, or `HOLD` signals from standard candle data.
- **Basic backtester** for a simple long-only, fixed-quantity historical simulation.
- **Paper trader** for in-memory fake trade recording and paper cash/position updates.
- **Paper risk checker** for deterministic cash and position checks before paper trades.
- **PostgreSQL candle persistence** for Binance spot candle storage, restartable historical backfill, and public WebSocket closed-candle ingestion.

Out of scope unless a future approved task explicitly asks for it:

- Live trading or real order execution.
- API keys, signed requests, or tracked `.env` files.
- Futures, leverage, portfolio optimization, dashboards, schedulers, FastAPI, Streamlit, and machine learning.
- Additional databases or Dockerized application services beyond the Task 014 local PostgreSQL developer service.

## Project layout

```text
quant_bitcoin/
  backtesting/        Basic backtest engine and result models.
  execution/          Paper-only execution simulation.
  market_data/        CSV provider, Binance public downloader, backfill, and WebSocket ingestion.
  persistence/        PostgreSQL candle repository and ingestion checkpoint storage.
  risk/               Paper-only risk checks.
  strategies/         RSI strategy and signal contract.
docs/                 Architecture, data contract, workflow, and decision docs.
tasks/                Task definitions and completion criteria.
tests/                Unit, contract, and safety tests.
```

## Requirements

- Python 3.10 or newer.
- `pandas` for data handling.
- `psycopg` for PostgreSQL persistence.
- `websockets` for optional live public WebSocket connections.
- `pytest` for tests.

The package metadata is defined in `pyproject.toml`.

## Installation

From the repository root, create and activate a virtual environment, then install the project with test dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[test]'
```

## Local PostgreSQL for candle persistence

Task 014 adds local PostgreSQL support for market-data persistence only. The
Docker Compose service uses non-secret development defaults and loads the
accepted candle schema from `db/init/001_market_data.sql`. Do not commit `.env`
files; override `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, or
`POSTGRES_PORT` in your shell when needed.

Start local PostgreSQL from the repository root:

```bash
docker compose up -d postgres
```

The matching development database URL is:

```text
postgresql://quant_bitcoin:quant_bitcoin_dev@localhost:5432/quant_bitcoin
```

Optional PostgreSQL integration tests use `QUANT_BITCOIN_TEST_DATABASE_URL`. The
ordinary unit test suite does not require Docker, a running PostgreSQL server, or
real Binance availability; network calls are mocked in ordinary tests.

Docker Compose is optional local developer verification only. If Docker is not
available in an environment, skip runtime startup there; it can be verified later
in a Docker-capable local environment.

### Backfill public Binance 1-minute candles

The recommended local path is to run the packaged CLI from the repository root
after installing the project and starting local PostgreSQL:

```bash
python -m pip install -e '.[test]'
docker compose up -d postgres
quant-bitcoin-binance-backfill
```

With the default Docker Compose database, the CLI connects to:

```text
postgresql://quant_bitcoin:quant_bitcoin_dev@localhost:5432/quant_bitcoin
```

The default command initializes the PostgreSQL schema if needed, backfills
`BTCUSDT` `1m` candles from the latest stored candle or Binance's earliest
available candle, persists only closed candles, and prints a JSON summary such as
`stored_candles` and `pages_fetched`. Re-running the command is safe because the
repository writes candles by the duplicate-safe
`source + symbol + interval + open_time` uniqueness rule.

Common bounded examples:

```bash
# Backfill a specific UTC date range.
quant-bitcoin-binance-backfill \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-02T00:00:00Z

# Use an explicit database URL and skip schema initialization if already managed.
quant-bitcoin-binance-backfill \
  --database-url postgresql://quant_bitcoin:quant_bitcoin_dev@localhost:5432/quant_bitcoin \
  --no-initialize-schema
```

Useful CLI options and matching environment variables:

| Option | Environment variable | Default |
| --- | --- | --- |
| `--database-url` | `DATABASE_URL` | Local Docker Compose PostgreSQL URL. |
| `--symbol` | `SYMBOL` | `BTCUSDT` |
| `--interval` | `INTERVAL` | `1m` |
| `--start-time` | `BACKFILL_START_TIME` | Resume after latest stored candle, or start from earliest available candle. |
| `--end-time` | `BACKFILL_END_TIME` | Latest closed candle at runtime. |
| `--limit` | `BACKFILL_LIMIT` | `1000` |
| `--base-url` | `BINANCE_MARKET_DATA_BASE_URL` | Binance public market-data REST base URL. |
| `--timeout-seconds` | `BACKFILL_TIMEOUT_SECONDS` | `10.0` |
| `--max-retries` | `BACKFILL_MAX_RETRIES` | `3` |

`--start-time` and `--end-time` accept UTC ISO-8601 values such as
`2024-01-01T00:00:00Z` or millisecond timestamps. Do not commit `.env` files;
set overrides in your shell or local process manager instead. The backfill uses
Binance public spot kline data only and does not require API keys, signed
requests, or order endpoints.

The same behavior can be invoked from Python when embedding the workflow:

```python
from quant_bitcoin.market_data import BinanceHistoricalBackfiller
from quant_bitcoin.persistence import PostgresCandleRepository

repository = PostgresCandleRepository(
    "postgresql://quant_bitcoin:quant_bitcoin_dev@localhost:5432/quant_bitcoin"
)
repository.initialize_schema()

result = BinanceHistoricalBackfiller(repository).run(symbol="BTCUSDT", interval="1m")
print(result.stored_candles)
```

## Run an RSI backtest from PostgreSQL candles

After PostgreSQL already contains closed candles, run the short packaged
backtest command from the repository root:

```bash
quant-bitcoin-postgres-backtest
```

The command reads candles through `PostgresCandleDataProvider`, runs the
existing `RsiStrategy` with `BasicBacktester`, saves the completed simulated
backtest result to PostgreSQL, and prints deterministic JSON containing the
input stream, strategy parameters, summary, simulated trades, and saved
`backtest_run_id`. It does not call Binance, place real orders, use API keys,
or call exchange account endpoints.

Saved runs use the graph-ready Task 021 schema in `strategy_configs`,
`backtest_runs`, `backtest_results`, `backtest_trades`, and
`backtest_graph_points`. The write is transactional for each run: strategy
metadata, run metadata, summary metrics, deterministic trade rows, and ordered
graph points are committed together or rolled back together. Re-running the same
deterministic backtest replaces the prior saved rows for the same `run_key`.
Use `--no-persist` only when you want to inspect stdout JSON without saving
simulated result rows.

If PostgreSQL is empty, populate it first with the accepted Task 014 backfill
workflow:

```bash
docker compose up -d postgres
quant-bitcoin-binance-backfill \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-02T00:00:00Z
quant-bitcoin-postgres-backtest \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-02T00:00:00Z
```

Common backtest options and matching environment variables:

| Option | Environment variable | Default |
| --- | --- | --- |
| `--database-url` | `DATABASE_URL` | Local Docker Compose PostgreSQL URL. |
| `--source` | `CANDLE_SOURCE` | `binance_spot` |
| `--symbol` | `SYMBOL` | `BTCUSDT` |
| `--interval` | `INTERVAL` | `1m` |
| `--start-time` | `BACKTEST_START_TIME` | No lower bound. |
| `--end-time` | `BACKTEST_END_TIME` | No upper bound. |
| `--starting-cash` | `BACKTEST_STARTING_CASH` | `10000.0` |
| `--trade-quantity` | `BACKTEST_TRADE_QUANTITY` | `0.01` |
| `--rsi-window` | `BACKTEST_RSI_WINDOW` | `14` |
| `--rsi-buy-threshold` | `BACKTEST_RSI_BUY_THRESHOLD` | `30.0` |
| `--rsi-sell-threshold` | `BACKTEST_RSI_SELL_THRESHOLD` | `70.0` |
| `--no-persist` | None | Persist simulated results by default. |

`--start-time` and `--end-time` accept UTC ISO-8601 values such as
`2024-01-01T00:00:00Z`. Do not commit `.env` files; set overrides in your shell
or local process manager instead.

### Ingest public Binance WebSocket closed candles

```python
import asyncio

from quant_bitcoin.market_data import BinanceWebSocketCandleIngestor
from quant_bitcoin.persistence import PostgresCandleRepository

repository = PostgresCandleRepository(
    "postgresql://quant_bitcoin:quant_bitcoin_dev@localhost:5432/quant_bitcoin"
)
repository.initialize_schema()

asyncio.run(
    BinanceWebSocketCandleIngestor(repository).run(symbol="BTCUSDT", interval="1m")
)
```

The WebSocket ingestor subscribes to Binance public spot kline streams, persists
only closed `BTCUSDT` `1m` candles, and relies on the PostgreSQL duplicate-safe
`source + symbol + interval + open_time` uniqueness rule. It does not perform
historical REST gap fill on startup; run the Task 014 backfill first whenever
historical completeness after downtime is required. Ordinary tests mock the
WebSocket connector and do not require real Binance availability.

## Running tests

```bash
pytest
```

The test suite is expected to run without real API keys and without calling real exchange order endpoints.

## Standard candle schema

All strategy and backtest code expects standard candle data with these columns:

| Column | Meaning |
| --- | --- |
| `timestamp` | Candle open time. |
| `open` | First traded price in the candle interval. |
| `high` | Highest traded price in the candle interval. |
| `low` | Lowest traded price in the candle interval. |
| `close` | Last traded price in the candle interval. |
| `volume` | Traded volume in the candle interval. |

Rows must be sorted by `timestamp` ascending. Price and volume fields must be numeric.

## Usage examples

### Load candles from CSV

```python
from quant_bitcoin.market_data import CsvCandleDataProvider

provider = CsvCandleDataProvider("data/btcusdt_1m.csv")
candles = provider.load()
```

The CSV provider normalizes column names and returns only the standard candle fields.

### Load candles from PostgreSQL for backtesting

After PostgreSQL has been populated by the Binance backfill or WebSocket
ingestion workflow, use `PostgresCandleDataProvider` to read stored `candles`
rows into the same standard candle schema used by CSV-backed backtests:

```python
from datetime import datetime, timezone

from quant_bitcoin.backtesting import BasicBacktester
from quant_bitcoin.market_data import PostgresCandleDataProvider
from quant_bitcoin.persistence import PostgresCandleRepository
from quant_bitcoin.strategies import RsiStrategy

repository = PostgresCandleRepository(
    "postgresql://quant_bitcoin:quant_bitcoin_dev@localhost:5432/quant_bitcoin"
)
provider = PostgresCandleDataProvider(
    repository,
    symbol="BTCUSDT",
    interval="1m",
    start_time=datetime(2024, 1, 1, tzinfo=timezone.utc),
    end_time=datetime(2024, 1, 2, tzinfo=timezone.utc),
)
candles = provider.load()

strategy = RsiStrategy(window=14)
result = BasicBacktester(starting_cash=10_000, trade_quantity=0.01).run(
    candles, strategy
)
print(result.summary)
```

The PostgreSQL provider maps `candles.open_time` to `timestamp`, returns only
`timestamp`, `open`, `high`, `low`, `close`, and `volume`, and sorts rows by
`timestamp` ascending before backtesting.

### Generate an RSI signal

```python
from quant_bitcoin.strategies import RsiStrategy

strategy = RsiStrategy(window=14, buy_threshold=30.0, sell_threshold=70.0)
signal = strategy.generate_signal(candles)
```

The RSI strategy consumes standard candle data only. It does not fetch data, decide quantity, or place orders.

### Run a basic backtest

```python
from quant_bitcoin.backtesting import BasicBacktester
from quant_bitcoin.strategies import RsiStrategy

strategy = RsiStrategy(window=14, buy_threshold=30.0, sell_threshold=70.0)
backtester = BasicBacktester(starting_cash=10_000.0, trade_quantity=0.01)
result = backtester.run(candles, strategy)

print(result.summary.final_equity)
print(result.summary.total_return)
```

The basic backtester is intentionally small: it runs a long-only, fixed-quantity simulation and does not model fees, slippage, optimization, or live execution.

### Record paper trades

```python
from quant_bitcoin.execution import PaperTrader
from quant_bitcoin.strategies import Signal

trader = PaperTrader(cash_balance=1_000.0)
trade = trader.apply_signal(
    symbol="BTCUSDT",
    signal=Signal.BUY,
    quantity=0.01,
    price=50_000.0,
)
```

`PaperTrader` records fake trades and updates local paper state only. It never calls exchange APIs.

### Check paper risk before a paper trade

```python
from quant_bitcoin.risk import PaperRiskChecker
from quant_bitcoin.strategies import Signal

checker = PaperRiskChecker()
decision = checker.check(
    symbol="BTCUSDT",
    signal=Signal.BUY,
    quantity=0.01,
    price=50_000.0,
    cash_balance=1_000.0,
    current_position=0.0,
)

if decision.approved:
    print("paper trade approved")
else:
    print(decision.reason)
```

The risk checker is paper-only and deterministic. It does not mutate state or call exchanges.

### Download public Binance historical candles

```python
from quant_bitcoin.market_data import BinanceCandleDownloader

downloader = BinanceCandleDownloader()
candles = downloader.fetch_historical_candles(
    symbol="BTCUSDT",
    interval="1m",
    limit=100,
)
```

The downloader uses Binance public kline data only and returns the standard candle schema. It must not be used for order execution.

## Safety rules

This repository is designed to keep strategy research and paper workflows separate from live execution.

- Strategy code returns signals only; it must not place orders.
- Market-data code may fetch or load candles; it must not execute trades.
- Backtests simulate historical execution only; they must not call live exchange order APIs.
- Paper trading records fake trades only; it must not call real exchange order APIs.
- Binance downloading, backfill, and WebSocket ingestion are limited to public candle data.
- Live trading remains blocked until a future human-approved task documents credential handling, sandbox/testnet policy, endpoint allowlist, kill switch behavior, and safety tests.

## Documentation

Important project documents:

- `AGENTS.md` — working rules and project safety constraints.
- `STATUS.md` — current phase, blockers, and next-step ledger.
- `docs/04_DATA_CONTRACT.md` — standard candle data contract.
- `docs/03_ARCHITECTURE_RULES.md` — role ownership and architecture boundaries.
- `docs/09_DECISIONS.md` — accepted architecture decisions.
- `tasks/012_LIVE_TRADING_IMPLEMENTATION_BLOCKER.md` — current live-trading blocker.

## Development notes

Before adding implementation changes:

1. Read `AGENTS.md` and `STATUS.md`.
2. Read the relevant task document under `tasks/`.
3. Keep changes small and within the assigned role boundary.
4. Add or update tests for implementation behavior.
5. Run `pytest` when possible.
6. Perform the Codex self-review checklist in `reviews/CODEX_SELF_REVIEW.md`.
