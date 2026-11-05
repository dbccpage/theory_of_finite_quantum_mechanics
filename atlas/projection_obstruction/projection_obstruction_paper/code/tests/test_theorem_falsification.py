"""Adversarial falsification attempts against the paper's PROVED claims.

Added 2026-09-03.  Every other test in this deposit asks "does the code do what
it says".  These tests ask the opposite question: **can a randomised search
find an instance where a theorem the ledger marks PROVED is false?**

Each test draws many pseudo-random instances inside the theorem's stated
hypotheses, evaluates the theorem's own inequality or equality, and fails if
any draw violates it.  Where a theorem has a margin, the worst margin observed
is printed so a counterexample would be legible rather than a bare assertion.

Scope, stated honestly: a passing run is **not** a proof.  These are finite
searches over a finite parameter box in double precision.  They can refute a
theorem; they cannot verify one.  What they do establish is that the Python
surface does not itself exhibit a counterexample to any claim the paper calls
PROVED -- which is the property that would be genuinely embarrassing to lack.

Several tests assert that the search was not vacuous (both branches of an
"iff" occurred, a hypothesis was actually satisfiable, an inequality was
sometimes strict).  A search that only ever exercises the easy case proves
nothing, and silently degenerating into one is the main way a suite like this
rots.

Seeds are fixed so any failure is reproducible.

AuthorityEffect: None.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import pytest

_CODE = str(Path(__file__).resolve().parents[1])
if _CODE not in sys.path:
    sys.path.insert(0, _CODE)

from cochain_presentation import LinearRepairProblem
from exactsym import Matrix, Rational
from observer_carriers import (
    LocalObserverCarrier,
    ObserverFamily,
    scaling_family_certificate,
    three_patch_certificate,
)
from quantum_lattice import (
    FiniteQuantumLattice,
    LocalHamiltonianTerm,
    trace_norm,
)
from replica_hierarchy import (
    FiniteDiagnosticFamily,
    absolute_gauge,
    lp_counterexample_diagnostic,
    scaled_sum_counterexample,
    unweighted_l1_diagnostic,
)
from worked_examples import tfim_normal_rate_example, two_qubit_xx_example

SEED = 20260903
DRAWS = 60


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _paulis() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    x = np.array([[0, 1], [1, 0]], dtype=np.complex128)
    y = np.array([[0, -1.0j], [1.0j, 0]], dtype=np.complex128)
    z = np.array([[1, 0], [0, -1]], dtype=np.complex128)
    return x, y, z


def _pure_density(vec: np.ndarray) -> np.ndarray:
    vec = np.asarray(vec, dtype=np.complex128)
    vec = vec / np.linalg.norm(vec)
    return np.outer(vec, vec.conj()).astype(np.complex128)


def _random_qubit_state(rng: np.random.Generator) -> np.ndarray:
    theta = rng.uniform(0.0, math.pi)
    phi = rng.uniform(0.0, 2.0 * math.pi)
    vec = np.array(
        [math.cos(theta / 2.0),
         complex(math.cos(phi), math.sin(phi)) * math.sin(theta / 2.0)],
        dtype=np.complex128,
    )
    return _pure_density(vec)


def _random_hermitian_2q(rng: np.random.Generator, scale: float) -> np.ndarray:
    x, y, z = _paulis()
    out = np.zeros((4, 4), dtype=np.complex128)
    for a in (x, y, z):
        for b in (x, y, z):
            out = out + rng.normal(0.0, scale) * np.kron(a, b)
    return (out + out.conj().T) / 2.0


def _random_chain(rng: np.random.Generator, n_sites: int, scale: float) -> FiniteQuantumLattice:
    """A random one-/two-local open chain in a random product state."""
    x, _y, z = _paulis()
    sites = tuple(f"q{i}" for i in range(n_sites))
    terms: list[LocalHamiltonianTerm] = []
    for i, site in enumerate(sites):
        terms.append(LocalHamiltonianTerm(
            label=f"field_{i}", support=(site,),
            operator=np.asarray(
                rng.normal(0.0, scale) * x + rng.normal(0.0, scale) * z,
                dtype=np.complex128,
            ),
        ))
    for i in range(n_sites - 1):
        terms.append(LocalHamiltonianTerm(
            label=f"bond_{i}", support=(sites[i], sites[i + 1]),
            operator=_random_hermitian_2q(rng, scale),
        ))
    return FiniteQuantumLattice(
        site_order=sites,
        dimensions={s: 2 for s in sites},
        terms=tuple(terms),
        product_state={s: _random_qubit_state(rng) for s in sites},
    )


def _random_observer_family(rng: np.random.Generator):
    """A random carrier with l1-contractive coordinate-selecting watcher maps.

    Rows of an identity are l1-contractive (every column sums to at most one),
    so the family always satisfies the paper's contractivity hypothesis while
    *what each observer can see* stays random.
    """
    dim = int(rng.integers(2, 4))
    edges = tuple(f"e{i}" for i in range(int(rng.integers(1, 4))))
    edge_dimensions = {e: dim for e in edges}
    observers = []
    for alpha in range(int(rng.integers(1, 4))):
        watched = tuple(e for e in edges if rng.random() < 0.75) or (edges[0],)
        maps = {}
        for e in watched:
            keep = sorted({int(rng.integers(0, dim)) for _ in range(dim)})
            maps[e] = Matrix([[1 if c == k else 0 for c in range(dim)] for k in keep])
        observers.append(LocalObserverCarrier(f"a{alpha}", maps))
    family = ObserverFamily(edge_dimensions, observers)
    defects = {e: tuple(Rational(int(rng.integers(-4, 5))) for _ in range(dim)) for e in edges}
    return family, defects


# ---------------------------------------------------------------------------
# E4 / Theorem 5.1 -- the headline bound
# ---------------------------------------------------------------------------

def test_theorem_5_1_survives_randomised_search_inside_its_window():
    """D_e(t) >= nu_e t - 24 g^2 t^2 on 0 < t <= nu_min/(48 g^2).

    Searched adversarially across the window, including its right-hand edge
    where the quadratic penalty is largest and the bound is tightest.
    """
    rng = np.random.default_rng(SEED)
    worst = math.inf
    worst_at = None
    checked = 0
    for _ in range(DRAWS):
        lattice = _random_chain(rng, int(rng.integers(2, 5)), float(rng.uniform(0.2, 1.5)))
        sites = lattice.site_order
        for i in range(len(sites) - 1):
            edge = (sites[i], sites[i + 1])
            window = lattice.half_slope_window(edge)
            if window <= 0.0:
                continue
            for frac in (0.05, 0.25, 0.5, 0.75, 0.95, 1.0):
                replay = lattice.short_time_bound_replay(edge, window * frac)
                checked += 1
                if replay.numerical_margin < worst:
                    worst = replay.numerical_margin
                    worst_at = (replay.edge, replay.t, replay.nu_e, replay.full_incident_g)
                assert replay.bound_satisfied_with_tolerance, (
                    "Theorem 5.1 VIOLATED: "
                    f"edge={replay.edge} t={replay.t!r} nu_e={replay.nu_e!r} "
                    f"g={replay.full_incident_g!r} D_e={replay.observed_defect!r} "
                    f"rhs={replay.signed_lower_bound_rhs!r} "
                    f"margin={replay.numerical_margin!r}"
                )
    assert checked > 100, f"search was too small to be meaningful: {checked}"
    print(f"\n  Theorem 5.1: {checked} draws, worst margin {worst:.3e} at {worst_at}")


def test_theorem_5_1_rhs_is_reported_signed_not_clipped():
    """Outside the window the RHS must be allowed to go negative.

    A clipped RHS makes the inequality trivially true and voids the theorem's
    content.  This asserts the deposit does not do that.
    """
    rng = np.random.default_rng(SEED + 1)
    lattice = _random_chain(rng, 3, 1.0)
    edge = (lattice.site_order[0], lattice.site_order[1])
    window = lattice.half_slope_window(edge)
    assert window > 0.0
    far = lattice.short_time_bound_replay(edge, window * 40.0)
    assert far.signed_lower_bound_rhs < 0.0, (
        "the signed RHS never went negative far outside the window; "
        "it may be clipped at zero, which would void the theorem's content"
    )


def test_defect_vanishes_at_time_zero():
    """D_e(0) = 0: at t=0 the evolved state is the product state itself."""
    rng = np.random.default_rng(SEED + 2)
    for _ in range(10):
        lattice = _random_chain(rng, int(rng.integers(2, 4)), 1.0)
        edge = (lattice.site_order[0], lattice.site_order[1])
        assert lattice.edge_evolution_replay(edge, 0.0).defect == pytest.approx(0.0, abs=1e-12)


# ---------------------------------------------------------------------------
# F1 / F2 / F3 -- the worked values
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("num_sites", [2, 3, 4, 5])
@pytest.mark.parametrize("coupling", [0.25, 1.0, 2.5, -1.0])
@pytest.mark.parametrize("field", [0.0, 0.5, 2.0])
def test_f2_tfim_normal_rate_is_exactly_two_abs_j(num_sites, coupling, field):
    """F2: nu_e = 2|J| on every bond, independent of the transverse field."""
    replay = tfim_normal_rate_example(num_sites=num_sites, coupling=coupling, field=field)
    assert replay.expected_rate == pytest.approx(2.0 * abs(coupling))
    assert replay.maximum_rate_error < 1e-9, (
        f"F2 VIOLATED: max |nu_e - 2|J|| = {replay.maximum_rate_error!r}"
    )
    for edge, rate in replay.edge_rates:
        assert rate == pytest.approx(2.0 * abs(coupling), abs=1e-9), f"edge {edge}"


@pytest.mark.parametrize("coupling", [0.5, 1.0, 3.0])
@pytest.mark.parametrize("field", [0.0, 1.0, 4.0])
def test_f3_incident_norm_respects_paper_bound(coupling, field):
    """F3: g <= 2|J| + |h|."""
    replay = tfim_normal_rate_example(num_sites=4, coupling=coupling, field=field)
    assert replay.g_within_paper_bound, (
        f"F3 VIOLATED: g={replay.full_incident_g!r} > 2|J|+|h|={replay.paper_g_upper_bound!r}"
    )


def test_f1_two_qubit_xx_matches_the_closed_form():
    """F1: the exact raw defect 1/sqrt(2) + 1/4 at t = pi/(8|J|)."""
    replay = two_qubit_xx_example()
    expected = 1.0 / math.sqrt(2.0) + 0.25
    assert replay.observed_defect == pytest.approx(expected, abs=1e-12), (
        f"F1 VIOLATED: observed {replay.observed_defect!r} vs closed form {expected!r}"
    )


def test_zero_coupling_gives_zero_normal_rate():
    """Degenerate but meaningful: J=0 must give nu_e=0, not numerical noise."""
    replay = tfim_normal_rate_example(num_sites=3, coupling=0.0, field=1.0)
    for _edge, rate in replay.edge_rates:
        assert rate == pytest.approx(0.0, abs=1e-12)
    assert replay.all_edges_active is False


# ---------------------------------------------------------------------------
# H3 / H4 / H5 / H6 / H7 -- the observer-visibility propositions
# ---------------------------------------------------------------------------

def test_h3_observers_are_passive_under_random_carriers():
    """H3 / Prop 7.4.3: every observed tally J^alpha(s) <= raw tally I(s)."""
    rng = np.random.default_rng(SEED + 3)
    checked = 0
    for _ in range(150):
        family, defects = _random_observer_family(rng)
        tallies = family.tallies(defects)
        for alpha, watched in tallies.J.items():
            checked += 1
            assert watched <= tallies.I, (
                f"H3 VIOLATED: observer {alpha} watched {watched} > raw {tallies.I}"
            )
        assert tallies.Lambda >= 0, f"H3 VIOLATED: negative visibility gap {tallies.Lambda}"
    assert checked > 100
    print(f"\n  H3: {checked} observer/instance pairs, no passivity violation")


def test_h4_all_green_iff_every_defect_lies_in_the_joint_kernel():
    """H4 / Prop 7.4.4: All-Green holds exactly when each defect is in ker Q_e."""
    rng = np.random.default_rng(SEED + 4)
    saw_green = saw_red = 0
    for _ in range(200):
        family, defects = _random_observer_family(rng)
        cert = family.all_green_kernel_certificate(defects)
        assert cert.equivalent is True, (
            "H4 VIOLATED: All-Green and joint-kernel membership disagreed; "
            f"all_green={cert.all_green} "
            f"membership={cert.edgewise_joint_kernel_membership}"
        )
        saw_green += bool(cert.all_green)
        saw_red += bool(not cert.all_green)
    assert saw_green > 0 and saw_red > 0, (
        f"search degenerate: green={saw_green} red={saw_red}; both cases must occur"
    )
    print(f"\n  H4: {saw_green} All-Green and {saw_red} non-All-Green instances agreed")


def _injective_family(rng: np.random.Generator, *, force_all_green: bool):
    """A family whose watchers are jointly injective on every edge, by construction.

    Purely random families almost never satisfy H7's hypotheses at once -- an
    earlier version of this test exercised exactly one instance in 400 draws,
    which is indistinguishable from testing nothing.  Here the hypotheses are
    built in and only the *conclusion* is left to check, with the search
    covering both All-Green and non-All-Green sections.
    """
    dim = int(rng.integers(2, 4))
    edges = tuple(f"e{i}" for i in range(int(rng.integers(1, 4))))
    edge_dimensions = {e: dim for e in edges}
    # One observer carrying the full identity on every edge: full coverage and
    # a trivial joint kernel on each edge.
    identity = {e: Matrix([[1 if r == c else 0 for c in range(dim)] for r in range(dim)])
                for e in edges}
    observers = [LocalObserverCarrier("full", identity)]
    # Extra partial watchers may be present; they cannot enlarge a kernel.
    for alpha in range(int(rng.integers(0, 3))):
        watched = tuple(e for e in edges if rng.random() < 0.6)
        if watched:
            maps = {e: Matrix([[1 if c == 0 else 0 for c in range(dim)]]) for e in watched}
            observers.append(LocalObserverCarrier(f"p{alpha}", maps))
    family = ObserverFamily(edge_dimensions, observers)
    if force_all_green:
        defects = {e: tuple(Rational(0) for _ in range(dim)) for e in edges}
    else:
        defects = {e: tuple(Rational(int(rng.integers(-4, 5))) for _ in range(dim))
                   for e in edges}
    return family, defects


def test_h7_joint_injectivity_forces_global_green():
    """H7 / Cor 7.4.7: full coverage + trivial joint kernels + All-Green => I = 0."""
    rng = np.random.default_rng(SEED + 5)
    exercised = 0
    saw_non_green = 0
    for index in range(300):
        family, defects = _injective_family(rng, force_all_green=(index % 2 == 0))
        assert family.full_edge_coverage, "constructed family should have full coverage"
        assert all(family.jointly_injective(e) for e in family.edge_dimensions), (
            "constructed family should be jointly injective on every edge"
        )
        tallies = family.tallies(defects)
        if any(v != 0 for v in tallies.J.values()):
            saw_non_green += 1
            continue  # hypothesis not met; H7 says nothing here
        exercised += 1
        assert tallies.I == 0, (
            f"H7 VIOLATED: full coverage, injective watchers, All-Green, but I={tallies.I}"
        )
    assert exercised >= 100, (
        f"H7's hypotheses were met only {exercised} times; the search is too weak"
    )
    assert saw_non_green > 0, (
        "no non-All-Green section occurred, so the All-Green filter was never load-bearing"
    )
    print(f"\n  H7: {exercised} instances met the hypotheses and all forced I=0; "
          f"{saw_non_green} non-All-Green sections were correctly excluded")


def test_h7_hypotheses_are_necessary_not_decorative():
    """Drop joint injectivity and the conclusion must become refutable.

    H8 settles this negatively in general, but the three-patch witness is the
    concrete case: full coverage and All-Green with I(s) = 6 > 0, which is only
    possible because the joint kernels are nontrivial.
    """
    cert = three_patch_certificate()
    assert cert.full_edge_coverage is True
    assert cert.all_green_kernel.all_green is True
    assert cert.tallies.I == 6
    family = cert.family
    assert not all(family.jointly_injective(e) for e in family.edge_dimensions), (
        "the three-patch family must NOT be jointly injective, or it would "
        "contradict H7 rather than illustrate why H7 needs that hypothesis"
    )


def test_h5_three_patch_is_all_green_with_positive_raw_tally():
    """H5 / Prop 7.4.5: full coverage, All-Green, and I(s)=6 simultaneously."""
    cert = three_patch_certificate()
    assert cert.full_edge_coverage is True
    assert cert.all_green_kernel.all_green is True
    assert cert.tallies.I == 6, f"H5 VIOLATED: raw tally {cert.tallies.I} != 6"
    assert all(v == 0 for v in cert.tallies.J.values()), "H5 VIOLATED: an observer saw the defect"
    assert cert.raw_formula_holds is True


def test_h6_scaling_gives_unbounded_invisible_gap():
    """H6 / Cor 7.4.6: I(s_lambda) = 6|lambda| while every tally stays zero."""
    scales = [1, 2, 3, 7, 100]
    cert = scaling_family_certificate(scales)
    assert cert.exact_linear_scaling is True, "H6 VIOLATED: scaling was not exactly linear"
    for scale, instance in zip(scales, cert.instances):
        assert instance.tallies.I == 6 * abs(scale), (
            f"H6 VIOLATED at lambda={scale}: I={instance.tallies.I} != {6 * abs(scale)}"
        )
        assert all(v == 0 for v in instance.tallies.J.values()), (
            f"H6 VIOLATED: an observer saw a nonzero tally at lambda={scale}"
        )


# ---------------------------------------------------------------------------
# D8 / G1 -- raw tally I versus quotient obstruction Phi
# ---------------------------------------------------------------------------

def test_d8_quotient_obstruction_never_exceeds_the_raw_tally():
    """Phi = inf_alpha ||omega - d0 alpha||_1 <= ||omega||_1 = I, taking alpha = 0.

    D8 turns on I and Phi being distinct.  This is the direction that must
    always hold; a violation would mean the repair infimum is taken over the
    wrong set.  A strict drop must also occur, or the search never exercised a
    repairable cochain.
    """
    rng = np.random.default_rng(SEED + 6)
    strict = 0
    for _ in range(80):
        rows = int(rng.integers(2, 5))
        cols = int(rng.integers(1, 4))
        d0 = Matrix([[Rational(int(rng.integers(-3, 4))) for _ in range(cols)]
                     for _ in range(rows)])
        omega = Matrix([[Rational(int(rng.integers(-5, 6)))] for _ in range(rows)])
        cert = LinearRepairProblem(d0).quotient_l1_distance(omega)
        raw = sum(abs(omega[r, 0]) for r in range(rows))
        assert cert.distance <= raw, f"D8 VIOLATED: Phi={cert.distance} > I={raw}"
        assert cert.distance >= 0, f"D8 VIOLATED: negative quotient distance {cert.distance}"
        strict += bool(cert.distance < raw)
    assert strict > 0, "Phi never fell strictly below I; the search was degenerate"
    print(f"\n  D8: Phi <= I held on 80 draws, strictly on {strict}")


def test_d8_exact_cochain_has_zero_obstruction():
    """If omega = d0 alpha exactly then Phi is exactly zero, not merely small."""
    d0 = Matrix([[Rational(1)], [Rational(-1)], [Rational(2)]])
    omega = d0 * Matrix([[Rational(3)]])
    cert = LinearRepairProblem(d0).quotient_l1_distance(omega)
    assert cert.distance == 0, f"exact cochain had nonzero obstruction {cert.distance}"


# ---------------------------------------------------------------------------
# D6 -- the replica-axiom countermodels
# ---------------------------------------------------------------------------

def _audit(diagnostic):
    family = FiniteDiagnosticFamily(
        edges=["e1", "e2"],
        gauges={"e1": absolute_gauge, "e2": absolute_gauge},
        diagnostic=diagnostic,
    )
    return family.audit(samples={"e1": [(Rational(1),)], "e2": [(Rational(1),)]})


def test_d6_dropping_re3_admits_a_nonadditive_diagnostic():
    """D6: the l^p countermodel really fails RE3, so the axiom bites."""
    audit = _audit(lp_counterexample_diagnostic)
    assert audit.re3_disjoint_replica_additivity is False, (
        "D6 VIOLATED: the RE3-drop countermodel satisfied RE3 after all"
    )


def test_d6_control_l1_diagnostic_satisfies_the_axioms_it_should():
    """The control: the honest l1 diagnostic passes what the countermodel fails."""
    audit = _audit(unweighted_l1_diagnostic)
    assert audit.re3_disjoint_replica_additivity is True
    assert audit.re5_singleton_calibration is True


@pytest.mark.parametrize("scale", ["2", "3", "1/2"])
def test_d6_dropping_re5_breaks_singleton_calibration(scale):
    """D6: the scaled-sum countermodel stays additive but loses unit calibration."""
    audit = _audit(scaled_sum_counterexample(Rational(scale)))
    assert audit.re3_disjoint_replica_additivity is True, (
        f"D6 VIOLATED: the RE5-drop countermodel lost additivity at scale {scale}"
    )
    assert audit.re5_singleton_calibration is False, (
        f"D6 VIOLATED: the RE5-drop countermodel stayed calibrated at scale {scale}"
    )


# ---------------------------------------------------------------------------
# structural invariants no claim may violate
# ---------------------------------------------------------------------------

def test_trace_norm_is_a_norm_on_random_hermitians():
    """Triangle inequality, absolute homogeneity, non-negativity."""
    rng = np.random.default_rng(SEED + 7)
    for _ in range(60):
        a = _random_hermitian_2q(rng, 1.0)
        b = _random_hermitian_2q(rng, 1.0)
        c = float(rng.normal(0.0, 2.0))
        assert trace_norm(a + b) <= trace_norm(a) + trace_norm(b) + 1e-9
        assert trace_norm(c * a) == pytest.approx(abs(c) * trace_norm(a), rel=1e-9)
        assert trace_norm(a) >= -1e-12


def test_normal_rate_decomposition_is_exact():
    """L_e = P_e L_e + n_e must hold to machine precision, or nu_e is meaningless."""
    rng = np.random.default_rng(SEED + 8)
    for _ in range(30):
        lattice = _random_chain(rng, int(rng.integers(2, 5)), 1.0)
        edge = (lattice.site_order[0], lattice.site_order[1])
        replay = lattice.normal_rate_replay(edge)
        assert replay.decomposition_error < 1e-10, (
            f"decomposition L_e = P_e L_e + n_e failed: {replay.decomposition_error!r}"
        )
        assert replay.l_e_trace_error < 1e-10, (
            f"L_e is not traceless: {replay.l_e_trace_error!r}"
        )
