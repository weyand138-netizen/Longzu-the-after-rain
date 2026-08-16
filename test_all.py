"""Root unittest discovery bridge for the project's ``*_test.py`` suite."""

import unittest
from pathlib import Path


def load_tests(loader, tests, pattern):
    """Make plain ``python -m unittest discover`` run the normal suite."""

    # ``tests`` intentionally uses namespace-style directories without
    # package marker files, so load the discovered modules by dotted name.
    root = Path(__file__).resolve().parent
    names = []
    for path in sorted((root / "tests").rglob("*_test.py")):
        relative = path.relative_to(root).with_suffix("")
        names.append(".".join(relative.parts))
    return loader.loadTestsFromNames(names)
