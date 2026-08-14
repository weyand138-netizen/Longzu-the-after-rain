import hashlib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
DAY7_SOURCE = ROOT / "game" / "chapters" / "day7.rpy"
RESOURCE_SOURCE = ROOT / "game" / "00_resources.rpy"
SCREEN_SOURCE = ROOT / "game" / "screens.rpy"
FONT = ROOT / "game" / "assets" / "fonts" / "SourceHanSansLite.ttf"
INVENTORY = ROOT / "design" / "assets" / "entity-inventory.md"
LEGAL_REGISTER = ROOT / "docs" / "legal" / "asset-register.md"
EVIDENCE = ROOT / "production" / "qa" / "evidence" / "day7-asset-admission-2026-08-14.md"


class Day7AssetAdmissionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.day7_source = DAY7_SOURCE.read_text(encoding="utf-8")
        cls.inventory = INVENTORY.read_text(encoding="utf-8")
        cls.legal_register = LEGAL_REGISTER.read_text(encoding="utf-8")
        cls.evidence = EVIDENCE.read_text(encoding="utf-8")

    def test_day7_runtime_uses_only_the_admitted_text_and_warm_room_primitives(self):
        runtime_references = tuple(
            line.strip()
            for line in self.day7_source.splitlines()
            if line.lstrip().startswith(("scene ", "show ", "play "))
        )
        self.assertEqual(("scene bg warm_room",), runtime_references)
        self.assertIn('image bg warm_room = Solid("#4a3840")', RESOURCE_SOURCE.read_text(encoding="utf-8"))
        self.assertIn("screen say(who, what):", SCREEN_SOURCE.read_text(encoding="utf-8"))
        self.assertNotIn("menu:", self.day7_source)
        self.assertNotIn("image ", self.day7_source)
        self.assertNotIn("play audio", self.day7_source)
        self.assertNotIn("play music", self.day7_source)

    def test_day7_reused_primitive_hashes_match_inventory_and_legal_records(self):
        expected_hashes = {
            "FONT-SOURCEHAN-LITE-P0": hashlib.sha256(FONT.read_bytes()).hexdigest(),
            "RUNTIME-SOLID-DAY1-WARM-ROOM": hashlib.sha256(RESOURCE_SOURCE.read_bytes()).hexdigest(),
            "RUNTIME-UI-DAY1-CHOICE-SURFACE": hashlib.sha256(SCREEN_SOURCE.read_bytes()).hexdigest(),
        }
        for asset_id, asset_hash in expected_hashes.items():
            with self.subTest(asset_id=asset_id):
                self.assertIn(asset_id, self.inventory)
                self.assertIn(asset_id, self.legal_register)
                self.assertIn(asset_hash, self.inventory)
                self.assertIn(asset_hash, self.legal_register)

    def test_day7_records_bind_text_accessibility_and_explicitly_reject_unused_scope(self):
        for record in (self.inventory, self.legal_register, self.evidence):
            self.assertIn("Day 7", record)
            self.assertIn("a11y.day7.text-copy", record)
            self.assertIn("a11y.day7.warm-room-decorative", record)
            self.assertIn("a11y.day7.say-surface", record)
            self.assertIn("No Day 7 image, audio, video, character art, CG, prop", record)
        self.assertIn("no Day 7 `choice` surface", self.inventory)
        self.assertIn("no Day 7 `choice` surface", self.legal_register)


if __name__ == "__main__":
    unittest.main()
