"""In-memory paper trading components.

This module is intentionally limited to execution-simulation responsibilities:
it receives a symbol, strategy signal, and quantity, then records fake trades
for BUY and SELL signals. It does not fetch market data, calculate indicators,
or call exchange APIs.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from math import isfinite

from quant_bitcoin.strategies import Signal


@dataclass(frozen=True)
class PaperTrade:
    """A fake trade recorded by the paper trader."""

    symbol: str
    signal: Signal
    quantity: float


@dataclass
class PaperTrader:
    """Record fake trades from strategy signals without exchange access."""

    trades: list[PaperTrade] = field(default_factory=list)

    def record_signal(
        self, symbol: str, signal: Signal, quantity: float
    ) -> PaperTrade | None:
        """Record a fake BUY/SELL trade or ignore HOLD.

        Args:
            symbol: Market symbol for the fake trade.
            signal: Strategy signal from the strategy contract.
            quantity: Fake quantity to record for BUY or SELL signals.

        Returns:
            The recorded fake trade for BUY/SELL, or ``None`` for HOLD.

        Raises:
            ValueError: If symbol is blank, signal is not a ``Signal`` value, or
                quantity is not positive.
        """

        normalized_symbol = _validate_symbol(symbol)
        _validate_signal(signal)
        _validate_quantity(quantity)

        if signal is Signal.HOLD:
            return None

        trade = PaperTrade(
            symbol=normalized_symbol,
            signal=signal,
            quantity=float(quantity),
        )
        self.trades.append(trade)
        return trade


def _validate_symbol(symbol: str) -> str:
    if not isinstance(symbol, str):
        raise ValueError("symbol must be a string")
    normalized_symbol = symbol.strip()
    if not normalized_symbol:
        raise ValueError("symbol must not be blank")
    return normalized_symbol


def _validate_signal(signal: Signal) -> None:
    if not isinstance(signal, Signal):
        raise ValueError("signal must be a Signal value")


def _validate_quantity(quantity: float) -> None:
    if not isinstance(quantity, int | float):
        raise ValueError("quantity must be numeric")
    if not isfinite(quantity) or quantity <= 0:
        raise ValueError("quantity must be positive")
