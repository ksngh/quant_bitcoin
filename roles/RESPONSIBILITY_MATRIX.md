# Responsibility Matrix

| Behavior | Owner Role | Supporting Role | Forbidden Role | Required Tests | PR Review Check |
| --- | --- | --- | --- | --- | --- |
| Define candle schema | Architect | Market Data Provider, Test Designer | Strategy, Execution | Contract tests for required fields | Schema matches `docs/04_DATA_CONTRACT.md` |
| Load CSV candle data | Market Data Provider | Test Designer | Strategy, Execution | Unit tests for valid and invalid CSV | Provider returns normalized schema |
| Fetch Binance historical candles | Market Data Provider | Configuration, Test Designer | Strategy, Execution | Mocked fetch test, safety test | No order endpoint is used |
| Normalize Binance raw response | Market Data Provider | Test Designer | Strategy, Execution | Contract test for normalized output | Raw Binance fields do not reach strategy |
| Generate BUY / SELL / HOLD | Strategy | Test Designer | Market Data Provider, Execution | BUY, SELL, HOLD unit tests | Strategy does not fetch data or place orders |
| Calculate RSI | Strategy | Test Designer | Market Data Provider, Execution | RSI behavior tests | RSI formula is inside strategy area only |
| Simulate historical trading | Backtest Engine | Strategy, Market Data Provider, Test Designer | Live order execution | Backtest integration test | No live exchange API calls |
| Record fake trade | Execution | Strategy, Test Designer | Market Data Provider | BUY/SELL/HOLD paper trader tests | Fake trades only; no exchange calls |
| Place real order | Later live execution only | Reviewer, Configuration | Current first version | Not allowed now | Must be rejected unless explicitly requested later |
| Decide task scope | Requirement Owner | Architect, Reviewer | Implementer alone | Documentation review | Scope matches requirement and task |
| Define acceptance criteria | Requirement Owner | Test Designer, Reviewer | Runtime components | Requirement review | Criteria are testable |
| Define required tests | Test Designer | Requirement Owner, Reviewer | Runtime components alone | Test plan review | Tests cover behavior, contract, and safety |
| Review PR | Reviewer | Architect, Test Designer | Implementer alone | Review checklist | Findings cover scope, tests, safety, and docs |
