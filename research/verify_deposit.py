"""Origin: verify_deposit.py
Claim: a deposit manifest matches every non-excluded file digest and a pytest junit report is accepted only when every testcase ran without failure, error, or skip
AuthorityEffect: None
Scope Fence: this file does not claim archive completeness or continuum physics
Level: L5
MutationKillCount: 4
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import cast

_HERE = Path(__file__).resolve().parent
BigRational = Fraction
ROOT = _HERE
ReadManifest = Callable[[Path, Path], list[tuple[str, str]]]
SafePath = Callable[[Path, str], Path]
DigestOf = Callable[[Path], str]
WalkFiles = Callable[[Path, set[str], set[str], set[str]], list[Path]]


def _library_dir() -> Path:
    bundled = _HERE / "code" / "deposit_paths.py"
    if bundled.is_file():
        return bundled.parent
    return _HERE


def _bind_paths() -> tuple[set[str], set[str], set[str], ReadManifest, SafePath, DigestOf, WalkFiles]:
    library = _library_dir()
    sys.path.insert(0, str(library))
    try:
        import deposit_paths as paths
    finally:
        sys.path.remove(str(library))
    return (
        set(cast(Iterable[str], paths.DEFAULT_EXCLUDED_DIRS)),
        set(cast(Iterable[str], paths.DEFAULT_EXCLUDED_NAMES)),
        set(cast(Iterable[str], paths.DEFAULT_EXCLUDED_SUFFIXES)),
        cast(ReadManifest, paths.read_manifest),
        cast(SafePath, paths.safe_path),
        cast(DigestOf, paths.sha256_of),
        cast(WalkFiles, paths.walk_files),
    )


(
    EXCLUDED_DIRS,
    EXCLUDED_NAMES,
    EXCLUDED_SUFFIXES,
    _read_manifest,
    _safe_path,
    _sha256_of,
    _walk_files,
) = _bind_paths()

REQUIRED_PATTERNS = (
    "finite_quantum_mechanics.md",
    "finite_quantum_mechanics.pdf",
    "finite_quantum_mechanics_change_log.md",
    "README.md",
    "LICENSE",
    "LICENSE-CODE",
    "pyproject.toml",
    "zenodo_metadata.json",
    "docs/descriptions.md",
    "docs/references.md",
    "code/deposit_paths.py",
)

E2E_DIRS = ("tests/e2e", "code/python/tests/e2e")
CUSTODY_TESTS = (
    "tests/legacy/unit/test_source_inventory.py",
    "tests/legacy/unit/test_retained_sources.py",
    "tests/legacy/unit/test_publication_status.py",
    "tests/legacy/unit/test_claim_ledger.py",
    "tests/legacy/unit/test_gap_register.py",
    "tests/legacy/unit/test_cochain.py",
)
PACKAGE_PATH = ("omega_engine_atlas", "coda_atlas", "F004_papers", "006_finite_qm")
_ORIGINAL_MANUSCRIPTS = 67
_PYTEST_TIMEOUT = 180


class ExactIntegerError(ValueError):
    def __init__(self, invariant: str) -> None:
        self.invariant = invariant
        super().__init__(invariant)


@dataclass(frozen=True)
class Verification:
    claim: str
    holds: bool
    detail: str


def exact_int(value: object) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ExactIntegerError("Expected exact integer, received boolean or non-integer")
    return value


def big_rational(numer: object, denom: object) -> BigRational:
    den = exact_int(denom)
    if den == 0:
        raise ExactIntegerError("rational denominator is nonzero")
    return BigRational(exact_int(numer), den)


def verify_original_count(found: object) -> Verification:
    number = exact_int(found)
    ratio = big_rational(number, _ORIGINAL_MANUSCRIPTS)
    return Verification(
        "original manuscripts",
        ratio == BigRational(1, 1),
        f"{number}/{_ORIGINAL_MANUSCRIPTS}",
    )


def verify_case_count(cases: object, blocked: object) -> Verification:
    total = exact_int(cases)
    bad = exact_int(blocked)
    if total <= 0:
        return Verification("executed test cases", False, "no cases")
    ratio = big_rational(total - bad, total)
    return Verification("executed test cases", ratio == BigRational(1, 1), f"{total - bad}/{total}")


def repository_checkout() -> Path | None:
    if ROOT.parts[-len(PACKAGE_PATH) :] != PACKAGE_PATH:
        return None
    candidate = ROOT.parents[len(PACKAGE_PATH) - 1]
    marker = candidate / "omega_engine" / "crates_rs" / "Cargo.toml"
    if not marker.is_file():
        return None
    return candidate


def _excluded_names(manifest_path: Path) -> set[str]:
    names = set(EXCLUDED_NAMES)
    if manifest_path.name == "MANIFEST.sha256":
        names.add("MANIFEST.sha256")
    return names


def _one_hash(root: Path, relative: str, digest: str) -> list[str]:
    path = _safe_path(root, relative)
    if not path.is_file():
        return [f"Recorded file missing: {relative}"]
    if _sha256_of(path) != digest:
        return [f"Hash mismatch: {relative}"]
    return []


def _hash_errors(root: Path, entries: list[tuple[str, str]]) -> list[str]:
    errors: list[str] = []
    for relative, digest in entries:
        errors.extend(_one_hash(root, relative, digest))
    return errors


def _sweep_errors(expected: set[str], recorded: set[str]) -> list[str]:
    errors: list[str] = []
    for relative in sorted(expected - recorded):
        errors.append(f"Unrecorded deposit file: {relative}")
    for relative in sorted(recorded - expected):
        errors.append(f"Excluded file listed in manifest: {relative}")
    return errors


def _pattern_file_error(root: Path, pattern: str) -> str | None:
    if "/" in pattern:
        target = root / pattern
        if target.is_file() and target.stat().st_size > 0:
            return None
        return f"Required file missing or empty: {pattern}"
    matches = [item for item in root.glob(pattern) if item.stat().st_size > 0]
    if matches:
        return None
    return f"Required file pattern missing or empty: {pattern}"


def _required_errors(root: Path) -> list[str]:
    errors: list[str] = []
    for pattern in REQUIRED_PATTERNS:
        message = _pattern_file_error(root, pattern)
        if message is not None:
            errors.append(message)
    return errors


def _originals_error(root: Path) -> list[str]:
    originals = list((root / "sources" / "original_papers").glob("*/*.md"))
    if verify_original_count(len(originals)).holds:
        return []
    found = len(originals)
    return [
        "Expected 67 original source manuscripts in "
        f"sources/original_papers, found {found}"
    ]


def _manifest_errors(manifest_path: Path) -> list[str]:
    excluded = _excluded_names(manifest_path)
    expected_files = _walk_files(ROOT, EXCLUDED_DIRS, excluded, EXCLUDED_SUFFIXES)
    entries = _read_manifest(ROOT, manifest_path)
    recorded = {relative for relative, _digest in entries}
    expected = {path.relative_to(ROOT).as_posix() for path in expected_files}
    errors = _hash_errors(ROOT, entries)
    errors.extend(_sweep_errors(expected, recorded))
    errors.extend(_required_errors(ROOT))
    errors.extend(_originals_error(ROOT))
    return errors


def check_manifest(manifest_path: Path) -> list[str]:
    try:
        return _manifest_errors(manifest_path)
    except (OSError, ValueError) as error:
        return [str(error)]


def _e2e_targets() -> list[str]:
    for relative in E2E_DIRS:
        tests_dir = ROOT / relative
        if tests_dir.is_dir():
            return sorted(
                path.relative_to(ROOT).as_posix()
                for path in tests_dir.glob("test_*.py")
                if path.name not in EXCLUDED_NAMES
            )
    return []


def default_test_targets() -> tuple[list[str], list[str]]:
    targets = _e2e_targets()
    if repository_checkout() is None:
        return targets, list(CUSTODY_TESTS)
    return targets + list(CUSTODY_TESTS), []


def _pytest_command(target: str, junit: Path) -> list[str]:
    return [
        sys.executable,
        "-m",
        "pytest",
        target,
        "-q",
        "-o",
        "xfail_strict=true",
        f"--junitxml={junit}",
    ]


def _case_blocked(case: ET.Element) -> bool:
    for tag in ("failure", "error", "skipped"):
        if case.find(tag) is not None:
            return True
    return False


def _blocked_count(cases: list[ET.Element]) -> int:
    total = 0
    for case in cases:
        if _case_blocked(case):
            total = total + 1
    return total


def _report_error(junit: Path, target: str) -> str | None:
    report = ET.parse(junit).getroot()
    cases = list(report.iter("testcase"))
    if report.tag not in {"testsuite", "testsuites"} or not cases:
        return f"No test-case evidence in {target}"
    if verify_case_count(len(cases), _blocked_count(cases)).holds:
        return None
    return f"Selected tests failed or skipped in {target}"


def _run_pytest(target: str) -> list[str]:
    path = _safe_path(ROOT, target)
    if not target.endswith(".py") or not path.is_file():
        return [f"Invalid test target: {target}"]
    with tempfile.TemporaryDirectory(prefix="finite-qm-pytest-") as temporary:
        junit = Path(temporary) / "results.xml"
        result = subprocess.run(
            _pytest_command(target, junit),
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=exact_int(_PYTEST_TIMEOUT),
            check=False,
        )
        if result.returncode:
            return [f"Pytest failure in {target}:\n{result.stdout}\n{result.stderr}"]
        message = _report_error(junit, target)
        if message is None:
            return []
        return [message]


def _one_test(target: str) -> list[str]:
    try:
        return _run_pytest(target)
    except (OSError, ValueError, ET.ParseError, subprocess.TimeoutExpired) as error:
        return [str(error)]


def check_tests(targets: list[str]) -> list[str]:
    if not targets:
        return ["No test files found in tests/e2e/"]
    errors: list[str] = []
    for target in targets:
        errors.extend(_one_test(target))
    return errors


def _manifest_path() -> Path | None:
    primary = ROOT / "SHA256SUMS"
    if primary.is_file():
        return primary
    alternate = ROOT / "MANIFEST.sha256"
    if alternate.is_file():
        return alternate
    return None


def _print_manifest(errors: list[str]) -> None:
    if errors:
        print(f"FAIL: Manifest checks failed ({len(errors)} issues):")
        for err in errors:
            print(f"  - {err}")
        return
    print("OK: Manifest and two-way sweep checks passed.")


def _named_tests(args: argparse.Namespace) -> list[str]:
    named: object = vars(args)["test"]
    if not isinstance(named, list):
        raise ExactIntegerError("test arguments are a list")
    names: list[str] = []
    for item in named:
        if not isinstance(item, str):
            raise ExactIntegerError("test argument is text")
        names.append(item)
    return names


def _selected_targets(named: list[str]) -> tuple[list[str], list[str]]:
    if named:
        return named, []
    return default_test_targets()


def _print_tests(targets: list[str], errors: list[str], not_run: list[str]) -> None:
    for error in errors:
        print(f"FAIL: {error}")
    if not errors:
        print(f"OK: Companion tests passed ({len(targets)} files).")
    for target in not_run:
        print(f"NOT RUN: {target} needs the repository checkout (README, Reproduction scope).")


def _print_result(error_count: int, not_run: list[str]) -> int:
    count = exact_int(error_count)
    if count:
        print(f"\nVerification FAILED with {count} errors.")
        return 1
    if not_run:
        print("\nVerification PASSED for the standalone scope only: manifest and end-to-end tests.")
        return 0
    print("\nVerification PASSED.")
    return 0


def _collect_manifest() -> list[str]:
    manifest_target = _manifest_path()
    if manifest_target is None:
        return [f"Manifest not found: {ROOT / 'SHA256SUMS'}"]
    errors = check_manifest(manifest_target)
    _print_manifest(errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify paper deposit package.")
    parser.add_argument("--test", action="append", default=[], help="Named test file; repeat as needed.")
    args = parser.parse_args()
    manifest_errors = _collect_manifest()
    targets, not_run = _selected_targets(_named_tests(args))
    test_errors = check_tests(targets)
    _print_tests(targets, test_errors, not_run)
    return _print_result(len(manifest_errors) + len(test_errors), not_run)


if __name__ == "__main__":
    raise SystemExit(main())
