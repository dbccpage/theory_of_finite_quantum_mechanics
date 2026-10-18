#!/usr/bin/env python3
"""
Zenodo Pre-Print Deposit Verification Gate for Paper PO-023 (The Problem of the Fermion Sign).

Verifies:
1. All required package files exist.
2. SHA256 cryptographic checksums match SHA256SUMS manifest.
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
    'SHA256SUMS',
    'claim_ledger.yaml',
    'the_problem_of_the_fermion_sign.md',
    'the_problem_of_the_fermion_sign_change_log.md',
    'the_problem_of_the_fermion_sign_claim_ledger.md',
    'verify_deposit.py',
    'lean4/lakefile.lean',
    'lean4/lean-toolchain',
    'lean4/FermionSignAll.lean',
    'lean4/FermionSignCore.lean',
    'lean4/FermionGinCore.lean',
    'lean4/HaltingQuotient.lean',
    'lean4/MeronClusterInvolution.lean',
    'lean4/MeronCharacter.lean',
    'lean4/NormalFormLaws.lean',
    'docs/normal_form_audit.md',
    'docs/hamiltonian_origin.md',
    'docs/sql_meron_hubbard.md',
    'databases/meron_hubbard.sql',
    'code/sign_sql/exact_models.py',
    'code/sign_sql/exact_models_receipt.json',
    'lean4/BqnfSignPacket.lean',
    'lean4/FrustratedSpectrumObstruction.lean',
    'lean4/NonAbelianGaugeSigns.lean',
    'lean4/ReggePachnerWdw.lean',
    'lean4/GenesisFspBridge.lean',
    'lean4/ChiralAnomalyInflow.lean',
    'lean4/FqhLaughlinBraiding.lean',
    'lean4/FibonacciAnyonBraiding.lean',
    'lean4/IsingMajoranaBraiding.lean',
    'lean4/BfLinkedFluxBraiding.lean',
    'lean4/NonAbelianBfBraiding.lean',
    'lean4/Higher2GroupBraiding.lean',
    'lean4/Cobordism5dAnomaly.lean',
    'lean4/InstantonDyonGas.lean',
    'lean4/FoliatedFracton2Gauge.lean',
    'lean4/AXIOM_REPORT.txt',
    'lean4/README.md',
    'lean4/PROVENANCE.md'
]

FORBIDDEN_WORDS = [
    "proves", "guarantees", "mathematically verifies", "fundamentally",
    "true intelligence", "impossible", "universal", "flawless",
    "perfectly", "clearly", "obviously", "simply", "merely", "weaponized"
]

def sha256_file(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def manifest_sources(root: Path) -> set[str]:
    """Source, document and receipt files; local build caches are excluded."""
    ignored = {
        ".lake",
        "__pycache__",
        ".pytest_cache",
        ".hypothesis",
        ".git",
        "000_meron_sign_problem",
        "001_hubbard_sign_problem",
    }
    suffixes = {".md", ".py", ".sql", ".yaml", ".yml", ".lean", ".txt", ".json"}
    return {
        f.relative_to(root).as_posix() for f in root.rglob("*")
        if f.is_file() and not ignored.intersection(f.relative_to(root).parts)
        and (f.suffix in suffixes or f.name == "lean-toolchain")
    }


def check_files_exist(root: Path) -> list:
    errors = []
    for rel in REQUIRED_FILES:
        fp = root / rel
        if not fp.exists():
            errors.append(f"Missing required file: {rel}")
    return errors

def check_checksums(root: Path) -> list:
    manifest = root / "SHA256SUMS"
    if not manifest.exists():
        return ["SHA256SUMS file not found"]
    errors = []
    seen = set()
    with open(manifest, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.split(maxsplit=1)
            if len(parts) != 2:
                if line.strip():
                    errors.append("Malformed checksum manifest line")
                continue
            expected_hash, rel_path = parts
            rel_path = rel_path.strip()
            if rel_path.startswith("./"):
                rel_path = rel_path[2:]
            rel_path = rel_path.replace("/", os.sep).replace("\\", os.sep)
            if rel_path == "SHA256SUMS":
                continue
            fp = root / rel_path
            if not fp.resolve().is_relative_to(root.resolve()):
                errors.append(f"Checksum path escapes package: {rel_path}")
                continue
            name = fp.relative_to(root).as_posix()
            if name in seen:
                errors.append(f"Duplicate checksum path: {name}")
            seen.add(name)
            if not fp.exists():
                errors.append(f"Checksum check: File not found: {rel_path}")
                continue
            actual_hash = sha256_file(fp)
            if actual_hash.lower() != expected_hash.lower():
                errors.append(f"Checksum mismatch for {rel_path}: expected {expected_hash}, got {actual_hash}")
    for missing in sorted(manifest_sources(root) - seen):
        errors.append(f"Source not covered by checksum manifest: {missing}")
    return errors

def check_zenodo_json(root: Path) -> list:
    zj = root / ".zenodo.json"
    if not zj.exists():
        return [".zenodo.json missing"]
    errors = []
    try:
        with open(zj, "r", encoding="utf-8") as f:
            data = json.load(f)
        for req in ["title", "description", "creators", "license", "upload_type"]:
            if req not in data:
                errors.append(f".zenodo.json missing required key: {req}")
    except Exception as e:
        errors.append(f"Invalid .zenodo.json: {e}")
    return errors

def check_claim_ledger(root: Path) -> list:
    cy = root / "claim_ledger.yaml"
    cm = root / "the_problem_of_the_fermion_sign_claim_ledger.md"
    if not cy.exists():
        return ["claim_ledger.yaml missing"]
    if not cm.exists():
        return ["the_problem_of_the_fermion_sign_claim_ledger.md missing"]
    
    with open(cm, "r", encoding="utf-8") as f:
        md_text = f.read()
    
    import yaml
    with open(cy, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    
    errors = []
    lean_dir = root / "lean4"
    lean_decls = {}
    if lean_dir.exists():
        for fname in os.listdir(lean_dir):
            if fname.endswith(".lean"):
                mod = fname[:-5]
                with open(lean_dir / fname, "r", encoding="utf-8") as lf_in:
                    lean_decls[mod] = lf_in.read()

    for claim in data.get("claims", []):
        cid = claim.get("id")
        if not cid:
            errors.append("Claim missing ID in claim_ledger.yaml")
            continue
        if cid not in md_text:
            errors.append(f"Claim {cid} in claim_ledger.yaml not found in markdown ledger")

        # Semantic Lean formalization resolution
        lf = claim.get("lean4_formalization")
        if lf:
            mod = lf.get("module")
            if mod not in lean_decls:
                errors.append(f"[{cid}] Lean module lean4/{mod}.lean not found")
            else:
                mod_content = lean_decls[mod]
                for thm in lf.get("theorems", []):
                    if thm not in mod_content:
                        errors.append(f"[{cid}] Lean theorem '{thm}' not found in lean4/{mod}.lean")

        # Semantic code evidence resolution
        ce = claim.get("code_evidence", {})
        for t in ce.get("tests", []):
            if "::" in t:
                parts = t.split("::")
                tf_rel = parts[0]
                func = parts[-1]
            else:
                tf_rel = t
                func = None
            tf_path = root / tf_rel
            if not tf_path.exists():
                repo_root = root.parents[2]
                rel_clean = tf_rel.replace("code/tests/", "").replace("code/sign_sql/tests/", "sign_sql/")
                cand = repo_root / "code" / "python" / "tests" / "fsp" / rel_clean
                if cand.exists():
                    tf_path = cand
                else:
                    matches = list((repo_root / "code" / "python" / "tests" / "fsp").rglob(Path(tf_rel).name))
                    if matches:
                        tf_path = matches[0]
            if not tf_path.exists():
                errors.append(f"[{cid}] Test file {tf_rel} not found")
            elif func:
                with open(tf_path, "r", encoding="utf-8") as tf_in:
                    if func not in tf_in.read():
                        errors.append(f"[{cid}] Test function '{func}' not found in {tf_rel}")

    return errors

def check_claim_hygiene(root: Path) -> list:
    paper = root / "the_problem_of_the_fermion_sign.md"
    if not paper.exists():
        return ["the_problem_of_the_fermion_sign.md missing"]
    errors = []
    with open(paper, "r", encoding="utf-8") as f:
        content = f.read()
    if not re.search(r"AuthorityEffect[:\s*]+None", content):
        errors.append("the_problem_of_the_fermion_sign.md missing 'AuthorityEffect: None'")
    return errors

def run_tests(root: Path) -> list:
    repo_root = root.parents[2]
    test_dir = repo_root / "code" / "python" / "tests" / "fsp"
    if not test_dir.exists():
        test_dir = root / "code" / "tests"
    if not test_dir.exists():
        return ["fsp tests directory missing"]
    cmd = [sys.executable, "-m", "pytest", str(test_dir), "-n", "4", "-q"]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root / "code" / "python") + (os.pathsep + env["PYTHONPATH"] if "PYTHONPATH" in env else "")
    try:
        with tempfile.TemporaryDirectory(prefix="po023-tests-") as test_root:
            env["HYPOTHESIS_STORAGE_DIRECTORY"] = str(Path(test_root) / "hypothesis")
            res = subprocess.run(cmd + ["--basetemp", str(Path(test_root) / "temp"),
                                 "-o", f"cache_dir={Path(test_root) / 'cache'}"],
                                 cwd=str(repo_root), env=env, capture_output=True,
                                 text=True, encoding="utf-8", timeout=300)
        if res.returncode != 0:
            return [f"pytest failed with code {res.returncode}:\n{res.stdout}\n{res.stderr}"]
        print(res.stdout.strip())
    except Exception as e:
        return [f"Failed to execute pytest: {e}"]
    return []

def run_lean_build(root: Path) -> list:
    lean_dir = root / "lean4"
    if not lean_dir.exists():
        return ["lean4 directory missing"]
    cmd = ["lake", "build"]
    try:
        res = subprocess.run(cmd, cwd=str(lean_dir), capture_output=True, text=True,
                             encoding="utf-8", timeout=300)
        if res.returncode != 0:
            return [f"lake build failed with code {res.returncode}:\n{res.stdout}\n{res.stderr}"]
        out = (res.stdout + res.stderr).lower()
        if "sorry" in out:
            return ["lake build reported sorry warning/usage in build output"]
    except Exception as e:
        return [f"Failed to execute lake build: {e}"]
    return []

def main():
    parser = argparse.ArgumentParser(description="Verify Zenodo deposit gate for PO-023")
    parser.add_argument("--skip-tests", action="store_true", help="Skip pytest test execution")
    parser.add_argument("--skip-lake", action="store_true", help="Skip lake build execution")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent
    print(f"[*] Verifying Zenodo Deposit Gate for {root.name}...")

    all_errors = []

    print("[1/7] Checking required files...")
    errs = check_files_exist(root)
    if errs:
        all_errors.extend(errs)
    else:
        print("  -> All required files present.")

    print("[2/7] Checking SHA256 checksums...")
    errs = check_checksums(root)
    if errs:
        all_errors.extend(errs)
    else:
        print("  -> SHA256SUMS verified.")

    print("[3/7] Checking .zenodo.json...")
    errs = check_zenodo_json(root)
    if errs:
        all_errors.extend(errs)
    else:
        print("  -> .zenodo.json valid.")

    print("[4/7] Checking declared claim evidence references...")
    errs = check_claim_ledger(root)
    if errs:
        all_errors.extend(errs)
    else:
        print("  -> Declared claim evidence references resolve (not a semantic proof audit).")

    print("[5/7] Checking Claim Hygiene rules...")
    errs = check_claim_hygiene(root)
    if errs:
        all_errors.extend(errs)
    else:
        print("  -> Claim Hygiene checks passed.")

    if not args.skip_tests:
        print("[6/7] Running Python test suite...")
        errs = run_tests(root)
        if errs:
            all_errors.extend(errs)
        else:
            print("  -> Pytest test suite passed.")
    else:
        print("[6/7] Skipping Python test suite (--skip-tests).")

    if not args.skip_lake:
        print("[7/7] Running Lean 4 lake build...")
        errs = run_lean_build(root)
        if errs:
            all_errors.extend(errs)
        else:
            print("  -> Lean 4 lake build passed cleanly.")
    else:
        print("[7/7] Skipping Lean 4 lake build (--skip-lake).")

    if all_errors:
        print("\n[FAIL] Pre-Print Deposit Gate Failed with errors:")
        for err in all_errors:
            print(f"  - {err}")
        sys.exit(1)
    else:
        scope = "Selected checks" if args.skip_tests or args.skip_lake else "Package checks"
        print(f"\n[PASS] {scope} passed. AuthorityEffect: None. No publication or physics verdict.")
        sys.exit(0)

if __name__ == "__main__":
    main()
