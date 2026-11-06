#!/usr/bin/env python3
"""Generate and replay the named Lean declarations in F005 axiom reports.

The reports are the pinned expected result.  Each generated ``Census.lean``
imports the package's declared Lake roots and issues one ``#print axioms``
command for every reported declaration.  Replay compares declaration names
and normalized axiom sets; it does not infer broader source coverage.
"""

from __future__ import annotations

import argparse
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGES = (
    "a",
    "coda",
    "coda_gtla",
    "cs",
    "cs_q",
    "fda",
    "foc",
    "mur",
    "or",
    "q",
)
EXPECTED_COUNTS = {
    "a": 73,
    "coda": 20,
    "coda_gtla": 21,
    "cs": 35,
    "cs_q": 80,
    "fda": 16,
    "foc": 150,
    "mur": 43,
    "or": 25,
    "q": 59,
}
EXPECTED_TOTAL = 522
DEPENDENCY_LINE = re.compile(r"^'(.+)' depends on axioms: \[(.*)\]$")
NO_DEPENDENCY_LINE = re.compile(r"^'(.+)' does not depend on any axioms$")
HEADER_NUMBER = re.compile(
    r"^(Declarations listed|Declarations with no axioms|"
    r"Declarations with axiom dependencies): (\d+)$"
)
LAKE_ROOTS = re.compile(r"roots\s*:=\s*#\[(.*?)\]", re.DOTALL)


@dataclass(frozen=True)
class Declaration:
    name: str
    axioms: frozenset[str]


def _declarations(text: str, source: Path | str) -> list[Declaration]:
    declarations: list[Declaration] = []
    for line in text.splitlines():
        no_dependency = NO_DEPENDENCY_LINE.fullmatch(line)
        dependency = DEPENDENCY_LINE.fullmatch(line)
        if no_dependency is not None:
            declarations.append(Declaration(no_dependency.group(1), frozenset()))
        elif dependency is not None:
            axioms = frozenset(
                axiom.strip() for axiom in dependency.group(2).split(",") if axiom.strip()
            )
            if not axioms:
                raise ValueError(f"empty axiom list in {source}: {line}")
            declarations.append(Declaration(dependency.group(1), axioms))
    names = [declaration.name for declaration in declarations]
    if len(names) != len(set(names)):
        raise ValueError(f"duplicate declaration in {source}")
    return declarations


def parse_report(package: str) -> list[Declaration]:
    report = ROOT / package / "lean4" / "axiom_report.txt"
    text = report.read_text(encoding="utf-8")
    declarations = _declarations(text, report)
    header_matches = [
        match
        for line in text.splitlines()
        if (match := HEADER_NUMBER.fullmatch(line)) is not None
    ]
    headers = {match.group(1): int(match.group(2)) for match in header_matches}
    required = {
        "Declarations listed",
        "Declarations with no axioms",
        "Declarations with axiom dependencies",
    }
    if len(header_matches) != len(required) or headers.keys() != required:
        raise ValueError(f"missing or duplicate count headers in {report}")
    without_axioms = sum(not declaration.axioms for declaration in declarations)
    with_axioms = len(declarations) - without_axioms
    actual_counts = (len(declarations), without_axioms, with_axioms)
    reported_counts = (
        headers["Declarations listed"],
        headers["Declarations with no axioms"],
        headers["Declarations with axiom dependencies"],
    )
    if actual_counts != reported_counts:
        raise ValueError(
            f"report counts disagree in {report}: {reported_counts} != {actual_counts}"
        )
    expected_count = EXPECTED_COUNTS[package]
    if len(declarations) != expected_count:
        raise ValueError(
            f"unexpected declaration count in {report}: {len(declarations)} != {expected_count}"
        )
    distinct_line = next(
        (line for line in text.splitlines() if line.startswith("Distinct axioms:")), None
    )
    if distinct_line is None:
        raise ValueError(f"missing distinct-axioms header in {report}")
    reported_axioms = frozenset(
        axiom.strip()
        for axiom in distinct_line.removeprefix("Distinct axioms:").split(",")
        if axiom.strip()
    )
    actual_axioms = frozenset(
        axiom for declaration in declarations for axiom in declaration.axioms
    )
    if reported_axioms != actual_axioms:
        raise ValueError(
            f"distinct axioms disagree in {report}: {reported_axioms} != {actual_axioms}"
        )
    return declarations


def import_roots(package: str) -> list[str]:
    lean_root = ROOT / package / "lean4"
    lakefile = lean_root / "lakefile.lean"
    text = lakefile.read_text(encoding="utf-8")
    match = LAKE_ROOTS.search(text)
    if match is None:
        raise ValueError(f"missing roots array in {lakefile}")
    roots = re.findall(r"`([A-Za-z0-9_.]+)", match.group(1))
    if not roots:
        raise ValueError(f"empty roots array in {lakefile}")
    imports: list[str] = []
    for root in roots:
        source = lean_root.joinpath(*root.split(".")).with_suffix(".lean")
        if not source.is_file():
            raise ValueError(f"Lake root has no source file: {root} ({source})")
        imports.append(root)
    if not imports:
        raise ValueError(f"no non-audit imports found in {lakefile}")
    return imports


def render_census(package: str) -> str:
    declarations = parse_report(package)
    lines = [
        "/-",
        "Generated by ../../tools/replay_lean_axiom_census.py.",
        "This replays only the declarations named in axiom_report.txt.",
        "Standalone build: lake build",
        "Standalone replay: lake env lean Census.lean",
        "Compare the replay with axiom_report.txt.",
        f"Repository check: python ../../tools/replay_lean_axiom_census.py --check {package}",
        "-/",
    ]
    lines.extend(f"import {root}" for root in import_roots(package))
    lines.append("")
    lines.extend(f"#print axioms {declaration.name}" for declaration in declarations)
    return "\n".join(lines) + "\n"


def census_path(package: str) -> Path:
    return ROOT / package / "lean4" / "Census.lean"


def write_census(package: str) -> None:
    with census_path(package).open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(render_census(package))


def check_census(package: str) -> None:
    path = census_path(package)
    actual = path.read_text(encoding="utf-8")
    expected = render_census(package)
    if actual != expected:
        raise ValueError(f"stale generated census: {path}")


def replay_census(package: str, timeout_seconds: int) -> None:
    check_census(package)
    lean_root = ROOT / package / "lean4"
    build = subprocess.run(
        ["lake", "build"],
        cwd=lean_root,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout_seconds,
    )
    if build.returncode != 0:
        raise ValueError(
            f"Lake build failed for {package} with exit {build.returncode}:\n"
            f"{build.stdout}"
        )
    completed = subprocess.run(
        ["lake", "env", "lean", "Census.lean"],
        cwd=lean_root,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout_seconds,
    )
    if completed.returncode != 0:
        raise ValueError(
            f"Lean replay failed for {package} with exit {completed.returncode}:\n"
            f"{completed.stdout}"
        )
    expected = parse_report(package)
    actual = _declarations(completed.stdout, f"Lean replay for {package}")
    if actual != expected:
        expected_by_name = {declaration.name: declaration.axioms for declaration in expected}
        actual_by_name = {declaration.name: declaration.axioms for declaration in actual}
        missing = sorted(expected_by_name.keys() - actual_by_name.keys())
        unexpected = sorted(actual_by_name.keys() - expected_by_name.keys())
        changed = sorted(
            name
            for name in expected_by_name.keys() & actual_by_name.keys()
            if expected_by_name[name] != actual_by_name[name]
        )
        raise ValueError(
            f"Lean replay disagrees for {package}: missing={missing}, "
            f"unexpected={unexpected}, changed={changed}, "
            f"order_matches={actual == expected}"
        )


def selected_packages(names: list[str]) -> tuple[str, ...]:
    packages = tuple(names) if names else PACKAGES
    unknown = sorted(set(packages) - set(PACKAGES))
    if unknown:
        raise ValueError(f"unknown package(s): {', '.join(unknown)}")
    if len(packages) != len(set(packages)):
        raise ValueError("duplicate package argument")
    return packages


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true", help="regenerate Census.lean")
    mode.add_argument("--replay", action="store_true", help="run Lean and compare output")
    mode.add_argument("--check", action="store_true", help="check generated files (default)")
    parser.add_argument("--timeout-seconds", type=int, default=600)
    parser.add_argument("packages", nargs="*")
    args = parser.parse_args()
    try:
        packages = selected_packages(args.packages)
        if args.timeout_seconds <= 0:
            raise ValueError("--timeout-seconds must be positive")
        total = sum(len(parse_report(package)) for package in PACKAGES)
        if total != EXPECTED_TOTAL:
            raise ValueError(f"aggregate declaration count changed: {total} != {EXPECTED_TOTAL}")
        for package in packages:
            if args.write:
                write_census(package)
                action = "generated"
            elif args.replay:
                replay_census(package, args.timeout_seconds)
                action = "replayed"
            else:
                check_census(package)
                action = "checked"
            print(f"OK {package}: {action} {EXPECTED_COUNTS[package]} declarations")
        print(f"OK aggregate: {total} named declarations across {len(PACKAGES)} reports")
    except (OSError, UnicodeError, ValueError, subprocess.TimeoutExpired) as error:
        print(f"FAIL: {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
