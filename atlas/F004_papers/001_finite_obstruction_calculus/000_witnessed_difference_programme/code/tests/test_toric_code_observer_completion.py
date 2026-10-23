"""test_toric_code_observer_completion.py — Unit tests for Toric Code Observer Completion (WDP Chapter 23).

AuthorityEffect: None.
Tests:
  - WDP-CH23-P01: Incidence matrix ranks, cycle/cut dimensions, and logical kernel.
  - WDP-CH23-P02: Distance d = L.
  - WDP-CH23-P06: Threshold 2t < L for B = S.
  - WDP-CH23-P13: Minimal uniform-cost spine |D| >= 2L^2 - 2.
  - WDP-CH23-P14: Primal / dual certificate dichotomy.
"""

import itertools
import sys
from pathlib import Path

import numpy as np

CODE_DIR = Path(__file__).resolve().parents[1]
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

import toric_code_observer_completion as tcoc


def test_commutation_kernel_is_sperp_not_s():
    report = tcoc.commutation_kernel_report(3)
    assert report["lattice"].startswith("periodic Z_L x Z_L")
    assert report["weight_convention"] == "wt(e)=|supp e_X|+|supp e_Z|"
    assert report["quotient_dimension"] == 4
    assert report["kernel_equals_stabilizer"] is False
    assert report["logical_in_kernel"] is True
    assert report["logical_in_stabilizer"] is False
    assert report["logical_weight"] == 3
    try:
        tcoc.check_kernel_claim({"kernel": "S"}, report)
    except ValueError as error:
        assert str(error) == "toric_kernel_identified_with_s"
    else:
        raise AssertionError("kernel was identified with S")


def test_t0_buys_no_detector_and_rank_defect_is_not_a_collision():
    from fractions import Fraction as F
    syndrome = tcoc.pauli_commutation_syndrome(3)
    errors = tcoc.t0_family(syndrome.shape[1])
    repair = tcoc.stabilizer_generator_rows(3)
    collision = tcoc.admitted_collision(syndrome, errors, repair)
    assert collision is None
    report = tcoc.commutation_kernel_report(3)
    try:
        tcoc.check_rank_defect_claim(
            {"collision_from_global_quotient": True}, collision, report["quotient_dimension"]
        )
    except ValueError as error:
        assert str(error) == "rank_defect_as_low_weight_collision"
    else:
        raise AssertionError("global quotient was treated as a collision")
    shelf = [syndrome[row].copy() for row in range(min(4, syndrome.shape[0]))]
    costs = [F(1), F(2), F(3), F(4)]
    produced = tcoc.minimum_cost_suite(shelf, costs, errors, repair)
    assert produced["indices"] == tuple()
    assert produced["cost"] == 0
    assert tcoc.check_minimum_cost_suite(shelf, costs, errors, repair, produced)["accepted"]

    def independent_min():
        best = None
        for size in range(len(shelf) + 1):
            for chosen in itertools.combinations(range(len(shelf)), size):
                rows = [shelf[index] for index in chosen]
                if tcoc.suite_separates(rows, errors, repair):
                    cost = sum(costs[index] for index in chosen)
                    if best is None or cost < best:
                        best = cost
        return best

    assert produced["cost"] == independent_min()
    bad = {"feasible": True, "indices": (0, 1, 2, 3), "cost": sum(costs)}
    try:
        tcoc.check_minimum_cost_suite(shelf, costs, errors, repair, bad)
    except ValueError as error:
        assert str(error) == "t0_requires_full_detector_basis"
    else:
        raise AssertionError("t=0 accepted a full purchase")
    insufficient = {"feasible": True, "indices": (0,), "cost": F(1)}
    # The empty family is already separated, so a positive one-detector suite
    # is a purchase, not an insufficient schedule.
    try:
        tcoc.check_minimum_cost_suite(shelf, costs, errors, repair, insufficient)
    except ValueError as error:
        assert str(error) == "t0_requires_full_detector_basis"
    else:
        raise AssertionError("positive t=0 purchase accepted")


def _weight_at_most_one(width: int):
    errors = [np.zeros(width, dtype=int)]
    for index in range(width):
        vector = np.zeros(width, dtype=int)
        vector[index] = 1
        errors.append(vector)
    return errors


def test_full_rank_is_sufficient_and_not_necessary_for_weight_one():
    face, star = tcoc.build_toric_incidence_matrices(3)
    selected = (0, 1, 3, 5, 7, 8)
    face_rows = face[list(selected)]
    assert tcoc.gf2_rank(face) == 8
    assert tcoc.gf2_rank(face_rows) == 6
    assert not any(np.all(face_rows[:, column] == 0) for column in range(face_rows.shape[1]))
    for left, right in ((0, 1), (4, 13), (5, 8)):
        assert np.all((face_rows[:, left] + face_rows[:, right]) % 2 == 0)
    pair = np.zeros(face.shape[1], dtype=int)
    pair[0] = 1
    pair[1] = 1
    assert tcoc.is_in_span(star, pair) is False
    qubits = face.shape[1]
    x_only = []
    for support in face_rows:
        vector = np.zeros(2 * qubits, dtype=int)
        vector[:qubits] = support
        x_only.append(vector)
    repair_l3 = tcoc.stabilizer_generator_rows(3)
    errors_l3 = _weight_at_most_one(2 * qubits)
    assert tcoc.suite_separates(x_only, errors_l3, repair_l3) is False
    assert tcoc.admitted_collision(np.vstack(x_only) % 2, errors_l3, repair_l3) is not None

    syndrome = tcoc.pauli_commutation_syndrome(4)
    assert syndrome.shape == (32, 64)
    assert tcoc.gf2_rank(syndrome) == 30
    without_two_faces = [index for index in range(syndrome.shape[0]) if index not in (1, 10)]
    held = syndrome[without_two_faces]
    assert held.shape[0] == 30
    assert tcoc.gf2_rank(held) == 29
    dropped = None
    for local, index in enumerate(without_two_faces):
        kept = [row for row in without_two_faces if row != index]
        if tcoc.gf2_rank(syndrome[kept]) == 29:
            dropped = index
            chosen = kept
            break
    assert dropped == 16
    assert chosen == [index for index in range(32) if index not in (1, 10, 16)]
    assert len(chosen) == 29
    assert tcoc.gf2_rank(syndrome[chosen]) == 29
    repair = tcoc.stabilizer_generator_rows(4)
    errors = _weight_at_most_one(syndrome.shape[1])
    rows = [syndrome[index].copy() for index in chosen]
    assert tcoc.admitted_collision(np.vstack(rows) % 2, errors, repair) is None
    assert tcoc.suite_separates(rows, errors, repair) is True


def test_small_positive_cost_shelf_matches_enumeration():
    from fractions import Fraction as F
    # Two admitted X-errors on the first two qubits, repair {0}. One cheap
    # detector sees the first, an expensive detector sees both.
    width = 4
    zero = np.zeros(width, dtype=int)
    first = zero.copy()
    first[0] = 1
    second = zero.copy()
    second[1] = 1
    errors = [zero, first, second]
    repair = np.zeros((1, width), dtype=int)
    see_first = np.array([1, 0, 0, 0], dtype=int)
    see_second = np.array([0, 1, 0, 0], dtype=int)
    see_both = np.array([1, 1, 0, 0], dtype=int)
    shelf = [see_both, see_first, see_second]
    costs = [F(5), F(2), F(2)]
    produced = tcoc.minimum_cost_suite(shelf, costs, errors, repair)

    def independent_min():
        best = None
        for size in range(len(shelf) + 1):
            for chosen in itertools.combinations(range(len(shelf)), size):
                if tcoc.suite_separates([shelf[i] for i in chosen], errors, repair):
                    cost = sum(costs[i] for i in chosen)
                    if best is None or cost < best:
                        best = cost
        return best

    assert produced["cost"] == independent_min() == F(4)
    assert tcoc.check_minimum_cost_suite(shelf, costs, errors, repair, produced)["accepted"]
    # see_both alone collides on the two admitted errors. Adding see_first
    # separates them, at a strictly higher cost than see_first plus see_second.
    costlier = {"feasible": True, "indices": (0, 1), "cost": F(7)}
    try:
        tcoc.check_minimum_cost_suite(shelf, costs, errors, repair, costlier)
    except ValueError as error:
        assert "not minimum" in str(error)
    else:
        raise AssertionError("costlier detector accepted")
    missed = {"feasible": True, "indices": (1,), "cost": F(2)}
    try:
        tcoc.check_minimum_cost_suite(shelf, costs, errors, repair, missed)
    except ValueError as error:
        assert str(error) == "insufficient suite"
    else:
        raise AssertionError("insufficient detector accepted")


def test_cost_shelf_refuses_bool_float_and_missing_feasible():
    from fractions import Fraction as F
    width = 4
    zero = np.zeros(width, dtype=int)
    first = zero.copy()
    first[0] = 1
    errors = [zero, first]
    repair = np.zeros((1, width), dtype=int)
    shelf = [np.array([1, 0, 0, 0], dtype=int)]
    try:
        tcoc.minimum_cost_suite(shelf, [True], errors, repair)
    except ValueError as error:
        assert str(error) == "positive rational costs required"
    else:
        raise AssertionError("boolean cost accepted")
    try:
        tcoc.minimum_cost_suite(shelf, [1.5], errors, repair)
    except ValueError as error:
        assert str(error) == "positive rational costs required"
    else:
        raise AssertionError("float cost accepted")
    produced = tcoc.minimum_cost_suite(shelf, [F(1)], errors, repair)
    missing = dict(produced)
    del missing["feasible"]
    try:
        tcoc.check_minimum_cost_suite(shelf, [F(1)], errors, repair, missing)
    except ValueError as error:
        assert str(error) == "feasible flag required"
    else:
        raise AssertionError("missing feasible flag accepted")


def test_toric_geometry_and_ranks():
    L = 3
    A, A_v = tcoc.build_toric_incidence_matrices(L)
    
    # P01: rank(A) = rank(A_v) = L^2 - 1 = 8
    rank_A = tcoc.gf2_rank(A)
    rank_Av = tcoc.gf2_rank(A_v)
    assert rank_A == L * L - 1
    assert rank_Av == L * L - 1
    
    # Nullspace dimensions: dim Cyc = dim Cut = 2L^2 - (L^2 - 1) = L^2 + 1 = 10
    cyc_basis = tcoc.gf2_nullspace(A)
    cut_basis = tcoc.gf2_nullspace(A_v)
    assert len(cyc_basis) == L * L + 1
    assert len(cut_basis) == L * L + 1
    
    # Logical space: 2 logical qubits (dimension 4 over F_2)
    assert len(cyc_basis) - rank_A == 2
    assert len(cut_basis) - rank_Av == 2


def test_toric_distance_and_logicals():
    L = 3
    A, A_v = tcoc.build_toric_incidence_matrices(L)
    logicals = tcoc.get_canonical_logicals(L)
    
    # X cycles commute with Z plaquettes and are not X stabilizers.
    for name in ("X1", "X2"):
        assert np.all(A @ logicals[name] % 2 == 0)
        assert not tcoc.is_in_span(A_v, logicals[name])
    # Z cycles commute with X stars and are not Z stabilizers.
    for name in ("Z1", "Z2"):
        assert np.all(A_v @ logicals[name] % 2 == 0)
        assert not tcoc.is_in_span(A, logicals[name])
    for i in (1, 2):
        for j in (1, 2):
            assert int(logicals[f"X{i}"] @ logicals[f"Z{j}"]) % 2 == int(i == j)

    # Weights equal L = 3
    assert np.sum(logicals["X1"]) == L
    assert np.sum(logicals["X2"]) == L
    assert np.sum(logicals["Z1"]) == L
    assert np.sum(logicals["Z2"]) == L


def test_observer_completion_dichotomy_primal():
    """Verify that for 2t < L (L=3, t=1), full measurement schedule admits a primal certificate."""
    L = 3
    geom = tcoc.build_toric_code_geometry(L)
    A, A_v = tcoc.build_toric_incidence_matrices(L)
    
    # Admissible error set E_1: weight <= 1 on X-errors
    # Measured by Z-plaquette matrix A
    admissible_errors = [np.zeros(geom.n_qubits, dtype=int)]
    for i in range(geom.n_qubits):
        e = np.zeros(geom.n_qubits, dtype=int)
        e[i] = 1
        admissible_errors.append(e)
        
    res = tcoc.evaluate_observer_completion(
        H_D=A,
        admissible_errors=admissible_errors,
        stabilizer_basis=A_v,
    )
    
    assert res.is_sufficient is True
    assert res.primal_recovery_table is not None
    assert res.dual_failure_witness is None
    assert res.authority_effect == "None"


def test_observer_completion_dichotomy_dual_on_insufficient_schedule():
    """Verify that omitting detectors creates an undetectable low-weight failure witness."""
    L = 3
    geom = tcoc.build_toric_code_geometry(L)
    A, A_v = tcoc.build_toric_incidence_matrices(L)
    
    # Omit multiple detectors to make an error pair undetectable
    # E.g. only measure 2 plaquettes out of 9
    H_partial = A[:2]
    
    admissible_errors = [np.zeros(geom.n_qubits, dtype=int)]
    for i in range(geom.n_qubits):
        e = np.zeros(geom.n_qubits, dtype=int)
        e[i] = 1
        admissible_errors.append(e)
        
    res = tcoc.evaluate_observer_completion(
        H_D=H_partial,
        admissible_errors=admissible_errors,
        stabilizer_basis=A_v,
    )
    
    # With only 2 checks, weight-1 errors must collide with zero syndrome
    assert res.is_sufficient is False
    assert res.primal_recovery_table is None
    assert res.dual_failure_witness is not None
    e1_str, e2_str = res.dual_failure_witness
    assert len(e1_str) == geom.n_qubits
    assert len(e2_str) == geom.n_qubits


def test_full_stabilizer_rank():
    """The full stabilizer rank is 2L^2-2; this is not minimum detector cost."""
    L = 3
    A, A_v = tcoc.build_toric_incidence_matrices(L)
    
    # CSS block structure: A measures X-errors, A_v measures Z-errors
    # Total stabilizer group S = Plaq + Star has rank = rank(A) + rank(A_v)
    rank_A = tcoc.gf2_rank(A)
    rank_Av = tcoc.gf2_rank(A_v)
    rank_S = rank_A + rank_Av
    # Total independent stabilizers on 2L^2 = 18 qubits is 2*9 - 2 = 16
    assert rank_S == 2 * L * L - 2


def test_p07c_coarser_question_diagonal_collision_counterexample():
    """WDP-CH23-P07C regression test:

    Verifies that for B = S + <u + v> with u in ker(Q) an X-logical loop and
    v in ker(Q) an independent Z-logical loop, the distance dB = min{wt(z) : z in ker Q \\ B}
    equals L, NOT 2L.

    At L=3, t=2:
      e1 = h_{0,0} (wt 1)
      e2 = {h_{1,0}, h_{2,0}} (wt 2)
    Both e1, e2 have wt <= 2 (in E_2).
    Their syndromes Q(e1) and Q(e2) are identical (since e1 + e2 = u in ker Q).
    Their difference is u.
    Since u not in B = S + <u + v>, e1 and e2 collide under Q but have distinct
    protected answers modulo B.
    Thus the claimed tolerance t <= L - 1 (t = 2 at L=3) fails, and the threshold
    retains 2t < L (t <= 1 at L=3).
    """
    L = 3
    face, star = tcoc.build_toric_incidence_matrices(L)
    qubits = face.shape[1]
    syndrome = tcoc.pauli_commutation_syndrome(L)
    repair = tcoc.stabilizer_generator_rows(L)

    # u: X-logical along column 0: h_{0,0}, h_{1,0}, h_{2,0}
    # Horizontal edge h_{i,j} has index 2*(i*L + j)
    # h_{0,0} = 0, h_{1,0} = 6, h_{2,0} = 12
    u = np.zeros(2 * qubits, dtype=int)
    u[0] = 1
    u[6] = 1
    u[12] = 1

    # v: independent Z-logical loop placed in Z-block (qubits to 2*qubits)
    # Using horizontal loop across row 0 in Z block
    v = np.zeros(2 * qubits, dtype=int)
    v[qubits:] = tcoc.get_canonical_logicals(L)["Z1"]

    # Verify u and v are in ker(Q) but not in S
    assert np.all(syndrome @ u % 2 == 0)
    assert not tcoc.is_in_span(repair, u)
    assert np.all(syndrome @ v % 2 == 0)
    assert not tcoc.is_in_span(repair, v)

    # Allowed subspace B = S + <u + v>
    diag = (u + v) % 2
    assert np.sum(diag) == 2 * L  # Weight 2L = 6
    B_basis = np.vstack([repair, diag.reshape(1, -1)])

    # Neither u nor v is in B
    assert not tcoc.is_in_span(B_basis, u)
    assert not tcoc.is_in_span(B_basis, v)

    # Errors e1 and e2 at t=2
    e1 = np.zeros(2 * qubits, dtype=int)
    e1[0] = 1  # h_{0,0}

    e2 = np.zeros(2 * qubits, dtype=int)
    e2[6] = 1   # h_{1,0}
    e2[12] = 1  # h_{2,0}

    assert np.sum(e1) == 1 <= 2
    assert np.sum(e2) == 2 <= 2

    # Identical syndromes
    syn1 = syndrome @ e1 % 2
    syn2 = syndrome @ e2 % 2
    assert np.array_equal(syn1, syn2)

    # Difference is u not in B
    diff = (e1 + e2) % 2
    assert np.array_equal(diff, u)
    assert not tcoc.is_in_span(B_basis, diff)

    # Check that evaluate_observer_completion with admissible errors {e1, e2} fails
    res = tcoc.evaluate_observer_completion(
        H_D=syndrome,
        admissible_errors=[e1, e2],
        stabilizer_basis=B_basis,
    )
    assert res.is_sufficient is False
    assert res.dual_failure_witness is not None

    # Check admitted_collision directly
    collision = tcoc.admitted_collision(syndrome, [e1, e2], B_basis)
    assert collision is not None

