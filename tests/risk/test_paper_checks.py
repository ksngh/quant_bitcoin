from __future__ import annotations

import socket
from math import inf, nan

import pytest

from quant_bitcoin.execution import PaperTrader
from quant_bitcoin.risk import PaperRiskChecker, RiskDecision
from quant_bitcoin.strategies import Signal


def test_buy_with_sufficient_paper_cash_is_approved():
    decision = PaperRiskChecker().check(
        symbol="BTCUSDT",
        signal=Signal.BUY,
        quantity=2,
        price=100,
        cash_balance=250,
        current_position=0,
    )

    assert decision == RiskDecision(approved=True, reason="approved")


def test_buy_with_insufficient_paper_cash_is_rejected():
    decision = PaperRiskChecker().check(
        symbol="BTCUSDT",
        signal=Signal.BUY,
        quantity=2,
        price=100,
        cash_balance=199.99,
        current_position=0,
    )

    assert decision == RiskDecision(approved=False, reason="insufficient_cash")


def test_sell_with_sufficient_paper_position_is_approved():
    decision = PaperRiskChecker().check(
        symbol="BTCUSDT",
        signal=Signal.SELL,
        quantity=0.5,
        price=100,
        cash_balance=0,
        current_position=1,
    )

    assert decision == RiskDecision(approved=True, reason="approved")


def test_sell_with_insufficient_paper_position_is_rejected():
    decision = PaperRiskChecker().check(
        symbol="BTCUSDT",
        signal=Signal.SELL,
        quantity=2,
        price=100,
        cash_balance=0,
        current_position=1,
    )

    assert decision == RiskDecision(
        approved=False, reason="insufficient_position"
    )


def test_hold_is_handled_as_no_trade():
    decision = PaperRiskChecker().check(
        symbol="BTCUSDT",
        signal=Signal.HOLD,
        quantity=1,
        price=100,
        cash_balance=0,
        current_position=0,
    )

    assert decision == RiskDecision(approved=True, reason="hold_no_trade")


@pytest.mark.parametrize(
    "kwargs",
    [
        {"symbol": ""},
        {"symbol": "   "},
        {"signal": "BUY"},
        {"quantity": 0},
        {"quantity": -1},
        {"quantity": inf},
        {"quantity": nan},
        {"quantity": "1"},
        {"price": 0},
        {"price": -1},
        {"price": inf},
        {"price": nan},
        {"price": "100"},
        {"cash_balance": -1},
        {"cash_balance": inf},
        {"cash_balance": nan},
        {"cash_balance": "100"},
        {"current_position": -1},
        {"current_position": inf},
        {"current_position": nan},
        {"current_position": "1"},
    ],
)
def test_invalid_inputs_are_reported_explicitly(kwargs):
    params = {
        "symbol": "BTCUSDT",
        "signal": Signal.BUY,
        "quantity": 1,
        "price": 100,
        "cash_balance": 1_000,
        "current_position": 0,
    }
    params.update(kwargs)

    decision = PaperRiskChecker().check(**params)

    assert decision == RiskDecision(approved=False, reason="invalid_input")


def test_risk_check_accepts_existing_strategy_signal_values():
    checker = PaperRiskChecker()

    buy_decision = checker.check(
        symbol="BTCUSDT",
        signal=Signal.BUY,
        quantity=1,
        price=100,
        cash_balance=100,
        current_position=0,
    )
    sell_decision = checker.check(
        symbol="BTCUSDT",
        signal=Signal.SELL,
        quantity=1,
        price=100,
        cash_balance=0,
        current_position=1,
    )
    hold_decision = checker.check(
        symbol="BTCUSDT",
        signal=Signal.HOLD,
        quantity=1,
        price=100,
        cash_balance=0,
        current_position=0,
    )

    assert buy_decision.approved is True
    assert sell_decision.approved is True
    assert hold_decision.reason == "hold_no_trade"


def test_risk_check_does_not_mutate_paper_trader_state():
    trader = PaperTrader(cash_balance=1_000, positions={"BTCUSDT": 2})
    original_trades = list(trader.trades)
    original_positions = dict(trader.positions)

    decision = PaperRiskChecker().check(
        symbol="BTCUSDT",
        signal=Signal.BUY,
        quantity=1,
        price=100,
        cash_balance=trader.cash_balance,
        current_position=trader.positions["BTCUSDT"],
    )

    assert decision == RiskDecision(approved=True, reason="approved")
    assert trader.cash_balance == 1_000
    assert trader.positions == original_positions
    assert trader.trades == original_trades


def test_risk_check_does_not_open_network_connections(monkeypatch):
    def fail_socket_creation(*args, **kwargs):
        raise AssertionError("paper risk checks must not create network sockets")

    monkeypatch.setattr(socket, "socket", fail_socket_creation)

    decision = PaperRiskChecker().check(
        symbol="BTCUSDT",
        signal=Signal.BUY,
        quantity=1,
        price=100,
        cash_balance=100,
        current_position=0,
    )

    assert decision == RiskDecision(approved=True, reason="approved")
