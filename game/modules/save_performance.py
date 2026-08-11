"""SYS-SAVE save/load performance protocol."""

from .persist_performance import PerformanceReport, evaluate_performance


def evaluate_save_latency(samples_ms: tuple[float, ...], *, approved_threshold: bool = True) -> PerformanceReport:
    return evaluate_performance(samples_ms, percentile=0.95, percentile_budget_ms=500.0, maximum_budget_ms=1000.0, approved_threshold=approved_threshold)
