# Task 044: Diamond Pattern Detection Engine

# Goal

Create the next pattern implementation assignment for the pattern detection engine: deterministic Diamond Pattern detection from completed candle data and confirmed pivot-derived expansion / contraction structure.

This task is an implementation task document only. It authorizes future implementation when the owner explicitly prompts `Mode: implement`; it does not implement code by itself.

# Source Requirement

The owner asked to define the next task for creating another pattern after the implemented Fair Value Gap, Trendline Break, Order Block, and Cup and Handle detectors.

Task 040 implemented the Fair Value Gap detector. Task 041 implemented the Trendline Break detector. Task 042 implemented the Order Block detector. Task 043 implemented the Cup and Handle detector. The next deferred pattern in the project pattern sequence is Diamond Pattern, and its mechanical definition is saved at `tasks/patterns/diamond_pattern.md`.

# Clean Requirement

Add a future implementation task for a pure Diamond Pattern detector that consumes normalized completed candles, reuses existing indicator outputs where applicable, identifies pivot-derived volatility expansion followed by contraction, validates contracting boundary breakout or breakdown strength, and returns stable pattern event records.

The future implementation must remain independent of WebSocket clients, exchange clients, databases, paper trading, backtesting runners, order execution, live trading, and risk management. Future WebSocket or backtest callers should be able to pass rolling or historical completed-candle windows into the pure detector.

# Extracted Roles

- Owner role: Diamond Pattern recognition from completed candle data and confirmed pivot-derived expansion / contraction structure.
- Supporting roles:
  - Market Data Contract, for normalized candle input shape.
  - Indicator modules, for Pivot High / Pivot Low, Swing Structure, ATR, Volume Ratio, Support / Resistance Zone, and optional Displacement Candle calculations where applicable.
  - Pattern Detection Engine, for stable pattern event output and rolling-window duplicate prevention.
  - WebSocket ingestion, only as a future caller that supplies rolling completed candles.
  - Backtesting, only as a future caller that supplies historical candle batches.
  - Test Designer, for deterministic Diamond Pattern event tests.
- Forbidden roles:
  - Live trading and real Binance order execution.
  - Paper order placement or real order placement.
  - Risk management, dashboard, database, scheduler, FastAPI, Streamlit, Docker, machine learning, futures, leverage, or portfolio optimization.
  - Market data fetching, because the detector consumes candles supplied by callers.

# Responsibility Boundary

The future Diamond Pattern detector is responsible for:

- Validating input candles against the standard schema in `docs/04_DATA_CONTRACT.md`.
- Evaluating completed candles in ascending timestamp order.
- Reusing existing indicator modules instead of duplicating indicator logic.
- Finding a confirmed pivot sequence with enough highs and lows to represent expansion followed by contraction.
- Finding the diamond center from the maximum local pivot range, or documenting a deterministic first-batch simplification if needed.
- Validating expansion phase behavior: rising pivot highs, falling pivot lows, and sufficient ATR-normalized range expansion.
- Validating contraction phase behavior: falling pivot highs, rising pivot lows, sufficient range contraction, and deterministic contraction boundaries.
- Evaluating bullish breakout above the upper contraction boundary and bearish breakdown below the lower contraction boundary with ATR buffer and Volume Ratio confirmation.
- Returning deterministic event records with stable event identifiers.
- Supporting repeated rolling-window calls without direct knowledge of WebSocket internals.

The future Diamond Pattern detector is not responsible for:

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
- `tasks/042_ORDER_BLOCK_PATTERN_ENGINE.md`
- `tasks/043_CUP_AND_HANDLE_PATTERN_ENGINE.md`
- `tasks/patterns/diamond_pattern.md`
- `quant_bitcoin/patterns/fair_value_gap.py`
- `quant_bitcoin/patterns/trendline_break.py`
- `quant_bitcoin/patterns/order_block.py`
- `quant_bitcoin/patterns/cup_and_handle.py`
- `quant_bitcoin/patterns/__init__.py`
- `tests/patterns/test_fair_value_gap.py`
- `tests/patterns/test_trendline_break.py`
- `tests/patterns/test_order_block.py`
- `tests/patterns/test_cup_and_handle.py`

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

If an expected indicator/filter module is unavailable or incomplete for the exact Diamond Pattern rule, the implementation must document the limitation and choose a deterministic behavior rather than silently approximating unrelated behavior.

# Pattern Mechanical Definition

Use this document as the source of truth:

- `tasks/patterns/diamond_pattern.md`

# First Diamond Pattern Implementation Batch

Include only this pattern:

- Diamond Pattern (`tasks/patterns/diamond_pattern.md`)

Required first-batch direction support:

- Bullish Diamond breakout.
- Bearish Diamond breakdown.

Recommended first-batch constraints:

- Use confirmed pivot highs and confirmed pivot lows only.
- Require at least `minimum_pivot_count` pivots and at least 3 highs / 3 lows in the selected sequence.
- Use a deterministic maximum local pivot range method for `diamond_center` when practical.
- Split selected pivots into expansion and contraction phases around the center.
- Build upper contraction boundary from contraction pivot highs.
- Build lower contraction boundary from contraction pivot lows.
- Use existing ATR and Volume Ratio modules for breakout / breakdown validation.
- Use optional Displacement Candle only when `require_displacement_breakout` is enabled or to report confirmation.
- Emit `VALID` and `WEAK` completed breakout / breakdown events by default.
- Defer optional `PENDING` diamond watchlist events unless explicitly implemented and tested.

# Deferred Work

Defer these until follow-up tasks explicitly assign them:

- Long-lived pending/watchlist lifecycle tracking.
- Consumer-side candidate merging beyond deterministic best-candidate selection.
- Resistance/support-zone-based boundary replacement beyond pivot-derived contraction boundaries.
- WebSocket integration.
- Backtest runner integration.
- Database persistence of pattern events.
- Adam and Eve pattern implementation.
- Missing Liquidity or Bid-Ask Spread modules.

# Scope

- Add or extend a pure pattern detection module under `quant_bitcoin/patterns/` for Diamond Pattern detection.
- Add small configuration and event result types only as needed for Diamond Pattern fields.
- Reuse existing indicator modules for pivots, ATR, Volume Ratio, Swing Structure, Support / Resistance Zone, and optional Displacement Candle where applicable.
- Add package exports only if needed for callers and tests.
- Add deterministic unit tests for valid bullish, valid bearish, weak, invalid, rolling-window, stable-ID, and input-validation behavior.
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
- Optional Diamond Pattern config.
- Optional precomputed indicator outputs only if doing so avoids recomputation and does not introduce contract ambiguity.

Input rules:

- Candles must be sorted ascending by `timestamp`; choose and document whether unsorted input is rejected or deterministically sorted.
- Only completed candles should be evaluated.
- Missing required OHLCV columns or invalid numeric values must fail deterministically with clear errors.
- Fewer than the minimum candles/pivots required for a full Diamond Pattern sequence must return an empty list or a documented invalid result.
- The detector must not mutate caller-provided candle data in place.

# Proposed Output Contract

The future detector should return pattern event records exposing at least:

- `event_id`: stable deterministic identifier for duplicate prevention.
- `pattern_type`: fixed value `DIAMOND` or `DIAMOND_PATTERN` documented by implementation.
- `direction`: `BULLISH`, `BEARISH`, or `NONE`.
- `pattern_status`: `VALID`, `WEAK`, `PENDING`, or `INVALID` when emitted.
- `symbol`: caller-supplied symbol, if available.
- `timeframe`: caller-supplied timeframe, if available.
- `timestamp`: event timestamp using the breakout / breakdown candle timestamp.
- `start_index` / `end_index` or equivalent pattern indices.
- `expansion_start_index`.
- `diamond_center_index`.
- `contraction_end_index`.
- `breakout_index`.
- `source_pivot_indices`.
- `upper_boundary_slope`.
- `upper_boundary_intercept`.
- `lower_boundary_slope`.
- `lower_boundary_intercept`.
- `upper_boundary_value` at breakout / breakdown index.
- `lower_boundary_value` at breakout / breakdown index.
- `expansion_high_slope`.
- `expansion_low_slope`.
- `contraction_high_slope`.
- `contraction_low_slope`.
- `expansion_range_change`.
- `expansion_range_change_atr`.
- `contraction_range_change`.
- `contraction_range_change_rate`.
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

- Build `event_id` from immutable event-defining fields such as `pattern_type`, `direction`, `symbol`, `timeframe`, selected pivot timestamps/indices, and breakout / breakdown candle timestamp.
- Repeated calls over overlapping rolling windows must return the same `event_id` for the same completed Diamond Pattern event.
- The detector may return all matching events in the supplied window; the caller may suppress duplicates by tracking seen `event_id` values.

# Mechanical Rules To Implement

Use the owner definition from `tasks/patterns/diamond_pattern.md`.

## Diamond Pattern

- Use confirmed pivots only.
- Require `minimum_pivot_count <= pivot_count <= maximum_pivot_count` for evaluated candidate sequences, or document deterministic candidate-window behavior.
- Require at least 3 pivot highs and at least 3 pivot lows in a selected candidate.
- Require `minimum_pattern_duration <= pattern_duration <= maximum_pattern_duration`.
- Determine `diamond_center` from maximum local pivot range when practical.
- Split selected pivots into expansion and contraction phases around `diamond_center`.
- Require expansion phase to include enough highs and lows for deterministic slope/range checks.
- Require contraction phase to include enough highs and lows for deterministic boundary construction.
- Require expansion pivot highs to rise and expansion pivot lows to fall.
- Require contraction pivot highs to fall and contraction pivot lows to rise.
- Require `expansion_range_change_atr >= minimum_expansion_range_change_atr`.
- Require `contraction_range_change_rate >= minimum_contraction_range_change_rate`.
- Require `minimum_pattern_height_atr <= pattern_height_atr <= maximum_pattern_height_atr`.
- Build an upper contraction boundary from contraction pivot highs.
- Build a lower contraction boundary from contraction pivot lows.
- Find breakout / breakdown candle after the contraction end.
- Bullish breakout requires `close > upper_boundary_value + breakout_atr_multiplier * ATR`.
- Bearish breakdown requires `close < lower_boundary_value - breakout_atr_multiplier * ATR`.
- Require `volume_ratio >= weak_breakout_volume_ratio`; emit `WEAK` when below `minimum_breakout_volume_ratio` and above/equal weak threshold.
- If `require_displacement_breakout = true`, require matching bullish / bearish displacement confirmation on the breakout / breakdown candle.
- Missing liquidity or spread modules must be handled explicitly via config or clear deterministic no-event / error behavior.

# Scoring Guidance

If scoring is implemented, keep it deterministic and simple. Suggested first-batch components:

- Expansion quality.
- Contraction quality.
- Boundary touch/deviation quality.
- Pattern height quality.
- Breakout / breakdown ATR distance.
- Volume Ratio confirmation.
- Optional displacement confirmation.
- Liquidity/spread pass only when explicitly supplied.

Do not use ML, probabilistic scoring, external data, wall-clock time, or network calls.

# Streaming / Rolling-Window Guidance

The detector must remain pure and stateless.

Future callers should be able to use this pattern:

```python
events = detect_diamond_patterns(
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
- How candidate pivot windows are selected when more than `maximum_pivot_count` confirmed pivots are available.
- How `diamond_center` is selected if multiple local range maxima tie.
- How boundary lines are fit when more than two contraction highs/lows are available.
- Whether first-batch implementation emits only completed `VALID` / `WEAK` breakout / breakdown events.
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

- A pure Diamond Pattern detector exists when the implementation task is later executed.
- The detector accepts rolling or historical completed candle data using the existing candle data contract.
- The detector returns deterministic Diamond Pattern event records for bullish breakout and bearish breakdown structures.
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

- No pattern detected when candles/pivots do not satisfy Diamond Pattern rules.
- One bullish Diamond Pattern event detected from a minimal valid expansion/contraction pivot sequence and breakout.
- One bearish Diamond Pattern event detected from a minimal valid expansion/contraction pivot sequence and breakdown.
- Insufficient candle or pivot history returns an empty list or documented invalid result.
- Missing enough pivot highs or pivot lows returns no event.
- Pattern duration outside configured bounds is deterministic.
- Expansion phase without rising highs or falling lows returns no event.
- Contraction phase without falling highs or rising lows returns no event.
- Insufficient expansion range change returns no event.
- Insufficient contraction range change returns no event.
- Pattern height below or above configured ATR bounds returns no event.
- Breakout / breakdown missing or without ATR buffer returns no event.
- Weak breakout / breakdown volume produces `WEAK` if weak emission is implemented.
- Missing ATR or Volume Ratio inputs fail deterministically or result in no event according to the documented implementation choice.
- Optional displacement requirement rejects events without matching displacement when enabled.
- Rolling/windowed detection behavior as new completed candles are appended.
- Stable `event_id` for the same completed pattern across overlapping rolling-window calls.
- No duplicate event emission for the same completed pattern when using the documented `seen_event_ids` caller pattern or optional helper.
- Missing required candle columns raise a clear deterministic error.
- Unsorted candle input behavior matches the documented implementation choice.

## Integration Tests

- Not required for the first Diamond Pattern implementation unless the owner explicitly asks for WebSocket or backtest wiring.
- If a lightweight integration-style test is added, it must call only the pure detector with in-memory candle data.

## Contract Tests

- Verify the detector accepts the existing standard candle schema.
- Verify returned event records expose the required common fields and Diamond Pattern fields.
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
- `tasks/patterns/diamond_pattern.md`
- existing pattern engine code and tests

# Codex Self-Review Requirement

Before completion of any implementation work under this task, run through `reviews/CODEX_SELF_REVIEW.md` and include the result in the final summary.

For this task-document creation step, perform the same self-review at documentation scope and confirm no application behavior was implemented.

# PR Review Requirement

Use `reviews/REVIEW_CHECKLIST.md` and `docs/06_PR_REVIEW_PROCESS.md` before merge.

Review must be strict about:

- Scope expansion beyond Diamond Pattern and the minimal detector contract.
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
