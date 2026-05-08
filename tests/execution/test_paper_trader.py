from __future__ import annotations

import socket
from math import inf, nan

import pytest

from quant_bitcoin.execution import PaperTrade, PaperTrader
from quant_bitcoin.strategies import Signal


def test_paper_trader_records_buy_fake_trade():
    trader = PaperTrader()

    trade = trader.record_signal("BTCUSDT", Signal.BUY, 0.5)

    assert trade == PaperTrade(symbol="BTCUSDT", signal=Signal.BUY, quantity=0.5)
    assert trader.trades == [trade]


def test_paper_trader_records_sell_fake_trade():
    trader = PaperTrader()

    trade = trader.record_signal("BTCUSDT", Signal.SELL, 0.25)

    assert trade == PaperTrade(symbol="BTCUSDT", signal=Signal.SELL, quantity=0.25)
    assert trader.trades == [trade]


def test_paper_trader_ignores_hold_signal():
    trader = PaperTrader()

    trade = trader.record_signal("BTCUSDT", Signal.HOLD, 1)

    assert trade is None
    assert trader.trades == []


def test_paper_trader_accepts_signal_values_defined_by_strategy_contract():
    trader = PaperTrader()

    buy_trade = trader.record_signal("BTCUSDT", Signal.BUY, 1)
    sell_trade = trader.record_signal("BTCUSDT", Signal.SELL, 1)
    hold_trade = trader.record_signal("BTCUSDT", Signal.HOLD, 1)

    assert buy_trade is not None
    assert sell_trade is not None
    assert hold_trade is None
    assert [trade.signal for trade in trader.trades] == [Signal.BUY, Signal.SELL]


def test_paper_trader_normalizes_symbol_whitespace():
    trader = PaperTrader()

    trade = trader.record_signal(" BTCUSDT ", Signal.BUY, 1)

    assert trade == PaperTrade(symbol="BTCUSDT", signal=Signal.BUY, quantity=1.0)


@pytest.mark.parametrize("symbol", ["", "   "])
def test_paper_trader_rejects_blank_symbol(symbol):
    trader = PaperTrader()

    with pytest.raises(ValueError, match="symbol must not be blank"):
        trader.record_signal(symbol, Signal.BUY, 1)


def test_paper_trader_rejects_non_string_symbol():
    trader = PaperTrader()

    with pytest.raises(ValueError, match="symbol must be a string"):
        trader.record_signal(123, Signal.BUY, 1)  # type: ignore[arg-type]


@pytest.mark.parametrize("quantity", [0, -1, inf, nan])
def test_paper_trader_rejects_non_positive_quantity(quantity):
    trader = PaperTrader()

    with pytest.raises(ValueError, match="quantity must be positive"):
        trader.record_signal("BTCUSDT", Signal.BUY, quantity)


def test_paper_trader_rejects_non_numeric_quantity():
    trader = PaperTrader()

    with pytest.raises(ValueError, match="quantity must be numeric"):
        trader.record_signal("BTCUSDT", Signal.BUY, "1")  # type: ignore[arg-type]


def test_paper_trader_rejects_unknown_signal_value():
    trader = PaperTrader()

    with pytest.raises(ValueError, match="signal must be a Signal value"):
        trader.record_signal("BTCUSDT", "BUY", 1)  # type: ignore[arg-type]


def test_paper_trader_does_not_open_network_connections(monkeypatch):
    trader = PaperTrader()

    def fail_socket_creation(*args, **kwargs):
        raise AssertionError("paper trader must not create network sockets")

    monkeypatch.setattr(socket, "socket", fail_socket_creation)

    trade = trader.record_signal("BTCUSDT", Signal.BUY, 1)

    assert trade == PaperTrade(symbol="BTCUSDT", signal=Signal.BUY, quantity=1.0)


def test_paper_trader_buy_updates_local_cash_position_and_history():
    trader = PaperTrader(cash_balance=1_000)

    trade = trader.apply_signal("BTCUSDT", Signal.BUY, quantity=2, price=100)

    assert trade == PaperTrade(
        symbol="BTCUSDT",
        signal=Signal.BUY,
        quantity=2.0,
        price=100.0,
        cash_after=800.0,
        position_after=2.0,
    )
    assert trader.cash_balance == 800
    assert trader.positions == {"BTCUSDT": 2.0}
    assert trader.trades == [trade]


def test_paper_trader_sell_updates_local_cash_position_and_history():
    trader = PaperTrader(cash_balance=500, positions={"BTCUSDT": 2})

    trade = trader.apply_signal("BTCUSDT", Signal.SELL, quantity=0.5, price=120)

    assert trade == PaperTrade(
        symbol="BTCUSDT",
        signal=Signal.SELL,
        quantity=0.5,
        price=120.0,
        cash_after=560.0,
        position_after=1.5,
    )
    assert trader.cash_balance == 560
    assert trader.positions == {"BTCUSDT": 1.5}
    assert trader.trades == [trade]


def test_paper_trader_sell_removes_symbol_when_position_is_closed():
    trader = PaperTrader(cash_balance=500, positions={"BTCUSDT": 2})

    trade = trader.apply_signal("BTCUSDT", Signal.SELL, quantity=2, price=120)

    assert trade is not None
    assert trade.position_after == 0
    assert trader.cash_balance == 740
    assert trader.positions == {}


def test_paper_trader_hold_leaves_local_state_unchanged():
    trader = PaperTrader(cash_balance=500, positions={"BTCUSDT": 2})

    trade = trader.apply_signal("BTCUSDT", Signal.HOLD, quantity=1, price=120)

    assert trade is None
    assert trader.cash_balance == 500
    assert trader.positions == {"BTCUSDT": 2.0}
    assert trader.trades == []


def test_paper_trader_rejects_buy_when_paper_cash_is_insufficient():
    trader = PaperTrader(cash_balance=50)

    with pytest.raises(ValueError, match="insufficient paper cash for BUY"):
        trader.apply_signal("BTCUSDT", Signal.BUY, quantity=1, price=100)

    assert trader.cash_balance == 50
    assert trader.positions == {}
    assert trader.trades == []


def test_paper_trader_rejects_sell_when_paper_position_is_insufficient():
    trader = PaperTrader(cash_balance=500, positions={"BTCUSDT": 0.5})

    with pytest.raises(ValueError, match="insufficient paper position for SELL"):
        trader.apply_signal("BTCUSDT", Signal.SELL, quantity=1, price=100)

    assert trader.cash_balance == 500
    assert trader.positions == {"BTCUSDT": 0.5}
    assert trader.trades == []


@pytest.mark.parametrize("price", [0, -1, inf, nan])
def test_paper_trader_stateful_signal_rejects_non_positive_price(price):
    trader = PaperTrader(cash_balance=1_000)

    with pytest.raises(ValueError, match="price must be positive"):
        trader.apply_signal("BTCUSDT", Signal.BUY, quantity=1, price=price)


def test_paper_trader_stateful_signal_rejects_non_numeric_price():
    trader = PaperTrader(cash_balance=1_000)

    with pytest.raises(ValueError, match="price must be numeric"):
        trader.apply_signal("BTCUSDT", Signal.BUY, quantity=1, price="100")  # type: ignore[arg-type]


def test_paper_trader_rejects_invalid_initial_cash_balance():
    with pytest.raises(ValueError, match="cash balance must be non-negative"):
        PaperTrader(cash_balance=-1)


def test_paper_trader_rejects_invalid_initial_position_quantity():
    with pytest.raises(ValueError, match="position quantity must be non-negative"):
        PaperTrader(positions={"BTCUSDT": -1})


def test_stateful_paper_trader_does_not_open_network_connections(monkeypatch):
    trader = PaperTrader(cash_balance=1_000)

    def fail_socket_creation(*args, **kwargs):
        raise AssertionError("stateful paper trader must not create network sockets")

    monkeypatch.setattr(socket, "socket", fail_socket_creation)

    trade = trader.apply_signal("BTCUSDT", Signal.BUY, quantity=1, price=100)

    assert trade is not None
    assert trader.cash_balance == 900
