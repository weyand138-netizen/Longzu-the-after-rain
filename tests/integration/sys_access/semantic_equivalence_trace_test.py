import hashlib
import unittest
from pathlib import Path

from game.modules.production_closeout import BLOCKED_INPUT, ExternalEvidence, classify_external_evidence


ROOT = Path(__file__).resolve().parents[3]
AUTOMATED_RUN = ROOT / "production" / "qa" / "evidence" / "sprint-013-n13-05-2026-08-15" / "accessibility-automated-current" / "run"
PAIRED_DIR = ROOT / "production" / "qa" / "evidence" / "sprint-013-n13-07-2026-08-15" / "paired"
TRANSCRIPT = ROOT / "production" / "qa" / "evidence" / "sprint-013-n13-06-2026-08-15" / "transcript-log.txt"


class SemanticEquivalenceTraceTests(unittest.TestCase):
    def test_automated_run_is_not_accepted_as_paired_human_evidence(self):
        self.assertTrue(AUTOMATED_RUN.exists())
        self.assertFalse(PAIRED_DIR.exists(), "paired evidence must be supplied by an independent reviewer")

    def test_paired_review_requires_current_raw_channels_and_transcript(self):
        self.assertEqual(
            BLOCKED_INPUT,
            classify_external_evidence(ExternalEvidence("paired semantic review", PAIRED_DIR.exists() and TRANSCRIPT.exists())),
        )
        self.assertFalse(PAIRED_DIR.exists())
        self.assertFalse(TRANSCRIPT.exists())


if __name__ == "__main__":
    unittest.main()
