from __future__ import annotations
"""OEAGS-S1: bijection residual consumer tests."""


from pathlib import Path

from omega_engine_governance.contracts.c2s1_bijection import BijectionReport
from omega_engine_governance.contracts.oeags_bijection_residual import (
    OeagsBijectionPacket,
    ResidualRow,
    build_oeags_packet,
    compare_baseline,
    parse_baseline_markdown,
    residuals_from_report,
    write_packet,
)


def test_parse_baseline_markdown_exact() -> None:
    md = """# Bijection report baseline (C2S1-002)

| Metric | Value |
| --- | ---: |
| Crates in include | 50 |
| Leaf `.rs` files (scoped) | 989 |
| `*.contract.yaml` | 631 |
| Contracts with `rust_binding` | 83 |
"""
    d = parse_baseline_markdown(md)
    assert d["crate_count"] == 50
    assert d["rs_file_count"] == 989
    assert d["contract_yaml_count"] == 631
    assert d["contracts_with_rust_binding"] == 83


def test_residuals_from_report() -> None:
    r = BijectionReport(residuals_open=[{"code": "DEV-UNCONTRACTED", "detail": "x"}])
    rows = residuals_from_report(r)
    assert len(rows) == 1
    assert rows[0].code == "DEV-UNCONTRACTED"
    assert rows[0].disposition == "OPEN"


def test_compare_baseline_pressure() -> None:
    live = {
        "crate_count": 50,
        "rs_file_count": 1000,
        "contract_yaml_count": 631,
        "contracts_with_rust_binding": 83,
    }
    base = {
        "crate_count": 50,
        "rs_file_count": 989,
        "contract_yaml_count": 631,
        "contracts_with_rust_binding": 83,
    }
    rows = compare_baseline(live, base)
    assert any(r.code == "DEV-UNCONTRACTED" and "grew" in r.detail for r in rows)


def test_compare_baseline_no_pressure_when_yaml_grows() -> None:
    live = {
        "rs_file_count": 1000,
        "contract_yaml_count": 640,
        "crate_count": 50,
        "contracts_with_rust_binding": 90,
    }
    base = {
        "rs_file_count": 989,
        "contract_yaml_count": 631,
        "crate_count": 50,
        "contracts_with_rust_binding": 83,
    }
    rows = compare_baseline(live, base)
    assert not any("grew" in r.detail for r in rows)


def test_ndjson_and_receipt(tmp_path: Path) -> None:
    pkt = OeagsBijectionPacket(
        live={
            "crate_count": 1,
            "rs_file_count": 2,
            "contract_yaml_count": 3,
            "contracts_with_rust_binding": 0,
        },
        baseline={
            "crate_count": 1,
            "rs_file_count": 2,
            "contract_yaml_count": 3,
            "contracts_with_rust_binding": 0,
        },
        residuals=[
            ResidualRow(code="DEV-UNCONTRACTED", disposition="OPEN", detail="gap")
        ],
        generated_at="t0",
    )
    assert "DEV-UNCONTRACTED" in pkt.residuals_ndjson()
    md = pkt.to_markdown_receipt()
    assert "AuthorityEffect" in md
    assert "None" in md
    write_packet(tmp_path, packet=pkt)
    assert (tmp_path / "residuals.ndjson").is_file()
    assert (tmp_path / "oeags_receipt_latest.md").is_file()


def test_build_packet_fixture_tree(tmp_path: Path) -> None:
    crates = tmp_path / "crates"
    corpus = tmp_path / "corpus"
    (crates / "a" / "src").mkdir(parents=True)
    (crates / "a" / "src" / "lib.rs").write_text("x\n", encoding="utf-8")
    (corpus).mkdir()
    (corpus / "c.contract.yaml").write_text(
        "schema_version: omega.contract.v1\n", encoding="utf-8"
    )
    base_md = tmp_path / "base.md"
    base_md.write_text(
        "| Crates in include | 1 |\n"
        "| Leaf `.rs` files (scoped) | 1 |\n"
        "| `*.contract.yaml` | 1 |\n"
        "| Contracts with `rust_binding` | 0 |\n",
        encoding="utf-8",
    )
    pkt = build_oeags_packet(
        crates_root=crates,
        corpus_root=corpus,
        baseline_md=base_md,
        baseline_json=tmp_path / "missing.json",
    )
    assert pkt.authority_effect == "None"
    assert pkt.live["rs_file_count"] == 1
    assert pkt.live["contract_yaml_count"] == 1
    assert any(r.code == "DEV-UNCONTRACTED" for r in pkt.residuals)


