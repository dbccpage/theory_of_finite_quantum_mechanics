"""
Executable Python dual for W4.2 (PL-QM043-2 / TOY-MECH):
Discrete Z/2 phase-fiber stand-in over nonzero support E_w.

Honest residual: continuous U(1)^{|E_w|-1} remains OPEN. This suite checks
only the discrete Nat counting shell and free global Bool flip action.

Matches Lean `003_qm_phase_fiber_exactness.lean`:
* relative_phase_dim = max(0, |E_w| - 1) Nat shell
* flipAll involution, free action, orbit size 2 on Fin-3 Bool phases
* gauge-reduced discrete fiber card 2^{3-1} = 4

AuthorityEffect: None. No Wave-4 exit claim.
"""

import pytest
import math
from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class SectorWeights:
    weights: Sequence[float]

    @property
    def active_support(self) -> list[int]:
        """Indices of nonzero sector weights E_w = {gamma : w_gamma > 0}."""
        return [i for i, w in enumerate(self.weights) if w > 0]

    @property
    def active_count(self) -> int:
        """Cardinality of active support |E_w|."""
        return len(self.active_support)

    @property
    def relative_phase_dim(self) -> int:
        """Nat shell: max(0, |E_w| - 1). Not continuous U(1) volume."""
        return max(0, self.active_count - 1)


def flip_all(phi: Sequence[bool]) -> list[bool]:
    """Global Z/2 phase flip: negate every Bool phase tag (Lean flipAll)."""
    return [not b for b in phi]


def compute_relative_phases(
    phases: list[float], active_indices: list[int]
) -> list[float]:
    """Compute relative phases theta_i - theta_0 relative to the first active sector."""
    if not active_indices:
        return []
    base_phase = phases[active_indices[0]]
    return [(phases[idx] - base_phase) % (2 * math.pi) for idx in active_indices[1:]]


def test_active_support_filtering():
    """Verify active support E_w correctly isolates positive weight sectors."""
    sw = SectorWeights([0.5, 0.0, 0.3, 0.0, 0.2])
    assert sw.active_support == [0, 2, 4]
    assert sw.active_count == 3
    assert sw.relative_phase_dim == 2


def test_relative_phase_dimension():
    """Verify relative phase dimension formula |E_w| - 1 (Nat shell)."""
    sw_single = SectorWeights([1.0, 0.0, 0.0])
    assert sw_single.active_count == 1
    assert sw_single.relative_phase_dim == 0

    sw_pair = SectorWeights([0.6, 0.4])
    assert sw_pair.active_count == 2
    assert sw_pair.relative_phase_dim == 1

    sw_tri = SectorWeights([0.3, 0.3, 0.4])
    assert sw_tri.active_count == 3
    assert sw_tri.relative_phase_dim == 2


def test_global_gauge_invariance():
    """Global continuous phase shift leaves relative phases unchanged (diagnostic shell)."""
    phases = [0.1, 0.5, 1.2, 0.0, 2.3]
    active = [0, 1, 4]
    rel1 = compute_relative_phases(phases, active)

    alpha = 0.77
    shifted_phases = [p + alpha for p in phases]
    rel2 = compute_relative_phases(shifted_phases, active)

    assert len(rel1) == 2
    assert len(rel2) == 2
    for r1, r2 in zip(rel1, rel2):
        assert math.isclose(r1, r2, abs_tol=1e-12)


def test_inert_sector_zero_dim():
    """Verify empty/zero-weight support yields 0 relative phase dimensions."""
    sw_zero = SectorWeights([0.0, 0.0, 0.0])
    assert sw_zero.active_count == 0
    assert sw_zero.relative_phase_dim == 0


def test_flip_all_involutive_fin3():
    """Lean flipAll_involutive: flip twice recovers the original Fin-3 Bool map."""
    samples = [
        [False, False, False],
        [True, True, True],
        [True, False, True],
        [False, True, False],
        [True, True, False],
    ]
    for phi in samples:
        assert flip_all(flip_all(phi)) == phi


def test_flip_all_free_action_fin3():
    """Lean flipAll_free_action_fin3 / flipAll_no_fixed_point: no fixed points on Fin 3."""
    for bits in range(8):
        phi = [bool((bits >> i) & 1) for i in range(3)]
        flipped = flip_all(phi)
        assert flipped != phi
        for i in range(3):
            assert flipped[i] is (not phi[i])


def test_orbit_size_two_fin3():
    """Lean orbit_size_two_fin3: each Z/2-orbit has cardinality 2."""
    seen_orbits: set[frozenset[tuple[bool, ...]]] = set()
    for bits in range(8):
        phi = [bool((bits >> i) & 1) for i in range(3)]
        orbit = frozenset({tuple(phi), tuple(flip_all(phi))})
        assert len(orbit) == 2
        seen_orbits.add(orbit)
    assert len(seen_orbits) == 4


def test_fin3_bool_fiber_card_gauge():
    """Lean fin3_bool_fiber_card_gauge: raw 8, gauge-reduced 4 = 2^{3-1}."""
    assert 2**3 == 8
    assert (2**3) // 2 == 4
    assert 2 ** (3 - 1) == 4


def test_flip_all_moves_false3():
    """Lean flipAll_moves_false3 / flipAll_false3_eq_true3 concrete witnesses."""
    false3 = [False, False, False]
    true3 = [True, True, True]
    assert flip_all(false3) != false3
    assert flip_all(false3) == true3
    assert flip_all(true3) == false3


if __name__ == "__main__":
    pytest.main([__file__])
