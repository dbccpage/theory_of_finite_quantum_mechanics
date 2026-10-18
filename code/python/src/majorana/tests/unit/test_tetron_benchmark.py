from __future__ import annotations

"""Invariants for the tetron homology benchmark and its certificate ledger.

The census reports an *analytic* count -- ``2 ** rank d0`` residuals per class
-- rather than enumerating ``ker d1``. That shortcut is only legitimate if it
agrees with brute force, which is what the first test checks.
"""


from collections import Counter

import pytest

from omega_engine.crates.majorana.carriers.surface_carrier import build_tetron_array
from omega_engine.crates.majorana.certificates.ledger import (
    verify_classified_ledger,
    write_classified_ledger,
)
from omega_engine.crates.majorana.core.gf2_matrix import GF2Matrix
from omega_engine.crates.majorana.demos.tetron_homology_benchmark import (
    _dense_hilbert_baseline,
    census_closed_exhaustive,
    census_iid_noise,
    ledger_rows,
    structure_row,
    timing_row,
)
from omega_engine.crates.majorana.engines.classifier import classify
from omega_engine.crates.majorana.engines.harmonic import DEFAULT_BUDGET




@pytest.mark.parametrize(
    "topology,rows,cols",
    [("disk", 2, 2), ("cylinder", 2, 2), ("torus", 2, 2), ("torus", 2, 3)],
)
def test_analytic_census_matches_brute_force(topology: str, rows: int, cols: int) -> None:
    carrier, report = build_tetron_array(rows, cols, topology)
    kernel = GF2Matrix(carrier.D1, cols=report.num_channels).kernel_basis()

    brute: Counter[str] = Counter()
    for code in range(1 << len(kernel)):
        residual = [0] * report.num_channels
        for index, vector in enumerate(kernel):
            if (code >> index) & 1:
                residual = [a ^ b for a, b in zip(residual, vector)]
        brute[classify(carrier.D0, carrier.D1, residual)["terminal_status"]] += 1

    analytic = census_closed_exhaustive(topology, rows, cols, DEFAULT_BUDGET)
    assert analytic["terminals"] == dict(brute)
    assert analytic["num_closed_residuals"] == (1 << len(kernel))
    assert sum(analytic["terminals"].values()) == (1 << len(kernel))


def test_census_class_count_is_two_to_the_betti_number() -> None:
    for topology, expected in (("disk", 0), ("cylinder", 1), ("torus", 2)):
        row = census_closed_exhaustive(topology, 3, 3, DEFAULT_BUDGET)
        assert row["dim_h1"] == expected
        assert len(row["classes"]) == 2 ** expected
        assert row["residuals_per_class"] * len(row["classes"]) == (
            row["num_closed_residuals"]
        )


def test_only_the_zero_class_is_exact() -> None:
    row = census_closed_exhaustive("torus", 3, 3, DEFAULT_BUDGET)
    exact = [c for c in row["classes"] if c["terminal_status"] == "Exact"]
    typed = [c for c in row["classes"] if c["terminal_status"] == "TypedHarmonic"]
    assert len(exact) == 1 and exact[0]["class_id"] == "h1:00"
    assert len(typed) == 3
    assert all(c["phi1_weight"] >= 3 for c in typed)




def test_iid_noise_is_dominated_by_open_obstructions() -> None:
    """Local island checks fire: that is what makes the code useful."""
    row = census_iid_noise("torus", 3, 3, rate=0.10, trials=200, seed=1, budget=1 << 16)
    assert row["terminals"].get("OpenObstruction", 0) > 0.5 * row["trials"]
    assert set(row["terminals"]) <= {
        "Exact",
        "OpenObstruction",
        "ClosedResidual",
        "TypedHarmonic",
    }


def test_zero_noise_is_all_exact() -> None:
    row = census_iid_noise("torus", 3, 3, rate=0.0, trials=20, seed=1, budget=1 << 16)
    assert row["terminals"] == {"Exact": 20}




@pytest.mark.parametrize("topology,expected", [("disk", 0), ("cylinder", 1), ("torus", 2)])
def test_structure_row_reports_measured_homology(topology: str, expected: int) -> None:
    row = structure_row(topology, 3, 3, DEFAULT_BUDGET)
    _, report = build_tetron_array(3, 3, topology)
    assert row["dim_h1"] == expected == report.dim_h1
    assert row["homology_matches_prediction"] is True
    assert row["hilbert_dim"] == 2 ** (report.num_mzm // 2)
    assert row["coset_size"] == 2 ** report.rank_d0


def test_structure_reports_code_distance_only_when_one_exists() -> None:
    assert structure_row("disk", 3, 3, DEFAULT_BUDGET)["code_distance"] is None
    assert structure_row("torus", 3, 4, DEFAULT_BUDGET)["code_distance"] == 3
    assert structure_row("cylinder", 3, 4, DEFAULT_BUDGET)["code_distance"] == 4




def test_dense_baseline_refuses_infeasible_dimensions() -> None:
    result = _dense_hilbert_baseline(262144, max_dim=2048)
    assert result["ran"] is False
    assert result["ms"] is None
    assert "GiB" in result["reason"]


def test_dense_baseline_runs_below_the_cap() -> None:
    result = _dense_hilbert_baseline(64, max_dim=2048)
    assert result["ran"] is True
    assert result["ms"] is not None and result["ms"] > 0


def test_timing_row_separates_the_two_costs() -> None:
    row = timing_row("torus", 3, 3, trials=5, seed=1, budget=1 << 16, max_dense_dim=64)
    assert row["split_ms_per_residual"] > 0
    assert row["phi1_ms_per_residual"] > 0
    assert row["dim_h1"] == 2
    assert row["authority_effect"] == "None"




def test_ledger_rows_cover_every_terminal_and_replay(tmp_path) -> None:
    rows = ledger_rows(budget=1 << 14)
    statuses = {row["terminal_status"] for row in rows}
    assert statuses == {
        "Exact",
        "OpenObstruction",
        "ClosedResidual",
        "TypedHarmonic",
    }
    assert all(row["authority_effect"] == "None" for row in rows)

    path = tmp_path / "classified.jsonl"
    write_classified_ledger(path, rows)
    verification = verify_classified_ledger(path)
    assert verification["checked"] == len(rows)
    assert verification["verified"], verification["failures"][:3]


def test_ledger_replay_detects_a_tampered_terminal(tmp_path) -> None:
    """A ledger that cannot fail is not a ledger."""
    rows = ledger_rows(budget=1 << 14)
    tampered = [dict(row) for row in rows]
    target = next(r for r in tampered if r["terminal_status"] == "TypedHarmonic")
    target["terminal_status"] = "Exact"

    path = tmp_path / "tampered.jsonl"
    write_classified_ledger(path, tampered)
    verification = verify_classified_ledger(path)
    assert not verification["verified"]
    assert any(f["field"] == "terminal_status" for f in verification["failures"])


def test_ledger_replay_detects_a_tampered_phi1_weight(tmp_path) -> None:
    rows = ledger_rows(budget=1 << 14)
    tampered = [dict(row) for row in rows]
    target = next(r for r in tampered if r["terminal_status"] == "TypedHarmonic")
    target["phi1_weight"] = 1

    path = tmp_path / "tampered2.jsonl"
    write_classified_ledger(path, tampered)
    verification = verify_classified_ledger(path)
    assert not verification["verified"]
    assert any(f["field"] == "phi1_weight" for f in verification["failures"])


def test_budget_is_part_of_the_replayed_input(tmp_path) -> None:
    """The same carrier under a smaller budget is a different, valid row."""
    rows = ledger_rows(budget=1 << 14)
    capped = [r for r in rows if r["instance"].endswith("logical_string_capped")]
    full = [r for r in rows if r["instance"].endswith("/ logical_string")]
    assert capped and full
    assert capped[0]["terminal_status"] == "ClosedResidual"
    assert full[0]["terminal_status"] == "TypedHarmonic"
    assert capped[0]["residual"] == full[0]["residual"]
    assert capped[0]["replay_hash"] != full[0]["replay_hash"]



