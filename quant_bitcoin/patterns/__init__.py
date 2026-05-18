"""Pattern detection engine exports."""

from quant_bitcoin.patterns.risk_exit import (
    BreakEvenSettings,
    PartialExitSettings,
    RiskExitConfig,
    RiskExitDirection,
    RiskExitPlan,
    RiskExitPlanStatus,
    RiskExitTarget,
    RiskExitTargetSource,
    TimeStopSettings,
    TrailingStopSettings,
    calculate_r_multiple_targets,
    combine_targets,
    create_risk_exit_plan,
)
from quant_bitcoin.patterns.trendline_break_risk_exit import (
    TrendlineBreakRiskExitConfig,
    TrendlineBreakRiskExitPlan,
    TrendlineBreakSoftInvalidation,
    create_trendline_break_risk_exit_plan,
)

from quant_bitcoin.patterns.order_block import (
    OrderBlockConfig,
    OrderBlockDirection,
    OrderBlockEvent,
    OrderBlockState,
    OrderBlockStatus,
    OrderBlockZoneDefinition,
    detect_order_blocks,
)

from quant_bitcoin.patterns.trendline_break import (
    TrendlineBreakConfig,
    TrendlineBreakDirection,
    TrendlineBreakEvent,
    TrendlineBreakStatus,
    TrendlineType,
    detect_trendline_breaks,
)

from quant_bitcoin.patterns.adam_and_eve import (
    AdamAndEveConfig,
    AdamAndEveDirection,
    AdamAndEveEvent,
    AdamAndEveStatus,
    detect_adam_and_eve_patterns,
)

from quant_bitcoin.patterns.diamond import (
    DiamondConfig,
    DiamondDirection,
    DiamondEvent,
    DiamondStatus,
    detect_diamond_patterns,
)

from quant_bitcoin.patterns.cup_and_handle import (
    CupAndHandleConfig,
    CupAndHandleDirection,
    CupAndHandleEvent,
    CupAndHandleStatus,
    detect_cup_and_handle_patterns,
)

from quant_bitcoin.patterns.fair_value_gap import (
    FairValueGapConfig,
    FairValueGapState,
    PatternDirection,
    PatternEvent,
    PatternStatus,
    PatternType,
    detect_fair_value_gaps,
    detect_patterns,
    filter_new_events,
)

__all__ = [
    "create_trendline_break_risk_exit_plan",
    "TrendlineBreakSoftInvalidation",
    "TrendlineBreakRiskExitPlan",
    "TrendlineBreakRiskExitConfig",
    "create_risk_exit_plan",
    "combine_targets",
    "calculate_r_multiple_targets",
    "TrailingStopSettings",
    "TimeStopSettings",
    "RiskExitTargetSource",
    "RiskExitTarget",
    "RiskExitPlanStatus",
    "RiskExitPlan",
    "RiskExitDirection",
    "RiskExitConfig",
    "PartialExitSettings",
    "BreakEvenSettings",
    "FairValueGapConfig",
    "FairValueGapState",
    "PatternDirection",
    "PatternEvent",
    "PatternStatus",
    "PatternType",
    "detect_fair_value_gaps",
    "detect_patterns",
    "filter_new_events",
    "TrendlineBreakConfig",
    "TrendlineBreakDirection",
    "TrendlineBreakEvent",
    "TrendlineBreakStatus",
    "TrendlineType",
    "detect_trendline_breaks",
    "AdamAndEveConfig",
    "AdamAndEveDirection",
    "AdamAndEveEvent",
    "AdamAndEveStatus",
    "detect_adam_and_eve_patterns",
    "DiamondConfig",
    "DiamondDirection",
    "DiamondEvent",
    "DiamondStatus",
    "detect_diamond_patterns",
    "CupAndHandleConfig",
    "CupAndHandleDirection",
    "CupAndHandleEvent",
    "CupAndHandleStatus",
    "detect_cup_and_handle_patterns",
    "OrderBlockConfig",
    "OrderBlockDirection",
    "OrderBlockEvent",
    "OrderBlockState",
    "OrderBlockStatus",
    "OrderBlockZoneDefinition",
    "detect_order_blocks",
]
