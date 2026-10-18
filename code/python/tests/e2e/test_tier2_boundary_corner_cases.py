"""Tier 2: Boundary Value Analysis & Corner Cases E2E Tests.

Exercises boundary limits, zero/negative, empty inputs, extreme configurations,
and refusal walls across MUB6, FSP, and Majorana modules.
Meets the threshold of >= 5 test cases per feature domain (17 total).
AuthorityEffect: None.
"""

from __future__ import annotations

from fractions import Fraction
import math
import pytest

# ---------------------------------------------------------------------------
# MUB6 Domain Imports
# ---------------------------------------------------------------------------
from src.mub import (
    Cyc24,
    RationalInterval,
    sqrt_rational_interval,
    verify_triple_pairwise_mu,
)
from src.mub.mub_verify import (
    dita_seed_triple_columns,
)
from src.mub.mub_verify.target_a4_gram_certifier import (
    verify_gramian_structure,
)

# ---------------------------------------------------------------------------
# FSP Domain Imports
# ---------------------------------------------------------------------------
from src.fsp import (
    refuse_removed_holonomy as fsp_refuse_removed_holonomy,
    refuse_foreign_fixture as fsp_refuse_foreign_fixture,
)
from src.fsp.bqnf_sign_evaluator import (
    CochainComplex,
    exact_rational,
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
    MajoranaError,
    MajoranaMonomial,
    MajoranaOperator,
    build_tetron_array,
    MAX_MODES,
    Topology,
)
from src.majorana.sparse_kitaev import SparseKitaevWire
from src.majorana.braid_action import (
    BraidActionError,
    MajoranaBraidAction,
    SignedMajorana,
)


# ===========================================================================
# Feature 1: MUB6 Boundary & Corner Cases (>= 5 tests)
# ===========================================================================

def test_tier2_mub6_degenerate_point_interval():
    """FEAT-MUB-B01: Verify degenerate point intervals [r, r] with zero width."""
    pt = RationalInterval.point(Fraction(3, 7))
    assert pt.lo == Fraction(3, 7)
    assert pt.hi == Fraction(3, 7)
    assert pt.width() == Fraction(0)
    assert pt.contains(Fraction(3, 7)) is True
    assert pt.contains(Fraction(4, 7)) is False

    # Adding two point intervals gives exact point sum
    pt2 = RationalInterval.point(Fraction(4, 7))
    sum_pt = pt.add(pt2)
    assert sum_pt.lo == Fraction(1)
    assert sum_pt.hi == Fraction(1)
    assert sum_pt.width() == Fraction(0)


def test_tier2_mub6_inverted_interval_bounds_rejection():
    """FEAT-MUB-B02: Verify rejection when lower bound exceeds upper bound."""
    with pytest.raises(ValueError, match="Invalid interval: lo .* > hi"):
        RationalInterval(lo=Fraction(2), hi=Fraction(1))

    with pytest.raises(ValueError, match="Invalid interval"):
        RationalInterval(lo=Fraction(1, 2), hi=Fraction(1, 3))


def test_tier2_mub6_sqrt_interval_lower_limit_and_negatives():
    """FEAT-MUB-B03: Verify sqrt_rational_interval at n=1 and rejection of non-positive n."""
    # n = 1: square root is exactly 1
    iv1 = sqrt_rational_interval(1, iters=10)
    assert iv1.contains(Fraction(1)) is True

    # n < 1 must be rejected
    with pytest.raises(ValueError, match="n must be >= 1"):
        sqrt_rational_interval(0)

    with pytest.raises(ValueError, match="n must be >= 1"):
        sqrt_rational_interval(-4)


def test_tier2_mub6_cyc24_zero_inversion_rejection():
    """FEAT-MUB-B04: Verify ZeroDivisionError when inverting zero in Q(zeta_24)."""
    zero = Cyc24.zero()
    with pytest.raises(ZeroDivisionError, match="Cannot invert zero"):
        zero.inv()

    one = Cyc24.one()
    with pytest.raises(ZeroDivisionError, match="Cannot invert zero"):
        one.div(zero)


def test_tier2_mub6_dita_seed_invalid_coordinates_rejection():
    """FEAT-MUB-B05: Verify rejection of uncertified non-seed coordinates for Dita triples."""
    with pytest.raises(ValueError, match="is not a locked genuine Dita seed"):
        dita_seed_triple_columns(1, 1)

    with pytest.raises(ValueError, match="is not a locked genuine Dita seed"):
        dita_seed_triple_columns(10, 20)

    # Incomplete basis (wrong column count) returns False
    dummy_cols = [tuple(Cyc24.zero() for _ in range(6)) for _ in range(5)]
    assert verify_triple_pairwise_mu(dummy_cols) is False


def test_tier2_mub6_gramian_dimension_mismatch_boundary():
    """FEAT-MUB-B06: Verify that Gramian verifier rejects non-24x24 matrices."""
    empty_mat: list[list[Cyc24]] = []
    report_empty = verify_gramian_structure(empty_mat)
    assert report_empty.verified_sound is False
    assert report_empty.dimension == 0

    sub_mat = [[Cyc24.one() for _ in range(6)] for _ in range(6)]
    report_sub = verify_gramian_structure(sub_mat)
    assert report_sub.verified_sound is False
    assert report_sub.dimension == 6


# ===========================================================================
# Feature 2: FSP Boundary & Corner Cases (>= 5 tests)
# ===========================================================================

def test_tier2_fsp_lattice_invalid_sites_and_edges():
    """FEAT-FSP-B01: Verify FermionicLattice rejection of non-positive sites and illegal edges."""
    with pytest.raises(ValueError, match="num_sites must be a positive integer"):
        FermionicLattice(num_sites=0, edges=[])

    with pytest.raises(ValueError, match="num_sites must be a positive integer"):
        FermionicLattice(num_sites=-3, edges=[])

    # Self-loops must be rejected
    with pytest.raises(ValueError, match="Self-loops are not permitted"):
        FermionicLattice(num_sites=3, edges=[(1, 1)])

    # Out of range site index
    with pytest.raises(ValueError, match="outside site range"):
        FermionicLattice(num_sites=3, edges=[(0, 3)])


def test_tier2_fsp_fock_state_vacuum_and_negative_masks():
    """FEAT-FSP-B02: Verify FockState particle counting on vacuum and negative bitmask rejection."""
    # Vacuum state (zero particles)
    vacuum = FockState(up_mask=0, down_mask=0)
    assert vacuum.total_particles() == 0
    assert vacuum.count_up() == 0
    assert vacuum.count_down() == 0
    assert vacuum.is_occupied(0, "up") is False

    # Negative mask rejection
    with pytest.raises(ValueError, match="Occupation masks must be non-negative"):
        FockState(up_mask=-1, down_mask=0)

    with pytest.raises(ValueError, match="Occupation masks must be non-negative"):
        FockState(up_mask=0, down_mask=-5)


def test_tier2_fsp_hamiltonian_negative_particles_and_nonfinite_couplings():
    """FEAT-FSP-B03: Verify DiscreteFermionicHamiltonian parameter boundary validation."""
    lat = FermionicLattice.linear_chain(2)

    with pytest.raises(ValueError, match="Fermion counts must be non-negative"):
        DiscreteFermionicHamiltonian(lat, num_up=-1, num_down=0)

    with pytest.raises(ValueError, match="Fermion counts must be non-negative"):
        DiscreteFermionicHamiltonian(lat, num_up=0, num_down=-2)

    with pytest.raises(ValueError, match="Couplings t and u must be finite"):
        DiscreteFermionicHamiltonian(lat, t=float("nan"), u=1)

    with pytest.raises(ValueError, match="Couplings t and u must be finite"):
        DiscreteFermionicHamiltonian(lat, t=1, u=float("inf"))


def test_tier2_fsp_refusal_gates_extreme_values():
    """FEAT-FSP-B04: Verify refusal gates on negative, extreme, and out-of-orbit values."""
    # Fixture gate
    with pytest.raises(ValueError, match="scalar is outside the computed orbit values"):
        fsp_refuse_foreign_fixture(-999)

    with pytest.raises(ValueError, match="scalar is outside the computed orbit values"):
        fsp_refuse_foreign_fixture(1_000_000)

    # Holonomy gate
    with pytest.raises(ValueError, match="claimed product is not the CAR"):
        fsp_refuse_removed_holonomy(-2)

    with pytest.raises(ValueError, match="claimed product is not the CAR"):
        fsp_refuse_removed_holonomy(100)


def test_tier2_fsp_cochain_complex_negative_dimensions_rejection():
    """FEAT-FSP-B05: Verify CochainComplex dimension bounds and matrix size checks."""
    with pytest.raises(ValueError, match="Dimensions must be nonnegative integers"):
        CochainComplex(dim_c0=-1, dim_c1=1, dim_c2=1, d0=[], d1=[])

    # Dimension mismatch between height and declared dim_c1
    with pytest.raises(ValueError, match="d0 dimension mismatch"):
        CochainComplex(dim_c0=1, dim_c1=2, dim_c2=1, d0=[[Fraction(1)]], d1=[[Fraction(0), Fraction(0)]])


# ===========================================================================
# Feature 3: Majorana Boundary & Corner Cases (>= 5 tests)
# ===========================================================================

def test_tier2_majorana_fock_carrier_mode_extremes():
    """FEAT-MAJ-B01: Verify FockCarrier mode limits and rejection outside [1, MAX_MODES]."""
    with pytest.raises(MajoranaError, match="outside 1..="):
        FockCarrier(0)

    with pytest.raises(MajoranaError, match="outside 1..="):
        FockCarrier(-1)

    with pytest.raises(MajoranaError, match="outside 1..="):
        FockCarrier(MAX_MODES + 1)

    # Boundary valid carrier at MAX_MODES
    carrier_max = FockCarrier(MAX_MODES)
    assert carrier_max.modes() == MAX_MODES
    assert carrier_max.dimension() == (1 << MAX_MODES)


def test_tier2_majorana_fock_carrier_generator_index_out_of_bounds():
    """FEAT-MAJ-B02: Verify majorana_generator rejection of indices outside [1, 2*modes]."""
    carrier = FockCarrier(2)  # 2 modes -> 4 Majorana generators {1, 2, 3, 4}

    with pytest.raises(MajoranaError, match="Majorana index .* outside"):
        carrier.majorana_generator(0)

    with pytest.raises(MajoranaError, match="Majorana index .* outside"):
        carrier.majorana_generator(5)


def test_tier2_majorana_monomial_identity_and_involution():
    """FEAT-MAJ-B03: Verify identity monomial behavior and self-annihilation (gamma_i^2 = 1)."""
    m_id = MajoranaMonomial.identity()
    assert m_id.modes == ()

    m2 = MajoranaMonomial.single(2)
    # Identity multiplication: id * m2 = (1, m2)
    sign_left, prod_left = m_id.multiply(m2)
    assert sign_left == Fraction(1)
    assert prod_left == m2

    sign_right, prod_right = m2.multiply(m_id)
    assert sign_right == Fraction(1)
    assert prod_right == m2

    # Self-annihilation: gamma_2 * gamma_2 = 1
    sign_self, prod_self = m2.multiply(m2)
    assert sign_self == Fraction(1)
    assert prod_self == m_id


def test_tier2_majorana_kitaev_wire_zero_hopping_trivial_phase():
    """FEAT-MAJ-B04: Verify SparseKitaevWire in trivial atomic phase (t=0, delta=0, mu=1)."""
    wire = SparseKitaevWire(4, Fraction(0), Fraction(0), Fraction(1))
    iso = wire.isolated_majoranas()
    # In the trivial insulating regime, zero edge modes are isolated
    assert iso == []


def test_tier2_majorana_braid_action_out_of_range_index():
    """FEAT-MAJ-B05: Verify MajoranaBraidAction rejection of out-of-bounds braid indices."""
    with pytest.raises(BraidActionError, match="braid index .* outside"):
        MajoranaBraidAction.elementary(4, 0)

    with pytest.raises(BraidActionError, match="braid index .* outside"):
        MajoranaBraidAction.elementary(4, 4)

    # Minimum mode count is 2
    with pytest.raises(BraidActionError, match="Mode count .* outside"):
        MajoranaBraidAction.elementary(1, 1)


def test_tier2_majorana_tetron_planar_vs_torus_topology():
    """FEAT-MAJ-B06: Verify topology boundaries: Disk (dim_h1=0), Cylinder (dim_h1=1), Torus (dim_h1=2)."""
    _, report_disk = build_tetron_array(2, 2, Topology.Disk)
    assert report_disk.dim_h1 == 0
    assert report_disk.topology == Topology.Disk

    _, report_cyl = build_tetron_array(2, 2, Topology.Cylinder)
    assert report_cyl.dim_h1 == 1
    assert report_cyl.topology == Topology.Cylinder

    _, report_torus = build_tetron_array(2, 2, Topology.Torus)
    assert report_torus.dim_h1 == 2
    assert report_torus.topology == Topology.Torus
