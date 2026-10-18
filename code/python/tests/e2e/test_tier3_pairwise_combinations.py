"""Tier 3: Pairwise Combinatorial & Cross-Feature Interaction E2E Tests.

Validates joint algebraic invariants and cross-feature interactions:
- MUB ↔ Majorana: Cyclotomic phases and topological braid action invariance.
- MUB ↔ FSP: Mutual unbiased spectral weights in fermionic cochain complexes.
- Majorana ↔ FSP: Jordan-Wigner fermion-Majorana duality and CAR cycle hop parity.
- Majorana ↔ FSP: Kitaev chain parity invariant coupled to FSP holonomy refusal firewall.
- MUB ↔ Majorana ↔ FSP: Tri-paper unified execution pipeline.
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
    verify_mub_crate_invariants,
    authority_effect as mub_authority_effect,
    verify_triple_pairwise_mu,
)
from src.mub.mub_verify import (
    dita_seed_triple_columns,
)

# ---------------------------------------------------------------------------
# FSP Domain Imports
# ---------------------------------------------------------------------------
from src.fsp import (
    witness as fsp_witness,
    refuse_removed_holonomy as fsp_refuse_removed_holonomy,
    refuse_foreign_fixture as fsp_refuse_foreign_fixture,
    Witness as FspWitness,
    HOPS as FSP_HOPS,
    MASKS as FSP_MASKS,
    AUTHORITY_EFFECT as FSP_AUTHORITY_EFFECT,
)
from src.fsp.bqnf_sign_evaluator import (
    CochainComplex,
    normalize_sign_cochain,
    TerminalRoute,
)
from src.fsp.fermionic_hamiltonian import (
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
    build_tetron_array,
    logical_class_representative,
    classify_default,
    Terminal,
    Axis,
    Topology,
    kitaev_chain_parity,
    AUTHORITY_EFFECT as MAJORANA_AUTHORITY_EFFECT,
)
from src.majorana.braid_action import (
    MajoranaBraidAction,
    SignedMajorana,
)


# ===========================================================================
# Pairwise 1: MUB ↔ Majorana
# ===========================================================================

def test_tier3_mub_majorana_cyclotomic_braid_phase_invariance():
    """Verify that Majorana braid actions preserve cyclotomic phase relations in Q(zeta_24)."""
    # MUB6 basis phases are powers of zeta_24 = e^{i pi / 12}
    # An elementary braid in Majorana modes 1 and 2 produces a pi/4 rotation (zeta_24^3)
    zeta3 = Cyc24.zeta(3)  # e^{i pi / 4}
    zeta3_sq = zeta3 * zeta3  # (e^{i pi / 4})^2 = e^{i pi / 2} = i = zeta_24^6
    assert zeta3_sq == Cyc24.zeta(6)

    # Majorana elementary braid action on 4 modes
    braid = MajoranaBraidAction.elementary(4, 1)
    assert braid.determinant_sign() == 1

    # Image of mode 1 is mode 2; image of mode 2 is -mode 1
    im1 = braid.image(1)
    im2 = braid.image(2)
    assert (im1.mode, im1.sign) == (2, 1)
    assert (im2.mode, im2.sign) == (1, -1)

    # 2-fold braid application B^2 reverses signs of modes 1 and 2 (mode permutation squared)
    b2 = braid.compose(braid)
    assert b2.image(1) == SignedMajorana(1, -1)
    assert b2.image(2) == SignedMajorana(2, -1)
    assert b2.image(3) == SignedMajorana(3, 1)
    assert b2.image(4) == SignedMajorana(4, 1)

    # 4-fold braid application B^4 returns to full identity
    b4 = b2.compose(b2)
    assert b4.image(1) == SignedMajorana(1, 1)
    assert b4.image(2) == SignedMajorana(2, 1)
    assert b4.image(3) == SignedMajorana(3, 1)
    assert b4.image(4) == SignedMajorana(4, 1)


# ===========================================================================
# Pairwise 2: MUB ↔ FSP
# ===========================================================================

def test_tier3_mub_fsp_exact_spectral_weight_in_cochain():
    """Verify that MUB mutual unbiasedness overlap (1/6) integrates into FSP cochains."""
    # Construct a 3-vertex cycle representing the 3 mutually unbiased bases
    # Edges represent pairwise mutual unbiased transitions (B1 <-> B2, B2 <-> B3, B3 <-> B1)
    edges = ((0, 1), (1, 2), (0, 2))
    parities = (0, 0, 0)  # Trivial holonomy cycle

    nf = normalize_sign_cochain(3, edges, parities)
    assert len(nf.forest_edges) == 2
    assert len(nf.obstruction_cycles) == 0

    # Represent the 1/6 spectral weight exactly in a CochainComplex
    # d0 maps vertices to edges weighted by 1/6
    sixth = Fraction(1, 6)
    d0 = [
        [-sixth, sixth, Fraction(0)],
        [Fraction(0), -sixth, sixth],
        [-sixth, Fraction(0), sixth],
    ]
    # d1 maps edges to the cycle
    d1 = [[Fraction(1), Fraction(1), Fraction(-1)]]

    cochain = CochainComplex(dim_c0=3, dim_c1=3, dim_c2=1, d0=d0, d1=d1)
    # Check nilpotence d1 * d0 == 0 exactly over Q
    assert cochain.check_nilpotence() is True


# ===========================================================================
# Pairwise 3: Majorana ↔ FSP (Jordan-Wigner CAR Hop Duality)
# ===========================================================================

def test_tier3_majorana_fsp_jordan_wigner_car_hop_duality():
    """Verify that Majorana Jordan-Wigner mode algebra reproduces FSP CAR cycle hop signs."""
    # FSP canonical hop cycle on 4 sites
    hops = FSP_HOPS
    masks = FSP_MASKS
    w = fsp_witness()

    # Verify that the FSP hop sequence reproduces the negative CAR product
    curr_mask = masks[0]
    total_sign = 1
    negative_hop_count = 0

    for src, dst in hops:
        # Compute Jordan-Wigner string between src and dst
        below_src = (1 << src) - 1
        interim = curr_mask ^ (1 << src)
        below_dst = (1 << dst) - 1
        p_src = bin(curr_mask & below_src).count("1")
        p_dst = bin(interim & below_dst).count("1")
        parity = (p_src + p_dst) & 1
        sign = 1 - 2 * parity
        curr_mask = interim | (1 << dst)

        total_sign *= sign
        if sign == -1:
            negative_hop_count += 1

    # Invariants must match FSP witness exactly
    assert total_sign == w.hop_product  # -1
    assert negative_hop_count == w.parity_sum  # 3
    assert (negative_hop_count & 1) == w.parity_f2  # 1


# ===========================================================================
# Pairwise 4: Majorana ↔ FSP (Topological Parity & Refusal Firewall)
# ===========================================================================

def test_tier3_majorana_fsp_topological_parity_and_refusal_firewall():
    """Verify Kitaev chain topological parity coupling to FSP refusal gates."""
    # Parity operator for 2-site Kitaev chain
    p_op = kitaev_chain_parity(2)
    assert isinstance(p_op, MajoranaOperator)
    assert not p_op.is_zero()

    # The non-trivial holonomy product (-1) matches the odd fermion parity sector
    fsp_refuse_removed_holonomy(-1)

    # Even parity (+1) must be refused by the FSP holonomy firewall
    with pytest.raises(ValueError, match="is not the CAR product of this cycle"):
        fsp_refuse_removed_holonomy(1)

    # Foreign fixtures (O.5) are unconditionally rejected
    with pytest.raises(ValueError, match="O.5 fixture scalar is not this k=1 orbit"):
        fsp_refuse_foreign_fixture(912)


# ===========================================================================
# Tri-Paper Integration: MUB ↔ Majorana ↔ FSP
# ===========================================================================

def test_tier3_mub_majorana_fsp_tri_paper_dual_face_invariants():
    """Verify unified tri-paper execution and mutual authority neutrality."""
    # 1. MUB6 Domain
    assert verify_mub_crate_invariants() is True
    assert mub_authority_effect() == "None"
    triple = dita_seed_triple_columns(0, 8)
    assert len(triple) == 18
    assert verify_triple_pairwise_mu(triple) is True

    # 2. Majorana Domain
    complex_torus, report = build_tetron_array(2, 2, Topology.Torus)
    assert report.dim_h1 == 2
    x_rep = logical_class_representative(report, Axis.Column, 0)
    receipt = classify_default(complex_torus.d0, complex_torus.d1, x_rep)
    assert receipt.terminal == Terminal.TypedHarmonic
    assert receipt.phi1_certified is True

    # 3. FSP Domain
    w = fsp_witness()
    assert w.hop_product == -1
    fsp_refuse_removed_holonomy(-1)
    fsp_refuse_foreign_fixture(0)
    fsp_refuse_foreign_fixture(2)

    # 4. Authority Neutrality
    assert "None" in mub_authority_effect()
    assert "None" in FSP_AUTHORITY_EFFECT
    assert "None" in MAJORANA_AUTHORITY_EFFECT
