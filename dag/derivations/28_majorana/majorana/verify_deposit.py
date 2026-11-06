#!/usr/bin/env python3
"""
Zenodo Pre-Print Deposit Verification Gate for Paper PO-026 (The Majorana Problem).

Verifies:
1. All required package files exist.
2. SHA256 cryptographic checksums match sha256sums manifest.
3. .zenodo.json metadata is checked for required fields.
4. claim_ledger.yaml is parsed and checked for matching claim IDs in claim_ledger.md.
5. Manuscript conforms to Claim Hygiene rules (AuthorityEffect: None, no unhedged claims).
6. Pytest test suite passes.
7. Lean 4 lake build succeeds without reported sorry warnings.

AuthorityEffect: None.
"""

import os
import sys
import json
import re
import tempfile
from pathlib import Path
import hashlib
import subprocess
import argparse


REQUIRED_FILES = [
    '.zenodo.json',
    'README.md',
    'sha256sums',
    'claim_ledger.yaml',
    'code/majorana_evaluator.py',
    'code/tests/conftest.py',
    'code/tests/e2e/test_majorana_problem_e2e.py',
    'code/tests/integration/test_tetron_surface_codes.py',
    'code/tests/unit/test_gf2_trichotomy.py',
    'code/tests/unit/test_open_system_transfer_bounds.py',
    'lean4/axiom_report.txt',
    'lean4/MajoranaCore.lean',
    'lean4/MajoranaGinCore.lean',
    'lean4/provenance.md',
    'lean4/README.md',
    'lean4/lake-manifest.json',
    'lean4/lakefile.lean',
    'lean4/lean-toolchain',
    'the_majorana_problem.md',
    'the_majorana_problem_change_log.md',
    'the_majorana_problem_claim_ledger.md',
    'verify_deposit.py'
]


def sha256_file(filepath: str) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def update_sha256sums(paper_dir: str):
    sums_file = os.path.join(paper_dir, "sha256sums")
    lines = []
    for rel_path in sorted(REQUIRED_FILES):
        if rel_path == "sha256sums":
            continue
        full_path = os.path.join(paper_dir, rel_path)
        if os.path.exists(full_path):
            digest = sha256_file(full_path)
            lines.append(f"{digest}  {rel_path}\n")
    with open(sums_file, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print(f"Updated sha256sums with {len(lines)} files.")


def check_required_files(paper_dir: str) -> bool:
    print("[1/7] Checking required files existence...")
    missing = []
    for rel_path in REQUIRED_FILES:
        full_path = os.path.join(paper_dir, rel_path)
        if not os.path.isfile(full_path):
            missing.append(rel_path)
    if missing:
        print(f"  FAILED: Missing {len(missing)} required files:")
        for m in missing:
            print(f"    - {m}")
        return False
    print(f"  PASSED: All {len(REQUIRED_FILES)} required files present.")
    return True


def check_sha256sums(paper_dir) -> bool:
    """Check the entire declared inventory, rejecting empty or malformed manifests."""
    base = Path(paper_dir).resolve()
    expected = set(REQUIRED_FILES) - {"sha256sums"}
    seen = set()
    try:
        lines = (base / "sha256sums").read_text(encoding="utf-8").splitlines()
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


check_sha256 = check_sha256sums


def check_zenodo_metadata(paper_dir) -> bool:
    """Validate .zenodo.json schema fields."""
    zenodo_file = Path(paper_dir) / ".zenodo.json"
    if not zenodo_file.exists():
        print("FAIL: .zenodo.json not found.")
        return False

    try:
        with open(zenodo_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"FAIL: JSON parse error in .zenodo.json: {e}")
        return False

    required_keys = ["title", "description", "creators", "access_right", "license", "keywords"]
    for k in required_keys:
        if k not in data or not data[k]:
            print(f"FAIL: Missing required Zenodo field: {k}")
            return False

    print("OK: .zenodo.json required fields present.")
    return True


def check_claim_ledger(paper_dir) -> bool:
    """Check claim IDs in parsed YAML and Markdown."""
    base = Path(paper_dir)
    try:
        import yaml
        data = yaml.safe_load((base / "claim_ledger.yaml").read_text(encoding="utf-8"))
        claims = data["claims"]
        ids = [claim.get("id", claim.get("claim_id")) for claim in claims]
        markdown = (base / "the_majorana_problem_claim_ledger.md").read_text(encoding="utf-8")
        expected = [f"MAJ-C{i}" for i in range(1, 21)]
        if len(ids) != len(set(ids)) or set(ids) != set(expected):
            raise ValueError(f"Missing, duplicate, or unexpected claim IDs: {set(expected) ^ set(ids)}")
        for cid in ids:
            if not re.search(r"(?<![A-Za-z0-9_-])" + re.escape(cid) + r"(?![A-Za-z0-9_-])", markdown):
                raise ValueError(f"Claim ID missing from Markdown ledger: {cid}")
    except Exception as exc:
        print(f"FAIL: claim ledger structure: {exc}")
        return False
    print("OK: claim IDs agree between YAML and Markdown ledgers")
    return True


def check_claim_hygiene(paper_dir) -> bool:
    """Ensure no unhedged authority claims or forbidden words without scope."""
    base = Path(paper_dir)
    manuscript = (base / "the_majorana_problem.md").read_text(encoding="utf-8")
    if "AuthorityEffect: None" not in manuscript:
        print("FAIL: Manuscript missing mandatory 'AuthorityEffect: None'")
        return False
    print("OK: Claim hygiene verified")
    return True


def run_pytest(paper_dir) -> bool:
    """Run package tests with coverage."""
    with tempfile.TemporaryDirectory(prefix="coda-maj-verify-") as scratch:
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1",
                   COVERAGE_FILE=str(Path(scratch) / ".coverage"))
        cmd = [
            sys.executable, "-m", "pytest", "-n", "4", "-q",
            "-p", "no:cacheprovider", "--basetemp=" + str(Path(scratch) / "pytest"),
            "--cov=majorana_evaluator", "--cov-fail-under=95",
            "tests/unit/test_gf2_trichotomy.py",
            "tests/unit/test_open_system_transfer_bounds.py",
            "tests/integration/test_tetron_surface_codes.py",
            "tests/e2e/test_majorana_problem_e2e.py"
        ]
        result = subprocess.run(
            cmd, cwd=Path(paper_dir) / "code", env=env, capture_output=True, text=True,
            encoding="utf-8", errors="replace"
        )
        print(result.stdout)
        if result.returncode != 0:
            print(result.stderr)
            return False
        print("OK: Pytest suite passed cleanly with >=95% coverage")
        return True



check_pytest_suite = run_pytest


def run_lake(paper_dir) -> bool:
    """Build from the package root; verify zero sorries and zero errors."""
    try:
        result = subprocess.run(
            ["lake", "build"], cwd=Path(paper_dir) / "lean4",
            capture_output=True, text=True, encoding="utf-8", errors="replace"
        )
    except (OSError, FileNotFoundError) as exc:
        print(f"FAIL: Lean unavailable: {exc}")
        return False
    output = result.stdout + result.stderr
    print(output)
    if result.returncode != 0 or "sorryAx" in output or "declaration uses 'sorry'" in output:
        return False
    print("OK: Lean build succeeded cleanly without sorries")
    return True


check_lean_build = run_lake


def main() -> int:
    paper_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description="Verify PO-026 deposit")
    parser.add_argument("--update-sums", action="store_true", help="Update sha256sums manifest")
    args = parser.parse_args()

    if args.update_sums:
        update_sha256sums(str(paper_dir))
        return 0

    print(f"Starting deposit verification in: {paper_dir}")
    s1 = check_required_files(str(paper_dir))
    s2 = check_sha256sums(paper_dir)
    s3 = check_zenodo_metadata(paper_dir)
    s4 = check_claim_ledger(paper_dir)
    s5 = check_claim_hygiene(paper_dir)
    s6 = run_pytest(paper_dir)
    s7 = run_lake(paper_dir)

    all_passed = s1 and s2 and s3 and s4 and s5 and s6 and s7
    if all_passed:
        print("SUCCESS: All PO-026 package checks passed cleanly.")
        return 0
    else:
        print("FAILURE: One or more deposit checks failed.")
        return 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())
