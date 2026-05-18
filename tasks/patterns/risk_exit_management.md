# Pattern Risk / Exit Management Source Requirement

# Owner Intent

The owner wants future implementation tasks for pattern-specific stop-loss and take-profit timing. The work should convert existing pattern recognition into a risk-manageable trading-system layer without live trading or real exchange order execution.

# Patterns Covered

- Trendline Break Pattern.
- Order Block.
- Fair Value Gap (FVG).
- Cup and Handle.
- Diamond Pattern.
- Adam and Eve Pattern.

# Shared Framework Requested

Future implementation should follow this mechanical framework:

1. Determine entry price.
2. Determine structural stop.
3. Apply ATR-based volatility buffer.
4. Calculate risk per unit.
5. Apply minimum R:R / minimum profit filter.
6. Calculate TP1 / TP2 / TP3.
7. Set time stop.
8. Set trailing stop.
9. Set break-even movement condition.
10. Set partial-exit ratios.

Long stop formula:

```text
structural_stop = pattern_invalidation_price
buffer = ATR(14) * buffer_multiplier
stop_price = structural_stop - buffer
risk_per_unit = entry_price - stop_price
```

Short stop formula:

```text
structural_stop = pattern_invalidation_price
buffer = ATR(14) * buffer_multiplier
stop_price = structural_stop + buffer
risk_per_unit = stop_price - entry_price
```

R-multiple targets:

```text
Long:
risk = entry_price - stop_price
tp1 = entry_price + risk * 1
tp2 = entry_price + risk * 2
tp3 = entry_price + risk * 3

Short:
risk = stop_price - entry_price
tp1 = entry_price - risk * 1
tp2 = entry_price - risk * 2
tp3 = entry_price - risk * 3
```

Structural target candidates:

- Long: nearest swing high, major pivot high, range high, supply zone, bearish order block, liquidity high, measured move target, Fibonacci extension, round number.
- Short: nearest swing low, range low, demand zone, bullish order block, liquidity low, measured move target.

Combined target preference:

```text
TP1 = 1R
TP2 = nearest structure target
TP3 = pattern measured target
```

When combining R multiples and structural targets, use a minimum profit filter so overly close targets do not create poor trades:

```text
If TP1 < 0.8R: skip trade
```

A stricter optional rule may require the nearest target to be at least 1.2R.

# Pattern-Specific Stop Notes

## Trendline Break

Long hypothesis: price broke the existing trendline, weakening the prior direction and creating reversal potential.

Long stop candidates:

- Close re-enters below the broken trendline.
- Breakout candle low is broken.
- Retest pivot low is broken.
- Last swing low before breakout is broken.
- Follow-through fails within N candles.

Mechanical long stop:

```text
stop_price = min(breakout_candle_low, retest_pivot_low) - ATR(14) * 0.2
```

Recommended ATR buffer range: 0.2 to 0.4 ATR.

## Order Block

Bullish hypothesis: price may react when it returns to the zone where institutional buying/selling occurred.

Bullish stop candidates:

- Order-block zone low is broken.
- Start of the impulsive move that formed the order block is broken.
- No reaction within N candles after entering the order block.
- Close below the order-block low.

Mechanical long stop:

```text
stop_price = order_block_low - ATR(14) * 0.2
```

Conservative alternative:

```text
stop_price = order_block_low - ATR(14) * 0.5
```

Automation should prefer entry near the OB 50% or 61.8% line over the upper edge when possible to reduce stop distance and improve R:R. Recommended ATR buffer range: 0.2 to 0.5 ATR.

## Fair Value Gap

Bullish hypothesis: a strong imbalance creates a price void that may be filled or act as a reaction zone.

Bullish stop candidates:

- FVG low is broken.
- Full FVG fill without rebound.
- No reaction within N candles after entering the FVG.
- Close below the FVG.

Mechanical long stop:

```text
stop_price = fvg_low - ATR(14) * 0.2
```

Time-based failure rule:

```text
If price enters FVG and does not close above FVG midpoint within N candles, exit the position.
```

Recommended ATR buffer range: 0.1 to 0.3 ATR.

## Cup and Handle

Long hypothesis: after a rounded base and handle pullback, a neckline breakout may continue the trend.

Long stop candidates:

- Handle low is broken.
- Price closes back below neckline after breakout.
- Breakout candle low is broken.
- Cup midpoint is broken.
- Breakout volume or momentum fails.

Mechanical long stop:

```text
stop_price = handle_low - ATR(14) * 0.2
```

Fast soft exit:

```text
If close < neckline after breakout, exit.
```

Wider hard exit:

```text
If close < handle_low, exit.
```

Recommended ATR buffer range: 0.3 to 0.6 ATR because the pattern is typically larger.

## Diamond

Long breakout hypothesis: after expanding then contracting volatility, a boundary breakout may lead to volatility expansion.

Long stop candidates:

- Price closes back inside the diamond range.
- Breakout candle low is broken.
- Last internal convergence pivot low is broken.
- Failed breakout is followed by opposite-direction breakout.

Mechanical long stop:

```text
stop_price = last_internal_pivot_low - ATR(14) * 0.2
```

Preferred structure:

- Entry: diamond boundary breakout close.
- Soft invalidation: close back inside diamond range.
- Hard stop: last internal pivot low minus ATR buffer.
- Time stop: if price does not move 1R within N candles, exit.

Recommended ATR buffer range: 0.2 to 0.5 ATR.

## Adam and Eve

Long hypothesis: after a sharp V-shaped Adam bottom and rounded Eve accumulation, neckline breakout may complete a double-bottom reversal.

Long stop candidates:

- Eve low is broken.
- Adam low is broken.
- Price closes back below neckline.
- Handle/retest low is broken.
- Breakout candle low is broken.

Mechanical long stop:

```text
stop_price = eve_low - ATR(14) * 0.2
```

Wider alternative:

```text
stop_price = min(adam_low, eve_low) - ATR(14) * 0.2
```

Automation should normally prefer Eve low because Adam-low stops can become too wide and hurt R:R and position sizing. Recommended ATR buffer range: 0.3 to 0.6 ATR.

# Pattern Measured Targets

- Trendline Break: nearest prior swing high/low.
- Cup and Handle: neckline plus cup depth.
- Diamond: breakout price plus diamond height.
- Adam and Eve: neckline plus pattern depth.
- Fair Value Gap: opposing liquidity or previous swing high.
- Order Block: previous liquidity high or market-structure-break target.

# Safety Boundary

This source requirement is about calculation and backtest/paper-trading planning only. It does not approve live trading, real Binance order execution, exchange order endpoints, futures, leverage, scheduler, dashboard, API services, or portfolio optimization.
