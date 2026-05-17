"""Displacement Candle indicator calculation.

This module consumes already-provided candle data, ATR, and volume-ratio values
and emits deterministic strong directional candle labels. It does not fetch
market data, read secrets, call exchange APIs, place orders, or make trading
decisions.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

import pandas as pd

REQUIRED_DISPLACEMENT_CANDLE_COLUMNS: tuple[str, ...] = (
    "symbol",
    "timestamp",
    "open",
    "high",
    "low",
    "close",
)

DISPLACEMENT_CANDLE_OUTPUT_COLUMNS: tuple[str, ...] = (
    "symbol",
    "timestamp",
    "open",
    "high",
    "low",
    "close",
    "candle_range",
    "body_size",
    "upper_wick",
    "lower_wick",
    "body_ratio",
    "close_position_ratio",
    "atr",
    "volume_ratio",
    "displacement_direction",
    "displacement_status",
    "is_displacement",
    "is_valid",
    "reason",
)


class DisplacementDirection(Enum):
    """Supported displacement direction values."""

    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    NONE = "NONE"
    INVALID = "INVALID"


class DisplacementStatus(Enum):
    """Supported displacement status values."""

    VALID = "VALID"
    WEAK = "WEAK"
    NONE = "NONE"
    INVALID = "INVALID"


@dataclass(frozen=True)
class DisplacementCandleConfig:
    """Configuration for deterministic Displacement Candle detection."""

    minimum_body_ratio: float = 0.6
    minimum_range_atr_multiplier: float = 1.5
    minimum_volume_ratio: float = 1.5
    allow_volume_filter: bool = True
    allow_atr_filter: bool = True
    minimum_close_position_ratio: float = 0.7
    reject_zero_range_candle: bool = True

    def __post_init__(self) -> None:
        if not 0 <= self.minimum_body_ratio <= 1:
            raise ValueError("minimum_body_ratio must be between 0 and 1")
        if self.minimum_range_atr_multiplier < 0:
            raise ValueError("minimum_range_atr_multiplier must be non-negative")
        if self.minimum_volume_ratio < 0:
            raise ValueError("minimum_volume_ratio must be non-negative")
        if not 0 <= self.minimum_close_position_ratio <= 1:
            raise ValueError("minimum_close_position_ratio must be between 0 and 1")


def detect_displacement_candles(
    candles: pd.DataFrame, config: DisplacementCandleConfig | None = None
) -> pd.DataFrame:
    """Return Displacement Candle rows for already-provided candle data.

    The returned frame has one row per input candle and includes candle body,
    wick, range, body-ratio, close-position, ATR, volume-ratio, displacement
    direction, status, and validity fields.

    Args:
        candles: Candle data containing symbol, timestamp, open, high, low, and
            close columns. ATR and volume_ratio columns are required only when
            their corresponding filters are enabled and a directional candle
            otherwise reaches those checks.
        config: Displacement Candle configuration. Defaults to
            ``DisplacementCandleConfig()``.

    Raises:
        ValueError: If required columns are missing, numeric values are
            non-numeric, or configuration values are invalid.
    """

    displacement_config = config or DisplacementCandleConfig()
    _validate_candles(candles)

    if candles.empty:
        return _empty_displacement_candle_frame()

    open_values = pd.to_numeric(candles["open"], errors="raise")
    high_values = pd.to_numeric(candles["high"], errors="raise")
    low_values = pd.to_numeric(candles["low"], errors="raise")
    close_values = pd.to_numeric(candles["close"], errors="raise")
    atr_values = _optional_numeric_series(candles, "atr")
    volume_ratio_values = _optional_numeric_series(candles, "volume_ratio")

    rows: list[dict[str, Any]] = []
    for position, (_, candle) in enumerate(candles.iterrows()):
        rows.append(
            detect_displacement_candle(
                {
                    "symbol": candle["symbol"],
                    "timestamp": candle["timestamp"],
                    "open": _optional_float(open_values.iloc[position]),
                    "high": _optional_float(high_values.iloc[position]),
                    "low": _optional_float(low_values.iloc[position]),
                    "close": _optional_float(close_values.iloc[position]),
                    "atr": _series_optional_float(atr_values, position),
                    "volume_ratio": _series_optional_float(
                        volume_ratio_values, position
                    ),
                },
                displacement_config,
            )
        )

    return pd.DataFrame(rows, columns=DISPLACEMENT_CANDLE_OUTPUT_COLUMNS)


def detect_displacement_candle(
    candle: dict[str, Any] | pd.Series,
    config: DisplacementCandleConfig | None = None,
) -> dict[str, Any]:
    """Return a deterministic Displacement Candle snapshot for one candle."""

    displacement_config = config or DisplacementCandleConfig()
    symbol = candle.get("symbol")
    timestamp = candle.get("timestamp")
    open_price = _optional_float(candle.get("open"))
    high = _optional_float(candle.get("high"))
    low = _optional_float(candle.get("low"))
    close = _optional_float(candle.get("close"))
    atr = _optional_float(candle.get("atr"))
    volume_ratio = _optional_float(candle.get("volume_ratio"))

    base = {
        "symbol": symbol,
        "timestamp": timestamp,
        "open": open_price,
        "high": high,
        "low": low,
        "close": close,
        "atr": atr,
        "volume_ratio": volume_ratio,
    }

    if open_price is None or high is None or low is None or close is None:
        return invalid_displacement_result("missing_ohlc", base)

    if high < low:
        return invalid_displacement_result("invalid_high_low", base)

    candle_range = high - low
    if candle_range == 0:
        if displacement_config.reject_zero_range_candle:
            return invalid_displacement_result("zero_range", base)
        return _result_row(
            base,
            candle_range=0.0,
            body_size=0.0,
            upper_wick=0.0,
            lower_wick=0.0,
            body_ratio=0.0,
            close_position_ratio=None,
            direction=DisplacementDirection.NONE,
            status=DisplacementStatus.NONE,
            is_displacement=False,
            is_valid=True,
            reason=None,
        )

    body_size = abs(close - open_price)
    upper_wick = high - max(open_price, close)
    lower_wick = min(open_price, close) - low
    body_ratio = body_size / candle_range

    if close > open_price:
        direction = DisplacementDirection.BULLISH
        close_position_ratio = (close - low) / candle_range
    elif close < open_price:
        direction = DisplacementDirection.BEARISH
        close_position_ratio = (high - close) / candle_range
    else:
        return _result_row(
            base,
            candle_range=candle_range,
            body_size=body_size,
            upper_wick=upper_wick,
            lower_wick=lower_wick,
            body_ratio=body_ratio,
            close_position_ratio=None,
            direction=DisplacementDirection.NONE,
            status=DisplacementStatus.NONE,
            is_displacement=False,
            is_valid=True,
            reason=None,
        )

    status = DisplacementStatus.VALID
    is_displacement = True
    reason = None

    if body_ratio < displacement_config.minimum_body_ratio:
        status = DisplacementStatus.NONE
        is_displacement = False
        reason = "body_ratio_below_threshold"
    elif close_position_ratio < displacement_config.minimum_close_position_ratio:
        status = DisplacementStatus.NONE
        is_displacement = False
        reason = "close_position_below_threshold"
    elif displacement_config.allow_atr_filter and atr is None:
        return invalid_displacement_result("missing_atr", base)
    elif (
        displacement_config.allow_atr_filter
        and candle_range < displacement_config.minimum_range_atr_multiplier * atr
    ):
        status = DisplacementStatus.NONE
        is_displacement = False
        reason = "range_below_atr_threshold"
    elif displacement_config.allow_volume_filter and volume_ratio is None:
        return invalid_displacement_result("missing_volume_ratio", base)
    elif (
        displacement_config.allow_volume_filter
        and volume_ratio < displacement_config.minimum_volume_ratio
    ):
        status = DisplacementStatus.NONE
        is_displacement = False
        reason = "volume_ratio_below_threshold"

    return _result_row(
        base,
        candle_range=candle_range,
        body_size=body_size,
        upper_wick=upper_wick,
        lower_wick=lower_wick,
        body_ratio=body_ratio,
        close_position_ratio=close_position_ratio,
        direction=direction if is_displacement else DisplacementDirection.NONE,
        status=status,
        is_displacement=is_displacement,
        is_valid=True,
        reason=reason,
    )


def calculate_displacement_candle_snapshot(
    candles: pd.DataFrame, config: DisplacementCandleConfig | None = None
) -> dict[str, Any]:
    """Return the latest Displacement Candle output row as a dictionary."""

    displacement_rows = detect_displacement_candles(candles, config)
    if displacement_rows.empty:
        return {column: None for column in DISPLACEMENT_CANDLE_OUTPUT_COLUMNS}
    return displacement_rows.iloc[-1].to_dict()


def invalid_displacement_result(
    reason: str, base: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Return an invalid Displacement Candle result with a reason code."""

    row_base = base or {}
    return _result_row(
        row_base,
        candle_range=None,
        body_size=None,
        upper_wick=None,
        lower_wick=None,
        body_ratio=None,
        close_position_ratio=None,
        direction=DisplacementDirection.INVALID,
        status=DisplacementStatus.INVALID,
        is_displacement=False,
        is_valid=False,
        reason=reason,
    )


def _result_row(
    base: dict[str, Any],
    *,
    candle_range: float | None,
    body_size: float | None,
    upper_wick: float | None,
    lower_wick: float | None,
    body_ratio: float | None,
    close_position_ratio: float | None,
    direction: DisplacementDirection,
    status: DisplacementStatus,
    is_displacement: bool,
    is_valid: bool,
    reason: str | None,
) -> dict[str, Any]:
    return {
        "symbol": base.get("symbol"),
        "timestamp": base.get("timestamp"),
        "open": base.get("open"),
        "high": base.get("high"),
        "low": base.get("low"),
        "close": base.get("close"),
        "candle_range": candle_range,
        "body_size": body_size,
        "upper_wick": upper_wick,
        "lower_wick": lower_wick,
        "body_ratio": body_ratio,
        "close_position_ratio": close_position_ratio,
        "atr": base.get("atr"),
        "volume_ratio": base.get("volume_ratio"),
        "displacement_direction": direction.value,
        "displacement_status": status.value,
        "is_displacement": bool(is_displacement),
        "is_valid": bool(is_valid),
        "reason": reason,
    }


def _validate_candles(candles: pd.DataFrame) -> None:
    missing_columns = [
        column
        for column in REQUIRED_DISPLACEMENT_CANDLE_COLUMNS
        if column not in candles.columns
    ]
    if missing_columns:
        joined = ", ".join(missing_columns)
        raise ValueError(f"missing required Displacement Candle columns: {joined}")


def _optional_numeric_series(candles: pd.DataFrame, column: str) -> pd.Series | None:
    if column not in candles.columns:
        return None
    return pd.to_numeric(candles[column], errors="raise")


def _series_optional_float(values: pd.Series | None, position: int) -> float | None:
    if values is None:
        return None
    return _optional_float(values.iloc[position])


def _empty_displacement_candle_frame() -> pd.DataFrame:
    return pd.DataFrame(columns=DISPLACEMENT_CANDLE_OUTPUT_COLUMNS)


def _optional_float(value: Any) -> float | None:
    if pd.isna(value):
        return None
    return float(value)
