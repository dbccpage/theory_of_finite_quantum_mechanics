"""Replay against an explicitly prepared, pinned Mathlib cache, without downloads.

Receipt verification checks recorded evidence and is not fresh compilation.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
TOOLCHAIN = "leanprover/lean4:v4.35.0"
ALLOWED = frozenset({"propext", "Quot.sound", "Classical.choice"})
SOURCES = ("lean4/ProjectionBounds.lean", "lean4/ProjectionCensus.lean",
           "lean4/projection_dependencies.json", "tools/replay_projection_bounds.py")
SCOPE = ("Real scalar and normed-carrier implications. Continuous evolution, "
         "tensor step bounds and validated numerical enclosures remain premises.")


def digest(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def expected_names(root: Path) -> list[str]:
    census = (root / SOURCES[1]).read_text(encoding="utf-8")
    names = re.findall(r"^#print axioms (ProjectionBounds\.\w+)\s*$", census, re.M)
    source = (root / SOURCES[0]).read_text(encoding="utf-8")
    declared = ["ProjectionBounds." + n for n in re.findall(r"^theorem (\w+)", source, re.M)]
    if not names or len(names) != len(set(names)) or set(names) != set(declared):
        raise ValueError("census must cover every named theorem exactly once")
    return names


def parse_axioms(output: str, expected: list[str]) -> dict[str, list[str]]:
    pattern = r"^'([^']+)' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)\s*$"
    records: dict[str, list[str]] = {}
    for name, axiom_text in re.findall(pattern, output, re.M):
        axioms = sorted(a.strip() for a in axiom_text.split(",") if a.strip())
        if name in records or not set(axioms) <= ALLOWED:
            raise ValueError("duplicate declaration or unapproved axiom: " + name)
        records[name] = axioms
    if set(records) != set(expected) or len(records) != len(expected):
        raise ValueError("incomplete or unexpected census output")
    return records


def source_hashes(root: Path) -> dict[str, str]:
    return {name: digest(root / name) for name in SOURCES}


def verify_receipt(root: Path = ROOT) -> dict:
    receipt = json.loads((root / "lean4/projection_axiom_census.json").read_text(encoding="utf-8"))
    expected = expected_names(root)
    report = (root / "lean4/projection_axiom_report.txt").read_text(encoding="utf-8")
    declarations = parse_axioms(report, expected)
    pins = json.loads((root / SOURCES[2]).read_text(encoding="utf-8"))
    if (receipt.get("schema_version") != 2 or receipt.get("toolchain") != TOOLCHAIN
            or receipt.get("sources") != source_hashes(root)
            or receipt.get("dependencies") != pins or receipt.get("declarations") != declarations
            or receipt.get("count") != len(expected) or receipt.get("scope") != SCOPE
            or receipt.get("report_sha256") != digest(root / "lean4/projection_axiom_report.txt")
            or receipt.get("fresh_compilation") is not True):
        raise ValueError("stored census does not bind the current sources, report and pins")
    return receipt


def run(command: list[str], *, cwd: Path, env: dict[str, str] | None = None) -> str:
    result = subprocess.run(command, cwd=cwd, env=env, capture_output=True,
                            text=True, encoding="utf-8", timeout=180, check=False)
    if result.returncode:
        raise ValueError(f"command failed ({result.returncode}): {command[0]}\n{result.stdout}{result.stderr}")
    return result.stdout + result.stderr


def dependency_paths(mathlib: Path, pins: dict) -> list[Path]:
    """Accept Mathlib's own or a containing project's dependency layout."""
    paths = []
    for name, pin in pins["packages"].items():
        candidates = [mathlib] if name == "mathlib" else [
            mathlib.parent / name, mathlib / ".lake/packages" / name]
        found = None
        for path in candidates:
            cache = path / ".lake/build/lib/lean"
            if not cache.is_dir():
                continue
            revision = run(["git", "rev-parse", "HEAD"], cwd=path).strip()
            dirty = run(["git", "status", "--porcelain", "--untracked-files=no"], cwd=path).strip()
            if revision == pin["rev"] and not dirty:
                found = cache.resolve()
                break
        if found is None:
            raise ValueError(f"prepare clean dependency {name} at {pin['rev']} with its compiled cache")
        paths.append(found)
    return paths


def replay(mathlib: Path, *, record: bool = False, root: Path = ROOT) -> dict:
    before = source_hashes(root)
    expected = expected_names(root)
    pins = json.loads((root / SOURCES[2]).read_text(encoding="utf-8"))
    if pins["toolchain"] != TOOLCHAIN:
        raise ValueError("dependency compiler pin mismatch")
    paths = dependency_paths(mathlib.resolve(), pins)
    home = Path(os.environ.get("ELAN_HOME", str(Path.home() / ".elan")))
    lean = home / "toolchains/leanprover--lean4---v4.35.0/bin" / ("lean.exe" if os.name == "nt" else "lean")
    version = run([str(lean), "--version"], cwd=root)
    if not re.search(r"Lean \(version 4\.35\.0(?:,|\s)", version):
        raise ValueError("compiler version disagrees with pin")
    with tempfile.TemporaryDirectory(prefix="projection-bounds-") as temporary:
        work = Path(temporary)
        for name in SOURCES[:2]:
            (work / Path(name).name).write_bytes((root / name).read_bytes())
        env = dict(os.environ, LEAN_PATH=os.pathsep.join(str(p) for p in [work, *paths]))
        run([str(lean), "-o", "ProjectionBounds.olean", "ProjectionBounds.lean"], cwd=work, env=env)
        output = run([str(lean), "ProjectionCensus.lean"], cwd=work, env=env)
        declarations = parse_axioms(output, expected)
    if before != source_hashes(root) or paths != dependency_paths(mathlib.resolve(), pins):
        raise ValueError("source or dependency changed during replay")
    # Compiler banners include OS/architecture; axiom evidence is portable.
    report = output
    result = {"schema_version": 2, "toolchain": TOOLCHAIN, "sources": before,
              "dependencies": pins, "declarations": declarations, "count": len(declarations),
              "fresh_compilation": True, "scope": SCOPE,
              "report_sha256": hashlib.sha256(report.encode("utf-8")).hexdigest()}
    if record:
        result["compiler_version"] = version.strip()
        result["recorded_at_utc"] = datetime.now(timezone.utc).isoformat()
        (root / "lean4/projection_axiom_report.txt").write_text(report, encoding="utf-8", newline="\n")
        (root / "lean4/projection_axiom_census.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    else:
        previous = verify_receipt(root)
        if any(previous.get(key) != value for key, value in result.items()):
            raise ValueError("stored census differs from fresh replay")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--record", action="store_true")
    mode.add_argument("--verify-receipt", action="store_true")
    parser.add_argument("--mathlib", type=Path, default=os.environ.get("PROJECTION_MATHLIB"))
    args = parser.parse_args()
    try:
        if args.verify_receipt:
            result = verify_receipt()
            label = "recorded evidence only; no fresh compilation"
        else:
            if args.mathlib is None:
                raise ValueError("supply --mathlib PATH or PROJECTION_MATHLIB; see docs/projection_formalization.md")
            result = replay(Path(args.mathlib), record=args.record)
            label = "fresh compilation"
    except (OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired) as error:
        print("FAIL:", error)
        return 1
    print(f"PASS {result['count']} supplemental theorems ({label}); standard axioms only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

