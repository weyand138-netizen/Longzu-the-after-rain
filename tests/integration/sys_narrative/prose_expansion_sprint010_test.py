import hashlib
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CHAPTERS = ROOT / "game" / "chapters"
LOCK = ROOT / "design" / "content-lock.md"
BASELINE = ROOT / "design" / "narrative" / "seven-day-content-baseline.md"

SOURCES = {
    "game/chapters/day3.rpy": CHAPTERS / "day3.rpy",
    "game/chapters/day4.rpy": CHAPTERS / "day4.rpy",
}
EXPECTED_CHOICES = {
    "day3.rpy": (
        ("day3_share_school_evidence", ("truth",)),
        ("day3_hide_school_evidence", ()),
        ("day3_honor_pause", ("understanding", "autonomy")),
        ("day3_force_explanation", ()),
    ),
    "day4.rpy": (
        ("day4_buy_two_tickets_real_name", ("preparation", "sacrifice")),
        ("day4_buy_single_ticket_cash", ("preparation",)),
        ("day4_follow_one_route_no_backup", ()),
        ("day4_register_independent_contact", ("truth",)),
        ("day4_decline_independent_contact", ()),
    ),
}
EXPECTED_COUNTS = {
    "day3.rpy": {"label": 1, "menu": 2, "scene": 1, "call": 0, "jump": 0},
    "day4.rpy": {"label": 1, "menu": 2, "scene": 1, "call": 0, "jump": 0},
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


class ProseExpansionSprint010Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources = {key: path.read_text(encoding="utf-8") for key, path in SOURCES.items()}
        cls.lock = LOCK.read_text(encoding="utf-8")
        cls.baseline = BASELINE.read_text(encoding="utf-8")

    def test_day3_day4_control_signatures_are_exact(self):
        for filename, expected in EXPECTED_CHOICES.items():
            source = self.sources["game/chapters/{}".format(filename)]
            actual = tuple(
                (choice_id, tuple(re.findall(r'"([a-z_]+)"\s*:\s*1', delta)))
                for choice_id, delta in re.findall(
                    r'apply_choice\("([a-z0-9_]+)",\s*\{([^}]*)\}\)', source
                )
            )
            self.assertEqual(expected, actual, filename)
            for control, count in EXPECTED_COUNTS[filename].items():
                self.assertEqual(count, len(re.findall(r"^\s*{}\b".format(control), source, re.MULTILINE)), (filename, control))

        day3 = self.sources["game/chapters/day3.rpy"]
        day4 = self.sources["game/chapters/day4.rpy"]
        for marker in (
            'DAY3_AGENCY_REQUEST_ID = "event_truth_pace_requested"',
            'DAY3_AGENCY_PAUSE_ANSWER_ID = "event_erii_closes_archive"',
            'event_empty_school_trace_confirmed = True',
        ):
            self.assertIn(marker, day3)
        for marker in (
            'DAY4_ROUTE_PREPARATION_ANSWER_STATE = "preserve_executable_self_controlled_option"',
            'DAY4_INDEPENDENT_CONTACT_ANSWER_STATE = "keep_independent_contact_option"',
            'resource_two_tickets = True',
            'resource_contact_card = True',
        ):
            self.assertIn(marker, day4)

    def test_added_player_prose_is_local_and_safe(self):
        for source in self.sources.values():
            self.assertNotRegex(source.lower(), r"(?:assets?|image|audio|music|voice|ui)/")
            for line in player_lines(source):
                self.assertNotRegex(line, FORBIDDEN)
        self.assertIn("## Formal Prose Expansion Delivery Boundary", self.baseline)
        self.assertIn("| 010 |", self.baseline)

    def test_content_lock_v5_binds_day3_day4_sources(self):
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
