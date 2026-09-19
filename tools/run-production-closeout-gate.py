"""Explicit Production RC closeout gate runner.

Normal regression discovery never invokes this runner. Run it deliberately
with ``--final`` when the external evidence boundary should produce a gate
verdict. Missing playtest, transcript, semantic review, performance samples,
DOCX/owner input, or archive evidence is therefore non-PASS only here.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from game.modules.production_closeout import (
    BLOCKED_INPUT,
    ExternalEvidence,
    PASS,
    REPORT_ONLY,
    classify_external_evidence,
    final_gate_status,
)


PREFLIGHT = ROOT / "production" / "preflight"
REPORT = ROOT / "production" / "gate-checks" / f"production-closeout-{date.today().isoformat()}.md"
LOCK = ROOT / "design" / "content-lock.md"
LOCK_ROW = re.compile(r"\| `([^`]+)` \|[^|]*\| (\d+) \| `([0-9a-f]{64})` \|")
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


def _source_lock_status() -> ExternalEvidence:
    drift = []
    text = LOCK.read_text(encoding="utf-8")
    for path_text, locked_lines, locked_hash in LOCK_ROW.findall(text):
        path = ROOT / Path(path_text)
        if not path.exists():
            drift.append(f"{path_text}:MISSING")
            continue
        actual_lines = len(path.read_text(encoding="utf-8").splitlines())
        actual_hash = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual_lines != int(locked_lines) or actual_hash != locked_hash:
            drift.append(f"{path_text}:DRIFT")
    return ExternalEvidence("content-lock/source identity", not drift)


def _candidate_status() -> ExternalEvidence:
    path = PREFLIGHT / "candidate-manifest-v1.json"
    flow_path = PREFLIGHT / "narrative-flow-manifest-v1.json"
    if not path.exists() or not flow_path.exists():
        return ExternalEvidence("candidate manifest", False)
    payload = json.loads(path.read_text(encoding="utf-8"))
    flow = json.loads(flow_path.read_text(encoding="utf-8"))
    identity = payload.get("candidate_identity", "")
    identity_payload = {
        "candidate_manifest": payload.get("candidate_manifest"),
        "candidate_type": payload.get("candidate_type"),
        "release_candidate": payload.get("release_candidate"),
        "source_head": payload.get("source_head"),
        "content_lock": payload.get("content_lock"),
        "narrative_flow_manifest": payload.get("narrative_flow_manifest"),
        "canonical_units": flow.get("canonical_units"),
        "source_hashes": payload.get("source_hashes"),
    }
    recomputed = hashlib.sha256(
        json.dumps(identity_payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    valid = (
        bool(re.fullmatch(r"[0-9a-f]{64}", identity))
        and payload.get("release_candidate") is False
        and identity == recomputed
    )
    return ExternalEvidence("preflight candidate identity", valid)


def _flow_manifest_status() -> ExternalEvidence:
    path = PREFLIGHT / "narrative-flow-manifest-v1.json"
    if not path.exists():
        return ExternalEvidence("complete narrative flow manifest", False)
    payload = json.loads(path.read_text(encoding="utf-8"))
    candidate_path = PREFLIGHT / "candidate-manifest-v1.json"
    if not candidate_path.exists():
        return ExternalEvidence("complete narrative flow manifest", False)
    candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
    units = payload.get("canonical_units", [])
    valid = (
        payload.get("manifest_id") == "narrative_flow_manifest:v1"
        and tuple(item.get("id") for item in units) == EXPECTED_UNITS
        and payload.get("partial_manifest_admitted") is False
    )
    valid = valid and payload.get("candidate_identity") == candidate.get("candidate_identity")
    return ExternalEvidence("complete narrative flow manifest", valid)


def _required_external_evidence() -> tuple[ExternalEvidence, ...]:
    return (
        ExternalEvidence("clean player seven-day run", False),
        ExternalEvidence("six human ending witnesses", False),
        ExternalEvidence("raw SAPI transcript and listening review", False),
        ExternalEvidence("semantic-equivalence adjudication", False),
        ExternalEvidence("player comprehension dossier", False),
        ExternalEvidence("DOCX provenance and owner decision", False),
        ExternalEvidence("current target-hardware performance samples", False, report_only=True),
        ExternalEvidence("staging/archive and exclusion reports", False),
    )


def build_result() -> tuple[str, list[ExternalEvidence]]:
    evidence = [_source_lock_status(), _candidate_status(), _flow_manifest_status()]
    evidence.extend(_required_external_evidence())
    return final_gate_status(tuple(evidence)), evidence


def render_report(status: str, evidence: list[ExternalEvidence]) -> str:
    rows = []
    for item in evidence:
        item_status = classify_external_evidence(item)
        rows.append(f"| {item.name} | {item_status} | {'yes' if item.present else 'no'} |")
    return "\n".join(
        [
            f"# Production RC Closeout Gate — {date.today().isoformat()}",
            "",
            "> Explicit final gate runner only. This report is not the Sprint 013 ordinary regression baseline.",
            "> It does not create, admit, or package formal game assets and never updates `production/stage.txt`.",
            "",
            f"- Candidate type: `non-formal-asset-automation-preflight`",
            f"- Candidate manifest: `{(PREFLIGHT / 'candidate-manifest-v1.json').relative_to(ROOT).as_posix()}`",
            f"- Final gate status: **{status}**",
            "- `REPORT_ONLY` performance protocol is retained as non-PASS until current target-hardware samples exist.",
            "",
            "## Evidence classification",
            "",
            "| Check | Status | Present |",
            "|---|---|---|",
            *rows,
            "",
            "## Boundary",
            "",
            "Missing playtest, transcript, semantic review, DOCX/owner input, performance samples and archive evidence remain external RC inputs. They are not deleted, skipped, downgraded, or promoted to PASS by the preflight suite.",
            "",
            "`production/stage.txt` remains `Production`.",
            "",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--final", action="store_true", help="run the external-evidence closeout gate")
    parser.add_argument("--output", type=Path, default=REPORT)
    args = parser.parse_args()
    status, evidence = build_result()
    if not args.final:
        print("Preflight classification available. Re-run with --final to produce a non-PASS closeout verdict.")
        for item in evidence:
            print(f"{classify_external_evidence(item)}\t{item.name}")
        return 0
    output = args.output if args.output.is_absolute() else ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_report(status, evidence), encoding="utf-8")
    print(render_report(status, evidence), end="")
    return 0 if status == PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
