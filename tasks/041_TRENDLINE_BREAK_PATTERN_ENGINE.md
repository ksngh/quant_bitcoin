# Task 041: Trendline Break Pattern Detection Engine

# Goal

Create the next pattern implementation assignment for the pattern detection engine: deterministic Trendline Break detection from completed candle data and confirmed pivot-derived structure.

This task is an implementation task document only. It authorizes future implementation when the owner explicitly prompts `Mode: implement`; it does not implement code by itself.

# Source Requirement

The owner asked to create the next pattern task after the first Fair Value Gap detector batch.

Task 040 implemented the first narrow Fair Value Gap batch. The next deferred pattern listed in `tasks/040_PATTERN_DETECTION_ENGINE.md` is Trendline Break, and its mechanical definition is saved at `tasks/patterns/trendline_break_pattern.md`.

# Clean Requirement

Add a future implementation task for a pure Trendline Break detector that consumes normalized completed candles, reuses existing indicator outputs where applicable, builds deterministic two-point trendlines from confirmed pivot highs/lows, evaluates bullish and bearish break conditions from the owner-approved mechanical definition, and returns stable pattern event records.

The future implementation must remain independent of WebSocket clients, exchange clients, databases, paper trading, backtesting runners, order execution, live trading, and risk management. Future WebSocket or backtest callers should be able to pass rolling or historical completed-candle windows into the pure detector.

# Extracted Roles

- Owner role: Trendline Break pattern recognition from completed candle data and confirmed pivot-derived structure.
- Supporting roles:
  - Market Data Contract, for normalized candle input shape.
  - Indicator modules, for Pivot High / Pivot Low, Swing Structure, ATR, Volume Ratio, Support / Resistance Zone, and optional Displacement Candle calculations where applicable.
  - Pattern Detection Engine, for stable pattern event output and rolling-window duplicate prevention.
  - WebSocket ingestion, only as a future caller that supplies rolling completed candles.
  - Backtesting, only as a future caller that supplies historical candle batches.
  - Test Designer, for deterministic trendline event tests.
- Forbidden roles:
  - Live trading and real Binance order execution.
  - Paper order placement or real order placement.
  - Risk management, dashboard, database, scheduler, FastAPI, Streamlit, Docker, machine learning, futures, leverage, or portfolio optimization.
  - Market data fetching, because the detector consumes candles supplied by callers.

# Responsibility Boundary

The future Trendline Break detector is responsible for:

- Validating input candles against the standard schema in `docs/04_DATA_CONTRACT.md`.
- Evaluating completed candles in ascending timestamp order.
- Reusing existing indicator modules instead of duplicating indicator logic.
- Building initial trendlines using the owner-recommended two-point method from confirmed pivots.
- Detecting bullish breaks above descending resistance trendlines and bearish breaks below ascending support trendlines.
- Returning deterministic event records with stable event identifiers.
- Supporting repeated rolling-window calls without direct knowledge of WebSocket internals.

The future Trendline Break detector is not responsible for:

- Opening WebSocket connections.
- Fetching data from Binance or any exchange.
- Reading API keys or environment secrets.
- Persisting detected events to a database.
- Creating strategy BUY / SELL / HOLD signals.
- Placing paper or real orders.
- Managing position sizing, stops, risk limits, or portfolio allocation.
- Implementing missing liquidity or bid-ask spread modules unless this task is explicitly amended.
- Implementing regression trendlines, complex multi-trendline state, or false-break lifecycle tracking in the first Trendline Break batch unless it remains small and deterministic.

# Existing Context To Review Before Implementation

## Project Workflow And Contracts

- `AGENTS.md`
- `STATUS.md`
- `docs/10_CODEX_COMMAND_GUIDE.md`
- `docs/04_DATA_CONTRACT.md`
- `docs/03_ARCHITECTURE_RULES.md`
- `reviews/CODEX_SELF_REVIEW.md`

## Pattern Engine Context

- `tasks/040_PATTERN_DETECTION_ENGINE.md`
- `quant_bitcoin/patterns/fair_value_gap.py`
- `quant_bitcoin/patterns/__init__.py`
- `tests/patterns/test_fair_value_gap.py`

Review the existing Fair Value Gap implementation for reusable conventions only. Do not silently redesign the public pattern event contract; if a shared contract change is required, stop and ask the owner for approval.

## Existing Indicator Implementation Tasks And Modules

Review these task documents and implementation modules before coding:

- `tasks/028_IMPLEMENT_PIVOT_HIGH_LOW.md`
- `tasks/029_IMPLEMENT_SWING_STRUCTURE.md`
- `tasks/030_IMPLEMENT_ATR.md`
- `tasks/031_IMPLEMENT_VOLUME_RATIO.md`
- `tasks/032_IMPLEMENT_SUPPORT_RESISTANCE_ZONE.md`
- `tasks/033_IMPLEMENT_DISPLACEMENT_CANDLE.md`
- `tasks/indicators/pivot_high_low.md`
- `tasks/indicators/swing_structure.md`
- `tasks/indicators/atr.md`
- `tasks/indicators/volume_ratio.md`
- `tasks/indicators/support_resistance_zone.md`
- `quant_bitcoin/indicators/pivots.py`
- `quant_bitcoin/indicators/swing_structure.py`
- `quant_bitcoin/indicators/atr.py`
- `quant_bitcoin/indicators/volume_ratio.py`
- `quant_bitcoin/indicators/support_resistance_zone.py`
- `quant_bitcoin/indicators/displacement_candle.py`

Also review these known source requirements before deciding whether to enforce or defer filters:

- `tasks/027_IMPLEMENT_BID_ASK_SPREAD.md`
- `tasks/indicators/liquidity.md`

If a required filter does not have an implemented reusable module, the implementation must explicitly handle that limitation by keeping the filter out of the first Trendline Break batch, requiring explicit caller-supplied pass/fail values, marking the result unavailable/unknown according to the mechanical definition, or stopping for owner approval. Do not implement unrelated prerequisite indicators inside this task unless amended.

## Pattern Mechanical Definition

Use this document as the source of truth:

- `tasks/patterns/trendline_break_pattern.md`

# First Trendline Break Implementation Batch

Include only this pattern:

- Trendline Break (`tasks/patterns/trendline_break_pattern.md`)

Required first-batch direction support:

- Bullish Trendline Break: close breaks above a descending resistance trendline built from confirmed pivot highs.
- Bearish Trendline Break: close breaks below an ascending support trendline built from confirmed pivot lows.

Recommended first-batch constraints:

- Use two-point trendline construction first.
- Use confirmed pivots only.
- Require at least `minimum_touch_count = 2` source pivots.
- Use the latest eligible trendline break candidates and select the best deterministic candidate if multiple exist.
- Emit events only for `VALID`, `WEAK`, or `PENDING` candidates unless invalid-result emission is explicitly chosen and tested.
- Keep false-break lifecycle tracking out of the first implementation unless it can be represented deterministically without persistent state.

# Deferred Work

Defer these until follow-up tasks explicitly assign them:

- Regression or multi-touch line fitting beyond the initial two-point method.
- Long-lived false-break state tracking.
- Trendline merge/de-duplication beyond deterministic best-candidate selection.
- WebSocket integration.
- Backtest runner integration.
- Database persistence of pattern events.
- Order Block, Cup and Handle, Diamond, and Adam and Eve pattern implementations.
- Missing Liquidity or Bid-Ask Spread modules.

# Scope

- Add or extend a pure pattern detection module under `quant_bitcoin/patterns/` for Trendline Break detection.
- Add small configuration and event result types only as needed for Trendline Break fields.
- Reuse existing indicator modules for pivots, ATR, Volume Ratio, Swing Structure, Support / Resistance Zone, and optional Displacement Candle where applicable.
- Add package exports only if needed for callers and tests.
- Add deterministic unit tests for bullish, bearish, weak, pending, invalid, rolling-window, stable-ID, and input-validation behavior.
- Update `STATUS.md` during implementation if phase, step, goal, active task, blockers, open questions, or completion state changes.

# Out of Scope

- Implementing code during this task-document creation step.
- Modifying WebSocket ingestion behavior.
- Modifying backtest runner behavior.
- Implementing live trading.
- Implementing real Binance order execution.
- Adding exchange order API calls.
- Adding paper order placement.
- Adding risk management, dashboard, database, scheduler, FastAPI, Streamlit, Docker, machine learning, futures, leverage, or portfolio optimization.
- Redesigning existing public market data, signal, strategy, backtest, execution, or pattern contracts without explicit owner approval.
- Implementing deferred patterns listed above.
- Implementing missing liquidity or bid-ask spread indicator modules unless the owner explicitly amends this task.
- Hardcoding API keys or secrets.
- Committing `.env` files.

# Proposed Input Contract

The future detector should accept:

- `candles`: a rolling or historical sequence of completed candles using the standard schema:
  - `timestamp`
  - `open`
  - `high`
  - `low`
  - `close`
  - `volume`
- Optional `symbol`.
- Optional `timeframe`.
- Optional Trendline Break config.
- Optional precomputed indicator outputs only if doing so avoids recomputation and does not introduce contract ambiguity.

Input rules:

- Candles must be sorted ascending by `timestamp`; choose and document whether unsorted input is rejected or deterministically sorted.
- Only completed candles should be evaluated.
- Missing required OHLCV columns or invalid numeric values must fail deterministically with clear errors.
- Fewer than the minimum candles/pivots required for a confirmed trendline must return an empty list or a documented invalid result.
- The detector must not mutate caller-provided candle data in place.

# Proposed Output Contract

The future detector should return pattern event records exposing at least:

- `event_id`: stable deterministic identifier for duplicate prevention.
- `pattern_type`: fixed value `TRENDLINE_BREAK`.
- `direction`: `BULLISH`, `BEARISH`, or `NONE`.
- `pattern_status`: `VALID`, `WEAK`, `PENDING`, or `INVALID` when emitted.
- `symbol`: caller-supplied symbol, if available.
- `timeframe`: caller-supplied timeframe, if available.
- `timestamp`: event timestamp using the completed breakout/breakdown candle timestamp.
- `start_index` / `end_index` or equivalent source-candle indices.
- `trendline_type`: `DESCENDING_RESISTANCE`, `ASCENDING_SUPPORT`, or `INVALID`.
- `trendline_slope`.
- `trendline_intercept`.
- `touch_count`.
- `source_pivot_indices`.
- `trendline_value` at the break candle.
- `break_price`.
- `break_distance`.
- `break_distance_atr`.
- `atr`.
- `volume_ratio`.
- `liquidity_pass` and `spread_pass` when available or explicitly supplied.
- `displacement_confirmed` when evaluated.
- `pattern_score`.
- `entry_reference`, `stop_reference`, `target_reference`, and `risk_reward` as reference values only, never order instructions.
- `reason`: concise deterministic reason.

Stable `event_id` guidance:

- Build `event_id` from immutable event-defining fields such as `pattern_type`, `direction`, `symbol`, `timeframe`, source pivot timestamps/indices, and breakout candle timestamp.
- Repeated calls over overlapping rolling windows must return the same `event_id` for the same completed Trendline Break event.
- The detector may return all matching events in the supplied window; the caller may suppress duplicates by tracking seen `event_id` values.

# Mechanical Rules To Implement

Use the owner definition from `tasks/patterns/trendline_break_pattern.md`.

## Bullish Trendline Break

- Use confirmed pivot highs.
- Build a descending resistance trendline from pivot highs.
- Require `touch_count >= minimum_touch_count`.
- Require `slope < 0` and reject flat trendlines according to config.
- Calculate `trendline_value` at the current candle.
- Require `close > trendline_value + breakout_atr_multiplier * ATR` for a valid break.
- Use breakout candle `volume_ratio` for volume confirmation.
- Classify weak/pending/invalid behavior according to the mechanical definition.

## Bearish Trendline Break

- Use confirmed pivot lows.
- Build an ascending support trendline from pivot lows.
- Require `touch_count >= minimum_touch_count`.
- Require `slope > 0` and reject flat trendlines according to config.
- Calculate `trendline_value` at the current candle.
- Require `close < trendline_value - breakout_atr_multiplier * ATR` for a valid break.
- Use breakdown candle `volume_ratio` for volume confirmation.
- Classify weak/pending/invalid behavior according to the mechanical definition.

# Default Parameters

Use the owner defaults unless a reviewed implementation reason requires a documented deviation:

```yaml
trendline_break:
  minimum_touch_count: 2
  strong_touch_count: 3
  maximum_pivot_lookback: 50
  minimum_trendline_length: 10
  maximum_trendline_length: 200
  minimum_slope_abs: 0.0
  maximum_slope_abs: null
  maximum_allowed_touch_deviation_atr: 0.5
  breakout_atr_multiplier: 0.2
  minimum_volume_ratio: 1.5
  weak_volume_ratio: 1.3
  require_liquidity_pass: true
  require_spread_pass: true
  require_confirmed_pivots: true
  allow_displacement_bonus: true
  minimum_pattern_score: 0.7
```

# Open Questions Before Implementation

Resolve or document these before coding if not already clear from reviewed files:

- Should the first Trendline Break implementation require liquidity and bid-ask spread filters while reusable modules are unavailable, or should it follow the Fair Value Gap approach of making them optional/unavailable unless explicitly supplied?
- Should the detector emit `PENDING` events for trendlines that exist but have not broken with ATR buffer, or only `VALID` / `WEAK` completed break events?
- Should the implementation return all matching candidates or only the best deterministic candidate per candle?
- Which pivot selection rule should be used when more than two eligible pivots exist: latest two, highest score pair, or all pairs with deterministic best-candidate selection?
- Should default ATR and Volume Ratio warmup settings use production defaults or small test-specific configs only in tests?
- What minimum rolling lookback should future WebSocket callers retain for pivot confirmation plus trendline construction?

# Status Tracking

## Before Implementation

- [ ] Read `STATUS.md`.
- [ ] Confirm this task matches the current phase and step.
- [ ] Confirm the active task is recorded or should be updated.
- [ ] Confirm parallel work is not needed for this implementation batch.
- [ ] Record assumptions, blockers, or unclear status items before coding.

## After Implementation

- [ ] Update `STATUS.md` if the phase, step, goal, active task, blocker, open question, or completion state changed.
- [ ] Mark checklist items complete only when acceptance criteria and verification are satisfied.
- [ ] Leave uncertain items open and document the uncertainty.
- [ ] Confirm the next step is accurate or explicitly left undecided.

# Acceptance Criteria

- A pure Trendline Break detector exists when the implementation task is later executed.
- The detector accepts rolling or historical completed candle data using the existing candle data contract.
- The detector returns deterministic Trendline Break event records for bullish and bearish structures.
- Repeated calls over overlapping rolling windows produce stable event identifiers for the same completed pattern.
- The detector can be used from future WebSocket ingestion code without importing or depending on exchange clients.
- Existing indicator modules are reused where applicable.
- Missing prerequisite filters are handled explicitly rather than silently approximated.
- No live trading, real Binance order execution, exchange order API calls, risk management, dashboard, database, scheduler, FastAPI, Streamlit, Docker, machine learning, futures, leverage, or portfolio optimization is added.
- Tests cover required behavior.
- `STATUS.md` is updated only for actual project-state changes.

# Required Tests

## Unit Tests

Add deterministic tests for:

- No pattern detected when candles/pivots do not satisfy Trendline Break rules.
- One bullish Trendline Break event detected from a minimal valid descending-resistance sequence.
- One bearish Trendline Break event detected from a minimal valid ascending-support sequence.
- Insufficient candle or pivot history returns an empty list or documented invalid result.
- Flat trendlines are rejected or ignored according to config.
- Break without ATR buffer is `PENDING` if pending emission is implemented; otherwise it is not emitted and the behavior is documented.
- Weak volume produces `WEAK` if weak emission is implemented.
- Missing ATR or Volume Ratio inputs fail deterministically or result in no event according to the documented implementation choice.
- Rolling/windowed detection behavior as new completed candles are appended.
- Stable `event_id` for the same completed pattern across overlapping rolling-window calls.
- No duplicate event emission for the same completed pattern when using the documented `seen_event_ids` caller pattern or optional helper.
- Missing required candle columns raise a clear deterministic error.
- Unsorted candle input behavior matches the documented implementation choice.

## Integration Tests

- Not required for the first Trendline Break implementation unless the owner explicitly asks for WebSocket or backtest wiring.
- If a lightweight integration-style test is added, it must call only the pure detector with in-memory candle data.

## Contract Tests

- Verify the detector accepts the existing standard candle schema.
- Verify returned event records expose the required common fields and Trendline Break fields.
- Verify the detector does not require Binance-specific raw fields.
- Verify existing public pattern API compatibility is not broken unless owner-approved.

## Safety Tests

- Verify implementation imports do not introduce exchange order clients or order execution dependencies.
- Verify tests do not call real exchange endpoints.
- Verify no API keys, `.env` files, or live-trading toggles are required.

# Verification

Default verification for future implementation:

```bash
pytest
```

Additional targeted verification recommended:

```bash
pytest tests/patterns
```

Documentation/task creation verification:

```bash
git diff --check
```

Manual review must compare this task and the eventual implementation against:

- `AGENTS.md`
- `STATUS.md`
- `docs/10_CODEX_COMMAND_GUIDE.md`
- `docs/04_DATA_CONTRACT.md`
- relevant indicator task documents
- `tasks/patterns/trendline_break_pattern.md`
- existing pattern engine code and tests

# Codex Self-Review Requirement

Before completion of any implementation work under this task, run through `reviews/CODEX_SELF_REVIEW.md` and include the result in the final summary.

For this task-document creation step, perform the same self-review at documentation scope and confirm no application behavior was implemented.

# PR Review Requirement

Use `reviews/REVIEW_CHECKLIST.md` and `docs/06_PR_REVIEW_PROCESS.md` before merge.

Review must be strict about:

- Scope expansion beyond Trendline Break and the minimal detector contract.
- Missing deterministic rolling-window tests.
- Missing stable event identifiers.
- Duplicate indicator logic instead of reusing existing modules.
- Architecture boundary violations.
- Data contract violations.
- Hardcoded secrets.
- Unsafe live trading behavior.
- Accidental exchange order calls.
- Unnecessary abstractions.

# Completion Summary Required

- files changed
- implementation summary
- tests added or updated
- tests run
- Codex self-review result
- known limitations
- recommended next task
