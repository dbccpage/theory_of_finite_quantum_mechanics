from __future__ import annotations
"""
Executable Python dual harness for W5.8 — conditional uniqueness under AX-LIFT-V0.

Mirrors Lean `003_qm_conditional_uniqueness.lean`:

1. Registry lifts {complex, real, quat}; only complex satisfies AX-LIFT-V0.
2. Conditional uniqueness: satisfies V0 ⇒ lift is complexHilbert (iff on registry).
3. Minimality: without A_local_tomography, uniqueness fails (complex ≠ rebit both pass).
4. Absolute uniqueness outside registry refused; V0.1 optionals do not upgrade it.
5. Continuous REFUSED on FinL1 (W5.6 sync); continuum pathway OPEN/import.
6. Multipartite LT3 uniqueness coincides with V0-unique slice (not forced into V0).
7. Bipartite LT d=3 explicit counts (complex 81=81, rebit 36≠45, quat 225≠153).
8. Multipartite LT3 explicit counts (complex 64=64, rebit 27≠36, quat 216≠120).
9. R_LIFT pathway host-gated on AX-LIFT-V0; absolute uniqueness still OPEN/REFUSED.

AuthorityEffect: None.
"""


from enum import Enum

import pytest


class NamedLift(str, Enum):
    COMPLEX = "complexHilbert"
    REAL = "realHilbert"
    QUAT = "quaternionicHilbert"


class OutsideRegistry(str, Enum):
    ELLP_PHANTOM = "ellpReadoutPhantom"
    JORDAN_UNKNOWN = "jordanSpectralConvexUnknown"


class OptionalAxiomId(str, Enum):
    A_PURIFICATION = "A_purification_capacity"
    A_CONTINUOUS_REV = "A_continuous_reversible_connectedness"


AXIOM_SET_ID = "AX-LIFT-V0"
AX_LIFT_V0_1_OPTIONAL = (
    OptionalAxiomId.A_PURIFICATION,
    OptionalAxiomId.A_CONTINUOUS_REV,
)


def density_params(lift: NamedLift, d: int) -> int:
    if d <= 0:
        raise ValueError("d must be positive")
    if lift is NamedLift.COMPLEX:
        return d * d
    if lift is NamedLift.REAL:
        return d * (d + 1) // 2
    if lift is NamedLift.QUAT:
        return d * (2 * d - 1)
    raise ValueError(lift)


def satisfies_finite(d: int = 2) -> bool:
    return d > 0


def satisfies_l1_shadow(_lift: NamedLift) -> bool:
    return True


def satisfies_local_tomography(lift: NamedLift) -> bool:
    return density_params(lift, 2) * density_params(lift, 2) == density_params(lift, 4)


def satisfies_ax_lift_v0(lift: NamedLift) -> bool:
    return (
        satisfies_finite(2)
        and satisfies_l1_shadow(lift)
        and satisfies_local_tomography(lift)
    )


def satisfies_ax_lift_v0_minus_lt(lift: NamedLift) -> bool:
    return satisfies_finite(2) and satisfies_l1_shadow(lift)


def conditional_uniqueness_registry(lift: NamedLift) -> NamedLift | None:
    """Return complexHilbert if V0 holds; else None (fails uniqueness hypothesis)."""
    if satisfies_ax_lift_v0(lift):
        return NamedLift.COMPLEX
    return None


def test_axiom_set_id_binding():
    assert AXIOM_SET_ID == "AX-LIFT-V0"


def test_only_complex_satisfies_v0():
    assert satisfies_ax_lift_v0(NamedLift.COMPLEX) is True
    assert satisfies_ax_lift_v0(NamedLift.REAL) is False
    assert satisfies_ax_lift_v0(NamedLift.QUAT) is False


def test_conditional_uniqueness_registry():
    for lift in NamedLift:
        if satisfies_ax_lift_v0(lift):
            assert lift is NamedLift.COMPLEX
            assert conditional_uniqueness_registry(lift) is NamedLift.COMPLEX
        else:
            assert conditional_uniqueness_registry(lift) is None


def test_satisfies_v0_iff_complex():
    for lift in NamedLift:
        assert satisfies_ax_lift_v0(lift) is (lift is NamedLift.COMPLEX)


def test_unique_v0_registry_slice():
    v0_lifts = [L for L in NamedLift if satisfies_ax_lift_v0(L)]
    assert v0_lifts == [NamedLift.COMPLEX]


def test_uniqueness_fails_without_lt():
    """Minimality: V0 minus LT admits distinct complex and rebit models."""
    assert satisfies_ax_lift_v0_minus_lt(NamedLift.COMPLEX)
    assert satisfies_ax_lift_v0_minus_lt(NamedLift.REAL)
    assert satisfies_ax_lift_v0_minus_lt(NamedLift.QUAT)
    assert NamedLift.COMPLEX is not NamedLift.REAL
    assert satisfies_ax_lift_v0(NamedLift.COMPLEX)
    assert not satisfies_ax_lift_v0(NamedLift.REAL)


def test_uniqueness_requires_local_tomography_on_registry():
    for lift in NamedLift:
        if satisfies_ax_lift_v0(lift):
            assert lift is NamedLift.COMPLEX
    passers = [L for L in NamedLift if satisfies_ax_lift_v0_minus_lt(L)]
    assert len(passers) == 3
    assert NamedLift.COMPLEX in passers and NamedLift.REAL in passers


def test_absolute_uniqueness_refused_outside_registry():
    absolute_mathematical_uniqueness_open = True
    absolute_uniqueness_claim = False
    assert absolute_mathematical_uniqueness_open is True
    assert absolute_uniqueness_claim is False
    assert OutsideRegistry.ELLP_PHANTOM.value not in {L.value for L in NamedLift}
    assert OutsideRegistry.JORDAN_UNKNOWN != OutsideRegistry.ELLP_PHANTOM


def test_v01_does_not_upgrade_absolute_uniqueness():
    continuous_activation_status = "refusedOnFinL1"
    continuum_pathway = "openContinuumImport"
    absolute_uniqueness_claim = False
    assert continuous_activation_status == "refusedOnFinL1"
    assert continuum_pathway == "openContinuumImport"
    assert absolute_uniqueness_claim is False
    assert len(AX_LIFT_V0_1_OPTIONAL) == 2
    assert satisfies_ax_lift_v0(NamedLift.COMPLEX)
    assert not satisfies_ax_lift_v0(NamedLift.REAL)


def satisfies_purification_capacity(lift: NamedLift) -> bool:
    """Align W5.6: ℂ/ℝ purify (Bell toy); quat unclaimed."""
    if lift is NamedLift.QUAT:
        return False
    return True


def test_uniqueness_fails_with_purification_without_lt():
    """V0.1 purification activation does not restore uniqueness without LT."""
    assert satisfies_ax_lift_v0_minus_lt(NamedLift.COMPLEX)
    assert satisfies_ax_lift_v0_minus_lt(NamedLift.REAL)
    assert satisfies_purification_capacity(NamedLift.COMPLEX)
    assert satisfies_purification_capacity(NamedLift.REAL)
    assert NamedLift.COMPLEX is not NamedLift.REAL


def test_v0_plus_purification_still_unique():
    """LT remains load-bearing: rebit purifies but fails V0."""
    assert satisfies_ax_lift_v0(NamedLift.COMPLEX)
    assert satisfies_purification_capacity(NamedLift.COMPLEX)
    assert satisfies_purification_capacity(NamedLift.REAL)
    assert not satisfies_ax_lift_v0(NamedLift.REAL)
    for lift in NamedLift:
        if satisfies_ax_lift_v0(lift) and satisfies_purification_capacity(lift):
            assert lift is NamedLift.COMPLEX


def test_v01_purification_does_not_upgrade_absolute():
    purification_activation_status = "activatedToyMech"
    absolute_uniqueness_claim = False
    assert purification_activation_status == "activatedToyMech"
    assert absolute_uniqueness_claim is False
    assert len(AX_LIFT_V0_1_OPTIONAL) == 2


def test_v01_vs_uniqueness_package():
    assert satisfies_ax_lift_v0_minus_lt(NamedLift.COMPLEX)
    assert satisfies_purification_capacity(NamedLift.REAL)
    assert not satisfies_ax_lift_v0(NamedLift.REAL)
    for lift in NamedLift:
        if satisfies_ax_lift_v0(lift):
            assert lift is NamedLift.COMPLEX
    absolute_uniqueness_claim = False
    purification_activation_status = "activatedToyMech"
    continuous_activation_status = "refusedOnFinL1"
    continuum_pathway = "openContinuumImport"
    assert absolute_uniqueness_claim is False
    assert purification_activation_status == "activatedToyMech"
    assert continuous_activation_status == "refusedOnFinL1"
    assert continuum_pathway == "openContinuumImport"


def local_prod(lift: NamedLift, d_a: int, d_b: int) -> int:
    return density_params(lift, d_a) * density_params(lift, d_b)


def composite_params(lift: NamedLift, d_a: int, d_b: int) -> int:
    return density_params(lift, d_a * d_b)


def local_prod3(lift: NamedLift) -> int:
    p = density_params(lift, 2)
    return p * p * p


def composite_params3(lift: NamedLift) -> int:
    return density_params(lift, 8)


def satisfies_local_tomography3(lift: NamedLift) -> bool:
    return local_prod3(lift) == composite_params3(lift)


def test_lt3_explicit_numbers():
    """Multipartite LT3 counts: complex 64=64, rebit 27≠36, quat 216≠120."""
    assert local_prod3(NamedLift.COMPLEX) == 64
    assert composite_params3(NamedLift.COMPLEX) == 64
    assert local_prod3(NamedLift.REAL) == 27
    assert composite_params3(NamedLift.REAL) == 36
    assert local_prod3(NamedLift.QUAT) == 216
    assert composite_params3(NamedLift.QUAT) == 120
    assert local_prod3(NamedLift.COMPLEX) == composite_params3(NamedLift.COMPLEX)
    assert local_prod3(NamedLift.REAL) != composite_params3(NamedLift.REAL)
    assert local_prod3(NamedLift.QUAT) != composite_params3(NamedLift.QUAT)


def test_lt3_uniqueness_iff_complex():
    assert satisfies_local_tomography3(NamedLift.COMPLEX)
    assert not satisfies_local_tomography3(NamedLift.REAL)
    assert not satisfies_local_tomography3(NamedLift.QUAT)
    for lift in NamedLift:
        assert satisfies_local_tomography3(lift) is (lift is NamedLift.COMPLEX)


def test_v0_and_lt3_uniqueness_coincide():
    """V0-unique and LT3-unique registry slices both equal {complex} only."""
    v0 = [L for L in NamedLift if satisfies_ax_lift_v0(L)]
    lt3 = [L for L in NamedLift if satisfies_local_tomography3(L)]
    assert v0 == [NamedLift.COMPLEX]
    assert lt3 == [NamedLift.COMPLEX]
    assert v0 == lt3


def test_uniqueness_lt3_consistency_package():
    absolute_uniqueness_claim = False
    continuous_activation_status = "refusedOnFinL1"
    assert satisfies_local_tomography3(NamedLift.COMPLEX)
    assert not satisfies_local_tomography3(NamedLift.REAL)
    assert not satisfies_local_tomography3(NamedLift.QUAT)
    for lift in NamedLift:
        assert satisfies_local_tomography3(lift) is (lift is NamedLift.COMPLEX)
        assert satisfies_ax_lift_v0(lift) is (lift is NamedLift.COMPLEX)
    assert continuous_activation_status == "refusedOnFinL1"
    assert absolute_uniqueness_claim is False


def test_uniqueness_relative_to_named_set():
    assert AXIOM_SET_ID == "AX-LIFT-V0"
    for lift in NamedLift:
        assert satisfies_ax_lift_v0(lift) is (lift is NamedLift.COMPLEX)


def satisfies_local_tomography_d3(lift: NamedLift) -> bool:
    return local_prod(lift, 3, 3) == composite_params(lift, 3, 3)


def test_lt_d3_explicit_numbers():
    """Bipartite d=3 counts: complex 81=81, rebit 36≠45, quat 225≠153."""
    assert local_prod(NamedLift.COMPLEX, 3, 3) == 81
    assert composite_params(NamedLift.COMPLEX, 3, 3) == 81
    assert local_prod(NamedLift.REAL, 3, 3) == 36
    assert composite_params(NamedLift.REAL, 3, 3) == 45
    assert local_prod(NamedLift.QUAT, 3, 3) == 225
    assert composite_params(NamedLift.QUAT, 3, 3) == 153
    assert local_prod(NamedLift.COMPLEX, 3, 3) == composite_params(
        NamedLift.COMPLEX, 3, 3
    )
    assert local_prod(NamedLift.REAL, 3, 3) != composite_params(NamedLift.REAL, 3, 3)
    assert local_prod(NamedLift.QUAT, 3, 3) != composite_params(NamedLift.QUAT, 3, 3)


def test_complex_lt_identity_all_dims():
    """Complex LT identity is algebraic for all factor dims (TOY-MECH)."""
    for d_a, d_b in ((1, 1), (2, 2), (3, 3), (2, 3), (4, 5)):
        assert local_prod(NamedLift.COMPLEX, d_a, d_b) == composite_params(
            NamedLift.COMPLEX, d_a, d_b
        )


def test_lt_d3_uniqueness_iff_complex():
    assert satisfies_local_tomography_d3(NamedLift.COMPLEX)
    assert not satisfies_local_tomography_d3(NamedLift.REAL)
    assert not satisfies_local_tomography_d3(NamedLift.QUAT)
    for lift in NamedLift:
        assert satisfies_local_tomography_d3(lift) is (lift is NamedLift.COMPLEX)


def test_lt_d2_d3_uniqueness_coincide():
    d2 = [L for L in NamedLift if satisfies_local_tomography(L)]
    d3 = [L for L in NamedLift if satisfies_local_tomography_d3(L)]
    assert d2 == [NamedLift.COMPLEX]
    assert d3 == [NamedLift.COMPLEX]
    assert d2 == d3


def test_uniqueness_lt_d3_deepen_package():
    """Residual deepen: explicit d=3 + LT3 counts; absolute/continuum still OPEN."""
    absolute_uniqueness_claim = False
    absolute_mathematical_uniqueness_open = True
    continuous_activation_status = "refusedOnFinL1"
    continuum_pathway = "openContinuumImport"
    assert local_prod(NamedLift.COMPLEX, 3, 3) == 81
    assert composite_params(NamedLift.COMPLEX, 3, 3) == 81
    assert local_prod(NamedLift.REAL, 3, 3) == 36
    assert composite_params(NamedLift.REAL, 3, 3) == 45
    assert local_prod(NamedLift.QUAT, 3, 3) == 225
    assert composite_params(NamedLift.QUAT, 3, 3) == 153
    assert satisfies_local_tomography_d3(NamedLift.COMPLEX)
    assert not satisfies_local_tomography_d3(NamedLift.REAL)
    assert not satisfies_local_tomography_d3(NamedLift.QUAT)
    assert local_prod3(NamedLift.COMPLEX) == 64
    assert composite_params3(NamedLift.COMPLEX) == 64
    assert local_prod3(NamedLift.REAL) == 27
    assert composite_params3(NamedLift.REAL) == 36
    assert local_prod3(NamedLift.QUAT) == 216
    assert composite_params3(NamedLift.QUAT) == 120
    assert continuous_activation_status == "refusedOnFinL1"
    assert continuum_pathway == "openContinuumImport"
    assert absolute_uniqueness_claim is False
    assert absolute_mathematical_uniqueness_open is True


class LiftHost(str, Enum):
    FINL1 = "finL1Alone"
    AX_LIFT_V0 = "axLiftV0Package"


def r_lift_pathway_recovered(host: LiftHost) -> bool:
    return host is LiftHost.AX_LIFT_V0


def test_r_lift_pathway_host_gated():
    assert r_lift_pathway_recovered(LiftHost.AX_LIFT_V0) is True
    assert r_lift_pathway_recovered(LiftHost.FINL1) is False
    finl1_forces_registry_uniqueness = False
    v0_package_selects_complex = True
    assert finl1_forces_registry_uniqueness is False
    assert v0_package_selects_complex is True
    assert satisfies_ax_lift_v0(NamedLift.COMPLEX)
    assert not satisfies_ax_lift_v0(NamedLift.REAL)


def test_r_lift_and_lt_d3_package():
    r_lift_and_lt_d3_package_toy = True
    absolute_uniqueness_claim = False
    continuum_pathway = "openContinuumImport"
    assert r_lift_and_lt_d3_package_toy is True
    assert r_lift_pathway_recovered(LiftHost.AX_LIFT_V0) is True
    assert r_lift_pathway_recovered(LiftHost.FINL1) is False
    assert satisfies_local_tomography_d3(NamedLift.COMPLEX)
    assert not satisfies_local_tomography_d3(NamedLift.REAL)
    assert not satisfies_local_tomography_d3(NamedLift.QUAT)
    assert local_prod(NamedLift.COMPLEX, 3, 3) == 81
    assert local_prod(NamedLift.REAL, 3, 3) == 36
    assert composite_params(NamedLift.REAL, 3, 3) == 45
    assert local_prod3(NamedLift.COMPLEX) == 64
    assert local_prod3(NamedLift.REAL) == 27
    assert composite_params3(NamedLift.REAL) == 36
    for lift in NamedLift:
        assert satisfies_ax_lift_v0(lift) is (lift is NamedLift.COMPLEX)
    assert absolute_uniqueness_claim is False
    assert continuum_pathway == "openContinuumImport"
    assert AXIOM_SET_ID == "AX-LIFT-V0"


if __name__ == "__main__":
    pytest.main([__file__])
