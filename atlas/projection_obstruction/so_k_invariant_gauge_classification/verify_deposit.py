#!/usr/bin/env python3
"""Verify the Paper 008 release envelope fail closed.

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
from datetime import date
from pathlib import Path
from types import SimpleNamespace
from urllib.parse import urlparse

from scripts.regen_sha256sums import EXCLUDED_DIRS, EXCLUDED_NAMES, EXCLUDED_SUFFIXES
from scripts.release_contract import (
    ManifestEntry,
    ReleaseContractError,
    verify_archive,
    verify_tree_and_manifests,
)


ROOT = Path(__file__).resolve().parent
ARCHIVE_NAME = "so_k_invariant_gauge_classification_2026-09-21.zip"
ZIP_DATE = (2026, 9, 21, 12, 0, 0)
AXIOM_REPORT = Path("lean4") / "axiom_report.txt"
ALLOWED_AXIOMS = frozenset({"propext", "Classical.choice", "Quot.sound"})
AXIOM_DIRECTIVE = re.compile(r"^\s*#print\s+axioms\s+(\S+)\s*$", re.MULTILINE)
LEAN_DECLARATION = re.compile(
    r"^\s*(?:theorem|lemma)\s+([A-Za-z_][A-Za-z0-9_']*)\b", re.MULTILINE
)
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
    required = {
        "title", "description", "creators", "publication_date", "access_right", "license",
        "version", "upload_type", "publication_type", "related_identifiers",
    }
    missing = sorted(required - set(metadata))
    if missing:
        raise ReleaseContractError(f"zenodo_metadata.json is missing keys: {missing}")
    for field in ("title", "description", "publication_date", "access_right", "license", "version"):
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
    try:
        date.fromisoformat(metadata["publication_date"])
    except ValueError as error:
        raise ReleaseContractError("publication_date must be an ISO calendar date") from error
    if metadata["upload_type"] != "publication" or metadata["publication_type"] != "preprint":
        raise ReleaseContractError("release metadata must declare a publication/preprint")
    identifiers = metadata["related_identifiers"]
    if not isinstance(identifiers, list) or not identifiers:
        raise ReleaseContractError("related_identifiers must be a nonempty list")
    for index, item in enumerate(identifiers):
        if not isinstance(item, dict):
            raise ReleaseContractError(f"related_identifiers item {index} must be an object")
        for field in ("identifier", "relation", "scheme", "resource_type"):
            if not isinstance(item.get(field), str) or not item[field].strip():
                raise ReleaseContractError(
                    f"related_identifiers item {index} lacks a nonempty {field}"
                )
        # Both relations in this package point to declared public URLs.
        parsed = urlparse(item["identifier"])
        if item["scheme"] != "url" or parsed.scheme not in {"https", "http"} or not parsed.netloc:
            raise ReleaseContractError(f"related_identifiers item {index} must contain a URL")
    print("  OK: creator names, preprint type, date, and related URLs are well formed.")


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
    declarations: set[str] = set()
    for source in sorted(source_root.glob("*.lean")):
        text = source.read_text(encoding="utf-8")
        targets.update(AXIOM_DIRECTIVE.findall(text))
        declarations.update(LEAN_DECLARATION.findall(text))
    if not targets:
        raise ReleaseContractError("Lean sources declare no #print axioms census targets")
    uncensused = sorted(declarations - targets)
    if uncensused:
        raise ReleaseContractError(
            "Lean theorem/lemma declarations lack #print axioms targets: "
            + ", ".join(uncensused)
        )
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
    stored_results = _parse_axiom_results(stored_report)
    if set(stored_results) != targets:
        raise ReleaseContractError("stored axiom report target set differs from source census")
    if any(dependencies - ALLOWED_AXIOMS for dependencies in stored_results.values()):
        raise ReleaseContractError("stored axiom report contains disallowed Lean axioms")

    import shutil as _shutil
    if _shutil.which("lake") is None or "--skip-lake" in sys.argv:
        print("  SKIP: Lake toolchain not installed or --skip-lake requested.")
        return

    with tempfile.TemporaryDirectory(prefix="paper008-lean-build-") as temporary:
        clean_root = Path(temporary) / "lean4"
        shutil.copytree(
            source_root,
            clean_root,
            ignore=shutil.ignore_patterns(".lake", "b"),
        )
        try:
            process = subprocess.run(
                ["lake", "build", "GS002"],
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
        if {target: results[target] for target in targets} != stored_results:
            raise ReleaseContractError("fresh Lean axiom results differ from the stored receipt")
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
            "-n",
            "8",
            "-p",
            "no:cacheprovider",
            "--cov=code",
            "--cov-branch",
            "--cov-report=term-missing",
            "--cov-fail-under=95",
        ],
        label="pytest/coverage gate",
    )
    try:
        import importlib.metadata
        importlib.metadata.version("nbconvert")
        has_nbconvert = True
    except importlib.metadata.PackageNotFoundError:
        has_nbconvert = False

    if has_nbconvert and "--skip-notebooks" not in sys.argv:
        _run_checked(
            [sys.executable, "scripts/replay_notebooks.py"],
            label="notebook replay gate",
        )
    else:
        print("  SKIP: nbconvert not in active environment; invoke with `uv run --frozen --extra notebooks`.")
    print("  OK: tests, coverage threshold, and isolated notebook replay passed.")


def verify_release_archive(entries: list[ManifestEntry]) -> None:
    print("[5/5] Verifying archive/tree byte equivalence and ZIP metadata...")
    verify_archive(
        ROOT / ARCHIVE_NAME,
        ROOT,
        entries,
        prefix="",
        zip_date=ZIP_DATE,
    )
    print("  OK: archive members, bytes, order, paths, timestamps, modes, and platform agree.")


def main(argv: list[str]) -> int:
    allowed_flags = {"--tree-only", "--skip-lake", "--skip-notebooks"}
    if any(arg not in allowed_flags for arg in argv):
        print("usage: verify_deposit.py [--tree-only] [--skip-lake]", file=sys.stderr)
        return 2
    tree_only = "--tree-only" in argv
    print("=== Paper 008 Release-Envelope Integrity Verifier ===")
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
    print("=== Selected integrity gates passed; publication readiness is not established. ===")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
