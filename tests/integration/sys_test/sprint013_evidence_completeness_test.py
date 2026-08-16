import re
import subprocess
import unittest
from pathlib import Path

from game.modules.production_closeout import BLOCKED_INPUT, ExternalEvidence, classify_external_evidence


ROOT = Path(__file__).resolve().parents[3]
EVIDENCE_ROOT = ROOT / "production" / "qa" / "evidence"
RELEASES = ROOT / "production" / "releases"
STATUS = ROOT / "production" / "sprint-status.yaml"


class Sprint013EvidenceCompletenessTests(unittest.TestCase):
    def test_each_work_package_has_current_raw_hash_status_and_qa_records(self):
        missing = []
        for package_no in range(1, 13):
            package = EVIDENCE_ROOT / f"sprint-013-n13-{package_no:02d}-2026-08-15"
            raw_files = list(package.rglob("*.stdout.txt")) + list(package.rglob("stdout.txt"))
            hash_files = list(package.rglob("*hash*.tsv")) + list(package.rglob("source-hashes.tsv"))
            if not package.exists() or not (package / "record.md").exists() or not raw_files or not hash_files:
                missing.append(f"N13-{package_no:02d}")
        self.assertEqual([], missing, f"missing current evidence components: {missing}")

    def test_all_evidence_binds_to_one_nonempty_candidate_identity(self):
        identities = set()
        for package in sorted(EVIDENCE_ROOT.glob("sprint-013-n13-*-2026-08-15")):
            for document in package.rglob("*.md"):
                text = document.read_text(encoding="utf-8", errors="replace")
                identities.update(re.findall(r"candidate_identity:\s*`?([0-9a-f]{64})`?", text, re.IGNORECASE))
        self.assertEqual(
            BLOCKED_INPUT,
            classify_external_evidence(ExternalEvidence("human evidence candidate binding", len(identities) == 1)),
        )
        self.assertEqual(0, len(identities))

    def test_current_release_archive_and_exclusion_reports_exist(self):
        present = RELEASES.exists() and bool(tuple(RELEASES.rglob("*.zip"))) and bool(tuple(RELEASES.rglob("*exclusion*")))
        self.assertEqual(
            BLOCKED_INPUT,
            classify_external_evidence(ExternalEvidence("current archive exclusion evidence", present)),
        )
        self.assertFalse(present)

    def test_required_manual_evidence_is_complete_and_unblocked(self):
        dossier = ROOT / "production" / "session-logs" / "playtest-sprint-013-n13-08.md"
        transcript = ROOT / "production" / "qa" / "evidence" / "sprint-013-n13-06-2026-08-15" / "transcript-log.txt"
        complete = (
            dossier.exists()
            and transcript.exists()
            and "BLOCKED_INPUT" not in dossier.read_text(encoding="utf-8")
            and "N13-08" not in STATUS.read_text(encoding="utf-8")
        )
        self.assertEqual(
            BLOCKED_INPUT,
            classify_external_evidence(ExternalEvidence("current manual evidence", complete)),
        )
        self.assertIn("BLOCKED_INPUT", dossier.read_text(encoding="utf-8"))

    def test_formal_asset_scope_has_no_worktree_changes(self):
        result = subprocess.run(
            ["git", "diff", "--name-only", "--", "game/assets", "game/assets/"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertEqual("", result.stdout.strip(), "formal asset paths changed")


if __name__ == "__main__":
    unittest.main()
