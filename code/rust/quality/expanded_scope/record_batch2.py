"""Store eight authored source reviews and their witnessed failure history.

All scores are explicit human-readable assessments. Neither AST metrics nor a
passing test run infers a capability level or silently certifies another file.
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


def pin(path):
    path = Path(path)
    return {"path": path.relative_to(ROOT).as_posix(), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def add(document, target, phase, contract, scoring):
    for kind, record in [("contract", contract), ("scoring", scoring)]:
        store.add(document, target.relative_to(ROOT).as_posix() + "#" + phase + "/" + kind,
                  (json.dumps(record, indent=2) + "\n").encode(), kind)


def historical(document, target, source, definition, folder, gates, phase, level):
    snapshot = folder / "sources" / source.relative_to(ROOT)
    if not snapshot.is_file():
        return
    subject = {"path": source.relative_to(ROOT).as_posix(), "sha256": pin(snapshot)["sha256"]}
    evidence = [pin(folder / "receipt.json"), pin(snapshot)]
    contract = {"AuthorityEffect": "None", "artifact": subject, "phase": phase, "profile": "Exact",
        "status": "historical_defect_review", "purpose": "Historical implementation under independent defect review; later policy and capabilities are not retroactively asserted.",
        "source_claims_verbatim": ast.get_docstring(ast.parse(snapshot.read_bytes())),
        "source_claims_status": "Captured claims, not endorsed verification or capability grades.",
        "scope": "Captured earlier implementation only; later production contracts do not retroactively describe its behavior.",
        "evidence": evidence}
    scoring = {"AuthorityEffect": "None", "artifact": subject, "phase": phase,
        "rubric": pin(ROOT / "SCORING.md"), "profile": "Exact", "level": level,
        "gates": {**dict.fromkeys(["G1", "G2", "G3", "G4", "G5"]), **gates},
        "is_complete": False, "composite_grade": None, "score_token": None,
        "grade_ceiling": "E" if "E" in gates.values() else "D", "target_achieved": False,
        "finding": ("User __class__ callback escaped the typed scalar admission boundary." if phase == "class-callback-counterexample"
            else "See source-pinned receipt: concrete callback/exit-status/error-rendering or invalid-mutant accounting counterexample; core resource-policy absences are inspected D findings."),
        "evidence": evidence}
    add(document, target, phase, contract, scoring)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("entrypoints")
    parser.add_argument("combinatorics")
    parser.add_argument("metrics")
    parser.add_argument("--additional-challenge", action="append", default=[])
    args = parser.parse_args()
    receipts = [ROOT / args.entrypoints, ROOT / args.combinatorics, *[ROOT / name for name in args.additional_challenge]]
    challenges = [json.loads(path.read_text()) for path in receipts]
    metrics_path = ROOT / args.metrics
    metrics = json.loads(metrics_path.read_text())
    assert metrics["status"] == "PASS"
    candidates = {}
    for challenge, receipt_path in zip(challenges, receipts, strict=True):
        assert challenge["inputs_unchanged"]
        for name, digest in challenge["inputs"].items():
            assert pin(ROOT / name)["sha256"] == digest, "Evidence dependency changed: " + name
        for module, result in challenge["files"].items():
            # A failed/invalid sibling's independent subprocess does not erase
            # a passing per-file receipt. It also cannot supply score evidence.
            if not result["baseline_passed"] or result["status"] != "PASS":
                continue
            assert result["outcomes"] == {"KILLED": len(result["mutants"])}
            candidates[module] = (result, receipt_path)
    base = ROOT / "evidence/quality/expanded_scope"
    baseline = base / "batch2-baseline.log"
    assert "133 passed" in baseline.read_text()
    specifications = json.loads(Path(__file__).with_name("batch2_reviews.json").read_text())
    assessments = {}
    for name, definition in specifications.items():
        source = ROOT / name
        subject = pin(source)
        assert definition["claim"] in source.read_text()
        result, receipt_path = candidates[definition["module"]]
        assert result["source_sha256"] == subject["sha256"]
        measured = metrics["sources"][name]
        assert measured["source_sha256"] == subject["sha256"] and measured["unchanged"]
        assert not measured["unsupported_syntax"]
        assert measured["maxima"]["radon_ccn"] <= 10 and measured["maxima"]["lizard_ccn"] <= 10
        assert measured["maxima"]["weighted_control_upper_bound"] <= 15 and measured["maxima"]["control_nesting"] <= 3
        target = source.with_name(source.stem + store.SUFFIX)
        document = store.load(target) if target.is_file() else store.empty(source)
        document["assurance"] = "Append-only captured failures and source-bound bounded L4 reviews; consult current source hashes and evidence scope."
        if "/combinatorics/" in name:
            initial = {"G4": "E"} if definition["role"].startswith("test") else {"G5": "D"} if source.stem == "finite_combinatorics" else {"G3": "E"}
            historical(document, target, source, definition, base / "20261020T210456Z-combinatorics-before", initial,
                       "initial-independent-review", "L3" if source.stem != "__init__" else "L2")
        else:
            historical(document, target, source, definition, base / "20261020T205900Z-entrypoints-before", {"G3": "E"}, "initial-independent-review", "L2")
        historical(document, target, source, definition, base / "20261020T212208Z-class-callback-before", {"G3": "E", "G4": "E"}, "class-callback-counterexample", "L4")
        evidence = [pin(receipt_path), pin(metrics_path), pin(baseline), pin(base / "batch2-atlas.log")]
        contract = {"AuthorityEffect": "None", "artifact": subject, "claim": definition["claim"],
            "profile": "Exact", "role": definition["role"], "purpose": definition["purpose"],
            "operations": definition["operations"], "engineering_policy": definition["policy"],
            "policy_origin": "Declared engineering limits, not empirical measurements or derived physical constants.",
            "failure_boundary": definition["failure"], "cost_model": definition["cost"], "scope_ceiling": definition["ceiling"],
            "trust": "Pinned CPython and providers in the challenge inputs. Type-based checks avoid value.__class__ and container/scalar overrides. This is not a security sandbox for arbitrary metaclass hooks, monkeypatching, hostile interpreter state, host exhaustion or deliberate reflection.",
            "negative_float_fixture_policy": "Tests may deliberately supply binary floats only as rejection probes under SCORING.md.",
            "evidence": evidence}
        g3 = definition.get("g3", "C")
        token = "L4D" if g3 == "D" else "L4C"
        scoring = {"AuthorityEffect": "None", "artifact": subject, "phase": "bounded-production-and-checker-review",
            "rubric": pin(ROOT / "SCORING.md"), "profile": "Exact", "level": "L4", "level_basis": definition["level_basis"],
            "gates": {"G1": "C", "G2": "C", "G3": g3, "G4": "C", "G5": "B"},
            "basis": {"G1": "Source SHA, exact claim ID, explicit operations/policy/trust/authority ceiling; no formal spec AST equivalence or full downstream provenance proof.",
                "G2": "Profile chosen before challenge; exact arithmetic and independent finite controls, strict scalar/container admission and explicit resource refusals. No general mathematical completeness from testing.",
                "G3": definition.get("g3_basis", "Expected failures have typed contexts, input and lifecycle guards are challenged, and concrete admission/callback regressions are fixed. No crash-freedom or arbitrary hostile-code isolation claim."),
                "G4": "Passing source-bound baseline and all " + str(len(result["mutants"])) + " designated valid faults killed, including the __class__ regression; source-binding checks prevent stale test imports. The complete eligible denominator and prior failed/surviving attempts remain visible. No A/A+ mutation-space claim.",
                "G5": "Independent Radon/Lizard observations and conservative calibrated AST controls meet low-complexity ceilings. Operation-specific bounded work/copies are reviewed; no zero-allocation benchmark or formal runtime/heap proof."},
            "metrics": measured["maxima"], "mutation_outcomes": result["outcomes"],
            "is_complete": True, "composite_grade": token[-1], "score_token": token,
            "requested_target": "L4E or higher", "target_achieved": True,
            "target_scope": "This exact file revision only; the full 24-directory objective remains open.",
            "evidence": evidence,
            "open_higher_grade_findings": ["Full downstream provenance and provider audits", "Exhaustive or formal semantic/failure assurance", "Independent alternate checker", "Measured peak allocation and whole-process deadline evidence"]}
        add(document, target, "bounded-production-and-checker-review", contract, scoring)
        store.save(target, document)
        assessments[name] = {"source": subject, "companion": pin(target), "score_token": token, "evidence": evidence}
    (base / "batch2-assessments.json").write_text(json.dumps({"AuthorityEffect": "None", "full_scope_target_achieved": False,
        "files": assessments}, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"complete_at_target": len(assessments), "scores": {name: row["score_token"] for name, row in assessments.items()}, "full_scope_target_achieved": False}, indent=2))


if __name__ == "__main__":
    main()
