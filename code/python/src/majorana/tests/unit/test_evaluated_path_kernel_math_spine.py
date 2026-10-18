import math
from fractions import Fraction
import pytest
from omega_engine.crates.type.epk.core import State, PathSegment, ComposedPath
from omega_engine.crates.type.epk.defects import (
    proposal_gluing_defect,
    cost_gluing_defect,
    residual_risk_gluing_defect,
    total_gluing_defect,
    verify_epk_transport_axis,
    attach_cech_diagnostic,
)
from omega_engine.crates.type.epk.evaluated_path import (
    path_weight_generalized,
    composed_kernel_generalized,
)
from omega_engine.crates.category_theory.transport import DiagonalTransportRefusal
from omega_engine.crates.type.sheaf.cech_gate import CechConsistent, LocalSection
from omega_engine.crates.homology_theory.qmatrix import QMatrix
from omega_engine.crates.type.refusal import Refusal


# ---------------------------------------------------------------------------
# Test Helpers
# ---------------------------------------------------------------------------


def _create_test_path(
    first_cost: float,
    second_cost: float,
    composed_cost: float | None = None,
    first_prob: float = 1.0,
    second_prob: float = 1.0,
    global_prob: float | None = None,
    first_risk: float = 0.0,
    second_risk: float = 0.0,
    global_risk: float | None = None,
    global_pass: bool = True,
    first_axis: str | None = None,
    second_axis: str | None = None,
    first_meta: dict | None = None,
    second_meta: dict | None = None,
) -> ComposedPath:
    s_a = State(id="S_a")
    s_b = State(id="S_b")
    s_c = State(id="S_c")

    fm = dict(first_meta) if first_meta else {}
    sm = dict(second_meta) if second_meta else {}

    fm["prob"] = first_prob
    fm["risk"] = first_risk
    if first_axis:
        fm["axis"] = first_axis

    sm["prob"] = second_prob
    sm["risk"] = second_risk
    if second_axis:
        sm["axis"] = second_axis

    seg1 = PathSegment(
        id="seg1", source=s_a, target=s_b, cost=first_cost, eval_pass=True, metadata=fm
    )
    seg2 = PathSegment(
        id="seg2", source=s_b, target=s_c, cost=second_cost, eval_pass=True, metadata=sm
    )

    gm = {}
    if global_prob is not None:
        gm["prob"] = global_prob
    if global_risk is not None:
        gm["risk"] = global_risk

    return ComposedPath(
        id="cp1",
        first=seg1,
        second=seg2,
        global_eval_pass=global_pass,
        composed_cost=composed_cost,
        metadata=gm,
    )


# ===========================================================================
# 1. Generalized Path Weight Tests
# ===========================================================================


def test_path_weight_generalized_valid():
    # E=True, C=1.5, R=0.5, P=0.8, lambda=2.0, mu=3.0
    # w = 0.8 * exp(-2.0*1.5 - 3.0*0.5) = 0.8 * exp(-3.0 - 1.5) = 0.8 * exp(-4.5)
    w = path_weight_generalized(
        eval_pass=True,
        cost=1.5,
        risk=0.5,
        prob=0.8,
        lambda_=2.0,
        mu_=3.0,
    )
    expected = 0.8 * math.exp(-4.5)
    assert w == pytest.approx(expected)


def test_path_weight_generalized_failed_eval_returns_zero():
    w = path_weight_generalized(
        eval_pass=False,
        cost=1.5,
        risk=0.5,
        prob=0.8,
    )
    assert w == 0.0


def test_path_weight_generalized_invalid_prob_rejected():
    with pytest.raises(ValueError, match="prob"):
        path_weight_generalized(True, 1.0, 0.0, 1.1)

    with pytest.raises(ValueError, match="non-negative"):
        path_weight_generalized(True, 1.0, 0.0, -0.1)


# ===========================================================================
# 2. Log-Space Defect Tests
# ===========================================================================


def test_proposal_gluing_defect_zero_default():
    # If global probability is omitted, it defaults to G4 boundary sufficiency (delta_p = 0.0)
    cp = _create_test_path(1.0, 1.0, first_prob=0.8, second_prob=0.9, global_prob=None)
    assert proposal_gluing_defect(cp) == pytest.approx(0.0)


def test_proposal_gluing_defect_with_mismatch():
    # P(1) = 0.8, P(2) = 0.9. P(global) = 0.5
    # delta_p = -log(0.5) + log(0.8) + log(0.9) = log(0.8 * 0.9 / 0.5) = log(1.44)
    cp = _create_test_path(1.0, 1.0, first_prob=0.8, second_prob=0.9, global_prob=0.5)
    expected = -math.log(0.5) + math.log(0.8) + math.log(0.9)
    assert proposal_gluing_defect(cp) == pytest.approx(expected)


def test_residual_risk_gluing_defect_zero_default():
    cp = _create_test_path(1.0, 1.0, first_risk=0.2, second_risk=0.3, global_risk=None)
    assert residual_risk_gluing_defect(cp) == pytest.approx(0.0)


def test_residual_risk_gluing_defect_with_mismatch():
    cp = _create_test_path(1.0, 1.0, first_risk=0.2, second_risk=0.3, global_risk=0.8)
    # delta_r = 0.8 - 0.2 - 0.3 = 0.3
    assert residual_risk_gluing_defect(cp) == pytest.approx(0.3)


def test_cost_gluing_defect():
    cp_add = _create_test_path(1.0, 2.0, composed_cost=None)
    assert cost_gluing_defect(cp_add) == pytest.approx(0.0)

    cp_override = _create_test_path(1.0, 2.0, composed_cost=3.5)
    assert cost_gluing_defect(cp_override) == pytest.approx(0.5)


def test_total_gluing_defect():
    # Set up mismatch on all three defects:
    # C1=1.0, C2=2.0, Cg=3.5 => delta_c = 0.5
    # P1=0.8, P2=0.9, Pg=0.5 => delta_p = log(1.44)
    # R1=0.2, R2=0.3, Rg=0.8 => delta_r = 0.3
    cp = _create_test_path(
        first_cost=1.0,
        second_cost=2.0,
        composed_cost=3.5,
        first_prob=0.8,
        second_prob=0.9,
        global_prob=0.5,
        first_risk=0.2,
        second_risk=0.3,
        global_risk=0.8,
    )
    dp = -math.log(0.5) + math.log(0.8) + math.log(0.9)
    dc = 0.5
    dr = 0.3

    assert total_gluing_defect(cp, lambda_=2.0, mu_=3.0) == pytest.approx(
        dp + 2.0 * dc + 3.0 * dr
    )


# ===========================================================================
# 3. Transport Axis Discipline Tests
# ===========================================================================


def test_verify_transport_axis_clean():
    cp = _create_test_path(1.0, 1.0, first_axis="vertical", second_axis="horizontal")
    assert verify_epk_transport_axis(cp) is True


def test_verify_transport_axis_mixed_refusal():
    cp = _create_test_path(1.0, 1.0, first_axis="mixed", second_axis="horizontal")
    res = verify_epk_transport_axis(cp)
    assert isinstance(res, DiagonalTransportRefusal)
    assert "mixed vertical+horizontal" in res.details


def test_verify_transport_axis_mixed_with_certificate():
    cp = _create_test_path(
        1.0,
        1.0,
        first_axis="mixed",
        second_axis="horizontal",
        first_meta={"chi_square": "replayable_witness"},
    )
    assert verify_epk_transport_axis(cp) is True


# ===========================================================================
# 4. Cech Contextual Diagnostics Tests
# ===========================================================================


def test_attach_cech_diagnostic_consistent():
    cp = _create_test_path(1.0, 1.0)
    secs = [
        LocalSection(patch=0, value=[Fraction(0)], valid=True),
        LocalSection(patch=1, value=[Fraction(1)], valid=True),
        LocalSection(patch=2, value=[Fraction(3)], valid=True),
    ]
    d0 = QMatrix.from_row_major(3, 3, [-1, 1, 0, 0, -1, 1, 1, 0, -1])
    d1 = QMatrix.zero(0, 3)
    z = [1, 2, -3]

    res = attach_cech_diagnostic(cp, secs, d0, d1, z)
    assert isinstance(res, CechConsistent)


def test_attach_cech_diagnostic_obstruction():
    cp = _create_test_path(1.0, 1.0)
    secs = [
        LocalSection(patch=0, value=[Fraction(0)], valid=True),
        LocalSection(patch=1, value=[Fraction(0)], valid=True),
        LocalSection(patch=2, value=[Fraction(0)], valid=True),
    ]
    d0 = QMatrix.from_row_major(3, 3, [-1, 1, 0, 0, -1, 1, 1, 0, -1])
    d1 = QMatrix.zero(0, 3)
    z = [1, 1, 1]  # sum is 3 != 0 => not in image, nonzero Čech class

    res = attach_cech_diagnostic(cp, secs, d0, d1, z)
    assert isinstance(res, Refusal)
    assert res.reason == "ContextualObstruction"


# ===========================================================================
# 5. Generalized Composed Kernel Tests
# ===========================================================================


def test_composed_kernel_generalized_aggregation():
    p1 = _create_test_path(
        first_cost=1.0,
        second_cost=2.0,
        composed_cost=3.0,
        first_prob=0.8,
        second_prob=0.9,
        global_prob=0.5,
        first_risk=0.2,
        second_risk=0.3,
        global_risk=0.4,
    )
    p2 = _create_test_path(
        first_cost=0.5,
        second_cost=1.5,
        composed_cost=2.0,
        first_prob=0.7,
        second_prob=0.8,
        global_prob=0.4,
        first_risk=0.1,
        second_risk=0.2,
        global_risk=0.3,
    )
    # Aggregated mass for S_a -> S_c:
    # w1 = 0.5 * exp(-2.0*3.0 - 3.0*0.4) = 0.5 * exp(-6.0 - 1.2) = 0.5 * exp(-7.2)
    # w2 = 0.4 * exp(-2.0*2.0 - 3.0*0.3) = 0.4 * exp(-4.0 - 0.9) = 0.4 * exp(-4.9)
    z = composed_kernel_generalized([p1, p2], lambda_=2.0, mu_=3.0)
    expected = 0.5 * math.exp(-7.2) + 0.4 * math.exp(-4.9)
    assert z[("S_a", "S_c")] == pytest.approx(expected)


