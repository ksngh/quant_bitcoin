"""Pattern strategy backtest integration.

This module wires completed candle data, existing pattern detection, existing
risk/exit planning, and the Task 054 exit simulator into a pure historical
backtest workflow. It does not fetch market data, read secrets, call exchange
APIs, place paper or real orders, or persist records.

First-batch assumptions:
- Fair Value Gap is the only configured pattern supported by default because it
  already has a detector and a risk/exit planner that operate on the shared
  pattern contracts.
- Completed candles are evaluated in ascending timestamp order using rolling
  prefixes; only events confirmed on the current candle are eligible, so pattern
  detection never uses candles after the event confirmation candle.
- A simulated entry happens at the plan entry reference on the pattern
  confirmation candle, and exit evaluation starts on the next completed candle.
- Only one simulated position is open at a time. If multiple eligible events are
  confirmed on the same candle, the deterministic sort order is pattern type,
  direction, then event id; the first valid plan is entered and the rest are not
  entered during that open position.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Literal

import pandas as pd

from quant_bitcoin.backtesting.basic import NUMERIC_CANDLE_COLUMNS, STANDARD_CANDLE_COLUMNS
from quant_bitcoin.patterns import (
    FairValueGapConfig,
    FairValueGapRiskExitConfig,
    PatternEvent,
    PatternExitReason,
    PatternExitSimulationResult,
    RiskExitDirection,
    RiskExitPlan,
    RiskExitPlanStatus,
    SoftInvalidationRule,
    create_fair_value_gap_risk_exit_plan,
    detect_fair_value_gaps,
    simulate_pattern_exit,
)

PatternName = Literal["FAIR_VALUE_GAP"]


@dataclass(frozen=True)
class PatternStrategyBacktestConfig:
    """Configuration for the first pattern strategy backtest workflow."""

    patterns: tuple[PatternName, ...] = ("FAIR_VALUE_GAP",)
    symbol: str | None = None
    timeframe: str | None = None
    fair_value_gap: FairValueGapConfig = field(default_factory=FairValueGapConfig)
    fair_value_gap_risk_exit: FairValueGapRiskExitConfig = field(
        default_factory=FairValueGapRiskExitConfig
    )

    def __post_init__(self) -> None:
        unsupported = [pattern for pattern in self.patterns if pattern != "FAIR_VALUE_GAP"]
        if unsupported:
            raise ValueError(f"unsupported configured patterns: {', '.join(unsupported)}")


@dataclass(frozen=True)
class PatternStrategyBacktestTrade:
    """One simulated pattern entry and its exit-analysis outcome."""

    event_id: str
    pattern_type: str
    pattern_direction: str
    pattern_status: str
    pattern_timestamp: Any
    entry_timestamp: Any
    entry_candle_index: int
    entry_price: float
    risk_plan: RiskExitPlan
    exit_reason: PatternExitReason
    exit_timestamp: Any | None
    exit_candle_index: int | None
    exit_price: float | None
    realized_pnl_per_unit: float
    realized_r_multiple: float | None
    remaining_quantity_ratio: float
    exit_simulation: PatternExitSimulationResult
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class PatternStrategyBacktestResult:
    """Result returned by the pattern strategy backtest workflow."""

    trades: tuple[PatternStrategyBacktestTrade, ...]
    evaluated_candle_count: int
    seen_event_ids: tuple[str, ...]

    @property
    def trade_count(self) -> int:
        """Return the number of simulated pattern entries."""

        return len(self.trades)


def run_pattern_strategy_backtest(
    candles: pd.DataFrame | Iterable[dict[str, Any]],
    *,
    config: PatternStrategyBacktestConfig | None = None,
) -> PatternStrategyBacktestResult:
    """Run a pure historical pattern strategy backtest over completed candles.

    The workflow normalizes a defensive copy of standard candle data, evaluates
    rolling completed-candle prefixes, detects only configured first-batch
    patterns, creates valid risk/exit plans, and delegates all exit decisions to
    ``simulate_pattern_exit``. Caller-provided candle data is not mutated.
    """

    backtest_config = config or PatternStrategyBacktestConfig()
    frame = _normalize_standard_candles(candles)
    if frame.empty or not backtest_config.patterns:
        return PatternStrategyBacktestResult((), len(frame), ())

    trades: list[PatternStrategyBacktestTrade] = []
    seen_event_ids: set[str] = set()
    row_index = 0

    while row_index < len(frame):
        prefix = frame.iloc[: row_index + 1].copy(deep=True)
        current_events = _detect_current_events(prefix, row_index, backtest_config)
        current_events = [event for event in current_events if event.event_id not in seen_event_ids]
        current_events.sort(key=_event_sort_key)

        entered_trade: PatternStrategyBacktestTrade | None = None
        for event in current_events:
            seen_event_ids.add(event.event_id)
            planned = _plan_event(event, backtest_config)
            if planned is None or planned.status != RiskExitPlanStatus.VALID:
                continue

            future_candles = frame.iloc[row_index + 1 :].copy(deep=True)
            exit_simulation = simulate_pattern_exit(
                planned,
                future_candles,
                soft_invalidation=_soft_invalidation_for_event(event, planned),
            )
            entered_trade = _build_trade(
                event=event,
                entry_candle=frame.iloc[row_index],
                entry_candle_index=row_index,
                risk_plan=planned,
                exit_simulation=exit_simulation,
            )
            trades.append(entered_trade)
            break

        if entered_trade is None:
            row_index += 1
            continue

        if entered_trade.exit_candle_index is None:
            break
        row_index = entered_trade.exit_candle_index + 1

    return PatternStrategyBacktestResult(
        trades=tuple(trades),
        evaluated_candle_count=len(frame),
        seen_event_ids=tuple(sorted(seen_event_ids)),
    )


def _normalize_standard_candles(candles: pd.DataFrame | Iterable[dict[str, Any]]) -> pd.DataFrame:
    frame = candles.copy(deep=True) if isinstance(candles, pd.DataFrame) else pd.DataFrame(list(candles))
    missing = [column for column in STANDARD_CANDLE_COLUMNS if column not in frame.columns]
    if missing:
        raise ValueError(f"missing required candle columns: {', '.join(missing)}")

    normalized = frame.loc[:, STANDARD_CANDLE_COLUMNS].copy(deep=True)
    normalized["timestamp"] = pd.to_datetime(normalized["timestamp"], errors="raise")
    if not normalized.empty and not normalized["timestamp"].is_monotonic_increasing:
        raise ValueError("candles must be sorted ascending by timestamp")

    for column in NUMERIC_CANDLE_COLUMNS:
        normalized[column] = pd.to_numeric(normalized[column], errors="raise")
        if normalized[column].isna().any():
            raise ValueError(f"candle column contains missing values: {column}")
    if (normalized["high"] < normalized["low"]).any():
        raise ValueError("candle high must be greater than or equal to low")
    if (normalized["volume"] < 0).any():
        raise ValueError("candle volume must be non-negative")
    return normalized.reset_index(drop=True)


def _detect_current_events(
    prefix: pd.DataFrame,
    row_index: int,
    config: PatternStrategyBacktestConfig,
) -> list[PatternEvent]:
    events: list[PatternEvent] = []
    if "FAIR_VALUE_GAP" in config.patterns:
        events.extend(
            detect_fair_value_gaps(
                prefix,
                symbol=config.symbol,
                timeframe=config.timeframe,
                config=config.fair_value_gap,
            )
        )
    return [event for event in events if event.end_index == row_index]


def _event_sort_key(event: PatternEvent) -> tuple[str, str, str]:
    return (event.pattern_type, event.direction, event.event_id)


def _plan_event(
    event: PatternEvent,
    config: PatternStrategyBacktestConfig,
) -> RiskExitPlan | None:
    if event.pattern_status != "VALID" or event.pattern_type != "FAIR_VALUE_GAP":
        return None
    return create_fair_value_gap_risk_exit_plan(
        event,
        config=config.fair_value_gap_risk_exit,
    ).risk_plan


def _soft_invalidation_for_event(
    event: PatternEvent,
    plan: RiskExitPlan,
) -> SoftInvalidationRule | None:
    if event.pattern_type != "FAIR_VALUE_GAP":
        return None
    direction = _coerce_direction(plan.direction)
    operator = "<=" if direction == RiskExitDirection.LONG else ">="
    return SoftInvalidationRule(
        invalidates_when=f"close {operator} fvg_midpoint",
        reference_price=float(event.zone_mid),
    )


def _build_trade(
    *,
    event: PatternEvent,
    entry_candle: pd.Series,
    entry_candle_index: int,
    risk_plan: RiskExitPlan,
    exit_simulation: PatternExitSimulationResult,
) -> PatternStrategyBacktestTrade:
    final_event = exit_simulation.events[-1] if exit_simulation.events else None
    exit_candle_index = None
    if final_event is not None:
        exit_candle_index = entry_candle_index + 1 + final_event.candle_index
    realized_pnl = _realized_pnl_per_unit(risk_plan, exit_simulation)
    realized_r = None
    if risk_plan.risk_per_unit is not None and risk_plan.risk_per_unit > 0:
        realized_r = realized_pnl / risk_plan.risk_per_unit

    return PatternStrategyBacktestTrade(
        event_id=event.event_id,
        pattern_type=event.pattern_type,
        pattern_direction=event.direction,
        pattern_status=event.pattern_status,
        pattern_timestamp=event.timestamp,
        entry_timestamp=entry_candle["timestamp"],
        entry_candle_index=entry_candle_index,
        entry_price=float(risk_plan.entry_price),
        risk_plan=risk_plan,
        exit_reason=exit_simulation.final_reason,
        exit_timestamp=final_event.timestamp if final_event is not None else None,
        exit_candle_index=exit_candle_index,
        exit_price=exit_simulation.final_price,
        realized_pnl_per_unit=realized_pnl,
        realized_r_multiple=realized_r,
        remaining_quantity_ratio=exit_simulation.remaining_quantity_ratio,
        exit_simulation=exit_simulation,
        metadata={
            "same_candle_entry_rule": "pattern_type_direction_event_id_order_first_valid_plan",
            "exit_evaluation": "starts_on_candle_after_entry",
        },
    )


def _realized_pnl_per_unit(
    plan: RiskExitPlan,
    exit_simulation: PatternExitSimulationResult,
) -> float:
    if plan.entry_price is None:
        return 0.0
    direction = _coerce_direction(plan.direction)
    total = 0.0
    for event in exit_simulation.events:
        if direction == RiskExitDirection.LONG:
            total += (event.price - plan.entry_price) * event.quantity_ratio
        else:
            total += (plan.entry_price - event.price) * event.quantity_ratio
    return total


def _coerce_direction(direction: RiskExitDirection | str) -> RiskExitDirection:
    if isinstance(direction, RiskExitDirection):
        return direction
    return RiskExitDirection(str(direction).upper())
