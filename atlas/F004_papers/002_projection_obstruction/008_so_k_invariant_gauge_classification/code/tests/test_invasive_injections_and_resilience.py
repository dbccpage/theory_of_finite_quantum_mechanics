"""
Invasive Injection and Resilience Test Suite.
Verifies break-and-recovery mechanisms under deliberate mathematical faults.
Paper: GS-002 (008_so_k_invariant_gauge_classification)
"""

import numpy as np

from carrier import GraphComplex, Cochain
from falsification import InvasiveAdversary


def test_invasive_divergence_injection_and_recovery() -> None:
    g = GraphComplex.create_cycle_graph(cycle_len=3, stalk_dim=2)
    omega = Cochain(np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]]))

    adversary = InvasiveAdversary(g)
    result = adversary.test_divergence_injection_and_recovery(
        omega, perturbation_magnitude=1.0
    )

    # Assert that the fault was caught
    assert result.detected_failure, (
        "Adversary failed to detect non-divergence-free dual perturbation!"
    )
    # Assert that recovery succeeded
    assert result.recovery_successful, (
        "Projection failed to recover divergence-free dual circulation!"
    )
    assert result.metrics["max_divergence_corrupted"] > 0.5
    assert result.metrics["max_divergence_recovered"] <= 1e-5


def test_invasive_gauge_anisotropy_injection() -> None:
    g = GraphComplex.create_cycle_graph(cycle_len=3, stalk_dim=2)
    adversary = InvasiveAdversary(g)

    result = adversary.test_gauge_anisotropy_injection(epsilon=0.3)

    assert result.detected_failure, (
        "Invariance detector failed to detect gauge anisotropy!"
    )
    assert result.recovery_successful, "Failed to restore isotropic SO(k) invariance!"
    assert result.metrics["corrupted_max_deviation"] > 0.1
    assert result.metrics["restored_max_deviation"] < 1e-6


def test_invasive_lipschitz_noise_resilience() -> None:
    g = GraphComplex.create_cycle_graph(cycle_len=3, stalk_dim=2)
    omega = Cochain(np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]]))

    adversary = InvasiveAdversary(g)
    result = adversary.test_lipschitz_noise_resilience(omega, noise_level=0.1)

    assert result.recovery_successful, (
        "Lipschitz continuity bound violated under noise perturbation!"
    )
    assert (
        result.metrics["absolute_difference"]
        <= result.metrics["theoretical_upper_bound"] + 1e-5
    )
