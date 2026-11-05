"""Adversarial Fault-Injection and Break-and-Recover Test Suite for GS-000.

AuthorityEffect: None.
Tests invasive injections breaking axioms H1-H5, orbit uniformity, and quantum operator support,
asserts that audits reliably detect the defect, and verifies that surgical recovery operators restore compliance.
"""

from __future__ import annotations

import numpy as np
import pytest
from coord_additivity import coord_l1
from perturbations import (
    audit_coordinate_symmetry,
    audit_disjoint_additivity,
    audit_edge_locality,
    audit_homogeneity,
    audit_orbit_uniformity,
    audit_orthogonal_support,
    inject_anisotropic_shear,
    inject_cross_coordinate_coupling,
    inject_cross_edge_coupling,
    inject_non_homogeneous_scaling,
    inject_orbit_weight_asymmetry,
    inject_quantum_support_leakage,
    recover_disjoint_additivity,
    recover_edge_locality,
    recover_homogeneity,
    recover_orbit_uniformity,
    recover_orthogonal_support,
    recover_permutation_symmetry,
)


class TestInvasiveAxiomPerturbations:
    """Break-and-recover cycles for all core axioms and mathematical extensions."""

    def test_coordinate_symmetry_break_and_recover(self):
        """H2 (Coordinate Permutation Symmetry) Break & Recover:

        Inject anisotropic shear -> audit detects -> recover mean -> audit passes.
        """
        # Baseline: isotropic weights
        base_weights = [1.0, 1.0, 1.0]
        compliant, disc = audit_coordinate_symmetry(base_weights)
        assert compliant
        assert disc == 0.0

        # Invalid shear parameter
        with pytest.raises(ValueError, match="Dimension must be at least 2"):
            inject_anisotropic_shear(1)
        with pytest.raises(ValueError, match="shear_factor must be > 1.0"):
            inject_anisotropic_shear(3, 0.8)

        # 1. INJECT VIOLATION
        corrupted_weights = inject_anisotropic_shear(3, shear_factor=2.5)
        # Verify that anisotropic l1 fails symmetry
        assert not audit_coordinate_symmetry(corrupted_weights)[0]
        compliant, excess = audit_coordinate_symmetry(corrupted_weights)
        assert not compliant
        assert np.isclose(excess, 1.5)

        # 2. SURGICAL RECOVERY
        recovered_weights = recover_permutation_symmetry(corrupted_weights)

        # 3. VERIFY RESTORATION
        compliant_post, disc_post = audit_coordinate_symmetry(recovered_weights)
        assert compliant_post
        assert disc_post == 0.0
        assert np.allclose(recovered_weights, [2.0, 2.0, 2.0])

    def test_disjoint_additivity_break_and_recover(self):
        """H3 (Disjoint-Coordinate Additivity) Break & Recover:

        Inject cross-coupling -> audit detects -> recover uncoupled l1 -> audit passes.
        """
        # Baseline: coord_l1 is disjoint additive
        compliant, disc = audit_disjoint_additivity(coord_l1, dim=2)
        assert compliant
        assert disc == 0.0

        with pytest.raises(ValueError, match="coupling_strength must be > 0.0"):
            inject_cross_coordinate_coupling(-0.5)

        # 1. INJECT VIOLATION
        coupled_nu = inject_cross_coordinate_coupling(coupling_strength=1.5)
        compliant, excess = audit_disjoint_additivity(coupled_nu, dim=2, test_scale=1.0)
        assert not compliant
        assert np.isclose(excess, 1.5)

        # 2. SURGICAL RECOVERY
        clean_nu = recover_disjoint_additivity(coupled_nu, dim=2)

        # 3. VERIFY RESTORATION
        compliant_post, disc_post = audit_disjoint_additivity(clean_nu, dim=2, test_scale=1.0)
        assert compliant_post
        assert disc_post <= 1e-12
        # Check linearity on test vector
        assert clean_nu(np.array([3.0, 4.0])) == 7.0

    def test_edge_locality_break_and_recover(self):
        """H1 (Edge Locality) Break & Recover:

        Inject cross-edge coupling -> audit detects -> decouple edgewise -> audit passes.
        """
        def standard_global_nu(edge_vectors: list[np.ndarray]) -> float:
            return sum(coord_l1(ev) for ev in edge_vectors)

        compliant, disc = audit_edge_locality(standard_global_nu, num_edges=2, k=2)
        assert compliant
        assert disc == 0.0

        with pytest.raises(ValueError, match="coupling_strength must be > 0.0"):
            inject_cross_edge_coupling(-0.2)

        # 1. INJECT VIOLATION
        coupled_global_nu = inject_cross_edge_coupling(coupling_strength=2.0)
        compliant, excess = audit_edge_locality(coupled_global_nu, num_edges=2, k=2)
        assert not compliant
        assert excess > 1.0

        # 2. SURGICAL RECOVERY
        clean_global_nu = recover_edge_locality(coupled_global_nu, num_edges=2, k=2)

        # 3. VERIFY RESTORATION
        compliant_post, disc_post = audit_edge_locality(clean_global_nu, num_edges=2, k=2)
        assert compliant_post
        assert disc_post <= 1e-12

    def test_homogeneity_break_and_recover(self):
        """H5 (Absolute Homogeneity) Break & Recover:

        Inject p-power scaling -> audit detects -> linearize -> audit passes.
        """
        probe = np.array([2.0, 3.0])
        compliant, disc = audit_homogeneity(coord_l1, probe, scalar=3.0)
        assert compliant
        assert disc == 0.0

        with pytest.raises(ValueError, match="power_p must be different from 1.0"):
            inject_non_homogeneous_scaling(1.0)

        # 1. INJECT VIOLATION
        power_nu = inject_non_homogeneous_scaling(power_p=2.0)
        compliant, excess = audit_homogeneity(power_nu, probe, scalar=2.0)
        assert not compliant
        assert excess > 10.0

        # 2. SURGICAL RECOVERY
        clean_nu = recover_homogeneity(power_nu, dim=2)

        # 3. VERIFY RESTORATION
        compliant_post, disc_post = audit_homogeneity(clean_nu, probe, scalar=3.0)
        assert compliant_post
        assert disc_post <= 1e-12

    def test_orbit_uniformity_break_and_recover(self):
        """Theorem 3 (Orbit Weight Uniformity) Break & Recover:

        Inject asymmetry across orbits -> audit detects -> project to mean -> audit passes.
        """
        base_orbits = (1.5, 1.5, 1.5)
        compliant, disc = audit_orbit_uniformity(base_orbits)
        assert compliant
        assert disc == 0.0

        with pytest.raises(ValueError, match="Must have at least 2 orbits"):
            inject_orbit_weight_asymmetry([1.0])

        # 1. INJECT VIOLATION
        skewed_orbits = inject_orbit_weight_asymmetry(base_orbits, skew_factor=3.0)
        compliant, excess = audit_orbit_uniformity(skewed_orbits)
        assert not compliant
        assert excess > 2.0

        # 2. SURGICAL RECOVERY
        recovered_orbits = recover_orbit_uniformity(skewed_orbits)

        # 3. VERIFY RESTORATION
        compliant_post, disc_post = audit_orbit_uniformity(recovered_orbits)
        assert compliant_post
        assert disc_post == 0.0
        assert np.allclose(recovered_orbits, [2.5, 2.5, 2.5])

    def test_quantum_orthogonal_support_break_and_recover(self):
        """Quantum Orthogonal Support Break & Recover:

        Inject subspace leakage between A and B -> audit detects -> SVD project to orthogonal complement -> audit passes.
        """
        # Baseline orthogonal rank-1 operators
        u1 = np.array([[1.0], [0.0]])
        u2 = np.array([[0.0], [1.0]])
        a = u1 @ u1.conj().T
        b = u2 @ u2.conj().T

        compliant, leakage = audit_orthogonal_support(a, b)
        assert compliant
        assert leakage == 0.0

        # Zero operator validation
        with pytest.raises(ValueError, match="Operators must be non-zero"):
            inject_quantum_support_leakage(np.zeros((2, 2)), b)

        # 1. INJECT VIOLATION (leakage angle = 0.4 rad)
        b_corrupted = inject_quantum_support_leakage(a, b, leakage_angle=0.4)
        compliant, excess = audit_orthogonal_support(a, b_corrupted)
        assert not compliant
        assert excess > 0.3

        # 2. SURGICAL RECOVERY
        b_clean = recover_orthogonal_support(a, b_corrupted)

        # 3. VERIFY RESTORATION
        compliant_post, disc_post = audit_orthogonal_support(a, b_clean)
        assert compliant_post
        assert disc_post <= 1e-12
        # Verify b_clean is non-zero
        assert np.linalg.norm(b_clean) > 0.5
