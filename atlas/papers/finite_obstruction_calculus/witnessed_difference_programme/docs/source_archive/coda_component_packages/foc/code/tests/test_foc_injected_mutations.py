"""Injected-fault mutants for CODA-FOC decision procedures.

AuthorityEffect: None.
Each mutant locally redefines one production decision. Tests assert that the
mutant disagrees with the real oracle on a known packet, so the suite kills
the fault if it is ever injected into production.
"""

from dataclasses import replace

import pytest
from finite_obstruction import (
    Diagnostic,
    FiniteObstructionPacket,
    diagnose,
    is_full_subspace_annihilator,
    quotient_certificate,
)
from sympy import Abs, Matrix, Rational, simplify


def coherent_packet() -> FiniteObstructionPacket:
    return FiniteObstructionPacket.create(
        d0=[[1], [0]],
        d1=[[0, 0]],
        a2=Matrix.zeros(1, 0),
        w1=[1, 1],
        w2=[1],
    )


def nonclosed_packet() -> FiniteObstructionPacket:
    return FiniteObstructionPacket.create(
        d0=[[1], [0]],
        d1=[[0, 1]],
        a2=Matrix.zeros(1, 0),
        w1=[1, 1],
        w2=[2],
    )


def mutant_diagnose_phi1_always_zero(packet, defect):
    """Treat Phi1==0 as always true, so every defect is ExactRepair."""
    result = diagnose(packet, defect)
    phi1_is_zero = True
    if phi1_is_zero:
        diagnostic = Diagnostic.EXACT_REPAIR
    elif result.gamma2.value == 0:
        diagnostic = Diagnostic.COHERENT_RESIDUAL
    else:
        diagnostic = Diagnostic.NONCLOSED_DEFECT
    return replace(result, diagnostic=diagnostic)


def mutant_l2_projection_scored_in_l1(repair_map, vector, _weights) -> Rational:
    """Swap the L1 quotient for an L2 projection, then score the residual in L1."""
    matrix = Matrix(repair_map)
    x = Matrix(vector)
    gram = matrix.T * matrix
    coeff = gram.inv() * (matrix.T * x)
    residual = x - matrix * coeff
    return simplify(sum((Abs(entry) for entry in residual), start=Rational(0)))


def mutant_diagnose_drop_d1d0(packet, defect) -> Diagnostic:
    """Drop the cochain check d1*d0=0 and classify anyway."""
    phi1 = quotient_certificate(packet.d0, defect, packet.w1)
    defect_column = Matrix(defect)
    gamma2 = quotient_certificate(packet.a2, packet.d1 * defect_column, packet.w2)
    if phi1.value == 0:
        return Diagnostic.EXACT_REPAIR
    if gamma2.value == 0:
        return Diagnostic.COHERENT_RESIDUAL
    return Diagnostic.NONCLOSED_DEFECT


def mutant_generator_only_as_full_subspace(repair_map, functional) -> bool:
    """Accept annihilation of the first generator as full-subspace annihilation."""
    matrix = Matrix(repair_map)
    z = Matrix(functional)
    if matrix.cols == 0:
        return True
    return bool((matrix[:, 0].T * z)[0, 0] == 0)


def test_mutant_phi1_always_zero_killed_on_known_packets() -> None:
    # Invariant: ExactRepair is Phi1==0, not a constant classifier.
    exact_real = diagnose(coherent_packet(), [3, 0])
    exact_mutant = mutant_diagnose_phi1_always_zero(coherent_packet(), [3, 0])
    assert exact_real.diagnostic is Diagnostic.EXACT_REPAIR
    assert exact_mutant.diagnostic is Diagnostic.EXACT_REPAIR

    residual_real = diagnose(coherent_packet(), [0, 4])
    residual_mutant = mutant_diagnose_phi1_always_zero(coherent_packet(), [0, 4])
    assert residual_real.diagnostic is Diagnostic.COHERENT_RESIDUAL
    assert residual_mutant.diagnostic is Diagnostic.EXACT_REPAIR
    assert residual_mutant.diagnostic is not residual_real.diagnostic

    nonclosed_real = diagnose(nonclosed_packet(), [0, 4])
    nonclosed_mutant = mutant_diagnose_phi1_always_zero(nonclosed_packet(), [0, 4])
    assert nonclosed_real.diagnostic is Diagnostic.NONCLOSED_DEFECT
    assert nonclosed_mutant.diagnostic is Diagnostic.EXACT_REPAIR
    assert nonclosed_mutant.diagnostic is not nonclosed_real.diagnostic


def test_mutant_l2_scored_in_l1_killed_on_column_instance() -> None:
    # Invariant: A=(1,1,1)^T, x=(0,0,10) has L1 value 10, not the L2 residual 40/3.
    repair_map = Matrix([[1], [1], [1]])
    vector = [0, 0, 10]
    weights = [1, 1, 1]
    real = quotient_certificate(repair_map, vector, weights)
    mutant_value = mutant_l2_projection_scored_in_l1(repair_map, vector, weights)
    assert real.value == Rational(10)
    assert mutant_value == Rational(40, 3)
    assert real.value != mutant_value


def test_mutant_drop_d1d0_killed_on_non_cochain_packet() -> None:
    # Invariant: d1*d0=0 is required; a dropped check admits a non-complex.
    d0 = [[1], [0]]
    d1 = [[1, 0]]
    a2 = Matrix.zeros(1, 0)
    w1 = [1, 1]
    w2 = [1]
    with pytest.raises(ValueError, match="cochain"):
        FiniteObstructionPacket.create(d0, d1, a2, w1, w2)
    mutant_packet = FiniteObstructionPacket(
        d0=Matrix(d0),
        d1=Matrix(d1),
        a2=a2,
        w1=Matrix(w1),
        w2=Matrix(w2),
    )
    mutant_diagnostic = mutant_diagnose_drop_d1d0(mutant_packet, [3, 0])
    assert mutant_diagnostic is Diagnostic.EXACT_REPAIR


def test_mutant_generator_only_annihilator_killed_on_full_subspace() -> None:
    # Invariant: annihilating one generator is not full-subspace annihilation.
    generator_only = Matrix([[1], [0]])
    full_repair_subspace = Matrix.eye(2)
    functional = [0, 1]
    assert is_full_subspace_annihilator(generator_only, functional)
    assert mutant_generator_only_as_full_subspace(generator_only, functional)
    assert not is_full_subspace_annihilator(full_repair_subspace, functional)
    mutant_full = mutant_generator_only_as_full_subspace(full_repair_subspace, functional)
    real_full = is_full_subspace_annihilator(full_repair_subspace, functional)
    assert mutant_full
    assert mutant_full != real_full
