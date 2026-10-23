"""
Tests for CPTP channels, cochain morphisms, and quotient monotonicity.
Paper: GS-003 (006_vector_and_quantum_observer_geometries)
AuthorityEffect: None.
"""

import pytest
import numpy as np

from cochain_complex import Cochain, GraphComplex
from quantum_geometry import HermitianOperator, QuantumQuotientSolver
from cptp_channels import (
    KrausChannel,
    CochainMorphism,
    verify_stochastic_l1_contraction,
)
from exceptions import DimensionMismatchError


def test_kraus_channel_construction_and_errors():
    # Empty
    with pytest.raises(ValueError):
        KrausChannel(kraus_operators=[])

    # Rectangular
    rect = np.zeros((2, 3), dtype=complex)
    with pytest.raises(DimensionMismatchError):
        KrausChannel(kraus_operators=[rect])

    # Shape mismatch
    k1 = np.eye(2, dtype=complex)
    k2 = np.eye(3, dtype=complex)
    with pytest.raises(DimensionMismatchError):
        KrausChannel(kraus_operators=[k1, k2])


def test_standard_channels_trace_preserving():
    # Unitary
    h = np.array([[1.0, 1.0], [1.0, -1.0]], dtype=complex) / np.sqrt(2.0)
    ch_u = KrausChannel.unitary(h)
    assert ch_u.is_trace_preserving()
    assert not ch_u.is_trace_decreasing()
    assert not ch_u.is_trace_increasing()
    ch_u.assert_cptp()

    # Depolarizing (d=2)
    ch_depol2 = KrausChannel.depolarizing(d=2, p=0.3)
    assert ch_depol2.is_trace_preserving()
    ch_depol2.assert_cptp()

    # Depolarizing (d=3)
    ch_depol3 = KrausChannel.depolarizing(d=3, p=0.5)
    assert ch_depol3.is_trace_preserving()
    ch_depol3.assert_cptp()

    # Amplitude damping
    ch_ad = KrausChannel.amplitude_damping(gamma=0.4)
    assert ch_ad.is_trace_preserving()
    ch_ad.assert_cptp()

    # Phase damping
    ch_pd = KrausChannel.phase_damping(lambda_param=0.25)
    assert ch_pd.is_trace_preserving()
    ch_pd.assert_cptp()


def test_channel_contractivity():
    ch_depol = KrausChannel.depolarizing(d=2, p=0.4)
    sz = HermitianOperator.SIGMA_Z

    ratio = ch_depol.contractivity_ratio(sz)
    # For traceless operator under depolarizing: E(X) = (1 - p) X => ratio = 1 - p = 0.6
    assert abs(ratio - 0.6) < 1e-12

    # Zero matrix ratio
    zero_mat = np.zeros((2, 2), dtype=complex)
    assert ch_depol.contractivity_ratio(zero_mat) == 1.0


def test_depolarizing_qutrit_matches_stated_replacement_channel():
    """d!=2 must implement E(X)=(1-p)X + p (I/d) Tr(X), not a (1-p/d) contraction."""
    p = 0.4
    d = 3
    ch = KrausChannel.depolarizing(d=d, p=p)
    assert ch.is_trace_preserving()
    ch.assert_cptp()

    gm0 = HermitianOperator.gell_mann_basis(d)[0]
    ratio = ch.contractivity_ratio(gm0)
    assert abs(ratio - (1.0 - p)) < 1e-9

    ket = np.zeros((d, d), dtype=complex)
    ket[0, 0] = 1.0
    expected = (1.0 - p) * ket + p * (np.eye(d, dtype=complex) / d)
    np.testing.assert_allclose(ch.apply(ket), expected, atol=1e-10)


def test_channel_factory_errors():
    # Non-unitary
    non_u = np.array([[1.0, 1.0], [0.0, 1.0]], dtype=complex)
    with pytest.raises(ValueError):
        KrausChannel.unitary(non_u)

    # Invalid depol p
    with pytest.raises(ValueError):
        KrausChannel.depolarizing(d=2, p=-0.1)
    with pytest.raises(ValueError):
        KrausChannel.depolarizing(d=2, p=1.2)

    # Invalid amplitude damping gamma
    with pytest.raises(ValueError):
        KrausChannel.amplitude_damping(gamma=-0.1)
    with pytest.raises(ValueError):
        KrausChannel.amplitude_damping(gamma=1.1)

    # Invalid phase damping lambda
    with pytest.raises(ValueError):
        KrausChannel.phase_damping(lambda_param=-0.1)
    with pytest.raises(ValueError):
        KrausChannel.phase_damping(lambda_param=1.5)

    # Non-contractive perturbation with scale <= 1
    base = KrausChannel.unitary(np.eye(2, dtype=complex))
    with pytest.raises(ValueError):
        KrausChannel.non_contractive_perturbation(base, scale=1.0)


def test_cochain_morphism():
    comp = GraphComplex.triangle_complex()
    ch = KrausChannel.depolarizing(d=2, p=0.3)
    morphism = CochainMorphism.uniform(comp, ch)

    sz = HermitianOperator.SIGMA_Z
    phi_0 = Cochain(np.array([sz, 2.0 * sz, -sz]), degree=0)
    transformed_0 = morphism.apply_to_cochain(phi_0)
    assert transformed_0.degree == 0
    np.testing.assert_allclose(transformed_0[0], 0.7 * sz)

    a_mat = 0.5 * sz
    delta_1 = Cochain(np.array([a_mat, a_mat, a_mat]), degree=1)
    transformed_1 = morphism.apply_to_cochain(delta_1)
    assert transformed_1.degree == 1
    np.testing.assert_allclose(transformed_1[0], 0.7 * a_mat)

    # Intertwining verification
    is_intertwined, max_err = morphism.verify_intertwining(comp)
    assert is_intertwined
    assert max_err < 1e-12

    # Monotonicity verification
    solver = QuantumQuotientSolver(comp, tol=1e-4)
    is_mono, phi_before, phi_after = morphism.verify_quotient_monotonicity(
        solver, delta_1
    )
    assert is_mono
    assert abs(phi_before - 1.5) < 1e-4
    assert abs(phi_after - 1.05) < 1e-4


def test_cochain_morphism_errors():
    comp = GraphComplex.triangle_complex()
    ch = KrausChannel.depolarizing(d=2, p=0.2)
    morphism = CochainMorphism.uniform(comp, ch)

    # Vector cochain
    c_vec = Cochain([[1.0, 2.0]], degree=0)
    with pytest.raises(ValueError):
        morphism.apply_to_cochain(c_vec)

    # Cell mismatch on degree 0
    sz = HermitianOperator.SIGMA_Z
    c_cells0 = Cochain(np.array([sz, sz]), degree=0)
    with pytest.raises(DimensionMismatchError):
        morphism.apply_to_cochain(c_cells0)

    # Cell mismatch on degree 1
    c_cells1 = Cochain(np.array([sz, sz]), degree=1)
    with pytest.raises(DimensionMismatchError):
        morphism.apply_to_cochain(c_cells1)

    # Unsupported degree 2
    c_deg2 = Cochain(np.array([sz]), degree=2)
    with pytest.raises(NotImplementedError):
        morphism.apply_to_cochain(c_deg2)

    # Complex mismatch in verify_intertwining
    comp2 = GraphComplex(num_vertices=2, edges=[(0, 1)])
    with pytest.raises(DimensionMismatchError):
        morphism.verify_intertwining(comp2)


def test_channel_apply_non_hermitian():
    ch = KrausChannel.depolarizing(d=2, p=0.2)
    non_herm = np.array([[1.0, 2.0], [0.0, 1.0]], dtype=complex)
    out = ch.apply(non_herm)
    assert out.shape == (2, 2)


def test_population_shadow_column_stochastic():
    """
    Test that CPTP channels induce column-stochastic population shadows:
        K_{i, j} = sum_k |(A_k)_{i, j}|^2, sum_i K_{i, j} = 1.
    (Absorbed from QM_082 / ENC-1127).
    """
    # 1. Depolarizing d=2
    ch_depol = KrausChannel.depolarizing(d=2, p=0.4)
    k_depol = ch_depol.population_shadow()
    assert k_depol.shape == (2, 2)
    assert np.all(k_depol >= -1e-12)
    np.testing.assert_allclose(k_depol.sum(axis=0), 1.0, atol=1e-10)

    # 2. Amplitude damping
    ch_ad = KrausChannel.amplitude_damping(gamma=0.35)
    k_ad = ch_ad.population_shadow()
    assert np.all(k_ad >= -1e-12)
    np.testing.assert_allclose(k_ad.sum(axis=0), 1.0, atol=1e-10)

    # 3. Phase damping
    ch_pd = KrausChannel.phase_damping(lambda_param=0.5)
    k_pd = ch_pd.population_shadow()
    assert np.all(k_pd >= -1e-12)
    np.testing.assert_allclose(k_pd.sum(axis=0), 1.0, atol=1e-10)

    # 4. Unitary (Hadamard)
    h = np.array([[1.0, 1.0], [1.0, -1.0]], dtype=complex) / np.sqrt(2.0)
    ch_u = KrausChannel.unitary(h)
    k_u = ch_u.population_shadow()
    np.testing.assert_allclose(k_u, [[0.5, 0.5], [0.5, 0.5]], atol=1e-10)
    np.testing.assert_allclose(k_u.sum(axis=0), 1.0, atol=1e-10)

    # 5. Qutrit depolarizing (d=3)
    ch_qutrit = KrausChannel.depolarizing(d=3, p=0.3)
    k_q3 = ch_qutrit.population_shadow()
    assert k_q3.shape == (3, 3)
    assert np.all(k_q3 >= -1e-12)
    np.testing.assert_allclose(k_q3.sum(axis=0), 1.0, atol=1e-10)


def test_population_shadow_diagonal_transport():
    """
    Test that the population shadow acts on diagonal input states as a Markov transition matrix:
        p' = K @ p for rho = diag(p).
    (Absorbed from QM_082 / ENC-1127).
    """
    ch_ad = KrausChannel.amplitude_damping(gamma=0.4)
    k_ad = ch_ad.population_shadow()

    p = np.array([0.7, 0.3])
    rho_diag = np.diag(p).astype(complex)

    out_rho = ch_ad.apply(rho_diag)
    out_diag = np.real(np.diag(out_rho))

    expected_p = k_ad @ p
    np.testing.assert_allclose(out_diag, expected_p, atol=1e-10)


def test_stochastic_l1_contraction():
    """
    Test column-stochastic l1 contraction:
        ||S x||_1 <= ||x||_1.
    (Absorbed from QM_082 / ENC-1055).
    """
    # Bit-flip kernel
    s_flip = np.array([[0.0, 1.0], [1.0, 0.0]])
    x = np.array([1.0, -1.0])
    is_cont, n_before, n_after = verify_stochastic_l1_contraction(s_flip, x)
    assert is_cont
    assert n_before == 2.0
    assert n_after == 2.0

    # Averaging kernel (strictly contractive on traceless x)
    s_avg = np.array([[0.5, 0.5], [0.5, 0.5]])
    is_cont2, n_before2, n_after2 = verify_stochastic_l1_contraction(s_avg, x)
    assert is_cont2
    assert n_before2 == 2.0
    assert n_after2 == 0.0

    # General random column-stochastic matrix on 3 outcomes
    rng = np.random.default_rng(42)
    raw = rng.uniform(0.1, 1.0, size=(3, 3))
    s_rand = raw / raw.sum(axis=0, keepdims=True)
    x3 = np.array([0.5, -0.2, -0.3])
    is_cont3, nb3, na3 = verify_stochastic_l1_contraction(s_rand, x3)
    assert is_cont3
    assert na3 <= nb3 + 1e-10


def test_rescaled_trace_norm_firewall():
    """
    Test the Metric Non-Selection Firewall:
        For any c > 0, j_c(X) = c * 0.5 * ||X||_1 is CPTP-monotone.
        Thus CPTP monotonicity alone underdetermines the normalization scale
        and cannot uniquely select the half-trace norm without operational axioms.
    (Absorbed from QM_081 / ENC-0247).
    """
    sz = HermitianOperator.SIGMA_Z
    ch_depol = KrausChannel.depolarizing(d=2, p=0.35)
    out_sz = ch_depol.apply(sz)

    norm_in = float(HermitianOperator.schatten_norm(sz, p=1))
    norm_out = float(HermitianOperator.schatten_norm(out_sz, p=1))

    for c in [0.5, 1.0, 2.0, 5.0]:
        j_in = c * 0.5 * norm_in
        j_out = c * 0.5 * norm_out
        assert j_out <= j_in + 1e-12, f"Scale c={c} violated monotonicity"
