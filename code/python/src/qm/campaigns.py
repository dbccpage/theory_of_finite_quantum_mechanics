"""Campaign package and the integer Pauli anticommutator.

Origin: lean4/CommutingObservables.lean definitions pauliX and pauliZ.
Claim: urn:omega:fqm:qm:pauli-anticommutator-entry:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/src/qm/tests/test_isolated_certificates.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 4; AST nesting depth max 1; lizard 1.24.1 cyclomatic complexity max 5.
Scope Fence: The (0, 1) entry of XZ is -1, and XZ + ZX is the zero matrix.
Importing the campaign modules does not discharge their claims.
"""

from fractions import Fraction
from typing import Mapping

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

_ENTRY = Fraction(-1)
_MARK = 7


class CampaignError(Exception):
    """One violated package invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> CampaignError:
    return CampaignError(invariant, parameters)


def _require_fraction(value: object, role: str) -> Fraction:
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", role=role, received="float")
    if type(value) is bool:
        raise _fail("boolean refused where a rational was required", role=role)
    if isinstance(value, Fraction):
        return value
    if type(value) is int:
        return Fraction(value)
    raise _fail("value is not an exact rational", role=role, received=type(value).__name__)


def _mark() -> int:
    return _MARK


def _entry(left: tuple[tuple[int, int], tuple[int, int]], right: tuple[tuple[int, int], tuple[int, int]], row: int, column: int) -> int:
    return left[row][0] * right[0][column] + left[row][1] * right[1][column]


def _mul(left: tuple[tuple[int, int], tuple[int, int]], right: tuple[tuple[int, int], tuple[int, int]]) -> tuple[tuple[int, int], tuple[int, int]]:
    return ((_entry(left, right, 0, 0), _entry(left, right, 0, 1)), (_entry(left, right, 1, 0), _entry(left, right, 1, 1)))


def _locked(value: Fraction, expected: Fraction, invariant: str) -> Fraction:
    if value != expected:
        raise _fail(invariant, value=str(value), expected=str(expected))
    return value


def campaign_pauli_anticommutator() -> Fraction:
    """(0, 1) entry of XZ. XZ + ZX is checked to be the zero matrix."""
    pauli_x = ((0, 1), (1, 0))
    pauli_z = ((1, 0), (0, -1))
    xz = _mul(pauli_x, pauli_z)
    zx = _mul(pauli_z, pauli_x)
    defect = abs(xz[0][0] + zx[0][0]) + abs(xz[0][1] + zx[0][1]) + abs(xz[1][0] + zx[1][0]) + abs(xz[1][1] + zx[1][1])
    if defect != 0:
        raise _fail("Pauli anticommutator defect is not zero", defect=defect)
    return Fraction(xz[0][1])


def certify(probe: object | None = None) -> Fraction:
    """Refuse a non-rational probe, then return the Pauli entry -1."""
    if probe is not None:
        _require_fraction(probe, "probe")
    if _mark() != 7:
        raise _fail("certificate mark drifted", mark=_mark())
    return _locked(campaign_pauli_anticommutator(), _ENTRY, "Pauli entry drifted")


def main() -> int:
    value = campaign_pauli_anticommutator()
    print(value)
    if value == _ENTRY:
        return 0
    return 1
