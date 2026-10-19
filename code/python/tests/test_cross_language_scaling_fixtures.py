"""Cross-language JSON fixture serialization tests comparing exact rational (Q) and F_2 outputs
of benchmark_fock_lattice_scaling, benchmark_hubbard_lattice_scaling, and
benchmark_tetron_lattice_scaling bit-for-bit between Rust (tfqm_fsp, tfqm_majorana) and
Python (code/python/src/fsp/, code/python/src/majorana/).

AuthorityEffect: None.
"""

from __future__ import annotations

from fractions import Fraction
import hashlib
import json
from pathlib import Path
import pytest

from src.fsp import (
    FockLatticeScalingRow,
    HubbardLatticeScalingRow,
    benchmark_fock_lattice_scaling,
    benchmark_hubbard_lattice_scaling,
    fock_scaling_from_canonical_json,
    fock_scaling_to_canonical_json,
    hubbard_scaling_from_canonical_json,
    hubbard_scaling_to_canonical_json,
)
from src.majorana import (
    MAX_WIRE_SITES,
    GF2ScheduleStatus,
    KitaevWireScalingReceipt,
    MultiQubitBraidScalingRow,
    PacketWallTerminal,
    PauliNoiseScalingRow,
    ResidualPacketWallReceipt,
    Terminal,
    TetronScalingRow,
    Topology,
    benchmark_classify_residual,
    benchmark_multiqubit_braid_scaling,
    benchmark_pauli_noise_scaling,
    benchmark_sparse_kitaev_scaling,
    benchmark_tetron_lattice_scaling,
    classify_residual_from_canonical_json,
    classify_residual_to_canonical_json,
    multiqubit_braid_scaling_from_canonical_json,
    multiqubit_braid_scaling_to_canonical_json,
    pauli_noise_scaling_from_canonical_json,
    pauli_noise_scaling_to_canonical_json,
    sparse_kitaev_scaling_from_canonical_json,
    sparse_kitaev_scaling_to_canonical_json,
    tetron_scaling_from_canonical_json,
    tetron_scaling_to_canonical_json,
)

REPO_ROOT = Path(__file__).resolve().parents[3]
FOCK_FIXTURE_PATH = REPO_ROOT / "code" / "rust" / "src" / "fsp" / "fixtures" / "fock_lattice_scaling.json"
HUBBARD_FIXTURE_PATH = REPO_ROOT / "code" / "rust" / "src" / "fsp" / "fixtures" / "hubbard_lattice_scaling.json"
TETRON_FIXTURE_PATH = REPO_ROOT / "code" / "rust" / "src" / "majorana" / "fixtures" / "tetron_lattice_scaling.json"
MULTIQUBIT_BRAID_FIXTURE_PATH = (
    REPO_ROOT / "code" / "rust" / "src" / "majorana" / "fixtures" / "multiqubit_braid_scaling.json"
)
SPARSE_KITAEV_FIXTURE_PATH = (
    REPO_ROOT / "code" / "rust" / "src" / "majorana" / "fixtures" / "sparse_kitaev_scaling.json"
)
CLASSIFY_RESIDUAL_FIXTURE_PATH = (
    REPO_ROOT / "code" / "rust" / "src" / "majorana" / "fixtures" / "classify_residual.json"
)
PAULI_NOISE_FIXTURE_PATH = (
    REPO_ROOT / "code" / "rust" / "src" / "majorana" / "fixtures" / "pauli_noise_scaling.json"
)


def _read_lf_bytes(path: Path) -> bytes:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n").encode("utf-8")


def test_fock_lattice_scaling_matches_rust_json_fixture_bit_for_bit() -> None:
    """Compare exact rational outputs of benchmark_fock_lattice_scaling bit-for-bit against the Rust JSON fixture."""
    assert FOCK_FIXTURE_PATH.is_file(), f"Missing fixture: {FOCK_FIXTURE_PATH}"

    rows = benchmark_fock_lattice_scaling(beta=Fraction(2), trotter_steps=3)
    assert len(rows) == 9

    py_json = fock_scaling_to_canonical_json(rows)
    py_bytes = py_json.encode("utf-8")
    fixture_bytes = _read_lf_bytes(FOCK_FIXTURE_PATH)

    assert py_bytes == fixture_bytes, "Python benchmark_fock_lattice_scaling JSON bytes differed from Rust fixture"
    assert hashlib.sha256(py_bytes).hexdigest() == hashlib.sha256(fixture_bytes).hexdigest()

    deserialized = fock_scaling_from_canonical_json(fixture_bytes.decode("utf-8"))
    assert deserialized == rows

    # Verify exact rational invariants on frustrated vs bipartite lattices
    by_label = {row.label: row for row in rows}
    assert by_label["triangle_3"].z_fermionic == Fraction(83, 9)
    assert by_label["triangle_3"].z_bosonic == Fraction(115, 9)
    assert by_label["triangle_3"].average_sign == Fraction(83, 115)
    assert by_label["triangle_3"].has_sign_cancellation is True

    assert by_label["ladder_2x3_rect"].fock_dim == 90
    assert by_label["ladder_2x3_rect"].z_fermionic == Fraction(1390, 3)
    assert by_label["ladder_2x3_rect"].z_bosonic == Fraction(1882, 3)
    assert by_label["ladder_2x3_rect"].average_sign == Fraction(695, 941)
    assert by_label["ladder_2x3_rect"].has_sign_cancellation is True

    assert by_label["triangular_ladder_8"].num_sites == 8
    assert by_label["triangular_ladder_8"].fock_dim == 28
    assert by_label["triangular_ladder_8"].z_fermionic == Fraction(836, 3)
    assert by_label["triangular_ladder_8"].z_bosonic == Fraction(300, 1)
    assert by_label["triangular_ladder_8"].average_sign == Fraction(209, 225)
    assert by_label["triangular_ladder_8"].has_sign_cancellation is True

    for bipartite_label in ("square_4", "chain_6_open", "grid_2x4_rect"):
        assert by_label[bipartite_label].average_sign == Fraction(1)
        assert by_label[bipartite_label].has_sign_cancellation is False


def test_hubbard_lattice_scaling_matches_rust_json_fixture_bit_for_bit() -> None:
    """Compare exact rational outputs of benchmark_hubbard_lattice_scaling bit-for-bit against the Rust JSON fixture."""
    assert HUBBARD_FIXTURE_PATH.is_file(), f"Missing fixture: {HUBBARD_FIXTURE_PATH}"

    rows = benchmark_hubbard_lattice_scaling()
    assert len(rows) == 8

    py_json = hubbard_scaling_to_canonical_json(rows)
    py_bytes = py_json.encode("utf-8")
    fixture_bytes = _read_lf_bytes(HUBBARD_FIXTURE_PATH)

    assert py_bytes == fixture_bytes, "Python benchmark_hubbard_lattice_scaling JSON bytes differed from Rust fixture"
    assert hashlib.sha256(py_bytes).hexdigest() == hashlib.sha256(fixture_bytes).hexdigest()

    deserialized = hubbard_scaling_from_canonical_json(fixture_bytes.decode("utf-8"))
    assert deserialized == rows

    expected_sites = [4, 6, 8, 9, 10, 12, 6, 9]
    for idx, row in enumerate(rows):
        assert row.sites == expected_sites[idx]
        assert row.evaluated_fields == 6
        if row.attractive:
            assert row.negative_fields_count == 0
            assert row.attractive_square_root_protected is True
            assert row.average_sign == Fraction(1)
        else:
            assert row.attractive_square_root_protected is False
            assert row.average_sign <= Fraction(1)


def test_tetron_lattice_scaling_matches_rust_json_fixture_bit_for_bit() -> None:
    """Compare F_2 cohomological outputs of benchmark_tetron_lattice_scaling bit-for-bit against the Rust JSON fixture."""
    assert TETRON_FIXTURE_PATH.is_file(), f"Missing fixture: {TETRON_FIXTURE_PATH}"

    sizes = [(2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (6, 8), (8, 8)]
    topologies = [Topology.Disk, Topology.Cylinder, Topology.Torus]
    rows = benchmark_tetron_lattice_scaling(sizes, topologies)
    assert len(rows) == 21

    py_json = tetron_scaling_to_canonical_json(rows)
    py_bytes = py_json.encode("utf-8")
    fixture_bytes = _read_lf_bytes(TETRON_FIXTURE_PATH)

    assert py_bytes == fixture_bytes, "Python benchmark_tetron_lattice_scaling JSON bytes differed from Rust fixture"
    assert hashlib.sha256(py_bytes).hexdigest() == hashlib.sha256(fixture_bytes).hexdigest()

    deserialized = tetron_scaling_from_canonical_json(fixture_bytes.decode("utf-8"))
    assert deserialized == rows

    for row in rows:
        assert row.boundary_exact is True
        assert row.euler_agrees is True
        assert row.generators_closed is True
        assert row.dim_h1 == row.expected_dim_h1
        assert row.num_islands == row.rows * row.cols

    torus_8x8 = [r for r in rows if r.topology == Topology.Torus and r.rows == 8 and r.cols == 8][0]
    assert (
        torus_8x8.num_mzm,
        torus_8x8.num_channels,
        torus_8x8.num_islands,
        torus_8x8.rank_d0,
        torus_8x8.rank_d1,
        torus_8x8.dim_h1,
    ) == (64, 128, 64, 63, 63, 2)


def test_multiqubit_braid_scaling_matches_rust_json_fixture_bit_for_bit() -> None:
    """Compare multi-qubit braid word compiler outputs bit-for-bit against the Rust JSON fixture."""
    assert MULTIQUBIT_BRAID_FIXTURE_PATH.is_file(), f"Missing fixture: {MULTIQUBIT_BRAID_FIXTURE_PATH}"

    counts = [2, 4, 8, 12, 16]
    rows = benchmark_multiqubit_braid_scaling(counts)
    assert len(rows) == 5

    py_json = multiqubit_braid_scaling_to_canonical_json(rows)
    py_bytes = py_json.encode("utf-8")
    fixture_bytes = _read_lf_bytes(MULTIQUBIT_BRAID_FIXTURE_PATH)

    assert (
        py_bytes == fixture_bytes
    ), "Python benchmark_multiqubit_braid_scaling JSON bytes differed from Rust fixture"
    assert hashlib.sha256(py_bytes).hexdigest() == hashlib.sha256(fixture_bytes).hexdigest()

    deserialized = multiqubit_braid_scaling_from_canonical_json(fixture_bytes.decode("utf-8"))
    assert deserialized == rows

    for nq, row in zip(counts, rows):
        assert row.num_qubits == nq
        assert row.mode_count == 4 * nq
        assert row.cnot_steps == 32 * (nq - 2) + 1
        assert row.determinant_sign == 1
        assert row.inverse_restores_identity is True


def test_sparse_kitaev_scaling_matches_rust_json_fixture_bit_for_bit() -> None:
    """Compare sparse Kitaev wire boundary isolation outputs bit-for-bit against the Rust JSON fixture."""
    assert SPARSE_KITAEV_FIXTURE_PATH.is_file(), f"Missing fixture: {SPARSE_KITAEV_FIXTURE_PATH}"

    site_counts = [16, 64, 256, 1024, 4096, 16384, MAX_WIRE_SITES]
    rows = benchmark_sparse_kitaev_scaling(site_counts)
    assert len(rows) == 7

    py_json = sparse_kitaev_scaling_to_canonical_json(rows)
    py_bytes = py_json.encode("utf-8")
    fixture_bytes = _read_lf_bytes(SPARSE_KITAEV_FIXTURE_PATH)

    assert (
        py_bytes == fixture_bytes
    ), "Python benchmark_sparse_kitaev_scaling JSON bytes differed from Rust fixture"
    assert hashlib.sha256(py_bytes).hexdigest() == hashlib.sha256(fixture_bytes).hexdigest()

    deserialized = sparse_kitaev_scaling_from_canonical_json(fixture_bytes.decode("utf-8"))
    assert deserialized == rows

    for sites, row in zip(site_counts, rows):
        assert row.sites == sites
        assert row.mode_count == 2 * sites
        assert row.bilinear_terms == sites - 1
        assert row.boundary_modes == (1, 2 * sites)
        assert row.isolated_count == 2
        assert row.endpoints_isolated is True
        assert row.is_sweet_spot is True


def test_classify_residual_matches_rust_json_fixture_bit_for_bit() -> None:
    """Compare Exact-vs-LGGR-vs-Open cochain packet wall classifier outputs bit-for-bit against the Rust JSON fixture."""
    assert CLASSIFY_RESIDUAL_FIXTURE_PATH.is_file(), f"Missing fixture: {CLASSIFY_RESIDUAL_FIXTURE_PATH}"

    rows = benchmark_classify_residual()
    assert len(rows) == 14

    py_json = classify_residual_to_canonical_json(rows)
    py_bytes = py_json.encode("utf-8")
    fixture_bytes = _read_lf_bytes(CLASSIFY_RESIDUAL_FIXTURE_PATH)

    assert (
        py_bytes == fixture_bytes
    ), "Python benchmark_classify_residual JSON bytes differed from Rust fixture"
    assert hashlib.sha256(py_bytes).hexdigest() == hashlib.sha256(fixture_bytes).hexdigest()

    deserialized = classify_residual_from_canonical_json(fixture_bytes.decode("utf-8"))
    assert deserialized == rows

    by_label = {row.label: row for row in rows}
    assert by_label["triangle_exact"].classified.terminal == Terminal.Exact
    assert by_label["triangle_exact"].schedule_status == GF2ScheduleStatus.Exact
    assert by_label["triangle_exact"].packet_wall.terminal == PacketWallTerminal.Exact
    assert by_label["triangle_open"].classified.terminal == Terminal.OpenObstruction
    assert by_label["triangle_open"].schedule_status == GF2ScheduleStatus.OpenObstruction
    assert by_label["torus_2x2_logical_x_lggr"].is_lggr is True
    assert by_label["torus_2x2_logical_x_lggr"].classified.terminal == Terminal.TypedHarmonic
    assert by_label["torus_2x2_logical_x_capacity_wall"].packet_wall.terminal == PacketWallTerminal.CapacityWallHit
    assert by_label["tetron_torus_3x3_logical_col_capped_budget"].classified.terminal == Terminal.ClosedResidual
    assert by_label["invalid_broken_boundary_refusal"].classified.terminal == Terminal.RepresentationInvalid
    assert by_label["invalid_broken_boundary_refusal"].packet_wall.terminal == PacketWallTerminal.IncompleteRefusal


def test_pauli_noise_scaling_matches_rust_json_fixture_bit_for_bit() -> None:
    """Compare exact rational correlated Pauli noise threshold evaluator outputs bit-for-bit against the Rust JSON fixture."""
    assert PAULI_NOISE_FIXTURE_PATH.is_file(), f"Missing fixture: {PAULI_NOISE_FIXTURE_PATH}"

    counts = [2, 4, 8, 12, 16]
    rows = benchmark_pauli_noise_scaling(counts)
    assert len(rows) == 5

    py_json = pauli_noise_scaling_to_canonical_json(rows)
    py_bytes = py_json.encode("utf-8")
    fixture_bytes = _read_lf_bytes(PAULI_NOISE_FIXTURE_PATH)

    assert (
        py_bytes == fixture_bytes
    ), "Python benchmark_pauli_noise_scaling JSON bytes differed from Rust fixture"
    assert hashlib.sha256(py_bytes).hexdigest() == hashlib.sha256(fixture_bytes).hexdigest()

    deserialized = pauli_noise_scaling_from_canonical_json(fixture_bytes.decode("utf-8"))
    assert deserialized == rows

    for nq, row in zip(counts, rows):
        assert row.num_qubits == nq
        assert row.mode_count == 4 * nq
        assert row.coupling_count == (4 * nq) * (4 * nq - 1) // 2
        assert row.tight_accepted is False
        assert row.tight_status == "REFUSAL_NOISE_LEAKAGE"
        assert row.boundary_accepted is True
        assert row.boundary_status == "ACCEPTED_STABLE"
        assert row.leakage_preserved is True
        assert row.inverse_restores_noise is True


def test_cross_language_json_fixture_tamper_detection() -> None:
    """Verify that any single-bit or rational-field mutation in deserialized JSON is rejected by equality."""
    fock_text = _read_lf_bytes(FOCK_FIXTURE_PATH).decode("utf-8")
    fock_rows = fock_scaling_from_canonical_json(fock_text)
    tampered_fock_payload = json.loads(fock_text)
    tampered_fock_payload[0]["average_sign"] = "84/115"
    tampered_fock_rows = fock_scaling_from_canonical_json(json.dumps(tampered_fock_payload))
    assert tampered_fock_rows != fock_rows

    tetron_text = _read_lf_bytes(TETRON_FIXTURE_PATH).decode("utf-8")
    tetron_rows = tetron_scaling_from_canonical_json(tetron_text)
    tampered_tetron_payload = json.loads(tetron_text)
    tampered_tetron_payload[-1]["dim_h1"] = 1
    tampered_tetron_rows = tetron_scaling_from_canonical_json(json.dumps(tampered_tetron_payload))
    assert tampered_tetron_rows != tetron_rows

    braid_text = _read_lf_bytes(MULTIQUBIT_BRAID_FIXTURE_PATH).decode("utf-8")
    braid_rows = multiqubit_braid_scaling_from_canonical_json(braid_text)
    tampered_braid_payload = json.loads(braid_text)
    tampered_braid_payload[-1]["cnot_steps"] = 450
    tampered_braid_rows = multiqubit_braid_scaling_from_canonical_json(json.dumps(tampered_braid_payload))
    assert tampered_braid_rows != braid_rows

    kitaev_text = _read_lf_bytes(SPARSE_KITAEV_FIXTURE_PATH).decode("utf-8")
    kitaev_rows = sparse_kitaev_scaling_from_canonical_json(kitaev_text)
    tampered_kitaev_payload = json.loads(kitaev_text)
    tampered_kitaev_payload[-1]["endpoints_isolated"] = False
    tampered_kitaev_rows = sparse_kitaev_scaling_from_canonical_json(json.dumps(tampered_kitaev_payload))
    assert tampered_kitaev_rows != kitaev_rows

    classify_text = _read_lf_bytes(CLASSIFY_RESIDUAL_FIXTURE_PATH).decode("utf-8")
    classify_rows = classify_residual_from_canonical_json(classify_text)
    tampered_classify_payload = json.loads(classify_text)
    tampered_classify_payload[5]["is_lggr"] = False
    tampered_classify_rows = classify_residual_from_canonical_json(json.dumps(tampered_classify_payload))
    assert tampered_classify_rows != classify_rows

    pauli_text = _read_lf_bytes(PAULI_NOISE_FIXTURE_PATH).decode("utf-8")
    pauli_rows = pauli_noise_scaling_from_canonical_json(pauli_text)
    tampered_pauli_payload = json.loads(pauli_text)
    tampered_pauli_payload[0]["circuit_noise_defect"] = "401/3115"
    tampered_pauli_rows = pauli_noise_scaling_from_canonical_json(json.dumps(tampered_pauli_payload))
    assert tampered_pauli_rows != pauli_rows


