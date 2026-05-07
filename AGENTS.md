# Project

This is a Python Bitcoin quantitative trading project.

The project starts small and evolves gradually. The current focus is candle data, technical-analysis strategies, basic backtesting, and paper trading.

# Current Scope

The current scope is:

- project setup
- market data contract
- CSV/local data provider
- RSI strategy
- basic backtest
- paper trader
- Binance historical candle downloader later

# Out of Scope by Default

Do not implement the following unless explicitly requested in an assigned task:

- live trading
- real Binance order execution
- risk management
- dashboard
- database
- scheduler
- FastAPI
- Streamlit
- Docker
- machine learning
- futures
- leverage
- portfolio optimization

# Working Rules

- Read `AGENTS.md` before working.
- Read the relevant docs before working.
- Read the assigned task file before coding.
- If the requirement is unclear, extract roles and write assumptions before implementation.
- Make small, incremental changes.
- Do not expand scope beyond the assigned task.
- Do not modify unrelated files.
- Add or update tests when implementation tasks are performed later.
- Run verification commands when possible.
- Summarize changed files, behavior added, tests run, and known limitations.

# Requirement-to-Implementation Workflow

Raw requirement
-> Clean requirement
-> Role extraction
-> Responsibility boundary check
-> Task document
-> Test plan
-> Implementation
-> Codex self-review
-> PR review
-> Decision/doc update if needed

# Safety Rules

- Do not hardcode API keys.
- Do not commit `.env` files.
- Do not place real orders unless a future task explicitly asks for real order execution.
- Paper trading must never call real exchange order APIs.
- Binance candle downloading is allowed only for data collection, not order execution.
- Strategy code must never call exchange APIs.

# Completion Rules

Every implementation task must end with:

- files changed
- implementation summary
- tests added or updated
- tests run
- known limitations
- recommended next task
