"""S7-03 source-contract tests for frozen ending closures and epilogue."""

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SOURCE_PATH = ROOT / "game" / "chapters" / "endings.rpy"

ENDING_IDS = (
    "rain_stops",
    "her_own_name",
    "see_the_sea",
    "one_person_train",
    "golden_cage",
    "unsent_postcard",
)

REQUIRED_CLOSURE_ANCHORS = {
    "rain_stops": ("旧身份", "自己的名字", "普通的一天"),
    "her_own_name": ("联系人卡", "自己名字", "保留一条"),
    "see_the_sea": ("两张靠窗的票", "旧身份", "共同承担"),
    "one_person_train": ("单人票", "失去可以站立", "独自"),
    "golden_cage": ("安全的方案", "旧秩序", "笼子"),
    "unsent_postcard": ("没有一条还能执行的路线", "没有寄出的明信片", "完整的后果"),
}


class EndingClosureSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = SOURCE_PATH.read_text(encoding="utf-8")
        cls.labels = {
            match.group("name"): match.group("body")
            for match in re.finditer(
                r"^label (?P<name>[a-z0-9_]+):\n(?P<body>.*?)(?=^label |\Z)",
                cls.source,
                re.MULTILINE | re.DOTALL,
            )
        }

    def test_exact_stable_labels_are_real_and_no_extra_ending_selector_exists(self):
        self.assertEqual(
            {"ending_" + ending_id for ending_id in ENDING_IDS}
            | {"epilogue_rain_stops_arcade"},
            set(self.labels),
        )
        self.assertNotIn("resolve_ending", self.source)
        self.assertNotIn("ENDING_LABEL_MAP", self.source)
        self.assertNotIn("apply_choice", self.source)
        self.assertNotIn("has_unresolved_token", self.source)
        self.assertNotIn("persistent.sys_persist_state", self.source)

    def test_each_closure_enters_before_visible_text_and_completes_once(self):
        for ending_id in ENDING_IDS:
            with self.subTest(ending_id=ending_id):
                body = self.labels["ending_" + ending_id]
                significant = [
                    line.strip()
                    for line in body.splitlines()
                    if line.strip() and not line.lstrip().startswith("#")
                ]
                self.assertEqual(
                    '$ commit_ending_entry("{}")'.format(ending_id),
                    significant[0],
                )
                completion = '$ commit_ending_completion("{}", "ending.{}.completion")'.format(
                    ending_id,
                    ending_id,
                )
                self.assertEqual(1, body.count(completion))
                self.assertGreater(body.index("narrator "), body.index(significant[0]))
                self.assertGreater(body.index(completion), body.index("narrator "))
                self.assertEqual(
                    REQUIRED_CLOSURE_ANCHORS[ending_id],
                    tuple(anchor for anchor in REQUIRED_CLOSURE_ANCHORS[ending_id] if anchor in body),
                )

    def test_only_rain_stops_transitions_to_the_epilogue_after_completion(self):
        rain = self.labels["ending_rain_stops"]
        completion = '$ commit_ending_completion("rain_stops", "ending.rain_stops.completion")'
        self.assertIn("jump epilogue_rain_stops_arcade", rain)
        self.assertGreater(rain.index("jump epilogue_rain_stops_arcade"), rain.index(completion))
        for ending_id in ENDING_IDS[1:]:
            self.assertNotIn("epilogue_rain_stops_arcade", self.labels["ending_" + ending_id])

    def test_epilogue_has_the_frozen_ordinary_future_echo_and_unique_events(self):
        epilogue = self.labels["epilogue_rain_stops_arcade"]
        for required in (
            "第二枚游戏币",
            "昵称",
            "今天第一位客人的预约",
            "event_epilogue_first_guest_completed = True",
            "cp_epilogue_first_guest_complete = True",
            "关灯",
            "event_epilogue_lights_out_completed = True",
            "cp_epilogue_lights_out_complete = True",
        ):
            self.assertIn(required, epilogue)
        self.assertEqual(
            1,
            self.source.count("$ event_epilogue_first_guest_completed = True"),
        )
        self.assertEqual(
            1,
            self.source.count("$ event_epilogue_lights_out_completed = True"),
        )
        self.assertLess(
            epilogue.index("今天第一位客人的预约"),
            epilogue.index("event_epilogue_first_guest_completed = True"),
        )
        self.assertLess(
            epilogue.index("关灯"),
            epilogue.index("event_epilogue_lights_out_completed = True"),
        )

    def test_only_existing_code_defined_presentation_primitives_are_used(self):
        self.assertEqual(7, self.source.count("scene bg warm_room"))
        active_lines = "\n".join(
            line for line in self.source.splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        )
        for forbidden in ("image ", "show ", "play ", "movie ", "with ", "menu:"):
            self.assertNotIn(forbidden, active_lines)


if __name__ == "__main__":
    unittest.main()
