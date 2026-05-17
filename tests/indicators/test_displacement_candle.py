import pandas as pd
import pytest

from quant_bitcoin.indicators.displacement_candle import (
    DISPLACEMENT_CANDLE_OUTPUT_COLUMNS,
    DisplacementCandleConfig,
    DisplacementDirection,
    DisplacementStatus,
    calculate_displacement_candle_snapshot,
    detect_displacement_candle,
    detect_displacement_candles,
    invalid_displacement_result,
)


def _candles(rows: list[dict]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "symbol": row.get("symbol", "BTCUSDT"),
                "timestamp": row.get("timestamp", f"2026-05-16T0{i}:00:00Z"),
                "open": row.get("open", 64000.0),
                "high": row.get("high", 65300.0),
                "low": row.get("low", 63800.0),
                "close": row.get("close", 65250.0),
                "volume": row.get("volume", 100.0),
                "atr": row.get("atr", 800.0),
                "volume_ratio": row.get("volume_ratio", 1.8),
            }
            for i, row in enumerate(rows)
        ]
    )


def test_detects_bullish_displacement_from_owner_default_rules() -> None:
    result = detect_displacement_candles(_candles([{}])).iloc[0]

    assert result["symbol"] == "BTCUSDT"
    assert result["timestamp"] == "2026-05-16T00:00:00Z"
    assert result["candle_range"] == pytest.approx(1500.0)
    assert result["body_size"] == pytest.approx(1250.0)
    assert result["upper_wick"] == pytest.approx(50.0)
    assert result["lower_wick"] == pytest.approx(200.0)
    assert result["body_ratio"] == pytest.approx(1250.0 / 1500.0)
    assert result["close_position_ratio"] == pytest.approx(1450.0 / 1500.0)
    assert result["atr"] == pytest.approx(800.0)
    assert result["volume_ratio"] == pytest.approx(1.8)
    assert result["displacement_direction"] == DisplacementDirection.BULLISH.value
    assert result["displacement_status"] == DisplacementStatus.VALID.value
    assert result["is_displacement"] == True
    assert result["is_valid"] == True
    assert result["reason"] is None


def test_detects_bearish_displacement_with_symmetric_rules() -> None:
    candles = _candles(
        [
            {
                "open": 65250.0,
                "high": 65400.0,
                "low": 63800.0,
                "close": 63900.0,
                "atr": 900.0,
                "volume_ratio": 2.0,
            }
        ]
    )

    result = detect_displacement_candles(candles).iloc[0]

    assert result["candle_range"] == pytest.approx(1600.0)
    assert result["body_size"] == pytest.approx(1350.0)
    assert result["upper_wick"] == pytest.approx(150.0)
    assert result["lower_wick"] == pytest.approx(100.0)
    assert result["close_position_ratio"] == pytest.approx(1500.0 / 1600.0)
    assert result["displacement_direction"] == DisplacementDirection.BEARISH.value
    assert result["displacement_status"] == DisplacementStatus.VALID.value
    assert result["is_displacement"] == True
    assert result["is_valid"] == True


def test_returns_none_for_ordinary_candles_and_records_first_failed_threshold() -> None:
    candles = _candles(
        [
            {
                "open": 64000.0,
                "high": 65300.0,
                "low": 63800.0,
                "close": 64500.0,
                "atr": 800.0,
                "volume_ratio": 1.8,
            }
        ]
    )

    result = detect_displacement_candles(candles).iloc[0]

    assert result["body_ratio"] == pytest.approx(500.0 / 1500.0)
    assert result["displacement_direction"] == DisplacementDirection.NONE.value
    assert result["displacement_status"] == DisplacementStatus.NONE.value
    assert result["is_displacement"] == False
    assert result["is_valid"] == True
    assert result["reason"] == "body_ratio_below_threshold"


def test_threshold_equality_counts_as_valid_displacement() -> None:
    candles = _candles(
        [
            {
                "open": 100.0,
                "high": 160.0,
                "low": 60.0,
                "close": 160.0,
                "atr": 100.0 / 1.5,
                "volume_ratio": 1.5,
            }
        ]
    )

    result = detect_displacement_candles(candles).iloc[0]

    assert result["body_ratio"] == pytest.approx(0.6)
    assert result["close_position_ratio"] == pytest.approx(1.0)
    assert result["displacement_status"] == DisplacementStatus.VALID.value
    assert result["is_displacement"] == True


def test_close_position_at_threshold_counts_as_valid() -> None:
    candles = _candles(
        [
            {
                "open": 100.0,
                "high": 130.0,
                "low": 30.0,
                "close": 100.0,
                "atr": 60.0,
                "volume_ratio": 1.5,
            }
        ]
    )

    result = detect_displacement_candles(candles).iloc[0]

    assert result["body_ratio"] == pytest.approx(0.0)
    assert result["displacement_status"] == DisplacementStatus.NONE.value

    edge = detect_displacement_candle(
        {
            "symbol": "BTCUSDT",
            "timestamp": "2026-05-16T01:00:00Z",
            "open": 40.0,
            "high": 110.0,
            "low": 10.0,
            "close": 80.0,
            "atr": 60.0,
            "volume_ratio": 1.5,
        },
        DisplacementCandleConfig(minimum_body_ratio=0.4),
    )
    assert edge["close_position_ratio"] == pytest.approx(0.7)
    assert edge["displacement_status"] == DisplacementStatus.VALID.value
    assert edge["is_displacement"] == True


def test_range_close_position_and_volume_below_threshold_return_none() -> None:
    too_small_range = detect_displacement_candles(
        _candles([{"atr": 1001.0, "volume_ratio": 1.8}])
    ).iloc[0]
    assert too_small_range["displacement_status"] == DisplacementStatus.NONE.value
    assert too_small_range["reason"] == "range_below_atr_threshold"

    poor_close = detect_displacement_candles(
        _candles(
            [
                {
                    "open": 63200.0,
                    "high": 66000.0,
                    "low": 63000.0,
                    "close": 65000.0,
                    "atr": 1000.0,
                    "volume_ratio": 1.8,
                }
            ]
        )
    ).iloc[0]
    assert poor_close["close_position_ratio"] == pytest.approx(2 / 3)
    assert poor_close["reason"] == "close_position_below_threshold"

    weak_volume = detect_displacement_candles(
        _candles([{"volume_ratio": 1.49}])
    ).iloc[0]
    assert weak_volume["displacement_status"] == DisplacementStatus.NONE.value
    assert weak_volume["reason"] == "volume_ratio_below_threshold"


def test_missing_atr_and_volume_ratio_are_invalid_only_when_filters_enabled() -> None:
    missing_atr = detect_displacement_candles(_candles([{"atr": None}])).iloc[0]
    assert missing_atr["displacement_status"] == DisplacementStatus.INVALID.value
    assert missing_atr["displacement_direction"] == DisplacementDirection.INVALID.value
    assert missing_atr["is_valid"] == False
    assert missing_atr["reason"] == "missing_atr"

    missing_volume_ratio = detect_displacement_candles(
        _candles([{"volume_ratio": None}])
    ).iloc[0]
    assert missing_volume_ratio["is_valid"] == False
    assert missing_volume_ratio["reason"] == "missing_volume_ratio"

    filters_disabled = detect_displacement_candles(
        _candles([{"atr": None, "volume_ratio": None}]),
        DisplacementCandleConfig(allow_atr_filter=False, allow_volume_filter=False),
    ).iloc[0]
    assert filters_disabled["displacement_status"] == DisplacementStatus.VALID.value
    assert filters_disabled["is_displacement"] == True
    assert filters_disabled["is_valid"] == True


def test_neutral_candle_is_valid_none_without_requiring_atr_or_volume_ratio() -> None:
    result = detect_displacement_candles(
        _candles(
            [
                {
                    "open": 64000.0,
                    "high": 65300.0,
                    "low": 63800.0,
                    "close": 64000.0,
                    "atr": None,
                    "volume_ratio": None,
                }
            ]
        )
    ).iloc[0]

    assert result["close_position_ratio"] is None
    assert result["displacement_direction"] == DisplacementDirection.NONE.value
    assert result["displacement_status"] == DisplacementStatus.NONE.value
    assert result["is_displacement"] == False
    assert result["is_valid"] == True


def test_invalid_ohlc_and_zero_range_edge_cases() -> None:
    missing_ohlc = detect_displacement_candles(_candles([{"open": None}])).iloc[0]
    assert missing_ohlc["reason"] == "missing_ohlc"
    assert missing_ohlc["displacement_status"] == DisplacementStatus.INVALID.value
    assert missing_ohlc["is_valid"] == False

    invalid_high_low = detect_displacement_candles(
        _candles([{"high": 100.0, "low": 101.0}])
    ).iloc[0]
    assert invalid_high_low["reason"] == "invalid_high_low"
    assert invalid_high_low["is_valid"] == False

    zero_range = detect_displacement_candles(
        _candles([{"open": 100.0, "high": 100.0, "low": 100.0, "close": 100.0}])
    ).iloc[0]
    assert zero_range["reason"] == "zero_range"
    assert zero_range["is_valid"] == False

    accepted_zero_range = detect_displacement_candles(
        _candles([{"open": 100.0, "high": 100.0, "low": 100.0, "close": 100.0}]),
        DisplacementCandleConfig(reject_zero_range_candle=False),
    ).iloc[0]
    assert accepted_zero_range["candle_range"] == pytest.approx(0.0)
    assert accepted_zero_range["body_ratio"] == pytest.approx(0.0)
    assert accepted_zero_range["displacement_status"] == DisplacementStatus.NONE.value
    assert accepted_zero_range["is_displacement"] == False
    assert accepted_zero_range["is_valid"] == True


def test_rejects_missing_required_columns_non_numeric_values_and_invalid_config() -> None:
    with pytest.raises(
        ValueError, match="missing required Displacement Candle columns: close"
    ):
        detect_displacement_candles(_candles([{}]).drop(columns=["close"]))

    with pytest.raises(ValueError):
        detect_displacement_candles(_candles([{"open": "not-a-number"}]))

    with pytest.raises(ValueError, match="minimum_body_ratio"):
        DisplacementCandleConfig(minimum_body_ratio=1.1)
    with pytest.raises(ValueError, match="minimum_range_atr_multiplier"):
        DisplacementCandleConfig(minimum_range_atr_multiplier=-0.1)
    with pytest.raises(ValueError, match="minimum_volume_ratio"):
        DisplacementCandleConfig(minimum_volume_ratio=-0.1)
    with pytest.raises(ValueError, match="minimum_close_position_ratio"):
        DisplacementCandleConfig(minimum_close_position_ratio=-0.1)


def test_returns_empty_frame_and_latest_snapshot_for_output_schema_consumers() -> None:
    empty = detect_displacement_candles(pd.DataFrame(columns=_candles([{}]).columns))
    assert empty.empty
    assert list(empty.columns) == list(DISPLACEMENT_CANDLE_OUTPUT_COLUMNS)

    snapshot = calculate_displacement_candle_snapshot(_candles([{}]))
    assert snapshot["symbol"] == "BTCUSDT"
    assert snapshot["displacement_direction"] == DisplacementDirection.BULLISH.value
    assert snapshot["displacement_status"] == DisplacementStatus.VALID.value
    assert snapshot["is_displacement"] == True
    assert snapshot["is_valid"] == True

    empty_snapshot = calculate_displacement_candle_snapshot(
        pd.DataFrame(columns=_candles([{}]).columns)
    )
    assert set(empty_snapshot) == set(DISPLACEMENT_CANDLE_OUTPUT_COLUMNS)
    assert all(value is None for value in empty_snapshot.values())


def test_invalid_result_helper_matches_invalid_schema_fields() -> None:
    result = invalid_displacement_result("missing_ohlc")

    assert result["reason"] == "missing_ohlc"
    assert result["displacement_direction"] == DisplacementDirection.INVALID.value
    assert result["displacement_status"] == DisplacementStatus.INVALID.value
    assert result["is_displacement"] == False
    assert result["is_valid"] == False
