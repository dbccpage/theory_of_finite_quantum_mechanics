"""Write the deterministic PO-000 replay and its SHA-256 manifest."""

from __future__ import annotations
import argparse
import hashlib
from pathlib import Path

from omega_engine.crates.projection_obstruction.po000_replay import (
    PACKAGE_ROOT,
    build_mechanization_run,
)


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

    run = build_mechanization_run(package_root)
    certificate = certificate_path.resolve()
    manifest = manifest_path.resolve()
    certificate.parent.mkdir(parents=True, exist_ok=True)
    manifest.parent.mkdir(parents=True, exist_ok=True)
    certificate.write_text(run.model_dump_json(indent=2) + "\n", encoding="utf-8")

    entries = dict(run.source_hashes)
    entries.update(
        {f"../{relative}": digest for relative, digest in run.publication_hashes.items()}
    )
    try:
        certificate_label = certificate.relative_to(package_root.resolve()).as_posix()
    except ValueError:
        certificate_label = certificate.name
    entries[certificate_label] = _sha256(certificate)
    manifest.write_text(
        "".join(f"{digest}  {relative}\n" for relative, digest in sorted(entries.items())),
        encoding="utf-8",
    )
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
        default=PACKAGE_ROOT / "SHA256SUMS",
    )
    args = parser.parse_args(argv)
    certificate, manifest = write_artifact_bundle(args.certificate, args.manifest)
    print(certificate)
    print(manifest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())



