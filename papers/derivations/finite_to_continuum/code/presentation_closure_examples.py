"""Exact finite illustrations for the CS/Q presentation-completion supplement.

These examples call the existing CS-Q and continuum owners. They neither
construct an infinite completion nor certify a physical or authority model.
"""
from __future__ import annotations

import importlib
import json
import sys
from fractions import Fraction
from itertools import product
from pathlib import Path

from sympy import Poly, QQ, cyclotomic_poly, symbols


def _level(value: int) -> int:
    if type(value) is not int:
        raise TypeError("level must be an exact Python integer")
    if not 0 <= value <= 6:
        raise ValueError("finite illustration supports levels 0 through 6")
    return value


def character_average_by_polynomial(level: int, frequency: int) -> Fraction:
    """Actually sum powers in Q[z]/Phi_N(z), independently of the delta rule."""
    order = 1 << _level(level)
    if type(frequency) is not int:
        raise TypeError("frequency must be an exact Python integer")
    z = symbols("z")
    total = Poly(sum(z ** ((frequency * k) % order) for k in range(order)), z, domain=QQ)
    remainder = total.rem(Poly(cyclotomic_poly(order, z), z, domain=QQ))
    if remainder.degree() > 0:
        raise ValueError("full character average did not reduce to a rational")
    scalar = remainder.nth(0) / order
    numerator, denominator = scalar.as_numer_denom()
    return Fraction(int(numerator), int(denominator))


def _csq_owner():
    root = Path(__file__).resolve().parents[3]
    code = root / "omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/docs/source_archive/coda_component_packages/cs_q/code"
    for name in ("cochain_presentation", "coda_cs_q_bridge_core"):
        loaded = sys.modules.get(name)
        if loaded is not None and Path(loaded.__file__).resolve() != code / (name + ".py"):
            raise RuntimeError("CS-Q example encountered a different loaded source owner")
    previous = list(sys.path)
    try:
        sys.path.insert(0, str(code))
        return importlib.import_module("coda_cs_q_bridge_core")
    finally:
        sys.path[:] = previous


def profile_examples() -> dict:
    """Run an image-only factor and a Lipschitz sampling collision in CS-Q."""
    csq = _csq_owner()
    tower = csq.CofinalShadowTower(
        [csq.ShadowNode("first", 1)], {"first": lambda x: x[0]}, {}
    )
    query = csq.QueryProbe("three-times-first", 1, lambda x: 3 * x[0])
    domain = [(-1, 9), (0, 7), (0, 20), (1, 4)]
    success, factor, error = csq.ProfileFactorizationSolver(tower, query, domain).solve_factorization()
    if not success or factor is None:
        raise ValueError(error)
    try:
        factor((2,))
    except KeyError:
        unused_refused = True
    else:
        unused_refused = False

    samples = {"zero": (Fraction(0),) * 4, "tent": (Fraction(0),) * 4}
    integrals = {"zero": Fraction(0), "tent": 4 * Fraction(1, 4) * Fraction(1, 8) / 2}
    sampling = csq.CofinalShadowTower(
        [csq.ShadowNode("grid", 4)], {"grid": samples.__getitem__}, {}
    )
    integral = csq.QueryProbe("piecewise-linear-integral", 1, integrals.__getitem__)
    recovered, _, collision = csq.ProfileFactorizationSolver(
        sampling, integral, ["zero", "tent"]
    ).solve_factorization()
    return {
        "image_factor_values": [factor((-1,)), factor((0,)), factor((1,))],
        "unused_profile_refused": unused_refused,
        "sampling_profiles_equal": samples["zero"] == samples["tent"],
        "sampling_integrals": [str(integrals["zero"]), str(integrals["tent"])],
        "sampling_query_factors": recovered,
        "sampling_collision_reported": collision is not None,
    }


def enclosure_examples() -> dict:
    """Compute actual grid averages and retain the original flag countermodels."""
    from coda_inductive_presentation import ContinuumEnclosure
    from continuous_haar_limit import LipschitzContinuumEnclosure, TrigPolynomial
    from interval_calculus import RationalInterval

    averages = []
    for level in range(5):
        order = 1 << level
        nodes = [Fraction(k, order) for k in range(order)]
        averages.append(sum((min(x, 1 - x) for x in nodes), Fraction(0)) / order)
    positive = LipschitzContinuumEnclosure(1, averages).to_continuum_enclosure("actual-circle-tent")
    integral = Fraction(1, 4)

    raw = [RationalInterval(-1, 1), RationalInterval(Fraction(1, 2), Fraction(3, 2)),
           RationalInterval(Fraction(5, 4), Fraction(7, 4))]
    direct = ContinuumEnclosure("shrinking-without-common-target", raw)
    wrapped = LipschitzContinuumEnclosure(
        1, [Fraction(0), Fraction(1), Fraction(3, 2)]
    ).to_continuum_enclosure("inconsistent-supplied-sums")
    early = TrigPolynomial({4: 1})
    report = early.verify_haar_recovery(max_level=0)
    return {
        "actual_tent_averages": [str(x) for x in averages],
        "actual_tent_integral": str(integral),
        "tent_target_in_every_enclosure": all(iv.lo <= integral <= iv.hi for iv in positive.intervals),
        "tent_finite_contraction_flag": positive.is_cauchy_contractive(),
        "direct_shrinking_flag": direct.is_cauchy_contractive(),
        "direct_intersection_empty": max(iv.lo for iv in raw) > min(iv.hi for iv in raw),
        "accumulated_wrapper_flag": wrapped.is_cauchy_contractive(),
        "early_haar_recovery_flag": report["recovers_exact_haar"],
        "early_observed_average": str(early.discrete_riemann_sum(0)),
        "early_declared_integral": str(early.exact_haar_integral),
        "early_stabilization_level": report["stabilization_level"],
    }


def alternating_character_turns(pairs: int = 5) -> list[dict]:
    """Finite even-level prefixes of the noninteger 2-adic family -1/3."""
    count = _level(pairs)
    if count == 0:
        raise ValueError("at least one prefix is needed")
    rows = []
    for m in range(1, count + 1):
        order = 1 << (2 * m)
        residue = sum(1 << (2 * r) for r in range(m))
        rows.append({"input_turn": str(Fraction(1, order)),
                     "character_turn": str(Fraction(residue, order))})
    return rows


def torus_tent_average(levels: tuple[int, ...]) -> dict:
    """Sample sum_i (i+1)*dist(x_i,Z) on one declared finite product grid."""
    if not 1 <= len(levels) <= 4:
        raise ValueError("finite illustration supports one through four coordinates")
    orders = [1 << _level(level) for level in levels]
    count = 1
    for order in orders:
        count *= order
    if count > 4096:
        raise ValueError("finite illustration allows at most 4096 grid nodes")
    grids = [[Fraction(k, order) for k in range(order)] for order in orders]
    total = sum((sum((i + 1) * min(x, 1 - x) for i, x in enumerate(point))
                 for point in product(*grids)), Fraction(0))
    integral = sum((Fraction(i + 1, 4) for i in range(len(levels))), Fraction(0))
    error_bound = sum((Fraction(i + 1, 2 * order) for i, order in enumerate(orders)), Fraction(0))
    return {"node_count": count, "average": str(total / count),
            "integral": str(integral), "conditional_error_bound": str(error_bound)}


def illustrations() -> dict:
    return {
        "authority_effect": "None",
        "scope": "Exact finite illustrations; the all-level completion arguments are written proofs.",
        "profile_examples": profile_examples(),
        "enclosure_examples": enclosure_examples(),
        "alternating_character_prefixes": alternating_character_turns(),
        "four_coordinate_torus_example": torus_tent_average((1, 1, 1, 1)),
    }


if __name__ == "__main__":
    print(json.dumps(illustrations(), indent=2))
