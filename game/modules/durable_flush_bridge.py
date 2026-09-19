"""Source-pinned Ren'Py persistent-write verification.

This module deliberately imports no Ren'Py module at import time, so pure
tests can provide a narrowly-shaped runtime double.  Production creates the
bridge from ``10_state.rpy``; the bridge is the only runtime flush port that
may report a verified durable result.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import os
from pathlib import Path
from typing import Any
import zlib

from .persist_batch import (
    PERSIST_FLUSH_FAILED_SAFE,
)
from .persist_schema import snapshot_persist_root


EXPECTED_RENPY_VERSION = (8, 5, 3, 26051504)
EXPECTED_SOURCE_HASHES = {
    "persistent.py": "392C209AB827AD51E0ECDE6303CBD12C5A31EBEC8FCBFF51C9FE94CDB2719400",
    "savelocation.py": "E0B32AAB4127325A307A8396B6A9B636781161FD23D595127E668D784342B85C",
    "loadsave.py": "70CD82D5FC2245F647306951AC2ED1A1426F7DC23B3EE8EBB2F5236EC32A34E1",
    "exports/persistentexports.py": "DE24EDD96BDE8AED33442BA35CB1D7B6AC374B8A0F4374850EB3CCAC15D7E969",
}

# These are bridge-internal observations.  In particular, preflight and the
# bridge itself must not leak another public success name to a caller.  The
# SYS-PERSIST coordinator maps ``verified`` to the sole public success status.
PREFLIGHT_READY = "PREFLIGHT_READY"
BRIDGE_VERIFIED = "BRIDGE_VERIFIED"
BRIDGE_UNKNOWN = "BRIDGE_UNKNOWN"


@dataclass(frozen=True)
class DurableFlushPreflight:
    """Detached pre-replacement admission result for one bridge operation."""

    status: str
    locations: tuple[Any, ...] = ()

    @property
    def ready(self) -> bool:
        return self.status == PREFLIGHT_READY


@dataclass(frozen=True)
class DurableFlushResult:
    """Internal bridge fact; only ``verified`` admits the public success."""

    status: str
    location_count: int = 0

    @property
    def verified(self) -> bool:
        return self.status == BRIDGE_VERIFIED


class DurableFlushBridge:
    """Verify the pinned native persistent path without public-wrapper success.

    The implementation intentionally supports only the source-pinned
    ``FileLocation`` adapter.  Any other active location is a known
    pre-replacement failure; a write or readback problem after replacement is
    deliberately indeterminate.
    """

    def __init__(self, *, renpy_module: Any | None = None, sdk_root: str | os.PathLike[str] | None = None):
        self._renpy_module = renpy_module
        self._sdk_root = None if sdk_root is None else Path(sdk_root)

    def _renpy(self) -> Any:
        if self._renpy_module is not None:
            return self._renpy_module
        import renpy  # type: ignore

        return renpy

    def _source_root(self, renpy_module: Any) -> Path:
        if self._sdk_root is not None:
            return self._sdk_root / "renpy"
        module_file = getattr(renpy_module, "__file__", None)
        if type(module_file) is not str or not module_file:
            raise RuntimeError("Ren'Py module path is unavailable")
        return Path(module_file).resolve().parent

    def _pins_match(self, renpy_module: Any) -> bool:
        version = tuple(getattr(renpy_module, "version_tuple", ()))
        if version != EXPECTED_RENPY_VERSION:
            return False
        source_root = self._source_root(renpy_module)
        for relative_path, expected_hash in EXPECTED_SOURCE_HASHES.items():
            source = source_root / relative_path
            if not source.is_file():
                return False
            actual_hash = hashlib.sha256(source.read_bytes()).hexdigest().upper()
            if actual_hash != expected_hash:
                return False
        return True

    def preflight(self) -> DurableFlushPreflight:
        """Check every known no-write condition before root replacement."""

        try:
            renpy_module = self._renpy()
            if not self._pins_match(renpy_module):
                return DurableFlushPreflight(PERSIST_FLUSH_FAILED_SAFE)
            if getattr(renpy_module.config, "save_persistent", None) is not True:
                return DurableFlushPreflight(PERSIST_FLUSH_FAILED_SAFE)
            if getattr(renpy_module.persistent, "should_save_persistent", None) is not True:
                return DurableFlushPreflight(PERSIST_FLUSH_FAILED_SAFE)
            location_manager = renpy_module.loadsave.location
            locations = tuple(location_manager.active_locations())
            file_location_type = renpy_module.savelocation.FileLocation
            if not locations:
                return DurableFlushPreflight(PERSIST_FLUSH_FAILED_SAFE)
            for location in locations:
                if type(location) is not file_location_type:
                    return DurableFlushPreflight(PERSIST_FLUSH_FAILED_SAFE)
                if getattr(location, "active", None) is not True:
                    return DurableFlushPreflight(PERSIST_FLUSH_FAILED_SAFE)
                filename = getattr(location, "persistent", None)
                if type(filename) is not str or not filename:
                    return DurableFlushPreflight(PERSIST_FLUSH_FAILED_SAFE)
            return DurableFlushPreflight(PREFLIGHT_READY, locations)
        except Exception:
            return DurableFlushPreflight(PERSIST_FLUSH_FAILED_SAFE)

    @staticmethod
    def _write_and_verify(filename: str, temporary_suffix: str, data: bytes) -> None:
        """Perform the pinned ``.tmp -> .new -> final`` shape with readback."""

        temporary = filename + temporary_suffix
        replacement = filename + ".new"
        # ``xb`` makes a stale temporary file an explicit ambiguous condition
        # rather than silently overwriting evidence from an interrupted write.
        with open(temporary, "xb") as handle:
            written = handle.write(data)
            if written != len(data):
                raise OSError("persistent temporary write was partial")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, replacement)
        os.replace(replacement, filename)
        with open(filename, "rb") as handle:
            if handle.read() != data:
                raise OSError("persistent readback did not match candidate bytes")

    @staticmethod
    def _observe_update_and_merge(renpy_module: Any, expected_root: Any) -> bool:
        """Run the pinned merge portion of ``update`` without its no-result save.

        ``persistent.update(True)`` ends by calling the engine's swallowing
        ``persistent.save``.  Reusing that public/no-result path would make the
        bridge's strict write redundant and could falsely admit a swallowed
        failure.  This is the source-pinned update equivalent: consume and
        merge newer persistent payloads, then let the bridge perform the one
        explicit strict write below.  Any observed merge is deliberately not a
        live durable success, even if it happens to produce equal values.
        """

        persistent_module = renpy_module.persistent
        location_manager = renpy_module.loadsave.location
        current_mtime = persistent_module.persistent_mtime
        pairs = tuple(location_manager.load_persistent(consume=True))
        ordered_pairs = tuple(sorted(pairs, key=lambda pair: pair[0]))
        newest_mtime = current_mtime
        merge_observed = False
        for mtime, other in ordered_pairs:
            if mtime <= current_mtime:
                continue
            newest_mtime = mtime
            if other is None:
                # The engine may represent an unreadable newer payload as
                # ``None``.  It cannot prove that the proposed candidate was
                # the only persistent state involved in this operation.
                merge_observed = True
                continue
            merge_observed = True
            persistent_module.merge(other)
        persistent_module.persistent_mtime = newest_mtime
        current_root = getattr(renpy_module.game.persistent, "sys_persist_state", None)
        return merge_observed or current_root != expected_root

    def flush_after_replacement(
        self,
        preflight: DurableFlushPreflight,
        expected_root: Any = None,
    ) -> DurableFlushResult:
        """Strictly write and read back the signed current persistent bytes.

        This method is valid only after the owner has assigned its complete
        candidate root.  Any failure here follows replacement and is therefore
        ``COMMIT_STATUS_UNKNOWN`` rather than a recoverable safe failure.
        """

        if not isinstance(preflight, DurableFlushPreflight) or not preflight.ready:
            return DurableFlushResult(BRIDGE_UNKNOWN)
        try:
            renpy_module = self._renpy()
            # Both controls were safe only because preflight read them before
            # replacement.  A late disable is not evidence that no write
            # began, so it must remain an indeterminate post-replacement
            # outcome rather than being relabelled as a safe failure.
            if getattr(renpy_module.config, "save_persistent", None) is not True:
                return DurableFlushResult(BRIDGE_UNKNOWN)
            if getattr(renpy_module.persistent, "should_save_persistent", None) is not True:
                return DurableFlushResult(BRIDGE_UNKNOWN)
            location_manager = renpy_module.loadsave.location
            current_locations = tuple(location_manager.active_locations())
            if current_locations != preflight.locations:
                return DurableFlushResult(BRIDGE_UNKNOWN)
            current_root = getattr(renpy_module.game.persistent, "sys_persist_state", None)
            # The owner provides a detached complete candidate. Passing the
            # live root (or nothing) would let a replacement-side mutation
            # redefine what the bridge claims to have verified.
            if expected_root is None or expected_root is current_root:
                return DurableFlushResult(BRIDGE_UNKNOWN)
            expected_candidate = snapshot_persist_root(expected_root)
            if self._observe_update_and_merge(renpy_module, expected_candidate):
                return DurableFlushResult(BRIDGE_UNKNOWN)
            data = renpy_module.persistent.dumps(
                renpy_module.game.persistent,
                bad_reduction_name="persistent",
            )
            compressed = zlib.compress(data, 3)
            signed_bytes = compressed + renpy_module.savetoken.sign_data(data).encode("utf-8")
            savelocation = renpy_module.savelocation
            with savelocation.disk_lock:
                savelocation.pause_syncfs()
                try:
                    for location in reversed(preflight.locations):
                        self._write_and_verify(location.persistent, savelocation.tmp, signed_bytes)
                        location.persistent_mtime = os.path.getmtime(location.persistent)
                        renpy_module.util.expose_file(location.persistent)
                finally:
                    savelocation.resume_syncfs()
            return DurableFlushResult(BRIDGE_VERIFIED, len(preflight.locations))
        except Exception:
            return DurableFlushResult(BRIDGE_UNKNOWN)
