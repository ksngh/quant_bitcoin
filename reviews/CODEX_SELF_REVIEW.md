# Codex Self-Review

# Scope

- Did I implement only the assigned task?
- Did I modify unrelated files?
- Did I avoid future-phase features?

# Requirement Match

- Did the change satisfy the clean requirement?
- Did I document assumptions?
- Did I meet the acceptance criteria?

# Status Tracking

- Did I read `STATUS.md`?
- Did I update `STATUS.md` if the project state changed?
- Did I avoid marking uncertain items as complete?

# Role Ownership

- Did I violate role ownership?
- Did the owner role own the behavior?
- Did supporting roles stay limited?
- Did forbidden roles remain untouched?

# Architecture

- Did I violate architecture boundaries?
- Did strategy avoid data fetching and order execution?
- Did market data avoid signals and quantity decisions?
- Did execution avoid indicator calculations and strategy rules?
- Did app wiring avoid embedded business logic?

# Tests

- Did I add or update tests?
- Did I include unit, integration, contract, or safety tests as required?
- Did I run verification?
- Did I explain failures?

# Safety

- Did I hardcode secrets?
- Did I avoid committing `.env` files?
- Did I accidentally add real trading behavior?
- Did I accidentally call exchange order APIs?
- Did paper trading avoid real exchange calls?
- Did Binance candle downloading avoid order endpoints?
- Did tests avoid real exchange order endpoints?

# Simplicity

- Did I add unnecessary abstractions?
- Did I avoid unrequested frameworks or services?
- Did I keep the change small?

# Documentation Updates

- Did I update docs or decisions if behavior changed?
- Did I keep requirement, task, test, and review documents consistent?

# Completion Summary

The final task summary must include:

- files changed
- implementation summary
- tests added or updated
- tests run
- Codex self-review result
- known limitations
- recommended next task
