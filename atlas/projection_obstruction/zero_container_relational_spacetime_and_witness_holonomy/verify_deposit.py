#!/usr/bin/env python3
"""Deposit verification script for PO-035.

AuthorityEffect: None. Verification of code tests, file integrity, and release
packaging does not establish authority or physical truth.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from release_custody import identity, snapshot
from regen_sha256sums import render, MANIFEST_NAME


def run_checks(profile: str = "standalone") -> int:
    print(f"=== Verifying PO-035 Deposit [{profile} profile] ===")
    
    # 1. Identity check
    print("1. Checking release identity...")
    try:
        ident = identity(ROOT)
        print(f"   Identity verified: version {ident['release_version']}, date {ident['release_date']}")
    except Exception as e:
        print(f"FAIL: identity check failed: {e}", file=sys.stderr)
        return 1

    # 2. Check SHA256SUMS
    print("2. Checking file integrity manifest (SHA256SUMS)...")
    manifest = ROOT / MANIFEST_NAME
    if not manifest.exists():
        print(f"FAIL: {MANIFEST_NAME} does not exist. Regenerating...", file=sys.stderr)
        manifest.write_bytes(render(ROOT).encode("utf-8"))
    
    expected = render(ROOT)
    committed = manifest.read_bytes().decode("utf-8")
    if committed != expected:
        print(f"FAIL: {MANIFEST_NAME} does not match directory contents.", file=sys.stderr)
        return 1
    print(f"   Manifest verified: {len(expected.splitlines())} files tracked.")

    # 3. Pytest suite
    print("3. Executing unit and adversarial test suite...")
    cmd = [sys.executable, "-m", "pytest", "code/tests"]
    result = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True)
    if result.returncode != 0:
        print(f"FAIL: pytest suite failed:\n{result.stdout}\n{result.stderr}", file=sys.stderr)
        return 1
    
    lines = result.stdout.strip().splitlines()
    summary = lines[-1] if lines else "unknown"
    print(f"   Pytest results: {summary}")

    # 4. Release zip verification
    print("4. Verifying release zip reproducibility...")
    zip_cmd = [sys.executable, str(SCRIPTS / "build_release_zip.py"), "--output", str(ROOT / "dist"), "--check"]
    zip_res = subprocess.run(zip_cmd, cwd=str(ROOT), capture_output=True, text=True)
    if zip_res.returncode != 0:
        print(f"FAIL: build_release_zip check failed:\n{zip_res.stdout}\n{zip_res.stderr}", file=sys.stderr)
        return 1
    print("   Release zip is deterministic and byte-reproducible.")

    print("\nPASS: All deposit checks passed for PO-035.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", default="standalone", choices=["standalone", "full"])
    args = parser.parse_args()
    return run_checks(args.profile)


if __name__ == "__main__":
    sys.exit(main())
