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
