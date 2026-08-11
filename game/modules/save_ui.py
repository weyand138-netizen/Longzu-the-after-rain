"""SYS-SAVE slot UI model with metadata and keyboard-accessible semantics."""

from dataclasses import dataclass


@dataclass(frozen=True)
class SlotPresentation:
    slot_id: str
    label: str
    metadata: tuple[tuple[str, str], ...]
    visible: bool
    enabled: bool
    focusable: bool
    timed: bool
    hover_required: bool


def build_slot_presentation(slot_id: str, metadata: dict[str, str], *, available: bool = True) -> SlotPresentation:
    if type(slot_id) is not str or not slot_id:
        raise TypeError("slot_id must be a non-empty string")
    if type(metadata) is not dict or any(type(k) is not str or type(v) is not str for k, v in metadata.items()):
        raise TypeError("metadata must be a string dict")
    label = metadata.get("location", "Empty slot")
    return SlotPresentation(slot_id, label, tuple(sorted(metadata.items())), True, available, available, False, False)


def keyboard_path(slots: tuple[SlotPresentation, ...], index: int) -> SlotPresentation:
    if not slots or type(index) is not int or index < 0 or index >= len(slots):
        raise IndexError("focus index outside slot list")
    return slots[index]
