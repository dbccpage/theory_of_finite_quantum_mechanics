"""Lossless migration, historical custody and single-file writer checks."""
import hashlib
import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
import contract_scores as store


@pytest.fixture
def repo(tmp_path, monkeypatch):
    monkeypatch.setattr(store, "ROOT", tmp_path)
    monkeypatch.setattr(store, "_cached_index", None)
    return tmp_path


def prepare(repo, monkeypatch):
    source = repo / "code/agent_functor.rs"
    source.parent.mkdir()
    source.write_text("// source stays unchanged\n")
    files = {
        "code/agent_functor.rs.contract.yaml": b"status: draft\r\nnote: exact original\r\n",
        "code/agent_functor.score.yaml": b"level: L3\nis_complete: true\nscore_token: L3A\n",
        "code/agent_functor.rs.scoring.yaml": b"is_complete: false\nscore_token: null\n",
        "evidence/prior/agent_functor.rs.scoring.yam": b"artifact:\n  path: code/agent_functor.rs\ngates:\n  G2: E\n",
    }
    for name, data in files.items():
        p = repo / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
    monkeypatch.setattr(store.subprocess, "check_output", lambda *a, **kw: ("\0".join(files) + "\0").encode())
    return source, files


def test_all_versions_preserved_without_upgrading_current_assessment(repo, monkeypatch):
    source, files = prepare(repo, monkeypatch)
    before = source.read_bytes()
    store.migrate(apply=True)
    doc = store.load(repo / "code/agent_functor.contract.score.yaml")
    assert doc["artifact"] == "code/agent_functor.rs"
    assert len(doc["scoring_history"]) == 3
    current = next(e["record"] for e in doc["scoring_history"] if e["sha256"] == doc["current_scoring"])
    assert current["score_token"] is None and current["is_complete"] is False
    assert doc["contract"]["status"] == "draft"
    for alias, raw in files.items():
        assert not (repo / alias).exists()
        assert store.read_bytes(repo / alias, hashlib.sha256(raw).hexdigest()) == raw
    assert source.read_bytes() == before
    store.check()
    store.migrate(apply=True)  # idempotent: the custody index must not be erased
    assert len(store.index()) == len(files)


def test_existing_writer_appends_history_without_recreating_sidecars(repo, monkeypatch):
    _, files = prepare(repo, monkeypatch)
    store.migrate(apply=True)
    alias = repo / "code/agent_functor.rs.scoring.yaml"
    virtual = store.RecordPath(alias)
    old = files["code/agent_functor.rs.scoring.yaml"]
    new = '{"is_complete": false, "score_token": null, "note": "review pending"}\n'
    virtual.write_text(new, encoding="utf-8", newline="\n")
    assert virtual.is_file() and virtual.exists()
    assert not Path(alias).exists()
    assert virtual.read_text() == new
    assert store.read_bytes(alias, store.sha(old)) == old
    doc = store.load(repo / "code/agent_functor.contract.score.yaml")
    count = len(doc["scoring_history"])
    virtual.write_text(new, encoding="utf-8", newline="\n")
    assert len(store.load(repo / "code/agent_functor.contract.score.yaml")["scoring_history"]) == count
    store.check()


def test_corrupt_history_is_refused(repo, monkeypatch):
    _, files = prepare(repo, monkeypatch)
    store.migrate(apply=True)
    path = repo / "code/agent_functor.contract.score.yaml"
    doc = store.load(path)
    doc["contract_history"][0]["raw_utf8"] += "tampered"
    store.save(path, doc)
    with pytest.raises(ValueError, match="Corrupt"):
        store.read_bytes(repo / "code/agent_functor.rs.contract.yaml")
    with pytest.raises(SystemExit):
        store.check()


def test_invalid_input_prevents_any_deletion(repo, monkeypatch):
    _, files = prepare(repo, monkeypatch)
    broken = repo / "code/agent_functor.rs.contract.yaml"
    broken.write_text("not: [valid\n")
    with pytest.raises(Exception):
        store.migrate(apply=True)
    assert all((repo / name).is_file() for name in files)
    assert not list(repo.rglob("*" + store.SUFFIX))


def test_registry_without_source_is_not_given_a_fictitious_artifact(repo, monkeypatch):
    p = repo / "registry.contract.yaml"
    p.write_text("contract_id: urn:example\n")
    monkeypatch.setattr(store.subprocess, "check_output", lambda *a, **kw: b"registry.contract.yaml\0")
    store.migrate(apply=True)
    doc = store.load(repo / "registry.contract.score.yaml")
    assert doc["artifact"] is None
    assert doc["contract"]["contract_id"] == "urn:example"
    assert doc["scoring_history"] == [] and doc["current_scoring"] is None


def test_escaping_index_is_refused(repo):
    store._cached_index = {"old.contract.yaml": {"combined_path": "../outside.contract.score.yaml"}}
    with pytest.raises(ValueError):
        store.canonical_path(repo / "old.contract.yaml")


def test_current_filename_is_not_mistaken_for_a_legacy_score():
    assert not store.LEGACY.search("agent_functor.contract.score.yaml")
    for suffix in (".rs.contract.yaml", ".rs.scoring.yaml", ".scoring.yam", ".score.yml"):
        assert store.LEGACY.search("agent_functor" + suffix)


def test_readable_score_cannot_be_changed_without_matching_original(repo, monkeypatch):
    _, _ = prepare(repo, monkeypatch)
    store.migrate(apply=True)
    path = repo / "code/agent_functor.contract.score.yaml"
    doc = store.load(path)
    doc["scoring_history"][0]["record"]["score_token"] = "invented-upgrade"
    store.save(path, doc)
    with pytest.raises(SystemExit):
        store.check()


def test_ambiguous_source_names_are_refused_before_deletion(repo, monkeypatch):
    (repo / "ambiguous.rs").write_text("// Rust")
    (repo / "ambiguous.py").write_text("# Python")
    old = repo / "ambiguous.score.yaml"
    old.write_text("is_complete: false\n")
    monkeypatch.setattr(store.subprocess, "check_output", lambda *a, **kw: b"ambiguous.score.yaml\0")
    with pytest.raises(ValueError, match="Ambiguous"):
        store.migrate(apply=True)
    assert old.is_file()


def test_four_alias_writer_and_archive_copy_create_only_combined_files(repo, monkeypatch):
    source = repo / "lib.rs"
    source.write_text("// source\n")
    contract = '{"status": "draft"}\n'
    scoring = '{"is_complete": false, "score_token": null}\n'
    for alias, text in [("lib.contract.yaml", contract), ("lib.rs.contract.yaml", contract),
                        ("lib.scoring.yaml", scoring), ("lib.rs.scoring.yaml", scoring)]:
        store.RecordPath(repo / alias).write_text(text, encoding="utf-8", newline="\n")
        assert not (repo / alias).exists()
    document = store.load(repo / "lib.contract.score.yaml")
    assert document["artifact"] == "lib.rs"
    assert len(document["contract_history"]) == len(document["scoring_history"]) == 1
    destination = repo / "previous" / "lib.rs.scoring.yaml"
    store.copy_file(repo / "lib.rs.scoring.yaml", destination)
    assert not destination.exists()
    assert store.read_bytes(destination) == scoring.encode()
    combined = ["lib.contract.score.yaml", "previous/lib.contract.score.yaml"]
    monkeypatch.setattr(store.subprocess, "check_output", lambda *a, **kw: ("\0".join(combined) + "\0").encode())
    store.check()
