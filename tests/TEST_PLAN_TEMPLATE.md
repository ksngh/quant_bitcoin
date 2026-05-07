# Test Plan Template

# Feature Under Test


# Source Requirement


# Owner Role


# Test Scope

- 

# Unit Tests

- 

# Integration Tests

- 

# Contract Tests

- 

# Safety Tests

- 

# Test Data

- Local fixtures:
- Mock responses:
- Edge cases:

# Mocking Strategy

- Mock external HTTP calls.
- Do not require real API keys for unit tests.
- Do not call exchange order endpoints.

# Verification Commands

```bash
pytest
```

If configured later:

```bash
ruff check .
mypy .
```

# Exit Criteria

- Required tests pass.
- Safety tests prove no real exchange order behavior.
- Contract tests prove standard candle schema where applicable.
