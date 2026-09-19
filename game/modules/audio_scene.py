"""Exact authored statement bindings; no inference from images or hidden state."""
from dataclasses import dataclass
import hashlib
from pathlib import PurePosixPath


@dataclass(frozen=True)
class AudioSceneAnchor:
    anchor_id: str
    source: str
    line: int
    source_sha256: str
    context_id: str
    oneshot_id: str | None = None

    def __post_init__(self):
        if any(not isinstance(v, str) or not v.strip() for v in (self.anchor_id, self.source, self.context_id)):
            raise ValueError("Missing anchor identity")
        p = PurePosixPath(self.source)
        if p.is_absolute() or ".." in p.parts or any(c in self.source for c in "\\:\x00") or p.suffix != ".rpy":
            raise ValueError("Invalid source path")
        if type(self.line) is not int or self.line < 1:
            raise ValueError("Invalid line")
        if len(self.source_sha256) != 64 or any(c not in "0123456789abcdef" for c in self.source_sha256):
            raise ValueError("Invalid source digest")
        if self.oneshot_id is not None and (not isinstance(self.oneshot_id, str) or not self.oneshot_id.strip()):
            raise ValueError("Invalid one-shot identity")


def compile_scene_anchors(anchors, read_source):
    """Reject the whole catalogue on ambiguity or stale source; never retarget it."""
    result, ids, sources = {}, set(), {}
    for anchor in anchors:
        if not isinstance(anchor, AudioSceneAnchor):
            raise ValueError("Invalid anchor")
        key = (anchor.source, anchor.line)
        if key in result or anchor.anchor_id in ids:
            raise ValueError("Ambiguous anchor")
        if anchor.source not in sources:
            sources[anchor.source] = read_source(anchor.source)
        raw = sources[anchor.source]
        if hashlib.sha256(raw).hexdigest() != anchor.source_sha256 or anchor.line > len(raw.splitlines()):
            raise ValueError("Stale source anchor")
        result[key] = anchor
        ids.add(anchor.anchor_id)
    return result
