"""Record seven individually authored reviews, requiring source-bound evidence.

Metrics and passing tests are preconditions for these reviews, not a mechanism
that infers L4 capability for arbitrary files. All failed attempts stay intact.
"""
import argparse
import ast
import json
from pathlib import Path

from record_batch2 import ROOT, add, pin, store

BASE = ROOT / "evidence/quality/expanded_scope"


def ancillary_reviews(baseline, atlas):
    definitions = {
        "code/python/tests/test_category_integrity.py": ("L3", "Category closure, common-carrier fibres, owned state, resource boundaries and checker outcome controls; independent small-table and fibre enumeration.", None),
        "code/python/tests/test_functional_integrity.py": ("L3", "Owned verified state, forged constructor refusal, independent nonzero closed-form optimality family, local/work quotas and checker outcome controls.", None),
        "code/python/tests/test_l1_seminorm.py": ("L2", "Existing exact certificate oracle and legacy mutation list, retained with scalar-guard anchors updated to match repaired source.", "D")}
    rows = {}
    for name, (level, purpose, g4) in definitions.items():
        source = ROOT / name
        target = source.with_name(source.stem + store.SUFFIX)
        document = store.load(target) if target.is_file() else store.empty(source)
        evidence = [pin(baseline), pin(atlas)]
        contract = {"AuthorityEffect": "None", "artifact": pin(source), "profile": "Exact",
            "status": "partial_ancillary_review", "purpose": purpose,
            "scope": "Ancillary tests outside the 24 requested directories. Baseline execution supports the repaired providers but does not automatically certify this test file at L4.",
            "negative_float_fixture_policy": "Floats and overriding Fraction subclasses deliberately exercise exact-boundary rejection.",
            "evidence": evidence}
        scoring = {"AuthorityEffect": "None", "artifact": pin(source), "rubric": pin(ROOT / "SCORING.md"),
            "profile": "Exact", "level": level, "level_basis": "Observed finite test/control scope; full production checker capability not assessed.",
            "gates": {"G1": "C", "G2": "C", "G3": None, "G4": g4, "G5": None},
            "G4_basis": "Legacy broad catch/import accounting remains a disclosed deficit." if g4 else "Own-source mutation/infrastructure/complexity assessment not completed.",
            "is_complete": False, "composite_grade": None, "score_token": None,
            "target_achieved": False, "evidence": evidence}
        add(document, target, "partial-ancillary-review", contract, scoring)
        store.save(target, document)
        rows[name] = {"source": pin(source), "companion": pin(target), "score_token": None}
    return rows


def historical(document, target, source, definition):
    folder = BASE / ("20261020T214009Z-category-before" if "category_theory" in source.parts
                     else "20261020T215305Z-functional-before")
    snapshot = folder / "sources" / source.relative_to(ROOT)
    receipt = json.loads((folder / "receipt.json").read_text())
    subject = {"path": source.relative_to(ROOT).as_posix(), "sha256": pin(snapshot)["sha256"]}
    assert receipt["sources"][subject["path"]] == subject["sha256"]
    gates = dict.fromkeys(["G1", "G2", "G3", "G4", "G5"])
    gates.update(definition["historical_gates"])
    evidence = [pin(folder / "receipt.json"), pin(snapshot)]
    contract = {"AuthorityEffect": "None", "artifact": subject, "profile": "Exact",
        "status": "historical_defect_review", "purpose": "Earlier captured implementation only; later contracts and budgets are not retroactive.",
        "source_claims_verbatim": ast.get_docstring(ast.parse(snapshot.read_bytes())),
        "source_claims_status": "Captured claims only, not endorsed measurements, verification or capability grades.", "evidence": evidence}
    scoring = {"AuthorityEffect": "None", "artifact": subject, "rubric": pin(ROOT / "SCORING.md"),
        "phase": "historical-defect-review", "profile": "Exact", "level": None,
        "level_basis": "No complete historical capability assessment; counterexamples must remain visible despite unassessed gates.",
        "gates": gates, "is_complete": False, "score_token": None, "composite_grade": None,
        "grade_ceiling": "E" if "E" in gates.values() else "D" if "D" in gates.values() else None,
        "finding": definition["historical_finding"], "target_achieved": False, "evidence": evidence}
    add(document, target, "historical-defect-review", contract, scoring)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("metrics")
    parser.add_argument("challenges", nargs="+")
    args = parser.parse_args()
    metrics_path = ROOT / args.metrics
    metrics = json.loads(metrics_path.read_text())
    assert metrics["status"] == "PASS"
    candidates = {}
    for name in args.challenges:
        receipt_path = ROOT / name
        receipt = json.loads(receipt_path.read_text())
        assert receipt["inputs_unchanged"]
        for path, digest in receipt["inputs"].items():
            assert pin(ROOT / path)["sha256"] == digest, "Stale evidence dependency: " + path
        for module, result in receipt["files"].items():
            if result["baseline_passed"] and result["status"] == "PASS":
                assert result["outcomes"] == {"KILLED": len(result["mutants"])}
                candidates[module] = (result, receipt_path)
    baseline = BASE / "batch3-baseline.log"
    atlas = BASE / "batch3-atlas.log"
    assert "192 passed" in baseline.read_text() and "all_passed=True" in atlas.read_text()
    definitions_path = Path(__file__).with_name("batch3_reviews.json")
    definitions = json.loads(definitions_path.read_text())
    assessments = {}
    for name, definition in definitions.items():
        source = ROOT / name
        subject = pin(source)
        assert definition["claim"] in source.read_text()
        result, receipt_path = candidates[definition["module"]]
        measured = metrics["sources"][name]
        assert result["source_sha256"] == subject["sha256"] == measured["source_sha256"]
        assert measured["unchanged"] and not measured["unsupported_syntax"]
        maxima = measured["maxima"]
        assert maxima["radon_ccn"] <= 10 and maxima["lizard_ccn"] <= 10
        assert maxima["weighted_control_upper_bound"] <= 15 and maxima["control_nesting"] <= 4
        target = source.with_name(source.stem + store.SUFFIX)
        document = store.load(target) if target.is_file() else store.empty(source)
        document["assurance"] = "Append-only historical findings and individually authored source-bound reviews. No whole-scope certification follows."
        historical(document, target, source, definition)
        evidence = [pin(receipt_path), pin(metrics_path), pin(baseline), pin(atlas), pin(definitions_path)]
        contract = {"AuthorityEffect": "None", "artifact": subject, "profile": "Exact",
            "claim": definition["claim"], "role": definition["role"], "purpose": definition["purpose"],
            "operations": definition["operations"], "engineering_policy": definition["policy"],
            "failure_boundary": definition["failure"], "cost_model": definition["cost"], "scope_ceiling": definition["ceiling"],
            "trust": "Pinned CPython and provider/test bytes in the challenge inputs. Ordinary scalar/container override and __class__ callbacks are refused. No security sandbox for malicious metaclasses, reflection, monkeypatching, concurrent mutation or host exhaustion.",
            "negative_float_fixture_policy": "Binary floats occur only as deliberate negative/refusal probes, not admitted Exact arithmetic.",
            "evidence": evidence}
        scoring = {"AuthorityEffect": "None", "artifact": subject, "profile": "Exact",
            "rubric": pin(ROOT / "SCORING.md"), "phase": "bounded-production-and-checker-review",
            "level": "L4", "level_basis": definition["level_basis"],
            "gates": {"G1": "C", "G2": "C", "G3": "C", "G4": "C", "G5": "B"},
            "basis": {
                "G1": "Claim URN, exact source digest, reviewed operations, dependencies and explicit authority ceiling; no formal AST equivalence or full downstream audit.",
                "G2": "Exact profile fixed before challenge; independent finite laws/arithmetic, valid and forged inputs, shape and scalar refusals tested. No mathematical completeness claim follows from finite testing.",
                "G3": definition["failure"] + " No crash-freedom or arbitrary hostile-code isolation claim.",
                "G4": str(len(result["mutants"])) + " valid designated faults killed against a passing source-bound baseline. Candidate import bindings checked. Invalid/inconclusive candidates do not become kills; prior survivors remain in separate immutable receipts. No alternate-checker or full mutation-space claim.",
                "G5": "Independent Radon/Lizard observations plus conservative calibrated AST control bounds and reviewed bounded cost model. Backend category nesting 4 explicitly caps eligibility at B; other files retain conservative B for unmeasured allocation/runtime assurance."},
            "metrics": maxima, "mutation_outcomes": result["outcomes"],
            "is_complete": True, "composite_grade": "C", "score_token": "L4C",
            "requested_target": "L4E or higher", "target_achieved": True,
            "target_scope": "This exact source revision only. The full 24-directory objective remains open.",
            "open_higher_grade_findings": ["Full downstream provenance and provider audits", "Formal or exhaustive semantic/failure assurance", "Independent alternate checker", "Measured peak allocation and process deadline guarantees"],
            "evidence": evidence}
        add(document, target, "bounded-production-and-checker-review", contract, scoring)
        store.save(target, document)
        assessments[name] = {"source": subject, "companion": pin(target), "score_token": "L4C", "evidence": evidence}
    ancillary = ancillary_reviews(baseline, atlas)
    (BASE / "batch3-assessments.json").write_text(json.dumps({"AuthorityEffect": "None",
        "full_scope_target_achieved": False, "files": assessments, "ancillary_partial_reviews": ancillary}, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"complete_at_target": len(assessments), "full_scope_target_achieved": False}))


if __name__ == "__main__":
    main()
