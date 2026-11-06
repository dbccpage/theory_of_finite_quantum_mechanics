"""Replay this scoped evidence; unrelated full-DAG failures stay separately reported.

Run with the repository Python environment. --lean-bin may select an installed
Lean executable; otherwise use the declared toolchain under ELAN_HOME.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
LEAN_SOURCE = ROOT / "lean4/CHSHNormAdmission.lean"
THEOREMS = """unitEffect_iff_dual_bound correlator_bound dual_sum_difference_bound
algebraic_bound chsh_sq_le_eight chsh_le_two_sqrt_two reconstructed_polarization
inner_product_implies_parallelogram probability_nonnegative probability_normalized
marginal_alice marginal_bob probability_recovers_correlator deterministic_local_bound
positive_mixture_bound l1_effect_plus l1_effect_minus l1_pr_witness
l1_fails_parallelogram linfty_effect_first linfty_effect_second linfty_pr_witness
l2_effect l2_norm_sq l2_parallelogram l2_upper_bound l2_witness_effects l2_attainment""".split()


def run(command, cwd=ROOT, env=None):
    p = subprocess.run(command, cwd=cwd, env=env, capture_output=True,
                       text=True, encoding="utf-8", errors="replace", timeout=600)
    return {"command": [str(x) for x in command], "cwd": str(cwd),
            "exit_code": p.returncode, "stdout": p.stdout, "stderr": p.stderr}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lean-bin", type=Path)
    args = parser.parse_args()
    toolchain = (ROOT / "lean4/lean-toolchain").read_text().strip()
    elan = Path(os.environ.get("ELAN_HOME", Path.home() / ".elan"))
    binary = args.lean_bin or (elan / "toolchains" /
        toolchain.replace("/", "--").replace(":", "---") / "bin" /
        ("lean.exe" if os.name == "nt" else "lean"))
    if not binary.is_file():
        parser.error("declared Lean binary not found; supply --lean-bin")
    env = os.environ.copy()
    env["LEAN_PATH"] = os.pathsep.join(str(p) for p in [
        ROOT / "lean4/b/lib/lean",
        *sorted((ROOT / "lean4/.lake/packages").glob("*/.lake/build/lib/lean")),
    ])
    print("Checking Lean declarations and axiom dependencies...", flush=True)
    lean = run([str(binary), "CHSHNormAdmission.lean"], ROOT / "lean4", env)
    reported = dict(re.findall(
        r"'CHSHNormAdmission\.([^']+)' depends on axioms: \[([^\]]*)\]", lean["stdout"]))
    axioms = {k: sorted(filter(None, (s.strip() for s in v.split(","))))
              for k, v in reported.items()}
    allowed = {"propext", "Classical.choice", "Quot.sound"}
    axiom_ok = set(axioms) == set(THEOREMS) and all(set(a) <= allowed for a in axioms.values())
    hole_free = not re.search(r"\b(sorry|admit|axiom)\b", LEAN_SOURCE.read_text(encoding="utf-8"))
    print("Checking exact replay, negative controls, and atlas...", flush=True)
    checks = {
        "lean": lean,
        "tests": run([sys.executable, "-m", "pytest", "-q",
            "code/python/tests/test_chsh_norm_admission.py",
            "code/python/tests/test_qm_atlas_loc.py",
            "--basetemp=.pytest_cache/chsh_verification_tmp"]),
        "atlas": run([sys.executable, "scripts/verify_qm_atlas_loc.py"]),
        "dag_structure_views": run([sys.executable, "dag/validate_derivation_dag.py",
                                    "--repo-root", ".", "--no-files"]),
    }
    module_path = ROOT / "code/python/src/qm/chsh_norm_admission.py"
    spec = importlib.util.spec_from_file_location("chsh_receipt_replay", module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    replay = module.replay()
    tracked_inputs = [LEAN_SOURCE, module_path, Path(__file__),
        ROOT / "code/python/tests/test_chsh_norm_admission.py",
        ROOT / "lean4/lean-toolchain", ROOT / "lean4/lake-manifest.json",
        ROOT / "lean4/lakefile.lean", ROOT / "dag/derivation_dag.json",
        ROOT / "dag/derivations/10_finite_qm_core/tfq_2621_chsh_norm_admission_comparison.md",
        HERE / "dag_validation.json", HERE / "dag_validation_baseline.json"]
    passed = axiom_ok and hole_free and all(c["exit_code"] == 0 for c in checks.values())
    receipt = {
        "schema": "chsh-norm-admission-verification/1",
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "Conditional norm/dual theorems and exact finite controls only; no selection of the admitted premises.",
        "scope_passed": passed,
        "toolchain": toolchain,
        "lean_version": run([str(binary), "--version"])["stdout"].strip(),
        "checks": checks,
        "expected_theorems": THEOREMS,
        "axiom_audit_passed": axiom_ok,
        "axiom_dependencies": axioms,
        "no_source_holes_or_new_axioms": hole_free,
        "finite_replay": replay,
        "source_sha256": {str(p.relative_to(ROOT)).replace(os.sep, "/"):
                          hashlib.sha256(p.read_bytes()).hexdigest() for p in tracked_inputs},
        "full_repository_dag_validation": json.loads((HERE / "dag_validation.json").read_text())["full_reference_validation"],
        "limitations": ["Full DAG reference validation has pre-existing failures; see separate comparison.",
                        "No derivation of carriers, real scalars, norm, effects or probability rule from Genesis.",
                        "Parallelogram law is an explicit premise of the general quadratic bound.",
                        "Negative controls are tests of invalid data, not a proof of minimal assumptions."],
    }
    (HERE / "verification.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"scope_passed": passed, "theorems": len(axioms),
                      "checks": {k: v["exit_code"] for k, v in checks.items()}}))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
