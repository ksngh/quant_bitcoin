# Task 045: Adam and Eve Pattern Detection Engine

# Goal

Create the next pattern implementation assignment for the pattern detection engine: deterministic Adam and Eve Pattern detection from completed candle data and confirmed pivot-derived double-bottom structure.

This task is an implementation task document only. It authorizes future implementation when the owner explicitly prompts `Mode: implement`; it does not implement code by itself.

# Source Requirement

The owner asked to create the next pattern task before implementing another pattern, and asked what patterns remain.

Task 040 implemented the Fair Value Gap detector. Task 041 implemented the Trendline Break detector. Task 042 implemented the Order Block detector. Task 043 implemented the Cup and Handle detector. Task 044 implemented the Diamond Pattern detector. The remaining owner-provided pattern mechanical definition that has not yet received a pattern-engine implementation task is Adam and Eve Pattern, saved at `tasks/patterns/adam_and_eve_pattern.md`.

# Remaining Pattern Inventory

Implemented or already assigned in the pattern engine sequence:

- Fair Value Gap: implemented by Task 040.
- Trendline Break: implemented by Task 041.
- Order Block: implemented by Task 042.
- Cup and Handle: implemented by Task 043.
- Diamond Pattern: implemented by Task 044.

Remaining owner-provided pattern mechanical definitions:

- Adam and Eve Pattern: this Task 045 creates the future implementation assignment.

Not pattern implementations, but still relevant blockers/filters:

- Liquidity / trading value filter module is still unavailable as a reusable module.
- Bid-Ask Spread filter module is still unavailable as a reusable module.

# Clean Requirement

Add a future implementation task for a pure Adam and Eve Pattern detector that consumes normalized completed candles, reuses existing indicator outputs where applicable, identifies a bullish Adam-and-Eve double-bottom sequence from confirmed pivots, validates Adam sharpness, Eve roundness, bottom similarity, neckline breakout strength, and volume confirmation, and returns stable pattern event records.

The future implementation must remain independent of WebSocket clients, exchange clients, databases, paper trading, backtesting runners, order execution, live trading, and risk management. Future WebSocket or backtest callers should be able to pass rolling or historical completed-candle windows into the pure detector.

# Extracted Roles

- Owner role: Adam and Eve Pattern recognition from completed candle data and confirmed pivot-derived double-bottom structure.
- Supporting roles:
  - Market Data Contract, for normalized candle input shape.
  - Indicator modules, for Pivot High / Pivot Low, Swing Structure, ATR, Volume Ratio, Support / Resistance Zone, and optional Displacement Candle calculations where applicable.
  - Pattern Detection Engine, for stable pattern event output and rolling-window duplicate prevention.
  - WebSocket ingestion, only as a future caller that supplies rolling completed candles.
  - Backtesting, only as a future caller that supplies historical candle batches.
  - Test Designer, for deterministic Adam and Eve Pattern event tests.
- Forbidden roles:
  - Live trading and real Binance order execution.
  - Paper order placement or real order placement.
  - Risk management, dashboard, database, scheduler, FastAPI, Streamlit, Docker, machine learning, futures, leverage, or portfolio optimization.
  - Market data fetching, because the detector consumes candles supplied by callers.

# Responsibility Boundary

The future Adam and Eve Pattern detector is responsible for:

- Validating input candles against the standard schema in `docs/04_DATA_CONTRACT.md`.
- Evaluating completed candles in ascending timestamp order.
- Reusing existing indicator modules instead of duplicating indicator logic.
- Finding a bullish sequence of confirmed pivots: Adam low, neckline pivot, Eve low, and breakout candle.
- Validating prior downtrend handling, bottom similarity, pattern duration, Adam sharpness, Adam local range, Eve rounded-bottom quality, Eve-to-Adam duration ratio, pattern height, breakout ATR buffer, and breakout volume.
- Returning deterministic event records with stable event identifiers.
- Supporting repeated rolling-window calls without direct knowledge of WebSocket internals.

The future Adam and Eve Pattern detector is not responsible for:

- Opening WebSocket connections.
- Fetching data from Binance or any exchange.
- Reading API keys or environment secrets.
- Persisting detected events to a database.
- Creating strategy BUY / SELL / HOLD signals.
- Placing paper or real orders.
- Managing position sizing, stops, risk limits, or portfolio allocation.
- Implementing missing liquidity or bid-ask spread modules unless this task is explicitly amended.
- Implementing bearish inverted Adam and Eve support unless a future task explicitly assigns it.
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
- `tasks/042_ORDER_BLOCK_PATTERN_ENGINE.md`
- `tasks/043_CUP_AND_HANDLE_PATTERN_ENGINE.md`
- `tasks/044_DIAMOND_PATTERN_ENGINE.md`
- `tasks/patterns/adam_and_eve_pattern.md`
- `quant_bitcoin/patterns/fair_value_gap.py`
- `quant_bitcoin/patterns/trendline_break.py`
- `quant_bitcoin/patterns/order_block.py`
- `quant_bitcoin/patterns/cup_and_handle.py`
- `quant_bitcoin/patterns/diamond.py`
- `quant_bitcoin/patterns/__init__.py`
- `tests/patterns/test_fair_value_gap.py`
- `tests/patterns/test_trendline_break.py`
- `tests/patterns/test_order_block.py`
- `tests/patterns/test_cup_and_handle.py`
- `tests/patterns/test_diamond.py`

Review the existing pattern implementations for reusable conventions only. Do not silently redesign the public pattern event contract; if a shared contract change is required, stop and ask the owner for approval.

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

If an expected indicator/filter module is unavailable or incomplete for the exact Adam and Eve rule, the implementation must document the limitation and choose a deterministic behavior rather than silently approximating unrelated behavior.

# Pattern Mechanical Definition

Use this document as the source of truth:

- `tasks/patterns/adam_and_eve_pattern.md`

# First Adam and Eve Implementation Batch

Include only this pattern:

- Adam and Eve Pattern (`tasks/patterns/adam_and_eve_pattern.md`)

Required first-batch direction support:

- Bullish Adam and Eve only.

Recommended first-batch constraints:

- Use confirmed pivot lows for Adam low and Eve low.
- Use a confirmed pivot high for the neckline pivot.
- Use `neckline = neckline_pivot.price`.
- Require or explicitly document handling of prior downtrend.
- Use existing ATR and Volume Ratio modules for breakout validation.
- Use optional Displacement Candle only when `require_displacement_breakout` is enabled or to report confirmation.
- Emit `VALID` and `WEAK` completed breakout events by default.
- Defer optional `PENDING` Adam and Eve watchlist events unless explicitly implemented and tested.
- Keep bearish inverted Adam and Eve out of this batch.

# Deferred Work

Defer these until follow-up tasks explicitly assign them:

- Bearish inverted Adam and Eve.
- Long-lived pending/watchlist lifecycle tracking.
- Resistance-zone-based neckline selection beyond the default neckline pivot price.
- Consumer-side candidate merging beyond deterministic best-candidate selection.
- WebSocket integration.
- Backtest runner integration.
- Database persistence of pattern events.
- Missing Liquidity or Bid-Ask Spread modules.

# Scope

- Add or extend a pure pattern detection module under `quant_bitcoin/patterns/` for Adam and Eve Pattern detection.
- Add small configuration and event result types only as needed for Adam and Eve Pattern fields.
- Reuse existing indicator modules for pivots, ATR, Volume Ratio, Swing Structure, Support / Resistance Zone, and optional Displacement Candle where applicable.
- Add package exports only if needed for callers and tests.
- Add deterministic unit tests for valid, weak, invalid, rolling-window, stable-ID, and input-validation behavior.
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
- Optional Adam and Eve Pattern config.
- Optional precomputed indicator outputs only if doing so avoids recomputation and does not introduce contract ambiguity.

Input rules:

- Candles must be sorted ascending by `timestamp`; choose and document whether unsorted input is rejected or deterministically sorted.
- Only completed candles should be evaluated.
- Missing required OHLCV columns or invalid numeric values must fail deterministically with clear errors.
- Fewer than the minimum candles/pivots required for a full Adam and Eve sequence must return an empty list or a documented invalid result.
- The detector must not mutate caller-provided candle data in place.

# Proposed Output Contract

The future detector should return pattern event records exposing at least:

- `event_id`: stable deterministic identifier for duplicate prevention.
- `pattern_type`: fixed value `ADAM_AND_EVE` or `ADAM_AND_EVE_PATTERN` documented by implementation.
- `direction`: `BULLISH` or `NONE`.
- `pattern_status`: `VALID`, `WEAK`, `PENDING`, or `INVALID` when emitted.
- `symbol`: caller-supplied symbol, if available.
- `timeframe`: caller-supplied timeframe, if available.
- `timestamp`: event timestamp using the breakout candle timestamp.
- `start_index` / `end_index` or equivalent pattern indices.
- `adam_low_index`.
- `neckline_pivot_index`.
- `eve_low_index`.
- `breakout_index`.
- `adam_low_price`.
- `neckline`.
- `eve_low_price`.
- `bottom_difference_rate`.
- `adam_bottom_duration`.
- `eve_bottom_duration`.
- `eve_bottom_zone_duration`.
- `adam_local_range_atr`.
- `eve_local_range_atr`.
- `eve_to_adam_duration_ratio`.
- `pattern_height`.
- `pattern_height_atr`.
- `breakout_price`.
- `breakout_distance`.
- `breakout_distance_atr`.
- `volume_ratio`.
- `liquidity_pass` and `spread_pass` when available or explicitly supplied.
- `displacement_confirmed` when evaluated.
- `pattern_score`.
- `entry_reference`, `stop_reference`, `target_reference`, and `risk_reward` as reference values only, never order instructions.
- `reason`: concise deterministic reason.

Stable `event_id` guidance:

- Build `event_id` from immutable event-defining fields such as `pattern_type`, `direction`, `symbol`, `timeframe`, Adam low / neckline / Eve low pivot timestamps or indices, and breakout candle timestamp.
- Repeated calls over overlapping rolling windows must return the same `event_id` for the same completed Adam and Eve event.
- The detector may return all matching events in the supplied window; the caller may suppress duplicates by tracking seen `event_id` values.

# Mechanical Rules To Implement

Use the owner definition from `tasks/patterns/adam_and_eve_pattern.md`.

## Bullish Adam and Eve

- Require or explicitly document handling of prior downtrend.
- Find `adam_low` as a confirmed pivot low.
- Find `neckline_pivot` as a confirmed pivot high after `adam_low`.
- Find `eve_low` as a confirmed pivot low after `neckline_pivot`.
- Require `adam_low.index < neckline_pivot.index < eve_low.index < breakout.index`.
- Require `minimum_pattern_duration <= pattern_duration <= maximum_pattern_duration`.
- Require `bottom_difference_rate <= maximum_bottom_difference_rate`.
- Define `neckline = neckline_pivot.price` for the first batch.
- Require `minimum_pattern_height_atr <= pattern_height_atr`; handle heights above `maximum_pattern_height_atr` deterministically as `WEAK` or no event per implementation notes.
- Require Adam bottom to be sharp and short enough using deterministic Adam local-window rules.
- Require `adam_local_range_atr >= minimum_adam_range_atr`.
- Require Eve bottom to be wider / more rounded than Adam.
- Require `eve_bottom_zone_duration >= minimum_eve_bottom_zone_duration`.
- Require `eve_to_adam_duration_ratio >= minimum_eve_to_adam_duration_ratio`.
- Find breakout candle after Eve low.
- Require breakout close `> neckline + breakout_atr_multiplier * ATR`.
- Require `volume_ratio >= weak_breakout_volume_ratio`; emit `WEAK` when below `minimum_breakout_volume_ratio` and above/equal weak threshold.
- If `require_displacement_breakout = true`, require matching bullish displacement confirmation on the breakout candle.
- Missing liquidity or spread modules must be handled explicitly via config or clear deterministic no-event / error behavior.

# Scoring Guidance

If scoring is implemented, keep it deterministic and simple. Suggested first-batch components:

- Bottom similarity.
- Adam sharpness / local range quality.
- Eve roundness / bottom-zone quality.
- Eve-to-Adam duration ratio.
- Pattern height quality.
- Breakout ATR distance.
- Volume Ratio confirmation.
- Optional displacement confirmation.
- Liquidity/spread pass only when explicitly supplied.

Do not use ML, probabilistic scoring, external data, wall-clock time, or network calls.

# Streaming / Rolling-Window Guidance

The detector must remain pure and stateless.

Future callers should be able to use this pattern:

```python
events = detect_adam_and_eve_patterns(
    rolling_completed_candles,
    symbol="BTCUSDT",
    timeframe="1m",
)
new_events = [event for event in events if event.event_id not in seen_event_ids]
seen_event_ids.update(event.event_id for event in new_events)
```

Implementation requirements for rolling-window suitability:

- No exchange client imports.
- No network calls.
- No database writes.
- No background scheduler.
- No reliance on wall-clock time for detection decisions.
- Deterministic output for the same candle window and configuration.
- Empty output for windows that do not include enough completed candles/pivots.
- Stable `event_id` values across overlapping windows for the same completed event.

# Assumptions To Document During Implementation

Before coding, document implementation assumptions in the implementation notes or code comments, including:

- Whether unsorted candle input is rejected or sorted.
- How Adam local-window duration is calculated in the first deterministic implementation.
- How Eve bottom-zone duration is counted around Eve low.
- Whether pattern heights above `maximum_pattern_height_atr` produce `WEAK` or no event.
- Whether first-batch implementation emits only completed `VALID` / `WEAK` breakout events.
- How missing ATR or Volume Ratio rows are handled.
- How unavailable liquidity and spread filters are handled.

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

- A pure Adam and Eve Pattern detector exists when the implementation task is later executed.
- The detector accepts rolling or historical completed candle data using the existing candle data contract.
- The detector returns deterministic Adam and Eve Pattern event records for bullish breakout structures.
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

- No pattern detected when candles/pivots do not satisfy Adam and Eve Pattern rules.
- One bullish Adam and Eve Pattern event detected from a minimal valid pivot sequence and breakout.
- Insufficient candle or pivot history returns an empty list or documented invalid result.
- Prior downtrend missing behavior is deterministic when required.
- Bottom mismatch returns no event.
- Pattern duration outside configured bounds is deterministic.
- Adam bottom not sharp enough returns `WEAK` or no event according to documented behavior.
- Adam local range too small returns no event.
- Eve bottom not rounded enough returns no event.
- Eve-to-Adam duration ratio too small returns no event.
- Pattern height below or above configured ATR bounds is deterministic.
- Breakout missing or breakout without ATR buffer returns no event.
- Weak breakout volume produces `WEAK` if weak emission is implemented.
- Missing ATR or Volume Ratio inputs fail deterministically or result in no event according to the documented implementation choice.
- Optional displacement requirement rejects events without matching bullish displacement when enabled.
- Rolling/windowed detection behavior as new completed candles are appended.
- Stable `event_id` for the same completed pattern across overlapping rolling-window calls.
- No duplicate event emission for the same completed pattern when using the documented `seen_event_ids` caller pattern or optional helper.
- Missing required candle columns raise a clear deterministic error.
- Unsorted candle input behavior matches the documented implementation choice.

## Integration Tests

- Not required for the first Adam and Eve implementation unless the owner explicitly asks for WebSocket or backtest wiring.
- If a lightweight integration-style test is added, it must call only the pure detector with in-memory candle data.

## Contract Tests

- Verify the detector accepts the existing standard candle schema.
- Verify returned event records expose the required common fields and Adam and Eve Pattern fields.
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
- `tasks/patterns/adam_and_eve_pattern.md`
- existing pattern engine code and tests

# Codex Self-Review Requirement

Before completion of any implementation work under this task, run through `reviews/CODEX_SELF_REVIEW.md` and include the result in the final summary.

For this task-document creation step, perform the same self-review at documentation scope and confirm no application behavior was implemented.

# PR Review Requirement

Use `reviews/REVIEW_CHECKLIST.md` and `docs/06_PR_REVIEW_PROCESS.md` before merge.

Review must be strict about:

- Scope expansion beyond Adam and Eve Pattern and the minimal detector contract.
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
