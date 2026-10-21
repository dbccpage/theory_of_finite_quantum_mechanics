"""Recompute every recoverable claim of the recovered Authorization-Incompleteness corpus.

Run from the repository root:  python -I -X utf8 papers/foundations/authorization_incompleteness/evidence/tools/recompute.py
It writes evidence/replay_results/recompute_report.json and prints a one-line verdict per check.

Nothing here executes the recovered PowerShell. The checks are:
  1. SHA-256 of every recovered file listed in formal_binding_manifest.md and in packet_manifest.json;
  2. the Python port of the replay packet (verified, terminal open, countertraces, control-only inadequate);
  3. the Python port of the carrier-candidate validator (non-strict: lists unrecovered evidence);
  4. the ported Lean axiom report (evidence/axiom_reports/ported_axioms.json) against the axiom ceilings
     recorded in the source README / manifest.

AuthorityEffect: None
"""

from __future__ import annotations

import hashlib
import importlib
import json
import re
import sys
import types
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
EVIDENCE = REPO / "papers/foundations/authorization_incompleteness/evidence"
pkg = types.ModuleType("staged_auth_incompleteness")
pkg.__path__ = [str(REPO / "code/python/src/qm/auth_incompleteness")]
sys.modules[pkg.__name__] = pkg
rp = importlib.import_module("staged_auth_incompleteness.replay_packet")
cc = importlib.import_module("staged_auth_incompleteness.carrier_candidates")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def hash_checks() -> list[dict]:
    text = (EVIDENCE / "original/formal_binding_manifest.md").read_text(encoding="utf-8")
    rows = []
    for m in re.finditer(r"\| `([^`]+)` \| `([0-9a-f]{64})` \|", text):
        rel, recorded = m.groups()
        local = EVIDENCE / ("reconstructed/lean-toolchain" if rel == "lean4/genx/lean-toolchain" else "original/" + rel)
        if not local.is_file():
            rows.append({"object": rel, "recorded": recorded, "status": "not_recovered"})
        else:
            actual = sha(local)
            rows.append({"object": rel, "recorded": recorded, "actual": actual, "status": ("match_reconstructed" if "reconstructed" in str(local) else "match") if actual == recorded else "MISMATCH"})
    return rows


CEILING_NONE = {
    "blank_symbol_is_not_option_absence", "write_and_halt_transition_writes_mark",
    "write_and_halt_transition_reaches_declared_halt", "decodeTapeSymbol_encodeTapeSymbol", "decodeMove_encodeMove",
    "closed_two_sided_terminalization_is_acceptance_complete",
}
PROPEXT_MODULES = ("DirectTuringMachineModels", "DirectTuringMachineTokenCodeModels", "TerminalAuthorizationBoundary")


def axiom_checks() -> dict:
    data = json.loads((EVIDENCE / "axiom_reports/ported_axioms.json").read_text(encoding="utf-8"))
    bad = []
    for entry in data["entries"]:
        name = entry["declaration"]
        short = name.rsplit(".", 1)[-1]
        in_propext_module = any(f".{m}." in name for m in PROPEXT_MODULES)
        expected = "propext" if (in_propext_module and short not in CEILING_NONE) else "none"
        if entry["axioms"] != expected:
            bad.append({"declaration": name, "got": entry["axioms"], "recorded_ceiling": expected})
    return {"declarations": data["count"], "deviations_from_recorded_ceilings": bad}


def main() -> int:
    report: dict = {"produced": "2026-10-21", "hash_checks": hash_checks()}
    packet = rp.verify(REPO)
    report["packet_replay"] = {
        "status": packet["verification_status"],
        "terminal": packet["terminal"],
        "control_only_authorization": packet["evaluation"]["control_only_authorization"],
        "marked_countertraces": [c["source"] for c in packet["evaluation"]["marked_countertraces"]],
        "control_only_counterexample": packet["evaluation"]["control_only_counterexample"],
    }
    record = cc.load_record(REPO / rp.map_path(cc.RECORD_RELATIVE, rp.PREFIX_MAP))
    report["carrier_candidates"] = cc.validate_record(record, cc.default_exists(REPO), strict=False)
    report["axioms"] = axiom_checks()
    out = EVIDENCE / "replay_results"
    out.mkdir(exist_ok=True)
    (out / "recompute_report.json").write_text(json.dumps(report, indent=1) + "\n", encoding="utf-8", newline="\n")
    h = report["hash_checks"]
    print("hashes: match", sum(r["status"].startswith("match") for r in h), "mismatch", sum(r["status"] == "MISMATCH" for r in h),
          "not_recovered", sum(r["status"] == "not_recovered" for r in h))
    print("packet:", report["packet_replay"]["status"], report["packet_replay"]["terminal"])
    print("candidates:", len(report["carrier_candidates"]["candidates"]), "unresolved evidence",
          len(report["carrier_candidates"]["unresolved_evidence"]))
    print("axioms: declarations", report["axioms"]["declarations"], "deviations", len(report["axioms"]["deviations_from_recorded_ceilings"]))
    ok = not any(r["status"] == "MISMATCH" for r in h) and packet["verification_status"] == "verified" and not report["axioms"]["deviations_from_recorded_ceilings"]
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
