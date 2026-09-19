import hashlib
import json
import re
import unittest
from pathlib import Path

from game.modules.production_closeout import BLOCKED_INPUT, ExternalEvidence, classify_external_evidence


ROOT = Path(__file__).resolve().parents[3]
SCREENS = ROOT / "game" / "screens.rpy"
OPTIONS = ROOT / "game" / "options.rpy"
LOCK = ROOT / "design" / "content-lock.md"
SAPI_PREFLIGHT = ROOT / "production" / "qa" / "evidence" / "sprint-013-n13-05-2026-08-15" / "accessibility-automated-current" / "run" / "sapi-preflight.json"
TRANSCRIPT = SAPI_PREFLIGHT.with_name("transcript-log.txt")
LOCK_ROW = re.compile(r"\| `([^`]+)` \|[^|]*\| (\d+) \| `([0-9a-f]{64})` \|")


class Sprint013SapiTranscriptTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.screens = SCREENS.read_text(encoding="utf-8")
        cls.options = OPTIONS.read_text(encoding="utf-8")
        cls.lock = LOCK.read_text(encoding="utf-8")

    def test_self_voicing_switch_is_player_setting_and_not_action_dispatch(self):
        self.assertIn('Preference("self voicing", "toggle")', self.screens)
        self.assertNotIn("self_voicing_action", self.screens)
        self.assertNotIn("self_voicing_action", self.options)

    def test_current_capability_preflight_exists_and_is_parseable(self):
        self.assertTrue(SAPI_PREFLIGHT.exists(), "current SAPI preflight is missing")
        payload = json.loads(SAPI_PREFLIGHT.read_text(encoding="utf-8-sig"))
        self.assertIsInstance(payload, dict)
        self.assertIn("voice_count", payload)
        self.assertGreaterEqual(payload["voice_count"], 1)
        self.assertIn("voice_descriptions", payload)

    def test_real_transcript_is_required_and_not_replaced_by_capability_enumeration(self):
        self.assertEqual(
            BLOCKED_INPUT,
            classify_external_evidence(ExternalEvidence("raw SAPI transcript", TRANSCRIPT.exists())),
        )
        self.assertFalse(TRANSCRIPT.exists())

    def test_current_lock_identity_is_required_for_transcript_generation(self):
        drift = []
        for path_text, locked_lines, locked_hash in LOCK_ROW.findall(self.lock):
            path = ROOT / Path(path_text)
            actual_lines = len(path.read_text(encoding="utf-8").splitlines())
            actual_hash = hashlib.sha256(path.read_bytes()).hexdigest()
            if actual_lines != int(locked_lines) or actual_hash != locked_hash:
                drift.append(path_text)
        self.assertEqual([], drift, "transcript generation blocked by content-lock drift: {}".format(drift))


if __name__ == "__main__":
    unittest.main()
