"""Adversarial deposit paths must fail before any external file is read."""
import hashlib
import importlib.util
from pathlib import Path

import pytest
from deposit_paths import read_manifest, safe_path, sha256_of, walk_files


@pytest.mark.parametrize("relative", ["", ".", "..", "../outside", "/outside", "C:/outside",
                                     "a//b", "a/./b", "a/../b", "a\\b", "file:stream",
                                     "file\nname", "file.", "file ", "CON.txt", "a/LPT1"])
def test_unsafe_manifest_paths_are_refused(tmp_path, relative):
    with pytest.raises(ValueError, match="unsafe"):
        safe_path(tmp_path, relative)


def test_clean_tree_and_flat_manifest(tmp_path):
    (tmp_path / "asset").write_bytes(b"exact bytes")
    (tmp_path / ".lake").mkdir()
    (tmp_path / ".lake/cache").write_bytes(b"excluded")
    (tmp_path / "old.zip").write_bytes(b"excluded archive")
    (tmp_path / "test.pyc").write_bytes(b"excluded cache")
    digest = hashlib.sha256(b"exact bytes").hexdigest()
    assert sha256_of(tmp_path / "asset") == digest
    manifest = tmp_path / "SHA256SUMS"
    manifest.write_text(f"# comment\n\n{digest}  asset\n", encoding="utf-8")
    assert read_manifest(tmp_path, manifest) == [("asset", digest)]
    assert walk_files(tmp_path, {".lake"}, {"SHA256SUMS"}, {".zip", ".pyc"}) == [tmp_path / "asset"]


@pytest.mark.parametrize("body", ["bad line", "x"*64+"  asset", "a"*64+" asset",
                                 "a"*64+"  ../outside", "a"*64+"  SHA256SUMS",
                                 "a"*64+"  stale.ZIP",
                                 "a"*64+"  asset\n"+"b"*64+"  asset",
                                 "a"*64+"  Asset\n"+"b"*64+"  asset",
                                 "a"*64+"  Asset\n"+"b"*64+"  asset/child",
                                 "a"*64+"  asset/child\n"+"b"*64+"  Asset",
                                 "a"*64+"  Dir/a\n"+"b"*64+"  dir/b"])
def test_malformed_circular_and_duplicate_entries(tmp_path, body):
    manifest = tmp_path / "SHA256SUMS"
    manifest.write_text(body, encoding="utf-8")
    with pytest.raises(ValueError):
        read_manifest(tmp_path, manifest)


@pytest.mark.parametrize("name,is_dir", [("leaf", False), ("parent", True), (".lake", True)])
def test_file_and_directory_links_are_refused_before_pruning(tmp_path, name, is_dir):
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "secret").write_bytes(b"must not read")
    root = tmp_path / "package"
    root.mkdir()
    link = root / name
    try:
        link.symlink_to(outside if is_dir else outside / "secret", target_is_directory=is_dir)
    except OSError as error:
        pytest.skip(f"Host cannot create test symlink: {error}")
    with pytest.raises(ValueError, match="symlink|junction"):
        safe_path(root, name + ("/secret" if is_dir else ""))
    with pytest.raises(ValueError, match="symlink|junction"):
        walk_files(root, {".lake"}, set(), set())
    if is_dir:
        with pytest.raises(ValueError, match="symlink|junction"):
            safe_path(link, "secret")


def test_deposit_verifier_checks_inventory_and_rejects_escape(tmp_path, monkeypatch):
    package = Path(__file__).resolve().parents[2]
    spec = importlib.util.spec_from_file_location("review_deposit_verifier", package / "verify_deposit.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    monkeypatch.setattr(module, "ROOT", tmp_path)
    monkeypatch.setattr(module, "REQUIRED_FILES", ("asset",))
    (tmp_path / "asset").write_bytes(b"input")
    sums = tmp_path / "SHA256SUMS"
    sums.write_text(sha256_of(tmp_path / "asset") + "  asset\n", encoding="utf-8")
    assert module.check_manifest(sums) == []
    (tmp_path / "extra").write_bytes(b"extra")
    assert any("Unrecorded" in error for error in module.check_manifest(sums))
    sums.write_text("a"*64 + "  ../outside\n", encoding="utf-8")
    assert any("unsafe" in error for error in module.check_manifest(sums))


def test_case_aliases_from_filesystem_enumeration_fail_closed(tmp_path, monkeypatch):
    import deposit_paths

    (tmp_path / "Asset").write_bytes(b"a")
    (tmp_path / "asset").write_bytes(b"b")
    monkeypatch.setattr(deposit_paths.os, "walk", lambda *a, **kw: iter([(str(tmp_path), [], ["Asset", "asset"])]))
    with pytest.raises(ValueError, match="case-colliding"):
        walk_files(tmp_path, set(), set(), set())


def test_case_colliding_file_and_directory_fail_closed(tmp_path, monkeypatch):
    import deposit_paths

    dummy_stat = Path(__file__).stat()
    monkeypatch.setattr(Path, "stat", lambda self, *args, **kwargs: dummy_stat)

    # Case 1: Root file Asset and directory asset with child
    monkeypatch.setattr(
        deposit_paths.os,
        "walk",
        lambda *a, **kw: iter([
            (str(tmp_path), ["asset"], ["Asset"]),
            (str(tmp_path / "asset"), [], ["child"]),
        ]),
    )
    with pytest.raises(ValueError, match="case-colliding"):
        walk_files(tmp_path, set(), set(), set())

    # Case 2: Reversed walk order (child first, then Asset file)
    monkeypatch.setattr(
        deposit_paths.os,
        "walk",
        lambda *a, **kw: iter([
            (str(tmp_path / "asset"), [], ["child"]),
            (str(tmp_path), [], ["Asset"]),
        ]),
    )
    with pytest.raises(ValueError, match="case-colliding"):
        walk_files(tmp_path, set(), set(), set())

    # Case 3: Conflicting directory components (Dir/a and dir/b)
    monkeypatch.setattr(
        deposit_paths.os,
        "walk",
        lambda *a, **kw: iter([
            (str(tmp_path / "Dir"), [], ["a"]),
            (str(tmp_path / "dir"), [], ["b"]),
        ]),
    )
    with pytest.raises(ValueError, match="case-colliding"):
        walk_files(tmp_path, set(), set(), set())


def test_resolution_escape_and_nonregular_files_are_refused(tmp_path, monkeypatch):
    import deposit_paths

    target = tmp_path / "asset"
    target.write_bytes(b"a")
    resolve = Path.resolve
    with monkeypatch.context() as patch:
        patch.setattr(Path, "resolve", lambda p, *a, **kw: tmp_path.parent / "outside" if p == target else resolve(p, *a, **kw))
        with pytest.raises(ValueError, match="escapes"):
            safe_path(tmp_path, "asset")
    monkeypatch.setattr(deposit_paths.stat, "S_ISREG", lambda mode: False)
    with pytest.raises(ValueError, match="nonregular"):
        walk_files(tmp_path, set(), set(), set())
