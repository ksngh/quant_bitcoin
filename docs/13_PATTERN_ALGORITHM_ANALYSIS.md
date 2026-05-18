# Pattern Algorithm Analysis

# Purpose

This document reviews the implemented pattern detectors in `quant_bitcoin.patterns` as of Task 046. It explains current behavior from the codebase and related pattern task documents. It does not create new pattern behavior, strategy logic, trading execution, persistence, scheduling, or live exchange integration.

# Assumptions And Boundaries

- Pattern detectors evaluate already-provided completed candles.
- Pattern detectors are deterministic and pure: they do not fetch market data, read secrets, call exchange APIs, place orders, persist records, or make trading decisions.
- Input candles must be sorted ascending by `timestamp`; current pattern normalizers reject unsorted input.
- Liquidity and bid-ask spread are not implemented as reusable modules. Pattern configs can accept explicit `liquidity_pass` and `spread_pass` values, but the detectors do not approximate those filters.
- Returned events are analysis events. They include entry/stop/target reference prices for deterministic context, but they are not orders.

# Package Structure

The package entry point is `quant_bitcoin/patterns/__init__.py`. It re-exports public pattern configuration dataclasses, enums, event dataclasses, and detector functions.

Implemented modules:

- `fair_value_gap.py`
- `trendline_break.py`
- `order_block.py`
- `cup_and_handle.py`
- `diamond.py`
- `adam_and_eve.py`

All detectors use stable event identifiers built from deterministic event components and a short SHA-256 digest. The stable identifiers support rolling-window duplicate prevention by callers.

# Common Validation And Event Flow

Although each detector has pattern-specific logic, the common flow is:

1. Normalize input candles from a DataFrame or iterable of dictionaries.
2. Ensure required candle columns exist.
3. Add or override `symbol` when the caller supplies a symbol.
4. Require ascending timestamps.
5. Convert OHLCV columns to numeric values and reject missing or invalid values.
6. Validate external filter requirements such as liquidity and spread pass/fail values when the config requires them.
7. Calculate reusable indicator outputs such as ATR, Volume Ratio, Pivots, and Displacement Candles where needed.
8. Build mechanical pattern candidates.
9. Evaluate structural, ATR, volume, displacement, and optional external-filter conditions.
10. Score the candidate and classify it as `VALID`, `WEAK`, `PENDING`, or reject it.
11. Build event dataclasses with stable `event_id` values.

# Reused Indicator Outputs

Current detectors reuse implemented indicator modules as follows:

- Fair Value Gap: ATR, Volume Ratio, Displacement Candle.
- Trendline Break: ATR, Volume Ratio, Pivot detection, Displacement Candle.
- Order Block: ATR, Volume Ratio, Displacement Candle.
- Cup and Handle: ATR, Volume Ratio, Pivot detection, Displacement Candle.
- Diamond: ATR, Volume Ratio, Pivot detection, Displacement Candle.
- Adam and Eve: ATR, Volume Ratio, Pivot detection, Displacement Candle.

Support / Resistance Zone and Swing Structure are implemented indicators, but the current pattern detector code primarily builds its own event-specific structures from pivots rather than invoking those modules in every detector. Liquidity and bid-ask spread remain explicit external pass/fail inputs when required.

# Fair Value Gap

Primary detector functions:

- `detect_patterns(candles, symbol=None, timeframe=None, config=None)`
- `detect_fair_value_gaps(candles, symbol=None, timeframe=None, config=None)`
- `filter_new_events(events, seen_event_ids)`

`detect_patterns` is currently an alias-style first-batch pattern entry point that delegates to Fair Value Gap detection.

## Algorithm

Fair Value Gap detection scans three-candle windows:

- bullish FVG: candle 1 high is below candle 3 low;
- bearish FVG: candle 1 low is above candle 3 high.

For each gap, the detector enriches candles with ATR and Volume Ratio, calculates displacement candle rows, and evaluates the three-candle gap. The event includes gap boundaries, gap size, ATR-normalized gap size, fill percentage, mitigation state, volume ratio, displacement confirmation, optional liquidity/spread pass values, score, and reason.

## Major Validation Phases

- Candle normalization and sorted timestamp validation.
- External filter validation for required liquidity/spread settings.
- ATR calculation for gap-size normalization.
- Volume Ratio calculation for volume confirmation.
- Displacement Candle detection for optional/bonus confirmation.
- Three-candle gap candidate construction.
- State classification: open, partial fill, filled/mitigated, or invalid.
- Pattern score calculation from gap size, displacement, volume, mitigation state, and external filter context.
- Status classification into `VALID` or `WEAK` when emitted.
- Stable event identifier generation from pattern type, direction, symbol, timeframe, and relevant timestamps/prices.

## Implemented Versus Deferred Behavior

Implemented behavior is limited to deterministic candle-gap events. Liquidity and spread checks are not calculated internally. The helper `filter_new_events` only filters by caller-provided `seen_event_ids`; it does not persist global state.

# Trendline Break

Primary detector function:

- `detect_trendline_breaks(candles, symbol=None, timeframe=None, config=None)`

## Algorithm

Trendline Break detection builds candidate trendlines from visible confirmed pivots and evaluates whether the current candle breaks a trendline with sufficient ATR buffer and volume confirmation.

The detector enriches candles with ATR and Volume Ratio, detects pivots, optionally filters to confirmed pivots, detects displacement candles, and then iterates over each current candle index. For each index, it selects visible pivots already confirmed by that point and inside the configured lookback. It builds trendline candidates from pivot highs and pivot lows.

Implemented trendline types:

- descending resistance, typically evaluated for bullish breaks above the line;
- ascending support, typically evaluated for bearish breaks below the line.

## Major Validation Phases

- Candle normalization and sorted timestamp validation.
- External liquidity/spread requirement validation.
- ATR and Volume Ratio enrichment.
- Pivot detection and optional confirmed-pivot filtering.
- Displacement Candle detection when displacement bonus is enabled.
- Visible-pivot filtering by confirmation index and maximum lookback.
- Candidate construction from pivot pairs/multi-touch groups.
- Slope, length, and touch-deviation validation.
- Breakout/breakdown validation using ATR buffer and close price.
- Volume classification using minimum and weak volume thresholds.
- Optional displacement bonus.
- Event scoring and best-event selection per current index.
- Stable event identifier generation.

## Implemented Versus Deferred Behavior

The detector computes trendline geometry and break events directly. It does not invoke Swing Structure or Support / Resistance Zone modules, even though the mechanical source document lists them as contextual modules. Liquidity/spread filters remain external explicit values.

# Order Block

Primary detector function:

- `detect_order_blocks(candles, symbol=None, timeframe=None, config=None)`

## Algorithm

Order Block detection identifies the last opposite-color source candle before a valid directional displacement candle:

- bullish order block: the last bearish candle before a bullish displacement;
- bearish order block: the last bullish candle before a bearish displacement.

The detector enriches candles with ATR and Volume Ratio, detects displacement candles, and evaluates each valid displacement candle as a potential order-block confirmation. It searches backward for the source candle within the configured lookback and constructs a demand/supply zone from the source candle according to the configured zone definition.

Zone definition options include using the full candle range or body-based boundaries. The event records zone low, zone high, zone midpoint, zone size, ATR-normalized zone size, source/displacement indices, mitigation state/depth, volume ratio, score, and deterministic reference prices.

## Major Validation Phases

- Candle normalization and sorted timestamp validation.
- External liquidity/spread requirement validation.
- ATR and Volume Ratio enrichment.
- Displacement Candle detection using an order-block-specific displacement config.
- Source candle lookup before displacement.
- Zone boundary construction.
- Zone-size validation with ATR-normalized minimum and maximum bounds.
- State classification as fresh, touched, mitigated, or broken based on later candles.
- Pattern score calculation from displacement strength, volume, zone quality, liquidity context, support/resistance context placeholder scoring, and freshness.
- Status classification into `VALID`, `WEAK`, or rejection.
- Stable event identifier generation.

## Implemented Versus Deferred Behavior

Order Block detection does not implement order execution or live order placement. The score includes mechanical placeholders for contextual concepts, but liquidity/spread and full support/resistance context are not computed by reusable modules inside the detector.

# Cup And Handle

Primary detector function:

- `detect_cup_and_handle_patterns(candles, symbol=None, timeframe=None, config=None)`

## Algorithm

Cup and Handle detection is implemented for bullish completed breakout events. The detector uses pivot highs and pivot lows to build candidate structures:

1. a left rim pivot high;
2. a cup bottom pivot low;
3. a right rim pivot high;
4. a handle low pivot low;
5. a later breakout candle above the rim/neckline.

The detector enriches candles with ATR and Volume Ratio, detects pivots, optionally restricts them to confirmed pivots, detects displacement candles, and evaluates each visible pivot-derived candidate. It checks cup duration, cup depth, rim similarity, handle duration, handle depth, prior uptrend when required, breakout distance, volume ratio, and optional displacement confirmation.

## Major Validation Phases

- Candle normalization and sorted timestamp validation.
- External liquidity/spread requirement validation.
- ATR and Volume Ratio enrichment.
- Pivot detection and optional confirmed-pivot filtering.
- Displacement Candle detection.
- Candidate construction from ordered high-low-high-low pivot sequences.
- Prior-uptrend validation when enabled.
- Cup depth and ATR-normalized height validation.
- Rim similarity validation.
- Handle depth/duration validation.
- Breakout ATR-buffer validation above the neckline/rim.
- Volume threshold validation, with weak and strong classifications.
- Pattern score calculation and best-event selection.
- Stable event identifier generation.

## Implemented Versus Deferred Behavior

Only bullish cup-and-handle breakout events are emitted. The detector does not implement bearish/inverted cup-and-handle behavior or trade execution.

# Diamond

Primary detector function:

- `detect_diamond_patterns(candles, symbol=None, timeframe=None, config=None)`

## Algorithm

Diamond Pattern detection builds pivot-window candidates that show expansion followed by contraction. It uses confirmed pivot highs and lows to fit upper and lower boundary lines and then evaluates a breakout candle.

The candidate must show a broadening/expansion phase and a narrowing/contraction phase. The detector measures expansion and contraction slopes, paired high/low ranges, contraction range change, pattern height, ATR-normalized height, breakout distance, volume ratio, optional displacement confirmation, and reference risk/reward fields.

The first implementation supports completed breakout events. Direction is determined by the breakout relative to the upper or lower boundary.

## Major Validation Phases

- Candle normalization and sorted timestamp validation.
- External liquidity/spread requirement validation.
- ATR and Volume Ratio enrichment.
- Pivot detection and optional confirmed-pivot filtering.
- Displacement Candle detection.
- Visible-pivot filtering by confirmation index and lookback.
- Candidate construction from rolling pivot windows.
- Expansion-phase validation.
- Contraction-phase validation.
- Boundary line fitting and boundary value calculation.
- Pattern-height and ATR-normalized range validation.
- Breakout validation with ATR buffer.
- Volume and optional displacement validation.
- Pattern scoring and best-event selection.
- Stable event identifier generation.

## Implemented Versus Deferred Behavior

The detector calculates diamond geometry from pivots; it does not use order-book data, liquidity modules, or bid-ask spread modules internally. It emits analysis events only.

# Adam And Eve

Primary detector function:

- `detect_adam_and_eve_patterns(candles, symbol=None, timeframe=None, config=None)`

## Algorithm

Adam and Eve Pattern detection is implemented for bullish completed breakout events. It looks for a double-bottom structure:

1. a sharp Adam pivot low;
2. a neckline pivot high;
3. a more rounded Eve pivot low;
4. a later breakout above the neckline.

The detector enriches candles with ATR and Volume Ratio, detects pivots, optionally filters to confirmed pivots, and evaluates ordered low-high-low pivot candidates. It checks bottom similarity, pattern duration, Adam sharpness, Eve roundness, Eve-to-Adam duration ratio, prior downtrend when required, pattern height, breakout ATR buffer, breakout volume ratio, and optional displacement confirmation.

## Major Validation Phases

- Candle normalization and sorted timestamp validation.
- External liquidity/spread requirement validation.
- ATR and Volume Ratio enrichment.
- Pivot detection and optional confirmed-pivot filtering.
- Displacement Candle detection.
- Candidate construction from ordered low-high-low pivot sequences.
- Prior-downtrend validation when enabled.
- Adam local sharpness validation.
- Eve bottom-zone duration and roundness validation.
- Bottom similarity validation.
- Pattern-height validation using ATR.
- Breakout validation above the neckline with ATR buffer.
- Volume validation with weak and strong thresholds.
- Pattern scoring and best-event selection.
- Stable event identifier generation.

## Implemented Versus Deferred Behavior

Only bullish Adam and Eve breakout events are emitted. Liquidity and bid-ask spread modules remain unavailable; the detector validates explicit config pass/fail values only when required.

# Event Output Style

Pattern detectors return lists of frozen event dataclass instances rather than DataFrames. Event fields vary by pattern, but common fields include:

- `event_id`
- `pattern_type`
- `direction`
- `pattern_status`
- `symbol`
- `timeframe`
- `timestamp`
- `start_index`
- `end_index`
- ATR and volume confirmation fields
- optional liquidity/spread pass fields
- `displacement_confirmed` where relevant
- `pattern_score`
- reference prices and `risk_reward` where implemented
- `reason`

Empty or insufficient input returns an empty list after normalization/validation. Missing required columns, invalid numeric data, unsorted timestamps, and impossible config combinations raise `ValueError`.

# Deferred Or Unavailable Filters

The source pattern documents reference liquidity and bid-ask spread checks. In the current codebase:

- reusable liquidity and bid-ask spread indicator modules are not present;
- pattern configs default to not requiring those filters in detectors where the first implementation cannot compute them;
- when a config sets `require_liquidity_pass=True` or `require_spread_pass=True`, the corresponding explicit pass/fail value must be supplied;
- detectors do not infer those filters from volume ratio or candle prices.
