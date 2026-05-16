"""Command-line runner for PostgreSQL-backed RSI backtests.

This CLI is intentionally limited to local backtest wiring: it reads already
persisted standard candle data from PostgreSQL, runs the existing RSI strategy
through the existing basic backtester, and prints a deterministic JSON summary.
It does not fetch Binance data, place orders, sign requests, or call exchange
account APIs.
"""

from __future__ import annotations

import argparse
import json
import os
from collections.abc import Callable, Sequence
from dataclasses import asdict
from datetime import datetime, timezone
from typing import Any

from quant_bitcoin.backtesting.basic import BacktestResult, BasicBacktester
from quant_bitcoin.market_data import PostgresCandleDataProvider
from quant_bitcoin.persistence import SOURCE_BINANCE_SPOT
from quant_bitcoin.strategies import RsiStrategy

DEFAULT_DATABASE_URL = (
    "postgresql://quant_bitcoin:quant_bitcoin_dev@localhost:5432/quant_bitcoin"
)
DEFAULT_SYMBOL = "BTCUSDT"
DEFAULT_INTERVAL = "1m"
DEFAULT_STARTING_CASH = 10_000.0
DEFAULT_TRADE_QUANTITY = 0.01
DEFAULT_RSI_WINDOW = 14
DEFAULT_RSI_BUY_THRESHOLD = 30.0
DEFAULT_RSI_SELL_THRESHOLD = 70.0

ProviderFactory = Callable[..., Any]
StrategyFactory = Callable[..., Any]
BacktesterFactory = Callable[..., Any]


def main(
    argv: Sequence[str] | None = None,
    *,
    provider_factory: ProviderFactory = PostgresCandleDataProvider.from_database_url,
    strategy_factory: StrategyFactory = RsiStrategy,
    backtester_factory: BacktesterFactory = BasicBacktester,
) -> int:
    """Run the PostgreSQL RSI backtest CLI and return a process exit code."""

    args = build_parser().parse_args(argv)
    provider = provider_factory(
        args.database_url,
        source=args.source,
        symbol=args.symbol,
        interval=args.interval,
        start_time=args.start_time,
        end_time=args.end_time,
    )
    candles = provider.load()

    strategy = strategy_factory(
        window=args.rsi_window,
        buy_threshold=args.rsi_buy_threshold,
        sell_threshold=args.rsi_sell_threshold,
    )
    backtester = backtester_factory(
        starting_cash=args.starting_cash,
        trade_quantity=args.trade_quantity,
    )
    result = backtester.run(candles, strategy)

    _print_json(
        build_output(
            result,
            candle_count=len(candles),
            source=args.source,
            symbol=args.symbol,
            interval=args.interval,
            start_time=args.start_time,
            end_time=args.end_time,
            rsi_window=args.rsi_window,
            rsi_buy_threshold=args.rsi_buy_threshold,
            rsi_sell_threshold=args.rsi_sell_threshold,
        )
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""

    parser = argparse.ArgumentParser(
        prog="quant-bitcoin-postgres-backtest",
        description="Run an RSI backtest from candles already stored in PostgreSQL.",
    )
    parser.add_argument(
        "--database-url",
        default=os.environ.get("DATABASE_URL", DEFAULT_DATABASE_URL),
        help="PostgreSQL connection URL containing previously stored candles",
    )
    parser.add_argument(
        "--source",
        default=os.environ.get("CANDLE_SOURCE", SOURCE_BINANCE_SPOT),
        help="stored candle source to read",
    )
    parser.add_argument(
        "--symbol",
        default=os.environ.get("SYMBOL", DEFAULT_SYMBOL),
        help="stored candle symbol to read",
    )
    parser.add_argument(
        "--interval",
        default=os.environ.get("INTERVAL", DEFAULT_INTERVAL),
        help="stored candle interval to read",
    )
    parser.add_argument(
        "--start-time",
        type=_optional_timestamp,
        default=_env_optional_timestamp("BACKTEST_START_TIME"),
        help="optional UTC ISO-8601 datetime for the first candle open time",
    )
    parser.add_argument(
        "--end-time",
        type=_optional_timestamp,
        default=_env_optional_timestamp("BACKTEST_END_TIME"),
        help="optional UTC ISO-8601 datetime for the last candle open time",
    )
    parser.add_argument(
        "--starting-cash",
        type=_non_negative_float,
        default=_env_non_negative_float(
            "BACKTEST_STARTING_CASH", DEFAULT_STARTING_CASH
        ),
        help="starting cash for the simulated backtest",
    )
    parser.add_argument(
        "--trade-quantity",
        type=_positive_float,
        default=_env_positive_float("BACKTEST_TRADE_QUANTITY", DEFAULT_TRADE_QUANTITY),
        help="fixed simulated quantity per backtest trade",
    )
    parser.add_argument(
        "--rsi-window",
        type=_positive_int,
        default=_env_positive_int("BACKTEST_RSI_WINDOW", DEFAULT_RSI_WINDOW),
        help="RSI rolling window",
    )
    parser.add_argument(
        "--rsi-buy-threshold",
        type=_threshold_float,
        default=_env_threshold_float(
            "BACKTEST_RSI_BUY_THRESHOLD", DEFAULT_RSI_BUY_THRESHOLD
        ),
        help="RSI value at or below which the strategy returns BUY",
    )
    parser.add_argument(
        "--rsi-sell-threshold",
        type=_threshold_float,
        default=_env_threshold_float(
            "BACKTEST_RSI_SELL_THRESHOLD", DEFAULT_RSI_SELL_THRESHOLD
        ),
        help="RSI value at or above which the strategy returns SELL",
    )
    return parser


def build_output(
    result: BacktestResult,
    *,
    candle_count: int,
    source: str,
    symbol: str,
    interval: str,
    start_time: datetime | None,
    end_time: datetime | None,
    rsi_window: int,
    rsi_buy_threshold: float,
    rsi_sell_threshold: float,
) -> dict[str, Any]:
    """Return a deterministic JSON-serializable backtest output object."""

    return {
        "candle_count": candle_count,
        "input": {
            "source": source,
            "symbol": symbol,
            "interval": interval,
            "start_time": _serialize_optional_datetime(start_time),
            "end_time": _serialize_optional_datetime(end_time),
        },
        "strategy": {
            "name": "RSI",
            "window": rsi_window,
            "buy_threshold": rsi_buy_threshold,
            "sell_threshold": rsi_sell_threshold,
        },
        "summary": asdict(result.summary),
        "trades": [
            {
                "timestamp": _serialize_datetime(trade.timestamp.to_pydatetime()),
                "signal": trade.signal.value,
                "price": trade.price,
                "quantity": trade.quantity,
                "cash_after": trade.cash_after,
                "position_after": trade.position_after,
            }
            for trade in result.trades
        ],
    }


def _optional_timestamp(value: str) -> datetime | None:
    if value == "":
        return None
    normalized = value.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as error:
        raise argparse.ArgumentTypeError(
            "timestamp must be an ISO-8601 datetime"
        ) from error
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _positive_int(value: str) -> int:
    integer = int(value)
    if integer < 1:
        raise argparse.ArgumentTypeError("value must be a positive integer")
    return integer


def _positive_float(value: str) -> float:
    number = float(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("value must be greater than zero")
    return number


def _non_negative_float(value: str) -> float:
    number = float(value)
    if number < 0:
        raise argparse.ArgumentTypeError("value must be non-negative")
    return number


def _threshold_float(value: str) -> float:
    number = float(value)
    if not 0 <= number <= 100:
        raise argparse.ArgumentTypeError("RSI threshold must be between 0 and 100")
    return number


def _env_optional_timestamp(name: str) -> datetime | None:
    value = os.environ.get(name)
    if value is None:
        return None
    return _optional_timestamp(value)


def _env_positive_int(name: str, default: int) -> int:
    value = os.environ.get(name)
    if value is None:
        return default
    return _positive_int(value)


def _env_positive_float(name: str, default: float) -> float:
    value = os.environ.get(name)
    if value is None:
        return default
    return _positive_float(value)


def _env_non_negative_float(name: str, default: float) -> float:
    value = os.environ.get(name)
    if value is None:
        return default
    return _non_negative_float(value)


def _env_threshold_float(name: str, default: float) -> float:
    value = os.environ.get(name)
    if value is None:
        return default
    return _threshold_float(value)


def _serialize_optional_datetime(value: datetime | None) -> str | None:
    if value is None:
        return None
    return _serialize_datetime(value)


def _serialize_datetime(value: datetime) -> str:
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _print_json(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
