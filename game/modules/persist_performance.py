"""Pure persistence benchmark protocol using nearest-rank percentiles."""

import math
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class PerformanceReport:
    """Deterministic benchmark result."""

    status: str
    percentile_ms: float | None
    maximum_ms: float | None
    sample_count: int


def nearest_rank_percentile(samples: Iterable[float], percentile: float) -> float:
    values = tuple(samples)
    if not values or type(percentile) not in (int, float) or not 0 < percentile <= 1:
        raise ValueError("percentile requires non-empty samples and (0,1] probability")
    if any(type(value) not in (int, float) or not math.isfinite(value) or value < 0 for value in values):
        raise ValueError("samples must be finite non-negative numbers")
    rank = max(1, math.ceil(percentile * len(values)))
    return sorted(values)[rank - 1]


def evaluate_performance(samples: Iterable[float], *, percentile: float, percentile_budget_ms: float, maximum_budget_ms: float, approved_threshold: bool = True) -> PerformanceReport:
    values = tuple(samples)
    if not approved_threshold:
        return PerformanceReport("REPORT_ONLY", None, max(values) if values else None, len(values))
    p = nearest_rank_percentile(values, percentile)
    maximum = max(values)
    status = "PASS" if p <= percentile_budget_ms and maximum <= maximum_budget_ms else "FAIL"
    return PerformanceReport(status, p, maximum, len(values))
