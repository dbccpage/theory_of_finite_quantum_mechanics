from __future__ import annotations

"""Repo-wide contract URN uniqueness: the map contract_id -> file must be a function."""


from pathlib import Path

from omega_engine_governance.contracts.contract_urn_uniqueness import (
    build_report,
    iter_contract_files,
    read_contract_ref,
)


def _write(root: Path, rel: str, contract_id: str | None) -> Path:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    body = "schema_version: omega.contract.v1\n"
    if contract_id is not None:
        body += f"contract_id: {contract_id}\n"
    p.write_text(body, encoding="utf-8")
    return p


def test_duplicate_id_across_directories_is_detected(tmp_path: Path):
    _write(
        tmp_path,
        "omega_engine_governance/contracts/contracts_system/a.contract.yaml",
        "urn:omega:state:packet:v1.0.0",
    )
    _write(
        tmp_path,
        "omega_engine/crates/symbol_game/_contracts/b.contract.yaml",
        "urn:omega:state:packet:v1.0.0",
    )

    report = build_report(repo_root=tmp_path)
    assert not report.ok
    assert list(report.duplicates) == ["urn:omega:state:packet:v1.0.0"]
    assert len(report.duplicates["urn:omega:state:packet:v1.0.0"]) == 2
    assert report.ungoverned_files == 1
    assert report.governed_files == 1


def test_distinct_ids_are_clean(tmp_path: Path):
    _write(
        tmp_path,
        "omega_engine_governance/contracts/contracts_math/a.contract.yaml",
        "urn:omega:math:adjoint:v0.1.0",
    )
    _write(
        tmp_path,
        "omega_engine_governance/contracts/contracts_math/b.contract.yaml",
        "urn:omega:math:carrier:v0.1.0",
    )

    report = build_report(repo_root=tmp_path)
    assert report.ok
    assert report.duplicates == {}
    assert report.scanned_files == 2


def test_fixtures_are_reported_but_do_not_fail_the_gate(tmp_path: Path):
    _write(
        tmp_path,
        "omega_engine_governance/contracts/contracts_math/live.contract.yaml",
        "urn:omega:math:trichotomy:v0.2.0",
    )
    _write(
        tmp_path,
        "omega_engine/_fixtures/v1/good/copy.contract.yaml",
        "urn:omega:math:trichotomy:v0.2.0",
    )

    report = build_report(repo_root=tmp_path)
    assert report.ok
    assert report.duplicates == {}
    assert report.fixture_files == 1
    assert report.fixture_shadows == {
        "urn:omega:math:trichotomy:v0.2.0": [
            "omega_engine/_fixtures/v1/good/copy.contract.yaml"
        ]
    }


def test_two_fixtures_sharing_an_id_do_not_fail_the_gate(tmp_path: Path):
    _write(
        tmp_path,
        "omega_engine/_fixtures/v1/good/a.contract.yaml",
        "urn:omega:math:x:v0.1.0",
    )
    _write(
        tmp_path,
        "omega_engine/_fixtures/v1/good/b.contract.yaml",
        "urn:omega:math:x:v0.1.0",
    )
    report = build_report(repo_root=tmp_path)
    assert report.ok
    assert report.fixture_files == 2


def test_quoted_ids_collide_with_unquoted_ids(tmp_path: Path):
    _write(
        tmp_path,
        "omega_engine_governance/contracts/contracts_system/a.contract.yaml",
        '"urn:omega:products:symbol_game:v1.0.0"',
    )
    _write(
        tmp_path,
        "omega_engine_governance/contracts/contracts_system/b.contract.yaml",
        "urn:omega:products:symbol_game:v1.0.0",
    )
    report = build_report(repo_root=tmp_path)
    assert not report.ok
    assert list(report.duplicates) == ["urn:omega:products:symbol_game:v1.0.0"]


def test_files_without_contract_id_are_ignored(tmp_path: Path):
    _write(
        tmp_path,
        "omega_engine_governance/contracts/contracts_system/a.contract.yaml",
        None,
    )
    report = build_report(repo_root=tmp_path)
    assert report.scanned_files == 0
    assert report.ok


def test_nested_worktrees_and_vendor_dirs_are_not_scanned(tmp_path: Path):
    _write(
        tmp_path,
        "omega_engine_governance/contracts/contracts_system/a.contract.yaml",
        "urn:omega:state:packet:v1.0.0",
    )
    _write(
        tmp_path,
        ".claude/worktrees/other/omega_engine_governance/contracts/a.contract.yaml",
        "urn:omega:state:packet:v1.0.0",
    )
    _write(
        tmp_path, "node_modules/pkg/a.contract.yaml", "urn:omega:state:packet:v1.0.0"
    )
    _write(tmp_path, "target/debug/a.contract.yaml", "urn:omega:state:packet:v1.0.0")

    report = build_report(repo_root=tmp_path)
    assert report.ok
    assert report.scanned_files == 1


def test_only_contract_yaml_suffix_is_collected(tmp_path: Path):
    _write(
        tmp_path,
        "omega_engine_governance/contracts/a.contract.yaml",
        "urn:omega:math:a:v0.1.0",
    )
    (tmp_path / "omega_engine_governance" / "contracts" / "plain.yaml").write_text(
        "contract_id: urn:omega:math:a:v0.1.0\n", encoding="utf-8"
    )
    files = iter_contract_files(tmp_path)
    assert len(files) == 1
    assert files[0].name == "a.contract.yaml"


def test_read_contract_ref_classifies_governed_and_fixture(tmp_path: Path):
    gov = _write(
        tmp_path,
        "omega_engine_governance/contracts/contracts_math/a.contract.yaml",
        "urn:omega:math:a:v0.1.0",
    )
    fix = _write(
        tmp_path,
        "omega_engine/_fixtures/v1/good/b.contract.yaml",
        "urn:omega:math:b:v0.1.0",
    )
    stray = _write(
        tmp_path,
        "omega_engine/crates/symbol_game/_contracts/c.contract.yaml",
        "urn:omega:math:c:v0.1.0",
    )

    g = read_contract_ref(gov, tmp_path)
    f = read_contract_ref(fix, tmp_path)
    s = read_contract_ref(stray, tmp_path)
    assert g is not None and g.is_governed and not g.is_fixture
    assert f is not None and f.is_fixture
    assert s is not None and not s.is_governed and not s.is_fixture


def test_inline_comment_cannot_hide_duplicate_contract_id(tmp_path: Path):
    contract_id = "urn:omega:math:a:v0.1.0"
    _write(
        tmp_path,
        "omega_engine_governance/contracts/contracts_math/a.contract.yaml",
        contract_id,
    )
    commented = _write(
        tmp_path,
        "omega_engine/crates/symbol_game/_contracts/a.contract.yaml",
        None,
    )
    commented.write_text(f"contract_id: {contract_id} # duplicate\n", encoding="utf-8")
    report = build_report(repo_root=tmp_path)
    assert report.ok is False
    assert list(report.duplicates) == [contract_id]


def test_only_canonical_contract_tree_is_governed(tmp_path: Path):
    path = _write(
        tmp_path,
        "omega_engine_governance/tests/a.contract.yaml",
        "urn:omega:math:a:v0.1.0",
    )
    ref = read_contract_ref(path, tmp_path)
    assert ref is not None
    assert ref.is_governed is False


def test_missing_root_reports_nothing(tmp_path: Path):
    report = build_report(repo_root=tmp_path / "absent")
    assert report.scanned_files == 0
    assert report.ok


def test_live_repository_has_no_duplicate_contract_ids():
    """Non-regression gate: the real corpus must keep contract_id a function."""
    report = build_report()
    assert report.scanned_files > 600
    assert report.duplicates == {}, (
        "duplicate contract_id claimed by multiple files: "
        + "; ".join(f"{k} -> {v}" for k, v in report.duplicates.items())
    )


def test_live_repository_has_no_contracts_outside_the_governed_tree():
    report = build_report()
    assert report.ungoverned == [], (
        "contract files outside omega_engine_governance/: "
        + ", ".join(report.ungoverned)
    )
