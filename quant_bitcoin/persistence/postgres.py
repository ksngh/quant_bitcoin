"""PostgreSQL persistence for market-data candles.

The repository in this module owns durable market-data storage only. It writes
public candle data and ingestion checkpoints; it does not know about strategies,
execution, signed requests, API keys, or exchange order endpoints.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any

SOURCE_BINANCE_SPOT = "binance_spot"
HISTORICAL_BACKFILL_MODE = "historical_backfill"

CANDLE_TABLE_COLUMNS: tuple[str, ...] = (
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

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS candles (
    id BIGSERIAL PRIMARY KEY,
    source TEXT NOT NULL,
    symbol TEXT NOT NULL,
    interval TEXT NOT NULL,
    open_time TIMESTAMPTZ NOT NULL,
    close_time TIMESTAMPTZ NOT NULL,
    open NUMERIC NOT NULL,
    high NUMERIC NOT NULL,
    low NUMERIC NOT NULL,
    close NUMERIC NOT NULL,
    volume NUMERIC NOT NULL,
    quote_asset_volume NUMERIC NOT NULL,
    number_of_trades INTEGER NOT NULL,
    taker_buy_base_asset_volume NUMERIC NOT NULL,
    taker_buy_quote_asset_volume NUMERIC NOT NULL,
    is_closed BOOLEAN NOT NULL,
    raw_payload JSONB,
    ingested_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT candles_source_symbol_interval_open_time_key
        UNIQUE (source, symbol, interval, open_time)
);

CREATE INDEX IF NOT EXISTS candles_lookup_idx
    ON candles (source, symbol, interval, open_time);

CREATE TABLE IF NOT EXISTS ingestion_checkpoints (
    id BIGSERIAL PRIMARY KEY,
    source TEXT NOT NULL,
    symbol TEXT NOT NULL,
    interval TEXT NOT NULL,
    mode TEXT NOT NULL,
    last_open_time TIMESTAMPTZ,
    last_close_time TIMESTAMPTZ,
    last_event_time TIMESTAMPTZ,
    status TEXT NOT NULL,
    error_message TEXT,
    metadata JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT ingestion_checkpoints_source_symbol_interval_mode_key
        UNIQUE (source, symbol, interval, mode)
);
"""


@dataclass(frozen=True)
class PersistedCandle:
    """A finalized candle row following the accepted Task 013 schema."""

    source: str
    symbol: str
    interval: str
    open_time: datetime
    close_time: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal
    quote_asset_volume: Decimal
    number_of_trades: int
    taker_buy_base_asset_volume: Decimal
    taker_buy_quote_asset_volume: Decimal
    is_closed: bool
    raw_payload: list[Any] | dict[str, Any] | None = None

    def as_insert_row(self) -> dict[str, Any]:
        """Return a row containing the Task 013 candle contract fields."""

        return {column: getattr(self, column) for column in CANDLE_TABLE_COLUMNS}


@dataclass(frozen=True)
class IngestionCheckpoint:
    """Progress record for restartable candle ingestion."""

    source: str
    symbol: str
    interval: str
    mode: str
    last_open_time: datetime | None
    last_close_time: datetime | None
    last_event_time: datetime | None
    status: str
    error_message: str | None = None
    metadata: dict[str, Any] | None = None


class PostgresCandleRepository:
    """PostgreSQL repository for candles and ingestion checkpoints."""

    def __init__(self, database_url: str) -> None:
        if not database_url:
            raise ValueError("database_url must not be blank")
        self.database_url = database_url

    def initialize_schema(self) -> None:
        """Create the local development schema if it does not exist."""

        import psycopg

        with psycopg.connect(self.database_url) as connection:
            connection.execute(SCHEMA_SQL)

    def upsert_candles(self, candles: Iterable[PersistedCandle]) -> int:
        """Insert finalized candles and update duplicates by unique candle key."""

        import psycopg
        from psycopg.types.json import Jsonb

        rows = [candle.as_insert_row() for candle in candles]
        if not rows:
            return 0
        for row in rows:
            row["raw_payload"] = Jsonb(row["raw_payload"])

        with psycopg.connect(self.database_url) as connection:
            with connection.cursor() as cursor:
                cursor.executemany(UPSERT_CANDLE_SQL, rows)
            return len(rows)

    def latest_open_time(
        self, source: str, symbol: str, interval: str
    ) -> datetime | None:
        """Return the latest stored open time for a candle stream."""

        import psycopg
        from psycopg.rows import dict_row

        with psycopg.connect(self.database_url, row_factory=dict_row) as connection:
            row = connection.execute(
                """
                SELECT MAX(open_time) AS latest_open_time
                FROM candles
                WHERE source = %s AND symbol = %s AND interval = %s
                """,
                (source, symbol, interval),
            ).fetchone()
        latest = row["latest_open_time"] if row else None
        if isinstance(latest, datetime):
            return _as_utc(latest)
        return None

    def load_standard_candles(
        self,
        *,
        source: str,
        symbol: str,
        interval: str,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
    ) -> list[dict[str, Any]]:
        """Return stored candles normalized to the standard candle schema."""

        import psycopg
        from psycopg.rows import dict_row

        query, params = _build_standard_candle_query(
            source=source,
            symbol=symbol,
            interval=interval,
            start_time=start_time,
            end_time=end_time,
        )
        with psycopg.connect(self.database_url, row_factory=dict_row) as connection:
            rows = connection.execute(query, params).fetchall()

        return [
            {
                "timestamp": _as_utc(row["timestamp"]),
                "open": row["open"],
                "high": row["high"],
                "low": row["low"],
                "close": row["close"],
                "volume": row["volume"],
            }
            for row in rows
        ]

    def save_checkpoint(self, checkpoint: IngestionCheckpoint) -> None:
        """Insert or update a restart checkpoint."""

        import psycopg
        from psycopg.types.json import Jsonb

        with psycopg.connect(self.database_url) as connection:
            connection.execute(
                UPSERT_CHECKPOINT_SQL,
                {
                    "source": checkpoint.source,
                    "symbol": checkpoint.symbol,
                    "interval": checkpoint.interval,
                    "mode": checkpoint.mode,
                    "last_open_time": checkpoint.last_open_time,
                    "last_close_time": checkpoint.last_close_time,
                    "last_event_time": checkpoint.last_event_time,
                    "status": checkpoint.status,
                    "error_message": checkpoint.error_message,
                    "metadata": Jsonb(checkpoint.metadata),
                },
            )

    def load_checkpoint(
        self, source: str, symbol: str, interval: str, mode: str
    ) -> IngestionCheckpoint | None:
        """Load a restart checkpoint if one exists."""

        import psycopg
        from psycopg.rows import dict_row

        with psycopg.connect(self.database_url, row_factory=dict_row) as connection:
            row = connection.execute(
                """
                SELECT source, symbol, interval, mode, last_open_time,
                       last_close_time, last_event_time, status, error_message,
                       metadata
                FROM ingestion_checkpoints
                WHERE source = %s AND symbol = %s AND interval = %s AND mode = %s
                """,
                (source, symbol, interval, mode),
            ).fetchone()
        if row is None:
            return None
        return IngestionCheckpoint(
            source=row["source"],
            symbol=row["symbol"],
            interval=row["interval"],
            mode=row["mode"],
            last_open_time=_optional_utc(row["last_open_time"]),
            last_close_time=_optional_utc(row["last_close_time"]),
            last_event_time=_optional_utc(row["last_event_time"]),
            status=row["status"],
            error_message=row["error_message"],
            metadata=row["metadata"],
        )


SELECT_STANDARD_CANDLES_BASE_SQL = """
SELECT open_time AS timestamp, open, high, low, close, volume
FROM candles
WHERE source = %(source)s AND symbol = %(symbol)s AND interval = %(interval)s
  AND is_closed IS TRUE
"""


UPSERT_CANDLE_SQL = """
INSERT INTO candles (
    source, symbol, interval, open_time, close_time, open, high, low, close,
    volume, quote_asset_volume, number_of_trades, taker_buy_base_asset_volume,
    taker_buy_quote_asset_volume, is_closed, raw_payload
) VALUES (
    %(source)s, %(symbol)s, %(interval)s, %(open_time)s, %(close_time)s,
    %(open)s, %(high)s, %(low)s, %(close)s, %(volume)s,
    %(quote_asset_volume)s, %(number_of_trades)s,
    %(taker_buy_base_asset_volume)s, %(taker_buy_quote_asset_volume)s,
    %(is_closed)s, %(raw_payload)s
)
ON CONFLICT (source, symbol, interval, open_time) DO UPDATE SET
    close_time = EXCLUDED.close_time,
    open = EXCLUDED.open,
    high = EXCLUDED.high,
    low = EXCLUDED.low,
    close = EXCLUDED.close,
    volume = EXCLUDED.volume,
    quote_asset_volume = EXCLUDED.quote_asset_volume,
    number_of_trades = EXCLUDED.number_of_trades,
    taker_buy_base_asset_volume = EXCLUDED.taker_buy_base_asset_volume,
    taker_buy_quote_asset_volume = EXCLUDED.taker_buy_quote_asset_volume,
    is_closed = EXCLUDED.is_closed,
    raw_payload = EXCLUDED.raw_payload,
    updated_at = now()
"""

UPSERT_CHECKPOINT_SQL = """
INSERT INTO ingestion_checkpoints (
    source, symbol, interval, mode, last_open_time, last_close_time,
    last_event_time, status, error_message, metadata
) VALUES (
    %(source)s, %(symbol)s, %(interval)s, %(mode)s, %(last_open_time)s,
    %(last_close_time)s, %(last_event_time)s, %(status)s, %(error_message)s,
    %(metadata)s
)
ON CONFLICT (source, symbol, interval, mode) DO UPDATE SET
    last_open_time = EXCLUDED.last_open_time,
    last_close_time = EXCLUDED.last_close_time,
    last_event_time = EXCLUDED.last_event_time,
    status = EXCLUDED.status,
    error_message = EXCLUDED.error_message,
    metadata = EXCLUDED.metadata,
    updated_at = now()
"""


def _build_standard_candle_query(
    *,
    source: str,
    symbol: str,
    interval: str,
    start_time: datetime | None,
    end_time: datetime | None,
) -> tuple[str, dict[str, Any]]:
    query_parts = [SELECT_STANDARD_CANDLES_BASE_SQL]
    params: dict[str, Any] = {
        "source": source,
        "symbol": symbol,
        "interval": interval,
    }
    if start_time is not None:
        query_parts.append("AND open_time >= %(start_time)s")
        params["start_time"] = start_time
    if end_time is not None:
        query_parts.append("AND open_time <= %(end_time)s")
        params["end_time"] = end_time
    query_parts.append("ORDER BY open_time ASC")
    return "\n".join(query_parts), params


def _optional_utc(value: datetime | None) -> datetime | None:
    if value is None:
        return None
    return _as_utc(value)


def _as_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)
