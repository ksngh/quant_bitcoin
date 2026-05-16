from __future__ import annotations

import json
import socket
from datetime import datetime, timezone
from typing import Any

import pandas as pd
import pytest

from quant_bitcoin.backtesting import BasicBacktester
from quant_bitcoin.backtesting import postgres_runner_cli
from quant_bitcoin.strategies import RsiStrategy


class FakeProvider:
    def __init__(self, candles: pd.DataFrame) -> None:
        self.candles = candles
        self.load_calls = 0

    def load(self) -> pd.DataFrame:
        self.load_calls += 1
        return self.candles


def make_candles(closes: list[float]) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "timestamp": pd.date_range(
                "2024-01-01T00:00:00Z", periods=len(closes), freq="min"
            ),
            "open": closes,
            "high": [close + 1 for close in closes],
            "low": [close - 1 for close in closes],
            "close": closes,
            "volume": [1.0] * len(closes),
        }
    )


def test_parser_accepts_postgres_backtest_configuration():
    args = postgres_runner_cli.build_parser().parse_args(
        [
            "--database-url",
            "postgresql://example/test",
            "--source",
            "binance_spot",
            "--symbol",
            "ETHUSDT",
            "--interval",
            "5m",
            "--start-time",
            "2024-01-01T00:00:00Z",
            "--end-time",
            "2024-01-02T00:00:00+00:00",
            "--starting-cash",
            "2500",
            "--trade-quantity",
            "0.25",
            "--rsi-window",
            "7",
            "--rsi-buy-threshold",
            "20",
            "--rsi-sell-threshold",
            "80",
        ]
    )

    assert args.database_url == "postgresql://example/test"
    assert args.source == "binance_spot"
    assert args.symbol == "ETHUSDT"
    assert args.interval == "5m"
    assert args.start_time == datetime(2024, 1, 1, tzinfo=timezone.utc)
    assert args.end_time == datetime(2024, 1, 2, tzinfo=timezone.utc)
    assert args.starting_cash == 2500
    assert args.trade_quantity == 0.25
    assert args.rsi_window == 7
    assert args.rsi_buy_threshold == 20
    assert args.rsi_sell_threshold == 80


def test_postgres_backtest_cli_wires_provider_strategy_and_backtester(capsys):
    calls: dict[str, Any] = {}
    provider = FakeProvider(make_candles([100, 95, 90, 85, 80]))

    def provider_factory(database_url: str, **kwargs: Any) -> FakeProvider:
        calls["provider"] = {"database_url": database_url, **kwargs}
        return provider

    exit_code = postgres_runner_cli.main(
        [
            "--database-url",
            "postgresql://example/test",
            "--source",
            "binance_spot",
            "--symbol",
            "BTCUSDT",
            "--interval",
            "1m",
            "--start-time",
            "2024-01-01T00:00:00Z",
            "--end-time",
            "2024-01-01T00:04:00Z",
            "--starting-cash",
            "1000",
            "--trade-quantity",
            "1",
            "--rsi-window",
            "2",
            "--rsi-buy-threshold",
            "30",
            "--rsi-sell-threshold",
            "70",
        ],
        provider_factory=provider_factory,
        strategy_factory=RsiStrategy,
        backtester_factory=BasicBacktester,
    )

    output = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert provider.load_calls == 1
    assert calls["provider"] == {
        "database_url": "postgresql://example/test",
        "source": "binance_spot",
        "symbol": "BTCUSDT",
        "interval": "1m",
        "start_time": datetime(2024, 1, 1, tzinfo=timezone.utc),
        "end_time": datetime(2024, 1, 1, 0, 4, tzinfo=timezone.utc),
    }
    assert output["candle_count"] == 5
    assert output["input"] == {
        "source": "binance_spot",
        "symbol": "BTCUSDT",
        "interval": "1m",
        "start_time": "2024-01-01T00:00:00Z",
        "end_time": "2024-01-01T00:04:00Z",
    }
    assert output["strategy"] == {
        "name": "RSI",
        "window": 2,
        "buy_threshold": 30.0,
        "sell_threshold": 70.0,
    }
    assert output["summary"]["starting_cash"] == 1000.0
    assert output["summary"]["trade_count"] == 1
    assert output["trades"] == [
        {
            "cash_after": 910.0,
            "position_after": 1.0,
            "price": 90.0,
            "quantity": 1.0,
            "signal": "BUY",
            "timestamp": "2024-01-01T00:02:00Z",
        }
    ]


def test_postgres_backtest_cli_reports_empty_candles(capsys):
    empty_candles = pd.DataFrame(
        columns=["timestamp", "open", "high", "low", "close", "volume"]
    )

    exit_code = postgres_runner_cli.main(
        [],
        provider_factory=lambda database_url, **kwargs: FakeProvider(empty_candles),
    )

    output = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert output["candle_count"] == 0
    assert output["summary"] == {
        "buy_count": 0,
        "ending_cash": 10000.0,
        "ending_position": 0.0,
        "final_equity": 10000.0,
        "final_price": None,
        "sell_count": 0,
        "starting_cash": 10000.0,
        "total_return": 0.0,
        "trade_count": 0,
    }
    assert output["trades"] == []


def test_postgres_backtest_cli_does_not_open_network_connections(monkeypatch, capsys):
    def fail_socket_creation(*args: Any, **kwargs: Any) -> None:
        raise AssertionError("PostgreSQL backtest tests must not open network sockets")

    monkeypatch.setattr(socket, "socket", fail_socket_creation)

    exit_code = postgres_runner_cli.main(
        [],
        provider_factory=lambda database_url, **kwargs: FakeProvider(make_candles([100])),
    )

    assert exit_code == 0
    assert json.loads(capsys.readouterr().out)["candle_count"] == 1


def test_postgres_backtest_cli_rejects_invalid_thresholds():
    with pytest.raises(SystemExit):
        postgres_runner_cli.build_parser().parse_args(["--rsi-buy-threshold", "-1"])
