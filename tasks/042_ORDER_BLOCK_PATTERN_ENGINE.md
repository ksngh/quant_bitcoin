# Task 042: Order Block Pattern Detection Engine

# Goal

Create the next pattern implementation assignment for the pattern detection engine: deterministic Order Block detection from completed candle data and existing indicator snapshots.

This task is an implementation task document only. It authorizes future implementation when the owner explicitly prompts `Mode: implement`; it does not implement code by itself.

# Source Requirement

The owner asked to create the next pattern implementation task after Fair Value Gap and Trendline Break.

Task 040 implemented the Fair Value Gap detector. Task 041 implemented the Trendline Break detector. The next deferred pattern listed in `tasks/040_PATTERN_DETECTION_ENGINE.md` is Order Block, and its mechanical definition is saved at `tasks/patterns/order_block_pattern.md`.

# Clean Requirement

Add a future implementation task for a pure Order Block detector that consumes normalized completed candles, reuses existing indicator outputs where applicable, identifies bullish and bearish source candles or source clusters before valid displacement candles, builds deterministic supply/demand zones, evaluates zone state and references, and returns stable pattern event records.

The future implementation must remain independent of WebSocket clients, exchange clients, databases, paper trading, backtesting runners, order execution, live trading, and risk management. Future WebSocket or backtest callers should be able to pass rolling or historical completed-candle windows into the pure detector.

# Extracted Roles

- Owner role: Order Block pattern recognition from completed candle data and existing indicator snapshots.
- Supporting roles:
  - Market Data Contract, for normalized candle input shape.
  - Indicator modules, for ATR, Volume Ratio, Displacement Candle, Pivot High / Pivot Low, Swing Structure, and Support / Resistance Zone calculations where applicable.
  - Pattern Detection Engine, for stable pattern event output and rolling-window duplicate prevention.
  - WebSocket ingestion, only as a future caller that supplies rolling completed candles.
  - Backtesting, only as a future caller that supplies historical candle batches.
  - Test Designer, for deterministic order-block event tests.
- Forbidden roles:
  - Live trading and real Binance order execution.
  - Paper order placement or real order placement.
  - Risk management, dashboard, database, scheduler, FastAPI, Streamlit, Docker, machine learning, futures, leverage, or portfolio optimization.
  - Market data fetching, because the detector consumes candles supplied by callers.

# Responsibility Boundary

The future Order Block detector is responsible for:

- Validating input candles against the standard schema in `docs/04_DATA_CONTRACT.md`.
- Evaluating completed candles in ascending timestamp order.
- Reusing existing indicator modules instead of duplicating indicator logic.
- Finding the nearest opposing source candle before a valid displacement candle.
- Optionally expanding to a deterministic source cluster only if it remains simple and covered by tests.
- Building order-block zones according to the configured zone definition.
- Validating displacement, volume, ATR, zone size, liquidity/spread availability, and optional structure/context rules.
- Classifying order-block state from subsequent candles.
- Returning deterministic event records with stable event identifiers.
- Supporting repeated rolling-window calls without direct knowledge of WebSocket internals.

The future Order Block detector is not responsible for:

- Opening WebSocket connections.
- Fetching data from Binance or any exchange.
- Reading API keys or environment secrets.
- Persisting detected events to a database.
- Creating strategy BUY / SELL / HOLD signals.
- Placing paper or real orders.
- Managing position sizing, stops, risk limits, or portfolio allocation.
- Implementing missing liquidity or bid-ask spread modules unless this task is explicitly amended.
- Implementing dashboard, API, scheduler, UI, Docker, or ML behavior.

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
- `tasks/041_TRENDLINE_BREAK_PATTERN_ENGINE.md`
- `quant_bitcoin/patterns/fair_value_gap.py`
- `quant_bitcoin/patterns/trendline_break.py`
- `quant_bitcoin/patterns/__init__.py`
- `tests/patterns/test_fair_value_gap.py`
- `tests/patterns/test_trendline_break.py`

Review the existing Fair Value Gap and Trendline Break implementations for reusable conventions only. Do not silently redesign the public pattern event contract; if a shared contract change is required, stop and ask the owner for approval.

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

If a required filter does not have an implemented reusable module, the implementation must explicitly handle that limitation by keeping the filter out of the first Order Block batch, requiring explicit caller-supplied pass/fail values, marking the result unavailable/unknown according to the mechanical definition, or stopping for owner approval. Do not implement unrelated prerequisite indicators inside this task unless amended.

## Pattern Mechanical Definition

Use this document as the source of truth:

- `tasks/patterns/order_block_pattern.md`

# First Order Block Implementation Batch

Include only this pattern:

- Order Block (`tasks/patterns/order_block_pattern.md`)

Required first-batch direction support:

- Bullish Order Block: nearest bearish source candle before a valid bullish displacement candle, defining a bullish demand zone.
- Bearish Order Block: nearest bullish source candle before a valid bearish displacement candle, defining a bearish supply zone.

Recommended first-batch constraints:

- Prefer single-candle source order blocks first.
- Use `FULL_RANGE` zone definition first.
- Use existing ATR, Volume Ratio, and Displacement Candle modules for displacement and validation.
- Treat source-cluster support as optional; include it only if implementation remains deterministic and tests cover it.
- Emit `VALID` and `WEAK` completed order-block events by default.
- Defer optional `PENDING` source-candidate events unless explicitly implemented and tested.
- Classify `FRESH`, `TOUCHED`, `MITIGATED`, and `BROKEN` from candles after displacement when possible.

# Deferred Work

Defer these until follow-up tasks explicitly assign them:

- Complex multi-candle source-cluster selection beyond nearest deterministic opposing candles.
- `BODY_ONLY` and `WICK_ADJUSTED` zones unless the first implementation remains small and fully tested.
- Long-lived order-block lifecycle persistence.
- Order-block merging or consumer-side zone consolidation.
- WebSocket integration.
- Backtest runner integration.
- Database persistence of pattern events.
- Cup and Handle, Diamond, and Adam and Eve pattern implementations.
- Missing Liquidity or Bid-Ask Spread modules.

# Scope

- Add or extend a pure pattern detection module under `quant_bitcoin/patterns/` for Order Block detection.
- Add small configuration and event result types only as needed for Order Block fields.
- Reuse existing indicator modules for ATR, Volume Ratio, Displacement Candle, Pivot, Swing Structure, and Support / Resistance Zone where applicable.
- Add package exports only if needed for callers and tests.
- Add deterministic unit tests for bullish, bearish, weak, invalid, state, rolling-window, stable-ID, and input-validation behavior.
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
- Optional Order Block config.
- Optional precomputed indicator outputs only if doing so avoids recomputation and does not introduce contract ambiguity.

Input rules:

- Candles must be sorted ascending by `timestamp`; choose and document whether unsorted input is rejected or deterministically sorted.
- Only completed candles should be evaluated.
- Missing required OHLCV columns or invalid numeric values must fail deterministically with clear errors.
- Fewer than the minimum candles required for a source plus displacement structure must return an empty list or a documented invalid result.
- The detector must not mutate caller-provided candle data in place.

# Proposed Output Contract

The future detector should return pattern event records exposing at least:

- `event_id`: stable deterministic identifier for duplicate prevention.
- `pattern_type`: fixed value `ORDER_BLOCK`.
- `direction`: `BULLISH`, `BEARISH`, or `NONE`.
- `pattern_status`: `VALID`, `WEAK`, `PENDING`, or `INVALID` when emitted.
- `symbol`: caller-supplied symbol, if available.
- `timeframe`: caller-supplied timeframe, if available.
- `timestamp`: event timestamp using the displacement candle timestamp.
- `start_index` / `end_index` or equivalent source/displacement candle indices.
- `order_block_state`: `FRESH`, `TOUCHED`, `MITIGATED`, `BROKEN`, or `INVALID`.
- `source_candle_index`.
- `source_candle_timestamp`.
- `displacement_candle_index`.
- `displacement_candle_timestamp`.
- `zone_low`.
- `zone_high`.
- `zone_mid`.
- `zone_size`.
- `zone_size_atr`.
- `source_mode`.
- `source_cluster_start_index` and `source_cluster_end_index` when clusters are implemented.
- `zone_definition`.
- `displacement_direction`.
- `displacement_range_atr`.
- `body_ratio`.
- `volume_ratio`.
- `liquidity_pass` and `spread_pass` when available or explicitly supplied.
- `structure_confirmed` and `structure_event` when evaluated.
- `support_resistance_context` when evaluated.
- `mitigation_depth`.
- `pattern_score`.
- `entry_reference`, `stop_reference`, `target_reference`, and `risk_reward` as reference values only, never order instructions.
- `reason`: concise deterministic reason.

Stable `event_id` guidance:

- Build `event_id` from immutable event-defining fields such as `pattern_type`, `direction`, `symbol`, `timeframe`, source candle timestamp(s), and displacement candle timestamp.
- Repeated calls over overlapping rolling windows must return the same `event_id` for the same completed Order Block event.
- The detector may return all matching events in the supplied window; the caller may suppress duplicates by tracking seen `event_id` values.

# Mechanical Rules To Implement

Use the owner definition from `tasks/patterns/order_block_pattern.md`.

## Bullish Order Block

- Find a valid bullish displacement candle.
- Find the nearest bearish source candle before displacement within `source_search_lookback`.
- Require displacement direction `BULLISH` and status `VALID`.
- Require displacement range, body ratio, ATR, close-location, and volume confirmation to satisfy the configured thresholds.
- Build a bullish demand zone from the source candle or source cluster.
- Validate zone size against ATR.
- Classify state from candles after displacement.
- Assign `VALID`, `WEAK`, or no event / invalid according to hard filters, volume, state, and score.

## Bearish Order Block

- Find a valid bearish displacement candle.
- Find the nearest bullish source candle before displacement within `source_search_lookback`.
- Require displacement direction `BEARISH` and status `VALID`.
- Require displacement range, body ratio, ATR, close-location, and volume confirmation to satisfy the configured thresholds.
- Build a bearish supply zone from the source candle or source cluster.
- Validate zone size against ATR.
- Classify state from candles after displacement.
- Assign `VALID`, `WEAK`, or no event / invalid according to hard filters, volume, state, and score.

# Default Parameters

Use the owner defaults unless a reviewed implementation reason requires a documented deviation:

```yaml
order_block:
  source_search_lookback: 5
  allow_single_candle_order_block: true
  allow_multi_candle_order_block: true
  maximum_source_cluster_size: 3
  zone_definition: FULL_RANGE
  allow_body_only_zone: true
  allow_wick_adjusted_zone: true
  require_displacement: true
  minimum_displacement_body_ratio: 0.6
  minimum_displacement_atr_multiplier: 1.5
  minimum_volume_ratio: 1.5
  weak_volume_ratio: 1.3
  close_extreme_threshold: 0.25
  require_liquidity_pass: true
  require_spread_pass: true
  require_structure_confirmation: false
  minimum_zone_size_atr_multiplier: 0.1
  maximum_zone_size_atr_multiplier: 2.0
  mitigation_threshold: 0.5
  broken_atr_buffer_multiplier: 0.2
  stop_atr_buffer_multiplier: 0.2
  minimum_pattern_score: 0.7
  weak_pattern_score: 0.5
  default_entry_reference: ZONE_MID
  default_risk_reward: 2.0
```

# Open Questions Before Implementation

Resolve or document these before coding if not already clear from reviewed files:

- Should the first Order Block implementation require liquidity and bid-ask spread filters while reusable modules are unavailable, or should it follow existing detector behavior of making them optional/unavailable unless explicitly supplied?
- Should the first implementation emit `PENDING` source candidates, or only completed `VALID` / `WEAK` order blocks after displacement?
- Should multi-candle source clusters be included in the first implementation, or deferred in favor of the nearest single opposing source candle?
- Which zone definition should be enabled by default in code: only `FULL_RANGE`, or configurable `FULL_RANGE` / `BODY_ONLY` / `WICK_ADJUSTED`?
- Should broken zones be omitted entirely or emitted as `INVALID` events when invalid emission is explicitly configured?
- What minimum rolling lookback should future WebSocket callers retain for source search, displacement validation, ATR/volume warmup, and post-displacement state classification?

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

- A pure Order Block detector exists when the implementation task is later executed.
- The detector accepts rolling or historical completed candle data using the existing candle data contract.
- The detector returns deterministic Order Block event records for bullish and bearish structures.
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

- No pattern detected when candles do not satisfy Order Block rules.
- One bullish Order Block event detected from a minimal valid source-plus-displacement sequence.
- One bearish Order Block event detected from a minimal valid source-plus-displacement sequence.
- Insufficient candle history returns an empty list or documented invalid result.
- Source candle not found behavior is deterministic.
- Zone size too small and too large behavior is deterministic.
- Weak displacement volume produces `WEAK` if weak emission is implemented.
- Missing ATR or Volume Ratio inputs fail deterministically or result in no event according to the documented implementation choice.
- `FRESH`, `TOUCHED`, `MITIGATED`, and `BROKEN` state classification when implemented.
- Broken zones are not emitted as valid order-block references.
- Rolling/windowed detection behavior as new completed candles are appended.
- Stable `event_id` for the same completed pattern across overlapping rolling-window calls.
- No duplicate event emission for the same completed pattern when using the documented `seen_event_ids` caller pattern or optional helper.
- Missing required candle columns raise a clear deterministic error.
- Unsorted candle input behavior matches the documented implementation choice.

## Integration Tests

- Not required for the first Order Block implementation unless the owner explicitly asks for WebSocket or backtest wiring.
- If a lightweight integration-style test is added, it must call only the pure detector with in-memory candle data.

## Contract Tests

- Verify the detector accepts the existing standard candle schema.
- Verify returned event records expose the required common fields and Order Block fields.
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
- `tasks/patterns/order_block_pattern.md`
- existing pattern engine code and tests

# Codex Self-Review Requirement

Before completion of any implementation work under this task, run through `reviews/CODEX_SELF_REVIEW.md` and include the result in the final summary.

For this task-document creation step, perform the same self-review at documentation scope and confirm no application behavior was implemented.

# PR Review Requirement

Use `reviews/REVIEW_CHECKLIST.md` and `docs/06_PR_REVIEW_PROCESS.md` before merge.

Review must be strict about:

- Scope expansion beyond Order Block and the minimal detector contract.
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
