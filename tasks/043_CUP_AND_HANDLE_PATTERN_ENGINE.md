# Task 043: Cup and Handle Pattern Detection Engine

# Goal

Create the next pattern implementation assignment for the pattern detection engine: deterministic Cup and Handle detection from completed candle data and confirmed pivot-derived structure.

This task is an implementation task document only. It authorizes future implementation when the owner explicitly prompts `Mode: implement`; it does not implement code by itself.

# Source Requirement

The owner asked to create the next pattern implementation task after the implemented Fair Value Gap, Trendline Break, and Order Block detectors.

Task 040 implemented the Fair Value Gap detector. Task 041 implemented the Trendline Break detector. Task 042 implemented the Order Block detector. The next deferred pattern listed in `tasks/040_PATTERN_DETECTION_ENGINE.md` is Cup and Handle, and its mechanical definition is saved at `tasks/patterns/cup_and_handle_pattern.md`.

# Clean Requirement

Add a future implementation task for a pure Cup and Handle detector that consumes normalized completed candles, reuses existing indicator outputs where applicable, identifies a bullish cup-and-handle sequence from confirmed pivots, validates cup shape, handle quality, breakout strength, and volume confirmation, and returns stable pattern event records.

The future implementation must remain independent of WebSocket clients, exchange clients, databases, paper trading, backtesting runners, order execution, live trading, and risk management. Future WebSocket or backtest callers should be able to pass rolling or historical completed-candle windows into the pure detector.

# Extracted Roles

- Owner role: Cup and Handle pattern recognition from completed candle data and confirmed pivot-derived structure.
- Supporting roles:
  - Market Data Contract, for normalized candle input shape.
  - Indicator modules, for Pivot High / Pivot Low, Swing Structure, ATR, Volume Ratio, Support / Resistance Zone, and optional Displacement Candle calculations where applicable.
  - Pattern Detection Engine, for stable pattern event output and rolling-window duplicate prevention.
  - WebSocket ingestion, only as a future caller that supplies rolling completed candles.
  - Backtesting, only as a future caller that supplies historical candle batches.
  - Test Designer, for deterministic cup-and-handle event tests.
- Forbidden roles:
  - Live trading and real Binance order execution.
  - Paper order placement or real order placement.
  - Risk management, dashboard, database, scheduler, FastAPI, Streamlit, Docker, machine learning, futures, leverage, or portfolio optimization.
  - Market data fetching, because the detector consumes candles supplied by callers.

# Responsibility Boundary

The future Cup and Handle detector is responsible for:

- Validating input candles against the standard schema in `docs/04_DATA_CONTRACT.md`.
- Evaluating completed candles in ascending timestamp order.
- Reusing existing indicator modules instead of duplicating indicator logic.
- Finding a bullish sequence of confirmed pivots: left rim, cup bottom, right rim, handle low, and breakout candle.
- Validating rim similarity, cup depth, cup duration, bottom-zone duration, slope balance, handle depth, handle duration, handle position, breakout ATR buffer, and breakout volume.
- Returning deterministic event records with stable event identifiers.
- Supporting repeated rolling-window calls without direct knowledge of WebSocket internals.

The future Cup and Handle detector is not responsible for:

- Opening WebSocket connections.
- Fetching data from Binance or any exchange.
- Reading API keys or environment secrets.
- Persisting detected events to a database.
- Creating strategy BUY / SELL / HOLD signals.
- Placing paper or real orders.
- Managing position sizing, stops, risk limits, or portfolio allocation.
- Implementing missing liquidity or bid-ask spread modules unless this task is explicitly amended.
- Implementing bearish inverted cup-and-handle support unless a future task explicitly assigns it.
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
- `quant_bitcoin/patterns/fair_value_gap.py`
- `quant_bitcoin/patterns/trendline_break.py`
- `quant_bitcoin/patterns/order_block.py`
- `quant_bitcoin/patterns/__init__.py`
- `tests/patterns/test_fair_value_gap.py`
- `tests/patterns/test_trendline_break.py`
- `tests/patterns/test_order_block.py`

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

Also review these known source requirements before deciding whether to enforce or defer filters:

- `tasks/027_IMPLEMENT_BID_ASK_SPREAD.md`
- `tasks/indicators/liquidity.md`

If a required filter does not have an implemented reusable module, the implementation must explicitly handle that limitation by keeping the filter out of the first Cup and Handle batch, requiring explicit caller-supplied pass/fail values, marking the result unavailable/unknown according to the mechanical definition, or stopping for owner approval. Do not implement unrelated prerequisite indicators inside this task unless amended.

## Pattern Mechanical Definition

Use this document as the source of truth:

- `tasks/patterns/cup_and_handle_pattern.md`

# First Cup and Handle Implementation Batch

Include only this pattern:

- Cup and Handle (`tasks/patterns/cup_and_handle_pattern.md`)

Required first-batch direction support:

- Bullish Cup and Handle only.

Recommended first-batch constraints:

- Use confirmed pivot highs for left and right rims.
- Use confirmed pivot lows for cup bottom and handle low.
- Use `neckline = max(left_rim.price, right_rim.price)`.
- Use existing ATR and Volume Ratio modules for breakout validation.
- Use optional Displacement Candle only when `require_displacement_breakout` is enabled or to report confirmation.
- Emit `VALID` and `WEAK` completed breakout events by default.
- Defer optional `PENDING` cup/handle watchlist events unless explicitly implemented and tested.
- Keep bearish inverted Cup and Handle out of this batch.

# Deferred Work

Defer these until follow-up tasks explicitly assign them:

- Bearish inverted Cup and Handle.
- Long-lived pending/watchlist lifecycle tracking.
- Resistance-zone-based neckline selection beyond the default max-rim neckline.
- Consumer-side candidate merging beyond deterministic best-candidate selection.
- WebSocket integration.
- Backtest runner integration.
- Database persistence of pattern events.
- Diamond and Adam and Eve pattern implementations.
- Missing Liquidity or Bid-Ask Spread modules.

# Scope

- Add or extend a pure pattern detection module under `quant_bitcoin/patterns/` for Cup and Handle detection.
- Add small configuration and event result types only as needed for Cup and Handle fields.
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
- Optional Cup and Handle config.
- Optional precomputed indicator outputs only if doing so avoids recomputation and does not introduce contract ambiguity.

Input rules:

- Candles must be sorted ascending by `timestamp`; choose and document whether unsorted input is rejected or deterministically sorted.
- Only completed candles should be evaluated.
- Missing required OHLCV columns or invalid numeric values must fail deterministically with clear errors.
- Fewer than the minimum candles/pivots required for a full Cup and Handle sequence must return an empty list or a documented invalid result.
- The detector must not mutate caller-provided candle data in place.

# Proposed Output Contract

The future detector should return pattern event records exposing at least:

- `event_id`: stable deterministic identifier for duplicate prevention.
- `pattern_type`: fixed value `CUP_AND_HANDLE`.
- `direction`: `BULLISH` or `NONE`.
- `pattern_status`: `VALID`, `WEAK`, `PENDING`, or `INVALID` when emitted.
- `symbol`: caller-supplied symbol, if available.
- `timeframe`: caller-supplied timeframe, if available.
- `timestamp`: event timestamp using the breakout candle timestamp.
- `start_index` / `end_index` or equivalent pattern indices.
- `left_rim_index`.
- `cup_bottom_index`.
- `right_rim_index`.
- `handle_low_index`.
- `breakout_index`.
- `left_rim_price`.
- `cup_bottom_price`.
- `right_rim_price`.
- `handle_low_price`.
- `neckline`.
- `cup_depth`.
- `cup_depth_rate`.
- `cup_duration`.
- `bottom_zone_duration`.
- `duration_ratio`.
- `handle_depth`.
- `handle_depth_ratio`.
- `handle_duration`.
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

- Build `event_id` from immutable event-defining fields such as `pattern_type`, `direction`, `symbol`, `timeframe`, pivot timestamps/indices, and breakout candle timestamp.
- Repeated calls over overlapping rolling windows must return the same `event_id` for the same completed Cup and Handle event.
- The detector may return all matching events in the supplied window; the caller may suppress duplicates by tracking seen `event_id` values.

# Mechanical Rules To Implement

Use the owner definition from `tasks/patterns/cup_and_handle_pattern.md`.

## Bullish Cup and Handle

- Require or explicitly document handling of prior uptrend.
- Find `left_rim` as a confirmed pivot high.
- Find `cup_bottom` as a confirmed pivot low after `left_rim`.
- Find `right_rim` as a confirmed pivot high after `cup_bottom`.
- Find `handle_low` as a confirmed pivot low after `right_rim`.
- Require `rim_difference_rate <= maximum_rim_difference_rate`.
- Require `minimum_cup_depth_rate <= cup_depth_rate <= maximum_cup_depth_rate`.
- Require `minimum_cup_duration <= cup_duration <= maximum_cup_duration`.
- Require `bottom_zone_duration >= minimum_bottom_zone_duration`.
- Require handle depth and handle position rules.
- Define `neckline = max(left_rim.price, right_rim.price)` for the first batch.
- Find breakout candle after handle low.
- Require breakout close above neckline with ATR buffer.
- Require breakout volume confirmation.
- Classify `VALID`, `WEAK`, or no event / invalid according to hard filters, weak quality conditions, volume, and score.

# Default Parameters

Use the owner defaults unless a reviewed implementation reason requires a documented deviation:

```yaml
cup_and_handle:
  minimum_cup_duration: 20
  maximum_cup_duration: 200
  minimum_handle_duration: 3
  maximum_handle_duration: 40
  maximum_rim_difference_rate: 0.05
  minimum_cup_depth_rate: 0.10
  maximum_cup_depth_rate: 0.40
  maximum_handle_depth_ratio: 0.35
  minimum_bottom_zone_duration: 3
  bottom_zone_atr_multiplier: 0.5
  minimum_slope_balance_ratio: 0.3
  breakout_atr_multiplier: 0.2
  minimum_breakout_volume_ratio: 1.5
  weak_breakout_volume_ratio: 1.3
  require_prior_uptrend: true
  require_liquidity_pass: true
  require_spread_pass: true
  require_displacement_breakout: false
  minimum_pattern_score: 0.7
```

# Open Questions Before Implementation

Resolve or document these before coding if not already clear from reviewed files:

- Should the first Cup and Handle implementation require prior uptrend by default when robust structure context may be unavailable, or make this optional/unavailable unless explicitly supplied?
- Should liquidity and bid-ask spread follow existing detector behavior of being optional/unavailable unless explicitly supplied?
- Should the detector emit `PENDING` cup/handle candidates, or only completed `VALID` / `WEAK` breakout events?
- How should bottom-zone duration be counted around the cup bottom in the first deterministic implementation?
- Should resistance-zone neckline selection be deferred in favor of `max(left_rim.price, right_rim.price)`?
- What minimum rolling lookback should future WebSocket callers retain for pivot confirmation, cup duration, handle duration, ATR/volume warmup, and breakout validation?

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

- A pure Cup and Handle detector exists when the implementation task is later executed.
- The detector accepts rolling or historical completed candle data using the existing candle data contract.
- The detector returns deterministic Cup and Handle event records for bullish structures.
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

- No pattern detected when candles/pivots do not satisfy Cup and Handle rules.
- One bullish Cup and Handle event detected from a minimal valid pivot sequence and breakout.
- Insufficient candle or pivot history returns an empty list or documented invalid result.
- Rim price mismatch behavior is deterministic.
- Cup too shallow and cup too deep behavior is deterministic.
- Cup duration outside configured bounds is deterministic.
- V-shaped or insufficient bottom-zone duration behavior is deterministic.
- Handle missing, handle too deep, and handle below cup midpoint behavior is deterministic.
- Breakout missing or breakout without ATR buffer behavior is deterministic.
- Weak breakout volume produces `WEAK` if weak emission is implemented.
- Missing ATR or Volume Ratio inputs fail deterministically or result in no event according to the documented implementation choice.
- Rolling/windowed detection behavior as new completed candles are appended.
- Stable `event_id` for the same completed pattern across overlapping rolling-window calls.
- No duplicate event emission for the same completed pattern when using the documented `seen_event_ids` caller pattern or optional helper.
- Missing required candle columns raise a clear deterministic error.
- Unsorted candle input behavior matches the documented implementation choice.

## Integration Tests

- Not required for the first Cup and Handle implementation unless the owner explicitly asks for WebSocket or backtest wiring.
- If a lightweight integration-style test is added, it must call only the pure detector with in-memory candle data.

## Contract Tests

- Verify the detector accepts the existing standard candle schema.
- Verify returned event records expose the required common fields and Cup and Handle fields.
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
- `tasks/patterns/cup_and_handle_pattern.md`
- existing pattern engine code and tests

# Codex Self-Review Requirement

Before completion of any implementation work under this task, run through `reviews/CODEX_SELF_REVIEW.md` and include the result in the final summary.

For this task-document creation step, perform the same self-review at documentation scope and confirm no application behavior was implemented.

# PR Review Requirement

Use `reviews/REVIEW_CHECKLIST.md` and `docs/06_PR_REVIEW_PROCESS.md` before merge.

Review must be strict about:

- Scope expansion beyond Cup and Handle and the minimal detector contract.
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
