from __future__ import annotations
"""C2S4-002: compliance residual report fixtures."""


import json
from pathlib import Path


from omega_engine_governance.contracts.c2s3_parity_refuse import REQUIRED_CLASS_CODES
from omega_engine_governance.contracts.c2s4_compliance_residual import (
    main,
    run_compliance,
)


def _classes(tmp: Path) -> Path:
    p = tmp / "classes.json"
    p.write_text(
        json.dumps({"classes": [{"code": c} for c in REQUIRED_CLASS_CODES]}),
        encoding="utf-8",
    )
    return p


def _scope(
    tmp: Path,
    crates: list[str],
    bindings: list[dict[str, str]],
    stubs: list[dict] | None = None,
) -> Path:
    p = tmp / "scope.json"
    p.write_text(
        json.dumps(
            {
                "crates_in_pass": crates,
                "required_bindings": bindings,
                "parity_stubs": stubs or [],
            }
        ),
        encoding="utf-8",
    )
    return p


def test_fixture_gap_dev_uncontracted(tmp_path: Path) -> None:
    crates = tmp_path / "crates"
    (crates / "alpha").mkdir(parents=True)
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    (corpus / "a.contract.yaml").write_text(
        "rust_binding:\n  crate: alpha\n  module: lib\n",
        encoding="utf-8",
    )
    scope = _scope(
        tmp_path,
        crates=["alpha"],
        bindings=[
            {"crate": "alpha", "module": "lib"},
            {"crate": "alpha", "module": "missing"},
        ],
    )
    report = run_compliance(
        scope_path=scope,
        corpus_root=corpus,
        crates_root=crates,
        classes_path=_classes(tmp_path),
    )
    assert report.authority_effect == "None"
    assert report.open_count >= 1
    codes = [r.code for r in report.residuals]
    assert "DEV-UNCONTRACTED" in codes
    gap = next(r for r in report.residuals if r.code == "DEV-UNCONTRACTED")
    assert gap.disposition == "OPEN"
    assert "missing" in gap.detail


def test_fixture_clean_bindings_no_uncontracted(tmp_path: Path) -> None:
    crates = tmp_path / "crates"
    (crates / "alpha").mkdir(parents=True)
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    (corpus / "a.contract.yaml").write_text(
        "rust_binding:\n  crate: alpha\n  module: lib\n",
        encoding="utf-8",
    )
    scope = _scope(
        tmp_path,
        crates=["alpha"],
        bindings=[{"crate": "alpha", "module": "lib"}],
    )
    report = run_compliance(
        scope_path=scope,
        corpus_root=corpus,
        crates_root=crates,
        classes_path=_classes(tmp_path),
    )
    uncontracted = [r for r in report.residuals if r.code == "DEV-UNCONTRACTED"]
    assert uncontracted == []


def test_main_exit_0_with_open_residuals(tmp_path: Path) -> None:
    crates = tmp_path / "crates"
    (crates / "alpha").mkdir(parents=True)
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    (corpus / "a.contract.yaml").write_text(
        "rust_binding:\n  crate: alpha\n  module: lib\n",
        encoding="utf-8",
    )
    scope = _scope(
        tmp_path,
        crates=["alpha"],
        bindings=[
            {"crate": "alpha", "module": "lib"},
            {"crate": "alpha", "module": "gone"},
        ],
    )
    report_path = tmp_path / "report.txt"
    ndjson_path = tmp_path / "open.ndjson"
    md_path = tmp_path / "open.md"
    code = main(
        [
            "--scope",
            str(scope),
            "--corpus",
            str(corpus),
            "--crates",
            str(crates),
            "--classes",
            str(_classes(tmp_path)),
            "--report",
            str(report_path),
            "--ndjson",
            str(ndjson_path),
            "--markdown",
            str(md_path),
        ]
    )
    assert code == 0
    assert report_path.is_file()
    assert "OPEN" in report_path.read_text(encoding="utf-8")
    lines = [ln for ln in ndjson_path.read_text(encoding="utf-8").splitlines() if ln]
    assert len(lines) >= 1
    row = json.loads(lines[0])
    assert row["disposition"] == "OPEN"
    assert "AuthorityEffect" in md_path.read_text(encoding="utf-8")


def test_tool_failure_missing_scope(tmp_path: Path) -> None:
    code = main(
        [
            "--scope",
            str(tmp_path / "nope.json"),
            "--classes",
            str(_classes(tmp_path)),
        ]
    )
    assert code == 1


def test_no_autogen_api() -> None:
    import omega_engine_governance.contracts.c2s4_compliance_residual as m

    assert not hasattr(m, "auto_write_empty_contracts")
    assert not hasattr(m, "generate_missing_contracts")


