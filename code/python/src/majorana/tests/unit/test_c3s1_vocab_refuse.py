from __future__ import annotations
"""C3S1-002/004: vocabulary refuse fixture PASS/FAIL."""


import json
from pathlib import Path

from omega_engine_governance.contracts.c3s1_vocab_refuse import (
    VocabFreeze,
    evaluate_corpus,
    normalize_token,
    run,
)


def _vocab(tmp: Path) -> Path:
    p = tmp / "vocab.json"
    p.write_text(
        json.dumps(
            {
                "canonical_kinds": ["math_contract", "evidence_contract"],
                "canonical_statuses": [
                    "active",
                    "draft",
                    "mathematical_wip",
                    "deprecated",
                ],
                "kind_aliases": {"mathematical-structure": "math_contract"},
                "status_aliases": {"active_provisional": "active"},
            }
        ),
        encoding="utf-8",
    )
    return p


def test_normalize_alias_and_quotes() -> None:
    aliases = {"mathematical-structure": "math_contract"}
    assert normalize_token("mathematical-structure", aliases) == "math_contract"
    assert normalize_token('"math_contract"', {}) == "math_contract"


def test_strict_fails_unknown_kind(tmp_path: Path) -> None:
    corpus = tmp_path / "c"
    corpus.mkdir()
    (corpus / "a.contract.yaml").write_text(
        "kind: totally_fake_kind\nstatus: active\n", encoding="utf-8"
    )
    vocab = VocabFreeze.load(_vocab(tmp_path))
    r = evaluate_corpus(vocab, corpus, mode="strict")
    assert r.unknown_kind == 1
    assert r.strict_should_fail(False) is True
    _, code = run(
        vocab_path=_vocab(tmp_path),
        corpus_root=corpus,
        mode="strict",
        fail_missing_kind=False,
    )
    assert code == 1


def test_strict_passes_alias(tmp_path: Path) -> None:
    corpus = tmp_path / "c"
    corpus.mkdir()
    (corpus / "a.contract.yaml").write_text(
        "kind: mathematical-structure\nstatus: active_provisional\n", encoding="utf-8"
    )
    _, code = run(
        vocab_path=_vocab(tmp_path),
        corpus_root=corpus,
        mode="strict",
        fail_missing_kind=False,
    )
    assert code == 0


def test_missing_kind_strict_default_ok(tmp_path: Path) -> None:
    corpus = tmp_path / "c"
    corpus.mkdir()
    (corpus / "a.contract.yaml").write_text("status: active\n", encoding="utf-8")
    report, code = run(
        vocab_path=_vocab(tmp_path),
        corpus_root=corpus,
        mode="strict",
        fail_missing_kind=False,
    )
    assert report.missing_kind == 1
    assert code == 0


def test_missing_kind_strict_with_flag_fails(tmp_path: Path) -> None:
    corpus = tmp_path / "c"
    corpus.mkdir()
    (corpus / "a.contract.yaml").write_text("status: active\n", encoding="utf-8")
    _, code = run(
        vocab_path=_vocab(tmp_path),
        corpus_root=corpus,
        mode="strict",
        fail_missing_kind=True,
    )
    assert code == 1


def test_report_mode_always_zero(tmp_path: Path) -> None:
    corpus = tmp_path / "c"
    corpus.mkdir()
    (corpus / "a.contract.yaml").write_text(
        "kind: totally_fake_kind\nstatus: active\n", encoding="utf-8"
    )
    _, code = run(
        vocab_path=_vocab(tmp_path),
        corpus_root=corpus,
        mode="report",
    )
    assert code == 0


def test_no_autogen() -> None:
    import omega_engine_governance.contracts.c3s1_vocab_refuse as m

    assert not hasattr(m, "auto_write_empty_contracts")
    assert not hasattr(m, "rewrite_corpus")


