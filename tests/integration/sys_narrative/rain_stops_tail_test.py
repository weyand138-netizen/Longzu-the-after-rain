import hashlib
import re
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "game"))
sys.path.insert(0, str(ROOT / "tests"))

from modules.ending_rules import (  # noqa: E402
    _PREDICATE_CLAUSE_RECORDS,
    _QUALIFICATION_BINDINGS,
    _TOKEN_DOMAINS,
    AXES,
    ENDING_PRIORITY,
)
from test_ending_rules import WITNESSES  # noqa: E402


ENDINGS_SOURCE = ROOT / "game" / "chapters" / "endings.rpy"
ENDING_RULES_SOURCE = ROOT / "game" / "modules" / "ending_rules.py"
STATE_SOURCE = ROOT / "game" / "10_state.rpy"
DAY7_SOURCE = ROOT / "game" / "chapters" / "day7.rpy"
BASELINE = ROOT / "design" / "narrative" / "seven-day-content-baseline.md"
CONTENT_LOCK = ROOT / "design" / "content-lock.md"

EXPECTED_UNITS = (
    "chapter_prologue_rain_platform",
    "chapter_day1_her_own_name",
    "chapter_day2_two_game_tokens",
    "chapter_day3_empty_school",
    "chapter_day4_seaside_train",
    "chapter_day5_family_lie",
    "chapter_day6_no_safe_house",
    "chapter_day7_before_red_well",
    "ending_rain_stops",
    "ending_her_own_name",
    "ending_see_the_sea",
    "ending_one_person_train",
    "ending_golden_cage",
    "ending_unsent_postcard",
    "epilogue_rain_stops_arcade",
)
EXPECTED_ENDINGS = (
    "rain_stops",
    "her_own_name",
    "see_the_sea",
    "one_person_train",
    "golden_cage",
    "unsent_postcard",
)
EXPECTED_AXES = (
    "understanding",
    "autonomy",
    "truth",
    "preparation",
    "sacrifice",
)
EXPECTED_TOKENS = (
    "token_override_first_destination",
    "token_override_daily_choice",
    "token_silence_as_consent",
    "token_hide_school_evidence",
    "token_withhold_family_truth",
    "token_abandon_backup_plan",
    "token_shift_promised_cost",
)
EXPECTED_QUALIFICATIONS = (
    "qualification_independent_contact_route",
    "qualification_shared_escape_route",
    "qualification_solo_departure_route",
    "qualification_old_order_return_route",
)
EXPECTED_LABELS = tuple(
    (ending_id, "ending_{}".format(ending_id)) for ending_id in EXPECTED_ENDINGS
)
FORBIDDEN_WORLD_STATE_MARKERS = ("夏弥", "源氏兄弟", "路鸣泽", "怀孕", "双胞胎", "龙凤胎")

EXPECTED_TOKEN_DOMAINS = {
    "token_override_first_destination": "autonomy",
    "token_override_daily_choice": "autonomy",
    "token_silence_as_consent": "understanding",
    "token_hide_school_evidence": "truth",
    "token_withhold_family_truth": "truth",
    "token_abandon_backup_plan": "preparation",
    "token_shift_promised_cost": "sacrifice",
}

EXPECTED_QUALIFICATION_BINDINGS = (
    (
        "qualification_independent_contact_route",
        ("day6_commit_independent_contact",),
        (
            "event_independent_route_committed",
            "event_contact_risk_handover_complete",
            "event_route_preference_honored",
        ),
        ("resource_contact_card",),
    ),
    (
        "qualification_shared_escape_route",
        ("day6_commit_shared_escape",),
        (
            "event_shared_route_committed",
            "event_shared_cost_acknowledged",
            "event_route_preference_honored",
        ),
        ("resource_two_tickets",),
    ),
    (
        "qualification_solo_departure_route",
        ("day6_commit_solo_departure",),
        (
            "event_solo_route_committed",
            "event_no_continuing_contact_commitment",
            "event_route_preference_honored",
        ),
        ("resource_single_ticket",),
    ),
    (
        "qualification_old_order_return_route",
        ("day6_commit_old_order_return",),
        ("event_old_order_route_committed",),
        (),
    ),
)

EXPECTED_PREDICATE_SHAPES = {
    "rain_stops": (
        ("root", 0, "group_all", (
            "rain_stops_axis_understanding_at_least_3",
            "rain_stops_axis_autonomy_at_least_3",
            "rain_stops_axis_truth_at_least_3",
            "rain_stops_axis_preparation_at_least_3",
            "rain_stops_axis_sacrifice_at_least_3",
            "rain_stops_tokens_all_absent",
        ), None, (), None, None),
        ("axis_understanding_at_least_3", 1, "atomic", (), "axis_value", ("understanding",), "at_least", 3),
        ("axis_autonomy_at_least_3", 2, "atomic", (), "axis_value", ("autonomy",), "at_least", 3),
        ("axis_truth_at_least_3", 3, "atomic", (), "axis_value", ("truth",), "at_least", 3),
        ("axis_preparation_at_least_3", 4, "atomic", (), "axis_value", ("preparation",), "at_least", 3),
        ("axis_sacrifice_at_least_3", 5, "atomic", (), "axis_value", ("sacrifice",), "at_least", 3),
        ("tokens_all_absent", 6, "atomic", (), "unresolved_token", tuple(EXPECTED_TOKEN_DOMAINS), "absent", None),
    ),
    "her_own_name": (
        ("root", 0, "group_all", (
            "her_own_name_axis_autonomy_at_least_3",
            "her_own_name_axis_truth_at_least_3",
            "her_own_name_axis_understanding_at_least_2",
            "her_own_name_qualification_independent_present",
            "her_own_name_tokens_autonomy_truth_absent",
        ), None, (), None, None),
        ("axis_autonomy_at_least_3", 1, "atomic", (), "axis_value", ("autonomy",), "at_least", 3),
        ("axis_truth_at_least_3", 2, "atomic", (), "axis_value", ("truth",), "at_least", 3),
        ("axis_understanding_at_least_2", 3, "atomic", (), "axis_value", ("understanding",), "at_least", 2),
        ("qualification_independent_present", 4, "atomic", (), "route_qualification", ("qualification_independent_contact_route",), "present", None),
        ("tokens_autonomy_truth_absent", 5, "atomic", (), "unresolved_token", (
            "token_override_first_destination",
            "token_override_daily_choice",
            "token_hide_school_evidence",
            "token_withhold_family_truth",
        ), "absent", None),
    ),
    "see_the_sea": (
        ("root", 0, "group_all", (
            "see_the_sea_axis_autonomy_at_least_2",
            "see_the_sea_axis_preparation_at_least_2",
            "see_the_sea_axis_sacrifice_at_least_2",
            "see_the_sea_axis_understanding_at_least_1",
            "see_the_sea_axis_truth_at_least_1",
            "see_the_sea_qualification_shared_present",
            "see_the_sea_tokens_autonomy_truth_sacrifice_absent",
        ), None, (), None, None),
        ("axis_autonomy_at_least_2", 1, "atomic", (), "axis_value", ("autonomy",), "at_least", 2),
        ("axis_preparation_at_least_2", 2, "atomic", (), "axis_value", ("preparation",), "at_least", 2),
        ("axis_sacrifice_at_least_2", 3, "atomic", (), "axis_value", ("sacrifice",), "at_least", 2),
        ("axis_understanding_at_least_1", 4, "atomic", (), "axis_value", ("understanding",), "at_least", 1),
        ("axis_truth_at_least_1", 5, "atomic", (), "axis_value", ("truth",), "at_least", 1),
        ("qualification_shared_present", 6, "atomic", (), "route_qualification", ("qualification_shared_escape_route",), "present", None),
        ("tokens_autonomy_truth_sacrifice_absent", 7, "atomic", (), "unresolved_token", (
            "token_override_first_destination",
            "token_override_daily_choice",
            "token_hide_school_evidence",
            "token_withhold_family_truth",
            "token_shift_promised_cost",
        ), "absent", None),
    ),
    "one_person_train": (
        ("root", 0, "group_all", ("one_person_train_qualification_solo_present", "one_person_train_loss_any"), None, (), None, None),
        ("qualification_solo_present", 1, "atomic", (), "route_qualification", ("qualification_solo_departure_route",), "present", None),
        ("loss_any", 2, "group_any", (
            "one_person_train_understanding_at_most_1",
            "one_person_train_preparation_at_most_1",
            "one_person_train_loss_tokens_present",
        ), None, (), None, None),
        ("understanding_at_most_1", 3, "atomic", (), "axis_value", ("understanding",), "at_most", 1),
        ("preparation_at_most_1", 4, "atomic", (), "axis_value", ("preparation",), "at_most", 1),
        ("loss_tokens_present", 5, "atomic", (), "unresolved_token", (
            "token_silence_as_consent",
            "token_hide_school_evidence",
            "token_withhold_family_truth",
            "token_abandon_backup_plan",
        ), "present", None),
    ),
    "golden_cage": (
        ("root", 0, "group_all", ("golden_cage_qualification_old_order_present", "golden_cage_tokens_autonomy_present"), None, (), None, None),
        ("qualification_old_order_present", 1, "atomic", (), "route_qualification", ("qualification_old_order_return_route",), "present", None),
        ("tokens_autonomy_present", 2, "atomic", (), "unresolved_token", (
            "token_override_first_destination",
            "token_override_daily_choice",
        ), "present", None),
    ),
    "unsent_postcard": (
        ("root", 0, "atomic", (), "constant", (), "always_true", None),
    ),
}


def label_block(source, label):
    match = re.search(
        r"^label {}:\n(?P<body>.*?)(?=^label |\Z)".format(label),
        source,
        re.MULTILINE | re.DOTALL,
    )
    if match is None:
        raise AssertionError("missing label: {}".format(label))
    return match.group("body")


def manifest_hash(content_lock, source_name):
    pattern = (
        r"\| `{}` \|.*?\|\s*\d+\s*\|\s*`([0-9a-fA-F]{{64}})`\s*\|"
    ).format(re.escape(source_name))
    match = re.search(pattern, content_lock)
    if match is None:
        raise AssertionError("missing content-lock source: {}".format(source_name))
    return match.group(1).lower()


class RainStopsTailTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.endings = ENDINGS_SOURCE.read_text(encoding="utf-8")
        cls.ending_rules = ENDING_RULES_SOURCE.read_text(encoding="utf-8")
        cls.state = STATE_SOURCE.read_text(encoding="utf-8")
        cls.day7 = DAY7_SOURCE.read_text(encoding="utf-8")
        cls.baseline = BASELINE.read_text(encoding="utf-8")
        cls.content_lock = CONTENT_LOCK.read_text(encoding="utf-8")
        cls.epilogue = label_block(cls.endings, "epilogue_rain_stops_arcade")
        cls.tail = cls.epilogue.split(
            "# story_025_tail_observer: ordinary neighborhood view, no named reunion.",
            1,
        )[1].split("    return", 1)[0]

    def test_frozen_production_units_and_ending_contracts_are_unchanged(self):
        units_section = self.baseline.split("## Canonical Production Units", 1)[1].split(
            "## Character Constraint Catalog", 1
        )[0]
        units = tuple(re.findall(r"^\d+\. `([^`]+)`$", units_section, re.MULTILINE))
        self.assertEqual(EXPECTED_UNITS, units)

        priority_section = self.ending_rules.split("ENDING_PRIORITY = (", 1)[1].split(")", 1)[0]
        self.assertEqual(EXPECTED_ENDINGS, tuple(re.findall(r'"([^\"]+)"', priority_section)))
        label_items = self.state.split("_ENDING_LABEL_MAP_ITEMS = (", 1)[1].split("\n    )", 1)[0]
        actual_labels = tuple(re.findall(r'\("([^\"]+)",\s*"([^\"]+)"\)', label_items))
        self.assertEqual(EXPECTED_LABELS, actual_labels)

        axes_section = self.ending_rules.split("AXES = (", 1)[1].split(")", 1)[0]
        self.assertEqual(EXPECTED_AXES, tuple(re.findall(r'"([^\"]+)"', axes_section)))
        for token_id in EXPECTED_TOKENS:
            self.assertIn("`{}`".format(token_id), self.baseline)
        for qualification_id in EXPECTED_QUALIFICATIONS:
            self.assertIn("`{}`".format(qualification_id), self.baseline)
        for ending_id in EXPECTED_ENDINGS:
            self.assertIn("witness_{}_v1".format(ending_id), self.baseline)
        self.assertIn("def resolve_ending_record", self.ending_rules)
        self.assertEqual(1, self.day7.count("jump day7_resolve_ending"))

        ending_blocks = [label_block(self.endings, "ending_{}".format(ending_id)) for ending_id in EXPECTED_ENDINGS]
        self.assertEqual(6, sum(block.count("commit_ending_completion") for block in ending_blocks))
        self.assertEqual(6, self.endings.count("commit_ending_completion"))
        self.assertNotIn("commit_ending_completion", self.epilogue)

    def test_frozen_tokens_qualifications_predicates_and_witnesses_are_exact(self):
        self.assertEqual(AXES, EXPECTED_AXES)
        self.assertEqual(tuple(ENDING_PRIORITY), EXPECTED_ENDINGS)
        self.assertEqual(dict(_TOKEN_DOMAINS), EXPECTED_TOKEN_DOMAINS)
        self.assertEqual(_QUALIFICATION_BINDINGS, EXPECTED_QUALIFICATION_BINDINGS)

        for ending_id in EXPECTED_ENDINGS:
            actual = tuple(
                (
                    record.clause_id.removeprefix(ending_id + "_"),
                    record.clause_order,
                    record.clause_kind,
                    record.operand_clause_ids,
                    record.source_kind,
                    record.source_reference_ids,
                    record.comparator,
                    record.expected_int,
                )
                for record in _PREDICATE_CLAUSE_RECORDS
                if record.ending_id == ending_id
            )
            self.assertEqual(EXPECTED_PREDICATE_SHAPES[ending_id], actual)

            history, axes = WITNESSES[ending_id]
            row = next(
                line
                for line in self.baseline.splitlines()
                if "`witness_{}_v1`".format(ending_id) in line
            )
            self.assertIn(" → ".join(history), row)
            self.assertIn("`{}/{}/{}/{}/{}`".format(*axes), row)
            self.assertIn("/ `{}`".format(ending_id), row)

    def test_rain_only_epilogue_and_lights_out_completion_order_remain_unique(self):
        ending_blocks = {
            ending_id: label_block(self.endings, "ending_{}".format(ending_id))
            for ending_id in EXPECTED_ENDINGS
        }
        self.assertEqual(1, ending_blocks["rain_stops"].count("jump epilogue_rain_stops_arcade"))
        for ending_id in EXPECTED_ENDINGS[1:]:
            self.assertNotIn("epilogue_rain_stops_arcade", ending_blocks[ending_id])
        self.assertEqual(1, self.endings.count("jump epilogue_rain_stops_arcade"))

        self.assertEqual(1, self.epilogue.count("event_epilogue_first_guest_completed = True"))
        self.assertEqual(1, self.epilogue.count("event_epilogue_lights_out_completed = True"))
        self.assertEqual(1, self.epilogue.count("cp_epilogue_first_guest_complete = True"))
        self.assertEqual(1, self.epilogue.count("cp_epilogue_lights_out_complete = True"))
        first_guest = self.epilogue.index("event_epilogue_first_guest_completed = True")
        lights_out = self.epilogue.index("event_epilogue_lights_out_completed = True")
        tail_start = self.epilogue.index("# story_025_tail_observer")
        self.assertLess(first_guest, lights_out)
        self.assertLess(lights_out, tail_start)

    def test_tail_has_both_approved_viewpoints_and_no_erii_spoken_line(self):
        self.assertIn("【普通街坊观察】", self.tail)
        self.assertIn("不具名的旧友", self.tail)
        self.assertIn("普通顾客", self.tail)
        self.assertIn("【绘梨衣的书面手记】", self.tail)
        self.assertRegex(self.tail, re.compile(r"【绘梨衣的书面手记】.*手记", re.DOTALL))
        self.assertNotRegex(self.tail, r"^\s*erii\s+", re.MULTILINE)
        self.assertNotIn('erii "', self.tail.lower())
        self.assertTrue(all("narrator " in line or line.strip().startswith("#") or not line.strip() for line in self.tail.splitlines()))

    def test_tail_adds_no_state_choice_asset_or_new_canonical_identifiers(self):
        self.assertNotRegex(self.tail, r"^\s*(\$|default |label |menu:|call |jump )", re.MULTILINE)
        self.assertNotRegex(self.tail, r"\b(scene|show|hide|image)\s+[a-zA-Z_]" )
        self.assertNotRegex(self.tail, r"(?:asset|assets|images?|audio|music|voice|ui)/")
        for forbidden in (
            "choice_",
            "route_",
            "ending_",
            "achievement",
            "Gallery",
            "persistent",
            "axis",
            "token",
            "resource",
            "qualification",
            "resolver",
            "event_",
            "canonical",
        ):
            self.assertNotIn(forbidden.lower(), self.tail.lower())
        self.assertNotIn("event_epilogue_lights_out_completed = True", self.tail)

    def test_tail_does_not_confirm_forbidden_extra_world_states(self):
        for marker in FORBIDDEN_WORLD_STATE_MARKERS:
            self.assertNotIn(marker, self.tail)
        self.assertNotRegex(self.tail.lower(), r"\b(pregnan|twins|family conversion)\w*")

    def test_content_lock_hashes_are_valid_and_baseline_is_current(self):
        endings_hash = manifest_hash(self.content_lock, "game/chapters/endings.rpy")
        baseline_hash = manifest_hash(self.content_lock, "design/narrative/seven-day-content-baseline.md")
        self.assertRegex(endings_hash, r"^[0-9a-f]{64}$")
        self.assertRegex(baseline_hash, r"^[0-9a-f]{64}$")
        self.assertEqual(hashlib.sha256(BASELINE.read_bytes()).hexdigest(), baseline_hash)
        self.assertEqual(hashlib.sha256(ENDINGS_SOURCE.read_bytes()).hexdigest(), endings_hash)
        self.assertIn("content_lock:player_visible:v3:2026-08-14", self.content_lock)


if __name__ == "__main__":
    unittest.main()
