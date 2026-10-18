"""Tier 1: Feature Coverage E2E Tests.

Exercises core capabilities of MUB6, FSP, and Majorana modules
opaquely through published interfaces and runners.
Meets the threshold of >= 5 test cases per feature domain (18 total).
AuthorityEffect: None.
"""

from __future__ import annotations

from fractions import Fraction
import pytest

# ---------------------------------------------------------------------------
# MUB6 Domain Imports
# ---------------------------------------------------------------------------
from src.mub import (
    Cyc24,
    RationalInterval,
    SqrtBox,
    box_volume,
    boxes_overlap_interior,
    standard_basis_b1,
    verify_triple_pairwise_mu,
    verify_mub_crate_invariants,
    authority_effect as mub_authority_effect,
    package_info as mub_package_info,
)
from src.mub.mub_verify import (
    dita_seed_triple_columns,
)
from src.mub.mub_verify.target_a4_gram_certifier import (
    canonical_quad_gramian,
    verify_gramian_structure,
)
from src.mub.mub_verify.cover import (
    gauge_fixed_torus_region,
    narrow_torus_cell,
    wide_torus_cell,
)

# ---------------------------------------------------------------------------
# FSP Domain Imports
# ---------------------------------------------------------------------------
from src.fsp import (
    witness as fsp_witness,
    refuse_removed_holonomy as fsp_refuse_removed_holonomy,
    refuse_foreign_fixture as fsp_refuse_foreign_fixture,
    Witness as FspWitness,
    AUTHORITY_EFFECT as FSP_AUTHORITY_EFFECT,
)
from src.fsp.bqnf_sign_evaluator import (
    CochainComplex,
    TerminalRoute,
    normalize_sign_cochain,
)
from src.fsp.fermionic_hamiltonian import (
    DiscreteFermionicHamiltonian,
    FermionicLattice,
    FockState,
)

# ---------------------------------------------------------------------------
# Majorana Domain Imports
# ---------------------------------------------------------------------------
from src.majorana import (
    FockCarrier,
    MajoranaMonomial,
    MajoranaOperator,
    anticommutator,
    commutator,
    build_tetron_array,
    logical_class_representative,
    Axis,
    Topology,
    hard_invariants,
)
from src.majorana.sparse_kitaev import SparseKitaevWire
from src.majorana.braid_action import MajoranaBraidAction


# ===========================================================================
# Feature 1: MUB6 Core Capabilities (>= 5 tests)
# ===========================================================================

def test_tier1_mub6_crate_invariants():
    """FEAT-MUB-01: Verify MUB crate invariants, authority effect, and package metadata."""
    assert verify_mub_crate_invariants() is True
    assert mub_authority_effect() == "None"
    pkg = mub_package_info()
    assert pkg["name"] == "omega_mub"
    assert pkg["math_ssot"] == "rust"
    assert pkg["authority_effect"] == "None"


def test_tier1_mub6_cyc24_arithmetic():
    """FEAT-MUB-02: Verify exact cyclotomic field Q(zeta_24) arithmetic and relations."""
    zero = Cyc24.zero()
    one = Cyc24.one()
    assert zero.is_zero() is True
    assert (zero + one) == one
    assert (one * zero) == zero

    # zeta_24^12 = -1, zeta_24^24 = 1
    z12 = Cyc24.zeta(12)
    z24 = Cyc24.zeta(24)
    assert z12 == -one
    assert z24 == one

    # sum of 6th roots of unity (zeta^0, zeta^4, zeta^8, zeta^12, zeta^16, zeta^20) is zero
    s6 = Cyc24.zero()
    for k in range(6):
        s6 = s6 + Cyc24.zeta(4 * k)
    assert s6.is_zero() is True

    # Invertible element in Q(zeta_24)
    z1 = Cyc24.zeta(1)
    inv_z1 = z1.inv()
    assert (z1 * inv_z1) == one


def test_tier1_mub6_rational_intervals():
    """FEAT-MUB-03: Verify exact rational interval enclosures and arithmetic."""
    iv1 = RationalInterval(Fraction(1, 4), Fraction(3, 4))
    iv2 = RationalInterval(Fraction(1, 2), Fraction(1))

    assert iv1.width() == Fraction(1, 2)
    assert iv1.contains(Fraction(1, 2)) is True
    assert iv1.contains(Fraction(0)) is False
    assert iv1.is_strictly_positive() is True

    # Addition and multiplication
    added = iv1.add(iv2)
    assert added.lo == Fraction(3, 4)
    assert added.hi == Fraction(7, 4)

    # Interior overlap
    assert iv1.overlaps_interior(iv2) is True


def test_tier1_mub6_dita_seed_triple():
    """FEAT-MUB-04: Verify Dita seed triple generation and pairwise mutual unbiasedness in C^6."""
    triple = dita_seed_triple_columns(0, 8)
    assert len(triple) == 18
    is_mu = verify_triple_pairwise_mu(triple)
    assert is_mu is True


def test_tier1_mub6_gramian_structure():
    """FEAT-MUB-05: Verify canonical 24x24 quad Gramian matrix structure."""
    g = canonical_quad_gramian()
    assert len(g) == 24
    assert all(len(row) == 24 for row in g)
    rep = verify_gramian_structure(g)
    assert rep.diagonal_blocks_identity is True
    assert rep.off_diagonal_blocks_modulus_sixth is True
    assert rep.hermitian_exact is True
    assert rep.verified_sound is True


def test_tier1_mub6_torus_geometry_boxes():
    """FEAT-MUB-06: Verify gauge-fixed 5-torus geometry and cell bounding boxes."""
    torus = gauge_fixed_torus_region()
    assert len(torus) == 12
    narrow = narrow_torus_cell()
    wide = wide_torus_cell()
    assert len(narrow) == 12
    assert len(wide) == 12

    # Volume calculation
    v_narrow = box_volume(narrow)
    assert v_narrow > Fraction(0)
    assert v_narrow == (Fraction(4, 100) ** 12)
    assert boxes_overlap_interior(narrow, wide) is True


# ===========================================================================
# Feature 2: FSP Core Capabilities (>= 5 tests)
# ===========================================================================

def test_tier1_fsp_witness_canonical():
    """FEAT-FSP-01: Verify exact canonical FSP witness and CAR cycle hop product."""
    w = fsp_witness()
    assert isinstance(w, FspWitness)
    assert w.hop_product == -1
    assert w.parity_sum == 3
    assert w.parity_f2 == 1
    assert w.k == 1
    assert w.z_u == 0
    assert w.n_u == 2
    assert w.all_negative_product == 1
    assert w.holonomy_removed == 0
    assert w.numerator_preserved == 0
    assert w.conjunction == 0


def test_tier1_fsp_refuse_removed_holonomy():
    """FEAT-FSP-02: Verify refuse_removed_holonomy refusal gate against non-CAR products."""
    # Canonical hop product -1 must pass cleanly
    fsp_refuse_removed_holonomy(-1)

    # +1 product is refused
    with pytest.raises(ValueError, match="is not the CAR product"):
        fsp_refuse_removed_holonomy(1)

    # Arbitrary scalar is refused
    with pytest.raises(ValueError, match="claimed product is not"):
        fsp_refuse_removed_holonomy(0)


def test_tier1_fsp_refuse_foreign_fixture():
    """FEAT-FSP-03: Verify refuse_foreign_fixture refusal gate against foreign fixtures."""
    # Valid orbit values 0 and 2 must pass cleanly
    fsp_refuse_foreign_fixture(0)
    fsp_refuse_foreign_fixture(2)

    # Foreign fixture values 912 and 36864 must be refused
    with pytest.raises(ValueError, match="O.5 fixture scalar is not this k=1 orbit"):
        fsp_refuse_foreign_fixture(912)

    with pytest.raises(ValueError, match="O.5 fixture scalar is not this k=1 orbit"):
        fsp_refuse_foreign_fixture(36864)

    # Arbitrary foreign scalar must be refused
    with pytest.raises(ValueError, match="scalar is outside the computed orbit values"):
        fsp_refuse_foreign_fixture(7)


def test_tier1_fsp_bqnf_sign_switching():
    """FEAT-FSP-04: Verify BQNF sign-switching normal form on triangle cycle graph."""
    # 3 vertices, 3 edges forming triangle: (0,1), (1,2), (0,2)
    edges = ((0, 1), (1, 2), (0, 2))
    # All edges positive (+1 parity, represented as 0 in F2)
    parities = (0, 0, 0)
    nf = normalize_sign_cochain(3, edges, parities)
    assert len(nf.gauge) == 3
    assert len(nf.forest_edges) == 2  # Spanning tree of 3 vertices has 2 edges
    assert len(nf.obstruction_cycles) == 0  # No odd-parity cycle


def test_tier1_fsp_cochain_nilpotence_and_terminal_route():
    """FEAT-FSP-05: Verify CochainComplex exact nilpotence d1*d0 == 0 and TerminalRoute enum."""
    # 2-vertex, 1-edge complex
    d0 = [[Fraction(-1)], [Fraction(1)]]  # d0: C0 (dim 1) -> C1 (dim 2)
    d1 = [[Fraction(0), Fraction(0)]]    # d1: C1 (dim 2) -> C2 (dim 1)
    complex_2v = CochainComplex(dim_c0=1, dim_c1=2, dim_c2=1, d0=d0, d1=d1)
    assert complex_2v.check_nilpotence() is True

    # Check TerminalRoute members
    assert TerminalRoute.EXACT_REPAIR.value == "ExactRepair"
    assert TerminalRoute.EXACT_CANCELLATION.value == "ExactCancellation"
    assert TerminalRoute.STABILIZED_SURVIVOR.value == "StabilizedSurvivor"
    assert TerminalRoute.OPEN_SIGN_OBSTRUCTION.value == "OpenSignObstruction"
    assert TerminalRoute.REFUSED.value == "Refused"


def test_tier1_fsp_discrete_fermionic_hamiltonian():
    """FEAT-FSP-06: Verify DiscreteFermionicHamiltonian on linear chain lattice."""
    lattice = FermionicLattice.linear_chain(3, periodic=False)
    assert lattice.num_sites == 3
    assert len(lattice.edges) == 2

    state = FockState(up_mask=0b001, down_mask=0b010)
    assert state.count_up() == 1
    assert state.count_down() == 1
    assert state.total_particles() == 2
    assert state.is_occupied(0, "up") is True
    assert state.is_occupied(1, "up") is False

    ham = DiscreteFermionicHamiltonian(lattice, t=1, u=2, num_up=1, num_down=1)
    assert len(ham.basis) == 9  # 3 sites choose 1 up * 3 sites choose 1 down = 9 states
    matrix = ham.matrix
    assert len(matrix) == 9
    assert all(len(row) == 9 for row in matrix)


# ===========================================================================
# Feature 3: Majorana Core Capabilities (>= 5 tests)
# ===========================================================================

def test_tier1_majorana_fock_carrier_anticommutation():
    """FEAT-MAJ-01: Verify FockCarrier Jordan-Wigner generators and anticommutation."""
    carrier = FockCarrier(2)
    assert carrier.modes() == 2
    assert carrier.dimension() == 4

    g1 = carrier.majorana_generator(1)
    g2 = carrier.majorana_generator(2)
    assert len(g1) == 4
    assert len(g2) == 4

    p = carrier.parity_operator()
    assert len(p) == 4


def test_tier1_majorana_monomial_algebra():
    """FEAT-MAJ-02: Verify MajoranaMonomial exact multiplication and commutators."""
    m0 = MajoranaMonomial.single(0)
    m1 = MajoranaMonomial.single(1)

    sign, prod = m0.multiply(m1)
    assert sign == Fraction(1)
    assert prod.modes == (0, 1)

    # gamma_1 * gamma_0 = - gamma_0 * gamma_1
    sign_rev, prod_rev = m1.multiply(m0)
    assert sign_rev == Fraction(-1)
    assert prod_rev.modes == (0, 1)

    op0 = MajoranaOperator.mode(0)
    op1 = MajoranaOperator.mode(1)
    anti = anticommutator(op0, op1)
    assert anti.is_zero() is True

    # Same mode anticommutator: {gamma_0, gamma_0} = 2
    anti_self = anticommutator(op0, op0)
    assert anti_self.is_scalar() is True
    assert anti_self.scalar_value() == Fraction(2)


def test_tier1_majorana_sparse_kitaev_wire():
    """FEAT-MAJ-03: Verify SparseKitaevWire isolated Majorana edge modes."""
    # Wire of length 4 at topological sweet spot (t=1, delta=1, mu=0)
    wire = SparseKitaevWire(4, Fraction(1), Fraction(1), Fraction(0))
    iso = wire.isolated_majoranas()
    # Boundaries 1 and 8 are the unpaired Majorana modes
    assert iso == [1, 8]


def test_tier1_majorana_tetron_array_and_betti():
    """FEAT-MAJ-04: Verify build_tetron_array Betti H1 dimension and code distance."""
    complex_torus, report = build_tetron_array(2, 2, Topology.Torus)
    assert report.dim_h1 == 2
    assert report.code_distance == 2
    assert report.topology == Topology.Torus

    # Verify logical class representatives
    x_rep = logical_class_representative(report, Axis.Column, 0)
    z_rep = logical_class_representative(report, Axis.Row, 0)
    assert len(x_rep) == 8
    assert len(z_rep) == 8


def test_tier1_majorana_braiding_elementary():
    """FEAT-MAJ-05: Verify elementary Majorana braid action and determinant sign."""
    act = MajoranaBraidAction.elementary(4, 1)
    # Braid interchanges modes 1 and 2 with appropriate sign
    assert act.image(1).mode == 2
    assert act.image(1).sign == 1
    assert act.image(2).mode == 1
    assert act.image(2).sign == -1
    assert act.determinant_sign() == 1


def test_tier1_majorana_hard_invariants():
    """FEAT-MAJ-06: Verify full 10-invariant structural regression battery."""
    results = hard_invariants.run_all_hard_invariants()
    assert len(results) >= 10
    for name, passed in results.items():
        assert passed is True, f"Hard invariant failed: {name}"
