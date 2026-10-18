"""Campaigns of the finite quantum mechanics programme."""

from . import advanced_targets
from . import atomic_dirac
from . import audit_map
from . import axiom_selection
from . import boost_composition
from . import born_gleason
from . import born_normalization
from . import bound_spectra
from . import branch_finegraining
from . import buildability
from . import busch_effects
from . import cancellations
from . import carrier
from . import causal_order
from . import channel_census
from . import clock_tower_control
from . import cochain
from . import commuting_obs
from . import composite_mub
from . import context_barrier
from . import context_parity
from . import context_thresholds
from . import contextuality_f2
from . import continuum
from . import continuum_lift
from . import cptp_channel
from . import density_matrix
from . import derivation_closure
from . import discrete_dynamics
from . import discrete_walk
from . import dressed_qed
from . import dynamics
from . import dynamics_dichotomy
from . import electroweak_dfm
from . import embedding_relativity
from . import engine_bridge
from . import everett
from . import everett_tree
from . import expressibility
from . import finite_geometry_host
from . import finite_qm_engine
from . import foundational_targets
from . import foundations
from . import four_wall_operad
from . import frame_function
from . import gleason
from . import gleason_cyclotomic
from . import growth_refinement
from . import heisenberg_unique
from . import higher_dim
from . import higher_entangle
from . import holonomy_bridge
from . import import_bundle
from . import interference
from . import lattice_gauge
from . import locality_limit
from . import lorentz_boost
from . import matrix_recovery
from . import mermin_peres
from . import mub_reports
from . import no_signalling
from . import nonabelian_dfm
from . import norm_frontier
from . import operational_closure
from . import page_wootters
from . import pauli_spin_stat
from . import phase_fiber
from . import qcd_confinement
from . import qed_hadronic
from . import quadratic_readout
from . import quantum_correlation
from . import quantum_protocols
from . import quantum_walk
from . import refinement_tower
from . import regge_gravity
from . import residual_density
from . import rotation_groups
from . import rungs
from . import sector_conditioning
from . import separating_preds
from . import simplicial_qm
from . import spectral_claims
from . import stabilizer_codes
from . import stinespring
from . import symanzik_two_forest
from . import tensor_correlation
from . import terminal_price_list
from . import toric
from . import tower
from . import tower_completion
from . import vacuum_polarization
from . import ward_takahashi
from . import weyl_ccr_residual


def campaign_pauli_anticommutator():
    """(0, 1) entry of XZ for the integer Pauli matrices. XZ + ZX is the zero matrix."""
    from fractions import Fraction

    pauli_x = ((0, 1), (1, 0))
    pauli_z = ((1, 0), (0, -1))

    def mul(left, right):
        return tuple(
            tuple(sum(left[i][k] * right[k][j] for k in range(2)) for j in range(2))
            for i in range(2)
        )

    xz = mul(pauli_x, pauli_z)
    zx = mul(pauli_z, pauli_x)
    defect = sum(abs(xz[i][j] + zx[i][j]) for i in range(2) for j in range(2))
    if defect != 0:
        raise ValueError(f"Pauli anticommutator defect is {defect}")
    return Fraction(xz[0][1])
