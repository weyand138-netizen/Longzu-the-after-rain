"""Immutable four-slot authored-SFX decisions, without engine or mutable globals."""
from dataclasses import dataclass, replace
from pathlib import PurePosixPath

PRIORITIES = {"DECORATIVE": 0, "OPTIONAL_UI_NOTIFICATION": 1, "IMPORTANT_NARRATIVE": 2}


@dataclass(frozen=True)
class OneShotCue:
    cue_id: str
    filename: str
    priority: str

    def __post_init__(self):
        if not isinstance(self.cue_id, str) or not self.cue_id.strip() or self.priority not in PRIORITIES:
            raise ValueError("Invalid one-shot cue")
        if not isinstance(self.filename, str) or not self.filename:
            raise ValueError("Invalid one-shot asset")
        path = PurePosixPath(self.filename)
        if path.is_absolute() or ".." in path.parts or any(c in self.filename for c in "\\:<>\x00"):
            raise ValueError("Invalid one-shot asset")


@dataclass(frozen=True)
class OneShotVoice:
    occurrence: str
    priority: int
    sequence: int


@dataclass(frozen=True)
class OneShotPool:
    claimed: frozenset[str] = frozenset()
    voices: tuple = (None, None, None, None)
    sequence: int = 0


@dataclass(frozen=True)
class OneShotDecision:
    pool: OneShotPool
    disposition: str
    slot: int | None = None
    preempted: str | None = None


def claim_oneshot(pool, occurrence):
    # Notifications retain their existing sole claim owner; reject their namespace.
    prefix = "authored-sfx:v1:"
    if not isinstance(occurrence, str) or not occurrence.startswith(prefix) or len(occurrence) <= len(prefix):
        return pool, "INVALID"
    if occurrence in pool.claimed:
        return pool, "DUPLICATE_NOOP"
    return replace(pool, claimed=pool.claimed | {occurrence}), None


def reap_oneshots(pool, busy_slots):
    return replace(pool, voices=tuple(v if i in busy_slots else None for i, v in enumerate(pool.voices)))


def retire_oneshots(pool):
    return replace(pool, voices=(None, None, None, None))


def dispatch_claimed_oneshot(pool, cue, occurrence, eligible):
    if occurrence not in pool.claimed or not isinstance(cue, OneShotCue):
        raise ValueError("Dispatcher requires one previously claimed valid request")
    if not eligible:
        return OneShotDecision(pool, "SUPPRESSED_CONSUMED")
    voices = list(pool.voices)
    preempted = None
    if None in voices:
        slot = voices.index(None)
    else:
        slot = min(range(4), key=lambda i: (voices[i].priority, voices[i].sequence))
        if PRIORITIES[cue.priority] <= voices[slot].priority:
            return OneShotDecision(pool, "DROPPED_CONSUMED")
        preempted = voices[slot].occurrence
    voices[slot] = OneShotVoice(occurrence, PRIORITIES[cue.priority], pool.sequence)
    return OneShotDecision(replace(pool, voices=tuple(voices), sequence=pool.sequence+1), "PLAY", slot, preempted)
