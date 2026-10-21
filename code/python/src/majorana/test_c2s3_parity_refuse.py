from __future__ import annotations
"""C2S3-002: typed parity refuse PASS/FAIL fixtures."""


import json
from pathlib import Path

from omega_engine_governance.contracts.c2s3_parity_refuse import (
    DEFAULT_MISSING_CLASS,
    REQUIRED_CLASS_CODES,
    run_parity_refuse,
)


def _write_classes(tmp_path: Path) -> Path:
    classes = tmp_path / "classes.json"
    classes.write_text(
        json.dumps(
            {
                "classes": [{"code": c} for c in REQUIRED_CLASS_CODES],
                "authority_effect": "None",
            }
        ),
        encoding="utf-8",
    )
    return classes


def test_fixture_pass_typed(tmp_path: Path) -> None:
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
        json.dumps({"pilot_required_bindings": [{"crate": "alpha", "module": "lib"}]}),
        encoding="utf-8",
    )
    report = run_parity_refuse(
        pilot_path=pilot,
        corpus_root=corpus,
        classes_path=_write_classes(tmp_path),
    )
    assert report.ok is True
    assert report.missing == []
    assert report.covered == ["alpha::lib"]
    assert report.authority_effect == "None"
    assert report.pilot_count == 1


def test_fixture_fail_dev_uncontracted(tmp_path: Path) -> None:
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
    report = run_parity_refuse(
        pilot_path=pilot,
        corpus_root=corpus,
        classes_path=_write_classes(tmp_path),
    )
    assert report.ok is False
    assert len(report.missing) == 1
    assert report.missing[0].target == "beta::missing"
    assert report.missing[0].refuse_class == DEFAULT_MISSING_CLASS
    assert report.missing[0].refuse_class == "DEV-UNCONTRACTED"
    assert report.authority_effect == "None"


def test_no_autogen_api() -> None:
    import omega_engine_governance.contracts.c2s3_parity_refuse as m

    assert not hasattr(m, "auto_write_empty_contracts")
    assert not hasattr(m, "generate_missing_contracts")


def test_main_exit_codes(tmp_path: Path) -> None:
    from omega_engine_governance.contracts.c2s3_parity_refuse import main

    corpus = tmp_path / "corpus"
    corpus.mkdir()
    (corpus / "a.contract.yaml").write_text(
        "schema_version: omega.contract.v1\n"
        "rust_binding:\n"
        "  crate: alpha\n"
        "  module: lib\n",
        encoding="utf-8",
    )
    pilot_ok = tmp_path / "ok.json"
    pilot_ok.write_text(
        json.dumps({"pilot_required_bindings": [{"crate": "alpha", "module": "lib"}]}),
        encoding="utf-8",
    )
    pilot_bad = tmp_path / "bad.json"
    pilot_bad.write_text(
        json.dumps(
            {
                "pilot_required_bindings": [
                    {"crate": "alpha", "module": "lib"},
                    {"crate": "z", "module": "nope"},
                ]
            }
        ),
        encoding="utf-8",
    )
    classes = _write_classes(tmp_path)
    assert (
        main(
            [
                "--pilot",
                str(pilot_ok),
                "--corpus",
                str(corpus),
                "--classes",
                str(classes),
            ]
        )
        == 0
    )
    assert (
        main(
            [
                "--pilot",
                str(pilot_bad),
                "--corpus",
                str(corpus),
                "--classes",
                str(classes),
            ]
        )
        == 1
    )


