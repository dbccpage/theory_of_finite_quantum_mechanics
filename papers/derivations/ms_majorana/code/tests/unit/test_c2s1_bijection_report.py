from __future__ import annotations

"""C2S1-002: mechanical bijection report — exact fixture counts + no autogen."""


from pathlib import Path


from omega_engine_governance.contracts.c2s1_bijection import (
    BijectionReport,
    build_report,
    count_rust_binding,
    count_file_binding,
    iter_contract_yaml,
    iter_prod_rs_files,
    write_report_markdown,
)


def test_fixture_exact_counts(tmp_path: Path) -> None:
    crates = tmp_path / "crates"
    corpus = tmp_path / "corpus"
    (crates / "alpha" / "src").mkdir(parents=True)
    (crates / "beta" / "src" / "nested").mkdir(parents=True)
    (crates / "alpha" / "src" / "lib.rs").write_text("// a\n", encoding="utf-8")
    (crates / "beta" / "src" / "lib.rs").write_text("// b\n", encoding="utf-8")
    (crates / "beta" / "src" / "nested" / "mod.rs").write_text(
        "// c\n", encoding="utf-8"
    )
    (crates / "alpha" / "target" / "x.rs").parent.mkdir(parents=True, exist_ok=True)
    (crates / "alpha" / "target" / "x.rs").write_text("skip\n", encoding="utf-8")

    (corpus / "math").mkdir(parents=True)
    (corpus / "math" / "one.contract.yaml").write_text(
        "schema_version: omega.contract.v1\nrust_binding:\n  crate: alpha\n",
        encoding="utf-8",
    )
    (corpus / "math" / "two.contract.yaml").write_text(
        "schema_version: omega.contract.v1\n",
        encoding="utf-8",
    )

    rs = iter_prod_rs_files(crates)
    assert len(rs) == 3
    contracts = iter_contract_yaml(corpus)
    assert len(contracts) == 2
    assert count_rust_binding(contracts) == 1

    report = build_report(crates_root=crates, corpus_root=corpus)
    assert report.rs_file_count == 3
    assert report.contract_yaml_count == 2
    assert report.contracts_with_rust_binding == 1
    assert report.crate_count == 2
    assert report.authority_effect == "None"
    assert any(r["code"] == "DEV-UNCONTRACTED" for r in report.residuals_open)


def test_mutation_drops_binding_count(tmp_path: Path) -> None:
    crates = tmp_path / "crates"
    corpus = tmp_path / "corpus"
    (crates / "a" / "src").mkdir(parents=True)
    (crates / "a" / "src" / "lib.rs").write_text("x\n", encoding="utf-8")
    (corpus).mkdir(parents=True)
    p = corpus / "b.contract.yaml"
    p.write_text("rust_binding: {}\n", encoding="utf-8")
    assert count_rust_binding([p]) == 1
    p.write_text("schema_version: omega.contract.v1\n", encoding="utf-8")
    assert count_rust_binding([p]) == 0


def test_empty_file_binding_fields_are_not_counted(tmp_path: Path) -> None:
    empty = tmp_path / "empty.contract.yaml"
    empty.write_text("crate:\nfile: null\n", encoding="utf-8")
    valid = tmp_path / "valid.contract.yaml"
    valid.write_text("crate: omega\nfile: src/lib.rs\n", encoding="utf-8")
    assert count_file_binding([empty, valid]) == 1


def test_no_autogen_contract_api() -> None:
    import omega_engine_governance.contracts.c2s1_bijection as m

    assert not hasattr(m, "auto_write_empty_contracts")
    assert not hasattr(m, "generate_missing_contracts")


def test_markdown_write(tmp_path: Path) -> None:
    out = tmp_path / "report.md"
    report = BijectionReport(
        crate_count=1,
        rs_file_count=2,
        contract_yaml_count=3,
        contracts_with_rust_binding=0,
        residuals_open=[{"code": "DEV-UNCONTRACTED", "detail": "x"}],
    )
    write_report_markdown(out, report)
    text = out.read_text(encoding="utf-8")
    assert "AuthorityEffect" in text
    assert "DEV-UNCONTRACTED" in text
    assert "| Leaf `.rs` files (scoped) | 2 |" in text
