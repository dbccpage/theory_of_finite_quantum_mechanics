#!/usr/bin/env python3
"""Replay axioms of all declarations in all deposited package-local Lean modules.

Lean enumerates the imported environment and selects declarations by their
defining module, including generated and private declarations. Imported Lean
library declarations are outside this package census. Default replay leaves
the deposited payload unchanged; --write explicitly regenerates the reports.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import re
import subprocess
from pathlib import Path

WHITELIST = {"propext", "Quot.sound", "Classical.choice"}
DEPENDENCY = re.compile(r"^'(.+)' depends on axioms: \[(.*)\]$")
NO_DEPENDENCY = re.compile(r"^'(.+)' does not depend on any axioms$")


def replay(root: Path, write: bool = False) -> int:
    lean = root / "lean4"
    modules = sorted(
        p.relative_to(lean).with_suffix("").as_posix().replace("/", ".")
        for p in lean.rglob("*.lean")
        if not any(part.startswith(".") for part in p.relative_to(lean).parts)
        and p.name not in {"lakefile.lean", "Census.lean", "FullCensus.lean"}
    )
    if not modules or any(not re.fullmatch(r"[A-Za-z0-9_.]+", m) for m in modules):
        raise ValueError("Missing or unsupported package-local module names")
    def source_hashes() -> dict[str, str]:
        return {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in lean.glob("*.lean")
                if p.name not in {"Census.lean", "FullCensus.lean"}}
    before = source_hashes()
    built = subprocess.run(["lake", "build"], cwd=lean, text=True,
                           capture_output=True, timeout=300)
    if built.returncode:
        raise ValueError(built.stdout + built.stderr)
    source = "\n".join(f"import {m}" for m in modules) + "\nimport Lean\n"
    source += "open Lean Elab Command\nrun_cmd do\n  let env ← getEnv\n"
    source += "  let modules : Array Name := #[" + ", ".join(f"`{m}" for m in modules) + "]\n"
    source += '''  for (name, _) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      if modules.contains env.header.moduleNames[idx.toNat]! then
        let axioms ← collectAxioms name
        if axioms.isEmpty then
          logInfo m!"'{name}' does not depend on any axioms"
        else
          let names := String.intercalate ", " (axioms.toList.map toString)
          logInfo m!"'{name}' depends on axioms: [{names}]"
'''
    census_path = lean / "FullCensus.lean"
    if write:
        census_path.write_text(source, encoding="utf-8")
    elif not census_path.is_file() or census_path.read_text(encoding="utf-8") != source:
        raise ValueError("FullCensus.lean is missing or stale; regenerate explicitly with --write")
    result = subprocess.run(["lake", "env", "lean", "FullCensus.lean"], cwd=lean,
                            text=True, capture_output=True, timeout=300)
    if result.returncode:
        raise ValueError(result.stdout + result.stderr)
    if source_hashes() != before:
        raise ValueError("Lean sources changed during the compiled census")
    rows = {}
    for line in result.stdout.splitlines():
        match = DEPENDENCY.fullmatch(line)
        empty = NO_DEPENDENCY.fullmatch(line)
        if match:
            name, axioms = match.groups()
            values = {v.strip() for v in axioms.split(",")}
        elif empty:
            name, values = empty.group(1), set()
        else:
            continue
        if name in rows:
            raise ValueError(f"Duplicate declaration: {name}")
        if not values <= WHITELIST:
            raise ValueError(f"Unapproved axioms for {name}: {sorted(values - WHITELIST)}")
        rows[name] = values
    if not rows:
        raise ValueError("Empty Lean declaration census")
    output = ["Full package-local Lean axiom census",
              f"Verification date: {datetime.date.today().isoformat()}",
              "Scope: all environment declarations defined in the listed package-local modules, including private and generated declarations.",
              "Modules: " + ", ".join(modules),
              f"Declarations listed: {len(rows)}",
              "Approved axioms: propext, Quot.sound, Classical.choice",
              "Execution: lake env lean FullCensus.lean exited 0.", ""]
    for name, values in sorted(rows.items()):
        output.append(f"'{name}' depends on axioms: [{', '.join(sorted(values))}]" if values
                      else f"'{name}' does not depend on any axioms")
    report = "\n".join(output) + "\n"
    for name in ("full_axiom_report.txt", "axiom_report.txt"):
        path = lean / name
        if write:
            path.write_text(report, encoding="utf-8")
        else:
            saved = {}
            for line in path.read_text(encoding="utf-8").splitlines():
                dependency = DEPENDENCY.fullmatch(line)
                empty = NO_DEPENDENCY.fullmatch(line)
                if dependency:
                    key = dependency[1]
                    values = {v.strip() for v in dependency[2].split(",")}
                elif empty:
                    key, values = empty[1], set()
                else:
                    continue
                if key in saved:
                    raise ValueError(f"Duplicate saved declaration in {name}: {key}")
                saved[key] = values
            if saved != rows:
                raise ValueError(f"Compiled declaration population differs from {name}")
            header = path.read_text(encoding="utf-8").splitlines()
            if f"Declarations listed: {len(rows)}" not in header or "Modules: " + ", ".join(modules) not in header:
                raise ValueError(f"Saved scope/count header differs from compiled population in {name}")
    print(f"PASS: {len(rows)} package-local declarations; {len(modules)} modules; approved axioms only")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Explicitly regenerate census source and reports")
    parser.add_argument("package", nargs="?", type=Path, default=Path.cwd())
    args = parser.parse_args()
    try:
        return replay(args.package.resolve(), write=args.write)
    except (OSError, ValueError, subprocess.TimeoutExpired) as error:
        print(f"FAIL: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
