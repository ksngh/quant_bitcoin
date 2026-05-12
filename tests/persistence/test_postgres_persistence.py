from __future__ import annotations

import os
from datetime import datetime, timezone
from decimal import Decimal

import pytest

from quant_bitcoin.persistence import (
    CANDLE_TABLE_COLUMNS,
    SCHEMA_SQL,
    IngestionCheckpoint,
    PersistedCandle,
    PostgresCandleRepository,
)
from quant_bitcoin.persistence.postgres import UPSERT_CANDLE_SQL


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
