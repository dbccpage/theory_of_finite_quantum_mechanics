#!/usr/bin/env python3
"""Verify Paper B's pinned release surface, executable tests, and proof bundle.

AuthorityEffect: None. A successful run establishes reproducibility of the
finite package. It does not prove empirical hypotheses or authorize deployment.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parent
PAPER_STEM = "witnessed_difference_programme"
RELEASE_DATE = "2026-10-13"
ARCHIVE_NAME = f"{ROOT.name}_{RELEASE_DATE}.zip"
RELEASE_ZIP_DATE = (*(int(part) for part in RELEASE_DATE.split("-")), 12, 0, 0)
MANIFEST = ROOT / "SHA256SUMS"
AXIOM_REPORT = Path("lean4") / "axiom_report.txt"
HISTORICAL_AXIOM_REPORT = Path("lean4") / "historical_axiom_report_202.txt"
EXPECTED_AXIOM_REPORTS = 305
COVERAGE_THRESHOLD = 95.0

PRODUCTION_MODULES = (
    "claims.py",
    "cochains.py",
    "complex_growth.py",
    "context_witness.py",
    "contraction.py",
    "duration.py",
    "exact.py",
    "exact_linear.py",
    "figures.py",
    "ground.py",
    "histories.py",
    "interference.py",
    "measurement.py",
    "notebook_support.py",
    "observation.py",
    "observer.py",
    "obstruction.py",
    "outcomes.py",
    "pointed_relation.py",
    "presentation_descent.py",
    "presentation_recovery.py",
    "probability.py",
    "projective.py",
    "proved_rows.py",
    "quantum.py",
    "quotient_observer.py",
    "receipts.py",
    "relative_status.py",
    "simplicial.py",
    "state_spaces.py",
    "symmetry.py",
    "truncation.py",
    "vector_obstruction.py",
    "witness.py",
)
AXIOM_WHITELIST = frozenset({"propext", "Classical.choice", "Quot.sound"})

IGNORED_DIR_NAMES = {
    "__pycache__",
    ".pytest_cache",
    ".hypothesis",
    ".lake",
    ".venv",
    "venv",
    "b",
    "scratch",
    ".ipynb_checkpoints",
    ".mypy_cache",
    ".ruff_cache",
    ".git",
    "dist",
    "build",
    "htmlcov",
    "target",
}
ROOT_SCOPED_DIRS = {"b", "build", "dist", "node_modules", "target"}
IGNORED_DIR_PATHS = (
    ROOT_SCOPED_DIRS
    | {f"lean4/{name}" for name in ROOT_SCOPED_DIRS}
    | {f"code/rust/{name}" for name in ROOT_SCOPED_DIRS}
    | {"code/coda_application/build", "code/coda_application/dist"}
)


def ignored_directory(relative: str) -> bool:
    parts = PurePosixPath(relative).parts
    return (
        any(part in IGNORED_DIR_NAMES - ROOT_SCOPED_DIRS or part.endswith(".egg-info") for part in parts)
        or any("/".join(parts[:i]) in IGNORED_DIR_PATHS for i in range(1, len(parts) + 1))
    )


# The root SHA256SUMS is the control file. Archived packages under docs/ keep
# their own checksum files, and those are pinned like any other member.
ROOT_CONTROL_FILES = {"SHA256SUMS"}
IGNORED_FILE_NAMES = {
    ".coverage",
    "coverage.json",
    "coverage.xml",
    "mutation-results.xml",
    "DEPOSIT_CHECKLIST.md",
    "STAGE_1_REPORT.md",
    "STAGE_2_REPORT.md",
    "paper_composition_manifest.json",
    "paper_composition_manifest.yaml",
    "paper_composition_receipt.json",
    ".DS_Store",
    "Thumbs.db",
}
IGNORED_SUFFIXES = {
    ".zip",
    ".aux",
    ".toc",
    ".out",
    ".log",
    ".synctex.gz",
}

PUBLIC_NOTEBOOKS = {
    "000_primitive_difference.ipynb",
    "010_cochains_and_vector_obstruction.ipynb",
    "020_retention_and_reaccess.ipynb",
    "030_observer_representations.ipynb",
    "040_observation_to_measurement.ipynb",
    "050_duration_and_finite_probability.ipynb",
    "060_bounded_history_sums.ipynb",
    "070_declared_u1_holonomy.ipynb",
    "080_claim_status_and_receipts.ipynb",
    "090_mutation_recovery_and_scope.ipynb",
    "supplements/100_trotter_cochain_extinction.ipynb",
    "supplements/110_certified_preservers.ipynb",
}

REQUIRED_FILES = (
    "README.md",
    "docs/references.md",
    "source_provenance.json",
    "witnessed_difference_programme.md",
    "witnessed_difference_programme_change_log.md",
    "witnessed_difference_programme_claim_ledger.md",
    "pyproject.toml",
    "uv.lock",
    "LICENSE",
    "LICENSE-CODE",
    "zenodo_metadata.json",
    "lean4/axiom_report.txt",
    "lean4/historical_axiom_report_202.txt",
    "lean4/lakefile.lean",
    "lean4/lake-manifest.json",
    "lean4/lean-toolchain",
    "lean4/README.md",
    "lean4/VERIFICATION.md",
    "lean4/claim_map.md",
    "lean4/PROVENANCE.md",
    "lean4/WitnessedDifference.lean",
    "lean4/WitnessedDifference/AxiomReport.lean",
    "lean4/WitnessedDifference/Core.lean",
    "lean4/WitnessedDifference/Difference.lean",
    "lean4/WitnessedDifference/Succession.lean",
    "lean4/WitnessedDifference/SemiringTransport.lean",
    "lean4/WitnessedDifference/QuantumImports.lean",
    "lean4/WitnessedDifference/History.lean",
    "lean4/WitnessedDifference/Symmetry.lean",
    "lean4/WitnessedDifference/Probability.lean",
    "lean4/WitnessedDifference/Descent.lean",
    "lean4/WitnessedDifference/Observer.lean",
    "lean4/WitnessedDifference/Measurement.lean",
    "lean4/WitnessedDifference/Obstruction.lean",
    "lean4/WitnessedDifference/PacketAdapter.lean",
    "lean4/WitnessedDifference/ObserverResolution.lean",
    "lean4/WitnessedDifference/PointedRelation.lean",
    "lean4/WitnessedDifference/ComplexGrowth.lean",
    "lean4/WitnessedDifference/Interference.lean",
    "lean4/WitnessedDifference/ClassicalCorner.lean",
    "lean4/WitnessedDifference/EmpiricalModel.lean",
    "lean4/WitnessedDifference/ClassicalPackage.lean",
    "lean4/WitnessedDifference/ToleranceAdapter.lean",
    "lean4/WitnessedDifference/Composition.lean",
    "lean4/WitnessedDifference/AmplitudeBridge.lean",
    "lean4/WitnessedDifference/InstrumentAdapter.lean",
    "scripts/build_deposit_zip.py",
    "scripts/build_paper_artifacts.py",
    "scripts/obstruction-preamble.tex",
    "scripts/capture_axiom_report.py",
    "scripts/regen_sha256sums.py",
    "scripts/verify_release.py",
    "manifests/claim_code_map.json",
    "manifests/figure_manifest.json",
    "manifests/historical_claim_occurrences.json",
    "manifests/notebook_manifest.json",
    "manifests/release_manifest.json",
    "manifests/release_verification.json",
    "images/conceptual/witnessed_difference_cover.png",
    "jupyter_notebooks/README.md",
    "jupyter_notebooks/000_primitive_difference.ipynb",
    "jupyter_notebooks/010_cochains_and_vector_obstruction.ipynb",
    "jupyter_notebooks/020_retention_and_reaccess.ipynb",
    "jupyter_notebooks/030_observer_representations.ipynb",
    "jupyter_notebooks/040_observation_to_measurement.ipynb",
    "jupyter_notebooks/050_duration_and_finite_probability.ipynb",
    "jupyter_notebooks/060_bounded_history_sums.ipynb",
    "jupyter_notebooks/070_declared_u1_holonomy.ipynb",
    "jupyter_notebooks/080_claim_status_and_receipts.ipynb",
    "jupyter_notebooks/090_mutation_recovery_and_scope.ipynb",
    "jupyter_notebooks/supplements/100_trotter_cochain_extinction.ipynb",
    "jupyter_notebooks/supplements/110_certified_preservers.ipynb",
    "verify_deposit.py",
)


def regular_path(path: Path, *, directory: bool = False, allow_missing: bool = False) -> Path:
    path = path.absolute()
    for part in reversed((path, *path.parents)):
        try:
            info = part.lstat()
        except FileNotFoundError:
            if allow_missing:
                break
            raise ValueError(f"missing custody path: {part}")
        expected = stat.S_ISDIR if part != path or directory else stat.S_ISREG
        if not expected(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
            raise ValueError(f"non-regular custody path: {part}")
    return path


def sha256_of(path: Path) -> str:
    path = regular_path(path)
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _validated_manifest_path(relative: str, lineno: int, root_dir: Path) -> Path:
    pure = PurePosixPath(relative)
    unsafe = (
        not relative
        or not pure.parts
        or pure.is_absolute()
        or pure.as_posix() != relative
        or ".." in pure.parts
        or "\\" in relative
        or ":" in pure.parts[0]
    )
    candidate = root_dir.joinpath(*pure.parts)
    if unsafe:
        raise SystemExit(
            f"FAIL: SHA256SUMS line {lineno} has unsafe path {relative!r}"
        )
    try:
        return regular_path(candidate, allow_missing=True)
    except (OSError, ValueError) as error:
        raise SystemExit(f"FAIL: SHA256SUMS line {lineno}: {error}") from error


def parse_manifest(
    manifest_path: Path = MANIFEST, root_dir: Path = ROOT
) -> dict[str, str]:
    if not manifest_path.is_file():
        raise SystemExit("FAIL: SHA256SUMS is missing; run scripts/regen_sha256sums.py first")
    regular_path(manifest_path)
    entries: dict[str, str] = {}
    for lineno, raw in enumerate(
        manifest_path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        line = raw.strip()
        if not line:
            continue
        parts = line.split(None, 1)
        if len(parts) != 2 or re.fullmatch(r"[0-9a-fA-F]{64}", parts[0]) is None:
            raise SystemExit(
                f"FAIL: SHA256SUMS line {lineno} is malformed: {raw!r}"
            )
        digest, relative = parts[0].lower(), parts[1].strip().lstrip("*")
        _validated_manifest_path(relative, lineno, root_dir)
        if relative.casefold() in {path.casefold() for path in entries}:
            raise SystemExit(f"FAIL: SHA256SUMS lists {relative} more than once")
        entries[relative] = digest
    return entries


def check_hashes(
    entries: dict[str, str], root_dir: Path = ROOT
) -> list[str]:
    problems: list[str] = []
    for relative, digest in sorted(entries.items()):
        path = root_dir / relative
        if not path.is_file():
            problems.append(f"missing file listed in SHA256SUMS: {relative}")
        else:
            try:
                if sha256_of(path) != digest:
                    problems.append(f"hash mismatch for {relative}")
            except (ValueError, OSError) as error:
                problems.append(str(error))
    return problems


def sweep_unlisted(
    entries: dict[str, str], root_dir: Path = ROOT
) -> list[str]:
    problems: list[str] = []
    try:
        regular_path(root_dir, directory=True)
    except (OSError, ValueError) as error:
        return [str(error)]
    for directory, names, filenames in os.walk(root_dir, followlinks=False,
                                              onerror=lambda error: problems.append(str(error))):
        current = Path(directory)
        kept = []
        for name in names:
            path = current / name
            try:
                regular_path(path, directory=True)
            except (OSError, ValueError) as error:
                problems.append(str(error))
                continue
            if not ignored_directory(path.relative_to(root_dir).as_posix()):
                kept.append(name)
        names[:] = kept
        for name in sorted(filenames):
            path = current / name
            relative = path.relative_to(root_dir).as_posix()
            try:
                regular_path(path)
            except (OSError, ValueError) as error:
                problems.append(str(error))
                continue
            if (relative in ROOT_CONTROL_FILES or name in IGNORED_FILE_NAMES
                    or name.startswith(".coverage")
                    or (relative not in {"witnessed_difference_programme.aux", "witnessed_difference_programme.toc", "witnessed_difference_programme.log"}
                        and any(name.endswith(suffix) for suffix in IGNORED_SUFFIXES))):
                continue
            if relative not in entries:
                problems.append(f"file present but not listed in SHA256SUMS: {relative}")
    return problems


def check_required(
    entries: dict[str, str], root_dir: Path = ROOT
) -> list[str]:
    problems: list[str] = []
    for relative in REQUIRED_FILES:
        if relative not in entries:
            problems.append(f"required file not pinned in SHA256SUMS: {relative}")
        elif not (root_dir / relative).is_file():
            problems.append(f"required file missing on disk: {relative}")
    return problems


def check_release_contracts(
    entries: dict[str, str], root_dir: Path = ROOT
) -> list[str]:
    problems: list[str] = []
    notebooks = {
        relative.removeprefix("jupyter_notebooks/")
        for relative in entries
        if relative.startswith("jupyter_notebooks/")
        and relative.endswith(".ipynb")
    }
    if notebooks != PUBLIC_NOTEBOOKS:
        problems.append(
            f"public notebook set mismatch: expected {sorted(PUBLIC_NOTEBOOKS)}, "
            f"got {sorted(notebooks)}"
        )

    archive_builder = root_dir / "scripts" / "build_deposit_zip.py"
    if archive_builder.is_file():
        source = archive_builder.read_text(encoding="utf-8")
        if f'RELEASE_DATE = "{RELEASE_DATE}"' not in source:
            problems.append("archive builder does not bind the release date")
        if 'ARCHIVE_NAME = f"{ROOT.name}_{RELEASE_DATE}.zip"' not in source:
            problems.append("archive builder does not use the required dated name")

    metadata_path = root_dir / "zenodo_metadata.json"
    if metadata_path.is_file():
        try:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            if metadata.get("publication_date") != RELEASE_DATE:
                problems.append("zenodo_metadata.json date does not match RELEASE_DATE")
            if metadata.get("license") != "cc-by-4.0":
                problems.append("zenodo_metadata.json license is not cc-by-4.0")
        except json.JSONDecodeError as err:
            problems.append(f"zenodo_metadata.json is not valid JSON: {err}")
    else:
        problems.append("zenodo_metadata.json is missing")

    return problems


def pytest_summary(output: str) -> str:
    lines = [line for line in output.splitlines() if line.strip()]
    for line in reversed(lines):
        if re.search(r"\b\d+ passed\b", line):
            return line
    return lines[-1] if lines else "(no pytest output)"


def coverage_counts(
    report: dict[str, object],
) -> tuple[dict[str, tuple[int, int, int, int]], list[str]]:
    """Check required modules and aggregate every reported package source file."""
    files = report.get("files")
    if not isinstance(files, dict):
        return {}, ["coverage JSON has no files mapping"]
    counts: dict[str, tuple[int, int, int, int]] = {}
    problems: list[str] = []
    for module_name in PRODUCTION_MODULES:
        matches = [
            value
            for key, value in files.items()
            if PurePosixPath(str(key).replace("\\", "/")).name == module_name
        ]
        if len(matches) != 1 or not isinstance(matches[0], dict):
            problems.append(
                f"coverage JSON has {len(matches)} entries for {module_name}; expected one"
            )
            continue
    for path, value in files.items():
        module_name = PurePosixPath(str(path).replace("\\", "/")).name
        label = module_name if module_name in PRODUCTION_MODULES else str(path)
        summary = value.get("summary") if isinstance(value, dict) else None
        if not isinstance(summary, dict):
            problems.append(f"coverage JSON lacks a summary for {label}")
            continue
        statements = int(summary.get("num_statements", 0))
        covered_lines = int(summary.get("covered_lines", 0))
        branches = int(summary.get("num_branches", 0))
        covered_branches = int(summary.get("covered_branches", 0))
        counts[label] = (
            covered_lines,
            statements,
            covered_branches,
            branches,
        )
        line_rate = 100.0 if statements == 0 else 100.0 * covered_lines / statements
        if module_name in PRODUCTION_MODULES and line_rate < COVERAGE_THRESHOLD:
            problems.append(
                f"{module_name} line coverage {line_rate:.4f}% is below "
                f"{COVERAGE_THRESHOLD:.4f}%"
            )

    if counts:
        covered_lines = sum(item[0] for item in counts.values())
        statements = sum(item[1] for item in counts.values())
        covered_branches = sum(item[2] for item in counts.values())
        branches = sum(item[3] for item in counts.values())
        line_rate = 100.0 if statements == 0 else 100.0 * covered_lines / statements
        branch_rate = 100.0 if branches == 0 else 100.0 * covered_branches / branches
        if line_rate < COVERAGE_THRESHOLD:
            problems.append(
                f"aggregate line coverage {covered_lines}/{statements} = "
                f"{line_rate:.4f}% is below {COVERAGE_THRESHOLD:.4f}%"
            )
        if branch_rate < COVERAGE_THRESHOLD:
            problems.append(
                f"aggregate branch coverage {covered_branches}/{branches} = "
                f"{branch_rate:.4f}% is below {COVERAGE_THRESHOLD:.4f}%"
            )
    return counts, problems


def run_tests(
    root_dir: Path = ROOT,
) -> tuple[int, str, dict[str, tuple[int, int, int, int]], list[str]]:
    with tempfile.TemporaryDirectory(prefix="wdp-pytest-") as raw_tmp:
        temporary = Path(raw_tmp)
        coverage_json = temporary / "coverage.json"
        environment = dict(os.environ)
        environment["COVERAGE_FILE"] = str(temporary / ".coverage")
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        code_dir = str(root_dir / "code")
        current_pythonpath = environment.get("PYTHONPATH", "")
        environment["PYTHONPATH"] = (
            f"{code_dir}{os.pathsep}{current_pythonpath}"
            if current_pythonpath
            else code_dir
        )
        try:
            process = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pytest",
                    "-q",
                    "-ra",
                    "-n",
                    os.environ.get("WDP_TEST_WORKERS", "12"),
                    "--dist=worksteal",
                    "-o",
                    "addopts=",
                    # Tests marked `monorepo` need the engine's native owner or
                    # sibling trees, which a standalone deposit does not contain.
                    "-m",
                    "not monorepo",
                    "-p",
                    "no:cacheprovider",
                    "--no-header",
                    "--basetemp",
                    str(temporary / "pytest"),
                    "--cov=witnessed_difference",
                    "--cov-branch",
                    "--cov-report=term",
                    f"--cov-report=json:{coverage_json}",
                    "--cov-fail-under=0",
                ],
                cwd=str(root_dir),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=int(os.environ.get("WDP_TEST_TIMEOUT", "1800")),
                env=environment,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            msg = f"pytest timed out after {exc.timeout}s"
            print(msg, file=sys.stderr)
            return 1, msg, {}, [msg]
        output = (process.stdout or "") + (process.stderr or "")
        summary = pytest_summary(output)
        if process.returncode:
            print(output, file=sys.stderr)
            return process.returncode, summary, {}, ["pytest failed"]
        if not coverage_json.is_file():
            return 1, summary, {}, ["pytest did not emit coverage JSON"]
        try:
            report = json.loads(coverage_json.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            return 1, summary, {}, [f"coverage JSON is invalid: {error}"]
        counts, problems = coverage_counts(report)
        return (1 if problems else 0), summary, counts, problems


def _group_axiom_reports(transcript: str) -> list[str]:
    lines = transcript.splitlines()
    reports: list[str] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        if "does not depend on any axioms" in line:
            # Strip info prefix if present
            cleaned = re.sub(r"^info:.*?:\d+:\d+:\s*", "", line).strip()
            reports.append(cleaned)
        elif "depends on axioms:" in line:
            chunks = [re.sub(r"^info:.*?:\d+:\d+:\s*", "", line).strip()]
            tail = line.partition("depends on axioms:")[2]
            while "]" not in tail and index + 1 < len(lines):
                index += 1
                continuation = lines[index].strip()
                chunks.append(continuation)
                tail += " " + continuation
            reports.append(" ".join(chunks))
        index += 1
    return reports


def _normalized(text: str) -> str:
    lines = text.replace("\r\n", "\n").replace("\r", "\n").splitlines()
    return "\n".join(line.rstrip() for line in lines).strip() + "\n"


_TARGET_TRIPLE = re.compile(r"[A-Za-z0-9_]+(?:-[A-Za-z0-9_]+){2,3}")


def _platform_neutral(lean_version: str) -> str:
    """Drop the host target triple so the report does not depend on the OS."""

    items = [item.strip() for item in lean_version.strip().split(",")]
    return ", ".join(item for item in items if not _TARGET_TRIPLE.fullmatch(item))


def render_axiom_report(lean_version: str, reports: list[str]) -> str:
    body = "\n".join(reports)
    return (
        "The Witnessed Difference Programme — theorem-level Lean axiom report\n"
        f"Date: {RELEASE_DATE}\n"
        f"Toolchain: {_platform_neutral(lean_version)}\n"
        "Build command: lake build\n"
        "Census command: lake build WitnessedDifference.AxiomReport\n"
        f"Axiom report count: {len(reports)}\n"
        f"Allowed dependencies: {', '.join(sorted(AXIOM_WHITELIST))}\n\n"
        f"{body}\n"
    )


def requested_axiom_declarations(lean_dir: Path) -> list[str]:
    axiom_target = lean_dir / "WitnessedDifference" / "AxiomReport.lean"
    if not axiom_target.is_file():
        return []
    decls = []
    for line in axiom_target.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("#print axioms"):
            parts = line.split()
            if len(parts) >= 3:
                decls.append(parts[2].strip())
    return decls


def capture_axiom_report(
    root_dir: Path = ROOT,
) -> tuple[str, list[str], list[str]]:
    problems: list[str] = []
    lean_dir = root_dir / "lean4"
    sources: list[Path] = []
    for directory, subdirs, files in os.walk(lean_dir):
        subdirs[:] = [name for name in subdirs if name not in IGNORED_DIR_NAMES]
        sources.extend(Path(directory) / name for name in files if name.endswith(".lean"))
    for source in sorted(sources):
        if re.search(r"\b(?:sorry|admit)\b", source.read_text(encoding="utf-8")):
            problems.append(f"placeholder proof token in {source.relative_to(lean_dir)}")
    if problems:
        return "", [], problems

    version = subprocess.run(
        ["lean", "--version"],
        cwd=lean_dir,
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    if version.returncode:
        return "", [], ["Lean version probe failed"]

    if not (lean_dir / ".lake" / "packages" / "mathlib").is_dir():
        return "", [], [
            "Mathlib is not fetched: run `lake exe cache get` in lean4/ first "
            "(on Windows, from a short-path copy; see lean4/README.md)"
        ]
    try:
        build = subprocess.run(
            ["lake", "build", "WitnessedDifference.AxiomReport"],
            cwd=lean_dir,
            capture_output=True,
            text=True,
            timeout=900,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return "", [], ["lake build WitnessedDifference.AxiomReport timed out after 900 s"]
    if build.returncode:
        print(build.stdout + build.stderr, file=sys.stderr)
        return "", [], ["lake build WitnessedDifference.AxiomReport failed"]

    reports = _group_axiom_reports(build.stdout + build.stderr)

    expected_decls = requested_axiom_declarations(lean_dir)
    expected_count = len(expected_decls) if expected_decls else EXPECTED_AXIOM_REPORTS

    if len(reports) != expected_count:
        problems.append(
            f"expected {expected_count} axiom reports, got {len(reports)}"
        )

    reported_decls: list[str] = []
    for report in reports:
        m = re.match(r"^'([^']+)'", report)
        if m:
            reported_decls.append(m.group(1))

    if expected_decls:
        missing = [d for d in expected_decls if d not in reported_decls]
        extra = [d for d in reported_decls if d not in expected_decls]
        if missing:
            problems.append(f"missing {len(missing)} requested declaration report(s): {missing[:3]}")
        if extra:
            problems.append(f"unexpected {len(extra)} extra declaration report(s): {extra[:3]}")
        if len(reported_decls) != len(set(reported_decls)):
            problems.append("duplicate declaration reports detected in axiom census")

    for report in reports:
        if "does not depend on any axioms" in report:
            continue
        match = re.search(r"depends on axioms:\s*\[([^]]*)]", report)
        if match is None:
            problems.append(f"could not parse axiom report: {report}")
            continue
        for name in (item.strip() for item in match.group(1).split(",")):
            if name not in AXIOM_WHITELIST:
                problems.append(f"axiom outside whitelist: {name} in {report}")
    if problems:
        return "", reports, problems
    return render_axiom_report(_normalized(version.stdout + version.stderr), reports), reports, []


def run_lean(root_dir: Path = ROOT) -> tuple[list[str], int]:
    rendered, reports, problems = capture_axiom_report(root_dir)
    report_path = root_dir / AXIOM_REPORT
    if not report_path.is_file():
        problems.append(f"bundled axiom report is missing: {AXIOM_REPORT.as_posix()}")
    elif rendered and report_path.read_text(encoding="utf-8") != rendered:
        problems.append("bundled axiom report is stale or non-deterministic")

    hist_report_path = root_dir / HISTORICAL_AXIOM_REPORT
    if not hist_report_path.is_file():
        problems.append(f"historical axiom report is missing: {HISTORICAL_AXIOM_REPORT.as_posix()}")

    if not problems:
        print(
            f"lean: build clean; bundled report matches {len(reports)} theorem "
            f"reports within {sorted(AXIOM_WHITELIST)}"
        )
    return problems, len(reports)


def check_archive_reproducibility(
    entries: dict[str, str], root_dir: Path = ROOT
) -> list[str]:
    problems: list[str] = []
    script = root_dir / "scripts" / "build_deposit_zip.py"
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    with tempfile.TemporaryDirectory(prefix="wdp-archive-") as raw_tmp:
        archives = [Path(raw_tmp) / "first.zip", Path(raw_tmp) / "second.zip"]
        for archive in archives:
            process = subprocess.run(
                [sys.executable, str(script), "--out", str(archive)],
                cwd=root_dir,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=300,
                env=environment,
                check=False,
            )
            if process.returncode:
                print(process.stdout + process.stderr, file=sys.stderr)
                return ["archive producer failed"]
        if archives[0].read_bytes() != archives[1].read_bytes():
            problems.append("two archive builds produced different bytes")

        committed = root_dir / "dist" / ARCHIVE_NAME
        if committed.is_file() and committed.read_bytes() != archives[0].read_bytes():
            problems.append("clean archive build does not reproduce committed archive")

        prefix = root_dir.name
        expected = {f"{prefix}/{relative}" for relative in entries}
        expected.add(f"{prefix}/SHA256SUMS")
        with zipfile.ZipFile(archives[0]) as handle:
            names = handle.namelist()
            if len(names) != len(set(names)):
                problems.append("archive has duplicate members")
            if set(names) != expected:
                problems.append("archive member set differs from the pinned public set")
            for info in handle.infolist():
                if info.date_time != RELEASE_ZIP_DATE:
                    problems.append(f"archive timestamp drift for {info.filename}")
                    break
    if not problems:
        print(
            f"archive: two builds matched; {len(entries) + 1} members under "
            f"{root_dir.name}/ with fixed timestamps"
        )
    return problems


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lean", action="store_true", help="compile and compare the Lean axiom census")
    parser.add_argument("--archive", action="store_true", help="build and compare two release archives")
    parser.add_argument(
        "--integrity-only",
        "--manifest-only",
        dest="integrity_only",
        action="store_true",
        help="verify manifest and package surface only; do not run tests",
    )
    args = parser.parse_args(argv)
    entries = parse_manifest()
    problems = (
        check_hashes(entries)
        + sweep_unlisted(entries)
        + check_required(entries)
        + check_release_contracts(entries)
    )
    if problems:
        for problem in problems:
            print(f"FAIL: {problem}", file=sys.stderr)
        print(f"verification FAILED: {len(problems)} package problem(s)")
        return 1
    print(f"files: all {len(entries)} pinned members verified")
    if args.integrity_only:
        print("OK: manifest and package integrity checks passed.")
        return 0

    return_code, summary, counts, coverage_problems = run_tests()
    if return_code or coverage_problems:
        for problem in coverage_problems:
            print(f"FAIL: {problem}", file=sys.stderr)
        print(f"verification FAILED: test or coverage gate failed -- {summary}")
        return 1
    if any(token in summary for token in ("skipped", "xfailed", "xpassed", "error")):
        print(f"verification FAILED: suite was not clean -- {summary}", file=sys.stderr)
        return 1
    print(f"tests: {summary}")
    for module_name, values in sorted(counts.items()):
        covered_lines, statements, covered_branches, branches = values
        line_pct = 100.0 if statements == 0 else 100.0 * covered_lines / statements
        branch_pct = 100.0 if branches == 0 else 100.0 * covered_branches / branches
        print(
            f"coverage: {module_name}: statements {covered_lines}/{statements} "
            f"({line_pct:.2f}%), branches {covered_branches}/{branches} "
            f"({branch_pct:.2f}%)"
        )
    total_lines = sum(values[0] for values in counts.values())
    total_statements = sum(values[1] for values in counts.values())
    total_covered_branches = sum(values[2] for values in counts.values())
    total_branches = sum(values[3] for values in counts.values())
    tot_line_pct = 100.0 * total_lines / total_statements
    tot_br_pct = 100.0 * total_covered_branches / total_branches
    print(
        f"coverage total: statements {total_lines}/{total_statements} "
        f"({tot_line_pct:.2f}%), branches {total_covered_branches}/{total_branches} "
        f"({tot_br_pct:.2f}%)"
    )

    axiom_count = 0
    if args.lean:
        lean_problems, axiom_count = run_lean()
        problems.extend(lean_problems)
    if args.archive:
        problems.extend(check_archive_reproducibility(entries))
    if problems:
        for problem in problems:
            print(f"FAIL: {problem}", file=sys.stderr)
        print(f"verification FAILED: {len(problems)} replay problem(s)")
        return 1

    detail = f", {axiom_count} axiom reports" if args.lean else ""
    print(
        f"verified: {len(entries)} files pinned, suite passed{detail}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
