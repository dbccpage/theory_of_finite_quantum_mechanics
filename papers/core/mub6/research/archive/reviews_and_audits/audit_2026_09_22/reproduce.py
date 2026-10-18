"""Adversarial audit probes, not a mathematical certificate or production verifier.

Run from any directory with Python 3.11+; all generated inputs/results stay in scratch.
AuthorityEffect: None.
stated region only; mints no authority
"""
from __future__ import annotations

import ast
import copy
import hashlib
import json
import re
import subprocess
import sys
from fractions import Fraction as Q
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "scratch/audit_2026_09_22"
OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(ROOT / "omega_engine/crates"))
sys.path.insert(0, str(ROOT))
from mub_verify import g1_classification_verifier as classification
from mub_verify import g1_case_verifier as cases
from mub_verify import verify_all_receipts as receipts
from mub_verify import target_b3_manifold_integration as b3
from mub_verify import target_b1_continuous_chaining as b1
from mub_verify.l1_governor import Edge, ConstraintGraph, Cochain1, compute_phi1, L1SymbolGameGovernor
from mub_verify.packet_firewall import PacketFirewallHost, DerivationStep


def dump(name, data):
    path = OUT / name
    path.write_text(json.dumps(data, indent=2, ensure_ascii=True, default=str) + "\n", encoding="utf-8")
    return path


def captured(fn):
    try:
        return {"returned": fn()}
    except Exception as exc:
        return {"exception": type(exc).__name__, "message": str(exc)}


def sha(data):
    return hashlib.sha256(data).hexdigest()


report = {"head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
          "scope": "audit observations; not proof of classification or non-extendibility"}
manifest = json.loads((ROOT / "artifacts/manifest.json").read_text(encoding="utf-8"))
report["receipt_hashes"] = []
for entry in manifest["receipts"]:
    raw = (ROOT / "artifacts" / entry["filename"]).read_bytes()
    report["receipt_hashes"].append({"filename": entry["filename"], "expected": entry["sha256"],
        "raw": sha(raw), "lf": sha(raw.replace(b"\r\n", b"\n")),
        "lf_matches": sha(raw.replace(b"\r\n", b"\n")) == entry["sha256"]})
report["all_receipts_explicit_root"] = receipts.verify_all_receipts(ROOT / "artifacts")
report["all_receipts_default_root"] = receipts.verify_all_receipts()
duplicate_manifest = copy.deepcopy(manifest)
duplicate_manifest["receipts"] = [copy.deepcopy(manifest["receipts"][0]) for _ in range(10)]
report["duplicate_receipts_accepted"] = receipts.verify_all_receipts(
    ROOT / "artifacts", dump("duplicate_manifest.json", duplicate_manifest))

original_classification = json.loads((ROOT / "research/g1_foundation/classification_manifest.json").read_text(encoding="utf-8"))
report["classification_digest_fields"] = [key for key in original_classification if "hash" in key or "sha" in key]
fake = copy.deepcopy(original_classification)
fake["schema"] = "wrong-schema"
for theorem in fake["theorems"]:
    theorem.update(name="Missing.theorem", lean_file="missing.lean", statement="False", axioms=["InventedAxiom"])
for branch in fake["eliminated_subvarieties"]:
    branch["witness_poly"] = "0 = 1"
report["fabricated_classification_accepted"] = captured(lambda: classification.verify_classification_manifest(
    dump("fabricated_classification.json", fake)))
ledger = json.loads((ROOT / "research/g1_foundation/case_ledger.json").read_text(encoding="utf-8"))
ledger["branches"] = [{} for _ in range(6)]
report["empty_branch_payloads_accepted"] = captured(lambda: cases.verify_case_ledger(dump("empty_branches.json", ledger)))

original_b3 = json.loads((ROOT / "artifacts/mub_target_b3_manifold_integration_receipt.json").read_text(encoding="utf-8"))
fake_b3 = copy.deepcopy(original_b3)
fake_b3["discrete_partition_summary"].update(min_margin="-1", total_volume="0")
fake_b3["loop_holonomy_circulation_summary"].update(deltoid_circulation_phi1=0, composite_circulation_phi1=0)
fake_b3["master_unified_obstruction"]["total_moduli_sample_points_checked"] = 0
report["inconsistent_b3_summaries_accepted"] = captured(lambda: b3.audit_target_b3_receipt(fake_b3))

graph = ConstraintGraph(vertices=("a", "b", "c"), edges=(Edge("a", "b"), Edge("b", "c"), Edge("c", "a")))
governor = L1SymbolGameGovernor(graph)
for edge in graph.edges:
    governor.step_assert(edge.u, edge.v, Q(1))
before = governor.primary_obstruction()
verdict = governor.step_cut(proposed_claims={})
report["claim_erasure_cut"] = {"before": str(before), "after": str(governor.primary_obstruction()),
    "admitted": verdict.admitted, "status": verdict.status, "remaining_claims": len(governor.edge_claims)}

# Deliberately hostile floating input: audit input only, never certifying data.
def _probe_float_weight():
    float_graph = ConstraintGraph(vertices=graph.vertices,
        edges=(Edge("a", "b", 0.1), Edge("b", "c"), Edge("c", "a")))
    value, potentials = compute_phi1(float_graph, Cochain1({e.key: Q(1) for e in graph.edges}))
    return {"accepted": True, "value": str(value), "output_type": type(value).__name__,
        "exact_decimal_weight_expected_objective": "3/10", "equals_decimal_expected": value == Q(3, 10)}
report["float_weight_laundering"] = captured(_probe_float_weight)
step = DerivationStep(op="UNDECLARED", position=0, rule_id="missing", substitution={},
                     pre_state_hash="bad", post_state_hash="bad", content="UNDECLARED invalid")
report["carrier_only_verify_step"] = vars(PacketFirewallHost().verify_step(step))

# Independent sparse coefficient arithmetic (no finite point sampling).
def add(*polys):
    result = {}
    for poly in polys:
        for exp, coefficient in poly.items():
            result[exp] = result.get(exp, Q(0)) + coefficient
    return {exp: q for exp, q in result.items() if q}


def scale(poly, q):
    return {exp: coefficient * q for exp, coefficient in poly.items() if coefficient * q}


def mul(left, right):
    terms = []
    for a, qa in left.items():
        for b, qb in right.items():
            terms.append({tuple(x + y for x, y in zip(a, b)): qa * qb})
    return add(*terms)


one, x, y = {(0, 0): Q(1)}, {(1, 0): Q(1)}, {(0, 1): Q(1)}
circle = add(mul(x, x), mul(y, y), scale(one, -1))
upper_g = add(x, scale(one, -2))
lower_g = add(scale(x, -1), scale(one, -2))
upper_sos = scale(add(mul(upper_g, upper_g), mul(y, y)), Q(1, 3))
lower_sos = scale(add(mul(lower_g, lower_g), mul(y, y)), Q(1, 3))
identities = {
    "upper_rhs_plus_one": add(scale(circle, Q(-1, 3)), upper_sos, scale(upper_g, Q(4, 3)), one),
    "lower_rhs_plus_one": add(scale(circle, Q(-1, 3)), lower_sos, scale(lower_g, Q(4, 3)), one),
    "annihilated_rhs_minus_one": add(scale(circle, -1), mul(x, x), mul(y, y), scale(one, -1)),
}
one5 = {(0,) * 5: Q(1)}
xs = [{tuple(int(i == j) for i in range(5)): Q(1)} for j in range(5)]
identities["all_ones_rhs_minus_one"] = add(scale(add(one5, *xs), Q(1, 6)),
    *(scale(add(xj, scale(one5, -1)), Q(-1, 6)) for xj in xs), scale(one5, -1))
report["exact_polynomial_identity_residuals"] = {key: {str(e): str(q) for e, q in poly.items()}
    for key, poly in identities.items()}
report["exact_constants"] = {"epsilon_minus_L_delta": str(Q(37249, 90000) - Q(85, 9) * Q(1, 1000)),
    "six_margins": str(6 * Q(12133, 30000)),
    "60_step_erosion": str(Q(37249, 90000) - 60 * Q(85, 9) * Q(1, 1000))}

diagonal = [Q(1), Q(-1), Q(1), Q(1), Q(1), Q(1)]
ray = [Q(1)] + [Q(0)] * 5
report["nonidentity_unitary_fixed_ray"] = {
    "diagonal": [str(x) for x in diagonal],
    "unitary": all(x * x == 1 for x in diagonal),
    "nonidentity": any(x != 1 for x in diagonal),
    "fixes_first_coordinate_vector": [a * b for a, b in zip(diagonal, ray)] == ray,
}

chain = b1.build_dense_chain_sample()
gap_point = Q(1, 122)
report["chain_coverage_gap"] = {
    "audit": b1.ContinuousChainingAuditor().audit_sample_chain(chain),
    "gap_point": str(gap_point),
    "covered_by_any_sample_ball": any(abs(p.t - gap_point) <= p.delta for p in chain),
    "sample_spacing": str(chain[1].t - chain[0].t),
    "sum_adjacent_radii": str(chain[0].delta + chain[1].delta),
    "nearest_distance": str(min(abs(p.t - gap_point) for p in chain)),
}

tracked = subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).splitlines()
source_records = []
ast_findings = []
rust_hits = []
lean_placeholders = []
for name in tracked:
    if not (name.startswith("omega_engine/crates/mub_verify/") or
            name.startswith("omega_engine/crates_rs/omega_mub/") or name.startswith("lean4/") or
            name in {"research/paper.md", "research/mub6_roadmap.md"} or name.startswith("research/g1_foundation/")):
        continue
    path = ROOT / name
    if path.suffix not in {".py", ".rs", ".lean", ".json", ".md", ".toml"} or not path.is_file():
        continue
    data = path.read_bytes()
    source_records.append({"path": name, "sha256_lf": sha(data.replace(b"\r\n", b"\n"))})
    text = data.decode("utf-8-sig")
    if path.suffix == ".py":
        tree = ast.parse(text, filename=name)
        for node in ast.walk(tree):
            kind = None
            if isinstance(node, ast.Constant) and isinstance(node.value, (float, complex)):
                kind = "inexact_numeric_literal"
            elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"float", "complex"}:
                kind = "inexact_constructor"
            elif isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
                kind = "division_review"
            elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "Fraction" and len(node.args) == 1:
                kind = "Fraction_input_boundary_review"
            if kind:
                ast_findings.append({"path": name, "line": node.lineno, "kind": kind, "expression": ast.unparse(node)[:220]})
    if path.suffix == ".rs":
        for i, line in enumerate(text.splitlines(), 1):
            if re.search(r"\b(f32|f64|from_float|to_f64)\b", line) and not line.lstrip().startswith("//"):
                rust_hits.append({"path": name, "line": i, "source": line.strip()[:220]})
    if path.suffix == ".lean":
        # Nested Lean block comments, then line comments; retain line numbers.
        chars = list(text)
        depth = 0
        i = 0
        while i < len(text):
            if text[i:i+2] == "/-":
                depth += 1
                chars[i:i+2] = "  "
                i += 2
            elif depth and text[i:i+2] == "-/":
                depth -= 1
                chars[i:i+2] = "  "
                i += 2
            elif depth:
                if text[i] != "\n":
                    chars[i] = " "
                i += 1
            else:
                i += 1
        stripped = "".join(chars)
        for i, line in enumerate(stripped.splitlines(), 1):
            code = line.split("--", 1)[0]
            if re.search(r"\b(axiom|sorry|admit|native_decide|implemented_by)\b", code):
                lean_placeholders.append({"path": name, "line": i, "source": code.strip()})
dump("source_hashes.json", {"head": report["head"], "files": source_records})
dump("static_scan.json", {"python_ast": ast_findings, "rust_float_tokens": rust_hits, "lean_trust_tokens": lean_placeholders})
report["static_scan_counts"] = {"source_files_hashed": len(source_records), "python_ast_review_sites": len(ast_findings),
    "python_inexact_literals": sum(x["kind"] == "inexact_numeric_literal" for x in ast_findings),
    "python_inexact_constructors": sum(x["kind"] == "inexact_constructor" for x in ast_findings),
    "rust_float_token_lines": len(rust_hits), "lean_trust_tokens": len(lean_placeholders)}
dump("probe_results.json", report)
print(json.dumps(report, indent=2, ensure_ascii=True, default=str))
