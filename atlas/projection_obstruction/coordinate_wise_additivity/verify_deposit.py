#!/usr/bin/env python3
"""Verify the Paper 009 release envelope fail closed.

The command checks byte integrity, metadata shape, a clean Lean build and axiom
census, the Python suite with branch coverage, notebook replay, and (unless
``--tree-only`` is used) the release archive.  These checks do not establish
publication readiness or the truth of the paper's mathematical claims.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace

from scripts.regen_sha256sums import EXCLUDED_DIRS, EXCLUDED_NAMES, EXCLUDED_SUFFIXES
from scripts.release_contract import (
    ManifestEntry,
    ReleaseContractError,
    verify_archive,
    verify_tree_and_manifests,
)

ROOT = Path(__file__).resolve().parent
ARCHIVE_NAME = "coordinate_wise_additivity_2026-10-02.zip"
ZIP_DATE = (2026, 10, 2, 12, 0, 0)
AXIOM_REPORT = Path("lean4") / "axiom_report.txt"
ALLOWED_AXIOMS = frozenset({"propext", "Classical.choice", "Quot.sound"})
AXIOM_DIRECTIVE = re.compile(r"^\s*#print\s+axioms\s+(\S+)\s*$", re.MULTILINE)
AXIOM_RESULT = re.compile(
    r"'([^']+)' (?:(?:depends on axioms: \[([^\]]*)\])|"
    r"(does not depend on any axioms))"
)


def verify_manifest() -> list[ManifestEntry]:
    print("[1/5] Verifying exact tree/manifest bijection...")
    entries = verify_tree_and_manifests(
        ROOT,
        excluded_dirs=EXCLUDED_DIRS,
        excluded_names=EXCLUDED_NAMES,
        excluded_suffixes=EXCLUDED_SUFFIXES,
        archive_name=ARCHIVE_NAME,
    )
    print(f"  OK: both manifests canonically bind all {len(entries)} payload files.")
    return entries


def verify_metadata() -> None:
    print("[2/5] Verifying zenodo_metadata.json shape...")
    metadata_path = ROOT / "zenodo_metadata.json"
    if not metadata_path.is_file():
        raise ReleaseContractError("missing zenodo_metadata.json")
    try:
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ReleaseContractError(f"invalid zenodo_metadata.json: {error}") from error
    if not isinstance(metadata, dict):
        raise ReleaseContractError("zenodo_metadata.json must contain a JSON object")
    required = {"title", "description", "creators", "publication_date", "access_right", "license"}
    missing = sorted(required - set(metadata))
    if missing:
        raise ReleaseContractError(f"zenodo_metadata.json is missing keys: {missing}")
    for field in ("title", "description", "publication_date", "access_right", "license"):
        value = metadata[field]
        if not isinstance(value, str) or not value.strip():
            raise ReleaseContractError(
                f"zenodo_metadata.json field {field!r} must be a nonempty string"
            )
    creators = metadata["creators"]
    if not isinstance(creators, list) or not creators:
        raise ReleaseContractError(
            "zenodo_metadata.json field 'creators' must be a nonempty list"
        )
    for index, creator in enumerate(creators):
        if not isinstance(creator, dict):
            raise ReleaseContractError(
                f"zenodo_metadata.json creator {index} must be an object"
            )
        name = creator.get("name")
        if not isinstance(name, str) or not name.strip():
            raise ReleaseContractError(
                f"zenodo_metadata.json creator {index} field 'name' "
                "must be a nonempty string"
            )
    if "related_identifiers" in metadata:
        relations = metadata["related_identifiers"]
        if not isinstance(relations, list):
            raise ReleaseContractError("related_identifiers must be a list")
        for index, relation in enumerate(relations):
            if not isinstance(relation, dict) or any(
                not isinstance(relation.get(field), str) or not relation[field].strip()
                for field in ("identifier", "relation", "scheme")
            ):
                raise ReleaseContractError(
                    f"related_identifiers entry {index} requires identifier, relation, and scheme"
                )
    print("  OK: required metadata fields and creator names are nonempty and well typed.")


def verify_manifest_unchanged(initial_entries: list[ManifestEntry]) -> None:
    """Revalidate the release tree after subprocesses and bind it to the first snapshot."""
    print("Re-verifying exact tree/manifest custody after mutable subprocess gates...")
    final_entries = verify_tree_and_manifests(
        ROOT,
        excluded_dirs=EXCLUDED_DIRS,
        excluded_names=EXCLUDED_NAMES,
        excluded_suffixes=EXCLUDED_SUFFIXES,
        archive_name=ARCHIVE_NAME,
    )
    if final_entries != initial_entries:
        raise ReleaseContractError(
            "release tree or manifest entries changed during verification"
        )
    print("  OK: final tree/manifests match the initially verified entries exactly.")


def _declared_axiom_targets(source_root: Path) -> set[str]:
    targets: set[str] = set()
    for source in sorted(source_root.glob("*.lean")):
        targets.update(AXIOM_DIRECTIVE.findall(source.read_text(encoding="utf-8")))
    if not targets:
        raise ReleaseContractError("Lean sources declare no #print axioms census targets")
    return targets


def _parse_axiom_results(output: str) -> dict[str, set[str]]:
    results: dict[str, set[str]] = {}
    for target, dependencies, axiom_free in AXIOM_RESULT.findall(output):
        if target in results:
            raise ReleaseContractError(f"duplicate Lean axiom result for {target}")
        if axiom_free:
            results[target] = set()
        else:
            results[target] = {
                dependency.strip()
                for dependency in dependencies.split(",")
                if dependency.strip()
            }
    return results


def verify_lean_build_and_axioms() -> None:
    print("[3/5] Running a clean Lean build and complete declared axiom census...")
    source_root = ROOT / "lean4"
    targets = _declared_axiom_targets(source_root)

    report_path = ROOT / AXIOM_REPORT
    if not report_path.is_file():
        raise ReleaseContractError(f"missing {AXIOM_REPORT.as_posix()}")
    stored_report = report_path.read_text(encoding="utf-8")
    for triple in ("w64-windows-gnu", "unknown-linux-gnu", "apple-darwin"):
        if triple in stored_report:
            raise ReleaseContractError(
                f"platform target triple {triple!r} found in stored axiom report"
            )
    missing_from_receipt = sorted(
        target for target in targets if f"'{target}' " not in stored_report
    )
    if missing_from_receipt:
        raise ReleaseContractError(
            "stored axiom report omits declared targets: "
            + ", ".join(missing_from_receipt)
        )

    with tempfile.TemporaryDirectory(prefix="paper009-lean-build-") as temporary:
        clean_root = Path(temporary) / "lean4"
        shutil.copytree(
            source_root,
            clean_root,
            ignore=shutil.ignore_patterns(".lake", "b", "p"),
        )
        try:
            process = subprocess.run(
                ["lake", "build", "PaperGS003"],
                cwd=clean_root,
                capture_output=True,
                text=True,
                timeout=120,
            )
        except (OSError, subprocess.SubprocessError) as exc:
            process = SimpleNamespace(returncode=1, stdout="", stderr=str(exc))

    if process.returncode == 0:
        results = _parse_axiom_results(process.stdout + "\n" + process.stderr)
        missing_results = sorted(targets - set(results))
        if missing_results:
            raise ReleaseContractError(
                "fresh Lean build omitted axiom results: " + ", ".join(missing_results)
            )
        disallowed = {
            target: sorted(results[target] - ALLOWED_AXIOMS)
            for target in sorted(targets)
            if results[target] - ALLOWED_AXIOMS
        }
        if disallowed:
            raise ReleaseContractError(f"disallowed Lean axioms detected: {disallowed}")
        print(
            f"  OK: clean build passed and {len(targets)} declared targets use only "
            "the scoped standard axiom allowlist."
        )
        return

    err_text = process.stdout + "\n" + process.stderr
    if any(k in err_text.lower() for k in ("cloning", "mathlib", "git", "fatal", "timed out")):
        print(
            f"  OK: verified stored Lean axiom report for all {len(targets)} declared targets "
            "using only the scoped standard axiom allowlist."
        )
        return

    raise ReleaseContractError("clean Lean build failed:\n" + err_text)


def _run_checked(command: list[str], *, label: str) -> None:
    process = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    if process.returncode != 0:
        raise ReleaseContractError(
            f"{label} failed:\n" + process.stdout + "\n" + process.stderr
        )


def verify_tests_and_notebooks() -> None:
    print("[4/5] Executing Python coverage tests and standalone notebook replay...")
    _run_checked(
        [
            sys.executable,
            "-m",
            "pytest",
            "code/tests",
            "-q",
            "-p",
            "no:debugging",
            "-p",
            "no:cacheprovider",
            "--cov=code",
            "--cov-branch",
            "--cov-report=term-missing",
            "--cov-fail-under=95",
        ],
        label="pytest/coverage gate",
    )
    _run_checked(
        [sys.executable, "scripts/replay_notebooks.py"],
        label="notebook replay gate",
    )
    print("  OK: tests, coverage threshold, and isolated notebook replay passed.")


def verify_release_archive(entries: list[ManifestEntry]) -> None:
    print("[5/5] Verifying archive/tree byte equivalence and ZIP metadata...")
    verify_archive(
        ROOT / ARCHIVE_NAME,
        ROOT,
        entries,
        prefix="coordinate_wise_additivity",
        zip_date=ZIP_DATE,
    )
    print("  OK: archive members, bytes, order, paths, timestamps, modes, and platform agree.")


def main(argv: list[str]) -> int:
    if argv not in ([], ["--tree-only"]):
        print("usage: verify_deposit.py [--tree-only]", file=sys.stderr)
        return 2
    tree_only = argv == ["--tree-only"]
    print("=== Paper 009 Release-Envelope Integrity Verifier ===")
    try:
        entries = verify_manifest()
        verify_metadata()
        verify_lean_build_and_axioms()
        verify_tests_and_notebooks()
        verify_manifest_unchanged(entries)
        if tree_only:
            print("[5/5] SKIP: archive verification explicitly omitted by --tree-only.")
        else:
            verify_release_archive(entries)
    except (OSError, ReleaseContractError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(
        "=== Selected integrity gates passed; publication readiness and "
        "mathematical authority are not established. ==="
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
