"""Volume Ratio indicator calculation.

This module consumes already-provided candle volume data and emits deterministic
relative-volume rows. It does not fetch market data, read secrets, call exchange
APIs, place orders, or make trading decisions.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from statistics import median
from typing import Any

import pandas as pd

REQUIRED_VOLUME_RATIO_COLUMNS: tuple[str, ...] = (
    "symbol",
    "timestamp",
    "volume",
)

VOLUME_RATIO_OUTPUT_COLUMNS: tuple[str, ...] = (
    "symbol",
    "timestamp",
    "volume",
    "average_volume",
    "volume_ratio",
    "minimum_volume_ratio_for_confirmation",
    "volume_confirmation",
    "volume_status",
    "is_valid",
)


class VolumeStatus(Enum):
    """Volume-ratio classifications."""

    HIGH = "HIGH"
    INCREASED = "INCREASED"
    NORMAL = "NORMAL"
    LOW = "LOW"
    INVALID = "INVALID"


class VolumeAverageMethod(Enum):
    """Supported volume baseline methods."""

    MEAN = "MEAN"
    MEDIAN = "MEDIAN"


@dataclass(frozen=True)
class VolumeRatioConfig:
    """Configuration for deterministic Volume Ratio calculation."""

    window: int = 20
    minimum_volume_ratio_for_confirmation: float = 1.5
    high_volume_ratio_threshold: float = 2.0
    low_volume_ratio_threshold: float = 0.5
    require_full_window: bool = True
    reject_zero_average_volume: bool = True
    average_method: VolumeAverageMethod | str = VolumeAverageMethod.MEAN

    def __post_init__(self) -> None:
        if self.window < 1:
            raise ValueError("window must be at least 1")
        if self.minimum_volume_ratio_for_confirmation < 0:
            raise ValueError(
                "minimum_volume_ratio_for_confirmation must be non-negative"
            )
        if self.high_volume_ratio_threshold < 0:
            raise ValueError("high_volume_ratio_threshold must be non-negative")
        if self.low_volume_ratio_threshold < 0:
            raise ValueError("low_volume_ratio_threshold must be non-negative")
        if (
            self.low_volume_ratio_threshold
            > self.minimum_volume_ratio_for_confirmation
        ):
            raise ValueError(
                "low_volume_ratio_threshold must be less than or equal to "
                "minimum_volume_ratio_for_confirmation"
            )
        if (
            self.minimum_volume_ratio_for_confirmation
            > self.high_volume_ratio_threshold
        ):
            raise ValueError(
                "minimum_volume_ratio_for_confirmation must be less than or "
                "equal to high_volume_ratio_threshold"
            )
        _coerce_average_method(self.average_method)


def calculate_volume_ratio(
    candles: pd.DataFrame, config: VolumeRatioConfig | None = None
) -> pd.DataFrame:
    """Return Volume Ratio rows for already-provided candle volume data.

    The returned frame has one row per input candle and includes current volume,
    the rolling baseline average volume, volume ratio, confirmation flag,
    status, and validity. With the default ``require_full_window`` setting, rows
    before the configured warm-up window are returned as invalid rows with
    ``volume_status`` set to ``INVALID``.

    The rolling baseline includes the current candle, matching the owner-provided
    mechanical definition and pseudocode for the latest snapshot.

    Args:
        candles: Candle data containing symbol, timestamp, and volume columns.
        config: Volume Ratio calculation configuration. Defaults to
            ``VolumeRatioConfig()``.

    Raises:
        ValueError: If required columns are missing, numeric values are
            non-numeric, or configuration values are invalid.
    """

    volume_config = config or VolumeRatioConfig()
    _validate_candles(candles)

    if candles.empty:
        return _empty_volume_ratio_frame()

    volume = pd.to_numeric(candles["volume"], errors="raise")
    rows: list[dict[str, Any]] = []

    for position, (_, candle) in enumerate(candles.iterrows()):
        current_volume = _optional_float(volume.iloc[position])
        start_position = max(0, position + 1 - volume_config.window)
        window_values = [
            _optional_float(value) for value in volume.iloc[start_position : position + 1]
        ]
        has_full_window = len(window_values) == volume_config.window

        if (
            current_volume is None
            or any(value is None for value in window_values)
            or any(value is not None and value < 0 for value in window_values)
            or (volume_config.require_full_window and not has_full_window)
        ):
            rows.append(_invalid_row(candle, current_volume, volume_config))
            continue

        numeric_window_values = [value for value in window_values if value is not None]
        average_volume = _calculate_average_volume(
            numeric_window_values,
            _coerce_average_method(volume_config.average_method),
        )

        if average_volume == 0:
            rows.append(_invalid_row(candle, current_volume, volume_config))
            continue

        volume_ratio = current_volume / average_volume
        volume_confirmation = (
            volume_ratio >= volume_config.minimum_volume_ratio_for_confirmation
        )
        volume_status = classify_volume_status(volume_ratio, volume_config)

        rows.append(
            {
                "symbol": candle["symbol"],
                "timestamp": candle["timestamp"],
                "volume": current_volume,
                "average_volume": average_volume,
                "volume_ratio": volume_ratio,
                "minimum_volume_ratio_for_confirmation": (
                    volume_config.minimum_volume_ratio_for_confirmation
                ),
                "volume_confirmation": bool(volume_confirmation),
                "volume_status": volume_status,
                "is_valid": True,
            }
        )

    return pd.DataFrame(rows, columns=VOLUME_RATIO_OUTPUT_COLUMNS)


def classify_volume_status(
    volume_ratio: float | None,
    config: VolumeRatioConfig | None = None,
) -> str:
    """Classify a volume ratio into HIGH, INCREASED, NORMAL, LOW, or INVALID."""

    volume_config = config or VolumeRatioConfig()
    if volume_ratio is None:
        return VolumeStatus.INVALID.value
    if volume_ratio >= volume_config.high_volume_ratio_threshold:
        return VolumeStatus.HIGH.value
    if volume_ratio >= volume_config.minimum_volume_ratio_for_confirmation:
        return VolumeStatus.INCREASED.value
    if volume_ratio <= volume_config.low_volume_ratio_threshold:
        return VolumeStatus.LOW.value
    return VolumeStatus.NORMAL.value


def calculate_volume_ratio_snapshot(
    candles: pd.DataFrame, config: VolumeRatioConfig | None = None
) -> dict[str, Any]:
    """Return the latest Volume Ratio output row as a dictionary."""

    volume_ratio_rows = calculate_volume_ratio(candles, config)
    if volume_ratio_rows.empty:
        return {column: None for column in VOLUME_RATIO_OUTPUT_COLUMNS}
    return volume_ratio_rows.iloc[-1].to_dict()


def _validate_candles(candles: pd.DataFrame) -> None:
    missing_columns = [
        column for column in REQUIRED_VOLUME_RATIO_COLUMNS if column not in candles.columns
    ]
    if missing_columns:
        joined = ", ".join(missing_columns)
        raise ValueError(f"missing required Volume Ratio columns: {joined}")


def _calculate_average_volume(
    values: list[float], average_method: VolumeAverageMethod
) -> float:
    if average_method == VolumeAverageMethod.MEDIAN:
        return float(median(values))
    return float(sum(values) / len(values))


def _invalid_row(
    candle: pd.Series, current_volume: float | None, config: VolumeRatioConfig
) -> dict[str, Any]:
    return {
        "symbol": candle["symbol"],
        "timestamp": candle["timestamp"],
        "volume": current_volume,
        "average_volume": None,
        "volume_ratio": None,
        "minimum_volume_ratio_for_confirmation": (
            config.minimum_volume_ratio_for_confirmation
        ),
        "volume_confirmation": False,
        "volume_status": VolumeStatus.INVALID.value,
        "is_valid": False,
    }


def _empty_volume_ratio_frame() -> pd.DataFrame:
    return pd.DataFrame(columns=VOLUME_RATIO_OUTPUT_COLUMNS)


def _optional_float(value: Any) -> float | None:
    if pd.isna(value):
        return None
    return float(value)


def _coerce_average_method(
    average_method: VolumeAverageMethod | str,
) -> VolumeAverageMethod:
    if isinstance(average_method, VolumeAverageMethod):
        return average_method
    try:
        return VolumeAverageMethod(str(average_method).upper())
    except ValueError as exc:
        allowed = ", ".join(method.value for method in VolumeAverageMethod)
        raise ValueError(f"average_method must be one of: {allowed}") from exc
