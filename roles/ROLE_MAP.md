# Role Map

## Requirement Owner

Owns:

- raw requirement capture
- clean requirement
- problem and user goal
- acceptance criteria

Must not own:

- implementation details
- test execution
- runtime architecture responsibilities

## Architect

Owns:

- responsibility boundaries
- architecture decisions
- scope fit across components

Must not own:

- unrequested feature expansion
- hidden business logic

## Implementer

Owns:

- smallest in-scope code change for an assigned task
- local verification commands
- completion summary

Must not own:

- changing requirements without documenting them
- adding unrelated features

## Test Designer

Owns:

- required tests
- test data expectations
- safety and contract test coverage

Must not own:

- production behavior outside the task
- skipping tests for changed behavior

## Reviewer

Owns:

- scope review
- requirement match
- architecture boundary checks
- safety checks

Must not own:

- approving undocumented scope expansion
- accepting missing verification without explanation

## Market Data Provider

Owns:

- loading local candle data
- later fetching Binance historical candles
- normalizing data into the standard candle schema

Must not own:

- trading signals
- execution
- quantity decisions
- risk management

## Strategy

Owns:

- indicator calculations needed by the strategy
- BUY / SELL / HOLD signal generation
- optional signal reason

Must not own:

- data fetching
- exchange API calls
- order placement
- quantity decisions
- API keys

## Backtest Engine

Owns:

- historical simulation loop
- strategy invocation on historical candles
- basic backtest result

Must not own:

- real order execution
- live exchange calls
- strategy rule definition

## Execution

Owns:

- paper trading behavior
- fake trade records
- later live execution only when explicitly requested

Must not own:

- strategy indicators
- market data fetching
- strategy rule definition

## Configuration

Owns:

- local settings
- later environment variable reads

Must not own:

- hardcoded secrets
- business logic
- trading decisions
