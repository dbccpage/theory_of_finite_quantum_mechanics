"""Retained witness replay, strict JSON, and source custody failures."""

import json

import pytest
from certified_progress import producer
from certified_progress.replay import replay, strict_json, write_evidence


@pytest.mark.parametrize("raw", [b'{"x":1,"x":2}', b'{"x":NaN}',
                                  b'{"x":Infinity}', b'{"x":-Infinity}'])
def test_disk_admission_refuses_ambiguous_json(raw):
    with pytest.raises(ValueError):
        strict_json(raw)


def test_retained_replay_never_invokes_producer(tmp_path, monkeypatch):
    written = write_evidence(tmp_path)
    assert written == {"status": "PASS", "records": 15, "accepted": 8,
                       "rejected": 7, "provider_calls": 0, "authority_effect": "None"}

    def forbidden(*args, **kwargs):
        raise AssertionError("replay called the proposal producer")

    monkeypatch.setattr(producer, "solve_progress", forbidden)
    assert replay(tmp_path) == written


def test_changed_witness_cannot_use_an_old_receipt(tmp_path):
    write_evidence(tmp_path)
    path = tmp_path / "records.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["records"][0]["certificate"]["task_id"] = "changed-question"
    path.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError, match="replay mismatch"):
        replay(tmp_path)


def test_changed_source_binding_refuses_before_math(tmp_path):
    write_evidence(tmp_path)
    path = tmp_path / "records.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    name = next(iter(payload["sources"]))
    payload["sources"][name] = "0" * 64
    path.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError, match="source bindings"):
        replay(tmp_path)


def test_same_byte_record_symlink_refuses(tmp_path):
    directory = tmp_path / "run"
    write_evidence(directory)
    path = directory / "records.json"
    copied = tmp_path / "same_bytes.json"
    copied.write_bytes(path.read_bytes())
    path.unlink()
    path.symlink_to(copied)
    with pytest.raises(ValueError, match="non-regular"):
        replay(directory)
