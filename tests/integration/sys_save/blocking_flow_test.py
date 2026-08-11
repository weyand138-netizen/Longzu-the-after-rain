import unittest

from game.modules.blocking_safe_flow import *
from game.modules.persist_schema import build_fresh_persist_root


class BlockingFlowTests(unittest.TestCase):
    def test_blocking_flow_removes_loaded_context_and_only_allows_safe_exits(self):
        root = build_fresh_persist_root()
        context = enter_blocking_flow(caller_context="loaded-scene", persistent_root=root)
        self.assertFalse(context.loaded_scene_visible or context.return_path_present)
        self.assertEqual(handle_blocking_action(context, "rollback", persistent_root=root).action, "blocked")
        self.assertTrue(handle_blocking_action(context, "main_menu", persistent_root=root).action == "main_menu")
        calls = []
        new_game = handle_blocking_action(context, "new_game", persistent_root=root, new_run_factory=lambda: calls.append(1))
        self.assertTrue(new_game.run_initialized)
        self.assertEqual(calls, [1])

    def test_os_quit_does_not_return_to_scene(self):
        context = enter_blocking_flow(caller_context="scene", persistent_root=build_fresh_persist_root())
        result = handle_blocking_action(context, "os_quit", persistent_root=build_fresh_persist_root())
        self.assertTrue(result.os_quit)


if __name__ == "__main__":
    unittest.main()
