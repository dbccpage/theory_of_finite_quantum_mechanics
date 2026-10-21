"""Non-vacuous FW-8 exact degree-n and PO-014 computational fixtures."""

from dataclasses import FrozenInstanceError, fields
from fractions import Fraction
from itertools import combinations

import pytest
from sympy import Abs, Matrix, Rational

from omega_engine.crates.functional.degree_k_phi import (
    DegreeKPricingDeclaration,
    DegreeKPricingRefused,
    phi_k_on_complex_exact,
    solve_degree_k_phi_exact,
)
from omega_engine.crates.functional.higher_simplex_assembly import (
    SimplexComplex,
)
from omega_engine.crates.functional.po014_minimax import (
    PO014AffineWitness,
    PO014LeastSquaresSurrogateResult,
    PO014MinimaxProblem,
    PO014MinimaxRefused,
    PO014WitnessIndex,
    solve_po014_least_squares_surrogate,
    verify_po014_minimax_receipt,
)


def _simplex_boundary(vertex_count: int, degree: int) -> SimplexComplex:
    vertices = list(range(vertex_count))
    return SimplexComplex(
        vertices=vertices,
        cells={
            dimension: list(combinations(vertices, dimension + 1))
            for dimension in range(degree + 1)
        },
        max_dim=degree,
    )


def _po014_six_cycle() -> PO014MinimaxProblem:
    weights = (
        1,
        Fraction(11, 10),
        Fraction(6, 5),
        Fraction(13, 10),
        Fraction(7, 5),
        Fraction(3, 2),
    )
    witnesses = []
    for edge, weight in enumerate(weights):
        coefficients = [0] * 6
        coefficients[edge] = 1
        coefficients[(edge + 1) % 6] = -1
        witnesses.append(
            PO014AffineWitness(f"w{edge}", tuple(coefficients), 1, weight)
        )
    return PO014MinimaxProblem(tuple(witnesses))


def test_degree_2_boundary_tetrahedron_positive_and_exact_carrier() -> None:
    carrier = _simplex_boundary(4, 2)
    declaration = DegreeKPricingDeclaration.exact_l1(2)

    positive = phi_k_on_complex_exact(carrier, 2, [2, 4, 4, 6], declaration)
    exact = phi_k_on_complex_exact(carrier, 2, [3, 3, 5, 5], declaration)

    assert positive.primal_value == positive.dual_value == Rational(4)
    assert positive.exact_gap == 0
    assert positive.verify()
    assert exact.primal_value == exact.dual_value == Rational(0)
    assert exact.residual == Matrix.zeros(4, 1)
    assert exact.verify()


def test_degree_3_boundary_four_simplex_fundamental_witness() -> None:
    carrier = _simplex_boundary(5, 3)
    receipt = phi_k_on_complex_exact(
        carrier,
        3,
        [1, -1, 1, -1, 1],
        DegreeKPricingDeclaration.exact_l1(3),
    )

    assert receipt.primal_value == receipt.dual_value == Rational(5)
    assert receipt.y_star == Matrix([1, -1, 1, -1, 1])
    assert receipt.exact_gap == 0
    assert receipt.verify()


def test_degree_k_dual_replay_is_exact_and_named_w_lp() -> None:
    carrier = _simplex_boundary(4, 2)
    receipt = phi_k_on_complex_exact(
        carrier, 2, [2, 4, 4, 6], DegreeKPricingDeclaration.exact_l1(2)
    )
    repair_map = receipt.certificate.repair_map
    omega = Matrix([2, 4, 4, 6])

    assert receipt.W_LP == receipt.y_star
    assert repair_map.T * receipt.y_star == Matrix.zeros(repair_map.cols, 1)
    assert all(Abs(value) <= 1 for value in receipt.y_star)
    assert (receipt.y_star.T * omega)[0] == receipt.dual_value == 4
    assert omega - repair_map * receipt.alpha == receipt.residual
    assert sum(Abs(value) for value in receipt.residual) == receipt.primal_value
    assert receipt.primal_value - receipt.dual_value == receipt.exact_gap == 0


def test_exact_degree_k_refuses_floats_missing_capability_and_degeneracy() -> None:
    declaration = DegreeKPricingDeclaration.exact_l1(1)
    with pytest.raises(TypeError, match="exact arithmetic rejects float"):
        solve_degree_k_phi_exact([[1.0]], [1], declaration)
    with pytest.raises(TypeError, match="exact arithmetic rejects float"):
        solve_degree_k_phi_exact([[1]], [1.0], declaration)
    with pytest.raises(DegreeKPricingRefused, match="requires a DegreeKPricingDeclaration"):
        solve_degree_k_phi_exact([[1]], [1], None)
    with pytest.raises(DegreeKPricingRefused, match="empty/degenerate"):
        solve_degree_k_phi_exact([], [], declaration)
    with pytest.raises(DegreeKPricingRefused, match="degree >= 1"):
        DegreeKPricingDeclaration.exact_l1(0).validate()
    with pytest.raises(DegreeKPricingRefused, match="reachability declaration"):
        DegreeKPricingDeclaration(1, True, True, "").validate()
    with pytest.raises(DegreeKPricingRefused, match="genuine l1"):
        DegreeKPricingDeclaration(1, False, True, "carrier declaration").validate()
    with pytest.raises(DegreeKPricingRefused, match="index-agnostic"):
        DegreeKPricingDeclaration(1, True, False, "carrier declaration").validate()
    with pytest.raises(DegreeKPricingRefused, match="AuthorityEffect"):
        DegreeKPricingDeclaration(
            1, True, True, "carrier declaration", authority_effect="mutating"
        ).validate()


def test_epic006_b1_two_fixture_separates_l1_l2_and_raw_mass() -> None:
    edges = ((0, 1), (1, 2), (0, 2), (2, 3), (0, 3))
    repair_map = Matrix.zeros(len(edges), 4)
    for row, (source, target) in enumerate(edges):
        repair_map[row, source] = -1
        repair_map[row, target] = 1
    omega = Matrix([-2, -2, 2, 2, -2])

    exact_l1 = solve_degree_k_phi_exact(
        repair_map, omega, DegreeKPricingDeclaration.exact_l1(1)
    )
    l2_alpha = Matrix([0, Rational(-1, 2), -1, Rational(-1, 2)])
    l2_residual = omega - repair_map * l2_alpha
    l2_surrogate_mass = sum(Abs(value) for value in l2_residual)
    raw_mass = sum(Abs(value) for value in omega)

    assert repair_map.T * l2_residual == Matrix.zeros(4, 1)
    assert l2_residual == Matrix(
        [Rational(-3, 2), Rational(-3, 2), 3, Rational(3, 2), Rational(-3, 2)]
    )
    stated_l1_alpha = Matrix([0, -2, -4, -2])
    assert repair_map * exact_l1.alpha == repair_map * stated_l1_alpha
    assert exact_l1.residual == Matrix([0, 0, 6, 0, 0])
    assert exact_l1.y_star == Matrix([0, 0, 1, 1, -1])
    assert exact_l1.primal_value == 6
    assert l2_surrogate_mass == 9
    assert raw_mass == 10
    assert exact_l1.primal_value < l2_surrogate_mass < raw_mass


def test_po014_six_cycle_exact_value_dual_and_shared_optimizer() -> None:
    problem = _po014_six_cycle()
    receipt = problem.solve_exact()

    assert receipt.t_star == Rational(4004, 3265)
    assert float(receipt.t_star) == pytest.approx(1.2263399694, abs=1e-10)
    assert len(receipt.residuals) == 6
    assert len(receipt.active_witnesses) == 6
    assert receipt.dual_lower_bound == receipt.t_star
    assert receipt.exact_gap == 0
    assert verify_po014_minimax_receipt(problem, receipt)


def test_po014_witness_permutation_and_duplication_invariance() -> None:
    problem = _po014_six_cycle()
    canonical = problem.solve_exact()
    permuted = PO014MinimaxProblem(tuple(reversed(problem.witnesses))).solve_exact()
    duplicated_witness = PO014AffineWitness(
        "w6-dup",
        problem.witnesses[2].coefficients,
        problem.witnesses[2].offset,
        problem.witnesses[2].weight,
    )
    duplicated = PO014MinimaxProblem(problem.witnesses + (duplicated_witness,)).solve_exact()

    assert permuted.t_star == canonical.t_star
    assert permuted.z_star == canonical.z_star
    assert permuted.residual_by_index == canonical.residual_by_index
    assert duplicated.t_star == canonical.t_star
    assert duplicated.z_star == canonical.z_star
    assert duplicated.residual_by_index[PO014WitnessIndex("w6-dup")] == (
        canonical.residual_by_index[problem.witnesses[2].index]
    )


def test_po014_enforces_one_optimizer_and_rejects_max_inf_swap() -> None:
    left = PO014AffineWitness("left", (1,), -1)
    right = PO014AffineWitness("right", (1,), 1)
    shared = PO014MinimaxProblem((left, right)).solve_exact()
    independently_optimized = max(
        PO014MinimaxProblem((witness,)).solve_exact().t_star
        for witness in (left, right)
    )

    assert shared.z_star == (Rational(0),)
    assert shared.t_star == 1
    assert independently_optimized == 0
    assert shared.t_star > independently_optimized


def test_po014_least_squares_is_unmistakably_surrogate_only() -> None:
    surrogate = solve_po014_least_squares_surrogate(_po014_six_cycle())

    assert isinstance(surrogate, PO014LeastSquaresSurrogateResult)
    assert surrogate.max_abs_residual == pytest.approx(1.475196334, abs=1e-9)
    assert surrogate.status == "SURROGATE_ONLY"
    assert not surrogate.is_canonical
    assert not surrogate.is_certified
    assert "status" not in {field.name for field in fields(surrogate)}
    with pytest.raises(FrozenInstanceError):
        surrogate.max_abs_residual = 0.0


def test_po014_exact_input_and_nondegeneracy_gate_refuses() -> None:
    with pytest.raises(TypeError, match="exact arithmetic rejects float"):
        PO014AffineWitness("float", (1.0,), 0)
    with pytest.raises(PO014MinimaxRefused, match="nonempty witness family"):
        PO014MinimaxProblem(())
    with pytest.raises(PO014MinimaxRefused, match="nondegenerate optimizer dimension"):
        PO014MinimaxProblem((PO014AffineWitness("constant", (), 1),))
    with pytest.raises(PO014MinimaxRefused, match="AuthorityEffect"):
        PO014MinimaxProblem(
            (PO014AffineWitness("w", (1,), 0),), authority_effect="mutating"
        )


