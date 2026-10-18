from __future__ import annotations
"""C2S2-002/004: pilot refuse PASS/FAIL fixtures."""


import json
from pathlib import Path

from omega_engine_governance.contracts.c2s2_uncontracted_refuse import (
    PilotEntry,
    evaluate_pilot,
    load_pilot_set,
    run_refuse,
)


def test_fixture_pass(tmp_path: Path) -> None:
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    (corpus / "a.contract.yaml").write_text(
        "schema_version: omega.contract.v1\n"
        "rust_binding:\n"
        "  crate: alpha\n"
        "  module: lib\n"
        "  symbols:\n"
        "  - Foo\n",
        encoding="utf-8",
    )
    pilot = tmp_path / "pilot.json"
    pilot.write_text(
        json.dumps({"pilot_required_bindings": [{"crate": "alpha", "module": "lib"}]}),
        encoding="utf-8",
    )
    report = run_refuse(pilot_path=pilot, corpus_root=corpus)
    assert report.ok is True
    assert report.missing == []
    assert report.covered == ["alpha::lib"]
    assert report.pilot_count == 1


def test_fixture_fail_missing(tmp_path: Path) -> None:
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    (corpus / "a.contract.yaml").write_text(
        "schema_version: omega.contract.v1\n"
        "rust_binding:\n"
        "  crate: alpha\n"
        "  module: lib\n",
        encoding="utf-8",
    )
    pilot = tmp_path / "pilot.json"
    pilot.write_text(
        json.dumps(
            {
                "pilot_required_bindings": [
                    {"crate": "alpha", "module": "lib"},
                    {"crate": "beta", "module": "missing"},
                ]
            }
        ),
        encoding="utf-8",
    )
    report = run_refuse(pilot_path=pilot, corpus_root=corpus)
    assert report.ok is False
    assert report.missing == ["beta::missing"]
    assert "alpha::lib" in report.covered


def test_no_autogen_api() -> None:
    import omega_engine_governance.contracts.c2s2_uncontracted_refuse as m

    assert not hasattr(m, "auto_write_empty_contracts")
    assert not hasattr(m, "generate_missing_contracts")


def test_evaluate_exact() -> None:
    pilot = [PilotEntry("c", "m"), PilotEntry("x", "y")]
    bindings = {("c", "m")}
    r = evaluate_pilot(pilot, bindings)
    assert r.covered == ["c::m"]
    assert r.missing == ["x::y"]
    assert r.ok is False


def test_repo_pilot_set_loads() -> None:
    from omega_engine_governance.contracts import c2s2_uncontracted_refuse as m

    if m._DEFAULT_PILOT.is_file():
        entries = load_pilot_set(m._DEFAULT_PILOT)
        assert len(entries) >= 1
        assert all(e.crate and e.module for e in entries)


