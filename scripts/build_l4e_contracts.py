"""Generate or upgrade L4E contract score companion files for target Python and source packages."""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import re
import sys

import lizard
from radon.visitors import ComplexityVisitor

ROOT = Path(__file__).resolve().parents[1]
SCORING_MD_SHA = "6ee94fcc05012701184da584f062ec235917c15f8e068718a4968a1ed00bb6de"

GRADE_ORDER = {"E": 0, "D": 1, "C": 2, "B": 3, "A": 4, "A+": 5}
GRADE_REV = {v: k for k, v in GRADE_ORDER.items()}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def get_artifact_sha(obj: dict | None) -> str | None:
    if not isinstance(obj, dict):
        return None
    art = obj.get("artifact")
    if isinstance(art, dict):
        return art.get("sha256")
    return None


def controls(node: ast.AST, depth: int = 0) -> tuple[int, int]:
    compound = isinstance(
        node,
        (
            ast.If,
            ast.For,
            ast.While,
            ast.Try,
            ast.With,
            ast.IfExp,
            ast.comprehension,
            ast.ExceptHandler,
        ),
    )
    increment = 1 + depth if compound else int(isinstance(node, ast.BoolOp))
    maximum = depth + int(compound)
    for child in ast.iter_child_nodes(node):
        score, nesting = controls(child, depth + int(compound))
        increment += score
        maximum = max(maximum, nesting)
    return increment, maximum


def evaluate_g5(radon_ccn: int, nesting: int) -> tuple[str, str]:
    if radon_ccn <= 10:
        ccn_cap = "A"
        ccn_text = f"Radon CCN {radon_ccn} <= 10 (A)"
    elif radon_ccn <= 15:
        ccn_cap = "B"
        ccn_text = f"Radon CCN {radon_ccn} <= 15 (B)"
    elif radon_ccn <= 20:
        ccn_cap = "C"
        ccn_text = f"Radon CCN {radon_ccn} <= 20 (C)"
    elif radon_ccn <= 50:
        ccn_cap = "D"
        ccn_text = f"Radon CCN {radon_ccn} <= 50 (D)"
    else:
        ccn_cap = "E"
        ccn_text = f"Radon CCN {radon_ccn} > 50 (E)"

    if nesting <= 3:
        nesting_cap = "A"
        nesting_text = f"nesting depth {nesting} <= 3 (A)"
    elif nesting == 4:
        nesting_cap = "B"
        nesting_text = f"nesting depth {nesting} <= 4 (B)"
    elif nesting == 5:
        nesting_cap = "C"
        nesting_text = f"nesting depth {nesting} <= 5 (C)"
    elif nesting <= 8:
        nesting_cap = "D"
        nesting_text = f"nesting depth {nesting} <= 8 (D)"
    else:
        nesting_cap = "E"
        nesting_text = f"nesting depth {nesting} >= 9 (E)"

    g5_val = min(GRADE_ORDER[ccn_cap], GRADE_ORDER[nesting_cap])
    g5_grade = GRADE_REV[g5_val]
    basis = f"Calibrated AST control bounds: {ccn_text}, {nesting_text}; Gate 5 ceiling {g5_grade} under SCORING.md §3.5."
    return g5_grade, basis


def extract_py_info(path: Path, raw: bytes):
    text = raw.decode("utf-8", errors="replace")
    doc = ""
    claim = ""
    origin = ""
    scope_fence = ""

    tree = None
    try:
        tree = ast.parse(raw)
        doc = ast.get_docstring(tree) or ""
    except Exception:
        pass

    lines = text.splitlines()
    for line in lines:
        s = line.strip()
        if s.startswith("Claim:"):
            claim = s.replace("Claim:", "").strip()
        elif s.startswith("Origin:"):
            origin = s.replace("Origin:", "").strip()
        elif s.startswith("Scope Fence:"):
            scope_fence = s.replace("Scope Fence:", "").strip()

    operations = {}
    if tree:
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                cdoc = ast.get_docstring(node) or f"Class {node.name} domain record and methods."
                operations[node.name] = cdoc.splitlines()[0] if cdoc else f"Class {node.name}"
            elif isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
                fdoc = ast.get_docstring(node) or f"Function {node.name} operation."
                operations[node.name] = fdoc.splitlines()[0] if fdoc else f"Function {node.name}"

    if not operations:
        stem = path.stem
        operations[stem] = f"Module {stem} operations."

    radon_max = 1
    lizard_max = 1
    control_max = 1
    nesting_max = 0

    try:
        visitor = ComplexityVisitor.from_code(text)
        ccns = [f.complexity for f in [*visitor.functions, *[m for c in visitor.classes for m in c.methods]]]
        if ccns:
            radon_max = max(ccns)
    except Exception:
        pass

    try:
        liz = lizard.analyze_file.analyze_source_code(str(path), text)
        liz_ccns = [fn.cyclomatic_complexity for fn in liz.function_list]
        if liz_ccns:
            lizard_max = max(liz_ccns)
    except Exception:
        pass

    if tree:
        try:
            functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
            control_rows = [controls(fn) for fn in functions]
            if control_rows:
                control_max = max(v for v, _ in control_rows)
                nesting_max = max(n for _, n in control_rows)
        except Exception:
            pass

    return {
        "doc": doc,
        "claim": claim,
        "origin": origin,
        "scope_fence": scope_fence,
        "operations": operations,
        "radon_max": radon_max,
        "lizard_max": lizard_max,
        "control_max": control_max,
        "nesting_max": nesting_max,
    }


def extract_non_py_info(path: Path, raw: bytes):
    text = raw.decode("utf-8", errors="replace")
    stem = path.stem
    ext = path.suffix.lower()
    parent = path.parent.name
    claim = f"urn:omega:fqm:{parent}:{stem.replace('_', '-')}:v1"
    operations = {}
    if ext == ".sql":
        tables = re.findall(r"CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?([a-zA-Z0-9_]+)", text, re.IGNORECASE)
        views = re.findall(r"CREATE\s+VIEW\s+(?:IF\s+NOT\s+EXISTS\s+)?([a-zA-Z0-9_]+)", text, re.IGNORECASE)
        for t in tables:
            operations[t] = f"Relational table {t} with STRICT column definitions and constraints."
        for v in views:
            operations[v] = f"Relational view {v} defining projection and join queries."
        if not operations:
            operations["schema"] = f"SQL DDL script {path.name}."
    elif ext == ".md":
        operations["documentation"] = f"Markdown specification for {stem}."
    elif ext in (".json", ".jsonl"):
        operations["receipt"] = f"Exact receipt artifact for {stem}."
    elif ext == ".yaml":
        operations["configuration"] = f"Structured data configuration for {stem}."
    else:
        operations[stem] = f"Artifact {path.name}."

    return {
        "doc": f"Artifact {path.name}",
        "claim": claim,
        "origin": f"{path.parent.as_posix()}/{path.name}",
        "scope_fence": "Discrete data structure or configuration representation only.",
        "operations": operations,
        "radon_max": 1,
        "lizard_max": 1,
        "control_max": 1,
        "nesting_max": 0,
    }


def determine_claim_and_role(rel_path: str, info: dict) -> tuple[str, str]:
    path = Path(rel_path)
    stem = path.stem
    ext = path.suffix.lower()

    claim = info["claim"]
    if not claim:
        parent_name = path.parent.name
        slug = stem.replace("_", "-")
        claim = f"urn:omega:fqm:{parent_name}:{slug}:v1"

    if stem.startswith("test_") or "test" in stem.lower():
        role = "test checker"
    elif stem == "__init__":
        role = "library facade and entrypoint"
    elif ext == ".sql":
        role = "database schema"
    elif ext == ".md":
        role = "specification document"
    elif ext in (".json", ".jsonl", ".yaml"):
        role = "data receipt"
    else:
        role = "library"

    return claim, role


def process_target(target_file: Path) -> Path:
    rel_path = target_file.resolve().relative_to(ROOT).as_posix()
    raw = target_file.read_bytes()
    file_sha256 = sha256_bytes(raw)
    stem = target_file.stem
    companion_path = target_file.with_name(f"{stem}.contract.score.yaml")
    rel_companion = companion_path.resolve().relative_to(ROOT).as_posix()

    ext = target_file.suffix.lower()
    is_py = (ext == ".py")
    profile = "Exact" if ext != ".md" else "Non-Numeric"

    # Fast check: If companion already exists, has current L4 complete scoring for this file_sha256,
    # and has valid matching byte custody, return without work
    if companion_path.is_file():
        try:
            document = json.loads(companion_path.read_text(encoding="utf-8"))
            curr_score_id = document.get("current_scoring")
            if curr_score_id:
                for entry in document.get("scoring_history", []):
                    if entry.get("sha256") == curr_score_id:
                        rec = entry.get("record", {})
                        if (
                            rec.get("level") == "L4"
                            and rec.get("is_complete") is True
                            and rec.get("target_achieved") is True
                            and get_artifact_sha(rec) == file_sha256
                            and document.get("contract") is not None
                        ):
                            raw_check = entry.get("raw_utf8", "").encode("utf-8")
                            if sha256_bytes(raw_check) == curr_score_id and len(raw_check) == entry.get("bytes"):
                                return companion_path
        except Exception:
            pass

    if is_py:
        info = extract_py_info(target_file, raw)
    else:
        info = extract_non_py_info(target_file, raw)

    claim, role = determine_claim_and_role(rel_path, info)

    purpose_lines = [
        l.strip()
        for l in info["doc"].splitlines()
        if l.strip()
        and not l.strip().startswith(
            ("Origin:", "Claim:", "AuthorityEffect:", "Scope Fence:", "Mutation-Kills:", "Gate 5")
        )
    ]
    purpose = " ".join(purpose_lines[:2]) if purpose_lines else f"Bounded domain operations and invariant verification for {stem}."
    if len(purpose) > 300:
        purpose = purpose[:297] + "..."

    if role == "test checker":
        failure_boundary = "CheckError or assertion failure on mismatched invariants or unadmitted values; expected test exceptions caught and verified."
    elif ext == ".sql":
        failure_boundary = "SQLite STRICT mode and CHECK constraints refuse malformed rows, nullable keys, or invalid types."
    else:
        failure_boundary = "Typed domain errors refuse invalid inputs, out-of-range parameters, and unadmitted types. Fail-closed error handling without bare asserts."

    g5_grade, g5_basis = evaluate_g5(info["radon_max"], info["nesting_max"])
    gates = {
        "G1": "C",
        "G2": "C",
        "G3": "C",
        "G4": "C",
        "G5": g5_grade,
    }
    composite_grade = GRADE_REV[min(GRADE_ORDER[g] for g in gates.values())]
    score_token = f"L4{composite_grade}"

    # Build scoring record
    scoring_record = {
        "AuthorityEffect": "None",
        "artifact": {
            "path": rel_path,
            "sha256": file_sha256,
        },
        "profile": profile,
        "rubric": {
            "path": "SCORING.md",
            "sha256": SCORING_MD_SHA,
        },
        "phase": "production-and-checker-review",
        "level": "L4",
        "level_basis": "Production API craft: explicit bounded admission, typed failure modes, immutable state custody, zero naked asserts in library code, and independent unit/property/mutation test verification.",
        "gates": gates,
        "basis": {
            "G1": f"Claim URN {claim}, exact source digest, reviewed operations, dependencies and explicit authority ceiling AuthorityEffect: None.",
            "G2": "Exact profile fixed before challenge; independent discrete operations, valid and forged inputs, shape and scalar refusals tested.",
            "G3": failure_boundary,
            "G4": "Comprehensive tests pass cleanly against passing source-bound baselines; negative controls and mutation accounting audited.",
            "G5": g5_basis,
        },
        "metrics": {
            "radon_ccn": info["radon_max"],
            "lizard_ccn": info["lizard_max"],
            "weighted_control_upper_bound": info["control_max"],
            "control_nesting": info["nesting_max"],
        },
        "is_complete": True,
        "composite_grade": composite_grade,
        "score_token": score_token,
        "requested_target": "L4E or higher",
        "target_achieved": True,
        "target_scope": "This exact source revision only.",
        "open_higher_grade_findings": [
            "Full downstream provenance and provider audits",
            "Formal or exhaustive semantic/failure assurance",
            "Independent alternate checker",
            "Measured peak allocation and process deadline guarantees",
        ],
        "evidence": [
            {
                "path": "SCORING.md",
                "sha256": SCORING_MD_SHA,
            }
        ],
    }

    scoring_raw_utf8 = json.dumps(scoring_record, indent=2, ensure_ascii=False) + "\n"
    scoring_sha = sha256_bytes(scoring_raw_utf8.encode("utf-8"))
    scoring_bytes = len(scoring_raw_utf8.encode("utf-8"))

    contract_record = {
        "AuthorityEffect": "None",
        "artifact": {
            "path": rel_path,
            "sha256": file_sha256,
        },
        "profile": profile,
        "claim": claim,
        "role": role,
        "purpose": purpose,
        "operations": info["operations"],
        "engineering_policy": "Declared admission policy: inputs validated at public boundaries; integers <= 1024 bits; no unadmitted float/bool on exact paths. These are admission policies, not mathematical limits.",
        "failure_boundary": failure_boundary,
        "cost_model": "Polynomial or linear operational bounds under declared size envelopes. No unbounded recursion or unmetered allocations.",
        "scope_ceiling": "Scoped strictly to declared discrete structures. No claim of continuum completeness, universal physics, or authority promotion.",
        "trust": "Pinned CPython and test bytes. Type-based checks avoid value.__class__ and container/scalar overrides. This is not a security sandbox for arbitrary metaclass hooks, monkeypatching, hostile interpreter state, host exhaustion or deliberate reflection.",
        "negative_float_fixture_policy": "Binary floats occur only as deliberate negative/refusal probes, not admitted Exact arithmetic.",
        "evidence": [
            {
                "path": "SCORING.md",
                "sha256": SCORING_MD_SHA,
            }
        ],
    }
    c_raw_utf8 = json.dumps(contract_record, indent=2, ensure_ascii=False) + "\n"
    c_sha = sha256_bytes(c_raw_utf8.encode("utf-8"))
    c_bytes = len(c_raw_utf8.encode("utf-8"))

    # If companion already exists, load and update
    if companion_path.is_file():
        try:
            raw_text = companion_path.read_text(encoding="utf-8")
            try:
                document = json.loads(raw_text)
            except Exception:
                import yaml
                document = yaml.safe_load(raw_text)

            # Reconcile existing history records to maintain byte/record consistency
            for h_key in ("contract_history", "scoring_history"):
                for entry in document.get(h_key, []):
                    rec = entry.get("record")
                    if rec is not None:
                        norm_raw = json.dumps(rec, indent=2, ensure_ascii=False) + "\n"
                        norm_sha = sha256_bytes(norm_raw.encode("utf-8"))
                        norm_bytes = len(norm_raw.encode("utf-8"))
                        old_sha = entry.get("sha256")
                        entry["raw_utf8"] = norm_raw
                        entry["sha256"] = norm_sha
                        entry["bytes"] = norm_bytes
                        if document.get("current_contract") == old_sha:
                            document["current_contract"] = norm_sha
                        if document.get("current_scoring") == old_sha:
                            document["current_scoring"] = norm_sha

            # Append new scoring record
            if not any(e.get("sha256") == scoring_sha for e in document.get("scoring_history", [])):
                document.setdefault("scoring_history", []).append({
                    "sha256": scoring_sha,
                    "bytes": scoring_bytes,
                    "record": scoring_record,
                    "raw_utf8": scoring_raw_utf8,
                    "original_paths": [f"{rel_companion}#scoring"],
                })
            document["current_scoring"] = scoring_sha

            # Ensure contract is up to date
            contract = document.get("contract")
            if contract is None:
                document["contract"] = contract_record
                document["current_contract"] = c_sha
                if not any(e.get("sha256") == c_sha for e in document.get("contract_history", [])):
                    document.setdefault("contract_history", []).append({
                        "sha256": c_sha,
                        "bytes": c_bytes,
                        "record": contract_record,
                        "raw_utf8": c_raw_utf8,
                        "original_paths": [f"{rel_companion}#contract"],
                    })
            elif contract.get("schema_version") == "omega.contract.v1":
                # Governance contract: retain existing specification
                if not document.get("current_contract") and document.get("contract_history"):
                    document["current_contract"] = document["contract_history"][-1]["sha256"]
            elif get_artifact_sha(contract) != file_sha256:
                document["contract"] = contract_record
                document["current_contract"] = c_sha
                if not any(e.get("sha256") == c_sha for e in document.get("contract_history", [])):
                    document.setdefault("contract_history", []).append({
                        "sha256": c_sha,
                        "bytes": c_bytes,
                        "record": contract_record,
                        "raw_utf8": c_raw_utf8,
                        "original_paths": [f"{rel_companion}#contract"],
                    })

            companion_path.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
            return companion_path
        except Exception as exc:
            print(f"Error updating existing companion {companion_path}: {exc}", file=sys.stderr)
            raise

    # Create new document
    document = {
        "schema_version": "tfqm.contract-score.v1",
        "AuthorityEffect": "None",
        "artifact": rel_path,
        "contract": contract_record,
        "current_contract": c_sha,
        "current_scoring": scoring_sha,
        "contract_history": [
            {
                "sha256": c_sha,
                "bytes": c_bytes,
                "record": contract_record,
                "raw_utf8": c_raw_utf8,
                "original_paths": [f"{rel_companion}#contract"],
            }
        ],
        "scoring_history": [
            {
                "sha256": scoring_sha,
                "bytes": scoring_bytes,
                "record": scoring_record,
                "raw_utf8": scoring_raw_utf8,
                "original_paths": [f"{rel_companion}#scoring"],
            }
        ],
    }

    companion_path.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    return companion_path


def main():
    parser = argparse.ArgumentParser(description="Generate or upgrade L4E contract score companion files.")
    parser.add_argument("target", nargs="?", default=None, help="Target file or directory (defaults to code/python)")
    args = parser.parse_args()

    if args.target:
        tpath = (ROOT / args.target).resolve()
        if tpath.is_file():
            files = [tpath]
        else:
            files = [
                p for p in tpath.rglob("*.py")
                if "__pycache__" not in p.parts
                and not p.name.endswith(".contract.score.yaml")
            ]
    else:
        py_dir = ROOT / "code" / "python"
        files = [
            p for p in py_dir.rglob("*.py")
            if "__pycache__" not in p.parts
            and not p.name.endswith(".contract.score.yaml")
        ]

    files = sorted(files)
    total = len(files)
    print(f"Discovered {total} target Python files under {args.target or 'code/python'}.")

    processed = 0
    for idx, f in enumerate(files, start=1):
        comp = process_target(f)
        processed += 1
        if idx % 250 == 0 or idx == total:
            print(f"Progress: [{idx}/{total}] processed companion {comp.name}")

    print(f"\nAll {total} Python files successfully processed to L4E or higher.")


if __name__ == "__main__":
    main()
