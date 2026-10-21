"""Retired unsafe L4E companion generator.

This file is retained so historical command references fail with an explicit
explanation.  Source inspection and file-name heuristics cannot establish the
five SCORING.md gates, so this command must not manufacture completed L4
records.  Use ``scripts/score_scope_contracts.py prepare`` for source-pinned
coverage contracts and incomplete baseline assessments.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import re
import sys

try:
    import lizard
except ImportError:
    # The legacy implementation is no longer reachable from the CLI.  Keeping
    # this import optional lets the safety refusal run in minimal environments.
    lizard = None

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
    if obj.get("source_sha256"):
        return obj.get("source_sha256")
    return None


def max_grade(g1: str | None, g2: str) -> str:
    if not g1 or g1 not in GRADE_ORDER:
        return g2
    return GRADE_REV[max(GRADE_ORDER[g1], GRADE_ORDER[g2])]


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


def compute_rust_nesting(text: str) -> tuple[int, int]:
    clean_lines = []
    for line in text.splitlines():
        clean_lines.append(line.split("//")[0])
    code = "\n".join(clean_lines)
    code = re.sub(r'r#".*?"#|"(?:\\.|[^"\\])*"', '""', code, flags=re.DOTALL)
    code = re.sub(r"b?'(?:\\.|[^'\\])'", "''", code)
    code = re.sub(r"'[A-Za-z_]\w*", "", code)
    code = re.sub(r"'(?:\\.|[^'\\])*'", "''", code)

    control_keywords = {"if", "match", "while", "for", "loop"}
    tokens = re.findall(r"\b(?:fn|if|match|while|for|loop)\b|[{}]", code)

    max_nesting = 0
    control_count = 0
    fn_brace_depth = 0
    curr_nesting = 0
    nesting_stack: list[int] = []

    for tok in tokens:
        if tok == "fn":
            pass
        elif tok == "{":
            fn_brace_depth += 1
        elif tok == "}":
            if nesting_stack and fn_brace_depth == nesting_stack[-1]:
                nesting_stack.pop()
                curr_nesting -= 1
            fn_brace_depth = max(0, fn_brace_depth - 1)
        elif tok in control_keywords:
            control_count += 1
            curr_nesting += 1
            nesting_stack.append(fn_brace_depth + 1)
            max_nesting = max(max_nesting, curr_nesting)

    return control_count, max_nesting


def evaluate_g5(ccn: int, nesting: int) -> tuple[str, str]:
    if ccn <= 10:
        ccn_cap = "A"
        ccn_text = f"CCN {ccn} <= 10 (A)"
    elif ccn <= 15:
        ccn_cap = "B"
        ccn_text = f"CCN {ccn} <= 15 (B)"
    elif ccn <= 20:
        ccn_cap = "C"
        ccn_text = f"CCN {ccn} <= 20 (C)"
    elif ccn <= 50:
        ccn_cap = "D"
        ccn_text = f"CCN {ccn} <= 50 (D)"
    else:
        ccn_cap = "E"
        ccn_text = f"CCN {ccn} > 50 (E)"

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


def extract_metrics_from_history(document: dict) -> tuple[int | None, int | None, int | None]:
    for entry in document.get("scoring_history", []):
        rec = entry.get("record", {})
        if not isinstance(rec, dict):
            continue
        if "structure" in rec and isinstance(rec["structure"], dict):
            st = rec["structure"]
            if "max_production_ccn" in st:
                return st.get("max_production_ccn"), st.get("control_nesting"), st.get("cognitive_complexity_upper_bound")
            if "functions" in st and isinstance(st["functions"], list) and st["functions"]:
                ccns = [f.get("ccn", 1) for f in st["functions"] if isinstance(f, dict)]
                nestings = [f.get("control_nesting", 0) for f in st["functions"] if isinstance(f, dict)]
                cogs = [f.get("cognitive_upper_bound", 0) for f in st["functions"] if isinstance(f, dict)]
                return (max(ccns) if ccns else 1, max(nestings) if nestings else 0, max(cogs) if cogs else 0)
        if "structural_measurement" in rec and isinstance(rec["structural_measurement"], dict):
            sm = rec["structural_measurement"]
            if "maxima" in sm and isinstance(sm["maxima"], dict):
                m = sm["maxima"]
                return m.get("ccn"), m.get("control_nesting"), m.get("cognitive_upper_bound")
        if "metrics" in rec and isinstance(rec["metrics"], dict):
            m = rec["metrics"]
            return m.get("lizard_ccn") or m.get("radon_ccn"), m.get("control_nesting"), m.get("weighted_control_upper_bound")
    return None, None, None


def extract_existing_gates(existing_doc: dict | None) -> dict[str, str]:
    best_gates = {"G1": "C", "G2": "C", "G3": "C", "G4": "C"}
    if not existing_doc:
        return best_gates
    for entry in existing_doc.get("scoring_history", []):
        rec = entry.get("record", {})
        if not isinstance(rec, dict):
            continue
        g = rec.get("gates", {})
        if isinstance(g, dict):
            for k in ("G1", "G2", "G3", "G4"):
                val = g.get(k)
                if isinstance(val, dict):
                    val = val.get("grade")
                if val in GRADE_ORDER:
                    if GRADE_ORDER[val] > GRADE_ORDER[best_gates[k]]:
                        best_gates[k] = val
    return best_gates


def extract_rust_info(path: Path, raw: bytes, existing_doc: dict | None = None) -> dict:
    text = raw.decode("utf-8", errors="replace")

    doc_lines = []
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("//!"):
            doc_lines.append(s.replace("//!", "").strip())
        elif s.startswith("///") and not doc_lines:
            doc_lines.append(s.replace("///", "").strip())
        elif s.startswith(("//", "/*")) or not s:
            continue
        else:
            break
    doc = "\n".join(doc_lines)
    if not doc:
        stem = path.stem
        doc = f"Rust module {stem} implementation and domain invariants."

    claim = ""
    origin = ""
    scope_fence = ""
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("// Claim:"):
            claim = s.replace("// Claim:", "").strip()
        elif s.startswith("// Origin:"):
            origin = s.replace("// Origin:", "").strip()
        elif s.startswith("// Scope Fence:"):
            scope_fence = s.replace("// Scope Fence:", "").strip()

    operations = {}
    if existing_doc:
        contract = existing_doc.get("contract")
        if isinstance(contract, dict):
            existing_ops = contract.get("operations")
            if isinstance(existing_ops, dict) and existing_ops:
                operations = dict(existing_ops)

    if not operations:
        for m in re.finditer(r"pub\s+(?:async\s+)?fn\s+([a-zA-Z0-9_]+)", text):
            fn_name = m.group(1)
            operations[fn_name] = f"Public function {fn_name} operation."
        for m in re.finditer(r"pub\s+struct\s+([a-zA-Z0-9_]+)", text):
            st_name = m.group(1)
            operations[st_name] = f"Domain struct {st_name} record and invariants."
        for m in re.finditer(r"pub\s+enum\s+([a-zA-Z0-9_]+)", text):
            en_name = m.group(1)
            operations[en_name] = f"Algebraic enum {en_name} variants and cases."
        for m in re.finditer(r"pub\s+trait\s+([a-zA-Z0-9_]+)", text):
            tr_name = m.group(1)
            operations[tr_name] = f"Domain trait {tr_name} interface contract."
        for m in re.finditer(r"pub\s+type\s+([a-zA-Z0-9_]+)", text):
            ty_name = m.group(1)
            operations[ty_name] = f"Type alias {ty_name} domain definition."

    if not operations:
        stem = path.stem
        operations[stem] = f"Module {stem} operations."

    file_sha256 = sha256_bytes(raw)
    syn_ccn, syn_nesting, syn_cog = (None, None, None)
    if existing_doc and get_artifact_sha(existing_doc) == file_sha256:
        syn_ccn, syn_nesting, syn_cog = extract_metrics_from_history(existing_doc)

    lizard_max = 1
    try:
        liz = lizard.analyze_file.analyze_source_code(str(path), text)
        liz_ccns = [fn.cyclomatic_complexity for fn in liz.function_list]
        if liz_ccns:
            lizard_max = max(liz_ccns)
    except Exception:
        pass

    ctrl_count, ctrl_nesting = compute_rust_nesting(text)

    radon_max = syn_ccn if syn_ccn is not None else lizard_max
    if lizard_max > radon_max:
        radon_max = lizard_max
    nesting_max = syn_nesting if syn_nesting is not None else ctrl_nesting
    control_max = syn_cog if syn_cog is not None else max(1, ctrl_count)

    return {
        "doc": doc,
        "claim": claim,
        "origin": origin or f"{path.parent.as_posix()}/{path.name}",
        "scope_fence": scope_fence,
        "operations": operations,
        "radon_max": radon_max,
        "lizard_max": lizard_max,
        "control_max": control_max,
        "nesting_max": nesting_max,
    }


def extract_py_info(path: Path, raw: bytes) -> dict:
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
        from radon.visitors import ComplexityVisitor
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


def extract_non_py_info(path: Path, raw: bytes) -> dict:
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
    elif ext == ".toml":
        operations["cargo_package"] = f"Cargo package manifest and workspace configuration for {stem}."
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

    if stem.startswith("test_") or "test" in stem.lower() or "tests" in path.parts:
        role = "test checker"
    elif stem in ("__init__", "lib", "mod"):
        role = "library facade and entrypoint"
    elif ext == ".toml":
        role = "crate manifest"
    elif ext == ".sql":
        role = "database schema"
    elif ext == ".md":
        role = "specification document"
    elif ext in (".json", ".jsonl", ".yaml"):
        role = "data receipt"
    else:
        role = "library"

    return claim, role


def process_target(target_file: Path, companion_path: Path | None = None) -> Path:
    rel_path = target_file.resolve().relative_to(ROOT).as_posix()
    raw = target_file.read_bytes()
    file_sha256 = sha256_bytes(raw)
    stem = target_file.stem
    if companion_path is None:
        companion_path = target_file.with_name(f"{stem}.contract.score.yaml")
    rel_companion = companion_path.resolve().relative_to(ROOT).as_posix()

    ext = target_file.suffix.lower()
    is_py = (ext == ".py")
    is_rs = (ext == ".rs")

    if is_rs:
        language = "Rust"
        profile = "Exact"
    elif is_py:
        language = "Python"
        profile = "Exact"
    elif ext == ".toml":
        language = "TOML"
        profile = "Non-Numeric"
    elif ext in (".json", ".jsonl"):
        language = "JSON"
        profile = "Exact"
    elif ext == ".sql":
        language = "SQL"
        profile = "Exact"
    else:
        language = "Other"
        profile = "Non-Numeric" if ext == ".md" else "Exact"

    # Fast check: If companion already exists, has current L4 complete scoring for this file_sha256,
    # target_achieved True, and valid byte custody, return without work
    existing_doc = None
    if companion_path.is_file():
        try:
            raw_text = companion_path.read_text(encoding="utf-8")
            try:
                existing_doc = json.loads(raw_text)
            except Exception:
                import yaml
                existing_doc = yaml.safe_load(raw_text)

            curr_score_id = existing_doc.get("current_scoring")
            if curr_score_id:
                for entry in existing_doc.get("scoring_history", []):
                    if entry.get("sha256") == curr_score_id:
                        rec = entry.get("record", {})
                        if (
                            rec.get("level") == "L4"
                            and rec.get("is_complete") is True
                            and rec.get("target_achieved") is True
                            and get_artifact_sha(rec) == file_sha256
                            and existing_doc.get("contract") is not None
                            and existing_doc.get("current_contract") is not None
                        ):
                            raw_check = entry.get("raw_utf8", "").encode("utf-8")
                            if sha256_bytes(raw_check) == curr_score_id and len(raw_check) == entry.get("bytes"):
                                return companion_path
        except Exception:
            pass

    if is_rs:
        info = extract_rust_info(target_file, raw, existing_doc)
    elif is_py:
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
        failure_boundary = "Assertion failure or panic on unadmitted invariants or forged witness; expected test exceptions caught and verified."
    elif ext == ".sql":
        failure_boundary = "SQLite STRICT mode and CHECK constraints refuse malformed rows, nullable keys, or invalid types."
    elif ext == ".toml":
        failure_boundary = "Cargo parser and TOML engine refuse malformed manifests, invalid dependency specifications, or missing required metadata."
    elif ext in (".json", ".jsonl"):
        failure_boundary = "JSON parser refuses malformed syntax, unadmitted keys, or schema validation mismatches."
    elif is_rs:
        failure_boundary = "Typed Result<T, E> error returns refuse unadmitted inputs, out-of-range bounds, and malformed state; zero unhandled panics on public interfaces."
    else:
        failure_boundary = "Typed domain errors refuse invalid inputs, out-of-range parameters, and unadmitted types. Fail-closed error handling without bare asserts."

    g5_grade, g5_basis = evaluate_g5(info["radon_max"], info["nesting_max"])
    existing_gates = extract_existing_gates(existing_doc)
    gates = {
        "G1": max_grade(existing_gates.get("G1"), "C"),
        "G2": max_grade(existing_gates.get("G2"), "C"),
        "G3": max_grade(existing_gates.get("G3"), "C"),
        "G4": max_grade(existing_gates.get("G4"), "C"),
        "G5": g5_grade,
    }
    composite_grade = GRADE_REV[min(GRADE_ORDER[g] for g in gates.values())]
    score_token = f"L4{composite_grade}"

    # Preserve any existing evidence or structural measurements
    evidence = [
        {
            "path": "SCORING.md",
            "sha256": SCORING_MD_SHA,
        }
    ]
    prev_structure = None
    if existing_doc:
        for entry in existing_doc.get("scoring_history", []):
            r = entry.get("record", {})
            if isinstance(r, dict):
                if "evidence" in r and isinstance(r["evidence"], list):
                    for ev in r["evidence"]:
                        if isinstance(ev, dict) and ev.get("path") and ev.get("path") != "SCORING.md":
                            if not any(e.get("path") == ev.get("path") for e in evidence):
                                evidence.append(ev)
                if prev_structure is None:
                    if "structure" in r and (get_artifact_sha(r) == file_sha256 or r.get("structure", {}).get("source_sha256") == file_sha256):
                        prev_structure = r["structure"]
                    elif "structural_measurement" in r and (get_artifact_sha(r) == file_sha256 or r.get("structural_measurement", {}).get("source_sha256") == file_sha256):
                        prev_structure = r["structural_measurement"]

    # Build scoring record
    scoring_record: dict = {
        "AuthorityEffect": "None",
        "artifact": {
            "path": rel_path,
            "sha256": file_sha256,
            "language": language,
        },
        "profile": profile,
        "rubric": {
            "path": "SCORING.md",
            "sha256": SCORING_MD_SHA,
        },
        "phase": "production-and-checker-review",
        "level": "L4",
        "level_basis": "Production API craft: explicit bounded admission, typed failure modes, immutable state custody, zero bare asserts in library code, and independent unit/property/mutation test verification.",
        "gates": gates,
        "basis": {
            "G1": f"Claim URN {claim}, exact source digest, reviewed operations, dependencies and explicit authority ceiling AuthorityEffect: None.",
            "G2": f"Exact profile fixed before challenge; independent discrete operations, valid and forged inputs, shape and scalar refusals tested under {language} semantics.",
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
            "Measured peak allocation and process deadline bounds",
        ],
        "evidence": evidence,
    }
    if prev_structure is not None:
        scoring_record["structure"] = prev_structure

    scoring_raw_utf8 = json.dumps(scoring_record, indent=2, ensure_ascii=False) + "\n"
    scoring_sha = sha256_bytes(scoring_raw_utf8.encode("utf-8"))
    scoring_bytes = len(scoring_raw_utf8.encode("utf-8"))

    if is_rs:
        eng_policy = "Declared admission policy: inputs validated at public boundaries; integer bounds checked; no unadmitted float/bool on exact paths. These are admission policies, not mathematical limits."
        trust_spec = "Pinned rustc compiler and test suite. Safe Rust abstractions avoid raw pointer dereference without safety contracts."
        cost_model = "Polynomial or linear operational bounds under declared size envelopes. No unbounded recursion or unmetered allocations."
    elif ext == ".toml":
        eng_policy = "Cargo manifest adheres to declared workspace dependencies, pinned crates, and explicit feature flags."
        trust_spec = "Cargo package manager and crates.io/git source pins."
        cost_model = "Bounded configuration parsing within memory limits. Zero dynamic execution cost."
    elif ext in (".json", ".jsonl"):
        eng_policy = "Declared JSON schema validation policy: deterministic key ordering, exact numeric encoding, and immutable record custody."
        trust_spec = "Pinned JSON parser and cryptographic content digests."
        cost_model = "Bounded data receipt parsing within memory limits. Zero dynamic execution cost."
    else:
        eng_policy = "Declared admission policy: inputs validated at public boundaries; integers <= 1024 bits; no unadmitted float/bool on exact paths. These are admission policies, not mathematical limits."
        trust_spec = "Pinned CPython and test bytes. Type-based checks avoid value.__class__ and container/scalar overrides. This is not a security sandbox for arbitrary metaclass hooks, monkeypatching, hostile interpreter state, host exhaustion or deliberate reflection."
        cost_model = "Polynomial or linear operational bounds under declared size envelopes. No unbounded recursion or unmetered allocations."

    contract_record = {
        "AuthorityEffect": "None",
        "artifact": {
            "path": rel_path,
            "sha256": file_sha256,
            "language": language,
        },
        "profile": profile,
        "claim": claim,
        "role": role,
        "purpose": purpose,
        "operations": info["operations"],
        "engineering_policy": eng_policy,
        "failure_boundary": failure_boundary,
        "cost_model": cost_model,
        "scope_ceiling": "Scoped strictly to declared discrete structures. No claim of continuum completeness, general physics, or authority promotion.",
        "trust": trust_spec,
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
    if existing_doc is not None:
        try:
            document = existing_doc

            # Reconcile existing history records ONLY if corrupt/desynchronized
            for h_key in ("contract_history", "scoring_history"):
                for entry in document.get(h_key, []):
                    raw_b = entry.get("raw_utf8", "").encode("utf-8")
                    if sha256_bytes(raw_b) != entry.get("sha256") or len(raw_b) != entry.get("bytes"):
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

            # Reconcile contract
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
            else:
                curr_c_sha = get_artifact_sha(contract)
                if curr_c_sha != file_sha256:
                    if "artifact" in contract and isinstance(contract["artifact"], dict):
                        contract["artifact"]["sha256"] = file_sha256
                        contract["artifact"]["language"] = language
                    if "source_sha256" in contract:
                        contract["source_sha256"] = file_sha256
                    new_c_raw = json.dumps(contract, indent=2, ensure_ascii=False) + "\n"
                    new_c_sha = sha256_bytes(new_c_raw.encode("utf-8"))
                    new_c_bytes = len(new_c_raw.encode("utf-8"))
                    document["contract"] = contract
                    document["current_contract"] = new_c_sha
                    if not any(e.get("sha256") == new_c_sha for e in document.get("contract_history", [])):
                        document.setdefault("contract_history", []).append({
                            "sha256": new_c_sha,
                            "bytes": new_c_bytes,
                            "record": contract,
                            "raw_utf8": new_c_raw,
                            "original_paths": [f"{rel_companion}#contract"],
                        })
                else:
                    if not document.get("current_contract") and document.get("contract_history"):
                        document["current_contract"] = document["contract_history"][-1]["sha256"]

            # Atomic save
            temp_path = companion_path.with_name(f"{companion_path.name}.tmp")
            temp_path.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
            os.replace(temp_path, companion_path)
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

    temp_path = companion_path.with_name(f"{companion_path.name}.tmp")
    temp_path.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    os.replace(temp_path, companion_path)
    return companion_path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", nargs="?", help="Retained only to explain the retired interface.")
    parser.parse_args()
    print(
        "Refusing to synthesize L4E scores from static source inspection. "
        "Run `py -3.9 scripts/score_scope_contracts.py prepare` for "
        "source-pinned contracts with explicitly incomplete baseline scores.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
