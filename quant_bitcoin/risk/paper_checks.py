"""Paper-only risk checks for proposed trades.

This module is intentionally limited to risk-management decisions. It evaluates
proposed paper actions against local paper cash and position values, then returns
a deterministic decision. It does not mutate state, fetch market data, calculate
strategy indicators, place orders, or call exchange APIs.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

from quant_bitcoin.strategies import Signal


@dataclass(frozen=True)
class RiskDecision:
    """Decision returned by paper risk checks."""

    approved: bool
    reason: str


@dataclass(frozen=True)
class PaperRiskChecker:
    """Approve or reject proposed paper trades without mutating state."""

    def check(
        self,
        *,
        symbol: str,
        signal: Signal,
        quantity: float,
        price: float,
        cash_balance: float,
        current_position: float,
    ) -> RiskDecision:
        """Return a deterministic risk decision for a proposed paper action."""

        try:
            _validate_symbol(symbol)
            _validate_signal(signal)
            normalized_quantity = _validate_positive_number(quantity)
            normalized_price = _validate_positive_number(price)
            normalized_cash = _validate_non_negative_number(cash_balance)
            normalized_position = _validate_non_negative_number(current_position)
        except ValueError:
            return RiskDecision(approved=False, reason="invalid_input")

        if signal is Signal.HOLD:
            return RiskDecision(approved=True, reason="hold_no_trade")

        if signal is Signal.BUY:
            notional = normalized_quantity * normalized_price
            if notional > normalized_cash:
                return RiskDecision(approved=False, reason="insufficient_cash")
            return RiskDecision(approved=True, reason="approved")

        if normalized_quantity > normalized_position:
            return RiskDecision(approved=False, reason="insufficient_position")
        return RiskDecision(approved=True, reason="approved")


def _validate_symbol(symbol: str) -> None:
    if not isinstance(symbol, str) or not symbol.strip():
        raise ValueError("symbol must be a non-blank string")


def _validate_signal(signal: Signal) -> None:
    if not isinstance(signal, Signal):
        raise ValueError("signal must be a Signal value")


def _validate_positive_number(value: float) -> float:
    if not isinstance(value, int | float) or not isfinite(value) or value <= 0:
        raise ValueError("value must be positive")
    return float(value)


def _validate_non_negative_number(value: float) -> float:
    if not isinstance(value, int | float) or not isfinite(value) or value < 0:
        raise ValueError("value must be non-negative")
    return float(value)
