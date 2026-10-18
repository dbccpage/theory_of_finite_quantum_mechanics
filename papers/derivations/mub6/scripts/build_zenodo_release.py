"""Zenodo Release Archive Bundling, Checksum Certification & Checklist Verifier.

AuthorityEffect: None.

Performs:
1. File collection & strict exclusion enforcement.
2. Reproducible, hermetic tarball construction: zenodo/mub6_formal_archive_v1.0.tar.gz
3. Manifest and checklist updates with exact SHA-256 digests.
4. Comprehensive release manifest generation: zenodo/release_manifest.sha256
5. Dry-run extraction test and 100% bit-for-bit SHA-256 verification.
"""

from __future__ import annotations

import gzip
import hashlib
import io
import json
import os
import shutil
import tarfile
from pathlib import Path
from typing import Dict, List, Set, Tuple

FIXED_MTIME = 1790188813
TARBALL_PATH = Path("zenodo/mub6_formal_archive_v1.0.tar.gz")
SHA256_MANIFEST_PATH = Path("zenodo/release_manifest.sha256")
RELEASE_MANIFEST_JSON_PATH = Path("zenodo/release_manifest.json")
RELEASE_CHECKLIST_PATH = Path("zenodo/release_checklist.md")

CANONICAL_RECEIPTS = [
    "mub_target_a2_deltoid_cusp_receipt.json",
    "mub_target_a8_collar_boundary_receipt.json",
    "mub_target_a9_haagerup_receipt.json",
    "mub_target_a10_global_cover_receipt.json",
    "mub_target_a11_orbit_exhaustiveness_receipt.json",
    "mub_target_a12_smale_sentry_receipt.json",
    "mub_target_a13_grand_synthesis_receipt.json",
    "mub_target_b1_continuous_chaining_receipt.json",
    "mub_target_b2_global_gluing_receipt.json",
    "mub_target_b3_manifold_integration_receipt.json",
    "mub_decisive_bifurcation_terminal_receipt.json",
    "manifest.json",
]

EXCLUDE_DIR_NAMES: Set[str] = {
    ".git",
    ".github",
    "target",
    ".lake",
    "lake-packages",
    "build",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    ".agents",
    "scratch",
    "logs",
    ".venv",
    "venv",
}

EXCLUDE_EXTENSIONS: Tuple[str, ...] = (
    ".pyc",
    ".pyo",
    ".swp",
    ".swo",
    "~",
    ".tmp",
    ".bak",
    ".log",
    ".pdb",
    ".rs.bk",
)

EXCLUDE_FILENAMES: Set[str] = {
    ".DS_Store",
    "Thumbs.db",
    ".gitignore",
    ".gitattributes",
    ".gitmodules",
    ".env",
}


def is_excluded(rel_path: str) -> bool:
    parts = Path(rel_path).parts
    for part in parts:
        if part in EXCLUDE_DIR_NAMES:
            return True
        if part.startswith(".git"):
            return True
        if part.startswith("mutants.out"):
            return True
    fname = Path(rel_path).name
    if fname in EXCLUDE_FILENAMES:
        return True
    if fname.startswith(".git"):
        return True
    if fname.endswith(EXCLUDE_EXTENSIONS):
        return True
    return False


def collect_archive_files() -> List[str]:
    """Collect all authorized files for inclusion in the formal archive."""
    collected: List[str] = []

    scan_dirs = [
        "lean4",
        "code/mub_verify",
        "omega_engine/crates_rs",
        "research",
    ]

    for d in scan_dirs:
        for root, dirs, filenames in os.walk(d):
            dirs[:] = [
                sub for sub in dirs
                if not is_excluded(Path(os.path.join(root, sub)).as_posix())
            ]
            for fn in filenames:
                p = os.path.join(root, fn)
                rel = Path(p).as_posix()
                if not is_excluded(rel):
                    collected.append(rel)

    for r in sorted(CANONICAL_RECEIPTS):
        p = f"artifacts/{r}"
        if not os.path.exists(p):
            raise FileNotFoundError(f"Missing canonical receipt in artifacts/: {p}")
        collected.append(p)

    extra_package_inits = [
        "omega_engine/__init__.py",
        "omega_engine/crates/__init__.py",
    ]
    for init_file in extra_package_inits:
        if os.path.exists(init_file):
            collected.append(init_file)

    collected = sorted(set(collected))

    for f in collected:
        parts = Path(f).parts
        for p in parts[:-1]:
            if p in EXCLUDE_DIR_NAMES or p.startswith(".git"):
                raise ValueError(f"Exclusion violation in directory: {f} (part '{p}')")
        fname = parts[-1]
        if fname in EXCLUDE_FILENAMES or fname.startswith(".git") or fname.endswith(EXCLUDE_EXTENSIONS):
            raise ValueError(f"Exclusion violation in file: {f}")

    return collected


def compute_sha256(filepath: Path | str) -> str:
    """Compute exact raw SHA-256 hex digest of a file."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def compute_bytes_sha256(data: bytes) -> str:
    """Compute raw SHA-256 hex digest of bytes."""
    return hashlib.sha256(data).hexdigest()


def build_hermetic_tarball(files: List[str], output_path: Path) -> str:
    """Construct a bit-for-bit reproducible, hermetic tar.gz archive."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    dir_entries: Set[str] = set()
    for f in files:
        parts = Path(f).parts
        for i in range(1, len(parts)):
            dir_entries.add("/".join(parts[:i]))
    sorted_dirs = sorted(dir_entries)

    buf = io.BytesIO()

    with gzip.GzipFile(fileobj=buf, mode="wb", mtime=0.0) as gz:
        with tarfile.open(fileobj=gz, mode="w") as tar:
            for d in sorted_dirs:
                ti_dir = tarfile.TarInfo(name=d)
                ti_dir.type = tarfile.DIRTYPE
                ti_dir.mode = 0o755
                ti_dir.mtime = FIXED_MTIME
                ti_dir.uid = 0
                ti_dir.gid = 0
                ti_dir.uname = "root"
                ti_dir.gname = "root"
                tar.addfile(ti_dir)

            for f in files:
                p = Path(f)
                content = p.read_bytes()
                ti = tarfile.TarInfo(name=f)
                ti.type = tarfile.REGTYPE
                ti.mode = 0o644
                ti.size = len(content)
                ti.mtime = FIXED_MTIME
                ti.uid = 0
                ti.gid = 0
                ti.uname = "root"
                ti.gname = "root"
                tar.addfile(ti, fileobj=io.BytesIO(content))

    tarball_bytes = buf.getvalue()
    output_path.write_bytes(tarball_bytes)
    digest = hashlib.sha256(tarball_bytes).hexdigest()
    print(f"Built hermetic tarball: {output_path} ({len(tarball_bytes):,} bytes, SHA-256: {digest})")
    return digest


def verify_dry_run_unpack(tarball_path: Path, archive_files: List[str], digests: Dict[str, str]) -> None:
    """Unpack tarball in an isolated dry-run directory and verify 100% SHA-256 match."""
    scratch_dir = Path("scratch/dry_run_zenodo_unpack").resolve()
    project_root = Path.cwd().resolve()
    if scratch_dir != project_root / "scratch" / "dry_run_zenodo_unpack":
        raise ValueError("Dry-run directory resolves outside the designated project scratch path")
    if scratch_dir.exists():
        shutil.rmtree(scratch_dir)
    scratch_dir.mkdir(parents=True, exist_ok=True)

    try:
        print(f"Extracting {tarball_path} to {scratch_dir}...")
        with tarfile.open(tarball_path, "r:gz") as tar:
            tar.extractall(path=scratch_dir)

        extracted_files: List[str] = []
        for root, dirs, filenames in os.walk(scratch_dir):
            for fn in filenames:
                p = os.path.join(root, fn)
                rel = Path(os.path.relpath(p, scratch_dir)).as_posix()
                extracted_files.append(rel)

        extracted_files = sorted(extracted_files)

        if len(extracted_files) != len(archive_files):
            raise AssertionError(
                f"File count mismatch: expected {len(archive_files)}, extracted {len(extracted_files)}"
            )

        print(f"Extracted {len(extracted_files)} files. Verifying exact SHA-256 digests...")
        for rel in extracted_files:
            if is_excluded(rel):
                raise AssertionError(f"Excluded file found in extracted archive: {rel}")
            extracted_path = scratch_dir / rel
            ext_digest = compute_sha256(extracted_path)
            expected_digest = digests.get(rel)
            if expected_digest is None:
                raise AssertionError(f"Extracted file not in expected digest manifest: {rel}")
            if ext_digest != expected_digest:
                raise AssertionError(
                    f"Digest mismatch on extracted file {rel}: expected {expected_digest}, got {ext_digest}"
                )

        print("Dry-run extraction passed: 100% bit-for-bit SHA-256 match across all archive files!")
    finally:
        if scratch_dir.exists():
            shutil.rmtree(scratch_dir)
            print(f"Cleaned up {scratch_dir}.")


def update_release_manifest_json(tarball_digest: str, archive_files: List[str]) -> None:
    """Record byte custody without minting mathematical or deposit approval."""
    paper = Path("mub6.md")
    paper_bytes = paper.read_bytes()
    non_archive = [
        TARBALL_PATH.as_posix(),
        RELEASE_CHECKLIST_PATH.as_posix(),
        RELEASE_MANIFEST_JSON_PATH.as_posix(),
    ]
    manifest = {
        "manifest_version": "1.1.0",
        "schema_version": "omega.mub.zenodo_release_manifest.v1",
        "project": "MUB(6)",
        "bundle_title": "MUB(6) historical research artifact archive with updated gap registry",
        "authority_effect": "None",
        "checkpoint_date": "2026-10-15",
        "license": "Apache-2.0",
        "publication_ready": False,
        "publication_status": "BLOCKED",
        "unresolved_obligations": [
            "Concrete certified Route C landing",
            "Generic native runtime/decoder qualification as needed, rectangular parity for later inputs, full 56-cell and three-cusp native replay and analytic kernel reflection",
            "Required variety emptiness and parameter coverage; justify flatness for proposed moment data",
            "Current manuscript and formal sources are not included in this historical archive layout",
        ],
        "canonical_manuscript": {
            "file": paper.as_posix(),
            "included_in_archive": False,
            "hashes": {
                "bytes": len(paper_bytes),
                "sha256_raw": compute_bytes_sha256(paper_bytes),
                "sha256_canonical_lf": compute_bytes_sha256(paper_bytes.replace(b"\r\n", b"\n")),
            },
        },
        "release_archive": {
            "filename": TARBALL_PATH.name,
            "path": TARBALL_PATH.as_posix(),
            "sha256": tarball_digest,
        },
        "receipt_inventory_scope": "Historical receipt labels are not renewed mathematical certificates.",
        "manuscript_license": "CC-BY-4.0",
        "custody_counts": {
            "manifest_entry_count": len(archive_files) + len(non_archive),
            "archive_file_member_count": len(archive_files),
            "non_archive_entries": non_archive,
        },
    }
    RELEASE_MANIFEST_JSON_PATH.write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n"
    )


def update_release_checklist(tarball_digest: str, archive_file_count: int) -> None:
    """Keep archive integrity separate from the unresolved publication gates."""
    text = f"""# MUB(6) Phase 6 Publication Release Checklist

AuthorityEffect: None.
Checkpoint: 2026-10-10.
Publication status: BLOCKED. Publication ready: false.

The former approval label is withdrawn. The current archive records historical
research artifacts with the current gap registry. Its legacy layout excludes the
current manuscript and the canonical Lean source tree. It is not the completed
publication package requested by the Option B roadmap.

## Byte-custody checks

Archive: `{TARBALL_PATH.as_posix()}`
SHA-256: `{tarball_digest}`
File members: {archive_file_count}.

These values are independently checked by the manifest and extraction tests.
Digest agreement does not establish a theorem or approve a deposit.

## Unresolved publication gates

- Concrete Route C Fourier landing and chart soundness.
- Generic runtime/decoder qualification as needed and rectangular parity for later inputs, complete 56-cell/cusp execution and analytic reflection.
  Continuous phase-family construction and variable-basis equations are checked.
- Required variety emptiness and parameter coverage; justify flatness for proposed data.
  The direct real coordinate positive-flat extraction is checked, with explicit premises.
- Current-source archive layout and package recertification.

Build, axiom and suite outcomes are recorded in the dated executive checkpoint;
this archive builder does not execute those gates.

Verdict: NO-GO for the current arXiv submission and a new Zenodo deposit asserting
mathematical closure. No external submission or deposit has been made.
"""
    RELEASE_CHECKLIST_PATH.write_text(text, encoding="utf-8", newline="\n")


def generate_sha256_manifest(archive_files: List[str], tarball_path: Path) -> None:
    """Generate zenodo/release_manifest.sha256 covering all archive files and release artifacts."""
    manifest_entries: List[Tuple[str, str]] = []

    for rel_path in archive_files:
        p = Path(rel_path)
        digest = compute_sha256(p)
        manifest_entries.append((digest, rel_path))

    release_artifacts = [
        tarball_path.as_posix(),
        RELEASE_MANIFEST_JSON_PATH.as_posix(),
        RELEASE_CHECKLIST_PATH.as_posix(),
    ]
    for rel_path in release_artifacts:
        p = Path(rel_path)
        digest = compute_sha256(p)
        manifest_entries.append((digest, rel_path))

    manifest_entries.sort(key=lambda item: item[1])

    with open(SHA256_MANIFEST_PATH, "w", encoding="utf-8", newline="\n") as f:
        for digest, rel_path in manifest_entries:
            f.write(f"{digest}  {rel_path}\n")

    print(f"Generated {SHA256_MANIFEST_PATH} with {len(manifest_entries)} byte digests.")


def verify_sha256_manifest() -> None:
    """Verify that all entries in zenodo/release_manifest.sha256 match current disk files."""
    with open(SHA256_MANIFEST_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()

    errors: List[str] = []
    checked = 0
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("  ", 1)
        if len(parts) != 2:
            errors.append(f"Malformed manifest line: {line}")
            continue
        expected_digest, rel_path = parts[0], parts[1]
        p = Path(rel_path)
        if not p.exists():
            errors.append(f"Missing file: {rel_path}")
            continue
        actual_digest = compute_sha256(p)
        if actual_digest != expected_digest:
            errors.append(f"Digest mismatch for {rel_path}: expected {expected_digest}, got {actual_digest}")
        checked += 1

    if errors:
        raise AssertionError(f"SHA-256 manifest verification failed with {len(errors)} errors:\n" + "\n".join(errors[:10]))
    print(f"SHA-256 manifest self-verification passed: all {checked} files match digests on disk 100% cleanly!")


def main() -> None:
    print("=" * 80)
    print("ZENODO RELEASE ARCHIVE BUNDLER & CHECKSUM CERTIFIER")
    print("AuthorityEffect: None")
    print("=" * 80)

    print("\n[Step 1] Collecting and auditing archive files...")
    archive_files = collect_archive_files()
    print(f"Total archive files verified: {len(archive_files)}")

    file_digests: Dict[str, str] = {}
    for f in archive_files:
        file_digests[f] = compute_sha256(Path(f))

    print("\n[Step 2] Building hermetic tarball...")
    tarball_digest = build_hermetic_tarball(archive_files, TARBALL_PATH)

    print("\n[Step 3] Running dry-run unpack and verification...")
    verify_dry_run_unpack(TARBALL_PATH, archive_files, file_digests)

    print("\n[Step 4] Updating release manifest and checklist...")
    update_release_manifest_json(tarball_digest, archive_files)
    update_release_checklist(tarball_digest, len(archive_files))

    print("\n[Step 5] Generating release_manifest.sha256...")
    generate_sha256_manifest(archive_files, TARBALL_PATH)

    print("\n[Step 6] Verifying release_manifest.sha256 against on-disk artifacts...")
    verify_sha256_manifest()

    print("\n" + "=" * 80)
    print("Historical archive byte custody built; publication status remains BLOCKED.")
    print(f"  Archive Tarball  : {TARBALL_PATH} ({TARBALL_PATH.stat().st_size:,} bytes)")
    print(f"  Tarball SHA-256  : {tarball_digest}")
    print(f"  Release Manifest : {SHA256_MANIFEST_PATH}")
    print(f"  Checklist Status : {RELEASE_CHECKLIST_PATH} (publication BLOCKED; byte custody only)")
    print("=" * 80)


if __name__ == "__main__":
    main()
