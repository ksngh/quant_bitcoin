# Architecture Decision Log

# 1. Strategy Returns Signal, Not Order

- Status: accepted
- Context: Strategy should express market opinion without owning execution.
- Decision: Strategy returns BUY, SELL, or HOLD, not an order.
- Consequences: Execution decides how to handle signals; strategy cannot place orders or decide quantity.

# 2. Use PaperTrader Before LiveTrader

- Status: accepted
- Context: The project must validate workflows before any real order execution.
- Decision: Paper trading is implemented before live trading.
- Consequences: Early execution code records fake trades only and must not call exchange order APIs.

# 3. Use Standard Candle Schema

- Status: accepted
- Context: Strategy and backtest code should not depend on provider-specific raw data.
- Decision: Candle data uses `timestamp`, `open`, `high`, `low`, `close`, `volume`.
- Consequences: Providers normalize data before strategy code sees it.

# 4. Keep Risk Management Out of First Version

- Status: accepted
- Context: Risk management is important but broad.
- Decision: Do not implement risk management in the first version.
- Consequences: Quantity sizing, exposure rules, and stop rules require future tasks.

# 5. Keep Live Trading Out of First Implementation Phase

- Status: accepted
- Context: Live trading creates safety risk and requires explicit gates.
- Decision: No live order execution in first implementation phase.
- Consequences: Tests and reviews must reject accidental exchange order calls.

# 6. Use Requirement and Role Extraction Before Implementation Tasks

- Status: accepted
- Context: The project needs strict scope control.
- Decision: Convert raw requirements into clean requirements and role ownership before coding.
- Consequences: Each implementation task should identify owner, supporting, and forbidden roles.

# 7. Every Implementation Task Should Define Tests and Review Criteria

- Status: accepted
- Context: Trading code has safety and boundary risks.
- Decision: Each task must include required tests and PR review checks.
- Consequences: Missing tests or review criteria should block completion.

# 8. Codex Self-Review Is Required Before Task Completion

- Status: accepted
- Context: Codex must check its own scope and safety before finishing.
- Decision: Use `reviews/CODEX_SELF_REVIEW.md` before completing implementation tasks.
- Consequences: Final task summaries must include Codex self-review result.

# 9. Codex PR Review Is Required Before Merge

- Status: accepted
- Context: PR review catches scope expansion and architecture boundary violations.
- Decision: Codex review must run before merge.
- Consequences: PR summaries must include requirement, task, tests, safety notes, and limitations.

# 10. Parallelism Is Allowed Only for Independent Leaf Tasks

- Status: accepted
- Context: Parallel work can corrupt shared contracts if used incorrectly.
- Decision: Parallelism is allowed only for independent leaf tasks.
- Consequences: Shared contract changes, public interfaces, and package layout changes must not be parallelized.
