# Task 040: Pattern Detection Engine

# Goal

Implement a small, deterministic pattern detection engine that evaluates rolling candle data and returns detected pattern events.

The first implementation priority is a pure detection function that can be called repeatedly as new completed candles arrive from a WebSocket stream, while also working for historical/backtest-style candle batches.

# Source Requirement

Owner requested code that detects whether candles contain patterns based on indicators already implemented in the project and pattern definitions already defined by the owner.

Because candles will continue arriving through a WebSocket stream, the first implementation priority must be a deterministic function that evaluates rolling candle data and recognizes patterns as new candles arrive.

Existing pattern definition documents under `tasks/patterns/` are source requirements. They define mechanical pattern rules unless they explicitly assign implementation. This task is the implementation assignment for the first pattern detection engine batch only.

# Clean Requirement

Add a pure pattern detection module/function that consumes a rolling sequence of normalized candles, computes or consumes required existing indicator outputs where appropriate, evaluates an approved first batch of mechanical pattern definitions, and returns deterministic pattern event records.

The detector must not depend on WebSocket clients, exchange clients, databases, paper trading, backtesting runners, or order execution. WebSocket ingestion code should be able to call the detector by passing the latest rolling completed-candle window into the pure function.

# Extracted Roles

- Owner role: Pattern recognition from completed candle data using approved mechanical pattern definitions.
- Supporting roles:
  - Market Data Contract, for normalized candle input shape.
  - Indicator modules, for ATR, Volume Ratio, Displacement Candle, Pivot High / Pivot Low, Swing Structure, and Support / Resistance Zone calculations where needed.
  - WebSocket ingestion, only as a future caller that supplies rolling completed candles.
  - Backtesting, only as a future caller that supplies historical candle batches.
  - Test Designer, for deterministic pattern-event tests.
- Forbidden roles:
  - Live trading, because this task must not place or route orders.
  - Real Binance order execution, because pattern detection must never call exchange order APIs.
  - Risk management, dashboard, database, scheduler, FastAPI, Streamlit, Docker, machine learning, futures, leverage, or portfolio optimization.
  - Market data fetching, because the detector consumes candles supplied by callers.

# Responsibility Boundary

The pattern detector is responsible for:

- Validating that input candles satisfy the existing standard candle schema required by `docs/04_DATA_CONTRACT.md`.
- Evaluating completed candles in ascending timestamp order.
- Reusing existing indicator modules where applicable instead of duplicating indicator logic.
- Applying the approved pattern mechanical definition documents as the source of truth.
- Returning deterministic pattern event records with stable event identifiers.
- Supporting repeated rolling-window calls without requiring direct knowledge of WebSocket internals.

The pattern detector is not responsible for:

- Opening WebSocket connections.
- Fetching market data from Binance or any other exchange.
- Reading API keys or environment secrets.
- Persisting detected events to a database.
- Creating trading signals, placing paper orders, placing real orders, or managing risk.
- Changing existing public market data, signal, strategy, backtest, or execution contracts unless the implementation discovers an unavoidable shared contract gap and stops for owner approval first.

# Existing Context To Review Before Implementation

## Project Workflow And Contracts

- `AGENTS.md`
- `STATUS.md`
- `docs/10_CODEX_COMMAND_GUIDE.md`
- `docs/04_DATA_CONTRACT.md`
- `reviews/CODEX_SELF_REVIEW.md`

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

If a required filter does not have an implemented reusable module, the implementation must either keep that filter out of the first batch, mark the result as unavailable/unknown according to the mechanical definition, or stop and ask the owner to approve a prerequisite task. Do not implement unrelated prerequisite indicators inside this task unless this task is explicitly amended.

## Pattern Mechanical Definitions

Use these documents as the source of truth for pattern rules:

- `tasks/patterns/fair_value_gap_pattern.md`
- `tasks/patterns/trendline_break_pattern.md`
- `tasks/patterns/order_block_pattern.md`
- `tasks/patterns/cup_and_handle_pattern.md`
- `tasks/patterns/diamond_pattern.md`
- `tasks/patterns/adam_and_eve_pattern.md`

# First Implementation Batch

Include only this pattern in the first implementation batch:

- Fair Value Gap (`tasks/patterns/fair_value_gap_pattern.md`)

Rationale:

- It has a clear three-candle core structure suitable for deterministic rolling-window evaluation.
- It can use existing implemented indicators: ATR, Volume Ratio, Displacement Candle, Swing Structure, and Support / Resistance Zone where applicable.
- It is the smallest useful vertical slice for proving the engine contract, event output, rolling behavior, and duplicate-prevention strategy.

The first implementation may support only event emission for newly detected Fair Value Gap structures on completed candles. More complex state tracking such as long-lived fill-state updates may be included only if it can be done without expanding scope or changing shared contracts; otherwise it must be deferred.

# Deferred Pattern Batches

Defer these patterns until follow-up implementation tasks explicitly assign them:

- Trendline Break (`tasks/patterns/trendline_break_pattern.md`)
- Order Block (`tasks/patterns/order_block_pattern.md`)
- Cup and Handle (`tasks/patterns/cup_and_handle_pattern.md`)
- Diamond (`tasks/patterns/diamond_pattern.md`)
- Adam and Eve (`tasks/patterns/adam_and_eve_pattern.md`)

Reasons for deferral:

- They require more pivot sequencing, trendline construction, multi-phase candidate management, or longer-lived pattern state than the first engine slice should introduce.
- Several definitions reference liquidity and bid-ask spread filters that may need separate implementation or explicit owner decisions before enforcement.
- Keeping the first batch narrow reduces risk of scope expansion and protects existing market data, strategy, signal, and backtest contracts.

# Scope

- Add a new pure pattern detection module under an appropriate package path, such as `quant_bitcoin/patterns/`.
- Add a deterministic detector function for Fair Value Gap events.
- Add small configuration and event result types only as needed for the first implementation batch.
- Reuse existing implemented indicator functions where applicable.
- Add package exports only if needed for callers and tests.
- Add unit tests for deterministic batch and rolling-window behavior.
- Update `STATUS.md` during implementation if the phase, step, goal, active task, blockers, open questions, or completion state changes.

# Out of Scope

- Implementing application code during this task-document creation step.
- Modifying WebSocket ingestion behavior unless a later implementation prompt explicitly assigns it.
- Implementing live trading.
- Implementing real Binance order execution.
- Adding exchange order API calls.
- Adding risk management, dashboard, database, scheduler, FastAPI, Streamlit, Docker, machine learning, futures, leverage, or portfolio optimization.
- Redesigning existing public market data, signal, strategy, backtest, or execution contracts without explicit owner approval.
- Implementing deferred patterns listed above.
- Implementing missing liquidity or bid-ask spread indicator modules unless the owner explicitly amends this task.
- Hardcoding API keys or secrets.
- Committing `.env` files.

# Proposed Input Contract

The first detector function should accept:

- `candles`: a rolling or historical sequence of completed candles using the standard schema:
  - `timestamp`
  - `open`
  - `high`
  - `low`
  - `close`
  - `volume`
- Optional `symbol`: string identifier, defaulting to `None` or a documented placeholder if omitted.
- Optional `timeframe`: string identifier if supplied by the caller.
- Optional `config`: pattern detector configuration.
- Optional precomputed indicator outputs only if doing so avoids recomputation and does not introduce contract ambiguity.

The implementation should prefer accepting a pandas `DataFrame` initially, consistent with the existing candle data contract. If helper functions accept records or sequences, they must normalize to the same standard candle schema at the module boundary.

Input ordering and completeness rules:

- Candles must be sorted ascending by `timestamp`; if not, either sort deterministically or raise a clear `ValueError`. The chosen behavior must be documented and tested.
- Only completed candles should be evaluated. A WebSocket caller must pass only closed candles or must explicitly exclude the currently open candle before calling the detector.
- The function must return an empty list when there is insufficient candle history for the requested pattern.
- Missing required OHLCV columns or invalid numeric values must fail deterministically with clear errors.

# Proposed Output Contract

The detector should return a list of pattern event records. The concrete implementation may use frozen dataclasses, dictionaries, or another simple existing project style, but each event must expose at least:

- `event_id`: stable deterministic identifier for duplicate prevention.
- `pattern_type`: for the first batch, `FAIR_VALUE_GAP`.
- `direction`: `BULLISH`, `BEARISH`, or `NONE` according to the mechanical definition.
- `pattern_status`: `VALID`, `WEAK`, `PENDING`, or `INVALID` when emitted.
- `symbol`: caller-supplied symbol, if available.
- `timeframe`: caller-supplied timeframe, if available.
- `timestamp`: event timestamp, using the completed detection candle timestamp.
- `start_index` / `end_index` or pattern-specific candle indices.
- Pattern-specific fields required by the Fair Value Gap output schema, including zone bounds and gap size fields where available.
- `reason`: concise deterministic reason for the event or status.

For Fair Value Gap, include at minimum:

- `candle_1_index`
- `candle_2_index`
- `candle_3_index`
- `zone_low`
- `zone_high`
- `zone_mid`
- `gap_size`
- `gap_size_atr` when ATR is available and required by the chosen config
- `fill_ratio` when implemented for the initial event
- `displacement_confirmed` when displacement is evaluated
- `displacement_direction` when displacement is evaluated
- `volume_ratio` when volume ratio is evaluated
- `pattern_score` if scoring is implemented in the first batch

Stable `event_id` guidance:

- Build `event_id` from immutable event-defining fields, such as `pattern_type`, `direction`, `symbol`, `timeframe`, and the three Fair Value Gap candle timestamps or candle indices.
- Repeated calls over overlapping rolling windows must return the same `event_id` for the same completed pattern.
- The detector may return all matching events in the supplied window; the caller may suppress duplicates by tracking seen `event_id` values.
- If the implementation adds a convenience helper for `seen_event_ids`, it must remain optional and must not require global mutable state.

# Streaming / WebSocket Calling Model

The detector must remain independent of WebSocket ingestion code.

A future WebSocket caller should be able to use it like this:

```python
rolling_candles.append(completed_candle)
rolling_candles = rolling_candles[-max_required_window:]
events = detect_patterns(
    rolling_candles,
    symbol="BTCUSDT",
    timeframe="1m",
)
new_events = [event for event in events if event.event_id not in seen_event_ids]
seen_event_ids.update(event.event_id for event in new_events)
```

Implementation requirements for streaming suitability:

- No exchange client imports.
- No network calls.
- No database writes.
- No background scheduler.
- No reliance on wall-clock time for detection decisions.
- Deterministic output for the same candle window and configuration.
- Empty output for windows that do not include enough completed candles.

# Requirements

- Read all documents listed in the review sections before coding.
- Implement only the first batch: Fair Value Gap detection and the minimal engine contract needed to return pattern events.
- Use `tasks/patterns/fair_value_gap_pattern.md` as the source of truth for the first pattern's mechanical rules.
- Reuse existing indicator modules where applicable instead of duplicating ATR, Volume Ratio, Displacement Candle, Swing Structure, Support / Resistance Zone, or Pivot logic.
- If a referenced indicator/filter is unavailable or not implemented, document the limitation in code comments or task/status notes and avoid silently inventing unrelated behavior.
- Keep the detector pure and deterministic.
- Do not mutate caller-provided candle data in place.
- Do not add live trading behavior, paper order placement, real order placement, exchange order endpoint calls, API key reads, or `.env` dependencies.
- Do not modify WebSocket ingestion behavior in the first implementation unless a later prompt explicitly assigns that integration.
- Do not redesign existing public market data, signal, strategy, or backtest contracts. If a shared contract change appears necessary, stop and ask the owner for approval.

# Open Questions Before Implementation

Resolve or document these before coding if the answer is not already clear from the reviewed files:

- Should the first Fair Value Gap implementation enforce liquidity and bid-ask spread filters when implemented modules are not yet available?
- Should the first Fair Value Gap implementation emit `PENDING` and `WEAK` events, or only `VALID` events plus deterministic invalid/empty behavior?
- Should ATR, Volume Ratio, and Displacement Candle outputs be computed internally from candles by default, or accepted as optional precomputed inputs for performance in streaming callers?
- Should unsorted candle input be sorted or rejected?
- What rolling lookback length should a future WebSocket caller retain for Fair Value Gap detection plus indicator warmup?

# Status Tracking

## Before Implementation

- [ ] Read `STATUS.md`.
- [ ] Confirm this task matches the current phase and step.
- [ ] Confirm the active task is recorded or should be updated.
- [ ] Confirm parallel work is not needed for the first implementation batch.
- [ ] Record assumptions, blockers, or unclear status items before coding.

## After Implementation

- [ ] Update `STATUS.md` if the phase, step, goal, active task, blocker, open question, or completion state changed.
- [ ] Mark checklist items complete only when acceptance criteria and verification are satisfied.
- [ ] Leave uncertain items open and document the uncertainty.
- [ ] Confirm the next step is accurate or explicitly left undecided.

# Acceptance Criteria

- A pattern detection module/function exists for the first implementation batch.
- The detector accepts rolling or historical completed candle data using the existing candle data contract.
- The detector returns deterministic pattern events for Fair Value Gap structures.
- Repeated calls over overlapping rolling windows produce stable event identifiers for the same completed pattern.
- The detector can be used from future WebSocket ingestion code without importing or depending on exchange clients.
- Existing indicator modules are reused where applicable.
- Missing prerequisite filters are handled explicitly rather than silently approximated.
- No live trading, real Binance order execution, exchange order API calls, risk management, dashboard, database, scheduler, FastAPI, Streamlit, Docker, machine learning, futures, leverage, or portfolio optimization is added.
- Tests cover the required behavior below.
- `STATUS.md` is updated only for actual project-state changes.

# Required Tests

## Unit Tests

Add deterministic tests for:

- No pattern detected when candles do not satisfy Fair Value Gap rules.
- One bullish or bearish Fair Value Gap event detected from a minimal valid candle sequence.
- Insufficient candle history returns an empty list.
- Rolling/windowed detection behavior as new completed candles are appended.
- Stable `event_id` for the same completed pattern across overlapping rolling-window calls.
- No duplicate event emission for the same completed pattern when using the documented `seen_event_ids` caller pattern or optional helper, if implemented.
- Missing required candle columns raise a clear deterministic error.
- Unsorted candle input behavior matches the documented implementation choice.

## Integration Tests

- Not required for the first implementation unless the owner explicitly asks for WebSocket or backtest wiring.
- If a lightweight integration-style test is added, it must call only the pure detector with in-memory candle data.

## Contract Tests

- Verify the detector accepts the existing standard candle schema.
- Verify returned event records expose the required common fields and Fair Value Gap fields.
- Verify the detector does not require Binance-specific raw fields.

## Safety Tests

- Verify implementation imports do not introduce exchange order clients or order execution dependencies.
- Verify tests do not call real exchange endpoints.
- Verify no API keys, `.env` files, or live-trading toggles are required.

# Verification

Default verification for the future implementation:

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
- relevant indicator task documents
- relevant pattern definition documents

# Codex Self-Review Requirement

Before completion of any implementation work under this task, run through `reviews/CODEX_SELF_REVIEW.md` and include the result in the final summary.

For this task-document creation step, perform the same self-review at documentation scope and confirm no application behavior was implemented.

# PR Review Requirement

Use `reviews/REVIEW_CHECKLIST.md` and `docs/06_PR_REVIEW_PROCESS.md` before merge.

Review must be strict about:

- Scope expansion beyond Fair Value Gap and the minimal engine contract.
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
