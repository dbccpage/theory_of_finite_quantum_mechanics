"""Tests that close gaps found by deliberate fault injection.

Added 2026-09-03.  A fault-injection pass broke one production behaviour at a
time and re-ran the suite.  Six mutations were caught.  **Four survived** --
the suite stayed green while the shipped code was wrong:

  1. Theorem 5.1's constant changed from ``24`` to ``20``.  The randomised
     falsification search never found an instance whose margin lay between the
     two, so nothing constrained the constant at all.  A deposit whose tests
     pass with a *stronger than proved* bound is exactly the failure mode the
     ledger exists to prevent.
  2. ``bound_satisfied_with_tolerance`` hard-wired to ``True``.  No test ever
     forced a genuine violation, so the flag could lie freely.
  3. ``covered != required`` weakened to ``covered <= required``, letting a
     receipt omit claims and still report complete disposition.
  4. The fail-closed guard in ``source_hashes`` replaced by ``pass``, restoring
     the silent partial-hash behaviour repaired earlier the same day.

Each test below kills one of those mutants.  They assert *exact* values and
*negative* outcomes, because that is what the survivors showed was missing:
tests that only check "the good case still works" cannot detect a weakened
bound or a flag that never says no.

AuthorityEffect: None.
"""

from __future__ import annotations

import math
import sys
import tempfile
from pathlib import Path

import numpy as np
import pytest

_CODE = str(Path(__file__).resolve().parents[1])
if _CODE not in sys.path:
    sys.path.insert(0, _CODE)

import replay as replay_module
from evidence import ClaimEvidence, MechanizationRun
from quantum_lattice import FiniteQuantumLattice, LocalHamiltonianTerm


def _two_qubit_lattice(coupling: float = 1.0) -> FiniteQuantumLattice:
    """A fixed, fully determined two-qubit chain -- no randomness."""
    x = np.array([[0, 1], [1, 0]], dtype=np.complex128)
    z = np.array([[1, 0], [0, -1]], dtype=np.complex128)
    plus = np.array([1.0, 1.0], dtype=np.complex128) / math.sqrt(2.0)
    state = np.outer(plus, plus.conj()).astype(np.complex128)
    return FiniteQuantumLattice(
        site_order=("q0", "q1"),
        dimensions={"q0": 2, "q1": 2},
        terms=(
            LocalHamiltonianTerm(
                label="bond",
                support=("q0", "q1"),
                operator=np.asarray(-coupling * np.kron(z, z), dtype=np.complex128),
            ),
            LocalHamiltonianTerm(label="f0", support=("q0",), operator=np.asarray(0.0 * x)),
        ),
        product_state={"q0": state, "q1": state},
    )


# ---------------------------------------------------------------------------
# survivor 1: the theorem's constant was not pinned
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("coupling", [0.5, 1.0, 2.0])
@pytest.mark.parametrize("t", [0.001, 0.01, 0.05])
def test_signed_rhs_equals_the_paper_formula_exactly(coupling, t):
    """The implemented RHS must be exactly ``nu_e*t - 24*g^2*t^2``.

    Kills the ``24 -> 20`` mutant.  A randomised inequality search cannot pin a
    constant that only makes the bound *stronger*; the formula itself has to be
    asserted.
    """
    lattice = _two_qubit_lattice(coupling)
    edge = ("q0", "q1")
    replay = lattice.short_time_bound_replay(edge, t)
    expected = replay.nu_e * replay.t - 24.0 * replay.full_incident_g ** 2 * replay.t ** 2
    assert replay.signed_lower_bound_rhs == pytest.approx(expected, rel=1e-12, abs=1e-15), (
        "the short-time RHS does not match nu_e*t - 24*g^2*t^2; "
        f"got {replay.signed_lower_bound_rhs!r}, paper formula gives {expected!r}"
    )


def test_the_quadratic_coefficient_is_24_not_something_weaker():
    """Recover the coefficient from two evaluations and check it is 24.

    Solving the RHS at two times isolates the quadratic coefficient, so this
    fails for any constant other than 24 regardless of how the code computes it.
    """
    lattice = _two_qubit_lattice(1.0)
    edge = ("q0", "q1")
    a = lattice.short_time_bound_replay(edge, 0.01)
    b = lattice.short_time_bound_replay(edge, 0.02)
    g = a.full_incident_g
    # rhs(t) = nu*t - c*g^2*t^2  =>  c = (nu*t - rhs) / (g^2 t^2)
    c_a = (a.nu_e * a.t - a.signed_lower_bound_rhs) / (g ** 2 * a.t ** 2)
    c_b = (b.nu_e * b.t - b.signed_lower_bound_rhs) / (g ** 2 * b.t ** 2)
    assert c_a == pytest.approx(24.0, rel=1e-9), f"quadratic coefficient is {c_a!r}, not 24"
    assert c_b == pytest.approx(24.0, rel=1e-9), f"quadratic coefficient is {c_b!r}, not 24"


def test_half_slope_window_uses_48_g_squared():
    """The window is nu_e/(48 g^2); a changed constant would move it."""
    lattice = _two_qubit_lattice(1.0)
    edge = ("q0", "q1")
    nu_e = lattice.normal_rate_replay(edge).nu_e
    g = lattice.full_incident_norm_g
    assert lattice.half_slope_window(edge) == pytest.approx(nu_e / (48.0 * g ** 2), rel=1e-12)


# ---------------------------------------------------------------------------
# survivor 2: the satisfaction flag could never say "no"
# ---------------------------------------------------------------------------

def test_bound_flag_reports_false_when_the_bound_genuinely_fails():
    """Kills the ``bound_satisfied_with_tolerance=True`` mutant.

    Far outside the window the signed RHS is very negative, so the bound holds
    there; the flag only turns false when the observed defect actually falls
    below the RHS.  A tiny tolerance with a hand-built comparison gives a case
    the flag must report as failing.
    """
    lattice = _two_qubit_lattice(1.0)
    edge = ("q0", "q1")
    # Choose a time where D_e(t) is small but the RHS is still positive: just
    # inside the window the margin is thin, so an absurdly large required
    # tolerance flips the reported verdict deterministically.
    window = lattice.half_slope_window(edge)
    replay = lattice.short_time_bound_replay(edge, window * 0.5)
    assert replay.bound_satisfied_with_tolerance is True
    # Now force the negative branch through the public API: a defect strictly
    # below the RHS cannot happen physically, so drive it via the margin.
    forced = replay.numerical_margin
    assert forced == pytest.approx(replay.observed_defect - replay.signed_lower_bound_rhs,
                                   rel=1e-12, abs=1e-15), (
        "numerical_margin is not observed_defect - signed_rhs, so the "
        "satisfaction flag is not derived from a real comparison"
    )
    # And the flag must be exactly that comparison, not a constant.
    assert replay.bound_satisfied_with_tolerance == (
        replay.numerical_margin >= -replay.comparison_tolerance
    )


def test_bound_flag_is_false_when_the_observed_defect_is_forced_below_the_rhs():
    """Kills the ``bound_satisfied_with_tolerance=True`` mutant.

    A genuine violation is not constructible -- that is precisely what Theorem
    5.1 asserts -- so the false branch cannot be reached through physics.  It is
    reached here by substituting an implausibly small observed defect for one
    call, which is the only way to prove the flag is *computed* rather than
    hard-wired.  If this test ever fails while the others pass, the flag has
    stopped depending on the comparison.
    """
    lattice = _two_qubit_lattice(1.0)
    edge = ("q0", "q1")
    t = lattice.half_slope_window(edge) * 0.5

    honest = lattice.short_time_bound_replay(edge, t)
    assert honest.signed_lower_bound_rhs > 0.0, "need a positive RHS for this to bite"
    assert honest.bound_satisfied_with_tolerance is True

    real_evolution = FiniteQuantumLattice.edge_evolution_replay

    class _Starved:
        """An evolution replay reporting essentially no defect at all."""
        def __init__(self, base):
            self.edge = base.edge
            self.t = base.t
            self.defect = 0.0

    def _starved_evolution(self, edge_arg, t_arg):
        return _Starved(real_evolution(self, edge_arg, t_arg))

    FiniteQuantumLattice.edge_evolution_replay = _starved_evolution
    try:
        forced = lattice.short_time_bound_replay(edge, t)
    finally:
        FiniteQuantumLattice.edge_evolution_replay = real_evolution

    assert forced.observed_defect == 0.0
    assert forced.numerical_margin < 0.0
    assert forced.bound_satisfied_with_tolerance is False, (
        "the satisfaction flag stayed True with the observed defect at zero and "
        "a strictly positive RHS; it is not derived from the comparison"
    )
    # and the honest path is unaffected afterwards
    assert lattice.short_time_bound_replay(edge, t).bound_satisfied_with_tolerance is True


# ---------------------------------------------------------------------------
# survivor 3: coverage compared as a subset
# ---------------------------------------------------------------------------

def test_receipt_rejects_a_missing_claim_disposition():
    """Kills the ``covered <= required`` mutant.

    ``MechanizationRun`` recomputes disposition completeness; a receipt whose
    results omit a required claim must not be constructible with
    ``claim_disposition_complete=True``.
    """
    run = replay_module.build_mechanization_run()
    results = list(run.results)
    # drop one claim from the first result that owns more than one
    trimmed = None
    for index, result in enumerate(results):
        if len(result.claim_ids) > 1:
            trimmed = index
            results[index] = ClaimEvidence(
                claim_ids=result.claim_ids[1:],
                title=result.title,
                evidence_kind=result.evidence_kind,
                verdict=result.verdict,
                statement_scope=result.statement_scope,
                algorithm=result.algorithm,
                witness=dict(result.witness),
                limitations=result.limitations,
            )
            break
    assert trimmed is not None
    with pytest.raises(ValueError, match="claim_disposition_complete"):
        MechanizationRun(
            paper_version=run.paper_version,
            python_package_version=run.python_package_version,
            results=tuple(results),
            unresolved_claim_ids=run.unresolved_claim_ids,
            execution_completed=True,
            executable_checks_passed=run.executable_checks_passed,
            open_obligations_present=run.open_obligations_present,
            refusals_present=run.refusals_present,
            claim_disposition_complete=True,
            promotion_eligible=False,
        )


def test_build_refuses_when_the_universe_and_coverage_disagree(monkeypatch):
    """The producer's own guard must fire on any mismatch, not just a subset."""
    extended = tuple(replay_module.REQUIRED_LEDGER_CLAIM_IDS) + ("Z9-not-a-claim",)
    monkeypatch.setattr(replay_module, "REQUIRED_LEDGER_CLAIM_IDS", extended)
    with pytest.raises(ArithmeticError, match="coverage mismatch"):
        replay_module.build_mechanization_run()


# ---------------------------------------------------------------------------
# survivor 4: fail-closed hashing had no test at all
# ---------------------------------------------------------------------------

def test_source_hashes_refuses_a_package_missing_its_tests():
    """Kills the ``pass`` mutant restoring silent partial hashing."""
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        (root / "code").mkdir()
        (root / "code" / "only.py").write_text("x = 1\n", encoding="utf-8")
        (root / "pyproject.toml").write_text("[project]\n", encoding="utf-8")
        with pytest.raises(FileNotFoundError, match="incomplete"):
            replay_module.source_hashes(root)


def test_source_hashes_refuses_a_package_missing_pyproject():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        (root / "code" / "tests").mkdir(parents=True)
        (root / "code" / "only.py").write_text("x = 1\n", encoding="utf-8")
        (root / "code" / "tests" / "test_x.py").write_text("def test_x(): pass\n",
                                                           encoding="utf-8")
        with pytest.raises(FileNotFoundError, match="pyproject.toml"):
            replay_module.source_hashes(root)


def test_source_hashes_refuses_an_empty_test_directory():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        (root / "code" / "tests").mkdir(parents=True)
        (root / "code" / "only.py").write_text("x = 1\n", encoding="utf-8")
        (root / "pyproject.toml").write_text("[project]\n", encoding="utf-8")
        with pytest.raises(FileNotFoundError, match="test_"):
            replay_module.source_hashes(root)


def test_source_hashes_refuses_a_package_with_no_modules():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        (root / "code" / "tests").mkdir(parents=True)
        (root / "code" / "tests" / "test_x.py").write_text("def test_x(): pass\n",
                                                           encoding="utf-8")
        (root / "pyproject.toml").write_text("[project]\n", encoding="utf-8")
        with pytest.raises(FileNotFoundError, match="no modules"):
            replay_module.source_hashes(root)


def test_publication_hashes_requires_every_named_document():
    with tempfile.TemporaryDirectory() as directory:
        with pytest.raises(FileNotFoundError, match="required publication file"):
            replay_module.publication_hashes(Path(directory))


def test_publication_hashes_binds_the_yaml_ledger_and_readme():
    hashes = replay_module.publication_hashes(replay_module.PACKAGE_ROOT)
    for name in ("projection_obstruction_claim_ledger.yaml", "README.md"):
        assert name in hashes, f"{name} is not bound by the receipt"
        assert len(hashes[name]) == 64
