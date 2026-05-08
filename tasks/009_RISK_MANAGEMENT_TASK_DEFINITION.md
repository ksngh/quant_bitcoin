# Task 009: Risk Management Task Definition

# Goal

Define the first concrete risk-management implementation task before any risk-management code is written.

# Source Requirement

`docs/08_ROADMAP.md` Phase 11: Later Risk Management.

# Extracted Roles

- Owner role: Architect
- Supporting roles: Risk Management, Test Designer, Execution
- Forbidden roles: Live Execution, Binance order client, Strategy, Market Data Provider

# Context

The roadmap intentionally leaves Phase 11 risk-management features to be defined by a future requirement. Risk management was out of scope for the first-version implementation. Before adding risk-management code, the project needs a documented task that defines ownership, responsibility boundaries, safety constraints, and acceptance criteria.

# Scope

- review existing docs and current implementation boundaries
- define the first risk-management implementation task in a new task document
- specify risk-management ownership and forbidden responsibilities
- specify tests and safety checks required for the future implementation
- update `STATUS.md` after the future task is selected

# Out of Scope

- implementing risk-management code
- changing strategy behavior
- changing backtest behavior
- changing paper trader behavior
- live trading
- real exchange APIs
- Binance order execution
- order routing
- real account state
- portfolio optimization
- machine learning
- futures
- leverage
- dashboard
- database
- scheduler

# Requirements

- No application code may be implemented in this task.
- The future risk-management task must explicitly define its input contract and output behavior.
- The future risk-management task must state that it does not place real orders or call exchange APIs.
- The future risk-management task must define safety tests before implementation starts.
- If risk-management requirements are unclear, record open questions in `STATUS.md` instead of implementing code.

# Status Tracking

## Before Implementation

- [ ] Read `AGENTS.md`.
- [ ] Read `STATUS.md`.
- [ ] Read `docs/08_ROADMAP.md` Phase 11.
- [ ] Confirm this task matches the current phase and step.
- [ ] Record assumptions, blockers, or unclear items in `STATUS.md` before coding if needed.

## After Implementation

- [ ] Update `STATUS.md` if the phase, step, goal, active task, blocker, open question, or completion state changed.
- [ ] Mark checklist items complete only when acceptance criteria and verification are satisfied.
- [ ] Leave uncertain items open and document the uncertainty.
- [ ] Confirm the next step is accurate or explicitly left undecided.

# Acceptance Criteria

- A future risk-management implementation task is defined in a task document.
- The future task includes owner/supporting/forbidden roles.
- The future task includes scope, out-of-scope items, requirements, acceptance criteria, tests, safety checks, and review checklist.
- No application code is changed.
- Existing tests continue to pass.

# Required Tests

- Unit Tests: none required because this is a documentation/task-definition task.
- Integration Tests: none required.
- Contract Tests: none required.
- Safety Tests: verify no application code or live-trading configuration changed.

# Review Checklist

- No application code was implemented.
- No live trading was introduced.
- No real exchange API usage was introduced.
- No Binance order execution was introduced.
- No risk-management behavior was implemented before the task was defined.
- `STATUS.md` accurately points to the next safe step.

# Verification

```bash
pytest
```
