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
