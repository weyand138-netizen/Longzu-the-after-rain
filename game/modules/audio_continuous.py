"""Pure continuous-layer transition plans. Mutable ownership stays in Ren'Py session."""
from dataclasses import dataclass, replace
from pathlib import PurePosixPath


LAYERS = ("music", "ambience")


@dataclass(frozen=True)
class ContinuousCue:
    cue_id: str
    layer: str
    filename: str | None
    fade_seconds: float = 0.8

    def __post_init__(self):
        if not isinstance(self.cue_id, str) or not self.cue_id.strip() or self.layer not in LAYERS:
            raise ValueError("Invalid continuous cue identity")
        if type(self.fade_seconds) not in (int, float) or not 0 <= self.fade_seconds <= 10:
            raise ValueError("Invalid transition duration")
        if self.filename is not None:
            p = PurePosixPath(self.filename)
            if (not self.filename or p.is_absolute() or ".." in p.parts or
                    any(c in self.filename for c in "\\:<>\x00")):
                raise ValueError("Cue must use a relative asset path without playback modifiers")


@dataclass(frozen=True)
class ContinuousLayer:
    target: ContinuousCue | None = None
    generation: int = 0
    active: int | None = None
    retiring: int | None = None
    status: str = "NO_CONTEXT"


@dataclass(frozen=True)
class AudioCommand:
    operation: str
    slot: int
    filename: str | None = None
    fade_seconds: float = 0.0


def request_continuous(state, cue):
    """Return the next immutable state and stop-before-play command sequence."""
    if not isinstance(state, ContinuousLayer) or not isinstance(cue, ContinuousCue):
        raise ValueError("Invalid layer request")
    if state.target is not None and state.target.layer != cue.layer:
        raise ValueError("Cross-layer target")
    if state.target == cue and state.status in ("CONTEXT_ACTIVE", "INTENTIONAL_SILENCE"):
        return state, ()
    generation = state.generation + 1
    if cue.filename is None:
        commands = tuple(AudioCommand("stop", slot) for slot in (0, 1))
        return ContinuousLayer(cue, generation, status="INTENTIONAL_SILENCE"), commands
    incoming = 0 if state.active is None else 1-state.active
    commands = [AudioCommand("stop", incoming)]
    if state.active is not None:
        commands.append(AudioCommand("stop", state.active, fade_seconds=cue.fade_seconds))
    commands.append(AudioCommand("play", incoming, cue.filename, cue.fade_seconds))
    return ContinuousLayer(cue, generation, incoming, state.active, "CONTEXT_ACTIVE"), tuple(commands)


def fault_continuous(state):
    """Retain only the requested identity, never a fictitious playing slot."""
    return replace(state, active=None, retiring=None, status="FAULT_SILENT")


def finish_continuous(state, generation):
    """A stale completion must never affect the replacement target."""
    if generation != state.generation or state.retiring is None:
        return state, ()
    return replace(state, retiring=None), (AudioCommand("stop", state.retiring),)
