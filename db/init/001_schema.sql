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

CREATE TABLE IF NOT EXISTS strategy_configs (
    id BIGSERIAL PRIMARY KEY,
    strategy_key TEXT NOT NULL,
    strategy_name TEXT NOT NULL,
    version TEXT NOT NULL,
    parameters JSONB NOT NULL,
    parameters_hash TEXT NOT NULL,
    metadata JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT strategy_configs_key_version_parameters_hash_key
        UNIQUE (strategy_key, version, parameters_hash)
);

CREATE INDEX IF NOT EXISTS strategy_configs_strategy_name_idx
    ON strategy_configs (strategy_name);

CREATE TABLE IF NOT EXISTS backtest_runs (
    id BIGSERIAL PRIMARY KEY,
    run_key TEXT NOT NULL,
    strategy_config_id BIGINT NOT NULL REFERENCES strategy_configs(id),
    engine_name TEXT NOT NULL,
    engine_version TEXT NOT NULL,
    candle_source TEXT NOT NULL,
    symbol TEXT NOT NULL,
    interval TEXT NOT NULL,
    requested_start_time TIMESTAMPTZ,
    requested_end_time TIMESTAMPTZ,
    actual_start_time TIMESTAMPTZ,
    actual_end_time TIMESTAMPTZ,
    candle_count INTEGER NOT NULL,
    starting_cash NUMERIC NOT NULL,
    trade_quantity NUMERIC NOT NULL,
    status TEXT NOT NULL,
    metadata JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    completed_at TIMESTAMPTZ,
    CONSTRAINT backtest_runs_run_key_key UNIQUE (run_key)
);

CREATE INDEX IF NOT EXISTS backtest_runs_created_at_idx
    ON backtest_runs (created_at DESC);

CREATE INDEX IF NOT EXISTS backtest_runs_market_created_at_idx
    ON backtest_runs (candle_source, symbol, interval, created_at DESC);

CREATE INDEX IF NOT EXISTS backtest_runs_market_range_idx
    ON backtest_runs (candle_source, symbol, interval, actual_start_time, actual_end_time);

CREATE INDEX IF NOT EXISTS backtest_runs_strategy_created_at_idx
    ON backtest_runs (strategy_config_id, created_at DESC);

CREATE TABLE IF NOT EXISTS backtest_results (
    backtest_run_id BIGINT PRIMARY KEY REFERENCES backtest_runs(id) ON DELETE CASCADE,
    starting_cash NUMERIC NOT NULL,
    ending_cash NUMERIC NOT NULL,
    ending_position NUMERIC NOT NULL,
    final_price NUMERIC,
    final_equity NUMERIC NOT NULL,
    total_return NUMERIC NOT NULL,
    trade_count INTEGER NOT NULL,
    buy_count INTEGER NOT NULL,
    sell_count INTEGER NOT NULL,
    metadata JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS backtest_trades (
    id BIGSERIAL PRIMARY KEY,
    backtest_run_id BIGINT NOT NULL REFERENCES backtest_runs(id) ON DELETE CASCADE,
    sequence INTEGER NOT NULL,
    candle_open_time TIMESTAMPTZ NOT NULL,
    signal TEXT NOT NULL,
    price NUMERIC NOT NULL,
    quantity NUMERIC NOT NULL,
    cash_after NUMERIC NOT NULL,
    position_after NUMERIC NOT NULL,
    metadata JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT backtest_trades_run_sequence_key UNIQUE (backtest_run_id, sequence)
);

CREATE INDEX IF NOT EXISTS backtest_trades_run_sequence_idx
    ON backtest_trades (backtest_run_id, sequence);

CREATE INDEX IF NOT EXISTS backtest_trades_run_candle_open_time_idx
    ON backtest_trades (backtest_run_id, candle_open_time);

CREATE INDEX IF NOT EXISTS backtest_trades_run_signal_idx
    ON backtest_trades (backtest_run_id, signal);

CREATE TABLE IF NOT EXISTS backtest_graph_points (
    id BIGSERIAL PRIMARY KEY,
    backtest_run_id BIGINT NOT NULL REFERENCES backtest_runs(id) ON DELETE CASCADE,
    sequence INTEGER NOT NULL,
    candle_open_time TIMESTAMPTZ NOT NULL,
    close_price NUMERIC NOT NULL,
    cash NUMERIC NOT NULL,
    position NUMERIC NOT NULL,
    equity NUMERIC NOT NULL,
    trade_id BIGINT REFERENCES backtest_trades(id) ON DELETE SET NULL,
    signal TEXT,
    metadata JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT backtest_graph_points_run_sequence_key
        UNIQUE (backtest_run_id, sequence),
    CONSTRAINT backtest_graph_points_run_candle_open_time_key
        UNIQUE (backtest_run_id, candle_open_time)
);

CREATE INDEX IF NOT EXISTS backtest_graph_points_run_candle_open_time_idx
    ON backtest_graph_points (backtest_run_id, candle_open_time);

CREATE INDEX IF NOT EXISTS backtest_graph_points_run_sequence_idx
    ON backtest_graph_points (backtest_run_id, sequence);
