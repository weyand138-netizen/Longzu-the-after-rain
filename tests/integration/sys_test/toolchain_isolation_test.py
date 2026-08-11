import unittest

from game.modules.toolchain_isolation import *


class ToolchainIsolationTests(unittest.TestCase):
    def test_environment_and_dependency_closure(self):
        approved = EnvironmentIdentity("RenPy", "8.5.3", "3.12", "software", "abc")
        self.assertTrue(environment_matches(approved, approved))
        self.assertEqual(scan_dependency_closure((("production/a", "tests/spy"),)), (("production/a", "tests/spy"),))

    def test_test_only_markers_and_cleanup(self):
        self.assertEqual(scan_test_only_markers(("tests/observer.py", "game/main.rpy")), ("tests/observer.py",))
        self.assertTrue(cleanup_guard(lambda: None))


if __name__ == "__main__":
    unittest.main()
