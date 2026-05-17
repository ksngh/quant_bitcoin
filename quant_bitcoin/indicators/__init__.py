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
    "classify_swing_structure",
    "classify_market_status",
    "classify_low",
    "classify_high",
    "SwingStructureConfig",
    "SwingLabel",
    "MarketStructureStatus",
]
