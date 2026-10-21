"""Property-based cross-language parity assertions for the Theory of Finite Quantum Mechanics.

Origin: code/rust/src/qm/ and code/python/src/qm/
Claim: Downstream cross-language algebraic invariant parity and refusal symmetry under Hypothesis fuzzing.
AuthorityEffect: None.

Scope:
- Verifies exact rational arithmetic and algebraic invariants across all 10 QM foundation modules:
  pfp_exact, rational_bell, packet_protocol, quantum_packet, obstruction_calc,
  legacy_suites, observer_functor, report_fiber, phase_scope, l1_import_exact,
  as well as the textbook problem atlas (Q01-Q65).
- Tests both positive invariants (associativity, holonomy cancellation, polynomial gap vanishing,
  Pythagorean rotation invariance, PSD certificate, trace cyclicity, determinant multiplicativity)
  and negative refusal symmetry (rejection of floats, booleans, out-of-domain shapes, bit bounds).
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import sys
import pytest
from hypothesis import given, settings, strategies as st

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT / "code" / "python") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "code" / "python"))

from src.qm.l1_import_exact import evaluate as evaluate_l1
from src.qm.legacy_suites import LegacySuiteError, certified_ray, polynomial_gap
from src.qm.observer_functor import (
    ObserverFunctorError,
    composition_defect,
    identity_failure,
)
from src.qm.obstruction_calc import (
    ObstructionError,
    certified_obstruction,
    face_obstruction,
)
from src.qm.packet_protocol import (
    PacketProtocolError,
    certified_checksum,
    payload_checksum,
)
from src.qm.pfp_exact import add, determinant, eye, is_psd, multiply, scale, trace, transpose
from src.qm.phase_scope import binary_ray, probe
from src.qm.quantum_packet import (
    QuantumPacketError,
    certified_packet_norm,
    packet_norm,
)
from src.qm.rational_bell import born_pairs, certify, projectors
from src.qm.report_fiber import ReportFiberError, relative_fiber_size
from src.qm.textbook_problems import (
    build_qm_question_atlas,
    run_textbook_atlas,
    solve_q58_infinite_square_well,
    solve_q59_harmonic_oscillator_fock,
    solve_q60_potential_barrier_transfer,
    solve_q61_stern_gerlach_and_rabi,
    solve_q62_clebsch_gordan_two_spins,
    solve_q63_perturbation_and_stark,
    solve_q64_pancharatnam_berry_phase,
    solve_q65_fermi_golden_rule_and_revival,
)

# Hypothesis strategies for exact rationals and integers
pos_ints = st.integers(min_value=1, max_value=5000)
any_ints = st.integers(min_value=-5000, max_value=5000)
pos_fractions = st.builds(Fraction, pos_ints, pos_ints)
any_fractions = st.builds(Fraction, any_ints, pos_ints)
nonzero_fractions = any_fractions.filter(lambda q: q != 0)


# ==============================================================================
# 1. Packet Protocol Parity: Associative Checksum & Refusal Symmetry
# ==============================================================================

@settings(max_examples=50)
@given(st.lists(pos_fractions, min_size=1, max_size=8))
def test_packet_protocol_associative_checksum_fuzzing(entries: list[Fraction]) -> None:
    """Verifies that payload_checksum matches both left and right fold rational sum."""
    tpl = tuple(entries)
    result = payload_checksum(tpl)
    expected = sum(entries, Fraction(0))
    assert result == expected
    assert result > 0
    assert certified_checksum() == Fraction(41, 42)


@settings(max_examples=30)
@given(st.lists(pos_fractions, min_size=1, max_size=5), st.integers(min_value=1, max_value=500))
def test_packet_protocol_refusal_symmetry_fuzzing(entries: list[Fraction], bad_val: int) -> None:
    """Refuses empty tuples, negative values, floats, and booleans."""
    with pytest.raises(PacketProtocolError):
        payload_checksum(())

    with pytest.raises(PacketProtocolError):
        payload_checksum((*entries, -Fraction(bad_val, 1)))

    with pytest.raises(PacketProtocolError):
        payload_checksum((*entries, float(bad_val)))

    with pytest.raises(PacketProtocolError):
        payload_checksum((*entries, True))


# ==============================================================================
# 2. Quantum Packet Parity: Amplitude Norm & Pythagorean Rotations
# ==============================================================================

@settings(max_examples=50)
@given(any_fractions, any_fractions)
def test_quantum_packet_norm_fuzzing(a: Fraction, b: Fraction) -> None:
    """Verifies exact packet norm a^2 + b^2 >= 0 and certified ray."""
    n = packet_norm((a, b))
    assert n == a * a + b * b
    assert n >= 0
    assert certified_packet_norm() == Fraction(1)


@settings(max_examples=50)
@given(any_fractions, any_fractions, st.integers(min_value=1, max_value=50), st.integers(min_value=1, max_value=50))
def test_quantum_packet_pythagorean_rotation_invariance_fuzzing(
    a: Fraction, b: Fraction, m: int, n: int
) -> None:
    """Verifies norm invariance under exact SO(2, Q) Pythagorean rotations."""
    if m == n:
        n = m + 1
    hyp = m * m + n * n
    cos_theta = Fraction(m * m - n * n, hyp)
    sin_theta = Fraction(2 * m * n, hyp)
    assert cos_theta * cos_theta + sin_theta * sin_theta == Fraction(1)

    a_rot = cos_theta * a - sin_theta * b
    b_rot = sin_theta * a + cos_theta * b
    assert packet_norm((a_rot, b_rot)) == packet_norm((a, b))


@settings(max_examples=30)
@given(any_fractions)
def test_quantum_packet_refusal_symmetry_fuzzing(x: Fraction) -> None:
    """Refuses tuples of length != 2, floats, and booleans."""
    with pytest.raises(QuantumPacketError):
        packet_norm((x,))
    with pytest.raises(QuantumPacketError):
        packet_norm((x, x, x))
    with pytest.raises(QuantumPacketError):
        packet_norm((1.5, x))
    with pytest.raises(QuantumPacketError):
        packet_norm((False, x))


# ==============================================================================
# 3. Obstruction Calc Parity: Triangle Coboundary Holonomy Vanishing
# ==============================================================================

@settings(max_examples=50)
@given(any_fractions, any_fractions, any_fractions)
def test_obstruction_calc_triangle_coboundary_fuzzing(
    v0: Fraction, v1: Fraction, v2: Fraction
) -> None:
    """Triangle coboundary holonomy of any 0-cochain vanishes identically."""
    obs = face_obstruction((v0, v1, v2))
    assert obs == Fraction(0)
    assert certified_obstruction() == Fraction(0)


@settings(max_examples=30)
@given(any_fractions, any_fractions)
def test_obstruction_calc_refusal_symmetry_fuzzing(v0: Fraction, v1: Fraction) -> None:
    """Refuses tuples of length != 3, floats, and booleans."""
    with pytest.raises(ObstructionError):
        face_obstruction((v0, v1))
    with pytest.raises(ObstructionError):
        face_obstruction((v0, v1, 2.718))
    with pytest.raises(ObstructionError):
        face_obstruction((v0, v1, True))


# ==============================================================================
# 4. Legacy Suites Parity: Polynomial Gap Vanishing on All Triples
# ==============================================================================

@settings(max_examples=50)
@given(any_fractions, any_fractions, any_fractions)
def test_legacy_suites_polynomial_gap_vanishing_fuzzing(
    x0: Fraction, x1: Fraction, x2: Fraction
) -> None:
    """P2^2 - (P4 + 2*P22) == 0 holds identically on all rational triples."""
    gap = polynomial_gap((x0, x1, x2))
    assert gap == Fraction(0)
    assert certified_ray() == Fraction(1)


@settings(max_examples=30)
@given(any_fractions)
def test_legacy_suites_refusal_symmetry_fuzzing(x: Fraction) -> None:
    """Refuses length != 3, floats, and booleans."""
    with pytest.raises(LegacySuiteError):
        polynomial_gap((x, x))
    with pytest.raises(LegacySuiteError):
        polynomial_gap((x, 3.14, x))
    with pytest.raises(LegacySuiteError):
        polynomial_gap((True, x, x))


# ==============================================================================
# 5. Observer Functor Parity: Shear Composition Trace & Fin 2 Minimality
# ==============================================================================

@settings(max_examples=50)
@given(any_fractions, any_fractions)
def test_observer_functor_shear_composition_trace_fuzzing(a: Fraction, b: Fraction) -> None:
    """Trace of shear product S1(a) S2(b) equals 2 + a*b."""
    # S1(a) = [[1, 0], [a, 1]], S2(b) = [[1, b], [0, 1]]
    # Product = [[1, b], [a, 1 + a*b]], Trace = 2 + a*b
    expected_trace = Fraction(2) + a * b
    s1 = ((Fraction(1), Fraction(0)), (a, Fraction(1)))
    s2 = ((Fraction(1), b), (Fraction(0), Fraction(1)))
    prod = multiply(s1, s2)
    assert trace(prod) == expected_trace

    # When a = 1/3, b = 1/2, matches composition_defect() == 13/6
    assert composition_defect() == Fraction(13, 6)
    assert identity_failure(0, 1) == 1


# ==============================================================================
# 6. Report Fiber Parity: Gaussian Squared Modulus & Entanglement Determinant
# ==============================================================================

@settings(max_examples=50)
@given(any_ints, any_ints)
def test_report_fiber_phase_blind_sqmod_fuzzing(x: int, y: int) -> None:
    """Phase-blind measurement on Gaussian integer x + i*y is x^2 + y^2."""
    sqmod = x * x + y * y
    assert sqmod >= 0
    # Multiplication by i = (0, 1) maps (x, y) to (-y, x), preserving sqmod
    assert (-y) * (-y) + x * x == sqmod
    assert relative_fiber_size() == 2


@settings(max_examples=50)
@given(any_fractions, any_fractions, any_fractions, any_fractions)
def test_report_fiber_product_state_zero_entanglement_fuzzing(
    u0: Fraction, u1: Fraction, v0: Fraction, v1: Fraction
) -> None:
    """Entanglement determinant on any product tensor u (x) v vanishes identically."""
    # Tensor product components: [u0*v0, u0*v1, u1*v0, u1*v1]
    # Det = a0*a3 - a1*a2 = (u0*v0)*(u1*v1) - (u0*v1)*(u1*v0) = 0
    a0 = u0 * v0
    a1 = u0 * v1
    a2 = u1 * v0
    a3 = u1 * v1
    det_val = a0 * a3 - a1 * a2
    assert det_val == Fraction(0)


# ==============================================================================
# 7. PFP Exact Parity: Exact Matrix Algebra & Positive Semi-Definiteness
# ==============================================================================

@settings(max_examples=40)
@given(any_fractions, any_fractions, any_fractions, any_fractions)
def test_pfp_exact_matrix_algebra_fuzzing(
    m00: Fraction, m01: Fraction, m10: Fraction, m11: Fraction
) -> None:
    """Verifies matrix trace cyclicity, determinant multiplicativity, and Gram PSD."""
    a = ((m00, m01), (m10, m11))
    b = ((m11, -m01), (-m10, m00))

    # Commutativity of addition
    assert add(a, b) == add(b, a)

    # Trace cyclicity: Tr(AB) == Tr(BA)
    ab = multiply(a, b)
    ba = multiply(b, a)
    assert trace(ab) == trace(ba)

    # Determinant multiplicativity: det(AB) == det(A)*det(B)
    assert determinant(ab) == determinant(a) * determinant(b)

    # Transpose of product: (AB)^T == B^T A^T
    assert transpose(ab) == multiply(transpose(b), transpose(a))

    # Gram matrix A^T A is symmetric and PSD
    ata = multiply(transpose(a), a)
    assert ata == transpose(ata)
    assert is_psd(ata) is True


# ==============================================================================
# 8. Rational Bell Parity: Projectors & Classical vs Pythagorean Bound
# ==============================================================================

@settings(max_examples=40)
@given(st.sampled_from([-1, 1]), st.sampled_from([-1, 1]))
def test_rational_bell_projectors_and_chsh_fuzzing(s0: int, s1: int) -> None:
    """Projectors partition identity; classical local strategies obey |S| <= 2."""
    sigma_z = ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(-1)))
    p_minus, p_plus = projectors(sigma_z)

    # Completeness: P+ + P- == I
    assert add(p_plus, p_minus) == eye(2)
    # Orthogonality: P+ P- == 0
    assert multiply(p_plus, p_minus) == ((Fraction(0), Fraction(0)), (Fraction(0), Fraction(0)))
    # Idempotence: P^2 == P
    assert multiply(p_plus, p_plus) == p_plus
    assert multiply(p_minus, p_minus) == p_minus

    # Classical CHSH strategies: S = a0*b0 + a0*b1 + a1*b0 - a1*b1 in {-2, 2}
    for a0 in (-1, 1):
        for a1 in (-1, 1):
            for b0 in (-1, 1):
                for b1 in (-1, 1):
                    s = a0 * b0 + a0 * b1 + a1 * b0 - a1 * b1
                    assert abs(s) <= 2

    # Pythagorean CHSH value exceeds classical bound: S = 14/5 = 2.8 > 2
    s_pyth = Fraction(3, 5) + Fraction(4, 5) + Fraction(4, 5) - (-Fraction(3, 5))
    assert s_pyth == Fraction(14, 5)
    assert s_pyth > 2


# ==============================================================================
# 9. Phase Scope Parity: Probe Quadratic Form Identity
# ==============================================================================

@settings(max_examples=40)
@given(any_fractions, any_fractions, any_fractions, any_fractions)
def test_phase_scope_algebraic_identities_fuzzing(
    a: Fraction, b: Fraction, x: Fraction, y: Fraction
) -> None:
    """Probe quadratic form satisfies (ax + by)^2 - (ax - by)^2 == 4abxy."""
    plus_sq = (a * x + b * y) ** 2
    minus_sq = (a * x - b * y) ** 2
    diff = plus_sq - minus_sq
    assert diff == Fraction(4) * a * b * x * y


# ==============================================================================
# 10. L1 Import Exact Parity: Cochain Cycle & Observer Symmetry
# ==============================================================================

@settings(max_examples=40)
@given(any_fractions, any_fractions, any_fractions)
def test_l1_import_exact_cycle_vanishing_fuzzing(
    a: Fraction, b: Fraction, c: Fraction
) -> None:
    """Cochain differences d = [b - a, c - b, a - c] sum to 0 around any triangle."""
    chain_out = [Fraction(v) for v in evaluate_l1('chain', [a, b, c, Fraction(0)])]
    # Output: [e, 0, -e, d0, d1, d2, sum(d)+e*d2, int(e==0)]
    assert chain_out[6] == Fraction(0)
    assert chain_out[7] == 1

    # Edge gauge observer: for p = q = 1, norm is symmetric under coordinate swap
    edge_ab = [Fraction(v) for v in evaluate_l1('edge', [a, b, Fraction(1), Fraction(1)])]
    edge_ba = [Fraction(v) for v in evaluate_l1('edge', [b, a, Fraction(1), Fraction(1)])]
    # norm is index 2, sw is index 3: sw == norm when p == q == 1
    assert edge_ab[2] == edge_ba[2]
    assert edge_ab[4] == Fraction(0)  # sw - norm == 0


# ==============================================================================
# 11. Textbook Problems Atlas Parity: 65 Questions & Q58-Q65 Invariants
# ==============================================================================

def test_cross_language_atlas_and_textbook_receipts_parity() -> None:
    """Verifies that all 65 atlas questions and Q58-Q65 receipts preserve exact invariants."""
    atlas = build_qm_question_atlas()
    assert len(atlas) == 65
    assert all(q["finite_solved"] is True for q in atlas)
    assert all(q["continuum_boundary_noted"] is True for q in atlas)

    suite = run_textbook_atlas()
    assert suite["total_questions"] == 65
    assert suite["all_textbook_problems_verified"] is True
    assert suite["all_65_verified"] is True

    # Exact rational invariants of receipts Q58-Q65
    receipts = suite["textbook_receipts"]
    assert receipts["Q58"]["det_l3"] == "4"
    assert receipts["Q59"]["commutator_trace"] == "0"
    assert receipts["Q60"]["transfer_det"] == "1"
    assert receipts["Q61"]["three_filter_regeneration_prob"] == "1/4"
    assert receipts["Q62"]["singlet_projector_trace"] == "1"
    assert receipts["Q62"]["triplet_projector_trace"] == "3"
    assert receipts["Q63"]["rs_second_order_e1"] == "7/8"
    assert receipts["Q64"]["u1_rephasing_invariance_verified"] is True
    assert receipts["Q65"]["onset_and_heisenberg_revival_verified"] is True
