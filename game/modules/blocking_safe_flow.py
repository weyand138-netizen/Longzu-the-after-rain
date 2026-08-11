"""SYS-SAVE blocking-safe context and explicit recovery exits."""

from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class BlockingContext:
    """Root-safe context that cannot retain a loaded-scene return path."""

    caller_context: Any
    loaded_scene_visible: bool
    loaded_scene_updated: bool
    focusable_loaded_controls: bool
    timer_count: int
    callback_count: int
    shortcut_count: int
    return_path_present: bool


@dataclass(frozen=True)
class SafeFlowResult:
    action: str
    context: BlockingContext
    persistent_root: dict[str, Any]
    run_initialized: bool
    os_quit: bool


def enter_blocking_flow(*, caller_context: Any, persistent_root: dict[str, Any]) -> BlockingContext:
    """Destroy loaded-scene context before making the blocking screen visible."""

    return BlockingContext(None, False, False, False, 0, 0, 0, False)


def handle_blocking_action(context: BlockingContext, action: str, *, persistent_root: dict[str, Any], new_run_factory: Callable[[], Any] | None = None) -> SafeFlowResult:
    """Permit only main-menu, explicit new-game, or OS quit from blocked state."""

    if action not in ("main_menu", "new_game", "os_quit"):
        return SafeFlowResult("blocked", context, persistent_root, False, False)
    if action == "os_quit":
        return SafeFlowResult(action, context, persistent_root, False, True)
    if action == "main_menu":
        return SafeFlowResult(action, context, persistent_root, False, False)
    if not callable(new_run_factory):
        raise TypeError("new_game requires a factory")
    new_run_factory()
    return SafeFlowResult(action, context, persistent_root, True, False)
