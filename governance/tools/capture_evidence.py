"""Capture the verification receipts cited by the governance crate's own score records.

Runs, on a copy of code/rust/src/governance outside the workspace (the workspace
needs the external omega crates to resolve):
  1. cargo test --locked                      -> cargo-test.log
  2. cargo clippy --locked --lib --bins with cognitive_complexity (<= 15) and
     excessive_nesting (<= 3) as errors        -> clippy.log
  3. lizard (cyclomatic complexity per function) -> lizard.csv
and writes receipt.json with each command, tool version, working directory,
exit status and the SHA-256 of every source and output file.

Usage: python -I -X utf8 governance/tools/capture_evidence.py OUT_DIR [--copy DIR] [--target DIR]
No network (cargo --offline) and no model calls.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Sequence, Mapping

ROOT = Path(__file__).resolve().parents[2]
CRATE = ROOT / "code" / "rust" / "src" / "governance"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_hashes(crate: Path) -> dict[str, str]:
    return {p.relative_to(crate).as_posix(): sha(p) for p in sorted(crate.rglob("*"))
            if p.is_file() and "target" not in p.parts and not p.name.endswith(".contract.score.yaml")}


def prepare_copy(crate: Path, destination: Path | None) -> Path:
    """Create a new retained snapshot. Existing directories are never removed."""
    source = crate.resolve()
    if destination is None:
        destination = Path(tempfile.mkdtemp(prefix="tfqm-governance-")) / "crate"
    destination = destination.resolve()
    if destination == source or source in destination.parents:
        raise ValueError("the evidence copy must be outside the source crate")
    if destination.exists():
        raise FileExistsError("evidence copy already exists: " + str(destination))
    before = source_hashes(source)
    shutil.copytree(source, destination, ignore=shutil.ignore_patterns("target"))
    if source_hashes(destination) != before or source_hashes(source) != before:
        raise ValueError("source changed while capturing the evidence snapshot")
    return destination


def version(command: Sequence[str]) -> str:
    try:
        return subprocess.run(command, capture_output=True, text=True).stdout.strip()
    except OSError as error:
        return "unavailable: " + str(error)


def run(command: Sequence[str], cwd: Path, env: Mapping[str, str], log: Path) -> dict[str, Any]:
    proc = subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True)
    log.write_text("$ " + " ".join(command) + "\n" + proc.stdout + proc.stderr + "\nexit status: %d\n" % proc.returncode,
                   encoding="utf-8", newline="\n")
    return {"command": command, "cwd": str(cwd), "exit_status": proc.returncode, "log": log.name, "log_sha256": sha(log)}


def first_test_line(path: Path) -> int:
    """First line of the `#[cfg(test)]` module, so test functions can be told apart."""
    for number, line in enumerate(path.read_text(encoding="utf-8").split("\n"), start=1):
        if line.strip() == "#[cfg(test)]":
            return number
    return 10 ** 9


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("out", type=Path)
    parser.add_argument("--copy", type=Path, help="new retained snapshot directory; an existing path is refused")
    parser.add_argument("--target", type=Path, help="Cargo build cache; defaults to the new snapshot parent")
    args = parser.parse_args()
    out = args.out if args.out.is_absolute() else ROOT / args.out
    try:
        args.copy = prepare_copy(CRATE, args.copy)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    captured = source_hashes(args.copy)
    out.mkdir(parents=True, exist_ok=True)
    args.target = args.target or args.copy.parent / "target"
    env = dict(os.environ, CARGO_TARGET_DIR=str(args.target), CARGO_PROFILE_DEV_DEBUG="0", CARGO_TERM_COLOR="never")
    env.pop("TFQM_GOVERNANCE", None)
    manifest = str(args.copy / "Cargo.toml")
    steps = {
        "test": run(["cargo", "test", "--offline", "--locked", "--manifest-path", manifest], args.copy, env, out / "cargo-test.log"),
        "clippy": run(["cargo", "clippy", "--offline", "--locked", "--manifest-path", manifest, "--lib", "--bins", "--",
                       "-D", "warnings", "-D", "clippy::cognitive_complexity", "-D", "clippy::excessive_nesting"],
                      args.copy, env, out / "clippy.log"),
    }
    lizard = subprocess.run([sys.executable, "-I", "-X", "utf8", "-m", "lizard", "-l", "rust", "--csv", str(args.copy / "src")],
                            capture_output=True, text=True)
    (out / "lizard.csv").write_text(lizard.stdout, encoding="utf-8", newline="\n")
    steps["lizard"] = {"command": ["python", "-m", "lizard", "-l", "rust", "--csv", "src"], "cwd": str(args.copy),
                       "exit_status": lizard.returncode, "log": "lizard.csv", "log_sha256": sha(out / "lizard.csv")}
    metrics: dict[str, dict[str, dict[str, Any]]] = {}
    for row in csv.reader(io.StringIO(lizard.stdout)):
        nloc, ccn, file_name, function, start = int(row[0]), int(row[1]), row[6], row[7], int(row[9])
        rel = Path(file_name).resolve().relative_to(args.copy.resolve()).as_posix()
        kind = "test" if start >= first_test_line(args.copy / rel) else "production"
        per = metrics.setdefault(rel, {"production": {"functions": 0, "max_ccn": 0, "max_ccn_function": None},
                                       "test": {"functions": 0, "max_ccn": 0, "max_ccn_function": None}})[kind]
        per["functions"] += 1
        if ccn > per["max_ccn"]:
            per["max_ccn"], per["max_ccn_function"] = ccn, function
    receipt = {
        "schema": "tfqm.governance-evidence.v1",
        "AuthorityEffect": "None",
        "tool": "governance/tools/capture_evidence.py",
        "versions": {"cargo": version(["cargo", "--version"]), "rustc": version(["rustc", "--version"]),
                     "clippy": version(["cargo", "clippy", "--version"]), "python": sys.version.split()[0],
                     "lizard": version([sys.executable, "-I", "-m", "lizard", "--version"])},
        "clippy_thresholds": {"cognitive_complexity": 15, "excessive_nesting": 3, "config": "code/rust/src/governance/clippy.toml"},
        "steps": steps,
        "complexity": metrics,
        "sources": captured,
        "snapshot": str(args.copy),
        "snapshot_unchanged_after_checks": source_hashes(args.copy) == captured,
    }
    (out / "receipt.json").write_text(json.dumps(receipt, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({k: v["exit_status"] for k, v in steps.items()}))
    return 0 if receipt["snapshot_unchanged_after_checks"] and all(v["exit_status"] == 0 for v in steps.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
