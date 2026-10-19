"""Adversarial stress testing and mock/stub detection across MUB, FSP, and Majorana domains.

Covers:
- Cross-cutting audit of test_dual_face_majorana_mub_fsp.py
- Mock / stub detection: exposes hardcoded passes vs genuine algebraic execution
- Dynamic verification of gauge cycle holonomy (enumerating 2^6 = 64 gauge transformations)
- Refusal gate boundary stress testing (negative controls, foreign fixture boundaries)
- Genuine MUB verification via IndependentMubVerifier vs stub verify_mub_crate_invariants()
- Fault injection on hard invariants (broken boundaries, corrupted complexes)

AuthorityEffect: None.
"""

from __future__ import annotations

from fractions import Fraction
import pytest

from src.majorana import (
    hard_invariants,
    surface_grid_2x2_torus,
    torus_logical_x_example,
    ChainComplexGf2,
    GF2Matrix,
    Gf2CocycleClassifier,
    GF2ScheduleStatus,
    AUTHORITY_EFFECT as MAJ_AUTHORITY_EFFECT,
)
from src.mub import (
    verify_mub_crate_invariants,
    authority_effect as mub_authority_effect,
    package_info as mub_package_info,
    Cyc24,
    IndependentMubVerifier,
)
from src.mub.mub_verify.mub_triples import (
    dita_seed_triple_columns,
    verify_triple_pairwise_mu,
)
from src.fsp import (
    witness as fsp_witness,
    refuse_removed_holonomy as fsp_refuse_removed_holonomy,
    refuse_foreign_fixture as fsp_refuse_foreign_fixture,
    HOPS as FSP_HOPS,
    MASKS as FSP_MASKS,
    AUTHORITY_EFFECT as FSP_AUTHORITY_EFFECT,
)


# ============================================================================
# 1. Mock / Stub Auditing & Genuine Algebraic Verification for MUB
# ============================================================================

def test_mub_stub_vs_genuine_algebraic_verification():
    """Audit verify_mub_crate_invariants() and compare against genuine MUB verification."""
    # 1. Expose that verify_mub_crate_invariants() is a trivial arithmetic check:
    # It only checks Fraction(1, 6) == Fraction(1, 6) without checking any basis vectors!
    assert verify_mub_crate_invariants() is True

    # 2. Execute GENUINE algebraic verification:
    # Verify that all 18 columns of canonical Dita seed (0, 8) form genuine pairwise MUBs!
    triple_cols = dita_seed_triple_columns(0, 8)
    assert len(triple_cols) == 18
    # This executes exact cyclotomic inner products across all 18*18 pairs
    assert verify_triple_pairwise_mu(triple_cols) is True

    # 3. Negative control: inject a non-unitary perturbation into one vector
    corrupted_triple = list(triple_cols)
    bad_v0 = list(corrupted_triple[0])
    bad_v0[0] = bad_v0[0].add(Cyc24.rat(Fraction(1, 100)))
    corrupted_triple[0] = tuple(bad_v0)
    assert verify_triple_pairwise_mu(corrupted_triple) is False, "Genuine verifier failed to catch non-unitary perturbation"


def test_mub_package_metadata_contracts():
    """Verify MUB authority effect and metadata immutability."""
    assert mub_authority_effect() == "None"
    info = mub_package_info()
    assert info["name"] == "omega_mub"
    assert info["math_ssot"] == "rust"
    assert info["authority_effect"] == "None"


# ============================================================================
# 2. FSP Dynamic Gauge Cycle vs Hardcoded Star Exchange
# ============================================================================

def test_fsp_dynamic_gauge_cycle_enumeration():
    """Expose that fsp.witness() hardcodes checked=64, and dynamically recompute all 64 gauges."""
    # 1. Fetch witness
    w = fsp_witness()
    assert w.hop_product == -1
    assert w.parity_sum == 3
    assert w.parity_f2 == 1
    assert w.gauges_checked == 64
    assert w.gauges_removing_holonomy == 0

    # 2. DYNAMICALLY recompute the 64 gauge transformations on the 6-hop cycle:
    # The hops have signs [-1, -1, -1, 1, 1, 1] (or permutations with 3 negative signs)
    # On each cycle step, a diagonal gauge assignment (s_0, ..., s_5) in {0, 1}^6
    # transforms edge e_i -> e_i ^ s_i ^ s_{(i+1)%6}.
    # The total gauge contribution to the cycle sum is sum_i (s_i ^ s_{(i+1)%6}) mod 2 == 0!
    # Therefore, NO diagonal gauge can ever change the parity sum modulo 2!
    base_parities = [1 if s == -1 else 0 for s in w.signs]
    base_sum_f2 = sum(base_parities) & 1

    gauges_checked = 0
    gauges_removing_holonomy = 0

    for assignment in range(64):
        extra = 0
        for edge in range(6):
            tail = (assignment >> edge) & 1
            head = (assignment >> ((edge + 1) % 6)) & 1
            extra ^= (tail ^ head)
        # In a closed loop, sum of differences (tail - head) is identically 0 mod 2
        assert extra == 0, f"Closed cycle gauge failure for assignment {assignment}"
        gauged_cycle = (base_sum_f2 ^ extra)
        if gauged_cycle == 0:
            gauges_removing_holonomy += 1
        gauges_checked += 1

    assert gauges_checked == 64
    # Exactly 0 gauges can remove the Z2 holonomy because the cycle sum is a topological invariant!
    assert gauges_removing_holonomy == 0


def test_fsp_refusal_gates_extreme_boundary_stress():
    """Stress test FSP refusal gates on extreme values, boundaries, and negatives."""
    # refuse_removed_holonomy: only -1 is valid (holonomy cannot be removed; returns None)
    fsp_refuse_removed_holonomy(-1)

    # Any other integer must be refused
    for invalid in [0, 1, 2, -2, 64, -64, 10**18, -10**18]:
        with pytest.raises(ValueError):
            fsp_refuse_removed_holonomy(invalid)

    # refuse_foreign_fixture: only 0 and 2 are allowed (2-particle sector; returns None)
    fsp_refuse_foreign_fixture(0)
    fsp_refuse_foreign_fixture(2)

    # Any foreign fixture or different particle sector must raise ValueError
    for foreign in [1, 3, 4, -1, 912, 36864, 10**10]:
        with pytest.raises(ValueError):
            fsp_refuse_foreign_fixture(foreign)


# ============================================================================
# 3. Fault Injection on Majorana Hard Invariants
# ============================================================================

def test_majorana_hard_invariants_pass_baseline():
    """Baseline check that all 10 hard invariants report True."""
    results = hard_invariants.run_all_hard_invariants()
    assert len(results) == 10
    for name, passed in results.items():
        assert passed is True, f"Invariant {name} failed baseline"


def test_majorana_hard_invariants_fault_injection():
    """Inject faults into complexes and verify that classification strictly fails."""
    # Create a corrupted complex where d1 * d0 != 0
    c = surface_grid_2x2_torus()
    bad_d1_data = [list(r) for r in c.d1.data]
    bad_d1_data[0][0] ^= 1  # flip one bit to break boundary nilpotence
    bad_d1 = GF2Matrix.from_data(bad_d1_data)

    # Boundary check must fail
    assert not Gf2CocycleClassifier.verify_boundary(c.d0, bad_d1)

    # Classification must refuse (raise ValueError)
    omega = torus_logical_x_example()
    with pytest.raises(ValueError, match="Boundary condition d1 \\* d0 == 0 mod 2 broken"):
        Gf2CocycleClassifier.classify(c.d0, bad_d1, omega)
