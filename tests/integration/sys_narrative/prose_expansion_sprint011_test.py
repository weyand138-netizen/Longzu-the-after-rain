import hashlib
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CHAPTERS = ROOT / "game" / "chapters"
LOCK = ROOT / "design" / "content-lock.md"
BASELINE = ROOT / "design" / "narrative" / "seven-day-content-baseline.md"

SOURCES = {
    "game/chapters/day5.rpy": CHAPTERS / "day5.rpy",
    "game/chapters/day6.rpy": CHAPTERS / "day6.rpy",
}
EXPECTED_CHOICES = {
    "day5.rpy": (
        ("day5_share_full_archive", ("truth",)),
        ("day5_give_safe_summary", ()),
        ("day5_honor_erii_response", ("autonomy",)),
        ("day5_replace_erii_response", ()),
        ("day5_include_self_in_truth", ("preparation", "sacrifice")),
        ("day5_blame_family_only", ()),
        ("day5_repair_school_evidence", ()),
        ("day5_keep_school_evidence_hidden", ()),
        ("day5_repair_daily_choice", ()),
        ("day5_keep_daily_override", ()),
    ),
    "day6.rpy": (
        ("day6_reopen_service_exit", ("preparation",)),
        ("day6_keep_backup_abandoned", ()),
        ("day6_keep_backup_abandoned", ()),
        ("day6_use_service_exit", ()),
        ("day6_abandon_backup", ()),
        ("day6_disclose_withheld_archive", ("truth",)),
        ("day6_keep_archive_withheld", ()),
        ("day6_burn_old_identity", ("sacrifice",)),
        ("day6_shift_cost_to_erii", ()),
        ("day6_take_cost_back", ("sacrifice",)),
        ("day6_leave_cost_shifted", ()),
        ("day6_commit_independent_contact", ()),
        ("day6_commit_shared_escape", ()),
        ("day6_commit_solo_departure", ()),
        ("day6_commit_old_order_return", ()),
        ("day6_no_executable_route", ()),
    ),
}
EXPECTED_COUNTS = {
    "day5.rpy": {"label": 1, "menu": 5, "scene": 1, "call": 0, "jump": 0},
    "day6.rpy": {"label": 1, "menu": 11, "scene": 1, "call": 0, "jump": 0},
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


class ProseExpansionSprint011Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources = {key: path.read_text(encoding="utf-8") for key, path in SOURCES.items()}
        cls.lock = LOCK.read_text(encoding="utf-8")
        cls.baseline = BASELINE.read_text(encoding="utf-8")

    def test_day5_day6_control_signatures_are_exact(self):
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
                self.assertEqual(
                    count,
                    len(re.findall(r"^\s*{}\b".format(control), source, re.MULTILINE)),
                    (filename, control),
                )

        day5 = self.sources["game/chapters/day5.rpy"]
        day6 = self.sources["game/chapters/day6.rpy"]
        for marker in (
            'DAY5_RESPONSE_REQUEST_ID = "event_family_response_requested"',
            'DAY5_RESPONSE_ANSWER_EVENT_ID = "event_erii_selects_route_response"',
            'event_full_archive_shared = True',
        ):
            self.assertIn(marker, day5)
        for marker in (
            'DAY6_SOURCE_UNIT_ID = "chapter_day6_no_safe_house"',
            'event_cost_bearer_requested = True',
            'agency_day6_commitment_state = agency_day6_commitment_derivation_record["selected_commitment_state_id"]',
        ):
            self.assertIn(marker, day6)

    def test_added_player_prose_is_local_and_safe(self):
        for source in self.sources.values():
            self.assertNotRegex(source.lower(), r"(?:assets?|image|audio|music|voice|ui)/")
            for line in player_lines(source):
                self.assertNotRegex(line, FORBIDDEN)
        self.assertIn("## Formal Prose Expansion Delivery Boundary", self.baseline)
        self.assertIn("| 011 |", self.baseline)

    def test_content_lock_v5_binds_day5_day6_sources(self):
        self.assertIn("content_lock:player_visible:v5:2026-08-14", self.lock)
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
