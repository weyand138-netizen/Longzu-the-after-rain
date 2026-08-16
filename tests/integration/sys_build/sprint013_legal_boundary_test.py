import unittest
from pathlib import Path

from game.modules.production_closeout import BLOCKED_INPUT, ExternalEvidence, classify_external_evidence


ROOT = Path(__file__).resolve().parents[3]
DOCS = ROOT / "docs"
DOCX = Path(r"C:\Users\Andwey\Downloads\好结局剧本标注版.docx")
REGISTER = DOCS / "legal" / "asset-register.md"
NOTICE = DOCS / "legal" / "fan-work-notice.md"
DECISION = ROOT / "production" / "qa" / "evidence" / "sprint-013-n13-10-2026-08-15" / "copyright-boundary.md"


class Sprint013LegalBoundaryTests(unittest.TestCase):
    def test_actual_docx_reference_is_present_for_provenance_review(self):
        self.assertEqual(
            BLOCKED_INPUT,
            classify_external_evidence(ExternalEvidence("DOCX provenance input", DOCX.exists())),
        )
        self.assertFalse(DOCX.exists())

    def test_owner_boundary_decision_is_closed_without_blocker(self):
        self.assertTrue(DECISION.exists(), "current copyright boundary record is missing")
        text = DECISION.read_text(encoding="utf-8")
        self.assertIn("owner_decision:", text)
        self.assertEqual(
            BLOCKED_INPUT,
            classify_external_evidence(ExternalEvidence("DOCX owner boundary", "BLOCKED_INPUT" not in text)),
        )
        self.assertIn("BLOCKED_INPUT", text)

    def test_static_register_and_notice_preserve_formal_asset_exclusion(self):
        register = REGISTER.read_text(encoding="utf-8")
        notice = NOTICE.read_text(encoding="utf-8")
        self.assertIn("Not admitted", register)
        self.assertIn("Official", register)
        self.assertIn("不使用官方插画", notice)
        self.assertIn("非商业", notice)


if __name__ == "__main__":
    unittest.main()
