"""Production audio catalogue validation, deliberately independent of Ren'Py.

The runtime bridge owns playback state.  This module only verifies an approved
mapping from source locations to stable continuous-audio contexts and builds
the exact statement anchors that can emit an authored one-shot.
"""
from dataclasses import dataclass
import hashlib
import re
from pathlib import PurePosixPath

from .audio_scene import AudioSceneAnchor


_SAY_LINE = re.compile(rb"^[ \t]*(?:narrator|lm|erii)[ \t]+(?:\"|')")


def _valid_relative_path(path, suffix=None):
    if not isinstance(path, str) or not path.strip():
        return False
    value = PurePosixPath(path)
    return (
        not value.is_absolute()
        and ".." not in value.parts
        and "\\" not in path
        and ":" not in path
        and "\x00" not in path
        and (suffix is None or value.suffix == suffix)
    )


def _valid_digest(value):
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(char in "0123456789abcdef" for char in value)
    )


@dataclass(frozen=True)
class AudioContextRange:
    """An intentional continuous context for every source line in a span."""

    source: str
    first_line: int
    last_line: int
    source_sha256: str
    context_id: str

    def __post_init__(self):
        if not _valid_relative_path(self.source, ".rpy"):
            raise ValueError("Invalid context source")
        if type(self.first_line) is not int or type(self.last_line) is not int:
            raise ValueError("Invalid context line")
        if self.first_line < 1 or self.last_line < self.first_line:
            raise ValueError("Invalid context range")
        if not _valid_digest(self.source_sha256):
            raise ValueError("Invalid context source digest")
        if not isinstance(self.context_id, str) or not self.context_id.strip():
            raise ValueError("Invalid context identity")


@dataclass(frozen=True)
class AudioOneShotBinding:
    """The limited set of reviewed narrative actions that may emit a sound."""

    anchor_id: str
    source: str
    line: int
    cue_id: str

    def __post_init__(self):
        if not isinstance(self.anchor_id, str) or not self.anchor_id.strip():
            raise ValueError("Invalid action anchor")
        if not _valid_relative_path(self.source, ".rpy"):
            raise ValueError("Invalid action source")
        if type(self.line) is not int or self.line < 1:
            raise ValueError("Invalid action line")
        if not isinstance(self.cue_id, str) or not self.cue_id.strip():
            raise ValueError("Invalid action cue")


@dataclass(frozen=True)
class AudioAssetRecord:
    asset_id: str
    filename: str
    sha256: str

    def __post_init__(self):
        if not isinstance(self.asset_id, str) or not self.asset_id.strip():
            raise ValueError("Invalid asset identity")
        if not _valid_relative_path(self.filename):
            raise ValueError("Invalid asset path")
        if not _valid_digest(self.sha256):
            raise ValueError("Invalid asset digest")


@dataclass(frozen=True)
class ProductionAudioSceneCatalog:
    anchors: tuple
    ranges: tuple
    ranges_by_source: dict

    def context_for(self, source, line):
        for item in self.ranges_by_source.get(source, ()):
            if item.first_line <= line <= item.last_line:
                return item.context_id
        return None


def _source_bytes(read_source, source):
    raw = read_source(source)
    if not isinstance(raw, bytes):
        raise ValueError("Source reader must return bytes")
    return raw


def _say_lines(raw):
    return tuple(
        number
        for number, line in enumerate(raw.splitlines(), 1)
        if _SAY_LINE.match(line)
    )


def compile_context_ranges(ranges, read_source):
    """Verify exact file hashes, non-overlap, and full readable-line coverage."""
    per_source = {}
    source_bytes = {}
    for item in ranges:
        if not isinstance(item, AudioContextRange):
            raise ValueError("Invalid context range")
        if item.source not in source_bytes:
            source_bytes[item.source] = _source_bytes(read_source, item.source)
        raw = source_bytes[item.source]
        if hashlib.sha256(raw).hexdigest() != item.source_sha256:
            raise ValueError("Stale context source")
        if item.last_line > len(raw.splitlines()):
            raise ValueError("Context range outside source")
        per_source.setdefault(item.source, []).append(item)

    normalized = {}
    for source, items in per_source.items():
        ordered = tuple(sorted(items, key=lambda value: (value.first_line, value.last_line)))
        for previous, current in zip(ordered, ordered[1:]):
            if current.first_line <= previous.last_line:
                raise ValueError("Overlapping context ranges")
        for line in _say_lines(source_bytes[source]):
            if sum(item.first_line <= line <= item.last_line for item in ordered) != 1:
                raise ValueError("Readable line has no unique audio context")
        normalized[source] = ordered
    if not normalized:
        raise ValueError("Empty context catalogue")
    return normalized


def compile_production_scene_catalog(ranges, oneshots, read_source):
    """Build every statement anchor after source/range validation.

    A continuous context is anchored at every readable say statement.  Only
    reviewed action lines receive a one-shot ID.  Thus a load can resolve a
    context independently from whether the position has an action sound.
    """
    ranges_by_source = compile_context_ranges(ranges, read_source)
    action_by_location = {}
    action_ids = set()
    for action in oneshots:
        if not isinstance(action, AudioOneShotBinding):
            raise ValueError("Invalid action binding")
        key = (action.source, action.line)
        if key in action_by_location or action.anchor_id in action_ids:
            raise ValueError("Ambiguous action binding")
        source_ranges = ranges_by_source.get(action.source, ())
        if not any(item.first_line <= action.line <= item.last_line for item in source_ranges):
            raise ValueError("Action has no continuous context")
        raw = _source_bytes(read_source, action.source)
        lines = raw.splitlines()
        if action.line > len(lines) or not _SAY_LINE.match(lines[action.line - 1]):
            raise ValueError("Action must point to a readable statement")
        action_by_location[key] = action
        action_ids.add(action.anchor_id)

    anchors = []
    anchor_ids = set(action_ids)
    for source, items in ranges_by_source.items():
        raw = _source_bytes(read_source, source)
        digest = hashlib.sha256(raw).hexdigest()
        for line in _say_lines(raw):
            context_id = next(
                item.context_id for item in items if item.first_line <= line <= item.last_line
            )
            action = action_by_location.get((source, line))
            anchor_id = action.anchor_id if action else "continuous:{}:{}".format(source, line)
            if anchor_id in anchor_ids and action is None:
                raise ValueError("Ambiguous generated anchor")
            anchor_ids.add(anchor_id)
            anchors.append(AudioSceneAnchor(
                anchor_id=anchor_id,
                source=source,
                line=line,
                source_sha256=digest,
                context_id=context_id,
                oneshot_id=action.cue_id if action else None,
            ))
    return ProductionAudioSceneCatalog(
        anchors=tuple(anchors),
        ranges=tuple(ranges),
        ranges_by_source=ranges_by_source,
    )


def verify_audio_assets(assets, read_asset):
    """Validate exactly the approved runtime bytes, without re-encoding them."""
    seen_ids = set()
    seen_files = set()
    for asset in assets:
        if not isinstance(asset, AudioAssetRecord):
            raise ValueError("Invalid asset record")
        if asset.asset_id in seen_ids or asset.filename in seen_files:
            raise ValueError("Duplicate asset admission")
        raw = read_asset(asset.filename)
        if not isinstance(raw, bytes) or hashlib.sha256(raw).hexdigest() != asset.sha256:
            raise ValueError("Stale or missing runtime asset")
        seen_ids.add(asset.asset_id)
        seen_files.add(asset.filename)
    if not seen_ids:
        raise ValueError("Empty asset admission")
    return True
