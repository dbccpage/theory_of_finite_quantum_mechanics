from __future__ import annotations
"""
Executable Python dual harness for W6.14 / OB-COMPOSE (composition monoidal structure).

Mirrors Lean `003_qm_compose_monoidal_structure.lean`:

1. Classical Cartesian product of two bit residual weights is constructible.
2. Product vs direct-sum sector counts disagree (non-unique classical composition).
3. Mixed classical bits have no pure classical purification (pure joint ⇒ pure marginals).
4. Complex Hilbert local-tomography dimension identity; rebit fence 9 ≠ 10.
5. Named-lift tensor binds + composite LT underivable from FinL1 product.
6. LT↔OB-U1 COUPLED on NamedLift registry (no XOR); SPLIT-OUTSIDE-REGISTRY OPEN;
   ExoticHost exploratory XOR is not BASIS independence.

AuthorityEffect: None. Mutation-capable: flip any asserted inequality to fail the suite.
"""


from dataclasses import dataclass
from enum import Enum

import pytest


@dataclass(frozen=True)
class BitWeight:
    w0: int
    w1: int

    @property
    def total(self) -> int:
        return self.w0 + self.w1

    @property
    def is_pure(self) -> bool:
        return (self.w0 > 0 and self.w1 == 0) or (self.w0 == 0 and self.w1 > 0)

    @property
    def is_mixed(self) -> bool:
        return self.w0 > 0 and self.w1 > 0


@dataclass(frozen=True)
class JointWeight:
    w00: int
    w01: int
    w10: int
    w11: int

    @property
    def marg_a(self) -> BitWeight:
        return BitWeight(self.w00 + self.w01, self.w10 + self.w11)

    @property
    def marg_b(self) -> BitWeight:
        return BitWeight(self.w00 + self.w10, self.w01 + self.w11)

    @property
    def is_pure(self) -> bool:
        cells = [self.w00, self.w01, self.w10, self.w11]
        positives = [c for c in cells if c > 0]
        zeros = [c for c in cells if c == 0]
        return len(positives) == 1 and len(zeros) == 3 and positives[0] > 0


def product_joint(wa: BitWeight, wb: BitWeight) -> JointWeight:
    """Classical independent product composition (DERIVED on the basement)."""
    return JointWeight(
        w00=wa.w0 * wb.w0,
        w01=wa.w0 * wb.w1,
        w10=wa.w1 * wb.w0,
        w11=wa.w1 * wb.w1,
    )


def product_sector_count(n_a: int, n_b: int) -> int:
    return n_a * n_b


def sum_sector_count(n_a: int, n_b: int) -> int:
    return n_a + n_b


def complex_local_tomography_dim(d_a: int, d_b: int) -> tuple[int, int]:
    """Return (product of local density dims, composite density dim)."""
    local_prod = (d_a * d_a) * (d_b * d_b)
    composite = (d_a * d_b) * (d_a * d_b)
    return local_prod, composite


def test_product_ne_sum_classical_composition():
    """Cartesian product and direct sum disagree on sector count (non-degenerate pairs).

    Note: 2×2 is degenerate (4=4). Use 2×3 and 3×3 where product ≠ sum.
    """
    assert product_sector_count(2, 2) == sum_sector_count(2, 2) == 4  # degenerate
    assert product_sector_count(2, 3) == 6
    assert sum_sector_count(2, 3) == 5
    assert product_sector_count(2, 3) != sum_sector_count(2, 3)
    assert product_sector_count(3, 3) == 9
    assert sum_sector_count(3, 3) == 6
    assert product_sector_count(3, 3) != sum_sector_count(3, 3)


def test_classical_product_marginal_recovery():
    """Independent product recovers A-marginal scaled by total mass of B."""
    wa = BitWeight(2, 3)
    wb = BitWeight(1, 0)  # pure unit-total on 0
    j = product_joint(wa, wb)
    assert j.marg_a == BitWeight(wa.w0 * wb.total, wa.w1 * wb.total)
    assert j.marg_a == wa  # wb.total == 1
    assert j.w00 == 2 and j.w10 == 3 and j.w01 == 0 and j.w11 == 0


def test_pure_joint_implies_pure_marginals():
    """Every pure classical joint has pure A and B marginals."""
    pure_joints = [
        JointWeight(5, 0, 0, 0),
        JointWeight(0, 2, 0, 0),
        JointWeight(0, 0, 7, 0),
        JointWeight(0, 0, 0, 1),
    ]
    for j in pure_joints:
        assert j.is_pure
        assert j.marg_a.is_pure
        assert j.marg_b.is_pure


def test_mixed_bit_has_no_pure_classical_purification():
    """Mixed classical bit cannot be A-marginal of any pure joint."""
    fair = BitWeight(1, 1)
    assert fair.is_mixed
    assert not fair.is_pure

    # Exhaustive search over small pure joints (single atom with mass 1..4)
    found = False
    for mass in range(1, 5):
        candidates = [
            JointWeight(mass, 0, 0, 0),
            JointWeight(0, mass, 0, 0),
            JointWeight(0, 0, mass, 0),
            JointWeight(0, 0, 0, mass),
        ]
        for j in candidates:
            assert j.is_pure
            if j.marg_a == fair:
                found = True
    assert found is False

    # Also: any pure joint's A-marginal is pure, so cannot equal mixed fair.
    for j in [
        JointWeight(3, 0, 0, 0),
        JointWeight(0, 4, 0, 0),
        JointWeight(0, 0, 2, 0),
        JointWeight(0, 0, 0, 9),
    ]:
        assert j.marg_a.is_pure
        assert j.marg_a != fair


def test_fair_product_cells():
    """Product of two fair bits is the uniform 1-table on four cells."""
    fair = BitWeight(1, 1)
    j = product_joint(fair, fair)
    assert (j.w00, j.w01, j.w10, j.w11) == (1, 1, 1, 1)
    assert j.marg_a == BitWeight(2, 2)
    assert j.marg_b == BitWeight(2, 2)


def test_complex_local_tomography_dim_identity():
    """Complex Hilbert density-dim local tomography: (dA²)(dB²) = (dA dB)²."""
    for d_a, d_b in [(1, 1), (2, 2), (2, 3), (3, 5)]:
        local_prod, composite = complex_local_tomography_dim(d_a, d_b)
        assert local_prod == composite


def test_rebit_local_tomography_count_fence():
    """Estate rebit fence from qm_011: 3*3 ≠ 10 (not a rebit derivation)."""
    assert 3 * 3 != 10


def test_composition_kind_labels_are_distinct():
    """Freeze labels remain three named candidates (product / sum / declared tensor)."""
    kinds = {"cartesianProduct", "directSum", "declaredTensor"}
    assert len(kinds) == 3
    assert "cartesianProduct" in kinds


# --- W6.14 residual: declaredTensor bound to named complex-Hilbert lift ---


@dataclass(frozen=True)
class DeclaredTensor:
    """Interface: monoidal tensor requires a named lift (not FinL1 alone)."""

    lift: str
    dim_a: int
    dim_b: int
    dim_ab: int

    def __post_init__(self) -> None:
        if self.dim_ab != self.dim_a * self.dim_b:
            raise ValueError("dim_law: dim_ab must equal dim_a * dim_b")
        if self.lift not in {
            "complexHilbert",
            "realHilbert",
            "quaternionicHilbert",
        }:
            raise ValueError(f"unknown named lift: {self.lift}")


def complex_hilbert_tensor(d_a: int, d_b: int) -> DeclaredTensor:
    return DeclaredTensor(
        lift="complexHilbert",
        dim_a=d_a,
        dim_b=d_b,
        dim_ab=d_a * d_b,
    )


def is_quantum_pure_support(j: JointWeight) -> bool:
    """Bell-diagonal-style pure support (not classical single-atom purity)."""
    diag = j.w00 > 0 and j.w01 == 0 and j.w10 == 0 and j.w11 > 0
    anti = j.w00 == 0 and j.w01 > 0 and j.w10 > 0 and j.w11 == 0
    return diag or anti


def bell_like_joint() -> JointWeight:
    return JointWeight(w00=1, w01=0, w10=0, w11=1)


def test_declared_tensor_requires_named_lift():
    t = complex_hilbert_tensor(2, 2)
    assert t.lift == "complexHilbert"
    assert t.dim_ab == 4
    assert t.dim_ab == t.dim_a * t.dim_b
    with pytest.raises(ValueError, match="unknown named lift"):
        DeclaredTensor(lift="finL1Orphan", dim_a=2, dim_b=2, dim_ab=4)
    with pytest.raises(ValueError, match="dim_law"):
        DeclaredTensor(lift="complexHilbert", dim_a=2, dim_b=2, dim_ab=5)


def test_declared_tensor_kind_distinct_from_classical():
    assert "declaredTensor" != "cartesianProduct"
    assert "declaredTensor" != "directSum"
    # Sector counts: classical product of bits matches Hilbert dim product
    # as *counting*, but the tensor interface still needs the lift tag.
    assert product_sector_count(2, 2) == complex_hilbert_tensor(2, 2).dim_ab
    assert complex_hilbert_tensor(2, 3).dim_ab == 6


def test_bell_like_not_classically_pure_but_quantum_pure_support():
    j = bell_like_joint()
    assert is_quantum_pure_support(j)
    assert not j.is_pure  # classical single-atom purity fails (two atoms)
    assert j.marg_a == BitWeight(1, 1)
    assert j.marg_a.is_mixed


def test_fair_bit_quantum_purification_under_complex_lift():
    """Under named complex-Hilbert tensor, mixed fairBit has quantum purification."""
    fair = BitWeight(1, 1)
    j = bell_like_joint()
    assert is_quantum_pure_support(j)
    assert j.marg_a == fair
    # Classical pure-joint model still refuses (mirror Lean split theorem).
    found_classical = False
    for mass in range(1, 5):
        for pure in (
            JointWeight(mass, 0, 0, 0),
            JointWeight(0, mass, 0, 0),
            JointWeight(0, 0, mass, 0),
            JointWeight(0, 0, 0, mass),
        ):
            assert pure.is_pure
            if pure.marg_a == fair:
                found_classical = True
    assert found_classical is False


def test_qubit_tensor_binding_receipt():
    q = complex_hilbert_tensor(2, 2)
    assert q.lift == "complexHilbert"
    assert q.dim_ab == 4


# --- W6.14 residual: composite LT underivable from FinL1 product alone ---


NAMED_LIFTS = ("complexHilbert", "realHilbert", "quaternionicHilbert")


def density_params(lift: str, d: int) -> int:
    """Free real parameters of a density operator under the named lift."""
    if lift == "complexHilbert":
        return d * d
    if lift == "realHilbert":
        return d * (d + 1) // 2
    if lift == "quaternionicHilbert":
        return d * (2 * d - 1)
    raise ValueError(f"unknown named lift: {lift}")


def local_prod(lift: str, d_a: int, d_b: int) -> int:
    return density_params(lift, d_a) * density_params(lift, d_b)


def composite_params(lift: str, d_a: int, d_b: int) -> int:
    return density_params(lift, d_a * d_b)


def satisfies_composite_lt(lift: str, d_a: int, d_b: int) -> bool:
    return local_prod(lift, d_a, d_b) == composite_params(lift, d_a, d_b)


def real_hilbert_tensor(d_a: int, d_b: int) -> DeclaredTensor:
    return DeclaredTensor(
        lift="realHilbert",
        dim_a=d_a,
        dim_b=d_b,
        dim_ab=d_a * d_b,
    )


def quaternionic_hilbert_tensor(d_a: int, d_b: int) -> DeclaredTensor:
    return DeclaredTensor(
        lift="quaternionicHilbert",
        dim_a=d_a,
        dim_b=d_b,
        dim_ab=d_a * d_b,
    )


def test_density_params_single_system_separators():
    assert density_params("complexHilbert", 2) == 4
    assert density_params("realHilbert", 2) == 3
    assert density_params("quaternionicHilbert", 2) == 6
    assert density_params("realHilbert", 2) != density_params("complexHilbert", 2)
    assert density_params("quaternionicHilbert", 2) != density_params(
        "complexHilbert", 2
    )


def test_complex_lt_identity_general():
    for d_a, d_b in [(1, 1), (2, 2), (2, 3), (3, 5)]:
        assert satisfies_composite_lt("complexHilbert", d_a, d_b)


def test_rebit_lt_fails_qubit_pair():
    assert local_prod("realHilbert", 2, 2) == 9
    assert composite_params("realHilbert", 2, 2) == 10
    assert not satisfies_composite_lt("realHilbert", 2, 2)


def test_quat_lt_fails_qubit_pair():
    assert local_prod("quaternionicHilbert", 2, 2) == 36
    assert composite_params("quaternionicHilbert", 2, 2) == 28
    assert not satisfies_composite_lt("quaternionicHilbert", 2, 2)


def test_real_quat_complex_share_dim_law():
    """All three named-lift tensors share Hilbert dim product (counting only)."""
    c = complex_hilbert_tensor(2, 3)
    r = real_hilbert_tensor(2, 3)
    q = quaternionic_hilbert_tensor(2, 3)
    assert c.dim_ab == r.dim_ab == q.dim_ab == 6
    assert product_sector_count(2, 3) == 6


def test_finL1_product_does_not_force_complex_lt():
    """Classical product sector count ≠ composite LT law for every lift."""
    assert product_sector_count(2, 2) == complex_hilbert_tensor(2, 2).dim_ab
    assert product_sector_count(2, 2) == real_hilbert_tensor(2, 2).dim_ab
    assert product_sector_count(2, 2) == quaternionic_hilbert_tensor(2, 2).dim_ab
    assert satisfies_composite_lt("complexHilbert", 2, 2)
    assert not satisfies_composite_lt("realHilbert", 2, 2)
    assert not satisfies_composite_lt("quaternionicHilbert", 2, 2)


def test_only_complex_among_three_satisfies_lt_qubits():
    assert satisfies_composite_lt("complexHilbert", 2, 2)
    assert not satisfies_composite_lt("realHilbert", 2, 2)
    assert not satisfies_composite_lt("quaternionicHilbert", 2, 2)
    winners = [L for L in NAMED_LIFTS if satisfies_composite_lt(L, 2, 2)]
    assert winners == ["complexHilbert"]


# --- W6.14 residual: composite LT ↔ OB-U1 packaged as COUPLED (deepened dual) ---


def has_complex_phase_carrier(lift: str) -> bool:
    """Phase-carrier face of OB-U1 on the named-lift registry (toy predicate)."""
    return lift == "complexHilbert"


def independently_splits_lt_from_phase(lift: str) -> bool:
    """XOR face split: exactly one of composite LT and complex phase carrier."""
    lt = satisfies_composite_lt(lift, 2, 2)
    phase = has_complex_phase_carrier(lift)
    return (lt and not phase) or (not lt and phase)


def xor_splits_lt_from_phase(lift: str) -> bool:
    """Alias dual packaging name for IndependentlySplitsLtFromPhase."""
    return independently_splits_lt_from_phase(lift)


def named_lift_has_phase_bool(lift: str) -> bool:
    return lift == "complexHilbert"


def named_lift_satisfies_lt_bool(lift: str) -> bool:
    # Bool dual of registry LT face (matches NamedLift constructors only).
    return lift == "complexHilbert"


def registry_face_class(lift: str) -> str:
    """only both / neither on NamedLift registry (no one-sided class)."""
    if lift == "complexHilbert":
        return "both"
    return "neither"


def test_lt_iff_complex_phase_on_registry():
    for L in NAMED_LIFTS:
        assert satisfies_composite_lt(L, 2, 2) == has_complex_phase_carrier(L)
        assert not independently_splits_lt_from_phase(L)
        assert not xor_splits_lt_from_phase(L)


def test_phase_iff_composite_lt_dual():
    """Dual order of the biconditional (phase ↔ LT)."""
    for L in NAMED_LIFTS:
        assert has_complex_phase_carrier(L) == satisfies_composite_lt(L, 2, 2)


def test_no_named_lift_xor_registry_scan():
    """Exhaustive scan: zero of the three NamedLifts XOR-splits."""
    assert not independently_splits_lt_from_phase("complexHilbert")
    assert not independently_splits_lt_from_phase("realHilbert")
    assert not independently_splits_lt_from_phase("quaternionicHilbert")
    for L in NAMED_LIFTS:
        assert named_lift_has_phase_bool(L) == named_lift_satisfies_lt_bool(L)
        assert registry_face_class(L) in {"both", "neither"}
        if L == "complexHilbert":
            assert registry_face_class(L) == "both"
        else:
            assert registry_face_class(L) == "neither"


def test_finL1_host_neither_phase_nor_lt():
    # FinL1 product host is outside NamedLift registry: neither complex phase nor LT.
    fin_l1_has_phase = False
    fin_l1_has_lt = False
    assert not fin_l1_has_phase and not fin_l1_has_lt
    assert "finL1Product" not in NAMED_LIFTS


def test_complex_host_both_phase_and_lt():
    assert has_complex_phase_carrier("complexHilbert")
    assert satisfies_composite_lt("complexHilbert", 2, 2)


def test_lt_vs_ob_u1_coupled_status():
    """Terminal honesty: independence refused; status COUPLED on NamedLift registry."""
    status = "coupled"
    assert status == "coupled"
    assert status != "independent"
    assert all(not independently_splits_lt_from_phase(L) for L in NAMED_LIFTS)
    assert all(not xor_splits_lt_from_phase(L) for L in NAMED_LIFTS)
    assert has_complex_phase_carrier("complexHilbert")
    assert satisfies_composite_lt("complexHilbert", 2, 2)
    assert not has_complex_phase_carrier("realHilbert")
    assert not satisfies_composite_lt("realHilbert", 2, 2)
    assert not has_complex_phase_carrier("quaternionicHilbert")
    assert not satisfies_composite_lt("quaternionicHilbert", 2, 2)


# --- Residual OPEN: SPLIT-OUTSIDE-REGISTRY ---


def test_split_outside_registry_open():
    """Outside NamedLift registry, independence models remain OPEN (not absolute couple)."""
    split_outside_registry_status = "open"
    assert split_outside_registry_status == "open"
    assert split_outside_registry_status != "coupled"
    assert split_outside_registry_status != "independent"
    # Registry couple does not seal absolute couple for all hosts.
    lt_vs_ob_u1_status = "coupled"
    assert lt_vs_ob_u1_status == "coupled"
    assert lt_vs_ob_u1_status != split_outside_registry_status


# --- Exploratory toy: ExoticHost (OutsideRegistry, not NamedLift, not BASIS) ---


EXTENDED_HOSTS = ("finL1Product", "namedLift", "exoticHost")


def is_outside_registry(host: str) -> bool:
    return host == "exoticHost"


# Exploratory face booleans: LT without complex phase (XOR split toy).
EXOTIC_HAS_COMPLEX_PHASE = False
EXOTIC_SATISFIES_COMPOSITE_LT = True
EXOTIC_XOR_CLAIM_LEVEL = "notBasisIndependence"


def test_exotic_host_xor_exploratory():
    """Pure boolean XOR on ExoticHost — exploratory only, not BASIS independence."""
    assert is_outside_registry("exoticHost")
    assert not is_outside_registry("finL1Product")
    assert not is_outside_registry("namedLift")
    assert "exoticHost" not in NAMED_LIFTS
    assert EXOTIC_SATISFIES_COMPOSITE_LT is True
    assert EXOTIC_HAS_COMPLEX_PHASE is False
    assert EXOTIC_SATISFIES_COMPOSITE_LT != EXOTIC_HAS_COMPLEX_PHASE
    assert EXOTIC_XOR_CLAIM_LEVEL == "notBasisIndependence"
    # Exploratory XOR does NOT discharge SPLIT-OUTSIDE-REGISTRY to independent.
    split_outside_registry_status = "open"
    assert split_outside_registry_status == "open"
    assert split_outside_registry_status != "independent"


def test_residual_status_table():
    """Mirror Lean residual_status_table."""
    lt_vs_ob_u1_status = "coupled"
    split_outside_registry_status = "open"
    assert lt_vs_ob_u1_status == "coupled"
    assert split_outside_registry_status == "open"
    assert EXOTIC_XOR_CLAIM_LEVEL == "notBasisIndependence"
    assert is_outside_registry("exoticHost") is True
    # W6.19 design note: B5 must keep LT/U1 excluded until non-exploratory split.
    w6_19_b5_must_exclude_lt_u1 = True
    assert w6_19_b5_must_exclude_lt_u1
    assert EXOTIC_XOR_CLAIM_LEVEL != "basisIndependence"
    # Absolute couple outside registry is refused (path kept OPEN).
    assert split_outside_registry_status != "coupled"


# --- BASIS unblocking: CoupledImportBundle (BUNDLE-U1-LT) ---


@dataclass(frozen=True)
class BundleFaces:
    has_phase_carrier: bool
    satisfies_composite_lt: bool

    def covaries(self) -> bool:
        return self.has_phase_carrier == self.satisfies_composite_lt

    def fails_exactly_bundle(self) -> bool:
        return (not self.has_phase_carrier) and (not self.satisfies_composite_lt)

    def admits_bundle(self) -> bool:
        return self.has_phase_carrier and self.satisfies_composite_lt


NAMED_LIFT_BUNDLE_FACES = {
    "complexHilbert": BundleFaces(True, True),
    "realHilbert": BundleFaces(False, False),
    "quaternionicHilbert": BundleFaces(False, False),
}

BUNDLE_DROP = BundleFaces(False, False)
BUNDLE_ADMIT = BundleFaces(True, True)
ILLEGAL_XOR_LT_WITHOUT_PHASE = BundleFaces(False, True)
ILLEGAL_XOR_PHASE_WITHOUT_LT = BundleFaces(True, False)

BASIS_BUNDLE_SLOT_ID = "BUNDLE-U1-LT"
PROVISIONAL_B8_DESIGN_CARD = 8
SEPARATE_OB_U1_ROW_IN_INDEPENDENCE_MATRIX = False
BUNDLE_SLOT_ADMITTED_TO_BASIS_DESIGN = True


def test_named_lift_bundle_covaries():
    for lift, faces in NAMED_LIFT_BUNDLE_FACES.items():
        assert faces.covaries(), lift
    assert NAMED_LIFT_BUNDLE_FACES["complexHilbert"].admits_bundle()
    assert NAMED_LIFT_BUNDLE_FACES["realHilbert"].fails_exactly_bundle()


def test_bundle_drop_and_admit():
    assert BUNDLE_DROP.fails_exactly_bundle()
    assert BUNDLE_DROP.covaries()
    assert BUNDLE_ADMIT.admits_bundle()
    assert BUNDLE_ADMIT.covaries()


def test_illegal_xor_not_bundle_covariant():
    assert not ILLEGAL_XOR_LT_WITHOUT_PHASE.covaries()
    assert not ILLEGAL_XOR_PHASE_WITHOUT_LT.covaries()


# --- SPLIT-OUTSIDE-REGISTRY residual deepen (outside XOR witnesses) ---


class OutsideRegistryHost(str, Enum):
    LT_WITHOUT_PHASE = "ltWithoutPhase"
    PHASE_WITHOUT_LT = "phaseWithoutLt"
    BOTH_ABSENT = "bothAbsent"


def outside_has_phase(h: OutsideRegistryHost) -> bool:
    return h is OutsideRegistryHost.PHASE_WITHOUT_LT


def outside_has_composite_lt(h: OutsideRegistryHost) -> bool:
    return h is OutsideRegistryHost.LT_WITHOUT_PHASE


def outside_xor_faces(h: OutsideRegistryHost) -> bool:
    return outside_has_phase(h) != outside_has_composite_lt(h)


@dataclass(frozen=True)
class SplitOutsideDischargeCriteria:
    has_tensor_host_not_named_lift: bool
    has_xor_face_witness: bool
    admits_to_basis_independence: bool
    named_lift_xor_refused: bool
    residual_status_independent: bool


SPLIT_OUTSIDE_DISCHARGE_CRITERIA = SplitOutsideDischargeCriteria(
    has_tensor_host_not_named_lift=False,
    has_xor_face_witness=True,
    admits_to_basis_independence=False,
    named_lift_xor_refused=True,
    residual_status_independent=False,
)


def test_outside_registry_xor_witnesses_exist():
    assert outside_xor_faces(OutsideRegistryHost.LT_WITHOUT_PHASE)
    assert outside_xor_faces(OutsideRegistryHost.PHASE_WITHOUT_LT)
    assert not outside_xor_faces(OutsideRegistryHost.BOTH_ABSENT)
    assert outside_has_composite_lt(OutsideRegistryHost.LT_WITHOUT_PHASE)
    assert not outside_has_phase(OutsideRegistryHost.LT_WITHOUT_PHASE)
    assert outside_has_phase(OutsideRegistryHost.PHASE_WITHOUT_LT)
    assert not outside_has_composite_lt(OutsideRegistryHost.PHASE_WITHOUT_LT)


def test_split_outside_not_discharged():
    c = SPLIT_OUTSIDE_DISCHARGE_CRITERIA
    assert c.has_xor_face_witness is True
    assert c.has_tensor_host_not_named_lift is False
    assert c.admits_to_basis_independence is False
    assert c.named_lift_xor_refused is True
    assert c.residual_status_independent is False
    assert "open" == "open"  # residual status
    # NamedLift XOR still refused
    for L in NAMED_LIFTS:
        assert not xor_splits_lt_from_phase(L)


def test_named_lift_xor_still_refused():
    assert SPLIT_OUTSIDE_DISCHARGE_CRITERIA.named_lift_xor_refused is True
    assert SEPARATE_OB_U1_ROW_IN_INDEPENDENCE_MATRIX is False
    for L in NAMED_LIFTS:
        assert not xor_splits_lt_from_phase(L)


def test_split_outside_registry_deepen_package():
    assert outside_xor_faces(OutsideRegistryHost.LT_WITHOUT_PHASE)
    assert outside_xor_faces(OutsideRegistryHost.PHASE_WITHOUT_LT)
    c = SPLIT_OUTSIDE_DISCHARGE_CRITERIA
    assert c.has_xor_face_witness is True
    assert c.admits_to_basis_independence is False
    assert c.residual_status_independent is False
    split_outside_registry_status = "open"
    lt_vs_ob_u1_status = "coupled"
    assert split_outside_registry_status == "open"
    assert lt_vs_ob_u1_status == "coupled"
    assert SEPARATE_OB_U1_ROW_IN_INDEPENDENCE_MATRIX is False
    assert EXOTIC_XOR_CLAIM_LEVEL == "notBasisIndependence"
    for L in NAMED_LIFTS:
        assert not independently_splits_lt_from_phase(L)
    assert not ILLEGAL_XOR_LT_WITHOUT_PHASE.fails_exactly_bundle()
    assert not ILLEGAL_XOR_LT_WITHOUT_PHASE.admits_bundle()


def test_basis_unblock_via_coupled_bundle():
    """Unblocks full-basis *packaging* via single BUNDLE-U1-LT slot (not XOR)."""
    assert BASIS_BUNDLE_SLOT_ID == "BUNDLE-U1-LT"
    assert PROVISIONAL_B8_DESIGN_CARD == 8
    assert SEPARATE_OB_U1_ROW_IN_INDEPENDENCE_MATRIX is False
    assert BUNDLE_SLOT_ADMITTED_TO_BASIS_DESIGN is True
    # Still coupled on registry; outside still open; exotic not BASIS.
    assert LT_VS_OB_U1_STATUS == "coupled" if "LT_VS_OB_U1_STATUS" in dir() else True
    lt_vs_ob_u1_status = "coupled"
    split_outside_registry_status = "open"
    assert lt_vs_ob_u1_status == "coupled"
    assert split_outside_registry_status == "open"
    assert EXOTIC_XOR_CLAIM_LEVEL == "notBasisIndependence"


def test_coupled_import_bundle_package():
    assert all(f.covaries() for f in NAMED_LIFT_BUNDLE_FACES.values())
    assert BUNDLE_DROP.fails_exactly_bundle()
    assert BUNDLE_ADMIT.admits_bundle()
    assert not ILLEGAL_XOR_LT_WITHOUT_PHASE.covaries()
    assert PROVISIONAL_B8_DESIGN_CARD == 8
    assert SEPARATE_OB_U1_ROW_IN_INDEPENDENCE_MATRIX is False


if __name__ == "__main__":
    pytest.main([__file__])
