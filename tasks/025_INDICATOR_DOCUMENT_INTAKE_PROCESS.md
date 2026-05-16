# Task 025: Indicator Document Intake Process

# Goal

Define the workflow for collecting user-provided technical indicator documents, storing them as project task inputs, and later implementing each approved indicator in small, reviewable tasks.

This task is a planning/documentation task only. It establishes how future indicator work should be requested and tracked; it does not implement indicator code.

# Source Requirement

The project owner wants to start building code that finds and computes indicators needed for future strategy work.

Requested process:

1. First define what the indicators are and work on them one by one.
2. The project owner will provide documents for each indicator, including indicator information and implementation guidance.
3. Codex should save the provided document content, then later implement code from that saved document when an implementation task is assigned.
4. Create this process as a task document so Codex can recognize the future workflow.
5. Continue to follow `AGENTS.md`.

# Clean Requirement

Create a documented intake workflow for future technical indicator work. When the project owner provides an indicator document, Codex must save it as an indicator-specific task input and must not implement code until a separate implementation task explicitly assigns that indicator.

# Extracted Roles

- Owner role: Product / Task Planning
- Supporting roles:
  - Strategy, for later indicator calculation implementation only when explicitly assigned.
  - Test Designer, for future deterministic indicator tests.
  - Documentation, for preserving owner-provided indicator specifications.
- Forbidden roles:
  - Market Data Provider, unless a later task explicitly changes candle inputs or data contracts.
  - Execution, because indicator work must not place trades or decide order execution.
  - Live Trading, because indicator work must not call real exchange order APIs.
  - Risk Management, unless a later task explicitly assigns risk controls.
  - Database, unless a later task explicitly assigns persistence for indicator outputs.

# Context

The project currently has an RSI strategy and backtesting/paper-trading foundations. Future indicators should be introduced incrementally without expanding into live trading, order execution, dashboards, schedulers, or unrelated infrastructure.

Indicator work must preserve existing architecture boundaries:

- Strategy/indicator code may calculate indicators from already-provided candle data.
- Strategy/indicator code must not fetch market data.
- Strategy/indicator code must not call Binance or any exchange API.
- Strategy/indicator code must not place orders, decide trade quantity, or read API keys.

# Proposed Indicator Document Storage

Future owner-provided indicator documents should be saved under:

```text
tasks/indicators/<INDICATOR_KEY>.md
```

Naming rules:

- Use lowercase snake_case for `<INDICATOR_KEY>`.
- Use a clear, stable indicator name, for example `macd.md`, `bollinger_bands.md`, or `stochastic_rsi.md`.
- Do not overwrite an existing indicator document unless the owner explicitly asks to update that indicator specification.

Each saved indicator document should preserve the owner-provided source text and add a small structured header when useful:

```markdown
# Indicator: <Name>

# Source Requirement

<owner-provided content>

# Implementation Notes

- To be implemented only by a later assigned implementation task.
- Assumptions or unclear items should be recorded here before coding.
```

# Future Workflow

## Step 1: Indicator Document Intake

When the owner sends an indicator document and asks Codex to save it:

- Read `AGENTS.md`, `STATUS.md`, and this task document.
- Save the provided content under `tasks/indicators/<INDICATOR_KEY>.md`.
- Preserve formulas, parameter definitions, edge-case notes, and examples from the owner-provided document.
- Record assumptions or unclear requirements in the saved indicator document.
- Update `STATUS.md` if the active task, next step, open questions, or phase state changes.
- Do not implement application code.

## Step 2: Indicator Implementation Task Creation

Before writing indicator code, create or update a separate implementation task document for that specific indicator.

The implementation task must define:

- Raw requirement and clean requirement.
- Owner role and forbidden roles.
- Input candle fields.
- Output indicator fields or signal inputs.
- Calculation formula and parameters.
- Warm-up/insufficient-data behavior.
- Numeric precision or tolerance expectations.
- Required deterministic tests.
- Safety tests proving no external API calls and no real order execution.

## Step 3: Indicator Implementation

Only after a specific implementation task is assigned, Codex may implement that indicator.

Implementation must:

- Stay limited to the assigned indicator.
- Use local candle data already supplied by callers.
- Add or update deterministic tests.
- Avoid fetching data, placing orders, reading secrets, or introducing live trading behavior.
- Run required verification.
- Complete Codex self-review using `reviews/CODEX_SELF_REVIEW.md`.

# Scope

- Define the indicator document intake workflow.
- Define where future owner-provided indicator documents should be stored.
- Define the minimum fields future indicator implementation tasks must contain.
- Preserve the one-indicator-at-a-time workflow.
- Keep future implementation gated behind explicit task assignment.

# Out of Scope

- Implementing any indicator code.
- Refactoring the existing RSI strategy.
- Changing candle data contracts.
- Changing strategy signal contracts.
- Fetching new market data.
- Adding dashboards, schedulers, databases, Docker changes, FastAPI, Streamlit, machine learning, futures, leverage, or portfolio optimization.
- Live trading or real Binance order execution.
- Risk management implementation.

# Requirements

- The indicator intake process must be documented in this task file.
- Future indicator documents must be stored as task inputs, not silently converted into code.
- Future implementation must require a separate indicator-specific task document.
- Each indicator must be handled independently unless the owner explicitly approves a batch and the work is parallel-safe.
- Shared contract changes must stop the task and be reported before implementation.
- Indicator tasks must include deterministic tests and safety checks.

# Status Tracking

## Before Future Indicator Intake

- [ ] Read `AGENTS.md`.
- [ ] Read `STATUS.md`.
- [ ] Read this task document.
- [ ] Confirm the owner asked Codex to save an indicator document.
- [ ] Confirm the indicator key and target path.
- [ ] Record assumptions, blockers, or unclear items before saving.

## Before Future Indicator Implementation

- [ ] Read `AGENTS.md`.
- [ ] Read `STATUS.md`.
- [ ] Read the saved indicator document under `tasks/indicators/`.
- [ ] Read the assigned indicator-specific implementation task.
- [ ] Confirm no shared contract changes are required.
- [ ] Confirm implementation is limited to the assigned indicator.

## After Future Indicator Implementation

- [ ] Update `STATUS.md` if the phase, step, goal, active task, blocker, open question, or completion state changed.
- [ ] Mark checklist items complete only when acceptance criteria and verification are satisfied.
- [ ] Leave uncertain items open and document the uncertainty.
- [ ] Confirm the next step is accurate or explicitly left undecided.

# Acceptance Criteria

- A clear process exists for saving owner-provided indicator documents.
- The process makes implementation impossible without a later explicit implementation task.
- The process preserves project safety boundaries around market data, strategy, execution, and live trading.
- The process defines minimum expectations for future indicator implementation tasks.
- No application code is changed by this planning task.

# Required Tests

## Unit Tests

- Not required for this planning-only task.
- Future indicator implementation tasks must define deterministic unit tests for calculations, warm-up behavior, and edge cases.

## Integration Tests

- Not required for this planning-only task.
- Future integration tests may be required if an indicator is wired into a strategy or backtest.

## Contract Tests

- Not required for this planning-only task.
- Required in a future task if an indicator changes or adds a public data contract.

## Safety Tests

- Not required for this planning-only task.
- Future implementation tasks must verify indicator code does not fetch market data, call exchange APIs, place orders, or read secrets.

# Review Checklist

- Scope respected.
- Requirement matched.
- Role ownership respected.
- Architecture boundaries respected.
- No application code implemented by this planning task.
- No hardcoded secrets.
- No real order execution.
- No unnecessary abstractions.
- Future indicator implementation remains gated behind explicit task assignment.

# Verification

Default for this documentation-only task:

```bash
git diff --check
```

Optional repository sanity check:

```bash
pytest
```

# Codex Self-Review Requirement

Before completion, run through `reviews/CODEX_SELF_REVIEW.md` and include the result in the final summary.

# PR Review Requirement

Use `reviews/CODEX_SELF_REVIEW.md`, `docs/06_PR_REVIEW_PROCESS.md`, and the review checklist in this file before merge.

# Completion Summary Required

- files changed
- implementation summary
- tests added or updated
- tests run
- Codex self-review result
- known limitations
- recommended next task
