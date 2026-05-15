from __future__ import annotations

import os
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any

import pytest

from quant_bitcoin.persistence import (
    CANDLE_TABLE_COLUMNS,
    SCHEMA_SQL,
    IngestionCheckpoint,
    PersistedCandle,
    PostgresCandleRepository,
)
from quant_bitcoin.persistence.postgres import (
    SELECT_STANDARD_CANDLES_BASE_SQL,
    UPSERT_CANDLE_SQL,
)


EXPECTED_CANDLE_COLUMNS = (
    "source",
    "symbol",
    "interval",
    "open_time",
    "close_time",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "quote_asset_volume",
    "number_of_trades",
    "taker_buy_base_asset_volume",
    "taker_buy_quote_asset_volume",
    "is_closed",
    "raw_payload",
)




class FakeResult:
    def __init__(self, rows: list[dict[str, Any]]) -> None:
        self.rows = rows

    def fetchall(self) -> list[dict[str, Any]]:
        return self.rows


class FakeConnection:
    def __init__(self, rows: list[dict[str, Any]]) -> None:
        self.rows = rows
        self.executed_query: str | None = None
        self.executed_params: dict[str, Any] | None = None

    def __enter__(self) -> "FakeConnection":
        return self

    def __exit__(self, *args: object) -> None:
        return None

    def execute(self, query: str, params: dict[str, Any]) -> FakeResult:
        self.executed_query = query
        self.executed_params = params
        return FakeResult(self.rows)

def persisted_candle(open_price: str = "42000") -> PersistedCandle:
    return PersistedCandle(
        source="binance_spot",
        symbol="BTCUSDT",
        interval="1m",
        open_time=datetime(2024, 1, 1, 0, 0, tzinfo=timezone.utc),
        close_time=datetime(2024, 1, 1, 0, 0, 59, 999000, tzinfo=timezone.utc),
        open=Decimal(open_price),
        high=Decimal("42100"),
        low=Decimal("41900"),
        close=Decimal("42050"),
        volume=Decimal("12.5"),
        quote_asset_volume=Decimal("525625"),
        number_of_trades=123,
        taker_buy_base_asset_volume=Decimal("6.1"),
        taker_buy_quote_asset_volume=Decimal("256405"),
        is_closed=True,
        raw_payload=["raw"],
    )


def test_candle_contract_columns_match_task_013_schema():
    assert CANDLE_TABLE_COLUMNS == EXPECTED_CANDLE_COLUMNS
    for column in EXPECTED_CANDLE_COLUMNS:
        assert column in SCHEMA_SQL


def test_schema_enforces_accepted_uniqueness_rules():
    assert "UNIQUE (source, symbol, interval, open_time)" in SCHEMA_SQL
    assert "UNIQUE (source, symbol, interval, mode)" in SCHEMA_SQL


def test_standard_candle_select_uses_open_time_timestamp_mapping():
    assert "SELECT open_time AS timestamp, open, high, low, close, volume" in (
        SELECT_STANDARD_CANDLES_BASE_SQL
    )
    assert "FROM candles" in SELECT_STANDARD_CANDLES_BASE_SQL
    assert "is_closed IS TRUE" in SELECT_STANDARD_CANDLES_BASE_SQL


def test_repository_load_standard_candles_maps_rows_and_filters(monkeypatch):
    import psycopg

    row_open_time = datetime(2024, 1, 1, 0, 0, tzinfo=timezone.utc)
    start_time = datetime(2024, 1, 1, 0, 0, tzinfo=timezone.utc)
    end_time = datetime(2024, 1, 1, 1, 0, tzinfo=timezone.utc)
    fake_connection = FakeConnection(
        [
            {
                "timestamp": row_open_time,
                "open": Decimal("100"),
                "high": Decimal("101"),
                "low": Decimal("99"),
                "close": Decimal("100.5"),
                "volume": Decimal("12.5"),
                "source": "binance_spot",
                "raw_payload": ["ignored"],
            }
        ]
    )

    def fake_connect(database_url: str, **kwargs: Any) -> FakeConnection:
        assert database_url == "postgresql://example/test"
        assert "row_factory" in kwargs
        return fake_connection

    monkeypatch.setattr(psycopg, "connect", fake_connect)

    rows = PostgresCandleRepository("postgresql://example/test").load_standard_candles(
        source="binance_spot",
        symbol="BTCUSDT",
        interval="1m",
        start_time=start_time,
        end_time=end_time,
    )

    assert rows == [
        {
            "timestamp": row_open_time,
            "open": Decimal("100"),
            "high": Decimal("101"),
            "low": Decimal("99"),
            "close": Decimal("100.5"),
            "volume": Decimal("12.5"),
        }
    ]
    assert fake_connection.executed_params == {
        "source": "binance_spot",
        "symbol": "BTCUSDT",
        "interval": "1m",
        "start_time": start_time,
        "end_time": end_time,
    }
    assert fake_connection.executed_query is not None
    assert "open_time >= %(start_time)s" in fake_connection.executed_query
    assert "open_time <= %(end_time)s" in fake_connection.executed_query
    assert "ORDER BY open_time ASC" in fake_connection.executed_query

def test_upsert_sql_is_duplicate_safe_for_candle_identity():
    assert (
        "ON CONFLICT (source, symbol, interval, open_time) DO UPDATE"
        in UPSERT_CANDLE_SQL
    )
    assert "updated_at = now()" in UPSERT_CANDLE_SQL


def test_persisted_candle_insert_row_contains_all_contract_fields():
    row = persisted_candle().as_insert_row()

    assert tuple(row) == EXPECTED_CANDLE_COLUMNS
    assert row["source"] == "binance_spot"
    assert row["symbol"] == "BTCUSDT"
    assert row["interval"] == "1m"
    assert row["open"] == Decimal("42000")


@pytest.mark.skipif(
    not os.environ.get("QUANT_BITCOIN_TEST_DATABASE_URL"),
    reason="QUANT_BITCOIN_TEST_DATABASE_URL is not configured",
)
def test_postgres_repository_upserts_duplicate_candles_idempotently():
    repository = PostgresCandleRepository(os.environ["QUANT_BITCOIN_TEST_DATABASE_URL"])
    repository.initialize_schema()

    repository.upsert_candles([persisted_candle("42000")])
    repository.upsert_candles([persisted_candle("42001")])

    latest = repository.latest_open_time("binance_spot", "BTCUSDT", "1m")
    assert latest == datetime(2024, 1, 1, 0, 0, tzinfo=timezone.utc)

    repository.save_checkpoint(
        IngestionCheckpoint(
            source="binance_spot",
            symbol="BTCUSDT",
            interval="1m",
            mode="historical_backfill",
            last_open_time=latest,
            last_close_time=datetime(
                2024, 1, 1, 0, 0, 59, 999000, tzinfo=timezone.utc
            ),
            last_event_time=None,
            status="completed",
            metadata={"stored_candles": 1},
        )
    )
    checkpoint = repository.load_checkpoint(
        "binance_spot", "BTCUSDT", "1m", "historical_backfill"
    )
    assert checkpoint is not None
    assert checkpoint.last_open_time == latest
