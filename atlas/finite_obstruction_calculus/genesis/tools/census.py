"""Discover all non-internal compiled theorem constants, then pin their axioms.

FullCensus checks module-specific policies inside Lean. The named replay
report and Census.lean are generated from that compiled population, not a
hand-selected theorem list. Sources are checked before and after execution.
"""
from __future__ import annotations
import argparse
import hashlib
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean4"
PATTERN = re.compile(r"^'(.+)' (?:does not depend on any axioms|depends on axioms: \[(.*)\])$")


def source_hashes():
    return {str(p.relative_to(LEAN)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in LEAN.rglob("*.lean") if ".lake" not in p.parts}


def census(write=False):
    before = source_hashes()
    built = subprocess.run(["lake", "build"], cwd=LEAN, capture_output=True, text=True, encoding="utf-8")
    if built.returncode:
        raise RuntimeError(built.stdout[-6000:] + built.stderr[-2000:])
    run = subprocess.run(["lake", "env", "lean", "FullCensus.lean"], cwd=LEAN,
                         capture_output=True, text=True, encoding="utf-8")
    if run.returncode:
        raise RuntimeError(run.stdout + run.stderr)
    if source_hashes() != before:
        raise RuntimeError("LEAN_SOURCE_CHANGED")
    reports = {}
    for line in run.stdout.splitlines():
        match = PATTERN.fullmatch(line)
        if match:
            if match[1] in reports:
                raise RuntimeError(f"duplicate census theorem: {match[1]}")
            reports[match[1]] = line
    if not reports or "GenesisPaper.history_report_criterion" not in reports:
        raise RuntimeError("missing compiled theorem population")
    lines = [reports[n] for n in sorted(reports)]
    count = len(lines)
    no_axioms = sum("does not depend" in line for line in lines)
    text = (f"Declarations listed: {count}\nDeclarations with no axioms: {no_axioms}\n"
            f"Declarations with axiom dependencies: {count - no_axioms}\n\n" + "\n".join(lines) + "\n")
    report = LEAN / "axiom_report.txt"
    if write:
        report.write_text(text, encoding="utf-8", newline="\n")
        subprocess.run([__import__("sys").executable, str(ROOT / "tools/replay_lean_axiom_census.py"),
                        "--write", str(ROOT)], check=True)
    elif not report.is_file() or report.read_text(encoding="utf-8") != text:
        raise RuntimeError("compiled theorem population or axioms differ from saved report")
    print(f"Compiled census: {count} non-internal theorem constants; axiom policy passed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    census(write=args.write)
