import hashlib
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CHAPTERS = ROOT / "game" / "chapters"
LOCK = ROOT / "design" / "content-lock.md"
BASELINE = ROOT / "design" / "narrative" / "seven-day-content-baseline.md"

SOURCES = {
    "game/chapters/day7.rpy": CHAPTERS / "day7.rpy",
    "game/chapters/endings.rpy": CHAPTERS / "endings.rpy",
}
ENDING_IDS = (
    "rain_stops",
    "her_own_name",
    "see_the_sea",
    "one_person_train",
    "golden_cage",
    "unsent_postcard",
)
EXPECTED_COUNTS = {
    "day7.rpy": {"label": 1, "menu": 0, "scene": 1, "call": 0, "jump": 1},
    "endings.rpy": {"label": 7, "menu": 0, "scene": 7, "call": 0, "jump": 1},
}
FORBIDDEN = re.compile(
    r"(?:axis|token|qualification|resolver|persistent|hidden\s+(?:score|state|number)|ending\s+(?:condition|prediction))",
    re.IGNORECASE,
)


def player_lines(source):
    return tuple(
        line.strip()
        for line in source.splitlines()
        if re.match(r"^(?:narrator|lm|erii)\s+\"", line.strip())
    )


class ProseExpansionSprint012Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources = {key: path.read_text(encoding="utf-8") for key, path in SOURCES.items()}
        cls.lock = LOCK.read_text(encoding="utf-8")
        cls.baseline = BASELINE.read_text(encoding="utf-8")

    def test_day7_and_endings_control_boundaries_are_exact(self):
        day7 = self.sources["game/chapters/day7.rpy"]
        endings = self.sources["game/chapters/endings.rpy"]
        for filename, source in (
            ("day7.rpy", day7),
            ("endings.rpy", endings),
        ):
            for control, count in EXPECTED_COUNTS[filename].items():
                self.assertEqual(
                    count,
                    len(re.findall(r"^\s*{}\b".format(control), source, re.MULTILINE)),
                    (filename, control),
                )
        self.assertEqual(
            ENDING_IDS,
            tuple(re.findall(r'commit_ending_entry\("([a-z_]+)"\)', endings)),
        )
        self.assertEqual(
            ENDING_IDS,
            tuple(re.findall(r'commit_ending_completion\("([a-z_]+)"', endings)),
        )
        self.assertIn("jump day7_resolve_ending", day7)
        self.assertIn("jump epilogue_rain_stops_arcade", endings)
        self.assertLess(
            endings.index('$ commit_ending_completion("rain_stops"'),
            endings.index("jump epilogue_rain_stops_arcade"),
        )

    def test_added_prose_and_rain_tail_boundary_are_safe(self):
        for source in self.sources.values():
            self.assertNotRegex(source.lower(), r"(?:assets?|image|audio|music|voice|ui)/")
            for line in player_lines(source):
                self.assertNotRegex(line, FORBIDDEN)
        self.assertIsNone(re.search(r'(?m)^\s*erii\s+"', self.sources["game/chapters/endings.rpy"]))
        endings = self.sources["game/chapters/endings.rpy"]
        lights_out = endings.index("# scene_epilogue_lights_out")
        tail = endings.index("# story_025_tail_observer")
        written = endings.index("# story_025_tail_written_note")
        self.assertLess(lights_out, tail)
        self.assertLess(tail, written)
        self.assertIn("【普通街坊观察】", endings)
        self.assertIn("【绘梨衣的书面手记】", endings)
        self.assertIn("## Formal Prose Expansion Delivery Boundary", self.baseline)
        self.assertIn("| 012 |", self.baseline)

    def test_content_lock_v6_binds_day7_endings_sources(self):
        self.assertIn("content_lock:player_visible:v6:2026-08-14", self.lock)
        for source_name, path in SOURCES.items():
            match = re.search(
                r"\| `{}` \|.*?\|\s*(\d+)\s*\|\s*`([0-9a-f]{{64}})`\s*\|".format(re.escape(source_name)),
                self.lock,
            )
            self.assertIsNotNone(match, source_name)
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), match.group(2), source_name)
            self.assertEqual(len(path.read_text(encoding="utf-8").splitlines()), int(match.group(1)), source_name)


if __name__ == "__main__":
    unittest.main()
