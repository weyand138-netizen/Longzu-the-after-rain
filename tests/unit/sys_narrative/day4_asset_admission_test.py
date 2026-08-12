import hashlib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
DAY4_SOURCE = ROOT / "game" / "chapters" / "day4.rpy"
RESOURCE_SOURCE = ROOT / "game" / "00_resources.rpy"
SCREEN_SOURCE = ROOT / "game" / "screens.rpy"
FONT = ROOT / "game" / "assets" / "fonts" / "SourceHanSansLite.ttf"
INVENTORY = ROOT / "design" / "assets" / "entity-inventory.md"
LEGAL_REGISTER = ROOT / "docs" / "legal" / "asset-register.md"


class Day4AssetAdmissionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.day4_source = DAY4_SOURCE.read_text(encoding="utf-8")
        cls.inventory = INVENTORY.read_text(encoding="utf-8")
        cls.legal_register = LEGAL_REGISTER.read_text(encoding="utf-8")

    def test_day4_runtime_references_only_admitted_reused_assets(self):
        self.assertEqual(("scene bg warm_room",), tuple(
            line.strip()
            for line in self.day4_source.splitlines()
            if line.lstrip().startswith(("scene ", "show ", "play "))
        ))
        self.assertIn('image bg warm_room = Solid("#4a3840")', RESOURCE_SOURCE.read_text(encoding="utf-8"))
        self.assertIn('id "quick_menu_root"', SCREEN_SOURCE.read_text(encoding="utf-8"))

    def test_reused_asset_hashes_match_the_admission_records(self):
        expected_hashes = {
            "FONT-SOURCEHAN-LITE-P0": hashlib.sha256(FONT.read_bytes()).hexdigest(),
            "RUNTIME-SOLID-DAY1-WARM-ROOM": hashlib.sha256(RESOURCE_SOURCE.read_bytes()).hexdigest(),
            "RUNTIME-UI-DAY1-CHOICE-SURFACE": hashlib.sha256(SCREEN_SOURCE.read_bytes()).hexdigest(),
        }
        for asset_id, asset_hash in expected_hashes.items():
            self.assertIn(asset_id, self.inventory)
            self.assertIn(asset_id, self.legal_register)
            self.assertIn(asset_hash, self.inventory)
            self.assertIn(asset_hash, self.legal_register)

    def test_day4_admission_records_preserve_semantic_and_scope_boundaries(self):
        for record in (self.inventory, self.legal_register):
            self.assertIn("Day 4", record)
            self.assertIn("a11y.day4.text-and-choice-copy", record)
            self.assertIn("a11y.day4.warm-room-decorative", record)
            self.assertIn("a11y.day4.choice-surface", record)
            self.assertIn("No Day 4 image, audio, video, character art, CG, prop", record)
        self.assertNotIn("image ", self.day4_source)
        self.assertNotIn("play audio", self.day4_source)
        self.assertNotIn("play music", self.day4_source)


if __name__ == "__main__":
    unittest.main()
