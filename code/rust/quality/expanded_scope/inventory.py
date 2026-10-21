"""Exact coverage ledger for the full expanded review, never a grade generator."""
from pathlib import Path
import ast
from collections import Counter, defaultdict
import hashlib
import json

ROOT = Path(__file__).resolve().parents[4]
PYTHON_GROUPS = (
    "bin category_theory combinatorics databases finite_probability fsp functional "
    "fusion_categories general_relativity higher_category_theory holonomy homology "
    "homotopy_type_theory lie_theory linear_algebra local_green_global_red_lggr "
    "majorana mub number_theory operad_theory qm sheaf_theory"
).split()
DIRECTORIES = ["code/rust/src/tests", "code/rust/src/wdp", *[
    "code/python/src/" + group for group in PYTHON_GROUPS]]
GENERATED = {"__pycache__", "target", ".git", ".pytest_cache", ".mypy_cache"}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def collect():
    subjects = {}
    companions = defaultdict(list)
    for directory in DIRECTORIES:
        parent = ROOT / directory
        if not parent.is_dir():
            raise FileNotFoundError(directory)
        for path in sorted(parent.rglob("*")):
            if not path.is_file() or GENERATED.intersection(path.relative_to(parent).parts):
                continue
            if path.name.endswith(".contract.score.yaml"):
                continue
            data = path.read_bytes()
            name = path.relative_to(ROOT).as_posix()
            companion = path.with_name(path.stem + ".contract.score.yaml").relative_to(ROOT).as_posix()
            row = {"path": name, "directory": directory, "sha256": digest(data), "bytes": len(data),
                   "extension": path.suffix, "companion": companion,
                   "companion_exists": (ROOT / companion).is_file(),
                   "review_status": "NOT_REVIEWED", "capability": None,
                   "gates": dict.fromkeys(["G1", "G2", "G3", "G4", "G5"]),
                   "score_token": None}
            if path.suffix == ".py":
                try:
                    tree = ast.parse(data, filename=name)
                    compile(tree, name, "exec", dont_inherit=True)
                    row["syntax"] = {"status": "PASS", "scope": "parse/compile only, no import or execution"}
                    row["declarations"] = [{"name": node.name, "line": node.lineno,
                        "kind": type(node).__name__} for node in tree.body
                        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))]
                except (SyntaxError, ValueError, TypeError) as error:
                    row["syntax"] = {"status": "FAIL", "error": str(error),
                        "scope": "requires role/claim review before grading"}
            subjects[name] = row
            companions[companion].append(name)
    collisions = {p: names for p, names in companions.items() if len(names) > 1}
    return {"AuthorityEffect": "None", "requested_directories": DIRECTORIES,
        "requested_target": "L4E", "target_interpretation": "User confirmed L4E or higher: actual capability >= L4 and an evidenced engineering grade >= E. Incomplete gates do not qualify; no failure is introduced to earn E.",
        "subject_count": len(subjects), "counts": dict(Counter(s["directory"] for s in subjects.values())),
        "extensions": dict(Counter(s["extension"] for s in subjects.values())),
        "missing_companions": sum(not s["companion_exists"] for s in subjects.values()),
        "companion_name_collisions": collisions, "subjects": subjects,
        "completion_requirements": ["Every listed directory and authored file accounted for",
            "Individual source/test/asset role and actual capability reviewed",
            "File-specific contract with public operations, invariants and failure boundaries",
            "G1-G5 evidence and refusal status recorded without invented grades",
            "Meaningful claim-specific baseline, negative and composition checks",
            "Contract and append-only scoring history in the single combined YAML",
            "Final source/receipt custody and full-scope completion audit"],
        "scope": "Coverage and syntax ledger only. No source capability, test adequacy or engineering grade is inferred."}


if __name__ == "__main__":
    import sys
    result = collect()
    output = ROOT / (sys.argv[1] if len(sys.argv) > 1 else "evidence/quality/expanded_scope/inventory.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: result[key] for key in ["subject_count", "extensions", "missing_companions", "companion_name_collisions"]}, indent=2))
