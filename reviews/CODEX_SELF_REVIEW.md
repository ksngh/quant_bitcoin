# Codex Self-Review

## Scope

- Did I only address the assigned task?
- Did I avoid unrelated files?
- Did I avoid future-phase features?

## Requirement Match

- Did the change satisfy the clean requirement?
- Did I document assumptions?
- Did I meet the acceptance criteria?

## Role Ownership

- Did the owner role own the behavior?
- Did supporting roles stay limited?
- Did forbidden roles remain untouched?

## Architecture

- Did strategy avoid data fetching and order execution?
- Did market data avoid signals and quantity decisions?
- Did execution avoid indicator calculations and strategy rules?
- Did app wiring avoid embedded business logic?

## Tests

- Did I add or update tests for changed code?
- Did I include unit, integration, contract, or safety tests as required?
- Did I run verification commands when possible?
- Did I explain failures?

## Safety

- Did I avoid hardcoded API keys?
- Did I avoid committing `.env` files?
- Did I avoid real order APIs unless explicitly requested?
- Did paper trading avoid real exchange calls?

## Simplicity

- Is the change small?
- Did I avoid unnecessary abstractions?
- Did I avoid adding unrequested frameworks or services?

## Completion Summary

- files changed
- implementation summary
- tests added or updated
- tests run
- known limitations
- recommended next task
