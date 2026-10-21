"""Write code-companion contract/score/doc records for the recovered Authorization-Incompleteness sources.

Run from the repository root:  python -I -X utf8 papers/foundations/authorization_incompleteness/evidence/tools/companions.py
Records go through scripts/contract_scores.py (write_legacy), as for every other source in this repository.
The score record states plainly that no five-gate engineering assessment was performed.

AuthorityEffect: None
"""

from __future__ import annotations

import hashlib
import importlib.util
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[5]
spec = importlib.util.spec_from_file_location("contract_scores", ROOT / "scripts/contract_scores.py")
cs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cs)
EVIDENCE = "papers/foundations/authorization_incompleteness/evidence/README.md"

BOUND_LEAN = [
    "Finite models only; no Mathlib computability library is imported and no Turing-completeness, universality, halting, Rice or Goedel statement is made.",
    "Statements are those of the recovered 2026-08-21 sources; only module names and a provenance header changed.",
]
BOUND_PY = [
    "Bounded finite replay under the recovered manifest's own trust root; not custody, collision resistance or evaluator soundness.",
    "Ported from PowerShell that was read, never executed; the PowerShell 7.6.3 runtime pin is not checked.",
]

TARGETS = {
    "lean4/AuthIncompleteness.lean": ("Root module importing the ten built recovered finite authorization models.", BOUND_LEAN),
    "lean4/AuthIncompleteness/Core.lean": ("Report-adequacy core: a split report fiber blocks every total report-only Bool authorizer.", BOUND_LEAN),
    "lean4/AuthIncompleteness/DirectTM.lean": ("DTM0: finite left-biased rule list, total Int tape, fuel-bounded evaluator with halted/stuck/fuelExhausted.", BOUND_LEAN),
    "lean4/AuthIncompleteness/TokenCode.lean": ("DTM1: List Nat token grammar for DTM0 machines with an all-consuming decoder and decode-after-encode round trip.", BOUND_LEAN),
    "lean4/AuthIncompleteness/GlobalLift.lean": ("Class-relative transport of a no-total-decider premise through a validity-preserving reduction.", BOUND_LEAN),
    "lean4/AuthIncompleteness/Terminal.lean": ("Conditional terminalization consequence of a supplied class-relative no-decider premise.", BOUND_LEAN),
    "lean4/AuthIncompleteness/PDModels.lean": ("Finite Bool model of two authorization extensions over one primitive-difference analogue.", BOUND_LEAN),
    "lean4/AuthIncompleteness/Externality.lean": ("Finite Site-label model: physical separation is neither necessary nor sufficient for a bounded authorization.", BOUND_LEAN),
    "lean4/AuthIncompleteness/Replay.lean": ("Finite structural replay-binding model with trust root, receipt, replay and separate terminal policy.", BOUND_LEAN),
    "lean4/AuthIncompleteness/TapeControl.lean": ("Tiny tape-control model separating halt control, read tokens, content contract and policy.", BOUND_LEAN),
    "lean4/AuthIncompleteness/TapeTransition.lean": ("Four-configuration transition table with one preserved and one violated supplied Boolean contract.", BOUND_LEAN),
    "lean4/AuthIncompleteness/MathlibBridge.lean": ("NEW (not recovered): instantiates the GlobalLift transport with Mathlib Computable and ComputablePred.halting_problem.", ["Written during recovery, not part of the source folder; compiled with lean against the Mathlib build, not a lakefile root.", "Gives a no-computable-decider transport for halting only; no Rice instance."]),
    "lean4/AuthIncompleteness/PDBridge.lean": ("J011 quotient specialization of the report-factorization boundary; NOT BUILT here because J011 is absent.", BOUND_LEAN + ["Imports J011_minimal_publication, which is not in this repository; excluded from the lakefile roots."]),
    "code/python/src/qm/auth_incompleteness/__init__.py": ("Package marker for the recovered Authorization-Incompleteness code.", BOUND_PY),
    "code/python/src/qm/auth_incompleteness/replay_packet.py": ("Python port of the SHA-256 replay packet evaluator and verifier for the four-configuration transition table.", BOUND_PY),
    "code/python/src/qm/auth_incompleteness/carrier_candidates.py": ("Python port of the computability-carrier candidate validator that refuses premature selection or admission.", BOUND_PY),
    "code/python/src/qm/auth_incompleteness/finite_models.py": ("Executable twins of the DTM0 evaluator, DTM1 token code and the four-configuration transition table.", BOUND_PY + ["Not claimed equivalent to Mathlib Turing.TM0; fuel exhaustion is not non-halting."]),
    "code/python/tests/test_auth_incompleteness_replay_packet.py": ("Port of the 23-case PowerShell replay-packet corpus with 21 tamper mutations.", BOUND_PY),
    "code/python/tests/test_auth_incompleteness_candidates.py": ("Port of the six-case carrier-candidate corpus with five promotion mutations.", BOUND_PY),
    "code/python/tests/test_auth_incompleteness_finite_models.py": ("Fixture replay of the recovered Lean DTM0, DTM1 and transition-table facts against the Python twins.", BOUND_PY),
    "papers/foundations/authorization_incompleteness/evidence/tools/recompute.py": ("Recomputes SHA-256 bindings, the packet replay, the candidate gate and the ported axiom ceilings.", BOUND_PY),
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def symbols(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    pattern = r"^(?:def|class) (\w+)" if path.suffix == ".py" else r"^(?:noncomputable )?(?:theorem|def|inductive|structure|abbrev) ([\w.]+)"
    return sorted({m[1] for m in re.finditer(pattern, text, re.M)})


def dump(value) -> str:
    return yaml.safe_dump(value, sort_keys=False, allow_unicode=True, width=100)


def write(rel: str, purpose: str, boundaries: list[str]) -> str:
    path = ROOT / rel
    digest = sha(path)
    head = {"schema_id": "finite-qm.code-companion.v1", "subject": rel, "source_sha256": digest, "authority_effect": "None"}
    contract = {**head, "contract_urn": f"urn:finite-qm:authincomp:recovery:{digest[:20]}", "symbols": symbols(path),
                "owned_invariants": ["Only the literal definitions and declared bounded replay contract of this source are claimed.",
                                     "Source bytes and kernel or test receipts are retained; labels do not admit a mathematical or physical target."],
                "boundaries": boundaries, "evidence": [EVIDENCE]}
    score = {**head, "rubric": "SCORING.md v2.0.0 section1.4", "capability_level": None, "engineering_grade": None,
             "composite_score": None, "assessment_status": "formal_scoring_not_performed",
             "gates": {g: {"grade": None, "status": "formal_scoring_not_performed"} for g in ("G1", "G2", "G3", "G4", "G5")},
             "refusal_reason": "A five-gate engineering-grade assessment was not performed; kernel and test receipts support only their stated bounded scopes.",
             "evidence": [EVIDENCE]}
    doc = {**head, "purpose": purpose,
           "design": {"profile": "Exact kernel-checked Lean or exact finite replay on the declared carrier; no floating point.",
                      "frozen_sources": "papers/foundations/authorization_incompleteness/evidence/original holds the unported bytes."},
           "boundaries": boundaries, "evidence": [EVIDENCE]}
    name = path.name
    cs.write_legacy(path.with_name(name + ".contract.yaml"), dump(contract).encode("utf-8"))
    cs.write_legacy(path.with_name(name + ".score.yaml"), dump(score).encode("utf-8"))
    path.with_name(name + ".doc.yaml").write_text(dump(doc), encoding="utf-8", newline="\n")
    return cs.canonical_path(path.with_name(name + ".contract.yaml")).relative_to(ROOT).as_posix()


if __name__ == "__main__":
    for rel, (purpose, boundaries) in TARGETS.items():
        print(write(rel, purpose, boundaries))
