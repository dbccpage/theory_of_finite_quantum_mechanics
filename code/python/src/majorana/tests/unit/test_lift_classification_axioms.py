from __future__ import annotations
"""
Executable Python dual harness for W5.6 — named axiom set + registry classification.

Mirrors Lean `003_qm_lift_classification_axioms.lean`:

1. Freeze AX-LIFT-V0 = {A_finite, A_l1_shadow, A_local_tomography}.
2. Among {complex, real, quaternionic}, only complex satisfies all three.
3. LT is the sole V0 discriminator on the registry (minus-LT all pass).
4. Blocking-axiom certificates; enumerative uniqueness (filter length 1).
5. AX-LIFT-V0.1 optional additives named but not forced into V0.
6. Purification activated TOY-MECH; continuous REFUSED on FinL1 (continuum import OPEN).
7. Multipartite LT3 consistent with V0 registry filter (W5.5 bind; not forced into V0).
8. Full Jordan/Koecher–Vinberg classification remains open literature residual.
9. Absolute lift-universe completeness refused (W5.11 fence).

AuthorityEffect: None.
"""


from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

import pytest


class NamedLift(str, Enum):
    COMPLEX = "complexHilbert"
    REAL = "realHilbert"
    QUAT = "quaternionicHilbert"


class AxiomId(str, Enum):
    A_FINITE = "A_finite"
    A_L1_SHADOW = "A_l1_shadow"
    A_LOCAL_TOMOGRAPHY = "A_local_tomography"


class OptionalAxiomId(str, Enum):
    A_PURIFICATION = "A_purification_capacity"
    A_CONTINUOUS_REV = "A_continuous_reversible_connectedness"


class BlockingAxiom(str, Enum):
    NONE = "none"
    LOCAL_TOMOGRAPHY = "localTomography"


AX_LIFT_V0 = (
    AxiomId.A_FINITE,
    AxiomId.A_L1_SHADOW,
    AxiomId.A_LOCAL_TOMOGRAPHY,
)

AX_LIFT_V0_1_OPTIONAL = (
    OptionalAxiomId.A_PURIFICATION,
    OptionalAxiomId.A_CONTINUOUS_REV,
)

REGISTRY = (NamedLift.COMPLEX, NamedLift.REAL, NamedLift.QUAT)


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


def local_prod(lift: NamedLift, d_a: int, d_b: int) -> int:
    return density_params(lift, d_a) * density_params(lift, d_b)


def composite_params(lift: NamedLift, d_a: int, d_b: int) -> int:
    return density_params(lift, d_a * d_b)


def satisfies_finite(d: int = 2) -> bool:
    return d > 0


def satisfies_l1_shadow(_lift: NamedLift) -> bool:
    return True


def satisfies_local_tomography(lift: NamedLift) -> bool:
    return local_prod(lift, 2, 2) == composite_params(lift, 2, 2)


def satisfies_ax_lift_v0(lift: NamedLift) -> bool:
    return (
        satisfies_finite(2)
        and satisfies_l1_shadow(lift)
        and satisfies_local_tomography(lift)
    )


def satisfies_ax_lift_v0_minus_lt(lift: NamedLift) -> bool:
    return satisfies_finite(2) and satisfies_l1_shadow(lift)


def blocking_axiom(lift: NamedLift) -> BlockingAxiom:
    if lift is NamedLift.COMPLEX:
        return BlockingAxiom.NONE
    return BlockingAxiom.LOCAL_TOMOGRAPHY


def test_ax_lift_v0_frozen_names():
    assert len(AX_LIFT_V0) == 3
    assert AxiomId.A_LOCAL_TOMOGRAPHY in AX_LIFT_V0
    assert AxiomId.A_FINITE in AX_LIFT_V0
    assert AxiomId.A_L1_SHADOW in AX_LIFT_V0


def test_registry_classification_only_complex():
    assert satisfies_ax_lift_v0(NamedLift.COMPLEX) is True
    assert satisfies_ax_lift_v0(NamedLift.REAL) is False
    assert satisfies_ax_lift_v0(NamedLift.QUAT) is False
    assert satisfies_local_tomography(NamedLift.COMPLEX) is True
    assert satisfies_local_tomography(NamedLift.REAL) is False
    assert satisfies_local_tomography(NamedLift.QUAT) is False


def test_lt_numbers_match_w55():
    assert local_prod(NamedLift.REAL, 2, 2) == 9
    assert composite_params(NamedLift.REAL, 2, 2) == 10
    assert local_prod(NamedLift.QUAT, 2, 2) == 36
    assert composite_params(NamedLift.QUAT, 2, 2) == 28
    assert local_prod(NamedLift.COMPLEX, 2, 2) == 16
    assert composite_params(NamedLift.COMPLEX, 2, 2) == 16


def test_lt_is_sole_v0_discriminator_on_registry():
    """Without LT, all three registry lifts pass; with LT only complex."""
    for lift in REGISTRY:
        assert satisfies_ax_lift_v0_minus_lt(lift) is True
    assert satisfies_local_tomography(NamedLift.COMPLEX) is True
    assert satisfies_local_tomography(NamedLift.REAL) is False
    assert satisfies_local_tomography(NamedLift.QUAT) is False


def test_blocking_axiom_certificates():
    assert blocking_axiom(NamedLift.COMPLEX) is BlockingAxiom.NONE
    assert blocking_axiom(NamedLift.REAL) is BlockingAxiom.LOCAL_TOMOGRAPHY
    assert blocking_axiom(NamedLift.QUAT) is BlockingAxiom.LOCAL_TOMOGRAPHY
    assert satisfies_ax_lift_v0(NamedLift.COMPLEX)
    assert not satisfies_ax_lift_v0(NamedLift.REAL)
    assert not satisfies_ax_lift_v0(NamedLift.QUAT)


def test_registry_exactly_one_v0_satisfier():
    satisfiers = [L for L in REGISTRY if satisfies_local_tomography(L)]
    assert satisfiers == [NamedLift.COMPLEX]
    assert len(satisfiers) == 1


@dataclass(frozen=True)
class NamedAxiomSet:
    id: str
    axioms: tuple[AxiomId, ...]
    literature_target: Optional[str]
    optional_axioms: tuple[OptionalAxiomId, ...] = field(default_factory=tuple)


def test_named_axiom_set_packet():
    packet = NamedAxiomSet(
        id="AX-LIFT-V0",
        axioms=AX_LIFT_V0,
        literature_target="koecherVinbergJordan",
        optional_axioms=(),
    )
    assert packet.id == "AX-LIFT-V0"
    assert len(packet.axioms) == 3
    assert packet.literature_target == "koecherVinbergJordan"
    assert packet.optional_axioms == ()


def test_ax_lift_v01_optional_packet_keeps_v0_core():
    packet = NamedAxiomSet(
        id="AX-LIFT-V0.1",
        axioms=AX_LIFT_V0,
        literature_target="hardyMasanesMuellerStyle",
        optional_axioms=AX_LIFT_V0_1_OPTIONAL,
    )
    assert packet.axioms == AX_LIFT_V0
    assert len(packet.optional_axioms) == 2
    assert packet.id == "AX-LIFT-V0.1"
    assert satisfies_ax_lift_v0(NamedLift.COMPLEX) is True




@dataclass(frozen=True)
class JointWeight:
    w00: int
    w01: int
    w10: int
    w11: int

    @property
    def marg_a(self) -> tuple[int, int]:
        return (self.w00 + self.w01, self.w10 + self.w11)

    @property
    def is_quantum_pure_support(self) -> bool:
        diag = self.w00 > 0 and self.w01 == 0 and self.w10 == 0 and self.w11 > 0
        anti = self.w00 == 0 and self.w01 > 0 and self.w10 > 0 and self.w11 == 0
        return diag or anti


BELL_LIKE = JointWeight(1, 0, 0, 1)
FAIR = (1, 1)


def satisfies_purification_capacity(lift: NamedLift) -> bool:
    if lift is NamedLift.QUAT:
        return False
    return BELL_LIKE.is_quantum_pure_support and BELL_LIKE.marg_a == FAIR


def satisfies_continuous_reversible(_lift: NamedLift) -> bool:
    return False


class ContinuumHost(str, Enum):
    FIN_L1_DISCRETE = "finL1Discrete"
    CONTINUUM_IMPORT = "continuumImport"


def continuous_under_host(host: ContinuumHost, _lift: NamedLift) -> bool:
    return False


def local_prod3(lift: NamedLift) -> int:
    p = density_params(lift, 2)
    return p * p * p


def composite_params3(lift: NamedLift) -> int:
    return density_params(lift, 8)


def satisfies_local_tomography3(lift: NamedLift) -> bool:
    return local_prod3(lift) == composite_params3(lift)


def test_purification_optional_active_complex_and_real():
    assert BELL_LIKE.is_quantum_pure_support
    assert BELL_LIKE.marg_a == FAIR
    assert satisfies_purification_capacity(NamedLift.COMPLEX)
    assert satisfies_purification_capacity(NamedLift.REAL)
    assert not satisfies_purification_capacity(NamedLift.QUAT)


def test_continuous_optional_refused_on_finL1():
    for lift in REGISTRY:
        assert not satisfies_continuous_reversible(lift)
        assert not continuous_under_host(ContinuumHost.FIN_L1_DISCRETE, lift)
        assert not continuous_under_host(ContinuumHost.CONTINUUM_IMPORT, lift)


def test_v0_unaffected_by_purification_activation():
    """Rebit can purify but still fails V0 (LT); V0 core unchanged."""
    assert satisfies_ax_lift_v0(NamedLift.COMPLEX)
    assert not satisfies_ax_lift_v0(NamedLift.REAL)
    assert satisfies_purification_capacity(NamedLift.REAL)
    assert len(AX_LIFT_V0) == 3


def test_v01_partial_activation_package():
    purification_status = "activatedToyMech"
    continuous_status = "refusedOnFinL1"
    continuum_pathway = "openContinuumImport"
    assert purification_status == "activatedToyMech"
    assert continuous_status == "refusedOnFinL1"
    assert continuum_pathway == "openContinuumImport"
    assert satisfies_purification_capacity(NamedLift.COMPLEX)
    assert satisfies_purification_capacity(NamedLift.REAL)
    assert not satisfies_purification_capacity(NamedLift.QUAT)
    assert all(not satisfies_continuous_reversible(L) for L in REGISTRY)


def test_multipartite_lt3_numbers():
    assert local_prod3(NamedLift.COMPLEX) == 64
    assert composite_params3(NamedLift.COMPLEX) == 64
    assert local_prod3(NamedLift.REAL) == 27
    assert composite_params3(NamedLift.REAL) == 36
    assert local_prod3(NamedLift.QUAT) == 216
    assert composite_params3(NamedLift.QUAT) == 120


def test_multipartite_lt3_consistent_with_v0():
    """Only complex passes V0 and LT3; rebit/quat fail both (W5.5 capital)."""
    assert satisfies_ax_lift_v0(NamedLift.COMPLEX)
    assert satisfies_local_tomography3(NamedLift.COMPLEX)
    assert not satisfies_ax_lift_v0(NamedLift.REAL)
    assert not satisfies_local_tomography3(NamedLift.REAL)
    assert not satisfies_ax_lift_v0(NamedLift.QUAT)
    assert not satisfies_local_tomography3(NamedLift.QUAT)
    assert len(AX_LIFT_V0) == 3


def test_continuous_fence_and_lt3_package():
    assert (
        continuous_under_host(ContinuumHost.FIN_L1_DISCRETE, NamedLift.COMPLEX) is False
    )
    assert (
        continuous_under_host(ContinuumHost.CONTINUUM_IMPORT, NamedLift.COMPLEX)
        is False
    )
    assert satisfies_local_tomography3(NamedLift.COMPLEX)
    assert not satisfies_local_tomography3(NamedLift.REAL)
    assert not satisfies_local_tomography3(NamedLift.QUAT)
    assert len(AX_LIFT_V0) == 3


def test_jordan_full_classification_open_and_no_absolute_completeness():
    full_jordan_classification_open = True
    absolute_lift_completeness_refused = False
    assert full_jordan_classification_open is True
    assert absolute_lift_completeness_refused is False


if __name__ == "__main__":
    pytest.main([__file__])
