"""Fail-closed helpers for a deterministic paper release envelope.

This module deliberately verifies only byte integrity and archive structure.  It
does not turn those checks into a mathematical, publication, or authority
claim.
"""

from __future__ import annotations

import hashlib
import io
import os
import re
import stat
import zipfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Iterable


CONTROL_NAMES = ("SHA256SUMS", "MANIFEST.sha256")
TRANSIENT_DIR_NAMES = frozenset(
    {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".ipynb_checkpoints"}
)
_DIGEST_RE = re.compile(r"[0-9a-fA-F]{64}")
_REPARSE_POINT = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)


class ReleaseContractError(ValueError):
    """Raised when release bytes violate the fail-closed envelope contract."""


@dataclass(frozen=True)
class ManifestEntry:
    path: str
    digest: str


def _lexists(path: Path) -> bool:
    try:
        path.lstat()
    except FileNotFoundError:
        return False
    return True


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _assert_root_directory(root: Path) -> None:
    try:
        metadata = root.lstat()
    except FileNotFoundError as error:
        raise ReleaseContractError(f"package root is missing: {root}") from error
    if stat.S_ISLNK(metadata.st_mode) or bool(
        getattr(metadata, "st_file_attributes", 0) & _REPARSE_POINT
    ):
        raise ReleaseContractError(f"package root is a symlink or reparse point: {root}")
    if not stat.S_ISDIR(metadata.st_mode):
        raise ReleaseContractError(f"package root is not a directory: {root}")


def _validate_relative_path(relative: str, *, source: str, lineno: int) -> PurePosixPath:
    pure = PurePosixPath(relative)
    unsafe = (
        not relative
        or not pure.parts
        or pure.is_absolute()
        or pure.as_posix() != relative
        or any(part in {"", ".", ".."} for part in pure.parts)
        or "\\" in relative
        or ":" in relative
        or any(ord(character) < 32 for character in relative)
    )
    if unsafe:
        raise ReleaseContractError(
            f"{source} line {lineno} has unsafe path {relative!r}"
        )
    return pure


def _assert_regular_file(path: Path, root: Path, *, label: str) -> None:
    _assert_root_directory(root)
    try:
        relative = path.relative_to(root)
    except ValueError as error:
        raise ReleaseContractError(f"{label} escapes package root: {path}") from error

    current = root
    for index, part in enumerate(relative.parts):
        current = current / part
        try:
            metadata = current.lstat()
        except FileNotFoundError as error:
            raise ReleaseContractError(f"missing {label}: {relative.as_posix()}") from error
        if stat.S_ISLNK(metadata.st_mode) or bool(
            getattr(metadata, "st_file_attributes", 0) & _REPARSE_POINT
        ):
            raise ReleaseContractError(
                f"unauthorized symlink or reparse point in {label}: "
                f"{current.relative_to(root).as_posix()}"
            )
        is_last = index == len(relative.parts) - 1
        if is_last and not stat.S_ISREG(metadata.st_mode):
            raise ReleaseContractError(f"non-regular {label}: {relative.as_posix()}")
        if not is_last and not stat.S_ISDIR(metadata.st_mode):
            raise ReleaseContractError(
                f"non-directory parent in {label}: {current.relative_to(root).as_posix()}"
            )


def parse_manifest_bytes(
    data: bytes,
    root: Path,
    *,
    source: str = "SHA256SUMS",
    reserved_names: Iterable[str] = CONTROL_NAMES,
) -> list[ManifestEntry]:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ReleaseContractError(f"{source} is not UTF-8") from error

    reserved = {name.casefold() for name in reserved_names}
    entries: list[ManifestEntry] = []
    seen: set[str] = set()
    for lineno, raw_line in enumerate(text.splitlines(), start=1):
        if not raw_line:
            continue
        parts = raw_line.split(None, 1)
        if len(parts) != 2 or _DIGEST_RE.fullmatch(parts[0]) is None:
            raise ReleaseContractError(
                f"{source} line {lineno} is malformed: {raw_line!r}"
            )
        relative = parts[1].lstrip("*")
        pure = _validate_relative_path(relative, source=source, lineno=lineno)
        key = pure.as_posix().casefold()
        if key in reserved:
            raise ReleaseContractError(
                f"{source} line {lineno} lists reserved control file {relative!r}"
            )
        if key in seen:
            raise ReleaseContractError(
                f"{source} line {lineno} duplicates a path case-insensitively: {relative!r}"
            )
        seen.add(key)
        entries.append(ManifestEntry(pure.as_posix(), parts[0].lower()))

    if not entries:
        raise ReleaseContractError(f"{source} has no payload entries")
    return entries


def enumerate_payload(
    root: Path,
    *,
    excluded_dirs: set[str],
    excluded_names: set[str],
    excluded_suffixes: set[str],
    archive_name: str,
) -> list[Path]:
    _assert_root_directory(root)

    payload: list[Path] = []
    control_keys = {name.casefold(): name for name in CONTROL_NAMES}
    archive_key = archive_name.casefold()
    def raise_walk_error(error: OSError) -> None:
        raise ReleaseContractError(f"cannot traverse release tree: {error}") from error

    for dirpath, dirnames, filenames in os.walk(
        root,
        topdown=True,
        followlinks=False,
        onerror=raise_walk_error,
    ):
        directory = Path(dirpath)
        retained_dirs: list[str] = []
        for name in sorted(dirnames):
            candidate = directory / name
            metadata = candidate.lstat()
            relative = candidate.relative_to(root).as_posix()
            if stat.S_ISLNK(metadata.st_mode) or bool(
                getattr(metadata, "st_file_attributes", 0) & _REPARSE_POINT
            ):
                raise ReleaseContractError(
                    f"unauthorized directory symlink or reparse point: {relative}"
                )
            if not stat.S_ISDIR(metadata.st_mode):
                raise ReleaseContractError(f"non-directory tree entry: {relative}")
            if relative in excluded_dirs or name in TRANSIENT_DIR_NAMES:
                continue
            if name.startswith("."):
                raise ReleaseContractError(f"unexpected hidden directory: {relative}")
            retained_dirs.append(name)
        dirnames[:] = retained_dirs

        for name in sorted(filenames):
            candidate = directory / name
            metadata = candidate.lstat()
            relative = candidate.relative_to(root).as_posix()
            if stat.S_ISLNK(metadata.st_mode) or bool(
                getattr(metadata, "st_file_attributes", 0) & _REPARSE_POINT
            ):
                raise ReleaseContractError(
                    f"unauthorized file symlink or reparse point: {relative}"
                )
            if not stat.S_ISREG(metadata.st_mode):
                raise ReleaseContractError(f"non-regular tree entry: {relative}")
            folded_relative = relative.casefold()
            if folded_relative in control_keys:
                canonical = control_keys[folded_relative]
                if relative != canonical:
                    raise ReleaseContractError(
                        f"case-variant release control file: {relative!r}; expected {canonical!r}"
                    )
                continue
            if folded_relative == archive_key:
                if relative != archive_name:
                    raise ReleaseContractError(
                        f"case-variant release archive: {relative!r}; expected {archive_name!r}"
                    )
                continue
            if name in excluded_names or candidate.suffix in excluded_suffixes:
                continue
            if candidate.suffix.casefold() == ".zip":
                raise ReleaseContractError(f"unexpected release archive: {relative}")
            payload.append(candidate)

    payload.sort(key=lambda path: path.relative_to(root).as_posix())
    return payload


def render_manifest(root: Path, payload: Iterable[Path]) -> bytes:
    lines = [
        f"{sha256_of(path)}  {path.relative_to(root).as_posix()}"
        for path in payload
    ]
    return ("\n".join(lines) + "\n").encode("utf-8")


def verify_tree_and_manifests(
    root: Path,
    *,
    excluded_dirs: set[str],
    excluded_names: set[str],
    excluded_suffixes: set[str],
    archive_name: str,
) -> list[ManifestEntry]:
    primary_path = root / CONTROL_NAMES[0]
    alternate_path = root / CONTROL_NAMES[1]
    _assert_regular_file(primary_path, root, label=CONTROL_NAMES[0])
    _assert_regular_file(alternate_path, root, label=CONTROL_NAMES[1])
    primary = primary_path.read_bytes()
    alternate = alternate_path.read_bytes()
    if primary != alternate:
        raise ReleaseContractError("SHA256SUMS and MANIFEST.sha256 differ byte-for-byte")

    entries = parse_manifest_bytes(primary, root, reserved_names=(*CONTROL_NAMES, archive_name))
    payload = enumerate_payload(
        root,
        excluded_dirs=excluded_dirs,
        excluded_names=excluded_names,
        excluded_suffixes=excluded_suffixes,
        archive_name=archive_name,
    )
    fresh = render_manifest(root, payload)
    if primary != fresh:
        recorded = {entry.path: entry.digest for entry in entries}
        actual = {
            path.relative_to(root).as_posix(): sha256_of(path)
            for path in payload
        }
        missing = sorted(set(recorded) - set(actual))
        extra = sorted(set(actual) - set(recorded))
        changed = sorted(
            path for path in set(recorded) & set(actual) if recorded[path] != actual[path]
        )
        details: list[str] = []
        details.extend(f"missing: {path}" for path in missing)
        details.extend(f"unmanifested: {path}" for path in extra)
        details.extend(f"hash mismatch: {path}" for path in changed)
        if not details:
            details.append("manifest serialization is not canonical UTF-8/LF sorted form")
        raise ReleaseContractError("manifest/tree mismatch: " + "; ".join(details))

    for entry in entries:
        candidate = root.joinpath(*PurePosixPath(entry.path).parts)
        _assert_regular_file(candidate, root, label=f"manifest payload {entry.path}")
        if sha256_of(candidate) != entry.digest:
            raise ReleaseContractError(f"hash mismatch: {entry.path}")
    return entries


def _archive_name(prefix: str, relative: str) -> str:
    if not prefix:
        return relative
    return f"{prefix.rstrip('/')}/{relative}"


def _validate_archive_member(name: str, index: int) -> None:
    pure = _validate_relative_path(name, source="ZIP", lineno=index)
    if pure.as_posix().endswith("/"):
        raise ReleaseContractError(f"ZIP member {index} is a directory entry: {name!r}")


def expected_archive_names(entries: Iterable[ManifestEntry], prefix: str) -> list[str]:
    return [
        *(_archive_name(prefix, name) for name in CONTROL_NAMES),
        *(_archive_name(prefix, entry.path) for entry in entries),
    ]


def _render_archive_bytes(
    members: list[tuple[str, bytes]],
    *,
    zip_date: tuple[int, int, int, int, int, int],
) -> bytes:
    output = io.BytesIO()
    seen: set[str] = set()
    with zipfile.ZipFile(
        output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
    ) as archive:
        for name, data in members:
            key = name.casefold()
            if key in seen:
                raise ReleaseContractError(f"duplicate archive member: {name}")
            seen.add(key)
            info = zipfile.ZipInfo(filename=name, date_time=zip_date)
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, data)
    return output.getvalue()


def verify_archive(
    archive_path: Path,
    root: Path,
    entries: list[ManifestEntry],
    *,
    prefix: str,
    zip_date: tuple[int, int, int, int, int, int],
) -> None:
    _assert_regular_file(archive_path, root, label="release archive")
    expected = expected_archive_names(entries, prefix)
    expected_casefold = [name.casefold() for name in expected]
    try:
        expected_manifest = (
            "".join(f"{entry.digest}  {entry.path}\n" for entry in entries)
        ).encode("utf-8")
        control_bytes: dict[str, bytes] = {}
        for name in CONTROL_NAMES:
            source = root / name
            _assert_regular_file(source, root, label=f"archive control source {name}")
            data = source.read_bytes()
            if data != expected_manifest:
                raise ReleaseContractError(f"{name} changed after manifest verification")
            control_bytes[name] = data

        payload_by_name = {entry.path: entry.digest for entry in entries}
        payload_sources = {
            entry.path: root.joinpath(*PurePosixPath(entry.path).parts)
            for entry in entries
        }
        payload_bytes: dict[str, bytes] = {}
        for relative, source in payload_sources.items():
            _assert_regular_file(source, root, label=f"archive comparison source {relative}")
            data = source.read_bytes()
            if hashlib.sha256(data).hexdigest() != payload_by_name[relative]:
                raise ReleaseContractError(
                    f"tree payload changed after manifest verification: {relative}"
                )
            payload_bytes[relative] = data

        canonical_members = [
            *(
                (_archive_name(prefix, name), control_bytes[name])
                for name in CONTROL_NAMES
            ),
            *(
                (_archive_name(prefix, entry.path), payload_bytes[entry.path])
                for entry in entries
            ),
        ]
        canonical_archive = _render_archive_bytes(canonical_members, zip_date=zip_date)
        with zipfile.ZipFile(archive_path, "r") as archive:
            if archive.comment:
                raise ReleaseContractError("ZIP has a noncanonical archive comment")
            infos = archive.infolist()
            names = [info.filename for info in infos]
            for index, name in enumerate(names, start=1):
                _validate_archive_member(name, index)
            folded = [name.casefold() for name in names]
            if len(folded) != len(set(folded)):
                raise ReleaseContractError("ZIP contains duplicate case-insensitive member names")
            if folded != expected_casefold or names != expected:
                raise ReleaseContractError(
                    f"ZIP member inventory/order mismatch: expected {expected!r}, got {names!r}"
                )
            expected_sizes = {
                **{name: len(data) for name, data in control_bytes.items()},
                **{relative: len(data) for relative, data in payload_bytes.items()},
            }
            for info in infos:
                if info.create_system != 3:
                    raise ReleaseContractError(
                        f"ZIP member {info.filename!r} has create_system={info.create_system}, expected 3"
                    )
                if info.date_time != zip_date:
                    raise ReleaseContractError(
                        f"ZIP member {info.filename!r} has noncanonical timestamp"
                    )
                if info.compress_type != zipfile.ZIP_DEFLATED:
                    raise ReleaseContractError(f"ZIP member {info.filename!r} is not deflated")
                if info.external_attr >> 16 != 0o100644:
                    raise ReleaseContractError(f"ZIP member {info.filename!r} has noncanonical mode")
                if info.extra or info.comment:
                    raise ReleaseContractError(
                        f"ZIP member {info.filename!r} has noncanonical extra/comment metadata"
                    )
                if info.flag_bits & 0x1:
                    raise ReleaseContractError(f"ZIP member {info.filename!r} is encrypted")
                relative = (
                    info.filename[len(prefix.rstrip("/") + "/") :]
                    if prefix
                    else info.filename
                )
                if info.file_size != expected_sizes[relative]:
                    raise ReleaseContractError(
                        f"ZIP member {info.filename!r} has unexpected uncompressed size"
                    )
                data = archive.read(info)
                if relative in CONTROL_NAMES:
                    if data != control_bytes[relative]:
                        raise ReleaseContractError(f"ZIP embeds stale {relative}")
                else:
                    digest = hashlib.sha256(data).hexdigest()
                    if digest != payload_by_name.get(relative):
                        raise ReleaseContractError(f"ZIP payload digest mismatch: {relative}")
                    if data != payload_bytes[relative]:
                        raise ReleaseContractError(f"ZIP/tree byte mismatch: {relative}")
        _assert_regular_file(archive_path, root, label="release archive")
        if archive_path.read_bytes() != canonical_archive:
            raise ReleaseContractError(
                "release ZIP bytes differ from the deterministic canonical rebuild"
            )
    except ReleaseContractError:
        raise
    except (EOFError, NotImplementedError, RuntimeError, zipfile.BadZipFile) as error:
        raise ReleaseContractError(f"invalid or unreadable release ZIP: {error}") from error


def build_archive(
    destination: Path,
    root: Path,
    entries: list[ManifestEntry],
    *,
    prefix: str,
    zip_date: tuple[int, int, int, int, int, int],
) -> None:
    _assert_root_directory(root)
    if destination.parent != root:
        raise ReleaseContractError("release archive destination must be the package root")
    if _lexists(destination):
        _assert_regular_file(destination, root, label="existing release archive")
    temporary = destination.with_name(destination.name + ".tmp")
    if _lexists(temporary):
        _assert_regular_file(temporary, root, label="temporary archive")
        temporary.unlink()

    names = expected_archive_names(entries, prefix)
    sources = [
        *(root / name for name in CONTROL_NAMES),
        *(root.joinpath(*PurePosixPath(entry.path).parts) for entry in entries),
    ]
    try:
        members: list[tuple[str, bytes]] = []
        for name, source in zip(names, sources, strict=True):
            _assert_regular_file(source, root, label=f"archive source {name}")
            members.append((name, source.read_bytes()))
        temporary.write_bytes(_render_archive_bytes(members, zip_date=zip_date))
        verify_archive(
            temporary,
            root,
            entries,
            prefix=prefix,
            zip_date=zip_date,
        )
        os.replace(temporary, destination)
    finally:
        if temporary.exists():
            temporary.unlink()
