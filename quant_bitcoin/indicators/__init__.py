"""Technical indicator calculations."""

from quant_bitcoin.indicators.atr import (
    ATR_OUTPUT_COLUMNS,
    AtrConfig,
    AtrSmoothingMethod,
    VolatilityStatus,
    calculate_atr,
    calculate_atr_snapshot,
    calculate_true_range,
    classify_volatility,
)

from quant_bitcoin.indicators.pivots import (
    PivotConfig,
    PivotType,
    detect_pivots,
    remove_close_duplicate_pivots,
)

from quant_bitcoin.indicators.volume_ratio import (
    REQUIRED_VOLUME_RATIO_COLUMNS,
    VOLUME_RATIO_OUTPUT_COLUMNS,
    VolumeAverageMethod,
    VolumeRatioConfig,
    VolumeStatus,
    calculate_volume_ratio,
    calculate_volume_ratio_snapshot,
    classify_volume_status,
)

from quant_bitcoin.indicators.swing_structure import (
    MarketStructureStatus,
    SwingLabel,
    SwingStructureConfig,
    classify_high,
    classify_low,
    classify_market_status,
    classify_swing_structure,
)

__all__ = [
    "ATR_OUTPUT_COLUMNS",
    "AtrConfig",
    "AtrSmoothingMethod",
    "VolatilityStatus",
    "calculate_atr",
    "calculate_atr_snapshot",
    "calculate_true_range",
    "classify_volatility",
    "PivotConfig",
    "PivotType",
    "detect_pivots",
    "remove_close_duplicate_pivots",
    "REQUIRED_VOLUME_RATIO_COLUMNS",
    "VOLUME_RATIO_OUTPUT_COLUMNS",
    "VolumeAverageMethod",
    "VolumeRatioConfig",
    "VolumeStatus",
    "calculate_volume_ratio",
    "calculate_volume_ratio_snapshot",
    "classify_volume_status",
    "classify_swing_structure",
    "classify_market_status",
    "classify_low",
    "classify_high",
    "SwingStructureConfig",
    "SwingLabel",
    "MarketStructureStatus",
]
