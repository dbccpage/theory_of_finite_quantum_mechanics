"""Read-only preprint custody checks; no mathematical or publication approval."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import stat
import struct
import sys
import zipfile
import zlib
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


def verify_archive_envelope(raw: bytes, members: list[zipfile.ZipInfo], publication_date: str) -> None:
    """Check the complete ZIP32 envelope without assuming a zlib encoder version.

    DEFLATE has multiple valid encodings. The sidecar binds the actual archive;
    member SHA-256 checks bind its decoded bytes. This checks the publication's
    fixed metadata and contiguous layout, including local/central agreement.
    """
    def require(condition: bool) -> None:
        if not condition:
            raise ValueError("Noncanonical complete archive bytes")

    require(len(raw) >= 22)
    end = struct.unpack("<4s4H2LH", raw[-22:])
    signature, disk, directory_disk, on_disk, total, directory_size, directory_at, comment = end
    require(signature == b"PK\x05\x06" and disk == directory_disk == comment == 0)
    require(on_disk == total == len(members) and directory_at + directory_size == len(raw) - 22)
    stamp = (*map(int, publication_date.split("-")), 12, 0, 0)
    year, month, day, hour, minute, second = stamp
    dos_time = (hour << 11) | (minute << 5) | (second // 2)
    dos_date = ((year - 1980) << 9) | (month << 5) | day
    require([m.filename for m in members] == sorted(m.filename for m in members))
    local_at, central_at = 0, directory_at
    for member in members:
        name = member.filename.encode("utf-8")
        flags = 0 if name.isascii() else 0x800
        require(member.date_time == stamp and member.header_offset == local_at)
        require(member.create_system == 3 and member.create_version == member.extract_version == 20)
        require(member.flag_bits == flags and member.compress_type == zipfile.ZIP_DEFLATED)
        require(member.external_attr == 0o100644 << 16 and member.internal_attr == 0)
        require(member.extra == member.comment == b"" and member.volume == 0)
        local = struct.pack("<4s5H3L2H", b"PK\x03\x04", 20, flags, 8, dos_time, dos_date,
                            member.CRC, member.compress_size, member.file_size, len(name), 0) + name
        require(raw[local_at:local_at + len(local)] == local)
        data_at = local_at + len(local)
        local_at = data_at + member.compress_size
        require(local_at <= directory_at)
        decoder = zlib.decompressobj(-15)
        decoded = decoder.decompress(raw[data_at:local_at], member.file_size + 1)
        require(len(decoded) == member.file_size and decoder.eof
                and not decoder.unused_data and not decoder.unconsumed_tail)
        central = struct.pack("<4s6H3L5H2L", b"PK\x01\x02", (3 << 8) | 20, 20, flags, 8,
                              dos_time, dos_date, member.CRC, member.compress_size,
                              member.file_size, len(name), 0, 0, 0, 0,
                              0o100644 << 16, member.header_offset) + name
        require(raw[central_at:central_at + len(central)] == central)
        central_at += len(central)
    require(local_at == directory_at and central_at == len(raw) - 22)


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
        verify_archive_envelope(archive.read_bytes(), members, meta["publication_date"])
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
    except (OSError, ValueError, KeyError, TypeError, zipfile.BadZipFile, zlib.error) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
