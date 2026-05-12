"""Binance public WebSocket candle ingestion into persistence.

This module is market-data-only. It connects to Binance public spot kline
streams, maps finalized kline events to the accepted candle persistence schema,
and writes closed candles through the repository's duplicate-safe upsert method.
It does not perform historical REST gap fill; run Task 014 historical backfill
before startup whenever downtime gaps must be complete.
"""

from __future__ import annotations

import asyncio
import json
from collections.abc import AsyncIterator, Awaitable, Callable, Sequence
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from typing import Any, Protocol

from quant_bitcoin.market_data.binance_backfill import _reject_order_endpoint
from quant_bitcoin.market_data.binance_downloader import MINUTE_INTERVALS
from quant_bitcoin.persistence import (
    SOURCE_BINANCE_SPOT,
    IngestionCheckpoint,
    PersistedCandle,
)

DEFAULT_WEBSOCKET_BASE_URL = "wss://stream.binance.com:9443/ws"
WEBSOCKET_INGESTION_MODE = "websocket_ingestion"
DEFAULT_RECONNECT_DELAY_SECONDS = 1.0

Sleep = Callable[[float], Awaitable[None]]
TimeProvider = Callable[[], datetime]


class WebSocketConnection(Protocol):
    """Async context manager yielding public WebSocket messages."""

    async def __aenter__(self) -> AsyncIterator[str | bytes | dict[str, Any]]: ...

    async def __aexit__(self, exc_type: object, exc: object, tb: object) -> object: ...


WebSocketConnector = Callable[[str], Awaitable[WebSocketConnection]]


class CandleRepository(Protocol):
    """Persistence behavior needed by WebSocket candle ingestion."""

    def upsert_candles(self, candles: Sequence[PersistedCandle]) -> int: ...

    def save_checkpoint(self, checkpoint: IngestionCheckpoint) -> None: ...


@dataclass(frozen=True)
class WebSocketIngestionResult:
    """Summary of one bounded WebSocket ingestion run."""

    symbol: str
    interval: str
    messages_seen: int
    candles_persisted: int
    reconnects: int


class BinanceWebSocketIngestionError(RuntimeError):
    """Base error for Binance WebSocket ingestion failures."""


class BinanceWebSocketCandleIngestor:
    """Ingest closed Binance public spot kline messages into persistence."""

    def __init__(
        self,
        repository: CandleRepository,
        *,
        base_url: str = DEFAULT_WEBSOCKET_BASE_URL,
        connector: WebSocketConnector | None = None,
        sleep: Sleep = asyncio.sleep,
        now: TimeProvider | None = None,
        reconnect_delay_seconds: float = DEFAULT_RECONNECT_DELAY_SECONDS,
        max_reconnects: int = 3,
    ) -> None:
        if reconnect_delay_seconds < 0:
            raise ValueError("reconnect_delay_seconds must be non-negative")
        if max_reconnects < 0:
            raise ValueError("max_reconnects must be non-negative")
        self.repository = repository
        self.base_url = base_url.rstrip("/")
        self._connector = connector or _connect_with_websockets
        self._sleep = sleep
        self._now = now or (lambda: datetime.now(timezone.utc))
        self.reconnect_delay_seconds = reconnect_delay_seconds
        self.max_reconnects = max_reconnects

    async def run(
        self,
        *,
        symbol: str = "BTCUSDT",
        interval: str = "1m",
        max_messages: int | None = None,
    ) -> WebSocketIngestionResult:
        """Consume public kline messages until stopped or ``max_messages`` is reached.

        ``max_messages`` exists for tests and bounded local checks. Production-style
        callers can leave it unset and manage process lifetime externally. Startup
        gap catch-up is intentionally not implemented here; run the Task 014
        historical backfill before this ingestor when historical completeness is
        required after downtime.
        """

        normalized_symbol = _normalize_symbol(symbol)
        _validate_interval(interval)
        if max_messages is not None and max_messages < 1:
            raise ValueError("max_messages must be positive when provided")

        url = build_kline_stream_url(
            self.base_url, symbol=normalized_symbol, interval=interval
        )
        messages_seen = 0
        candles_persisted = 0
        reconnects = 0
        last_open_time: datetime | None = None
        last_close_time: datetime | None = None
        last_event_time: datetime | None = None

        self._save_checkpoint(
            symbol=normalized_symbol,
            interval=interval,
            status="running",
            last_open_time=None,
            last_close_time=None,
            last_event_time=None,
            error_message=None,
            metadata={"startup_catch_up": "requires_task_014_backfill"},
        )

        while True:
            try:
                connection = await self._connector(url)
                async with connection as messages:
                    async for raw_message in messages:
                        messages_seen += 1
                        candle = parse_binance_kline_message(
                            raw_message,
                            expected_symbol=normalized_symbol,
                            expected_interval=interval,
                        )
                        if candle is not None:
                            candles_persisted += self.repository.upsert_candles([candle])
                            last_open_time = candle.open_time
                            last_close_time = candle.close_time
                            last_event_time = _extract_event_time(raw_message)
                            self._save_checkpoint(
                                symbol=normalized_symbol,
                                interval=interval,
                                status="running",
                                last_open_time=last_open_time,
                                last_close_time=last_close_time,
                                last_event_time=last_event_time,
                                error_message=None,
                                metadata={
                                    "messages_seen": messages_seen,
                                    "candles_persisted": candles_persisted,
                                    "reconnects": reconnects,
                                },
                            )

                        if max_messages is not None and messages_seen >= max_messages:
                            self._save_checkpoint(
                                symbol=normalized_symbol,
                                interval=interval,
                                status="completed",
                                last_open_time=last_open_time,
                                last_close_time=last_close_time,
                                last_event_time=last_event_time,
                                error_message=None,
                                metadata={
                                    "messages_seen": messages_seen,
                                    "candles_persisted": candles_persisted,
                                    "reconnects": reconnects,
                                },
                            )
                            return WebSocketIngestionResult(
                                symbol=normalized_symbol,
                                interval=interval,
                                messages_seen=messages_seen,
                                candles_persisted=candles_persisted,
                                reconnects=reconnects,
                            )
            except Exception as error:
                reconnects += 1
                if reconnects > self.max_reconnects:
                    self._save_checkpoint(
                        symbol=normalized_symbol,
                        interval=interval,
                        status="failed",
                        last_open_time=last_open_time,
                        last_close_time=last_close_time,
                        last_event_time=last_event_time,
                        error_message=str(error),
                        metadata={
                            "messages_seen": messages_seen,
                            "candles_persisted": candles_persisted,
                            "reconnects": reconnects,
                        },
                    )
                    raise BinanceWebSocketIngestionError(
                        "Binance WebSocket ingestion exceeded reconnect limit"
                    ) from error

                self._save_checkpoint(
                    symbol=normalized_symbol,
                    interval=interval,
                    status="reconnecting",
                    last_open_time=last_open_time,
                    last_close_time=last_close_time,
                    last_event_time=last_event_time,
                    error_message=str(error),
                    metadata={
                        "messages_seen": messages_seen,
                        "candles_persisted": candles_persisted,
                        "reconnects": reconnects,
                    },
                )
                await self._sleep(self.reconnect_delay_seconds)

    def _save_checkpoint(
        self,
        *,
        symbol: str,
        interval: str,
        status: str,
        last_open_time: datetime | None,
        last_close_time: datetime | None,
        last_event_time: datetime | None,
        error_message: str | None,
        metadata: dict[str, object],
    ) -> None:
        self.repository.save_checkpoint(
            IngestionCheckpoint(
                source=SOURCE_BINANCE_SPOT,
                symbol=symbol,
                interval=interval,
                mode=WEBSOCKET_INGESTION_MODE,
                last_open_time=last_open_time,
                last_close_time=last_close_time,
                last_event_time=last_event_time,
                status=status,
                error_message=error_message,
                metadata=metadata,
            )
        )


def build_kline_stream_url(base_url: str, *, symbol: str, interval: str) -> str:
    """Build the Binance public spot kline stream URL."""

    normalized_symbol = _normalize_symbol(symbol)
    _validate_interval(interval)
    url = f"{base_url.rstrip('/')}/{normalized_symbol.lower()}@kline_{interval}"
    _reject_order_endpoint(url)
    return url


def parse_binance_kline_message(
    message: str | bytes | dict[str, Any],
    *,
    expected_symbol: str = "BTCUSDT",
    expected_interval: str = "1m",
) -> PersistedCandle | None:
    """Map a Binance kline WebSocket event to a finalized candle row.

    Returns ``None`` for non-kline messages, mismatched streams, and open
    in-progress klines. Only messages with Binance's final-candle flag ``x`` set
    to true are persisted by the ingestor.
    """

    payload = _decode_message(message)
    event = payload.get("data") if isinstance(payload.get("data"), dict) else payload
    if event.get("e") != "kline" or not isinstance(event.get("k"), dict):
        return None

    kline = event["k"]
    symbol = _normalize_symbol(str(kline.get("s") or event.get("s") or ""))
    interval = str(kline.get("i") or "")
    if symbol != _normalize_symbol(expected_symbol) or interval != expected_interval:
        return None
    if kline.get("x") is not True:
        return None

    return PersistedCandle(
        source=SOURCE_BINANCE_SPOT,
        symbol=symbol,
        interval=interval,
        open_time=_from_milliseconds(_integer_kline_field(kline, "t", "open_time")),
        close_time=_from_milliseconds(_integer_kline_field(kline, "T", "close_time")),
        open=_decimal_kline_field(kline, "o", "open"),
        high=_decimal_kline_field(kline, "h", "high"),
        low=_decimal_kline_field(kline, "l", "low"),
        close=_decimal_kline_field(kline, "c", "close"),
        volume=_decimal_kline_field(kline, "v", "volume"),
        quote_asset_volume=_decimal_kline_field(kline, "q", "quote_asset_volume"),
        number_of_trades=_integer_kline_field(kline, "n", "number_of_trades"),
        taker_buy_base_asset_volume=_decimal_kline_field(
            kline, "V", "taker_buy_base_asset_volume"
        ),
        taker_buy_quote_asset_volume=_decimal_kline_field(
            kline, "Q", "taker_buy_quote_asset_volume"
        ),
        is_closed=True,
        raw_payload=payload,
    )


async def _connect_with_websockets(url: str) -> WebSocketConnection:
    _reject_order_endpoint(url)
    import websockets

    return websockets.connect(url, ping_interval=20)


def _decode_message(message: str | bytes | dict[str, Any]) -> dict[str, Any]:
    if isinstance(message, dict):
        return message
    if isinstance(message, bytes):
        message = message.decode("utf-8")
    if not isinstance(message, str):
        raise ValueError("Binance WebSocket message must be JSON text or a dict")
    payload = json.loads(message)
    if not isinstance(payload, dict):
        raise ValueError("Binance WebSocket message must decode to an object")
    return payload


def _extract_event_time(message: str | bytes | dict[str, Any]) -> datetime | None:
    payload = _decode_message(message)
    event = payload.get("data") if isinstance(payload.get("data"), dict) else payload
    event_time = event.get("E")
    if event_time is None:
        return None
    return _from_milliseconds(_coerce_non_negative_int(event_time, "event_time"))


def _integer_kline_field(kline: dict[str, Any], key: str, field_name: str) -> int:
    if key not in kline:
        raise ValueError(f"Binance WebSocket kline field {field_name} is required")
    return _coerce_non_negative_int(kline[key], field_name)


def _coerce_non_negative_int(value: object, field_name: str) -> int:
    try:
        integer = int(value)  # type: ignore[arg-type]
    except (TypeError, ValueError) as error:
        raise ValueError(
            f"Binance WebSocket kline field {field_name} must be an integer"
        ) from error
    if integer < 0:
        raise ValueError(
            f"Binance WebSocket kline field {field_name} must be non-negative"
        )
    return integer


def _decimal_kline_field(kline: dict[str, Any], key: str, field_name: str) -> Decimal:
    if key not in kline:
        raise ValueError(f"Binance WebSocket kline field {field_name} is required")
    try:
        return Decimal(str(kline[key]))
    except (InvalidOperation, ValueError) as error:
        raise ValueError(
            f"Binance WebSocket kline field {field_name} must be numeric"
        ) from error


def _normalize_symbol(symbol: str) -> str:
    if not isinstance(symbol, str):
        raise ValueError("symbol must be a string")
    normalized = symbol.strip().upper()
    if not normalized:
        raise ValueError("symbol must not be blank")
    return normalized


def _validate_interval(interval: str) -> None:
    if interval not in MINUTE_INTERVALS:
        supported = ", ".join(sorted(MINUTE_INTERVALS))
        raise ValueError(f"interval must be a supported minute interval: {supported}")


def _from_milliseconds(value: int) -> datetime:
    return datetime.fromtimestamp(value / 1000, tz=timezone.utc)
