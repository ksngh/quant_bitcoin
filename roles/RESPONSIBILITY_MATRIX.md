# Responsibility Matrix

| Behavior | Owner Role | Supporting Role | Forbidden Role | Required Tests | PR Review Check |
| --- | --- | --- | --- | --- | --- |
| Define candle schema | Architect | Market Data Provider, Test Designer | Strategy, Execution | contract tests | schema is standard and not provider-specific |
| Load CSV candle data | Market Data Provider | Test Designer | Strategy, Execution | unit, contract | returns standard schema and sorted rows |
| Fetch Binance historical candles | Market Data Provider | Configuration, Test Designer | Strategy, Execution | unit with mocks, safety | uses data endpoints only |
| Normalize Binance raw response | Market Data Provider | Test Designer | Strategy, Execution | contract | strategy never sees Binance raw fields |
| Generate BUY / SELL / HOLD | Strategy | Test Designer | Market Data Provider, Execution | unit | no data fetching or order execution |
| Calculate RSI | Strategy | Test Designer | Market Data Provider, Execution | unit | formula stays in strategy layer |
| Simulate historical trading | Backtest Engine | Strategy, Market Data Provider, Test Designer | Live Execution | integration, safety | no live exchange calls |
| Record fake trade | Execution | Test Designer | Strategy, Market Data Provider | unit, safety | fake trade only, no exchange order API |
| Place real order | Future Live Execution | Risk Management when later approved | Current first-version work | future explicit safety tests | rejected unless future task explicitly requests it |
| Decide task scope | Requirement Owner | Architect | Implementer alone | requirement review | scope matches assigned task |
| Define acceptance criteria | Requirement Owner | Test Designer, Reviewer | Implementer alone | acceptance tests | criteria are observable |
| Define required tests | Test Designer | Architect, Reviewer | Market Data Provider alone | test plan | test types match risk |
| Review PR | Reviewer | Architect, Test Designer | Implementer alone | review checklist | scope, tests, architecture, safety checked |
| Perform Codex self-review | Implementer | Reviewer | none | self-review checklist | summary included before completion |
