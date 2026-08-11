"""SYS-TEST runner identity, dependency closure, and cleanup scans."""

from dataclasses import dataclass
from typing import Iterable


TEST_ONLY_MARKERS = frozenset(("observer", "spy", "fault_injector", "protocol_bomb", "synthetic_save", "synthetic_root", "benchmark_harness", "evidence_forger"))


@dataclass(frozen=True)
class EnvironmentIdentity:
    engine: str
    version: str
    python_version: str
    renderer: str
    runner_hash: str


def environment_matches(observed: EnvironmentIdentity, approved: EnvironmentIdentity) -> bool:
    return observed == approved


def scan_dependency_closure(edges: Iterable[tuple[str, str]], *, production_prefix: str = "production/", test_only_prefix: str = "tests/") -> tuple[tuple[str, str], ...]:
    """Return production-to-test-only edges; a non-empty result blocks release."""

    return tuple(sorted((source, target) for source, target in edges if source.startswith(production_prefix) and target.startswith(test_only_prefix)))


def scan_test_only_markers(paths: Iterable[str]) -> tuple[str, ...]:
    return tuple(sorted(path for path in paths if any(marker in path.lower() for marker in TEST_ONLY_MARKERS)))


def cleanup_guard(cleanup: callable) -> bool:
    try:
        cleanup()
    except Exception:
        return False
    return True
