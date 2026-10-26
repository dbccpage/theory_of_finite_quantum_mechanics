"""
Tests for Relational Algebra & Database Theory Domain Kernel
AuthorityEffect: None
"""

import sqlite3
import sys
from pathlib import Path

# Add domain code directory to sys.path
_code_dir = Path(__file__).resolve().parent.parent / "code"
if str(_code_dir) not in sys.path:
    sys.path.insert(0, str(_code_dir))

import pytest
from domain_ansi_sql_kernel import (
    DomainEngine,
    SimplicialBoundaryReceipt,
    compute_mertens,
)


def test_initial_void_to_root():
    engine = DomainEngine()
    assert engine.state.step == 0
    assert engine.step_01_admit_root("<>")
    assert engine.state.step == 1
    assert "<>" in engine.state.carrier
    assert "branch_root_single" in engine.state.branches_retained


def test_germ_creation_and_witness():
    engine = DomainEngine()
    engine.step_01_admit_root("<>")
    assert engine.step_02_admit_germ("pt_alpha", "pt_beta")
    assert engine.state.step == 2
    assert ("pt_alpha", "pt_beta") in engine.state.relations


def test_irreflexive_enforcement_and_distinctness():
    engine = DomainEngine()
    engine.step_01_admit_root("<>")
    engine.step_02_admit_germ("pt_alpha", "pt_beta")
    # inject reflexive defect
    engine.state.relations.add(("pt_alpha", "pt_alpha"))
    assert not engine.setting.is_irrefl()

    # Discharge obstruction
    assert engine.step_03_enforce_irrefl()
    assert engine.setting.is_irrefl()
    assert engine.setting.is_distinct()


def test_boundary_closure_invariant():
    engine = DomainEngine()
    engine.step_01_admit_root("<>")
    engine.step_02_admit_germ("pt_alpha", "pt_beta")
    engine.step_03_enforce_irrefl()
    receipt = engine.evaluate_boundary_closure()
    assert isinstance(receipt, SimplicialBoundaryReceipt)
    assert receipt.is_nilpotent
    assert bool(receipt) is True


def test_explicit_recovery_gap_detection():
    engine = DomainEngine()
    gap_info = engine.check_gap_obstruction()
    assert gap_info["gap_id"] == "ThreeValuedNullObstruction"
    assert gap_info["status"] == "UNBRIDGED_OBSTRUCTION"
    assert engine.gap_detected


def test_step_01_through_16_complete_progression():
    """Verifies all 16 steps of the Genesis Domain ANSI SQL scenario progression."""
    engine = DomainEngine()

    assert engine.step_01_admit_root("<>")
    assert engine.state.step == 1

    assert engine.step_02_admit_germ("a", "b")
    assert engine.state.step == 2

    assert engine.step_03_enforce_irrefl()
    assert engine.state.step == 3

    assert engine.step_04_admit_orientation()
    assert engine.state.step == 4
    assert set(engine.state.branches_retained) == {"branch_D2", "branch_S2"}

    assert engine.step_05_admit_transposition()
    assert engine.state.step == 5
    assert engine.state.invariants["transposition_sign_inversion"] is True

    assert engine.step_06_instantiate_relational_schema()
    assert engine.state.step == 6

    receipt = engine.step_07_evaluate_boundary_closure()
    assert engine.state.step == 7
    assert receipt.is_nilpotent

    assert engine.step_08_synthesize_relational_poset()
    assert engine.state.step == 8

    assert engine.step_09_resolve_parity()
    assert engine.state.step == 9

    assert engine.step_10_admit_higher_complexes()
    assert engine.state.step == 10

    assert engine.step_11_enforce_conservation()
    assert engine.state.step == 11

    assert engine.step_12_quotient_observer_interface()
    assert engine.state.step == 12

    assert engine.step_13_prune_fuel_bounded_branches()
    assert engine.state.step == 13

    assert engine.step_14_establish_frontier()
    assert engine.state.step == 14

    gap = engine.step_15_isolate_gap_obstruction()
    assert engine.state.step == 15
    assert gap["gap_id"] == "ThreeValuedNullObstruction"

    cert = engine.step_16_terminal_certification()
    assert engine.state.step == 16
    assert cert["status"] == "CERTIFIED"
    assert cert["steps_completed"] == 16
    assert cert["authority_effect"] == "None"


def test_root_w_relational_schema_sql_views():
    """Validates Root W DDL, check constraints, and boundary views in SQLite."""
    engine = DomainEngine()
    result = engine.verify_root_w_sql_schema()
    assert result["check_constraint_verified"] is True
    assert result["transposition_verified"] is True
    assert result["sign_inversion_verified"] is True


def test_bareiss_exact_integer_determinants():
    """Validates Bareiss fraction-free determinant on identity, diagonal, and singular matrices."""
    engine = DomainEngine()

    # 1. Identity 3x3
    I3 = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    r_i3 = engine.compute_bareiss_determinant(I3)
    assert r_i3.determinant == 1
    assert r_i3.is_exact_integer

    # 2. Diagonal with negative entry
    diag = [[2, 0, 0], [0, 3, 0], [0, 0, -5]]
    r_diag = engine.compute_bareiss_determinant(diag)
    assert r_diag.determinant == -30

    # 3. Singular matrix with linearly dependent rows
    sing = [[1, 2, 3], [4, 5, 6], [5, 7, 9]]  # Row 3 = Row 1 + Row 2
    r_sing = engine.compute_bareiss_determinant(sing)
    assert r_sing.determinant == 0

    # 4. 4x4 matrix with row swaps
    M4 = [[0, 1, 2, 0], [3, 0, 0, 4], [0, 5, 6, 0], [7, 0, 0, 8]]
    # det = -16 by Laplace expansion: (-1)*1*(-24) + (+1)*2*(-20) = 24 - 40 = -16.
    r_m4 = engine.compute_bareiss_determinant(M4)
    assert r_m4.determinant == -16


def test_redheffer_mertens_benchmark_1_through_10():
    """
    Validates Redheffer's theorem det(R_n) = M(n) for n = 1 to 10
    using exact integer Bareiss determinant.
    """
    engine = DomainEngine()
    expected_mertens = {
        1: 1,
        2: 0,
        3: -1,
        4: -1,
        5: -2,
        6: -1,
        7: -2,
        8: -2,
        9: -2,
        10: -1,
    }

    for n, expected_m in expected_mertens.items():
        assert compute_mertens(n) == expected_m
        receipt = engine.verify_redheffer_benchmark(n)
        assert receipt.is_benchmark_verified is True
        assert receipt.bareiss_determinant == expected_m
        assert receipt.mertens_m_n == expected_m


def test_fermion_gin_index_sign_resolution():
    """
    Validates GIN index inverted posting list pairing for fermion sign cancellation in SQL.
    """
    engine = DomainEngine()
    receipt = engine.evaluate_fermion_gin_resolution(num_pairs=6)

    assert receipt.num_configurations == 12
    assert receipt.num_involution_pairs == 6
    assert receipt.exact_cancellation_verified is True
    assert receipt.average_sign == 1.0


def test_negative_controls_sql_and_bareiss():
    """Negative controls: non-square matrix, negative Redheffer size, and SQL check constraint."""
    engine = DomainEngine()

    # Non-square matrix
    with pytest.raises(ValueError, match="Matrix must be square"):
        engine.compute_bareiss_determinant([[1, 2, 3], [4, 5, 6]])

    # Invalid Redheffer dimension
    with pytest.raises(ValueError, match="must be >= 1"):
        engine.verify_redheffer_benchmark(0)

    # SQLite CHECK constraint blocks reflexive edge
    conn = sqlite3.connect(":memory:")
    sql_path = (
        Path(__file__).resolve().parent.parent / "code" / "queries" / "root_w_relational_schema.sql"
    )
    with open(sql_path, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.execute("INSERT INTO carrier_elements (element_id, admitted_step) VALUES ('v1', 1);")
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            "INSERT INTO difference_relations (src, dst, admitted_step) VALUES ('v1', 'v1', 1);"
        )
    conn.close()


def test_root_w_multi_edge_boundary_sign_inversion():
    """
    Validates that view_boundary_sign_inversion correctly aggregates weights on multi-edge paths
    (e.g., c -> a -> b and d -> a -> e) without Cartesian product expansion or non-zero residuals.
    """
    conn = sqlite3.connect(":memory:")
    sql_path = (
        Path(__file__).resolve().parent.parent / "code" / "queries" / "root_w_relational_schema.sql"
    )
    with open(sql_path, "r", encoding="utf-8") as f:
        conn.executescript(f.read())

    # Insert carrier vertices
    for v in ["a", "b", "c", "d", "e"]:
        conn.execute(
            "INSERT INTO carrier_elements (element_id, admitted_step) VALUES (?, 1);", (v,)
        )

    # Insert multi-edge configuration: vertex 'a' has in-degree 2 and out-degree 2
    relations = [("c", "a"), ("a", "b"), ("d", "a"), ("a", "e")]
    for src, dst in relations:
        conn.execute(
            "INSERT INTO difference_relations (src, dst, admitted_step) VALUES (?, ?, 2);",
            (src, dst),
        )

    rows = conn.execute(
        "SELECT vertex, orig_weight, trans_weight, net_sum FROM view_boundary_sign_inversion ORDER BY vertex;"
    ).fetchall()

    # Invariants:
    # 1. Exactly 1 row per active vertex (no Cartesian cross-term duplication)
    assert len(rows) == 5, f"Expected exactly 5 vertex rows, got {len(rows)}"

    # 2. Every vertex satisfies net_sum == 0 and trans_weight == -orig_weight
    for vertex, orig_w, trans_w, net_sum in rows:
        assert net_sum == 0, f"Vertex {vertex} failed boundary cancellation: net_sum={net_sum}"
        assert trans_w == -orig_w, (
            f"Vertex {vertex} failed transposition sign flip: orig={orig_w}, trans={trans_w}"
        )

    conn.close()


def test_claim_hygiene_bareiss_determinant_docstring():
    """Asserts that domain_ansi_sql_kernel.py docstrings contain zero unhedged forbidden hype verbs."""
    kernel_path = Path(__file__).resolve().parent.parent / "code" / "domain_ansi_sql_kernel.py"
    with open(kernel_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Grep specifically for unhedged 'Guarantees ' in compute_bareiss_determinant
    import re

    assert not re.search(r"^\s*Guarantees\s+zero\b", content, re.MULTILINE), (
        "Forbidden hype verb 'Guarantees' detected in domain_ansi_sql_kernel.py docstring"
    )
