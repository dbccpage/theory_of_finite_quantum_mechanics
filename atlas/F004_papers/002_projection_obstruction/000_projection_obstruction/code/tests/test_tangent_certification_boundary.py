"""Exact controls against certification of thresholded/SLSQP tangent candidates."""

from __future__ import annotations

import sys
from dataclasses import FrozenInstanceError, asdict, replace
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

_code_dir = Path(__file__).resolve().parents[1]
if str(_code_dir) not in sys.path:
    sys.path.insert(0, str(_code_dir))

from feasible_tangent_cone import (  # noqa: E402
    AmbientFeasibleTangentCone,
    BoundaryGeometryError,
    ClusterProductManifold,
    TangentCertificationError,
    operator_norm,
    trace_norm,
)


def _ambient_result():
    cone = AmbientFeasibleTangentCone(np.diag([1.0, 0.0]))
    return cone.solve_distance_certified(np.diag([1.0, -1.0]))


def test_tiny_positive_eigenvalue_changes_diagnostic_not_exact_tangent_cone() -> None:
    epsilon = Fraction(1, 10**13)
    # Both exact eigenvalues are positive: rho + tL remains positive for
    # 0 <= t < epsilon. L is therefore an exact tangent, of distance zero.
    assert 1 - epsilon > 0 and epsilon > 0
    rho = np.diag([float(1 - epsilon), float(epsilon)])
    action = np.diag([1.0, -1.0])
    thresholded = AmbientFeasibleTangentCone(rho)
    unthresholded = AmbientFeasibleTangentCone(rho, zero_threshold=0.0)
    assert thresholded.rank == 1
    assert unthresholded.rank == 2

    threshold_result = thresholded.solve_distance_certified(action)
    zero_threshold_result = unthresholded.solve_distance_certified(action)
    assert threshold_result.distance == 2.0
    assert zero_threshold_result.distance == 0.0
    # Removing a threshold does not turn floating-point arithmetic into proof.
    for result in (threshold_result, zero_threshold_result):
        assert result.certificate_status == "not_certified"
        assert result.evidence_kind == "numerical_tangent_candidate"
        assert "rank thresholds" in " ".join(result.limitations)


def test_product_residual_sign_can_exceed_primal_and_violate_polar() -> None:
    rho = np.diag([0.8, 0.2])
    action = np.diag([1.0, -1.0, -1.0, 1.0])
    manifold = ClusterProductManifold([rho, rho])
    result = manifold.solve_feasible_tangent_distance_certified(action)
    candidate_dual_value = float(np.trace(result.dual_witness @ action).real)
    feasible_direction = np.kron(np.diag([1.0, -1.0]), rho)

    assert manifold.is_feasible_tangent(feasible_direction)
    assert result.distance == pytest.approx(2.5, abs=1e-5)
    assert candidate_dual_value == pytest.approx(3.0, abs=1e-5)
    assert candidate_dual_value > result.distance + 0.4
    assert result.duality_gap == pytest.approx(0.5, abs=1e-5)
    assert float(np.trace(result.dual_witness @ feasible_direction).real) > 0.3
    assert result.certificate_status == "not_certified"
    assert "polar constraints" in " ".join(result.limitations)


def test_exact_product_control_has_matching_valid_primal_and_dual() -> None:
    # This rational certificate is independent of the numerical optimizer.
    q = Fraction
    rho = (q(4, 5), q(1, 5))
    local_tangent = (q(5, 8), q(-5, 8))
    primal = tuple(
        local_tangent[i] * rho[j] + rho[i] * local_tangent[j]
        for i in range(2)
        for j in range(2)
    )
    action = (q(1), q(-1), q(-1), q(1))
    dual = (q(-1, 2), q(-1), q(-1), q(1))
    assert primal == (q(1), q(-3, 8), q(-3, 8), q(-1, 4))
    assert sum(local_tangent) == 0
    assert max(abs(entry) for entry in dual) == 1
    # Both weighted partial traces are scalar multiples of I; off-diagonal
    # pairings vanish because W and rho are diagonal. Thus W annihilates all
    # traceless product tangents, including nondiagonal ones.
    assert tuple(sum(dual[2 * i + j] * rho[j] for j in range(2)) for i in range(2)) == (
        q(-3, 5), q(-3, 5)
    )
    assert tuple(sum(dual[2 * i + j] * rho[i] for i in range(2)) for j in range(2)) == (
        q(-3, 5), q(-3, 5)
    )
    assert sum(abs(a - v) for a, v in zip(action, primal, strict=True)) == q(5, 2)
    assert sum(w * a for w, a in zip(dual, action, strict=True)) == q(5, 2)
    # Floating-point replay is a consistency check, separately scoped.
    action_matrix = np.diag([float(v) for v in action])
    primal_matrix = np.diag([float(v) for v in primal])
    assert trace_norm(action_matrix - primal_matrix) == 2.5
    assert operator_norm(np.diag([float(v) for v in dual])) == 1.0


@pytest.mark.parametrize("product", [False, True])
def test_certification_request_refuses_before_action_evaluation(product: bool) -> None:
    class UnreadableAction:
        def tolist(self):
            pytest.fail("A refused certification request must not evaluate the action")

    if product:
        evaluate = ClusterProductManifold([np.eye(2) / 2] * 2).solve_feasible_tangent_distance_certified
    else:
        evaluate = AmbientFeasibleTangentCone(np.eye(2) / 2).solve_distance_certified
    with pytest.raises(TangentCertificationError, match="Certified tangent evaluation is unavailable"):
        evaluate(UnreadableAction(), require_certified=True)


@pytest.mark.parametrize("require_certified", [1, 0, None, "yes"])
@pytest.mark.parametrize("product", [False, True])
def test_certification_flag_requires_a_boolean(require_certified, product: bool) -> None:
    if product:
        evaluate = ClusterProductManifold([np.eye(2) / 2] * 2).solve_feasible_tangent_distance_certified
        action = np.zeros((4, 4))
    else:
        evaluate = AmbientFeasibleTangentCone(np.eye(2) / 2).solve_distance_certified
        action = np.zeros((2, 2))
    with pytest.raises(BoundaryGeometryError, match="require_certified must be a bool"):
        evaluate(action, require_certified=require_certified)


def test_result_evidence_metadata_is_fixed_and_serialized() -> None:
    result = _ambient_result()
    payload = asdict(result)
    assert payload["certificate_status"] == "not_certified"
    assert payload["evidence_kind"] == "numerical_tangent_candidate"
    with pytest.raises(FrozenInstanceError):
        result.certificate_status = "certified"
    with pytest.raises(FrozenInstanceError):
        result.evidence_kind = "exact_dual_certificate"
    with pytest.raises((ValueError, TypeError), match="init=False"):
        replace(result, certificate_status="certified")
    with pytest.raises((ValueError, TypeError), match="init=False"):
        replace(result, evidence_kind="exact_dual_certificate")


def test_already_feasible_product_branch_is_also_noncertifying() -> None:
    manifold = ClusterProductManifold([np.eye(2) / 2] * 2)
    result = manifold.solve_feasible_tangent_distance_certified(np.zeros((4, 4)))
    assert result.is_feasible
    assert result.distance == 0.0
    assert result.duality_gap == 0.0
    assert result.certificate_status == "not_certified"
    assert result.evidence_kind == "numerical_tangent_candidate"
