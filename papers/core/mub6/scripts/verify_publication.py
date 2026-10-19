"""Read-only preprint custody checks; no mathematical or publication approval."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import stat
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code"))
from deposit_paths import read_manifest, safe_path, walk_files


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def regular_control(path: Path) -> None:
    safe_path(path.absolute().parent, path.name)
    if not stat.S_ISREG(path.lstat().st_mode):
        raise ValueError(f"Nonregular control file: {path.name}")


def canonical_archive(root: Path, names: set[str], publication_date: str) -> bytes:
    stamp = (*map(int, publication_date.split("-")), 12, 0, 0)
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as target:
        for name in sorted(names):
            info = zipfile.ZipInfo(name, stamp)
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            target.writestr(info, safe_path(root, name).read_bytes())
    return buffer.getvalue()


def verify(root: Path, archive: Path | None = None) -> None:
    root = root.absolute()
    for name in ("manifest.sha256", "sha256sums"):
        regular_control(root / name)
    payload = dict(read_manifest(root, root / "manifest.sha256"))
    sums = dict(read_manifest(root, root / "sha256sums"))
    if not payload or sums != {**payload, "manifest.sha256": sha(root / "manifest.sha256")}:
        raise ValueError("Two-tier manifest disagreement or empty payload")
    actual = {p.relative_to(root).as_posix() for p in walk_files(root, {"__pycache__"}, set(), {".pyc"})}
    if actual != set(sums) | {"sha256sums"}:
        raise ValueError(f"Manifest/tree disagreement: {sorted(actual ^ (set(sums) | {'sha256sums'}))}")
    required = {"mub6.md", "mub6.tex", "mub6.pdf", "render_binding.json", "README.md",
                "LICENSE", "LICENSE-CODE", "zenodo_metadata.json", "release_identity.json",
                "docs/descriptions.md", "docs/references.md", "docs/keywords.md", "docs/quick_start.md",
                "scripts/verify_publication.py", "scripts/build_pdf.py", "scripts/paper_code_wrap.lua",
                "code/deposit_paths.py"}
    if not required <= set(payload):
        raise ValueError(f"Missing required publication files: {sorted(required - set(payload))}")
    for relative, expected in sums.items():
        path = safe_path(root, relative)
        if sha(path) != expected:
            raise ValueError(f"Hash mismatch: {relative}")
    for name in ("descriptions", "references", "keywords", "quick_start"):
        if (root / "docs" / f"{name}.md").stat().st_size < 100:
            raise ValueError(f"Stub documentation: {name}")
    meta = json.loads((root / "zenodo_metadata.json").read_text(encoding="utf-8"))
    identity = json.loads((root / "release_identity.json").read_text(encoding="utf-8"))
    header = (root / "mub6.md").read_text(encoding="utf-8").split("\n\n", 1)[0]
    rows = re.findall(r'^<div align="center">(.+)</div>$', header, re.M)
    if rows != ["# " + meta["title"], "Jeremy H. Carroll", meta["publication_date"], "Version " + meta["version"]]:
        raise ValueError("Manuscript/metadata header disagreement")
    if any(identity[k] != meta[k] for k in ("title", "version", "publication_date")):
        raise ValueError("Release identity disagreement")
    if meta["upload_type"] != "publication" or meta["publication_type"] != "preprint":
        raise ValueError("Expected preprint metadata")
    if meta["creators"] != [{"name": "Carroll, Jeremy H."}] or meta["license"] != "cc-by-4.0":
        raise ValueError("Creator/license disagreement")
    if identity.get("publication_ready") is not False or identity.get("external_deposit_performed") is not False:
        raise ValueError("Candidate cannot assert publication approval or an external deposit")
    for item in meta.get("related_identifiers", []):
        if not all(item.get(k) for k in ("identifier", "relation", "resource_type", "scheme")):
            raise ValueError("Incomplete related identifier")
    if identity.get("concept_doi") and not any(
        i["relation"] == "isVersionOf" and i["identifier"] == identity["concept_doi"]
        for i in meta.get("related_identifiers", [])
    ):
        raise ValueError("Missing concept DOI lineage")
    binding = json.loads((root / "render_binding.json").read_text(encoding="utf-8"))
    expected_bound = {"mub6.md", "mub6.tex", "mub6.pdf", "scripts/build_pdf.py", "scripts/paper_code_wrap.lua"}
    if set(binding["sha256"]) != expected_bound:
        raise ValueError("Incomplete render binding")
    for name, expected in binding["sha256"].items():
        if sha(safe_path(root, name)) != expected:
            raise ValueError(f"Stale render binding: {name}")
    if binding["missing_glyphs"] or binding["overfull_hbox_gt_10pt"] or binding["pages"] < 1:
        raise ValueError("Unclean PDF render")
    if f"% manuscript-sha256: {sha(root / 'mub6.md')}\n" not in (root / "mub6.tex").read_text(encoding="utf-8"):
        raise ValueError("TeX/source disagreement")
    if archive is not None:
        sidecar = archive.with_suffix(archive.suffix + ".sha256")
        regular_control(archive)
        regular_control(sidecar)
        if sidecar.read_text(encoding="utf-8") != f"{sha(archive)}  {archive.name}\n":
            raise ValueError("Archive sidecar disagreement")
        with zipfile.ZipFile(archive) as z:
            members = z.infolist()
            names = [m.filename for m in members]
            if len(names) != len(set(names)) or set(names) != actual:
                raise ValueError("Archive member set disagreement")
            for member in members:
                path = safe_path(root, member.filename)
                if member.is_dir() or member.external_attr >> 16 != 0o100644:
                    raise ValueError("Nonregular archive member")
                if hashlib.sha256(z.read(member)).hexdigest() != sha(path):
                    raise ValueError(f"Archive member mismatch: {member.filename}")
        if archive.read_bytes() != canonical_archive(root, actual, meta["publication_date"]):
            raise ValueError("Noncanonical complete archive bytes")
        if dict(read_manifest(root, root / "sha256sums")) != sums or any(
            sha(safe_path(root, name)) != expected for name, expected in sums.items()
        ):
            raise ValueError("Payload changed during archive verification")
        print(f"PASS: {len(names)} archive members and sidecar match the sealed preprint")
    else:
        print("PASS: sealed preprint tree; archive verification NOT performed")
    print("Scope: byte custody, metadata and render bindings only; formal replay NOT performed; author review outstanding.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--archive", type=Path)
    args = parser.parse_args()
    try:
        verify(args.root, args.archive)
    except (OSError, ValueError, KeyError, TypeError, zipfile.BadZipFile) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
