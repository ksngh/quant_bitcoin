from __future__ import annotations

import asyncio
import json
from datetime import datetime, timezone
from decimal import Decimal

import pytest

from quant_bitcoin.market_data.binance_websocket import (
    WEBSOCKET_INGESTION_MODE,
    BinanceWebSocketCandleIngestor,
    BinanceWebSocketIngestionError,
    build_kline_stream_url,
    parse_binance_kline_message,
)
from quant_bitcoin.persistence import SOURCE_BINANCE_SPOT


OPEN_TIME_MS = 1_704_067_200_000


def sample_message(
    *,
    open_time_ms: int = OPEN_TIME_MS,
    closed: bool = True,
    symbol: str = "BTCUSDT",
    interval: str = "1m",
) -> dict[str, object]:
    return {
        "e": "kline",
        "E": open_time_ms + 60_000,
        "s": symbol,
        "k": {
            "t": open_time_ms,
            "T": open_time_ms + 59_999,
            "s": symbol,
            "i": interval,
            "o": "42000.00",
            "c": "42050.00",
            "h": "42100.00",
            "l": "41900.00",
            "v": "12.50000000",
            "n": 123,
            "x": closed,
            "q": "525625.00000000",
            "V": "6.10000000",
            "Q": "256405.00000000",
            "B": "0",
        },
    }


class InMemoryCandleRepository:
    def __init__(self) -> None:
        self.rows = {}
        self.checkpoints = []
        self.upsert_calls = 0

    def upsert_candles(self, candles):
        self.upsert_calls += 1
        for candle in candles:
            key = (candle.source, candle.symbol, candle.interval, candle.open_time)
            self.rows[key] = candle
        return len(candles)

    def save_checkpoint(self, checkpoint):
        self.checkpoints.append(checkpoint)


class FakeConnection:
    def __init__(self, messages=None, enter_error: Exception | None = None) -> None:
        self.messages = list(messages or [])
        self.enter_error = enter_error

    async def __aenter__(self):
        if self.enter_error is not None:
            raise self.enter_error
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    def __aiter__(self):
        return self

    async def __anext__(self):
        if not self.messages:
            raise StopAsyncIteration
        next_message = self.messages.pop(0)
        if isinstance(next_message, Exception):
            raise next_message
        return next_message


class FakeConnector:
    def __init__(self, connections) -> None:
        self.connections = list(connections)
        self.urls = []

    async def __call__(self, url: str):
        self.urls.append(url)
        if not self.connections:
            raise RuntimeError("no fake connections left")
        return self.connections.pop(0)


def test_websocket_ingestor_persists_closed_btcusdt_one_minute_candle():
    repository = InMemoryCandleRepository()
    connector = FakeConnector([FakeConnection([json.dumps(sample_message())])])

    result = asyncio.run(
        BinanceWebSocketCandleIngestor(
            repository,
            connector=connector,
            sleep=_fake_sleep,
        ).run(max_messages=1)
    )

    assert result.messages_seen == 1
    assert result.candles_persisted == 1
    assert result.reconnects == 0
    assert connector.urls == [
        "wss://stream.binance.com:9443/ws/btcusdt@kline_1m"
    ]
    assert len(repository.rows) == 1
    stored = next(iter(repository.rows.values()))
    assert stored.source == SOURCE_BINANCE_SPOT
    assert stored.symbol == "BTCUSDT"
    assert stored.interval == "1m"
    assert stored.open_time == datetime(2024, 1, 1, 0, 0, tzinfo=timezone.utc)
    assert stored.close_time == datetime(2024, 1, 1, 0, 0, 59, 999000, tzinfo=timezone.utc)
    assert stored.close == Decimal("42050.00")
    assert stored.is_closed is True
    assert repository.checkpoints[-1].status == "completed"
    assert repository.checkpoints[-1].mode == WEBSOCKET_INGESTION_MODE


def test_websocket_ingestor_ignores_open_in_progress_kline():
    repository = InMemoryCandleRepository()
    connector = FakeConnector([FakeConnection([sample_message(closed=False)])])

    result = asyncio.run(
        BinanceWebSocketCandleIngestor(
            repository,
            connector=connector,
            sleep=_fake_sleep,
        ).run(max_messages=1)
    )

    assert result.messages_seen == 1
    assert result.candles_persisted == 0
    assert repository.rows == {}
    assert repository.upsert_calls == 0


def test_websocket_ingestor_duplicate_messages_are_duplicate_safe_by_candle_key():
    repository = InMemoryCandleRepository()
    duplicate = sample_message()
    connector = FakeConnector([FakeConnection([duplicate, duplicate])])

    result = asyncio.run(
        BinanceWebSocketCandleIngestor(
            repository,
            connector=connector,
            sleep=_fake_sleep,
        ).run(max_messages=2)
    )

    assert result.messages_seen == 2
    assert result.candles_persisted == 2
    assert repository.upsert_calls == 2
    assert len(repository.rows) == 1


def test_websocket_ingestor_reconnects_after_mocked_transient_failure():
    repository = InMemoryCandleRepository()
    sleeps = []
    connector = FakeConnector(
        [
            FakeConnection(enter_error=ConnectionError("temporary disconnect")),
            FakeConnection([sample_message()]),
        ]
    )

    async def fake_sleep(seconds: float) -> None:
        sleeps.append(seconds)

    result = asyncio.run(
        BinanceWebSocketCandleIngestor(
            repository,
            connector=connector,
            sleep=fake_sleep,
            reconnect_delay_seconds=0.25,
            max_reconnects=1,
        ).run(max_messages=1)
    )

    assert result.reconnects == 1
    assert result.candles_persisted == 1
    assert sleeps == [0.25]
    assert [checkpoint.status for checkpoint in repository.checkpoints] == [
        "running",
        "reconnecting",
        "running",
        "completed",
    ]


def test_websocket_ingestor_fails_after_reconnect_limit():
    repository = InMemoryCandleRepository()
    connector = FakeConnector(
        [
            FakeConnection(enter_error=ConnectionError("first")),
            FakeConnection(enter_error=ConnectionError("second")),
        ]
    )

    with pytest.raises(BinanceWebSocketIngestionError):
        asyncio.run(
            BinanceWebSocketCandleIngestor(
                repository,
                connector=connector,
                sleep=_fake_sleep,
                max_reconnects=1,
            ).run(max_messages=1)
        )

    assert repository.checkpoints[-1].status == "failed"


def test_parse_binance_kline_message_maps_contract_fields():
    candle = parse_binance_kline_message(
        {"stream": "btcusdt@kline_1m", "data": sample_message()},
        expected_symbol="btcusdt",
        expected_interval="1m",
    )

    assert candle is not None
    assert candle.source == SOURCE_BINANCE_SPOT
    assert candle.symbol == "BTCUSDT"
    assert candle.interval == "1m"
    assert candle.open == Decimal("42000.00")
    assert candle.high == Decimal("42100.00")
    assert candle.low == Decimal("41900.00")
    assert candle.close == Decimal("42050.00")
    assert candle.volume == Decimal("12.50000000")
    assert candle.quote_asset_volume == Decimal("525625.00000000")
    assert candle.number_of_trades == 123
    assert candle.taker_buy_base_asset_volume == Decimal("6.10000000")
    assert candle.taker_buy_quote_asset_volume == Decimal("256405.00000000")
    assert candle.raw_payload["data"]["k"]["x"] is True


def test_parse_binance_kline_message_ignores_non_matching_or_open_messages():
    assert parse_binance_kline_message({"e": "ping"}) is None
    assert parse_binance_kline_message(sample_message(closed=False)) is None
    assert parse_binance_kline_message(sample_message(symbol="ETHUSDT")) is None
    assert parse_binance_kline_message(sample_message(interval="3m")) is None


@pytest.mark.parametrize(
    ("message", "expected"),
    [
        ("not-json", "Expecting value"),
        ({"e": "kline", "k": {"s": "BTCUSDT", "i": "1m", "x": True}}, "open_time is required"),
        (
            sample_message() | {"k": sample_message()["k"] | {"o": "bad"}},
            "open must be numeric",
        ),
    ],
)
def test_parse_binance_kline_message_rejects_invalid_payloads(message, expected):
    with pytest.raises((ValueError, json.JSONDecodeError), match=expected):
        parse_binance_kline_message(message)


def test_build_kline_stream_url_uses_public_market_data_stream_without_signed_data():
    url = build_kline_stream_url(
        "wss://stream.binance.com:9443/ws", symbol=" btcusdt ", interval="1m"
    )

    assert url == "wss://stream.binance.com:9443/ws/btcusdt@kline_1m"
    assert "order" not in url.lower()
    assert "apiKey" not in url
    assert "signature" not in url
    assert "X-MBX-APIKEY" not in url


async def _fake_sleep(seconds: float) -> None:
    return None
