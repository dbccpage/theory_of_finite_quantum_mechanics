"""Mutation tests for the fail-closed release-envelope tools."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
import zipfile
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

PAPER_ROOT = Path(__file__).resolve().parents[2]
CONTRACT_PATH = PAPER_ROOT / "scripts" / "release_contract.py"
ARCHIVE_NAME = "coordinate_wise_additivity_2026-10-02.zip"
ZIP_DATE = (2026, 10, 2, 12, 0, 0)
PREFIX = "coordinate_wise_additivity"
EXCLUDED_DIRS = {".git", ".lake", "__pycache__"}
EXCLUDED_NAMES = {".coverage"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}


def _load_contract() -> ModuleType:
    module_name = "paper009_release_contract_under_test"
    spec = importlib.util.spec_from_file_location(module_name, CONTRACT_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


contract = _load_contract()


def _enumerate(root: Path) -> list[Path]:
    return contract.enumerate_payload(
        root,
        excluded_dirs=EXCLUDED_DIRS,
        excluded_names=EXCLUDED_NAMES,
        excluded_suffixes=EXCLUDED_SUFFIXES,
        archive_name=ARCHIVE_NAME,
    )


def _verify(root: Path) -> list[Any]:
    return contract.verify_tree_and_manifests(
        root,
        excluded_dirs=EXCLUDED_DIRS,
        excluded_names=EXCLUDED_NAMES,
        excluded_suffixes=EXCLUDED_SUFFIXES,
        archive_name=ARCHIVE_NAME,
    )


@pytest.fixture
def release_tree(tmp_path: Path) -> tuple[Path, list[Any]]:
    root = tmp_path / "paper"
    (root / "nested").mkdir(parents=True)
    (root / ".lake" / "build").mkdir(parents=True)
    (root / "alpha.txt").write_bytes(b"alpha\n")
    (root / "nested" / "beta.bin").write_bytes(b"beta\x00")
    (root / ".lake" / "build" / "ignored.bin").write_bytes(b"ignored")
    manifest = contract.render_manifest(root, _enumerate(root))
    (root / "SHA256SUMS").write_bytes(manifest)
    (root / "MANIFEST.sha256").write_bytes(manifest)
    return root, _verify(root)


def _write_member(
    archive: zipfile.ZipFile,
    name: str,
    data: bytes,
    *,
    create_system: int = 3,
    date_time: tuple[int, int, int, int, int, int] = ZIP_DATE,
    mode: int = 0o100644,
    extra: bytes = b"",
    comment: bytes = b"",
) -> None:
    info = zipfile.ZipInfo(name, date_time=date_time)
    info.create_system = create_system
    info.external_attr = mode << 16
    info.compress_type = zipfile.ZIP_DEFLATED
    info.extra = extra
    info.comment = comment
    archive.writestr(info, data)


def _write_expected_members(
    archive: zipfile.ZipFile,
    root: Path,
    entries: list[Any],
) -> None:
    for name in contract.expected_archive_names(entries, PREFIX):
        _write_member(archive, name, _member_bytes(root, name))


def _member_bytes(root: Path, archive_name: str) -> bytes:
    prefix = f"{PREFIX}/"
    assert archive_name.startswith(prefix)
    return (root / archive_name.removeprefix(prefix)).read_bytes()


def test_verify_deposit_imports_release_tools_as_package() -> None:
    result = subprocess.run(
        [sys.executable, "-c", "import verify_deposit"],
        cwd=PAPER_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize(
    ("script", "argument"),
    [
        ("scripts/regen_sha256sums.py", "--invalid"),
        ("scripts/build_deposit_zip.py", "--invalid"),
        ("verify_deposit.py", "--invalid"),
    ],
)
def test_release_cli_rejects_unknown_modes(script: str, argument: str) -> None:
    result = subprocess.run(
        [sys.executable, script, argument],
        cwd=PAPER_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2, result.stdout + result.stderr


def test_tree_manifest_bijection_rejects_extra_file(
    release_tree: tuple[Path, list[Any]],
) -> None:
    root, _ = release_tree
    (root / "UNMANIFESTED_EXTRA.md").write_text("extra", encoding="utf-8")
    with pytest.raises(contract.ReleaseContractError, match="unmanifested"):
        _verify(root)


def test_tree_manifest_bijection_rejects_nested_extra_file(
    release_tree: tuple[Path, list[Any]],
) -> None:
    root, _ = release_tree
    (root / "nested" / "UNMANIFESTED_EXTRA.md").write_text("extra", encoding="utf-8")
    with pytest.raises(contract.ReleaseContractError, match="unmanifested"):
        _verify(root)


def test_tree_manifest_bijection_rejects_missing_file(
    release_tree: tuple[Path, list[Any]],
) -> None:
    root, _ = release_tree
    (root / "nested" / "beta.bin").unlink()
    with pytest.raises(contract.ReleaseContractError, match="missing"):
        _verify(root)


def test_tree_manifest_bijection_rejects_changed_file(
    release_tree: tuple[Path, list[Any]],
) -> None:
    root, _ = release_tree
    (root / "alpha.txt").write_bytes(b"changed\n")
    with pytest.raises(contract.ReleaseContractError, match="hash mismatch"):
        _verify(root)


def test_tree_manifest_requires_both_identical_controls(
    release_tree: tuple[Path, list[Any]],
) -> None:
    root, _ = release_tree
    (root / "MANIFEST.sha256").write_bytes(b"different\n")
    with pytest.raises(contract.ReleaseContractError, match="differ byte-for-byte"):
        _verify(root)


@pytest.mark.parametrize("control", contract.CONTROL_NAMES)
def test_tree_manifest_rejects_missing_control(
    release_tree: tuple[Path, list[Any]], control: str
) -> None:
    root, _ = release_tree
    (root / control).unlink()
    with pytest.raises(contract.ReleaseContractError, match="missing"):
        _verify(root)


def test_manifest_rejects_malformed_digest(tmp_path: Path) -> None:
    with pytest.raises(contract.ReleaseContractError, match="malformed"):
        contract.parse_manifest_bytes(b"not-a-digest  alpha.txt\n", tmp_path)


@pytest.mark.parametrize(
    "relative",
    ["../escape.txt", "/absolute.txt", "nested\\windows.txt", "C:/drive.txt", "a/./b"],
)
def test_manifest_rejects_unsafe_paths(tmp_path: Path, relative: str) -> None:
    data = f"{'0' * 64}  {relative}\n".encode()
    with pytest.raises(contract.ReleaseContractError, match="unsafe path"):
        contract.parse_manifest_bytes(data, tmp_path)


def test_manifest_rejects_case_insensitive_duplicate(tmp_path: Path) -> None:
    digest = "0" * 64
    data = f"{digest}  Alpha.txt\n{digest}  alpha.txt\n".encode()
    with pytest.raises(contract.ReleaseContractError, match="case-insensitively"):
        contract.parse_manifest_bytes(data, tmp_path)


def test_manifest_rejects_reserved_control_file(tmp_path: Path) -> None:
    data = f"{'0' * 64}  sha256sums\n".encode()
    with pytest.raises(contract.ReleaseContractError, match="reserved control"):
        contract.parse_manifest_bytes(data, tmp_path)


def test_excluded_directory_is_pruned_before_descent(
    release_tree: tuple[Path, list[Any]], monkeypatch: pytest.MonkeyPatch
) -> None:
    root, _ = release_tree
    visited: list[str] = []
    original_walk = contract.os.walk

    def recording_walk(*args: Any, **kwargs: Any) -> Any:
        for dirpath, dirnames, filenames in original_walk(*args, **kwargs):
            visited.append(Path(dirpath).relative_to(root).as_posix())
            yield dirpath, dirnames, filenames

    monkeypatch.setattr(contract.os, "walk", recording_walk)
    payload = _enumerate(root)
    assert ".lake" not in visited
    assert all(".lake" not in path.relative_to(root).parts for path in payload)


def test_excluded_directory_paths_do_not_hide_same_basename_nested_payload(
    tmp_path: Path,
) -> None:
    root = tmp_path / "paper"
    (root / "build").mkdir(parents=True)
    (root / "nested" / "build").mkdir(parents=True)
    (root / "build" / "ignored.txt").write_text("ignored", encoding="utf-8")
    nested = root / "nested" / "build" / "payload.txt"
    nested.write_text("payload", encoding="utf-8")
    payload = contract.enumerate_payload(
        root,
        excluded_dirs={"build"},
        excluded_names=set(),
        excluded_suffixes=set(),
        archive_name=ARCHIVE_NAME,
    )
    assert payload == [nested]


def test_walk_error_is_fatal(
    release_tree: tuple[Path, list[Any]], monkeypatch: pytest.MonkeyPatch
) -> None:
    root, _ = release_tree

    def denied_walk(*args: Any, onerror: Any = None, **kwargs: Any) -> Any:
        assert onerror is not None
        onerror(PermissionError("denied"))
        return iter(())

    monkeypatch.setattr(contract.os, "walk", denied_walk)
    with pytest.raises(contract.ReleaseContractError, match="cannot traverse"):
        _enumerate(root)


def test_nested_symlink_is_rejected_or_platform_skip(
    release_tree: tuple[Path, list[Any]],
) -> None:
    root, _ = release_tree
    link = root / "nested" / "alpha-link.txt"
    try:
        link.symlink_to(root / "alpha.txt")
    except (NotImplementedError, OSError) as error:
        pytest.skip(f"host does not permit symlink creation: {error}")
    with pytest.raises(contract.ReleaseContractError, match="symlink or reparse point"):
        _enumerate(root)


def test_nested_directory_symlink_is_rejected_or_platform_skip(
    release_tree: tuple[Path, list[Any]], tmp_path: Path
) -> None:
    root, _ = release_tree
    target = tmp_path / "outside"
    target.mkdir()
    link = root / "linked-directory"
    try:
        link.symlink_to(target, target_is_directory=True)
    except (NotImplementedError, OSError) as error:
        pytest.skip(f"host does not permit directory symlink creation: {error}")
    with pytest.raises(contract.ReleaseContractError, match="symlink or reparse point"):
        _enumerate(root)


def test_archive_build_is_deterministic_portable_and_exact(
    release_tree: tuple[Path, list[Any]],
) -> None:
    root, entries = release_tree
    archive_path = root / ARCHIVE_NAME
    contract.build_archive(archive_path, root, entries, prefix=PREFIX, zip_date=ZIP_DATE)
    first = archive_path.read_bytes()
    contract.verify_archive(archive_path, root, entries, prefix=PREFIX, zip_date=ZIP_DATE)
    contract.build_archive(archive_path, root, entries, prefix=PREFIX, zip_date=ZIP_DATE)
    assert archive_path.read_bytes() == first

    with zipfile.ZipFile(archive_path) as archive:
        infos = archive.infolist()
    assert [info.filename for info in infos] == contract.expected_archive_names(entries, PREFIX)
    assert len(infos) == len({info.filename.casefold() for info in infos})
    assert all(info.create_system == 3 for info in infos)
    assert all(info.external_attr >> 16 == 0o100644 for info in infos)
    assert all(info.date_time == ZIP_DATE for info in infos)
    assert all(info.compress_type == zipfile.ZIP_DEFLATED for info in infos)


@pytest.mark.parametrize("wrapper", ["prefix", "trailer"])
def test_archive_rejects_unbound_outer_bytes(
    release_tree: tuple[Path, list[Any]], wrapper: str
) -> None:
    root, entries = release_tree
    archive_path = root / ARCHIVE_NAME
    contract.build_archive(
        archive_path, root, entries, prefix=PREFIX, zip_date=ZIP_DATE
    )
    original = archive_path.read_bytes()
    mutated = b"UNBOUND" + original if wrapper == "prefix" else original + b"UNBOUND"
    archive_path.write_bytes(mutated)
    with pytest.raises(contract.ReleaseContractError, match="canonical rebuild"):
        contract.verify_archive(
            archive_path, root, entries, prefix=PREFIX, zip_date=ZIP_DATE
        )


def test_archive_rejects_control_symlink_after_initial_verification(
    release_tree: tuple[Path, list[Any]], tmp_path: Path
) -> None:
    root, entries = release_tree
    archive_path = root / ARCHIVE_NAME
    contract.build_archive(
        archive_path, root, entries, prefix=PREFIX, zip_date=ZIP_DATE
    )
    control = root / "SHA256SUMS"
    external = tmp_path / "same-bytes-manifest"
    external.write_bytes(control.read_bytes())
    control.unlink()
    try:
        control.symlink_to(external)
    except (NotImplementedError, OSError) as error:
        pytest.skip(f"host does not permit symlink creation: {error}")
    with pytest.raises(contract.ReleaseContractError, match="symlink or reparse point"):
        contract.verify_archive(
            archive_path, root, entries, prefix=PREFIX, zip_date=ZIP_DATE
        )


def test_archive_build_rejects_dangling_temporary_symlink_or_platform_skip(
    release_tree: tuple[Path, list[Any]], tmp_path: Path
) -> None:
    root, entries = release_tree
    temporary = root / f"{ARCHIVE_NAME}.tmp"
    try:
        temporary.symlink_to(tmp_path / "missing-outside-target")
    except (NotImplementedError, OSError) as error:
        pytest.skip(f"host does not permit symlink creation: {error}")
    with pytest.raises(contract.ReleaseContractError, match="symlink or reparse point"):
        contract.build_archive(
            root / ARCHIVE_NAME,
            root,
            entries,
            prefix=PREFIX,
            zip_date=ZIP_DATE,
        )


def test_archive_verifier_rejects_duplicate_member(
    release_tree: tuple[Path, list[Any]],
) -> None:
    root, entries = release_tree
    archive_path = root / ARCHIVE_NAME
    with zipfile.ZipFile(archive_path, "w") as archive:
        _write_expected_members(archive, root, entries)
        with pytest.warns(UserWarning, match="Duplicate name"):
            _write_member(
                archive,
                f"{PREFIX}/SHA256SUMS",
                (root / "SHA256SUMS").read_bytes(),
            )
    with pytest.raises(contract.ReleaseContractError, match="duplicate"):
        contract.verify_archive(archive_path, root, entries, prefix=PREFIX, zip_date=ZIP_DATE)


def test_archive_verifier_rejects_traversal_member(
    release_tree: tuple[Path, list[Any]],
) -> None:
    root, entries = release_tree
    archive_path = root / ARCHIVE_NAME
    with zipfile.ZipFile(archive_path, "w") as archive:
        _write_expected_members(archive, root, entries)
        _write_member(archive, "../escape.txt", b"escape")
    with pytest.raises(contract.ReleaseContractError, match="unsafe path"):
        contract.verify_archive(archive_path, root, entries, prefix=PREFIX, zip_date=ZIP_DATE)


@pytest.mark.parametrize("mutation", ["missing", "extra", "reordered"])
def test_archive_verifier_rejects_inventory_mutation(
    release_tree: tuple[Path, list[Any]], mutation: str
) -> None:
    root, entries = release_tree
    archive_path = root / ARCHIVE_NAME
    names = contract.expected_archive_names(entries, PREFIX)
    if mutation == "missing":
        names = names[:-1]
    elif mutation == "extra":
        names = [*names, f"{PREFIX}/extra.txt"]
    else:
        names = [names[1], names[0], *names[2:]]
    with zipfile.ZipFile(archive_path, "w") as archive:
        for name in names:
            data = b"extra" if name.endswith("extra.txt") else _member_bytes(root, name)
            _write_member(archive, name, data)
    with pytest.raises(contract.ReleaseContractError, match="inventory/order mismatch"):
        contract.verify_archive(archive_path, root, entries, prefix=PREFIX, zip_date=ZIP_DATE)


def test_archive_verifier_rejects_wrong_platform_metadata(
    release_tree: tuple[Path, list[Any]],
) -> None:
    root, entries = release_tree
    archive_path = root / ARCHIVE_NAME
    names = contract.expected_archive_names(entries, PREFIX)
    with zipfile.ZipFile(archive_path, "w") as archive:
        for index, name in enumerate(names):
            _write_member(
                archive,
                name,
                _member_bytes(root, name),
                create_system=0 if index == 0 else 3,
            )
    with pytest.raises(contract.ReleaseContractError, match="create_system"):
        contract.verify_archive(archive_path, root, entries, prefix=PREFIX, zip_date=ZIP_DATE)


@pytest.mark.parametrize(
    ("kwargs", "match"),
    [
        ({"date_time": (2026, 9, 18, 12, 0, 0)}, "timestamp"),
        ({"mode": 0o100755}, "mode"),
        ({"extra": b"\x01\x00\x00\x00"}, "extra/comment"),
        ({"comment": b"note"}, "extra/comment"),
    ],
)
def test_archive_verifier_rejects_noncanonical_member_metadata(
    release_tree: tuple[Path, list[Any]],
    kwargs: dict[str, Any],
    match: str,
) -> None:
    root, entries = release_tree
    archive_path = root / ARCHIVE_NAME
    names = contract.expected_archive_names(entries, PREFIX)
    with zipfile.ZipFile(archive_path, "w") as archive:
        for index, name in enumerate(names):
            _write_member(
                archive,
                name,
                _member_bytes(root, name),
                **(kwargs if index == 0 else {}),
            )
    with pytest.raises(contract.ReleaseContractError, match=match):
        contract.verify_archive(archive_path, root, entries, prefix=PREFIX, zip_date=ZIP_DATE)


def test_archive_verifier_rejects_archive_comment(
    release_tree: tuple[Path, list[Any]],
) -> None:
    root, entries = release_tree
    archive_path = root / ARCHIVE_NAME
    with zipfile.ZipFile(archive_path, "w") as archive:
        _write_expected_members(archive, root, entries)
        archive.comment = b"noncanonical"
    with pytest.raises(contract.ReleaseContractError, match="archive comment"):
        contract.verify_archive(archive_path, root, entries, prefix=PREFIX, zip_date=ZIP_DATE)


def test_archive_verifier_rejects_stale_manifest_member(
    release_tree: tuple[Path, list[Any]],
) -> None:
    root, entries = release_tree
    archive_path = root / ARCHIVE_NAME
    names = contract.expected_archive_names(entries, PREFIX)
    with zipfile.ZipFile(archive_path, "w") as archive:
        for name in names:
            data = _member_bytes(root, name)
            if name.endswith("/SHA256SUMS"):
                data = bytes([data[0] ^ 1]) + data[1:]
            _write_member(archive, name, data)
    with pytest.raises(contract.ReleaseContractError, match="stale SHA256SUMS"):
        contract.verify_archive(archive_path, root, entries, prefix=PREFIX, zip_date=ZIP_DATE)


def test_archive_verifier_rejects_payload_byte_mismatch(
    release_tree: tuple[Path, list[Any]],
) -> None:
    root, entries = release_tree
    archive_path = root / ARCHIVE_NAME
    names = contract.expected_archive_names(entries, PREFIX)
    with zipfile.ZipFile(archive_path, "w") as archive:
        for name in names:
            data = _member_bytes(root, name)
            if name.endswith("/alpha.txt"):
                data = b"omega\n"
            _write_member(archive, name, data)
    with pytest.raises(contract.ReleaseContractError, match="payload digest mismatch"):
        contract.verify_archive(archive_path, root, entries, prefix=PREFIX, zip_date=ZIP_DATE)


def test_archive_verifier_rejects_tree_change_after_archive_build(
    release_tree: tuple[Path, list[Any]],
) -> None:
    root, entries = release_tree
    archive_path = root / ARCHIVE_NAME
    contract.build_archive(archive_path, root, entries, prefix=PREFIX, zip_date=ZIP_DATE)
    (root / "alpha.txt").write_bytes(b"omega\n")
    with pytest.raises(contract.ReleaseContractError, match="tree payload changed"):
        contract.verify_archive(archive_path, root, entries, prefix=PREFIX, zip_date=ZIP_DATE)


def test_archive_verifier_wraps_invalid_zip(
    release_tree: tuple[Path, list[Any]],
) -> None:
    root, entries = release_tree
    archive_path = root / ARCHIVE_NAME
    archive_path.write_bytes(b"not a zip")
    with pytest.raises(contract.ReleaseContractError, match="invalid or unreadable"):
        contract.verify_archive(archive_path, root, entries, prefix=PREFIX, zip_date=ZIP_DATE)
