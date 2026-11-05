#!/usr/bin/env python3
"""One-command verifier for the PO-000 (Projection Obstruction) deposit.

AuthorityEffect: None. A successful run establishes reproducibility of the
finite package. It does not prove empirical hypotheses or authorize deployment.

Checks performed:
1. Manifest integrity: MANIFEST.sha256 covers payload; SHA256SUMS covers payload
   plus that manifest. Both exact member sets and every recorded hash are checked.
2. Sweep unlisted files: no regular file exists in the deposit tree that SHA256SUMS does not list
   (except SHA256SUMS itself and excluded transient/VCS directories).
3. Required release surface: critical files (manuscript, ledgers, configs, tests, scripts) are pinned.
4. Python profiles: standalone deselects native integration; selected tests must not skip.
5. Replay & independent verification: re-runs claim mechanization and validates receipt via verify_certificate.py.
6. Exact selected archive: complete canonical bytes and regular sidecar; deterministic rebuild.
--integrity-only reports a partial check. --lean-source-scan is not Lean compilation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from collections.abc import Callable
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "SHA256SUMS"
sys.path.insert(0, str(ROOT / "scripts"))
from build_release_zip import canonical_bytes
from release_custody import files, identity, regular, snapshot, unchanged

IGNORED_DIR_NAMES = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".hypothesis",
    ".mypy_cache",
    ".ruff_cache",
    ".ipynb_checkpoints",
    ".lake",
    "dist",
    "build",
    "htmlcov",
}

IGNORED_SUFFIXES = {".pyc", ".pyo", ".zip", ".sha256"}

IGNORED_FILE_NAMES = {
    ".coverage",
    # Local Lake cache resolution is host-specific, not part of the deposit.
    "lake-manifest.json",
    "projection_obstruction.aux",
    "projection_obstruction.log",
    "projection_obstruction.toc",
    "paper_composition_manifest.json",
    "paper_composition_manifest.yaml",
    "paper_composition_receipt.json",
}

ROOT_CONTROL_FILES = {"SHA256SUMS", "MANIFEST.sha256"}

REQUIRED_FILES = (
    "MANIFEST.sha256",
    "README.md",
    "LICENSE",
    "pyproject.toml",
    "projection_obstruction.md",
    "projection_obstruction.pdf",
    "projection_obstruction.tex",
    "projection_obstruction_change_log.md",
    "projection_obstruction_claim_ledger.md",
    "projection_obstruction_claim_ledger.yaml",
    "scripts/build_enter_notebook.py",
    "scripts/build_paper_artifacts.py",
    "scripts/build_release_zip.py",
    "scripts/obstruction-preamble.tex",
    "scripts/regen_sha256sums.py",
    "code/replay.py",
    "code/verify_certificate.py",
    "code/finite_certificates.py",
    "code/verify_finite_certificates.py",
    "code/local_persistent_zero.py",
    "docs/claim_dependencies.json",
    "lean4/Po000JordanLie.lean",
    "lean4/Po000JordanLieImage.lean",
    "lean4/Po000JordanTrace.lean",
    "lean4/lakefile.lean",
    "lean4/lean-toolchain",
    "verify_deposit.py",
    "release_identity.json",
    "scripts/release_custody.py",
)


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _validated_manifest_path(
    relative: str, lineno: int, root_dir: Path, manifest_name: str = "SHA256SUMS"
) -> Path:
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
    try:
        candidate.resolve().relative_to(root_dir.resolve())
    except ValueError:
        unsafe = True
    if candidate.exists() or candidate.is_symlink():
        regular(candidate, root_dir)
    if candidate.is_symlink():
        unsafe = True
    if unsafe:
        raise SystemExit(
            f"FAIL: {manifest_name} line {lineno} has unsafe path {relative!r}"
        )
    return candidate


def parse_manifest(
    manifest_path: Path = MANIFEST, root_dir: Path = ROOT
) -> dict[str, str]:
    manifest_name = manifest_path.name
    regular(manifest_path, root_dir)
    if not manifest_path.is_file():
        raise SystemExit(f"FAIL: {manifest_name} is missing; run scripts/regen_sha256sums.py first")
    entries: dict[str, str] = {}
    for lineno, raw in enumerate(
        manifest_path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split(None, 1)
        if len(parts) != 2 or re.fullmatch(r"[0-9a-fA-F]{64}", parts[0]) is None:
            raise SystemExit(
                f"FAIL: {manifest_name} line {lineno} is malformed: {raw!r}"
            )
        digest, relative = parts[0].lower(), parts[1].strip().lstrip("*")
        _validated_manifest_path(relative, lineno, root_dir, manifest_name)
        if relative.casefold() in {path.casefold() for path in entries}:
            raise SystemExit(f"FAIL: {manifest_name} lists {relative} more than once")
        entries[relative] = digest
    return entries


def check_hashes(
    entries: dict[str, str], root_dir: Path = ROOT, manifest_name: str = "SHA256SUMS"
) -> list[str]:
    problems: list[str] = []
    for relative, digest in sorted(entries.items()):
        path = root_dir / relative
        if not path.is_file():
            problems.append(f"missing file listed in {manifest_name}: {relative}")
        elif sha256_of(path) != digest:
            problems.append(f"hash mismatch in {manifest_name} for {relative}")
    return problems


def check_manifest_pair(entries: dict[str, str], root_dir: Path = ROOT) -> list[str]:
    """Independently verify noncircular membership and hashes of the inner manifest.

    A primary hash of a stale MANIFEST.sha256 is not sufficient. Enumerate the
    admitted physical payload and validate the inner manifest against it, rather
    than accepting an outer checksum or silently regenerating either control.
    """
    secondary_name = "MANIFEST.sha256"
    secondary = parse_manifest(root_dir / secondary_name, root_dir)
    payload = {path.relative_to(root_dir).as_posix() for path in files(root_dir)}
    payload -= ROOT_CONTROL_FILES
    problems = check_hashes(secondary, root_dir, secondary_name)
    for name, recorded, expected in (
        (secondary_name, set(secondary), payload),
        ("SHA256SUMS", set(entries), payload | {secondary_name}),
    ):
        for relative in sorted(expected - recorded):
            problems.append(f"file present but not listed in {name}: {relative}")
        for relative in sorted(recorded - expected):
            problems.append(f"file outside {name} coverage: {relative}")
    return problems


def sweep_unlisted(
    entries: dict[str, str], root_dir: Path = ROOT
) -> list[str]:
    return [f"file present but not listed in SHA256SUMS: {path.relative_to(root_dir).as_posix()}"
            for path in files(root_dir)
            if path.relative_to(root_dir).as_posix() not in {*entries, "SHA256SUMS"}]


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


def pytest_summary(output: str) -> str:
    lines = [line for line in output.splitlines() if line.strip()]
    for line in reversed(lines):
        if re.search(r"\b\d+ passed\b", line):
            return line
    return lines[-1] if lines else "(no pytest output)"


def run_tests(root_dir: Path = ROOT, profile: str = "standalone") -> tuple[int, str, list[str]]:
    with tempfile.TemporaryDirectory(prefix="po000-pytest-") as raw_tmp:
        temporary = Path(raw_tmp)
        environment = dict(os.environ)
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        environment["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
        code_dir = str(root_dir / "code")
        environment["PYTHONPATH"] = os.pathsep.join((code_dir, str(root_dir / "scripts")))
        environment["PO000_NATIVE_INTEGRATION"] = "1" if profile == "native" else "0"
        process = subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                "-q",
                "-ra",
                "-p",
                "no:cacheprovider",
                "--no-header",
                "--runxfail",
                "--basetemp",
                str(temporary / "pytest"),
                *(["-m", "not native_integration"] if profile == "standalone" else []),
                "code/tests",
            ],
            cwd=str(root_dir),
            capture_output=True,
            text=True,
            timeout=600,
            env=environment,
            check=False,
        )
        output = (process.stdout or "") + (process.stderr or "")
        summary = pytest_summary(output)
        if (
            process.returncode != 0
            or re.search(r"\b\d+ (?:skipped|xfailed|xpassed)\b", output)
            or not re.search(r"\b\d+ passed\b", output)
        ):
            print(output, file=sys.stderr)
            return (
                process.returncode or 1,
                summary,
                ["pytest failed, unexpectedly skipped tests, contained expected failures (xfail/xpass), or had no passing tests"],
            )
        return 0, summary, []


def run_replay_and_certificate(
    root_dir: Path = ROOT, profile: str = "standalone", guard: Callable[[], None] = lambda: None
) -> list[str]:
    problems: list[str] = []
    with tempfile.TemporaryDirectory(prefix="po000-cert-") as raw_tmp:
        cert_path = Path(raw_tmp) / "mechanization_run.json"
        environment = dict(os.environ)
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        environment["PYTHONPATH"] = str(root_dir / "code")
        environment["PO000_NATIVE_INTEGRATION"] = "1" if profile == "native" else "0"

        replay_proc = subprocess.run(
            [
                sys.executable,
                str(root_dir / "code" / "replay.py"),
                "--output",
                str(cert_path),
            ],
            cwd=str(root_dir),
            capture_output=True,
            text=True,
            timeout=300,
            env=environment,
            check=False,
        )
        guard()
        if replay_proc.returncode != 0:
            print(replay_proc.stdout + replay_proc.stderr, file=sys.stderr)
            return ["replay.py execution failed"]

        if not cert_path.is_file():
            return ["replay.py did not emit certificate file"]

        verify_proc = subprocess.run(
            [
                sys.executable,
                str(root_dir / "code" / "verify_certificate.py"),
                str(cert_path),
            ],
            cwd=str(root_dir),
            capture_output=True,
            text=True,
            timeout=60,
            env=environment,
            check=False,
        )
        guard()
        if verify_proc.returncode != 0:
            print(verify_proc.stdout + verify_proc.stderr, file=sys.stderr)
            return ["verify_certificate.py rejected replay certificate"]

        run = json.loads(cert_path.read_text(encoding="utf-8"))
        finite = run.get("finite_certificates", {})
        native_names = ("separable_correlated", "three_factor", "ising_five_cycle")
        if profile == "native" and any(finite.get(name, {}).get("status") != "verified" for name in native_names):
            problems.append("native profile did not verify every measurement record")
        print("measurement records: " + ", ".join(
            f"{name}={finite.get(name, {}).get('status', 'missing')}" for name in native_names))
        try:
            verdict_json = json.loads(verify_proc.stdout.strip().splitlines()[-1])
            if verdict_json.get("verdict") != "pass":
                problems.append(f"certificate verdict was {verdict_json.get('verdict')}")
            if verdict_json.get("errors"):
                problems.append(f"certificate errors: {verdict_json.get('errors')}")
        except Exception as exc:
            problems.append(f"failed to parse verify_certificate.py output: {exc}")

    return problems


def check_archive_reproducibility(root_dir: Path = ROOT, guard: Callable[[], None] = lambda: None) -> list[str]:
    problems: list[str] = []
    script = root_dir / "scripts" / "build_release_zip.py"
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    with tempfile.TemporaryDirectory(prefix="po000-archive-") as raw_tmp:
        tmp_dir = Path(raw_tmp)
        process = subprocess.run(
            [sys.executable, str(script), "--output", str(tmp_dir), "--check"],
            cwd=str(root_dir),
            capture_output=True,
            text=True,
            timeout=300,
            env=environment,
            check=False,
        )
        guard()
        if process.returncode != 0:
            print(process.stdout + process.stderr, file=sys.stderr)
            return ["archive build reproducibility check failed"]
    return problems


def scan_lean_sources(root_dir: Path = ROOT) -> tuple[list[str], int]:
    problems: list[str] = []
    lean_dir = root_dir / "lean4"
    if not lean_dir.is_dir():
        return ["lean4/ directory is missing"], 0
    lean_files = sorted(lean_dir.glob("*.lean"))
    for file in lean_files:
        content = file.read_text(encoding="utf-8")
        if re.search(r"\b(?:sorry|admit)\b", content):
            problems.append(f"placeholder proof token found in {file.name}")
    return problems, len(lean_files)


def check_selected_archive(archive: Path, root_dir: Path = ROOT) -> dict[str, str]:
    sidecar = archive.with_suffix(".zip.sha256")
    for control in (archive, sidecar):
        regular(control, Path(control.anchor))
    data = archive.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if sidecar.read_bytes() != f"{digest}  {archive.name}\n".encode("utf-8"):
        raise ValueError("selected archive sidecar mismatch")
    if data != canonical_bytes(root_dir):
        raise ValueError("selected archive differs from canonical complete ZIP envelope")
    return {str(archive): digest, str(sidecar): sha256_of(sidecar)}


def verify(args: argparse.Namespace) -> int:
    entries = parse_manifest()
    problems = (check_hashes(entries) + sweep_unlisted(entries)
                + check_required(entries) + check_manifest_pair(entries))
    if problems:
        raise ValueError("; ".join(problems))
    release = identity(ROOT)
    archive_path = args.archive or (ROOT / "dist" / f"projection_obstruction_v{release['release_version']}.zip")
    archive = archive_path.absolute()
    if args.archive:
        controls = check_selected_archive(archive)
        archive_verified = True
    elif archive.is_file():
        controls = check_selected_archive(archive)
        archive_verified = True
    else:
        if getattr(args, "require_archive", False):
            raise ValueError(f"required release archive not found: {archive}")
        controls = {}
        archive_verified = False
    # The shared physical payload selector excludes .sha256 sidecars. Bind this
    # explicit root control separately so same-byte links and later mutations
    # cannot escape the release guard.
    secondary = ROOT / "MANIFEST.sha256"
    regular(secondary, ROOT)
    controls[str(secondary)] = sha256_of(secondary)
    initial = snapshot(ROOT)

    def guard() -> None:
        unchanged(ROOT, initial)
        for name, digest in controls.items():
            control = Path(name)
            regular(control, Path(control.anchor))
            if sha256_of(control) != digest:
                raise ValueError(f"selected archive control changed: {control}")

    if archive_verified:
        print(f"integrity: {len(entries)} pinned payload files; exact selected archive and sidecar verified")
    else:
        print(f"integrity: {len(entries)} pinned payload files; bare repository payload verified")
    if args.lean_source_scan:
        scan_problems, count = scan_lean_sources()
        if scan_problems:
            raise ValueError("; ".join(scan_problems))
        print(f"Lean SOURCE SCAN ONLY: {count} files; no lexical sorry/admit tokens. No compilation or axiom audit.")
    if args.integrity_only:
        guard()
        print("PARTIAL: integrity only; Python tests, replay, native integration and Lean compilation not executed.")
        return 0
    ret, summary, test_problems = run_tests(profile=args.profile)
    guard()
    if ret or test_problems:
        raise ValueError(f"{test_problems}: {summary}")
    print(f"tests ({args.profile}): {summary}")
    cert_problems = run_replay_and_certificate(profile=args.profile, guard=guard)
    if cert_problems:
        raise ValueError("; ".join(cert_problems))
    archive_problems = check_archive_reproducibility(guard=guard)
    if archive_problems:
        raise ValueError("; ".join(archive_problems))
    guard()
    if archive_verified:
        print(f"PASS ({args.profile} profile): selected archive, Python tests and scoped replay verified.")
    else:
        print(f"PASS ({args.profile} profile): repository payload, Python tests and scoped replay verified (archive verification NOT performed).")
    if args.profile == "standalone":
        print("Native measurement integration NOT VERIFIED; native tests deliberately deselected.")
    print("Lean compilation/axiom audit and publication approval NOT established.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--profile", choices=("standalone", "native"), default="standalone")
    parser.add_argument("--archive", type=Path, help="exact selected release ZIP (sidecar required)")
    parser.add_argument("--require-archive", action="store_true", help="require release archive and sidecar to be verified")
    parser.add_argument("--integrity-only", action="store_true", help="partial integrity check; no test/replay claim")
    parser.add_argument("--lean-source-scan", action="store_true", help="lexical token scan only; does not compile Lean")
    args = parser.parse_args(argv)
    try:
        return verify(args)
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError, SystemExit) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
