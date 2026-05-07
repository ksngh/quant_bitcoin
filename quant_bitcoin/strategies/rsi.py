"""RSI-based strategy components.

This module is intentionally limited to strategy responsibilities: it consumes
standard candle data, calculates RSI from close prices, and returns a signal.
It does not fetch market data, choose quantities, or execute orders.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import pandas as pd

STANDARD_CANDLE_COLUMNS: tuple[str, ...] = (
    "timestamp",
    "open",
    "high",
    "low",
    "close",
    "volume",
)


class Signal(Enum):
    """Trading signal returned by strategies."""

    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"


@dataclass(frozen=True)
class RsiStrategy:
    """Generate signals from the latest RSI value.

    Assumption for Task 003: because the task does not define a threshold
    crossing rule, the first implementation uses the latest available RSI
    value only. RSI values at or below ``buy_threshold`` return BUY, values at
    or above ``sell_threshold`` return SELL, and all other cases return HOLD.
    """

    window: int = 14
    buy_threshold: float = 30.0
    sell_threshold: float = 70.0

    def __post_init__(self) -> None:
        if self.window < 1:
            raise ValueError("RSI window must be at least 1")
        if not 0 <= self.buy_threshold <= 100:
            raise ValueError("RSI buy threshold must be between 0 and 100")
        if not 0 <= self.sell_threshold <= 100:
            raise ValueError("RSI sell threshold must be between 0 and 100")
        if self.buy_threshold >= self.sell_threshold:
            raise ValueError("RSI buy threshold must be below sell threshold")

    def generate_signal(self, candles: pd.DataFrame) -> Signal:
        """Return BUY, SELL, or HOLD for standard candle data."""

        rsi = calculate_rsi(candles, window=self.window)
        latest_rsi = rsi.iloc[-1] if not rsi.empty else pd.NA

        if pd.isna(latest_rsi):
            return Signal.HOLD
        if latest_rsi <= self.buy_threshold:
            return Signal.BUY
        if latest_rsi >= self.sell_threshold:
            return Signal.SELL
        return Signal.HOLD


def calculate_rsi(candles: pd.DataFrame, window: int = 14) -> pd.Series:
    """Calculate the simple rolling RSI from standard candle close prices.

    Args:
        candles: Standard candle data containing the required candle schema.
        window: Rolling lookback window for average gains and losses.

    Raises:
        ValueError: If required candle columns are missing, the window is
            invalid, or close prices cannot be treated as numeric values.
    """

    if window < 1:
        raise ValueError("RSI window must be at least 1")
    _validate_standard_candle_schema(candles)

    close = _numeric_close_prices(candles["close"])
    price_changes = close.diff()
    gains = price_changes.clip(lower=0)
    losses = -price_changes.clip(upper=0)

    average_gain = gains.rolling(window=window, min_periods=window).mean()
    average_loss = losses.rolling(window=window, min_periods=window).mean()

    relative_strength = average_gain / average_loss
    rsi = 100 - (100 / (1 + relative_strength))
    rsi = rsi.mask((average_loss == 0) & (average_gain > 0), 100.0)
    rsi = rsi.mask((average_gain == 0) & (average_loss > 0), 0.0)
    rsi = rsi.mask((average_gain == 0) & (average_loss == 0), 50.0)

    return rsi


def _validate_standard_candle_schema(candles: pd.DataFrame) -> None:
    missing_columns = [
        column for column in STANDARD_CANDLE_COLUMNS if column not in candles.columns
    ]
    if missing_columns:
        missing = ", ".join(missing_columns)
        raise ValueError(f"Candle data is missing required columns: {missing}")


def _numeric_close_prices(close_prices: pd.Series) -> pd.Series:
    try:
        return pd.to_numeric(close_prices, errors="raise")
    except (TypeError, ValueError) as error:
        raise ValueError("Candle data contains non-numeric close values") from error
