from __future__ import annotations
"""C3S0-002: corpus census exact fixtures + no corpus write."""


from pathlib import Path

from omega_engine_governance.contracts.c3s0_corpus_census import (
    build_census,
    parse_top_fields,
    write_census,
)


def test_parse_top_fields_strips_quotes() -> None:
    text = 'kind: "math_contract"\nstatus: mathematical_wip\n'
    f = parse_top_fields(text)
    assert f["kind"] == "math_contract"
    assert f["status"] == "mathematical_wip"


def test_fixture_exact_counts(tmp_path: Path) -> None:
    corpus = tmp_path / "corpus"
    (corpus / "a").mkdir(parents=True)
    (corpus / "a" / "one.contract.yaml").write_text(
        "kind: math_contract\nstatus: mathematical_wip\n", encoding="utf-8"
    )
    (corpus / "a" / "two.contract.yaml").write_text(
        'kind: "math_contract"\nstatus: active\n', encoding="utf-8"
    )
    (corpus / "b.contract.yaml").write_text(
        "kind: evidence_contract\nstatus: active\n", encoding="utf-8"
    )
    report = build_census(
        corpus_root=corpus, review_index_path=tmp_path / "missing.json"
    )
    assert report.total_contracts == 3
    assert report.kind_histogram["math_contract"] == 2
    assert report.kind_histogram["evidence_contract"] == 1
    assert report.status_histogram["mathematical_wip"] == 1
    assert report.status_histogram["active"] == 2
    assert report.disposition_histogram["suspect"] == 3
    assert any(a["code"] == "DEV-KIND-DRIFT" for a in report.anomalies)


def test_index_admits_one(tmp_path: Path) -> None:
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    (corpus / "x.contract.yaml").write_text(
        "kind: math_contract\nstatus: mathematical_wip\n", encoding="utf-8"
    )
    idx = tmp_path / "idx.json"
    idx.write_text('{"entries": {"x.contract.yaml": "admitted"}}', encoding="utf-8")
    report = build_census(corpus_root=corpus, review_index_path=idx)
    assert report.disposition_histogram.get("admitted") == 1
    assert report.disposition_histogram.get("suspect", 0) == 0


def test_write_does_not_touch_corpus(tmp_path: Path) -> None:
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    p = corpus / "z.contract.yaml"
    p.write_text("kind: state_contract\nstatus: draft\n", encoding="utf-8")
    before = p.read_text(encoding="utf-8")
    out_md = tmp_path / "out.md"
    report = build_census(corpus_root=corpus, review_index_path=None)
    write_census(out_md, tmp_path / "out.json", report)
    assert p.read_text(encoding="utf-8") == before
    assert out_md.is_file()
    assert "AuthorityEffect" in out_md.read_text(encoding="utf-8")


def test_mutation_changes_count(tmp_path: Path) -> None:
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    (corpus / "a.contract.yaml").write_text(
        "kind: math_contract\nstatus: active\n", encoding="utf-8"
    )
    r1 = build_census(corpus_root=corpus, review_index_path=None)
    assert r1.total_contracts == 1
    (corpus / "b.contract.yaml").write_text(
        "kind: math_contract\nstatus: active\n", encoding="utf-8"
    )
    r2 = build_census(corpus_root=corpus, review_index_path=None)
    assert r2.total_contracts == r1.total_contracts + 1


