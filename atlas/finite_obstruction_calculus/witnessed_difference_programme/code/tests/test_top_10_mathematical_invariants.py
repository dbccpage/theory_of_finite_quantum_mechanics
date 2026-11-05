"""Top 10 Mathematical Invariant Tests across the Witnessed Difference Programme.

Executable finite evidence; AuthorityEffect: None.

This test module verifies the 10 foundational mathematical invariants across WDP:
1.  Projective Scaling Denominator Clearing (avoiding Phase 1 common denominator swell)
2.  Dual Certificate Infeasibility Bounds & Strong Duality (WDP-CH04-P07, obstruction.py)
3.  Fixed-repair & Subdivision Invariance of Quotient Defect (WDP-CH04-P09, complex_growth.py)
4.  Equivariant Obstruction & Fixed-Point Absence on Symmetric Carriers (WDP-CH03-P01, symmetry.py)
5.  Frustrated Spin Holonomy & Diagnostic Trichotomy (WDP-CH04-D02, WDP-CH04-P05, obstruction.py)
6.  Linear Quotient Observer Passivity & Kernel Preorder (WDP-CH10-P01, WDP-CH10-P02, quotient_observer.py)
7.  Finite Grammar Resolution & Pigeonhole Collision (WDP-CH10-P03, quotient_observer.py)
8.  Contextual System & Critical Context Separators (WDP-CH11-P01, context_witness.py)
9.  Orthogonal Projector Idempotent Energy Leakage Bound (WDP-CH05-P07, WDP-CH16-P04, truncation.py)
10. Profile-Relative Evaluator Completeness & Refusal Precedence (WDP-CH20-D01, relative_status.py, finite_profile_evaluator.py)
"""

from __future__ import annotations

from fractions import Fraction
import random
import pytest

from witnessed_difference.cochains import FiniteComplex
from witnessed_difference.native_functionals import dual_bound
from witnessed_difference.obstruction import (
    DEFAULT_PIVOT_BUDGET,
    DiagnosticClass,
    d0_adjoint,
    d0_matrix,
    exact_quotient_l1,
    obstruction_signature,
    solve_standard_lp,
    verify_quotient_certificate,
    verify_standard_lp,
)
from witnessed_difference.complex_growth import (
    attach_face,
    claim_growth_repair,
    growth_receipt,
    make_window,
    subdivide_edge,
)
from witnessed_difference.symmetry import (
    exhaustive_relation_audit,
    fixed_oriented_edges,
    fixed_points,
    invariant_binary_relations,
    invariant_strict_total_orders,
)
from witnessed_difference.quotient_observer import (
    check_passivity,
    grammar_resolution,
    kernel_le,
    make_linear_quotient_observer,
    observer_family_order,
)
from witnessed_difference.context_witness import (
    ContextualSystem,
    apply_coordinate_change,
    contextual_congruence,
    critical_context_witnesses,
    witness_rank,
)
from witnessed_difference.truncation import (
    truncation_leakage,
    validate_projector,
)
from witnessed_difference.rational_phase_witness import (
    rational_phase_and_readout_witness,
)
from witnessed_difference.relative_status import (
    Claim,
    ClaimStatus,
    EvaluationProfile,
    attach_finite_witness,
    route_claim,
)
from witnessed_difference.outcomes import (
    Accepted,
    AuthorityEffect,
    RefusalCode,
    Refused,
)
from finite_profile_evaluator import (
    Evidence,
    Profile,
    Status,
    evaluate,
    status_guards,
)


def _unwrap(outcome):
    assert isinstance(outcome, Accepted), f"Expected Accepted, got {outcome}"
    assert outcome.authority_effect is AuthorityEffect.NONE
    return outcome.value


# ==============================================================================
# 1. Projective Scaling Denominator Clearing
# ==============================================================================
def test_01_projective_scaling_eliminates_phase1_swell():
    """Verify that row-wise clearing of denominators avoids O(m * B) Phase 1 common denominator swell."""
    n = 6
    bit_len = 48
    rng = random.Random(101)
    vertices = tuple(f"v{i}" for i in range(n))
    edges = tuple((f"v{i}", f"v{j}") for i in range(n) for j in range(i + 1, n))
    comp = FiniteComplex(vertices, edges)
    m = len(edges)
    width = len(vertices)
    w = (Fraction(1),) * m

    cochain = [
        Fraction(rng.randint(-(1 << bit_len), 1 << bit_len), rng.randint(1, 1 << bit_len))
        for _ in edges
    ]
    d = d0_matrix(comp)

    # Standard rational formulation
    rows_std = [
        list(row) + [-entry for entry in row] + [Fraction(int(i == k)) for k in range(m)]
        + [-Fraction(int(i == k)) for k in range(m)]
        for i, row in enumerate(d)
    ]
    costs = [Fraction(0)] * (2 * width) + list(w) + list(w)

    # Projective row-cleared formulation: multiply row i by q_i
    rows_proj = []
    cochain_proj = []
    for i in range(m):
        q_i = cochain[i].denominator
        rows_proj.append([q_i * val for val in rows_std[i]])
        cochain_proj.append(cochain[i].numerator)

    std_phase1_bits = sum((abs(x) for x in cochain), start=Fraction(0)).denominator.bit_length()
    proj_phase1_bits = sum((abs(b.numerator) for b in cochain), start=0).bit_length()

    # Assert significant bit reduction at initialization
    assert proj_phase1_bits < std_phase1_bits
    assert std_phase1_bits / max(1, proj_phase1_bits) >= 4.0

    solved_std = _unwrap(solve_standard_lp(costs, rows_std, cochain, max_pivots=DEFAULT_PIVOT_BUDGET))
    solved_proj = _unwrap(solve_standard_lp(costs, rows_proj, cochain_proj, max_pivots=DEFAULT_PIVOT_BUDGET))

    assert verify_standard_lp(costs, rows_std, cochain, solved_std)
    assert verify_standard_lp(costs, rows_proj, cochain_proj, solved_proj)
    assert solved_std.value == solved_proj.value


# ==============================================================================
# 2. Dual Certificate Infeasibility Bounds & Strong Duality
# ==============================================================================
def test_02_dual_certificate_infeasibility_bounds_and_duality():
    """Verify strong duality, dual feasibility |y_e| <= w_e, and divergence-free annihilation."""
    comp = FiniteComplex((0, 1, 2, 3), ((0, 1), (1, 2), (2, 3), (0, 3)))
    cochain = {(0, 1): Fraction(1), (1, 2): Fraction(1), (2, 3): Fraction(1), (0, 3): Fraction(-1)}
    weights = {(0, 1): Fraction(2), (1, 2): Fraction(3), (2, 3): Fraction(2), (0, 3): Fraction(3)}

    cert = _unwrap(exact_quotient_l1(comp, cochain, weights))
    reverified = _unwrap(verify_quotient_certificate(cert))
    assert reverified == cert

    # 1. Strong Duality: primal value equals dual pairing
    dual_pairing = dual_bound(d0_matrix(comp), len(comp.vertices), cert.cochain, cert.weights, cert.dual)
    assert dual_pairing == cert.value

    # 2. Dual Feasibility: |y_e| <= w_e
    for y_e, w_e in zip(cert.dual, cert.weights):
        assert abs(y_e) <= w_e

    # 3. Divergence-free: d0* y == 0
    divergence = d0_adjoint(comp, dict(zip(comp.edges, cert.dual)))
    assert all(div == 0 for div in divergence.values())

    # 4. Tampering detection: perturbed dual must be rejected
    perturbed_dual = list(cert.dual)
    perturbed_dual[0] += Fraction(1, 100)
    bad_cert = cert.__class__(
        cert.complex_, cert.cochain, cert.weights, cert.potential, cert.residual, cert.value, tuple(perturbed_dual)
    )
    outcome = verify_quotient_certificate(bad_cert)
    assert isinstance(outcome, Refused)
    assert outcome.code is RefusalCode.CERTIFICATE_MISMATCH


# ==============================================================================
# 3. Fixed-repair & Subdivision Invariance of Quotient Defect
# ==============================================================================
def test_03_fixed_repair_and_subdivision_invariance_of_quotient_defect():
    """Verify that attaching 2-simplices and subdividing edges strictly preserve Phi_1([h])."""
    # Base complex: cycle with one chord
    vertices = (0, 1, 2, 3)
    edges = ((0, 1), (1, 2), (2, 3), (0, 3), (0, 2))
    faces = ((0, 1, 2),)
    comp = FiniteComplex(vertices, edges, faces)
    cochain = {(0, 1): 1, (1, 2): 1, (2, 3): 1, (0, 3): 0, (0, 2): 2}

    window = _unwrap(make_window(comp, cochain))
    receipt_before = _unwrap(growth_receipt(window, window))
    assert receipt_before.phi1_change == 0

    # 1. Attach second face (0, 2, 3) to form a disk
    attached_window = _unwrap(attach_face(window, (0, 2, 3)))
    receipt_attached = _unwrap(growth_receipt(window, attached_window))
    # Face attachment leaves d0, weights and the cochain unchanged, so Phi_1 is unchanged.
    # It can change H1 and need not preserve homotopy type.
    assert receipt_attached.before_phi1 == receipt_attached.after_phi1

    # 2. Subdivide edge (2, 3) into (2, 4) and (4, 3)
    subdivided_window = _unwrap(subdivide_edge(window, (2, 3), 4, Fraction(1, 2)))
    receipt_subdivided = _unwrap(growth_receipt(window, subdivided_window))
    # Subdivision invariance: subdividing edge preserves Phi_1 exactly!
    assert receipt_subdivided.before_phi1 == receipt_subdivided.after_phi1

    # 3. Carrier changes never constitute a repair
    repair_claim = claim_growth_repair(receipt_attached)
    assert isinstance(repair_claim, Refused)
    assert repair_claim.code is RefusalCode.SCOPE_VIOLATION


# ==============================================================================
# 4. Equivariant Obstruction & Fixed-Point Absence on Symmetric Carriers
# ==============================================================================
def test_04_equivariant_obstruction_and_fixed_points_on_symmetric_carriers():
    """Verify absence of equivariant point selection and strict orderings on symmetric carriers."""
    for n in (2, 3, 4):
        # Absence of fixed points under Sn
        assert fixed_points(n) == ()
        # Absence of fixed oriented edges under Sn
        assert fixed_oriented_edges(n) == ()
        # Absence of invariant strict total orders under Sn
        assert invariant_strict_total_orders(n) == ()

    # For n = 3, exactly 2^2 = 4 invariant binary relations exist
    inv_rel_3 = invariant_binary_relations(3)
    assert len(inv_rel_3) == 4
    # The 4 relations: empty, diagonal, off-diagonal, full
    audit = exhaustive_relation_audit(3)
    assert audit["invariant_relation_count"] == 4
    assert audit["invariant_strict_order_count"] == 0
    assert audit["relation_count"] == 512  # 2^(3*3) = 2^9 = 512


# ==============================================================================
# 5. Frustrated Spin Holonomy & Diagnostic Trichotomy
# ==============================================================================
def test_05_frustrated_spin_holonomy_and_diagnostic_trichotomy():
    """Verify frustrated cycle holonomy and the three mutually exclusive diagnostic states."""
    # Frustrated C5: spin flip across closing edge
    c5 = FiniteComplex((0, 1, 2, 3, 4), ((0, 1), (1, 2), (2, 3), (3, 4), (0, 4)))

    # 1. Closed residual: non-zero cycle holonomy with no faces declared (Gamma2 = 0, Phi1 > 0)
    cochain_frustrated = {(0, 1): 1, (1, 2): 1, (2, 3): 1, (3, 4): 1, (0, 4): -1}
    sig_residual = _unwrap(obstruction_signature(c5, cochain_frustrated, closure_declared=True))
    assert sig_residual.phi1 > 0
    assert sig_residual.gamma2 == 0
    assert sig_residual.diagnostic_class is DiagnosticClass.CLOSED_RESIDUAL

    # 2. Exact class: exact gradient of a potential function (Phi1 = 0, Gamma2 = 0)
    pot = {0: 10, 1: 15, 2: 7, 3: 20, 4: 12}
    cochain_exact = {(u, v): pot[v] - pot[u] for u, v in c5.edges}
    sig_exact = _unwrap(obstruction_signature(c5, cochain_exact, closure_declared=True))
    assert sig_exact.phi1 == 0
    assert sig_exact.gamma2 == 0
    assert sig_exact.diagnostic_class is DiagnosticClass.EXACT_CLASS

    # 3. Active closure failure: with a face attached, non-zero boundary curl (Gamma2 > 0)
    c5_with_face = FiniteComplex(
        (0, 1, 2, 3, 4),
        ((0, 1), (1, 2), (2, 3), (3, 4), (0, 4), (0, 2)),
        ((0, 1, 2),),
    )
    cochain_active = {(0, 1): 1, (1, 2): 1, (2, 3): 0, (3, 4): 0, (0, 4): 0, (0, 2): 0}
    sig_active = _unwrap(obstruction_signature(c5_with_face, cochain_active, closure_declared=True))
    assert sig_active.gamma2 > 0
    assert sig_active.diagnostic_class is DiagnosticClass.ACTIVE_CLOSURE_FAILURE


# ==============================================================================
# 6. Linear Quotient Observer Passivity & Kernel Preorder
# ==============================================================================
def test_06_linear_quotient_observer_passivity_and_kernel_preorder():
    """Verify observer passivity Phi_O(R delta) <= Phi_1([delta]) and kernel containment preorder."""
    comp = FiniteComplex((0, 1, 2, 3), ((0, 1), (1, 2), (2, 3), (0, 3)), ())
    # A cycle report map that annihilates d0: (0, 1) + (1, 2) + (2, 3) - (0, 3)
    cycle_row = (Fraction(1), Fraction(1), Fraction(1), Fraction(-1))
    observer = _unwrap(make_linear_quotient_observer(comp, (cycle_row,)))

    # Test passivity for various cochains
    for delta_vals in [(1, 0, 0, 0), (1, 1, 1, -1), (2, 3, 5, 7)]:
        cochain = dict(zip(comp.edges, delta_vals))
        receipt = _unwrap(check_passivity(observer, cochain))
        # Passivity invariant: observer norm never exceeds quotient defect!
        assert receipt.observer_norm <= receipt.phi1
        assert receipt.exact_stays_exact

    # Kernel preorder: full cycle vs zero row vs independent row
    zero_row = (Fraction(0), Fraction(0), Fraction(0), Fraction(0))
    obs_cycle = observer
    obs_zero = _unwrap(make_linear_quotient_observer(comp, (zero_row,)))

    # ker(obs_cycle) is contained in ker(obs_zero) because ker(obs_zero) is the whole space
    assert kernel_le(obs_cycle, obs_zero) is True

    family = {"cycle": obs_cycle, "zero": obs_zero}
    order = _unwrap(observer_family_order(family))
    assert ("cycle", "zero") in order.relation


# ==============================================================================
# 7. Finite Grammar Resolution & Pigeonhole Collision
# ==============================================================================
def test_07_finite_grammar_resolution_and_pigeonhole_collision():
    """Verify that reporting |C| classes through a grammar of size |G| < |C| forces collisions."""
    classes = ("c1", "c2", "c3", "c4", "c5")
    # Sub-capacity grammar of size 3
    grammar = frozenset({"W1", "W2", "W3"})
    report_colliding = {"c1": "W1", "c2": "W2", "c3": "W3", "c4": "W1", "c5": "W2"}

    receipt_col = _unwrap(grammar_resolution(classes, report_colliding, grammar))
    assert receipt_col.pigeonhole_forced is True
    assert receipt_col.collision is not None
    assert receipt_col.visible_classes <= 3

    # Adequate capacity grammar of size 5
    grammar_large = frozenset({"W1", "W2", "W3", "W4", "W5"})
    report_injective = {"c1": "W1", "c2": "W2", "c3": "W3", "c4": "W4", "c5": "W5"}
    receipt_inj = _unwrap(grammar_resolution(classes, report_injective, grammar_large))
    assert receipt_inj.pigeonhole_forced is False
    assert receipt_inj.collision is None
    assert receipt_inj.visible_classes == 5


# ==============================================================================
# 8. Contextual System & Critical Context Separators
# ==============================================================================
def test_08_contextual_system_and_critical_context_separators():
    """Verify critical context witnesses exposing failure of report-fiber preservation and witness rank."""
    states = ("s1", "s2", "s3", "s4")
    # Context C0 is identity, C1 swaps s1 and s3
    contexts = {
        "C0": {"s1": "s1", "s2": "s2", "s3": "s3", "s4": "s4"},
        "C1": {"s1": "s3", "s2": "s2", "s3": "s1", "s4": "s4"},
    }
    # States s1 and s2 have identical local profiles: p(s1) = p(s2) = (1, 0)
    profile = {
        "s1": (Fraction(1), Fraction(0)),
        "s2": (Fraction(1), Fraction(0)),
        "s3": (Fraction(0), Fraction(1)),
        "s4": (Fraction(0), Fraction(1)),
    }
    system = ContextualSystem(states, contexts, profile)

    # Congruence identifies s1 ~ s2 and s3 ~ s4
    congruence = _unwrap(contextual_congruence(system))
    assert frozenset({"s1", "s2"}) in congruence
    assert frozenset({"s3", "s4"}) in congruence

    # Critical context witnesses: under C1, rho(C1) s1 = s3, exposing a difference!
    witnesses = _unwrap(critical_context_witnesses(system))
    assert len(witnesses) > 0
    w0 = witnesses[0]
    assert (w0.x, w0.y) == ("s1", "s2")
    assert w0.context == "C1"
    assert w0.exposed == (Fraction(-1), Fraction(1))

    # Exact witness rank is 1
    rank = _unwrap(witness_rank(system))
    assert rank == 1

    # Invertible coordinate change preserves witness rank
    coord_change = ((Fraction(2), Fraction(1)), (Fraction(1), Fraction(1)))
    transformed = _unwrap(apply_coordinate_change(system, coord_change))
    assert _unwrap(witness_rank(transformed)) == 1


# ==============================================================================
# 9. Orthogonal Projector Idempotent Energy Leakage Bound
# ==============================================================================
def test_09_orthogonal_projector_idempotent_energy_leakage():
    """Verify that truncation under idempotent orthogonal projector satisfies P A* A P = (PAP)*(PAP) + L_P."""
    # 2x2 non-commuting system
    a = (
        (Fraction(1), Fraction(2)),
        (Fraction(3), Fraction(4)),
    )
    # Projector onto first coordinate: P = diag(1, 0)
    p = (
        (Fraction(1), Fraction(0)),
        (Fraction(0), Fraction(0)),
    )
    _unwrap(validate_projector(p, 2))

    leakage = _unwrap(truncation_leakage(a, p))
    # Exact algebraic energy conservation
    assert leakage.identity_holds is True
    # The leakage certificate is positive semi-definite
    assert leakage.leakage_certificate.positive_semidefinite is True
    # Off-diagonal element in A causes leakage: range is not invariant
    assert leakage.range_invariant is False
    assert leakage.leakage_free is False

    # For an operator that commutes with P, leakage is exactly zero
    a_diag = (
        (Fraction(5), Fraction(0)),
        (Fraction(0), Fraction(7)),
    )
    leakage_zero = _unwrap(truncation_leakage(a_diag, p))
    assert leakage_zero.identity_holds is True
    assert leakage_zero.range_invariant is True
    assert leakage_zero.leakage_free is True

    # Non-idempotent matrix must be rejected by validate_projector
    bad_p = (
        (Fraction(2), Fraction(0)),
        (Fraction(0), Fraction(0)),
    )
    assert isinstance(validate_projector(bad_p, 2), Refused)


# ==============================================================================
# 10. Profile-Relative Evaluator Completeness & Refusal Precedence
# ==============================================================================
def test_10_profile_relative_evaluator_completeness_and_refusal_precedence():
    """Verify 5-status partition and that outside-profile strictly precedes refusal."""
    table = (
        ("q_proved", True),
        ("q_refuted", False),
        ("q_undetermined", True),
        ("q_refused", True),
        ("q_outside", True),
    )
    admitted = frozenset({"q_proved", "q_refuted", "q_undetermined", "q_refused"})
    refused = frozenset({"q_refused"})
    profile = Profile(table=table, admitted=admitted, refused=refused, budget=2)

    ev_true = Evidence("q_proved", True)
    ev_false = Evidence("q_refuted", False)
    ev_refused = Evidence("q_refused", True)
    ev_outside = Evidence("q_outside", True)

    # 1. Proved: admitted, allowed, and replayed evidence matches
    assert evaluate(profile, "q_proved", (ev_true,)) is Status.PROVED

    # 2. Refuted: admitted, allowed, and replayed counter-evidence matches
    assert evaluate(profile, "q_refuted", (ev_false,)) is Status.REFUTED

    # 3. Undetermined: admitted and allowed, but no matching evidence supplied
    assert evaluate(profile, "q_undetermined", ()) is Status.UNDETERMINED

    # 4. Refused: in refused set, taking precedence over supplied candidate evidence
    assert evaluate(profile, "q_refused", (ev_refused,)) is Status.REFUSED

    # 5. OutsideProfile: not in admitted set, taking precedence over refusal and evidence
    assert evaluate(profile, "q_outside", (ev_outside,)) is Status.OUTSIDE_PROFILE

    # Status guards are mutually exclusive and partition the space
    for q in ("q_proved", "q_refuted", "q_undetermined", "q_refused", "q_outside"):
        guards = status_guards(profile, q, (ev_true, ev_false))
        assert sum(1 for g in guards if g) == 1

    # Verify claim status routing from relative_status.py
    eval_prof = EvaluationProfile("prof_test", frozenset({"WDP-01"}))
    claim_in = Claim("WDP-01", ClaimStatus.FINITE_PROPOSITION)
    claim_out = Claim("WDP-99", ClaimStatus.FINITE_PROPOSITION)

    routed_in = route_claim(claim_in, eval_prof)
    routed_out = route_claim(claim_out, eval_prof)
    assert routed_in.relative_status is ClaimStatus.FINITE_PROPOSITION
    assert routed_out.relative_status is ClaimStatus.OUTSIDE_PROFILE

    # Attaching a finite witness to an outside-profile claim does not promote it
    witnessed_out = attach_finite_witness(routed_out, "WITNESS-001")
    assert witnessed_out.relative_status is ClaimStatus.OUTSIDE_PROFILE
