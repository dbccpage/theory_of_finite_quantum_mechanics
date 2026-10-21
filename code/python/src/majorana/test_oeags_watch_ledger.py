from __future__ import annotations
"""OEAGS-S2: watch residual ledger + interval runner tests."""


import json
from pathlib import Path


from omega_engine_governance.contracts.oeags_bijection_residual import ResidualRow
from omega_engine_governance.contracts.oeags_watch_ledger import (
    append_rows,
    collect_from_c2s4_ndjson,
    collect_from_c3s3_index,
    main,
    run_interval,
    run_tick,
)


def test_append_only_dedupes(tmp_path: Path) -> None:
    ledger = tmp_path / "watch.ndjson"
    rows = [
        ResidualRow(
            code="DEV-PARITY-STUB",
            disposition="OPEN",
            detail="x",
            path="p",
            source="t",
        )
    ]
    assert append_rows(ledger, rows) == 1
    assert append_rows(ledger, rows) == 0
    lines = [ln for ln in ledger.read_text(encoding="utf-8").splitlines() if ln]
    assert len(lines) == 1
    d = json.loads(lines[0])
    assert d["code"] == "DEV-PARITY-STUB"
    assert d["authority_effect"] == "None"
    assert "watched_at" in d


def test_collect_c2s4(tmp_path: Path) -> None:
    p = tmp_path / "c2s4.ndjson"
    p.write_text(
        json.dumps(
            {
                "code": "DEV-PARITY-STUB",
                "disposition": "OPEN",
                "detail": "stub",
                "path": "x",
                "source": "c2s4",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    rows = collect_from_c2s4_ndjson(p)
    assert len(rows) == 1
    assert rows[0].code == "DEV-PARITY-STUB"


def test_collect_c3s3_missing_index(tmp_path: Path) -> None:
    rows = collect_from_c3s3_index(tmp_path / "nope.json")
    assert len(rows) == 1
    assert rows[0].code == "DEV-CORPUS"


def test_collect_c3s3_admitted_ok(tmp_path: Path) -> None:
    p = tmp_path / "idx.json"
    p.write_text(
        json.dumps({"entries": {"math/a.contract.yaml": "admitted"}}),
        encoding="utf-8",
    )
    assert collect_from_c3s3_index(p) == []


def test_run_tick_appends(tmp_path: Path) -> None:
    ledger = tmp_path / "w.ndjson"
    c2 = tmp_path / "c2.ndjson"
    c2.write_text(
        json.dumps(
            {
                "code": "DEV-UNCONTRACTED",
                "disposition": "OPEN",
                "detail": "gap",
                "path": "c::m",
                "source": "c2s4",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    c3 = tmp_path / "c3.json"
    c3.write_text(
        json.dumps({"entries": {"math/x.contract.yaml": "admitted"}}),
        encoding="utf-8",
    )
    rep = run_tick(
        tick=1,
        ledger_path=ledger,
        include_bijection=False,
        include_c2s4=True,
        include_c3s3=True,
        c2s4_path=c2,
        c3s3_path=c3,
    )
    assert rep.authority_effect == "None"
    assert rep.rows_appended >= 1
    assert ledger.is_file()


def test_interval_two_ticks_second_zero_append(tmp_path: Path) -> None:
    ledger = tmp_path / "w.ndjson"
    c2 = tmp_path / "c2.ndjson"
    c2.write_text(
        json.dumps(
            {
                "code": "DEV-PARITY-STUB",
                "disposition": "OPEN",
                "detail": "s",
                "path": "",
                "source": "c2s4",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    reps = run_interval(
        interval_s=0.0,
        max_ticks=2,
        ledger_path=ledger,
        include_bijection=False,
        include_c2s4=True,
        include_c3s3=False,
        c2s4_path=c2,
    )
    assert len(reps) == 2
    assert reps[0].rows_appended == 1
    assert reps[1].rows_appended == 0


def test_main_tick_exit_0(tmp_path: Path) -> None:
    ledger = tmp_path / "w.ndjson"
    report = tmp_path / "r.txt"
    c2 = tmp_path / "c2.ndjson"
    c2.write_text("\n", encoding="utf-8")
    c3 = tmp_path / "c3.json"
    c3.write_text(
        json.dumps({"entries": {"math/a.contract.yaml": "admitted"}}),
        encoding="utf-8",
    )
    code = main(
        [
            "--mode",
            "tick",
            "--ledger",
            str(ledger),
            "--report",
            str(report),
            "--no-bijection",
            "--c2s4",
            str(c2),
            "--c3s3-index",
            str(c3),
        ]
    )
    assert code == 0
    assert report.is_file()
    assert "AuthorityEffect" in report.read_text(
        encoding="utf-8"
    ) or "authority_effect" in report.read_text(encoding="utf-8")


def test_no_autogen_contracts_api() -> None:
    import omega_engine_governance.contracts.oeags_watch_ledger as m

    assert not hasattr(m, "auto_write_empty_contracts")
    assert not hasattr(m, "git_commit")


