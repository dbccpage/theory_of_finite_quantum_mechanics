"""Append the explicitly authored partial reviews; never manufacture L4 grades."""
import ast
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "scripts"))
import contract_scores as store


def pin(path):
    return {"path": path.relative_to(ROOT).as_posix(), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def declarations(raw):
    tree = ast.parse(raw)
    return [{"name": node.name, "line": node.lineno, "kind": type(node).__name__}
            for node in tree.body if isinstance(node, (ast.FunctionDef, ast.ClassDef))]


def append(source, raw, definition, phase, g2, evidence):
    destination = source.with_name(source.stem + store.SUFFIX)
    document = store.load(destination) if destination.is_file() else store.empty(source)
    previous = {key: document[key] for key in ("contract", "current_contract", "current_scoring")}
    actual_sha = hashlib.sha256(source.read_bytes()).hexdigest()
    preserve_current = bool(document["contract"] and document["contract"].get("artifact", {}).get("sha256") == actual_sha
                            and hashlib.sha256(raw).hexdigest() != actual_sha)
    document["assurance"] = "Partial source-bound review snapshots; incomplete gates and unmet capability targets remain explicit."
    subject = {"path": source.relative_to(ROOT).as_posix(), "sha256": hashlib.sha256(raw).hexdigest()}
    contract = {"AuthorityEffect": "None", "artifact": subject, "status": "partial_source_review",
        "profile": "Exact", "purpose": definition["purpose"], "operations": definition["operations"],
        "failure_boundary": definition["failures"], "open_limits": definition["limits"],
        "declaration_index": declarations(raw), "declaration_index_scope": "Top-level AST index only; not semantic coverage.",
        "scalar_policy": ("Exact arithmetic requires exact return values; the captured source accepted an overriding Fraction subclass and returned float. Closed-type admission was not yet enforced."
            if g2 == "E" else "This repaired boundary accepts built-in Fraction/int coefficients (and validated integer ratio pairs in simplex); overriding Fraction subclasses are refused before arithmetic."
            if g2 == "C" else "Local admission and provider trust remain under partial review; see the operations and open limits."),
        "evidence": evidence}
    scoring = {"AuthorityEffect": "None", "artifact": subject, "rubric": pin(ROOT / "SCORING.md"),
        "phase": phase, "requested_target": "L4E", "target_achieved": False,
        "level": definition["level"], "level_basis": definition["level_basis"],
        "profile": "Exact", "gates": {"G1": None, "G2": g2, "G3": None, "G4": None, "G5": None},
        "is_complete": False, "composite_grade": None, "score_token": None, "grade_ceiling": g2,
        "G2_basis": ("Public-input subclass counterexample returns float 0.5 instead of rational 1."
            if g2 == "E" else "Closed scalar admission plus bounded negative and arithmetic controls; broader verification remains open."
            if g2 == "C" else "No complete gate assessment yet."),
        "assessment_status": "partial_not_L4_certification", "evidence": evidence,
        "open_findings": definition["limits"] + ["Complete independent G1/G3/G4/G5 reviews and establish actual L4 architecture before claiming the target."]}
    for kind, record in [("contract", contract), ("scoring", scoring)]:
        payload = (json.dumps(record, indent=2) + "\n").encode()
        address = destination.relative_to(ROOT).as_posix() + "#" + phase + "/" + kind
        store.add(document, address, payload, kind)
    if preserve_current:
        document.update(previous)
    store.save(destination, document)
    return {"companion": pin(destination), "reviewed_source": subject, "matches_current_source": subject["sha256"] == actual_sha,
            "review_status": "PARTIAL", "level": definition["level"], "target_achieved": False}


def main():
    base = ROOT / "evidence/quality/expanded_scope"
    reviews = json.loads(Path(__file__).with_name("reviews.json").read_text())
    before = json.loads((base / "20261020-exact-subclass-before-sealed/receipt.json").read_text())
    after = json.loads((base / "20261020-exact-subclass-after/receipt.json").read_text())
    assert all(c["exact_invariant_violated"] and c["source_unchanged"] for c in before["cases"])
    assert all(c["status"] == "REFUSED" and c["source_unchanged"] for c in after["cases"])
    before_names = {c["source"] for c in before["cases"]}
    result = {}
    for name, definition in reviews.items():
        source = ROOT / name
        if name in before_names:
            raw = (base / "20261020-exact-subclass-before-sealed/sources" / name).read_bytes()
            append(source, raw, definition, "counterexample-before-repair", "E", [pin(base / "20261020-exact-subclass-before-sealed/receipt.json")])
        # Keep this historical review bound to the bytes actually probed. Later
        # production edits receive a separate review, never stale test credit.
        after_raw = (base / "20261020-exact-subclass-after/sources" / name).read_bytes() if name in before_names else source.read_bytes()
        result[name] = append(source, after_raw, definition, "partial-review-after-admission-repair",
            "C" if name in before_names else None, [pin(base / "20261020-exact-subclass-after/receipt.json"),
                pin(base / "python-baseline-after.log"), pin(ROOT / "code/python/tests/test_expanded_exact_admission.py")])
    (base / "review-progress.json").write_text(json.dumps({"AuthorityEffect": "None", "target_achieved": False,
        "files": result, "scope": "Five partial source reviews only; the entire 24-directory objective remains open."}, indent=2) + "\n")
    print(json.dumps({"partial_reviews": len(result), "target_achieved": False}))


if __name__ == "__main__":
    main()
