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
    price: float | None = None
    cash_after: float | None = None
    position_after: float | None = None


@dataclass
class PaperTrader:
    """Record fake trades from strategy signals without exchange access."""

    trades: list[PaperTrade] = field(default_factory=list)
    cash_balance: float = 0.0
    positions: dict[str, float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _validate_non_negative_cash(self.cash_balance)
        self.cash_balance = float(self.cash_balance)
        self.positions = {
            _validate_symbol(symbol): _validate_position_quantity(quantity)
            for symbol, quantity in self.positions.items()
        }

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

    def apply_signal(
        self, symbol: str, signal: Signal, quantity: float, price: float
    ) -> PaperTrade | None:
        """Apply a signal to local paper cash, positions, and trade history.

        BUY decreases local paper cash and increases the symbol position. SELL
        increases local paper cash and decreases the symbol position. HOLD
        leaves all local state unchanged. No exchange, market-data, or order API
        is called.
        """

        normalized_symbol = _validate_symbol(symbol)
        _validate_signal(signal)
        normalized_quantity = _validate_quantity(quantity)
        normalized_price = _validate_price(price)

        if signal is Signal.HOLD:
            return None

        if signal is Signal.BUY:
            return self._apply_buy(
                symbol=normalized_symbol,
                quantity=normalized_quantity,
                price=normalized_price,
            )

        return self._apply_sell(
            symbol=normalized_symbol,
            quantity=normalized_quantity,
            price=normalized_price,
        )

    def _apply_buy(self, symbol: str, quantity: float, price: float) -> PaperTrade:
        cost = quantity * price
        if cost > self.cash_balance:
            raise ValueError("insufficient paper cash for BUY")

        self.cash_balance -= cost
        position_after = self.positions.get(symbol, 0.0) + quantity
        self.positions[symbol] = position_after
        return self._record_stateful_trade(
            symbol=symbol,
            signal=Signal.BUY,
            quantity=quantity,
            price=price,
            position_after=position_after,
        )

    def _apply_sell(self, symbol: str, quantity: float, price: float) -> PaperTrade:
        current_position = self.positions.get(symbol, 0.0)
        if quantity > current_position:
            raise ValueError("insufficient paper position for SELL")

        self.cash_balance += quantity * price
        position_after = current_position - quantity
        if position_after == 0:
            self.positions.pop(symbol, None)
        else:
            self.positions[symbol] = position_after
        return self._record_stateful_trade(
            symbol=symbol,
            signal=Signal.SELL,
            quantity=quantity,
            price=price,
            position_after=position_after,
        )

    def _record_stateful_trade(
        self,
        *,
        symbol: str,
        signal: Signal,
        quantity: float,
        price: float,
        position_after: float,
    ) -> PaperTrade:
        trade = PaperTrade(
            symbol=symbol,
            signal=signal,
            quantity=quantity,
            price=price,
            cash_after=self.cash_balance,
            position_after=position_after,
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


def _validate_quantity(quantity: float) -> float:
    if not isinstance(quantity, int | float):
        raise ValueError("quantity must be numeric")
    if not isfinite(quantity) or quantity <= 0:
        raise ValueError("quantity must be positive")
    return float(quantity)


def _validate_position_quantity(quantity: float) -> float:
    if not isinstance(quantity, int | float):
        raise ValueError("position quantity must be numeric")
    if not isfinite(quantity) or quantity < 0:
        raise ValueError("position quantity must be non-negative")
    return float(quantity)


def _validate_non_negative_cash(cash_balance: float) -> None:
    if not isinstance(cash_balance, int | float):
        raise ValueError("cash balance must be numeric")
    if not isfinite(cash_balance) or cash_balance < 0:
        raise ValueError("cash balance must be non-negative")


def _validate_price(price: float) -> float:
    if not isinstance(price, int | float):
        raise ValueError("price must be numeric")
    if not isfinite(price) or price <= 0:
        raise ValueError("price must be positive")
    return float(price)
