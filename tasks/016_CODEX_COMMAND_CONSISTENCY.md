# Task 016: Codex Command Consistency

# Goal

Create a consistent command format and response workflow for future Codex requests in this project.

# Source Requirement

User request on 2026-05-11:

- Make Codex act consistently when the user gives new commands.
- Support coding requests, documentation requests, review requests, and other project commands.
- Explain whether project documents or rules should change.
- Save reusable example prompts if consistent prompts are useful.
- User approved creating this task after Codex noted that no active task was assigned.

# Extracted Roles

- Owner role: Project Workflow
- Supporting roles: Product role, Documentation, Quality Review
- Forbidden roles: Market Data Provider, Strategy, Backtest Engine, Execution, Risk Management, Live Trading, Binance order client

# Context

The project already requires Codex to read `AGENTS.md`, read `STATUS.md`, and avoid implementation or documentation changes unless a task document is assigned. This task preserves that rule while documenting a reusable command format that the project owner can use for future requests.

# Scope

- Create a reusable Codex command guide.
- Include prompt templates for coding, documentation, review, status, and task-creation requests.
- Clarify when a task document is required.
- Update project rules only enough to point future Codex sessions to the command guide.
- Update `STATUS.md` for the project-state change.

# Out of Scope

- Changing application code.
- Changing market data, strategy, backtesting, execution, risk, persistence, or trading behavior.
- Weakening the task-document requirement.
- Adding live trading, exchange order execution, API keys, schedulers, dashboards, databases, Docker, FastAPI, Streamlit, or machine learning.
- Creating GitHub pull requests.

# Requirements

- Document a stable prompt format for future user commands.
- Provide copy/paste examples for common request types.
- State that repository-changing coding and documentation requests require an assigned task document.
- State that answer-only requests do not require repository changes or task assignment.
- State that Codex should stop and ask for a task assignment when a repository-changing request has no assigned task.
- Preserve all existing safety rules around secrets, `.env` files, live trading, and exchange order endpoints.
- Keep the change documentation-only.

# Status Tracking

## Before Implementation

- [x] Read `STATUS.md`.
- [x] Confirm the task matches the current phase and step.
- [x] Confirm the current active task is recorded or should be updated.
- [x] Confirm parallel work is allowed before starting any parallel tasks.
- [x] Record assumptions, blockers, or unclear status items before coding.

## After Implementation

- [x] Update `STATUS.md` if the phase, step, goal, active task, blocker, open question, or completion state changed.
- [x] Mark checklist items complete only when acceptance criteria and verification are satisfied.
- [x] Leave uncertain items open and document the uncertainty.
- [x] Confirm the next step is accurate or explicitly left undecided.

# Acceptance Criteria

- A command guide exists under `docs/`.
- `AGENTS.md` references the command guide for consistent command handling.
- The guide includes reusable prompt templates.
- The guide distinguishes answer-only, task-creation, documentation, coding, review, and status requests.
- The guide does not authorize implementation without an assigned task document.
- Verification passes with `git diff --check`.

# Required Tests

## Unit Tests

- Not required. This is documentation-only.

## Integration Tests

- Not required. This is documentation-only.

## Contract Tests

- Not required. This is documentation-only.

## Safety Tests

- Manual documentation review for scope expansion, live trading, exchange order calls, secrets, and `.env` handling.

# Verification

Default:

```bash
git diff --check
```

# Codex Self-Review Requirement

Before completion, run through `reviews/CODEX_SELF_REVIEW.md` and include the result in the final summary.

# PR Review Requirement

Use `reviews/REVIEW_CHECKLIST.md` and `docs/06_PR_REVIEW_PROCESS.md` before merge if a pull request is opened.

# Completion Summary Required

- files changed
- implementation summary
- tests added or updated
- tests run
- Codex self-review result
- known limitations
- recommended next task
