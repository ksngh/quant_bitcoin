from __future__ import annotations

import socket

import pandas as pd
import pytest

from quant_bitcoin.market_data.csv_provider import (
    CsvCandleDataProvider,
    STANDARD_CANDLE_COLUMNS,
)


def test_valid_csv_returns_standard_candle_data_sorted_by_timestamp(tmp_path):
    csv_path = tmp_path / "candles.csv"
    csv_path.write_text(
        " Timestamp ,Open,High,Low,Close,Volume,ignored\n"
        "2024-01-01 00:02:00,43000.5,43100,42950,43050,12.5,drop-me\n"
        "2024-01-01 00:00:00,42000,42500,41900,42400,10,drop-me\n"
        "2024-01-01 00:01:00,42400,43000,42350,42900,11,drop-me\n"
    )

    candles = CsvCandleDataProvider(csv_path).load()

    assert list(candles.columns) == list(STANDARD_CANDLE_COLUMNS)
    assert candles["timestamp"].tolist() == [
        pd.Timestamp("2024-01-01 00:00:00"),
        pd.Timestamp("2024-01-01 00:01:00"),
        pd.Timestamp("2024-01-01 00:02:00"),
    ]
    assert candles["open"].tolist() == [42000.0, 42400.0, 43000.5]
    assert candles["high"].tolist() == [42500, 43000, 43100]
    assert candles["low"].tolist() == [41900, 42350, 42950]
    assert candles["close"].tolist() == [42400, 42900, 43050]
    assert candles["volume"].tolist() == [10.0, 11.0, 12.5]


def test_missing_required_column_is_rejected(tmp_path):
    csv_path = tmp_path / "missing_volume.csv"
    csv_path.write_text(
        "timestamp,open,high,low,close\n"
        "2024-01-01 00:00:00,42000,42500,41900,42400\n"
    )

    with pytest.raises(ValueError, match="missing required columns: volume"):
        CsvCandleDataProvider(csv_path).load()


@pytest.mark.parametrize(
    ("column", "bad_value"),
    [
        ("open", "not-a-number"),
        ("high", "not-a-number"),
        ("low", "not-a-number"),
        ("close", "not-a-number"),
        ("volume", "not-a-number"),
    ],
)
def test_numeric_columns_are_rejected_when_values_are_not_numeric(
    tmp_path, column, bad_value
):
    csv_path = tmp_path / f"bad_{column}.csv"
    row = {
        "timestamp": "2024-01-01 00:00:00",
        "open": "42000",
        "high": "42500",
        "low": "41900",
        "close": "42400",
        "volume": "10",
    }
    row[column] = bad_value
    csv_path.write_text(
        "timestamp,open,high,low,close,volume\n"
        f"{row['timestamp']},{row['open']},{row['high']},{row['low']},{row['close']},{row['volume']}\n"
    )

    with pytest.raises(
        ValueError, match=f"non-numeric values in column: {column}"
    ):
        CsvCandleDataProvider(csv_path).load()


def test_invalid_timestamp_is_rejected(tmp_path):
    csv_path = tmp_path / "bad_timestamp.csv"
    csv_path.write_text(
        "timestamp,open,high,low,close,volume\n"
        "not-a-timestamp,42000,42500,41900,42400,10\n"
    )

    with pytest.raises(ValueError, match="invalid timestamp values"):
        CsvCandleDataProvider(csv_path).load()


def test_csv_provider_does_not_open_network_connections(tmp_path, monkeypatch):
    csv_path = tmp_path / "candles.csv"
    csv_path.write_text(
        "timestamp,open,high,low,close,volume\n"
        "2024-01-01 00:00:00,42000,42500,41900,42400,10\n"
    )

    def fail_socket_creation(*args, **kwargs):
        raise AssertionError("CSV provider must not create network sockets")

    monkeypatch.setattr(socket, "socket", fail_socket_creation)

    candles = CsvCandleDataProvider(csv_path).load()

    assert list(candles.columns) == list(STANDARD_CANDLE_COLUMNS)
