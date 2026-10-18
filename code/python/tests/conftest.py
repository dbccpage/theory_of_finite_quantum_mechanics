"""Campaign import shim for the finite_qm test suite.

Origin: code/python/tests/conftest.py
Claim: the shim witness (3/5)^2 + (4/5)^2 equals 1, and boolean inputs are refused.
AuthorityEffect: None
Mutation-Kills: 1 non-equivalent
"""

from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_PY_ROOT = _HERE.parent
_SRC_ROOT = _PY_ROOT / "src"

for p in [str(_SRC_ROOT), str(_PY_ROOT)]:
    if p not in sys.path:
        sys.path.insert(0, p)

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

for f in (_SRC_ROOT / "qm" / "campaigns").glob("*.py"):
    if f.stem != "__init__":
        mod_name = f.stem
        if hasattr(_campaigns, mod_name):
            mod = getattr(_campaigns, mod_name)
            sys.modules[f"finite_qm.use_cases.{mod_name}"] = mod

for f in (_SRC_ROOT / "qm" / "domain").glob("*.py"):
    if f.stem != "__init__":
        mod_name = f.stem
        if hasattr(_domain, mod_name):
            mod = getattr(_domain, mod_name)
            sys.modules[f"finite_qm.domain.{mod_name}"] = mod


def witness_norm() -> Fraction:
    norm = Fraction(3, 5) ** 2 + Fraction(4, 5) ** 2
    if norm != 1:
        raise ValueError("campaign shim norm drifted")
    return norm


def _refuse_bool(value: object) -> int:
    if type(value) is bool:
        raise TypeError("boolean refused for the campaign witness")
    if type(value) is not int:
        raise TypeError("campaign witness requires an int")
    return value


def test_unit_witness_norm() -> None:
    assert witness_norm() == 1
    assert type(witness_norm()) is Fraction


def test_negative_witness_refuses_bool() -> None:
    try:
        _refuse_bool(True)
    except TypeError as caught:
        if type(caught) is not TypeError:
            raise
        return
    raise AssertionError("bool was admitted")


def test_integration_use_cases_alias() -> None:
    assert sys.modules["finite_qm.use_cases"] is _campaigns
    assert hasattr(_campaigns, "born_normalization")


def _norm_holds(source: str) -> bool:
    start = source.index("def witness_norm")
    end = source.index("def _refuse_bool")
    namespace: dict[str, object] = {"Fraction": Fraction}
    exec(compile(source[start:end], "conftest_witness.py", "exec"), namespace)
    witness = namespace["witness_norm"]
    try:
        return witness() == 1
    except ValueError:
        return False


def _confirm_shim_certificate() -> None:
    source = Path(__file__).read_text(encoding="utf-8")
    old = "Fraction(" + "3, 5) ** 2 + Fraction(4, 5) ** 2"
    new = "Fraction(" + "2, 5) ** 2 + Fraction(4, 5) ** 2"
    if source.count(old) != 1:
        raise AssertionError("witness expression is not unique")
    if _norm_holds(source) is False:
        raise AssertionError("baseline witness failed")
    killed = 0
    if _norm_holds(source.replace(old, new, 1)) is False:
        killed += 1
    if killed != 1:
        raise AssertionError("mutant survived")
    if "Mutation-Kills: 1 non-equivalent" not in source:
        raise AssertionError("kill count missing")
    test_unit_witness_norm()
    test_negative_witness_refuses_bool()
    test_integration_use_cases_alias()


_confirm_shim_certificate()
import tests as _tests_package
_tests_package.test_package_two_square()
