# Scope Check

- Did Codex only implement the assigned task?
- Did Codex avoid unrelated files?
- Did Codex avoid future-phase features?
- Did Codex avoid adding unrequested frameworks or services?

# Requirement Match Check

- Does the change satisfy the clean requirement?
- Are assumptions documented?
- Are acceptance criteria met or explicitly marked incomplete?

# Role Ownership Check

- Is the behavior owned by the correct role?
- Are supporting roles limited to support responsibilities?
- Did forbidden roles remain unchanged?

# Architecture Boundary Check

- Does strategy avoid data fetching?
- Does strategy avoid order execution?
- Does market data avoid signal generation?
- Does market data avoid quantity decisions?
- Does backtest avoid live exchange order APIs?
- Does execution avoid indicator calculation and strategy rules?
- Does app wiring avoid embedded business logic?

# Data Contract Check

- Does candle data follow `timestamp`, `open`, `high`, `low`, `close`, `volume`?
- Are rows sorted ascending by `timestamp` where data is returned?
- Are numeric fields numeric?
- Are Binance-specific fields normalized before strategy code sees data?

# Test Check

- Were tests added or updated when implementation code changed?
- Were required unit, integration, contract, and safety tests covered where applicable?
- Were relevant tests run?
- Are failures explained?

# Safety Check

- Are API keys absent from code?
- Is `.env` not committed?
- Are real order APIs avoided unless explicitly requested?
- Does paper trading avoid real exchange calls?
- Does Binance candle downloading avoid order endpoints?
- Do tests avoid real exchange order endpoints?
- Is there no `ENABLE_LIVE_TRADING=true` default?

# Simplicity Check

- Is the implementation small?
- Are there unnecessary abstractions?
- Did Codex avoid adding frameworks?
- Did Codex avoid redesigning public interfaces outside scope?

# Documentation Check

- Were docs updated when behavior or architecture changed?
- Were decisions updated when a new architecture decision was made?
- Were task and test documents kept consistent?

# Parallel Work Check

- Was parallelism limited to independent leaf tasks?
- Were shared contracts kept out of parallel batches?
- Were public interfaces not renamed or redesigned during parallel work?
- If a shared contract change was needed, did Codex stop and report it?
