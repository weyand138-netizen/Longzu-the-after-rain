"""Production focus graph and keyboard viewport helpers.

Ren'Py's default focus navigation only considers focusables that are already
inside the rendered viewport.  P0 screens instead need a semantic graph: the
next node is selected first, its viewport is made visible, and only then is
the node focused.  This module deliberately performs no activation while
moving focus or scrolling.
"""

import renpy
from renpy.exports import get_widget
from renpy.display.screen import get_displayable


_active_graph = None
_installed = False


def _install_key_router():
    global _installed
    if _installed:
        return

    original = renpy.display.focus.key_handler

    def routed_key_handler(event):
        graph = _active_graph
        if graph is not None and graph.is_active():
            if renpy.display.behavior.map_event(event, "focus_graph_next") or renpy.display.behavior.map_event(event, "K_TAB"):
                graph.move(1)
                return True
            if renpy.display.behavior.map_event(event, "focus_graph_previous") or renpy.display.behavior.map_event(event, "shift_K_TAB"):
                graph.move(-1)
                return True
        return original(event)

    renpy.display.focus.key_handler = routed_key_handler
    _installed = True


class FocusAwareGraph(object):
    """A stable semantic focus graph with focus-aware viewport scrolling.

    ``nodes`` may be a list of semantic ids or dictionaries.  A dictionary
    can provide ``id`` and an optional ``estimated_rect`` (x, y, width, height)
    in the viewport's screen coordinate space.  The estimate is used only
    when Ren'Py has not rendered the target into its focus list yet.
    """

    def __init__(self, screen_name, nodes, viewport_id=None, default_id=None, viewport_rect=None):
        self.screen_name = screen_name
        self.nodes = []
        for node in nodes:
            if isinstance(node, dict):
                self.nodes.append(dict(node))
            else:
                self.nodes.append({"id": node})
        self.viewport_id = viewport_id
        self.default_id = default_id or (self.nodes[0]["id"] if self.nodes else None)
        self.viewport_rect = viewport_rect
        self.last_id = None
        _install_key_router()

    def is_active(self):
        return self._widget(self.default_id) is not None

    def activate(self):
        global _active_graph
        _active_graph = self

    def _widget(self, semantic_id):
        if semantic_id is None:
            return None
        return (
            get_displayable(self.screen_name, semantic_id, base=True)
            or get_widget(self.screen_name, semantic_id)
            or get_widget(None, semantic_id)
        )

    @staticmethod
    def _same_widget(left, right):
        return (
            left is right
            or getattr(left, "child", None) is right
            or getattr(right, "child", None) is left
        )

    def current_id(self):
        focused = renpy.display.focus.get_focused()
        for node in self.nodes:
            if self._same_widget(focused, self._widget(node["id"])):
                return node["id"]
        if focused is not None and self.last_id in [node["id"] for node in self.nodes]:
            return self.last_id
        return None

    def _focus_item(self, widget):
        if widget is None:
            return None
        for item in renpy.display.focus.focus_list:
            if self._same_widget(item.widget, widget) and item.arg is None:
                if item.x is not False and item.x is not None:
                    return item
        return None

    def _rect(self, semantic_id):
        widget = self._widget(semantic_id)
        item = self._focus_item(widget)
        if item is not None:
            return (item.x, item.y, item.w, item.h)

        # Displayables retain their last layout rectangle after rendering.
        # This is useful for a target that has just moved out of the viewport.
        if widget is not None:
            values = tuple(getattr(widget, key, None) for key in ("x", "y", "width", "height"))
            if all(value is not None for value in values):
                return values

        for node in self.nodes:
            if node["id"] == semantic_id:
                estimate = node.get("estimated_rect")
                if estimate is not None:
                    viewport = (
                        get_widget(self.screen_name, self.viewport_id)
                        or get_widget(None, self.viewport_id)
                    )
                    offset = getattr(getattr(viewport, "yadjustment", None), "value", 0) or 0
                    return (estimate[0], estimate[1] - offset, estimate[2], estimate[3])
        return None

    def _viewport_rect(self):
        viewport = (
            get_widget(self.screen_name, self.viewport_id)
            or get_widget(None, self.viewport_id)
        )
        if viewport is None:
            return None
        values = tuple(getattr(viewport, key, None) for key in ("x", "y", "width", "height"))
        if not all(value is not None for value in values):
            if self.viewport_rect is None:
                return None
            values = self.viewport_rect
        if not all(value is not None for value in values):
            return None
        return viewport, values

    def _scroll_target_into_view(self, semantic_id):
        viewport_data = self._viewport_rect()
        target = self._rect(semantic_id)
        if viewport_data is None or target is None:
            return False

        viewport, (vx, vy, vw, vh) = viewport_data
        _, target_y, _, target_h = target
        current = viewport.yadjustment.value
        desired = current

        if target_y < vy:
            desired = current - (vy - target_y)
        elif target_y + target_h > vy + vh:
            desired = current + (target_y + target_h - (vy + vh))

        desired = max(0, min(desired, viewport.yadjustment.range))
        if desired != current:
            # Adjustment.change only changes layout state.  No story action,
            # rollback, or activation is attached to this adjustment.
            viewport.yadjustment.change(desired)
            return True
        return False

    def ensure_initial_focus(self):
        """Establish the screen's legal initial focus without mouse input."""

        if not self.nodes:
            return
        self.activate()
        if self.current_id() is not None:
            return
        widget = self._widget(self.default_id)
        if widget is not None:
            self._scroll_target_into_view(self.default_id)
            self.last_id = self.default_id
            renpy.display.focus.force_focus(widget)

    def move(self, delta):
        """Move within the graph; scrolling never activates a node."""

        if not self.nodes:
            return
        self.activate()

        current = self.current_id()
        ids = [node["id"] for node in self.nodes]
        if current in ids:
            index = ids.index(current) + delta
        else:
            index = 0 if delta > 0 else len(ids) - 1
        index = max(0, min(index, len(ids) - 1))
        target_id = ids[index]
        target = self._widget(target_id)
        if target is None:
            return

        self._scroll_target_into_view(target_id)
        self.last_id = target_id
        renpy.display.focus.force_focus(target)

    def is_fully_visible(self, semantic_id):
        viewport_data = self._viewport_rect()
        target = self._rect(semantic_id)
        if viewport_data is None or target is None:
            return False
        _, (vx, vy, vw, vh) = viewport_data
        tx, ty, tw, th = target
        return tx >= vx and ty >= vy and tx + tw <= vx + vw and ty + th <= vy + vh
