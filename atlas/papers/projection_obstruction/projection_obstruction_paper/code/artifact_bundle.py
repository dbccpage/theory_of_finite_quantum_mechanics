"""Write the deterministic PO-000 replay and its SHA-256 manifest."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from replay import PACKAGE_ROOT, build_mechanization_run


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_artifact_bundle(
    certificate_path: Path,
    manifest_path: Path,
    *,
    package_root: Path = PACKAGE_ROOT,
) -> tuple[Path, Path]:
    """Write a replay certificate plus a non-self-referential hash manifest."""

    certificate = certificate_path.resolve()
    manifest = manifest_path.resolve()
    if certificate == manifest:
        raise ValueError(
            f"certificate_path and manifest_path must be distinct resolved files, got '{certificate}'"
        )

    run = build_mechanization_run(package_root)
    pkg_resolved = package_root.resolve()

    input_paths = {
        (pkg_resolved / rel).resolve()
        for rel in list(run.source_hashes.keys()) + list(run.publication_hashes.keys())
    }

    if certificate in input_paths:
        raise ValueError(
            f"certificate output path '{certificate}' collides with read-only hashed input file"
        )
    if manifest in input_paths:
        raise ValueError(
            f"manifest output path '{manifest}' collides with read-only hashed input file"
        )

    certificate.parent.mkdir(parents=True, exist_ok=True)
    manifest.parent.mkdir(parents=True, exist_ok=True)

    cert_bytes = (run.model_dump_json(indent=2) + "\n").encode("utf-8")
    temp_cert = certificate.with_suffix(".tmp_cert")
    temp_cert.write_bytes(cert_bytes)
    temp_cert.replace(certificate)

    entries = dict(run.source_hashes)
    entries.update(dict(run.publication_hashes))
    try:
        certificate_label = certificate.relative_to(pkg_resolved).as_posix()
    except ValueError:
        certificate_label = certificate.name
    entries[certificate_label] = _sha256(certificate)

    manifest_bytes = "".join(
        f"{digest}  {relative}\n"
        for relative, digest in sorted(entries.items())
    ).encode("utf-8")
    temp_manifest = manifest.with_suffix(".tmp_manifest")
    temp_manifest.write_bytes(manifest_bytes)
    temp_manifest.replace(manifest)

    return certificate, manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--certificate",
        type=Path,
        default=PACKAGE_ROOT / "evidence" / "000_mechanization_run.json",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        # 2026-08-31: default moved into evidence/ so a replay cannot clobber
        # the release-wide SHA256SUMS manifest at the package root, which is a
        # different artifact (full-tree checksums written at release time).
        default=PACKAGE_ROOT / "evidence" / "SHA256SUMS",
    )
    args = parser.parse_args(argv)
    certificate, manifest = write_artifact_bundle(args.certificate, args.manifest)
    print(certificate)
    print(manifest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
