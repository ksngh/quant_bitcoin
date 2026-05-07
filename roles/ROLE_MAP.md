# Role Map

| Role | Owns | Must Not Own |
| --- | --- | --- |
| Requirement Owner | raw requirement, clean requirement, user goal, acceptance criteria | implementation details, trading execution |
| Architect | architecture boundaries, responsibility ownership, data contracts | hidden scope expansion, unrequested frameworks |
| Implementer | assigned task implementation only | unrelated files, future-phase features |
| Test Designer | required tests, test data, verification commands | production behavior, live exchange calls |
| Reviewer | PR checks, scope validation, safety validation | silent redesign, unreviewed architecture changes |
| Market Data Provider | local candle loading, Binance historical candle fetching later, normalization to candle schema | signals, quantity decisions, order execution, risk management |
| Strategy | indicator calculation required by strategy, BUY / SELL / HOLD signal generation | fetching data, Binance calls, order execution, quantity decisions, file/database writes |
| Backtest Engine | historical simulation, simple backtest result | live exchange calls, real orders, strategy rules |
| Execution | paper trading actions, later live execution only when explicitly requested | RSI calculation, strategy rules, market data fetching |
| Configuration | local settings, later environment variable reads | hardcoded secrets, business logic, trading decisions |
