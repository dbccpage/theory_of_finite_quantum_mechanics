#!/usr/bin/env python3
"""Self-contained verification script for Paper 1 (033_certified_adaptive_quantum_dynamics).

Audits cryptographic checksums (SHA256SUMS), Zenodo deposit metadata (.zenodo.json),
claim ledger mappings, executes the non-vacuous pytest suite with coverage,
and builds the Lean 4 formalization.

AuthorityEffect: None.
"""

import argparse
import ast
import re
import tempfile
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys

from scripts.rebuild_release import ARCHIVE_NAME, verify_release


REQUIRED_FILES = ['.gitignore', '.zenodo.json', '033_certified_adaptive_quantum_dynamics.aux', '033_certified_adaptive_quantum_dynamics.log', '033_certified_adaptive_quantum_dynamics.md', '033_certified_adaptive_quantum_dynamics.pdf', '033_certified_adaptive_quantum_dynamics.tex', '033_certified_adaptive_quantum_dynamics_change_log.md', '033_certified_adaptive_quantum_dynamics_claim_ledger.md', 'LICENSE', 'LICENSE-CODE', 'MANIFEST.sha256', 'README.md', 'SHA256SUMS', 'claim_ledger.yaml', 'code/caqd/__init__.py', 'code/caqd/adaptive.py', 'code/caqd/bounds.py', 'code/caqd/dynamics.py', 'code/caqd/residuals.py', 'code/caqd/spin_chains.py', 'code/pyproject.toml', 'code/tests/__init__.py', 'code/tests/conftest.py', 'code/tests/test_adaptive.py', 'code/tests/test_bounds.py', 'code/tests/test_causal_adaptive_dynamics.py', 'code/tests/test_coverage_edge_cases.py', 'code/tests/test_dynamics.py', 'code/tests/test_e2e_scenarios.py', 'code/tests/test_numerical_refusal.py', 'code/tests/test_release_integrity.py', 'code/tests/test_residuals.py', 'code/tests/test_review_regressions.py', 'code/tests/test_spin_chains.py', 'jupyter_notebooks/001_reviewer_adaptive_quantum.ipynb', 'lean4/CAQD.lean', 'lean4/CAQD/AxiomAudit.lean', 'lean4/CAQD/Core.lean', 'lean4/CAQD/Duhamel.lean', 'lean4/CAQD/ErrorBound.lean', 'lean4/CAQD/LocalDecomposition.lean', 'lean4/CAQD/ShortTimeRate.lean', 'lean4/README.md', 'lean4/axiom_report.txt', 'lean4/lake-manifest.json', 'lean4/lakefile.lean', 'lean4/lean-toolchain', 'review_observations.json', 'review_report.md', 'scripts/build_paper_artifacts.py', 'scripts/obstruction-preamble.tex', 'scripts/rebuild_release.py', 'scripts/replay_notebook.py', 'scripts/reproduce_review.py', 'tools/rebuild_release.py', 'verify_deposit.py', 'zenodo_metadata.json']

def log(msg: str) -> None:
    print(f"[VERIFY-DEPOSIT] {msg}")


def check_sha256(paper_dir) -> bool:
    """Check the entire declared inventory, rejecting empty or malformed manifests."""
    base = Path(paper_dir).resolve()
    expected = set(REQUIRED_FILES) - {"SHA256SUMS"}
    seen = set()
    try:
        lines = (base / "SHA256SUMS").read_text(encoding="utf-8").splitlines()
        for line in lines:
            if not line.strip() or line.startswith("#"):
                continue
            match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
            if match is None:
                raise ValueError("Malformed checksum record")
            digest, relative = match.groups()
            if relative not in expected or relative in seen:
                raise ValueError(f"Unexpected or duplicate manifest path: {relative}")
            target = (base / relative).resolve()
            if not target.is_relative_to(base) or not target.is_file():
                raise ValueError(f"Missing or escaping file: {relative}")
            if hashlib.sha256(target.read_bytes()).hexdigest() != digest:
                raise ValueError(f"Hash mismatch: {relative}")
            seen.add(relative)
        if not expected or seen != expected:
            raise ValueError(f"Manifest inventory mismatch; missing: {sorted(expected - seen)}")
    except (OSError, ValueError) as exc:
        print(f"FAIL: {exc}")
        return False
    print(f"OK: all {len(seen)} declared package hashes match")
    return True


def check_zenodo_metadata(paper_dir: Path) -> bool:
    """Check aligned deposit metadata, declared licenses, and package version."""
    zenodo_file = paper_dir / ".zenodo.json"
    if not zenodo_file.exists():
        log("FAIL: .zenodo.json not found.")
        return False

    try:
        with open(zenodo_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        log(f"FAIL: JSON parse error in .zenodo.json: {e}")
        return False

    required_keys = ["title", "description", "creators", "access_right", "license", "keywords"]
    for k in required_keys:
        if k not in data or not data[k]:
            log(f"FAIL: Missing required Zenodo field: {k}")
            return False

    try:
        companion = json.loads((paper_dir / "zenodo_metadata.json").read_text(encoding="utf-8"))
        shared = [*required_keys, "version", "publication_date", "upload_type", "publication_type"]
        if any(data.get(key) != companion.get(key) for key in shared):
            raise ValueError("deposit metadata files disagree")
        if data["license"] != "cc-by-4.0" or data["publication_type"] != "preprint":
            raise ValueError("unexpected document license or publication type")
        if "HEURISTIC_UNCERTIFIED" not in data["description"]:
            raise ValueError("numerical certification scope missing from description")
        if {item["id"] for item in companion["rights"]} != {"cc-by-4.0", "apache-2.0"}:
            raise ValueError("rights must match LICENSE and LICENSE-CODE")
        init_tree = ast.parse((paper_dir / "code/caqd/__init__.py").read_text(encoding="utf-8"))
        init_version = next(ast.literal_eval(node.value) for node in init_tree.body
                            if isinstance(node, ast.Assign)
                            and any(isinstance(t, ast.Name) and t.id == "__version__" for t in node.targets))
        project = (paper_dir / "code/pyproject.toml").read_text(encoding="utf-8")
        project_version = re.search(r'^version = "([^"]+)"$', project, re.M).group(1)
        if init_version != project_version or data["version"] != project_version:
            raise ValueError("package and deposit versions disagree")
        if 'license = { text = "Apache-2.0" }' not in project:
            raise ValueError("project license declaration disagrees")
        if "Apache License" not in (paper_dir / "LICENSE-CODE").read_text(encoding="utf-8"):
            raise ValueError("code license file disagrees")
    except (OSError, ValueError, KeyError, TypeError, StopIteration, AttributeError) as exc:
        log(f"FAIL: metadata consistency: {exc}")
        return False
    log("OK: deposit descriptions, authors, licenses, and versions agree.")
    return True


def check_claim_ledger(paper_dir) -> bool:
    """Check stable IDs and real source/test associations; not proof entailment."""
    base = Path(paper_dir)
    try:
        import yaml
        data = yaml.safe_load((base / "claim_ledger.yaml").read_text(encoding="utf-8"))
        claims = data["claims"]
        ids = [claim.get("id", claim.get("claim_id")) for claim in claims]
        markdown = (base / "033_certified_adaptive_quantum_dynamics_claim_ledger.md").read_text(encoding="utf-8")
        manuscript = (base / "033_certified_adaptive_quantum_dynamics.md").read_text(encoding="utf-8")
        expected = [f"PO033-C{i}" for i in range(1, 7)]
        if len(ids) != len(set(ids)) or set(ids) != set(expected):
            raise ValueError("Missing, duplicate, or unexpected claim IDs")
        if any(re.search(r"(?<![A-Za-z0-9_-])" + re.escape(cid) + r"(?![A-Za-z0-9_-])", markdown) is None for cid in ids):
            raise ValueError("Claim ID missing from Markdown ledger")
        for claim in claims:
            if claim["id"] not in manuscript or not claim["status"] or not claim["assumptions"]:
                raise ValueError("claim scope or manuscript association missing")
            evidence = claim.get("code_evidence")
            if evidence:
                module = evidence["module"]
                module_file = base / "code" / (module.replace(".", "/") + ".py")
                definitions = {node.name for node in ast.walk(ast.parse(module_file.read_text(encoding="utf-8")))
                               if isinstance(node, (ast.FunctionDef, ast.ClassDef))}
                if not set(evidence["functions"]) <= definitions:
                    raise ValueError(f"unknown function in {module}")
                for selector in evidence["tests"]:
                    path, function = selector.split("::")
                    target = (base / "code" / path).resolve()
                    if not target.is_relative_to((base / "code/tests").resolve()):
                        raise ValueError("escaping test mapping")
                    names = {node.name for node in ast.walk(ast.parse(target.read_text(encoding="utf-8")))
                             if isinstance(node, ast.FunctionDef)}
                    if function not in names:
                        raise ValueError(f"unknown test selector: {selector}")
            formal = claim.get("lean4_formalization")
            if formal:
                source = (base / "lean4" / (formal["module"].replace(".", "/") + ".lean")).read_text(encoding="utf-8")
                if not formal["scope"] or not formal["audit_status"]:
                    raise ValueError("Lean scope or audit provenance missing")
                for theorem in formal["theorems"]:
                    if re.search(r"\btheorem\s+" + re.escape(theorem) + r"\b", source) is None:
                        raise ValueError(f"unknown Lean theorem: {theorem}")
    except Exception as exc:
        print(f"FAIL: claim ledger structure: {exc}")
        return False
    print("OK: six claim IDs and source/test associations agree; no semantic entailment check")
    return True


def run_pytest(paper_dir) -> bool:
    """Run package tests with an enforced coverage threshold and isolated scratch."""
    with tempfile.TemporaryDirectory(prefix="coda-caqd-verify-") as scratch:
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1",
                   COVERAGE_FILE=str(Path(scratch) / ".coverage"))
        cmd = [sys.executable, "-m", "pytest", "-q",
               "-p", "no:cacheprovider", "--basetemp=" + str(Path(scratch) / "pytest"),
               "--cov=caqd", "--cov-report=term", "--cov-fail-under=95"]
        result = subprocess.run(cmd, cwd=Path(paper_dir) / "code", env=env,
                                capture_output=True, text=True, encoding="utf-8", errors="replace")
        print(result.stdout)
        if result.returncode:
            print(result.stderr)
        return result.returncode == 0


def run_lake(paper_dir) -> bool:
    """Build from the package root; a stored report is not a live proof audit."""
    try:
        result = subprocess.run(["lake", "build"], cwd=Path(paper_dir) / "lean4",
                                capture_output=True, text=True, encoding="utf-8", errors="replace")
    except OSError as exc:
        print(f"FAIL: Lean unavailable: {exc}")
        return False
    output = result.stdout + result.stderr
    print(output)
    if result.returncode or "sorryAx" in output or "declaration uses 'sorry'" in output:
        return False
    audit = subprocess.run(["lake", "env", "lean", "CAQD/AxiomAudit.lean"],
                           cwd=Path(paper_dir) / "lean4", capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
    audit_output = audit.stdout + audit.stderr
    print(audit_output)
    selectors = re.findall(r"#print axioms (CAQD\.\w+)", (Path(paper_dir) / "lean4/CAQD/AxiomAudit.lean").read_text())
    if (audit.returncode or "sorryAx" in audit_output
            or any(f"'{name}'" not in audit_output for name in selectors)):
        return False
    print("OK: fresh Lean build and axiom audit; conditional scope is recorded in the ledger")
    return True


def check_artifact_association(paper_dir: Path) -> bool:
    """Check the recorded source digest, not mathematical correctness or layout."""
    digest = hashlib.sha256((paper_dir / "033_certified_adaptive_quantum_dynamics.md").read_bytes()).hexdigest()
    marker = "manuscript-sha256:" + digest
    try:
        tex = (paper_dir / "033_certified_adaptive_quantum_dynamics.tex").read_text(encoding="utf-8")
        if marker not in tex:
            raise ValueError("TeX source digest differs from manuscript")
        info = subprocess.run(["pdfinfo", str(paper_dir / "033_certified_adaptive_quantum_dynamics.pdf")],
                              capture_output=True, text=True, check=True)
        if marker not in info.stdout:
            raise ValueError("PDF source digest differs from manuscript")
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        log(f"FAIL: artifact association: {exc}")
        return False
    log("OK: TeX and PDF carry the canonical manuscript digest; layout requires visual review")
    return True


def run_review_replays(paper_dir: Path) -> bool:
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", MPLBACKEND="Agg",
               OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1")
    for args in [("scripts/reproduce_review.py", "--check"),
                 ("scripts/replay_notebook.py",),
                 ("scripts/replay_notebook.py", "--from-notebook-dir")]:
        process = subprocess.run([sys.executable, *args], cwd=paper_dir, env=env,
                                 capture_output=True, text=True, encoding="utf-8", errors="replace")
        print(process.stdout)
        if process.returncode:
            print(process.stderr)
            return False
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skip-lean", action="store_true", help="Explicit scoped verification without a fresh Lean build/audit")
    parser.add_argument("--extracted", action="store_true", help="Verify the extracted payload without its outer ZIP")
    args = parser.parse_args()
    paper_dir = Path(__file__).resolve().parent
    log(f"Starting deposit verification in: {paper_dir}")

    step1 = check_zenodo_metadata(paper_dir)
    step2 = check_claim_ledger(paper_dir)
    step3 = run_pytest(paper_dir)
    if args.skip_lean:
        log("SKIPPED: fresh Lean build and axiom audit (--skip-lean explicitly selected)")
        step4 = True
    else:
        step4 = run_lake(paper_dir)
    step5 = check_sha256(paper_dir)
    step6 = verify_release(paper_dir, None if args.extracted else paper_dir / ARCHIVE_NAME)
    step7 = check_artifact_association(paper_dir)
    step8 = run_review_replays(paper_dir)

    all_passed = all((step1, step2, step3, step4, step5, step6, step7, step8))
    if all_passed:
        scope = "Lean SKIPPED; " if args.skip_lean else "fresh conditional Lean checks included; "
        log(f"SUCCESS: Scoped package checks passed ({scope}not numerical certification or publication sign-off).")
        return 0
    else:
        log("FAILURE: One or more deposit checks failed.")
        return 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())
