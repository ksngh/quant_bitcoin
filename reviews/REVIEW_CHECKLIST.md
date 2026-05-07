# Scope Check

- Did Codex only implement the assigned task?
- Did Codex avoid unrelated files?
- Did Codex avoid adding future-phase features?

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
- Does data provider avoid signal generation?
- Does execution avoid indicator calculation?

# Data Contract Check

- Does candle data follow `timestamp`, `open`, `high`, `low`, `close`, `volume`?
- Are Binance-specific fields normalized before strategy code?

# Test Check

- Were tests added or updated when code changed?
- Were relevant tests run?
- Are failures explained?

# Safety Check

- Are API keys absent from code?
- Is `.env` not committed?
- Are real order APIs avoided unless explicitly requested?
- Does paper trading avoid real exchange calls?

# Simplicity Check

- Is the implementation small?
- Are there unnecessary abstractions?
- Did Codex avoid adding frameworks?

# Documentation Check

- Were docs updated when behavior or architecture changed?
- Were decisions updated when a new architecture decision was made?
- Were task and test documents kept consistent?
