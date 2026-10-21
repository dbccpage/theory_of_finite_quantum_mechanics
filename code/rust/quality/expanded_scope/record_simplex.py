"""Publish the manually reviewed L4C simplex assessment, bound to its evidence.

The grade is an authored scoped review. This is not a score inference engine.
"""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "scripts"))
import contract_scores as store

SUBJECT = "code/python/src/finite_probability/simplex.py"
REQUIREMENTS = [
    {"id": "admission", "symbols": ["ProbabilitySimplex.__init__", "StochasticMap.__init__", "_require_fraction", "_pair_fraction", "_require_sequence"],
     "relation": "Built-in Fraction/int/ratio-pair entries and built-in list/tuple containers only. Refuse float, bool, overriding subclasses, negative masses, zero denominators, empty or non-unit distributions, and malformed row shapes before exposing a value object."},
    {"id": "lifecycle", "symbols": ["ProbabilitySimplex", "StochasticMap"],
     "relation": "Freeze constructed state in tuples and frozen slots; detach caller containers; probs returns a copy. Refuse ordinary assignment, subclassing and repeated initialization. Python reflection, monkeypatching and mutation of standard-library private internals are outside this API contract."},
    {"id": "constructors", "symbols": ["ProbabilitySimplex.uniform", "ProbabilitySimplex.dirac"],
     "relation": "Positive bounded built-in integer n; uniform gives n equal 1/n weights; dirac requires 0<=index<n and gives one unit mass. Label is a built-in bounded string."},
    {"id": "inspection", "symbols": ["ProbabilitySimplex.dim", "ProbabilitySimplex.probs", "ProbabilitySimplex.__iter__", "ProbabilitySimplex.__getitem__", "ProbabilitySimplex.__eq__", "StochasticMap.rows", "StochasticMap.cols"],
     "relation": "Expose exact entries and shape without mutable container aliases. Integer indexing admits -n<=index<n; slices, bool and out-of-range positions raise SimplexError. Equality compares only weights and returns False for other types; labels are metadata."},
    {"id": "variation", "symbols": ["ProbabilitySimplex.total_variation_distance", "_variation"],
     "relation": "Equal-dimensional admitted distributions p,q -> (1/2)*sum_i abs(p_i-q_i), exactly; otherwise typed refusal."},
    {"id": "mixture", "symbols": ["ProbabilitySimplex.mixture", "_mix"],
     "relation": "Equal dimensions and admitted w in [0,1] -> w*p+(1-w)*q, revalidated before publication. Generated label and output entries must also fit the declared budgets; refusal never rounds the result."},
    {"id": "expectation", "symbols": ["ProbabilitySimplex.expectation", "_expectation"],
     "relation": "One admitted scalar per mass -> sum_i p_i*x_i, exactly, or explicit work-budget refusal."},
    {"id": "channel", "symbols": ["StochasticMap.apply", "_push"],
     "relation": "Input dimension equals matrix row count; output_j=sum_i p_i*M_ij, revalidated as an exact distribution; output too large for admission is refused, never approximated."},
    {"id": "half-witness", "symbols": ["half_simplex_mass", "main"],
     "relation": "The two weights of uniform(2) are 1/2; their exact sum is 1. main prints 1 and returns 0. This calculation does not prove or extract the cited Lean theorem."},
]


def pin(path):
    path = Path(path)
    return {"path": path.relative_to(ROOT).as_posix(), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("challenge")
    parser.add_argument("metrics")
    args = parser.parse_args()
    challenge_path, metrics_path = ROOT / args.challenge, ROOT / args.metrics
    challenge, metrics = [json.loads(path.read_text()) for path in [challenge_path, metrics_path]]
    source = ROOT / SUBJECT
    subject = pin(source)
    assert challenge["status"] == "PASS" and challenge["inputs_unchanged"]
    assert challenge["inputs"][SUBJECT] == metrics["source_sha256"] == subject["sha256"]
    assert challenge["outcomes"] == {"KILLED": 15}
    assert challenge["detection_fraction"] == {"numerator": 15, "denominator": 15}
    assert metrics["source_unchanged"] and not metrics["unsupported_syntax"]
    assert max(row["ccn"] for row in metrics["radon"]) == 5
    assert max(row["ccn"] for row in metrics["lizard"]) == 5
    assert max(row["weighted_control_upper_bound"] for row in metrics["structural_upper_bound"]) == 4
    assert max(row["control_nesting"] for row in metrics["structural_upper_bound"]) == 2
    for name, expected in challenge["inputs"].items():
        assert pin(ROOT / name)["sha256"] == expected, name
    base = ROOT / "evidence/quality/expanded_scope"
    evidence = [pin(challenge_path), pin(metrics_path), pin(base / "batch2-baseline.log")]
    contract = {"AuthorityEffect": "None", "artifact": subject,
        "claim": "urn:omega:fqm:simplex:fractional-half:v1", "profile": "Exact",
        "scope": "Bounded finite Python probability API. No Born-rule uniqueness, Lean theorem extraction, cross-language equivalence, or OS-wide resource guarantee.",
        "requirements": REQUIREMENTS,
        "resource_policy": {"status": "Declared engineering limits, not measured mathematical constants",
            "max_dimension": 4096, "max_matrix_entries": 65536, "max_input_integer_bits": 1024,
            "max_work_fraction_component_bits": 8192, "max_label_characters": 256,
            "semantics": "Reject before oversized container copying/allocation or scalar admission. Check accumulating sum component bits after each exact step. A transient rational addition may exceed the work bound before being refused. Fractions in a returned distribution must fit the input bound. This is an operation envelope, not a wall-clock timeout or OS memory reservation."},
        "cost_model": {"scalar_model": "Arbitrary precision rational arithmetic; integer operation cost depends on coefficient bit length.",
            "loops": "Construction, TV, mixture and expectation take O(n) rational operations; matrix admission and pushforward take O(rows*cols). Copy/storage is O(n) or O(rows*cols). All are capped by declared dimensions and coefficient budgets.",
            "caveat": "No benchmark, hard real-time guarantee, formal allocation bound or zero-allocation claim."},
        "failure_boundary": {"SimplexError": "Malformed scalar/container, invalid dimension/index/shape/label/normalization, incompatible operations, repeated initialization, or budget overflow. Carries invariant and parameter mapping.",
            "FrozenInstanceError_or_TypeError": "Dataclass frozen-slot assignment refusal; exact exception for non-field attributes follows the pinned CPython dataclass implementation.",
            "TypeError": "Subclass declaration refused.",
            "outside_envelope": "Host allocation exhaustion, process termination, concurrent mutation of caller containers during a call, deliberate reflection/private-internal mutation and monkeypatching are not handled by this in-process mathematical API."},
        "dependencies": ["Pinned CPython standard-library fractions.Fraction, dataclasses, tuple/list/int/str behavior"],
        "evidence": evidence}
    scoring = {"AuthorityEffect": "None", "artifact": subject, "rubric": pin(ROOT / "SCORING.md"),
        "phase": "bounded-production-lifecycle-review", "profile": "Exact", "level": "L4",
        "level_basis": "Intentional bounded value-object API with immutable lifecycle, closed scalar/container admission, typed refusals, coefficient/dimension work budgets, public operation contracts and independently challenged composition. No L5 certificate-carrying architecture is claimed.",
        "gates": {"G1": "C", "G2": "C", "G3": "C", "G4": "C", "G5": "B"},
        "basis": {"G1": "Source SHA, unique claim, explicit authority ceiling and public operation/requirement mapping; no full downstream bidirectional provenance audit.",
            "G2": "Closed exact admission and explicit range policy; independent integer-based controls across all 284 two-state pairs at scales 1..8, plus exact arithmetic, subclass and resource rejection probes. B/A-level completeness is not claimed from finite testing.",
            "G3": "Typed expected refusals and frozen lifecycle, detached input containers, reinitialization and hostile-container rejection checks. No proof of crash-freedom outside the declared in-process trust envelope.",
            "G4": "Systematic API/negative/generated finite controls and 15/15 designated valid semantic mutants killed by pytest assertions, including a user __class__ callback regression. Earlier 12/14 and 14/14 campaigns and the later independent counterexample are retained. No independent alternate runner, complete error-path proof or A-level verification claim.",
            "G5": "Radon and Lizard source CCN max 5; calibrated conservative weighted-control upper bound 4 and nesting max 2. Bounded loops/copies with explicit rational bit-cost caveat; no allocation benchmark or zero-allocation certification."},
        "is_complete": True, "composite_grade": "C", "score_token": "L4C",
        "requested_target": "L4E or higher", "target_achieved": True,
        "target_scope": "This exact source revision only, not all 24 directories.", "evidence": evidence,
        "open_higher_grade_findings": ["Full downstream consumer provenance audit", "Exhaustive or formal failure/path assurance", "Independent alternate harness", "Measured peak allocation and performance evidence"]}
    destination = source.with_name(source.stem + store.SUFFIX)
    document = store.load(destination)
    document["assurance"] = "Append-only historical failures, partial reviews and a source-bound bounded L4C assessment. Only current source-matching entries describe the current revision."
    for kind, record in [("contract", contract), ("scoring", scoring)]:
        raw = (json.dumps(record, indent=2) + "\n").encode()
        store.add(document, destination.relative_to(ROOT).as_posix() + "#bounded-production-lifecycle-review/" + kind, raw, kind)
    store.save(destination, document)
    (base / "simplex-assessment.json").write_text(json.dumps({"AuthorityEffect": "None", "source": subject,
        "companion": pin(destination), "score_token": "L4C", "full_scope_target_achieved": False,
        "evidence": evidence}, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"subject": subject, "score": "L4C", "full_scope_target_achieved": False}))


if __name__ == "__main__":
    main()
