import hashlib
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
ACCESS = ROOT / "design" / "gdd" / "sys-access.md"
LOCK = ROOT / "design" / "content-lock.md"
LOCK_ROW = re.compile(r"\| `([^`]+)` \|[^|]*\| (\d+) \| `([0-9a-f]{64})` \|")


class SemanticEquivalenceContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.access = ACCESS.read_text(encoding="utf-8")
        cls.lock = LOCK.read_text(encoding="utf-8")

    def test_contract_requires_same_manifest_actions_outcomes_and_summary_identity(self):
        for marker in (
            "accessible_causal_summary_id",
            "same_manifest_identity",
            "canonical_choice_ids",
            "enabled_action_ids",
            "outcome_ids",
            "normalized_semantic_output_ids",
            "semantic_equivalence",
        ):
            self.assertIn(marker, self.access)

    def test_contract_forbids_hidden_state_substitution(self):
        for marker in ("不得暴露轴", "不得暴露", "preserve the source ambiguity"):
            self.assertIn(marker, self.access)

    def test_current_lock_identity_is_required_for_semantic_pairing(self):
        drift = []
        for path_text, locked_lines, locked_hash in LOCK_ROW.findall(self.lock):
            path = ROOT / Path(path_text)
            actual_lines = len(path.read_text(encoding="utf-8").splitlines())
            actual_hash = hashlib.sha256(path.read_bytes()).hexdigest()
            if actual_lines != int(locked_lines) or actual_hash != locked_hash:
                drift.append(path_text)
        self.assertEqual([], drift, "semantic pairing blocked by content-lock drift: {}".format(drift))


if __name__ == "__main__":
    unittest.main()
