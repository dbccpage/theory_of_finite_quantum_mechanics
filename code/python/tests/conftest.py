"""Pytest configuration, fixtures, and source compatibility shims for Finite QM test suite."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Callable, Dict, List
import importlib
import types

import numpy as np
import pytest

# Ensure code/python and code/python/src are on sys.path
_HERE = Path(__file__).resolve().parent
_PY_ROOT = _HERE.parent
_SRC_ROOT = _PY_ROOT / "src"

for p in [str(_SRC_ROOT), str(_PY_ROOT)]:
    if p not in sys.path:
        sys.path.insert(0, p)

# Install compatibility shims for legacy package names
import src.qm as _qm
import src.qm.domain as _domain
import src.qm.campaigns as _campaigns
import src.qm.entrypoints as _entrypoints
import src.qm.data as _data
import src.linear_algebra as _la

sys.modules["finite_qm"] = _qm
sys.modules["finite_qm.domain"] = _domain
sys.modules["finite_qm.campaigns"] = _campaigns
sys.modules["finite_qm.use_cases"] = _campaigns
sys.modules["finite_qm.entrypoints"] = _entrypoints
sys.modules["finite_qm.data"] = _data
if hasattr(_qm, "api"):
    sys.modules["finite_qm.api"] = _qm.api
if hasattr(_qm, "cli"):
    sys.modules["finite_qm.cli"] = _qm.cli
if hasattr(_qm, "evidence"):
    sys.modules["finite_qm.evidence"] = _qm.evidence
sys.modules["oracles"] = _la
if hasattr(_campaigns, "no_signalling"):
    sys.modules["no_signalling"] = _campaigns.no_signalling


# Map legacy campaign names to new module names in sys.modules
_CAMPAIGN_MAP = {
    "algebraic_bound_state_spectra_control": "bound_spectra",
    "atomic_dirac_lamb_hartree_fock_control": "atomic_dirac",
    "buildability_criterion": "buildability",
    "cancellation_certificates": "cancellations",
    "commuting_observables": "commuting_obs",
    "composition_tensor_mub": "composite_mub",
    "context_parity_control": "context_parity",
    "contextuality_obstruction": "context_barrier",
    "contextuality_thresholds": "context_thresholds",
    "continuous_time_locality_limit": "locality_limit",
    "cptp_channels_stinespring": "stinespring",
    "dirac_ward_takahashi_control": "ward_takahashi",
    "discrete_walk_engines": "discrete_walk",
    "dressed_qed_g2_control": "dressed_qed",
    "electroweak_dfm_weinberg_control": "electroweak_dfm",
    "finite_operational_closure_contract": "operational_closure",
    "finite_qm_expressibility_and_measurement_control": "expressibility",
    "foundational_derivation_closure_control": "derivation_closure",
    "four_wall_reconstruction_and_operad_control": "four_wall_operad",
    "frame_function_control": "frame_function",
    "heisenberg_representation_uniqueness": "heisenberg_unique",
    "higher_dim_entanglement": "higher_entangle",
    "holonomy_bridge_control": "holonomy_bridge",
    "lattice_gauge_manybody_benchmark": "lattice_gauge",
    "nonabelian_dfm_control": "nonabelian_dfm",
    "norm_approximation_frontier": "norm_frontier",
    "operational_axiom_selection": "axiom_selection",
    "page_wootters_tsirelson_wigner_control": "page_wootters",
    "pauli_spin_statistics_graph_control": "pauli_spin_stat",
    "qcd_beta0_wilson_confinement_control": "qcd_confinement",
    "qed_weak_hadronic_control": "qed_hadronic",
    "quadratic_readout_control": "quadratic_readout",
    "refinement_subsystem_tower": "refinement_tower",
    "regge_gravity_ghz_chern_control": "regge_gravity",
    "residual_density_calculus": "residual_density",
    "sealed_finite_matrix_recovery": "matrix_recovery",
    "separating_predictions": "separating_preds",
    "simplicial_complex_qm": "simplicial_qm",
    "symanzik_two_forest_bphz_control": "symanzik_two_forest",
    "tensor_commuting_correlation_frontier": "tensor_correlation",
    "tower_topological_completion": "tower_completion",
    "vacuum_polarization_lamb_shift_control": "vacuum_polarization",
}

for old, new in _CAMPAIGN_MAP.items():
    if hasattr(_campaigns, new):
        mod = getattr(_campaigns, new)
        setattr(_campaigns, old, mod)
        sys.modules[f"finite_qm.use_cases.{old}"] = mod
        sys.modules[f"src.qm.campaigns.{old}"] = mod

# Also map any module directly in src.qm.campaigns
for f in (_SRC_ROOT / "qm" / "campaigns").glob("*.py"):
    if f.stem != "__init__":
        mod_name = f.stem
        if hasattr(_campaigns, mod_name):
            mod = getattr(_campaigns, mod_name)
            sys.modules[f"finite_qm.use_cases.{mod_name}"] = mod

# Map domain modules
for f in (_SRC_ROOT / "qm" / "domain").glob("*.py"):
    if f.stem != "__init__":
        mod_name = f.stem
        if hasattr(_domain, mod_name):
            mod = getattr(_domain, mod_name)
            sys.modules[f"finite_qm.domain.{mod_name}"] = mod


@pytest.fixture
def qubit_basis_states() -> Dict[str, np.ndarray]:
    """Single-qubit pure state vectors in computational and Hadamard bases."""
    return {
        "0": np.array([1.0, 0.0], dtype=complex),
        "1": np.array([0.0, 1.0], dtype=complex),
        "+": np.array([1.0, 1.0], dtype=complex) / np.sqrt(2.0),
        "-": np.array([1.0, -1.0], dtype=complex) / np.sqrt(2.0),
    }


@pytest.fixture
def bell_states() -> Dict[str, np.ndarray]:
    """Canonical two-qubit Bell states."""
    phi_plus = np.array([1.0, 0.0, 0.0, 1.0], dtype=complex) / np.sqrt(2.0)
    phi_minus = np.array([1.0, 0.0, 0.0, -1.0], dtype=complex) / np.sqrt(2.0)
    psi_plus = np.array([0.0, 1.0, 1.0, 0.0], dtype=complex) / np.sqrt(2.0)
    psi_minus = np.array([0.0, 1.0, -1.0, 0.0], dtype=complex) / np.sqrt(2.0)
    return {
        "phi_plus": phi_plus,
        "phi_minus": phi_minus,
        "psi_plus": psi_plus,
        "psi_minus": psi_minus,
    }


@pytest.fixture
def depolarizing_channel_factory() -> Callable[[float], Callable[[np.ndarray], np.ndarray]]:
    """Factory creating depolarizing channels with noise parameter p."""
    def _create(p: float) -> Callable[[np.ndarray], np.ndarray]:
        def _channel(rho: np.ndarray) -> np.ndarray:
            d = rho.shape[0]
            return (1.0 - p) * rho + p * np.eye(d, dtype=complex) / d
        return _channel
    return _create


@pytest.fixture
def amplitude_damping_channel_factory() -> Callable[[float], List[np.ndarray]]:
    """Factory creating Kraus operators for amplitude damping with parameter gamma."""
    def _create(gamma: float) -> List[np.ndarray]:
        e0 = np.array([[1.0, 0.0], [0.0, np.sqrt(1.0 - gamma)]], dtype=complex)
        e1 = np.array([[0.0, np.sqrt(gamma)], [0.0, 0.0]], dtype=complex)
        return [e0, e1]
    return _create
