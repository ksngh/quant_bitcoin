"""CSV-backed candle data provider.

This module is intentionally limited to market-data responsibilities: reading
local candle CSV files, normalizing them to the standard candle schema, and
returning rows sorted by candle open timestamp.
"""

from __future__ import annotations

from pathlib import Path
from typing import Mapping

import pandas as pd

STANDARD_CANDLE_COLUMNS: tuple[str, ...] = (
    "timestamp",
    "open",
    "high",
    "low",
    "close",
    "volume",
)

NUMERIC_CANDLE_COLUMNS: tuple[str, ...] = (
    "open",
    "high",
    "low",
    "close",
    "volume",
)


class CsvCandleDataProvider:
    """Load local candle data from a CSV file.

    The provider returns only the standard candle schema documented in
    ``docs/04_DATA_CONTRACT.md``. CSV headers are normalized by stripping
    surrounding whitespace and converting to lowercase before validation.
    """

    def __init__(self, csv_path: str | Path) -> None:
        self.csv_path = Path(csv_path)

    def load(self) -> pd.DataFrame:
        """Return normalized candle data sorted by timestamp ascending.

        Raises:
            FileNotFoundError: If the configured CSV file does not exist.
            ValueError: If required columns are missing or values cannot be
                normalized to the candle data contract.
        """

        raw_candles = pd.read_csv(self.csv_path)
        candles = self._normalize_columns(raw_candles)
        self._validate_required_columns(candles)

        normalized = candles.loc[:, STANDARD_CANDLE_COLUMNS].copy()
        normalized["timestamp"] = self._parse_timestamps(normalized["timestamp"])
        for column in NUMERIC_CANDLE_COLUMNS:
            normalized[column] = self._parse_numeric(normalized[column], column)

        return normalized.sort_values("timestamp", kind="mergesort").reset_index(drop=True)

    @staticmethod
    def _normalize_columns(candles: pd.DataFrame) -> pd.DataFrame:
        rename_map: Mapping[object, str] = {
            column: str(column).strip().lower() for column in candles.columns
        }
        return candles.rename(columns=rename_map)

    @staticmethod
    def _validate_required_columns(candles: pd.DataFrame) -> None:
        missing_columns = [
            column for column in STANDARD_CANDLE_COLUMNS if column not in candles.columns
        ]
        if missing_columns:
            missing = ", ".join(missing_columns)
            raise ValueError(f"CSV candle data is missing required columns: {missing}")

    @staticmethod
    def _parse_timestamps(timestamp: pd.Series) -> pd.Series:
        try:
            return pd.to_datetime(timestamp, errors="raise")
        except (TypeError, ValueError) as error:
            raise ValueError("CSV candle data contains invalid timestamp values") from error

    @staticmethod
    def _parse_numeric(values: pd.Series, column: str) -> pd.Series:
        try:
            return pd.to_numeric(values, errors="raise")
        except (TypeError, ValueError) as error:
            raise ValueError(
                f"CSV candle data contains non-numeric values in column: {column}"
            ) from error
