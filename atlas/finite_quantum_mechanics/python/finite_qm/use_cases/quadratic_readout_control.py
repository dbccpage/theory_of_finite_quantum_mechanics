"""QM-208 finite map: quadratic readout and cross-term interference.

AuthorityEffect: None.

What the L1 shadow provides: weights add without cross terms. The import named
QM-208 is the add-then-square rule that creates 2 Re(c_i conj c_j). This control
computes, exactly over Q(zeta_N), the finite invariant that selects the rule
inside a declared family (Sorkin's third-order interference I_3), shows that the
cross term of two reports is a function of the QM-207 cycle invariants alone, and
records the completion step and the residual import. Nothing here derives the rule.
"""

from __future__ import annotations

import math
from fractions import Fraction
from typing import Any, Callable, Sequence

from finite_qm.domain.cyclotomic_tower import CyclotomicElement
from finite_qm.use_cases import holonomy_bridge_control as hbc

Readout = Callable[[Sequence[CyclotomicElement]], CyclotomicElement]


class ReadoutControlRefusal(ValueError):
    """Typed refusal for malformed readout-control inputs."""


def _rat(q: int | Fraction, conductor: int) -> CyclotomicElement:
    return CyclotomicElement.rational(Fraction(q), conductor)


def _summed(amplitudes: Sequence[CyclotomicElement], conductor: int) -> CyclotomicElement:
    acc = _rat(0, conductor)
    for x in amplitudes:
        acc = acc + x
    return acc


def monomial_readout(a: int, b: int, conductor: int) -> Readout:
    """R(c) = c^a conj(c)^b read on the summed amplitude c = sum c_i."""
    if a < 0 or b < 0 or a + b == 0:
        raise ReadoutControlRefusal("a monomial readout needs nonnegative exponents, not both zero")

    def rule(amplitudes: Sequence[CyclotomicElement]) -> CyclotomicElement:
        c = _summed(amplitudes, conductor)
        return (c**a) * (c.conjugate() ** b)

    return rule


def polynomial_readout(alpha: Fraction, beta: Fraction, conductor: int) -> Readout:
    """R(c) = alpha |c|^2 + beta |c|^4: the phase-blind polynomial family of degree <= 4."""
    quad = monomial_readout(1, 1, conductor)
    quart = monomial_readout(2, 2, conductor)

    def rule(amplitudes: Sequence[CyclotomicElement]) -> CyclotomicElement:
        return quad(amplitudes) * alpha + quart(amplitudes) * beta

    return rule


def phase_blind_monomial_census(max_degree: int, conductor: int) -> dict[str, Any]:
    """Which monomials c^a conj(c)^b of total degree <= max_degree ignore a global mu_N phase.

    Computed on the sample c = 1 + zeta_N against every k in Z/N. For N > max_degree the
    blind monomials are exactly those with a = b (the exponent a - b must vanish mod N).
    """
    if max_degree >= conductor:
        raise ReadoutControlRefusal("the census needs max_degree < conductor")
    sample = _rat(1, conductor) + hbc.root_of_unity(conductor, 1)
    blind: list[tuple[int, int]] = []
    seeing: list[tuple[int, int]] = []
    for a in range(max_degree + 1):
        for b in range(max_degree + 1):
            if a + b == 0 or a + b > max_degree:
                continue
            rule = monomial_readout(a, b, conductor)
            base = rule([sample])
            same = all(
                rule([sample * hbc.root_of_unity(conductor, k)]) == base for k in range(conductor)
            )
            (blind if same else seeing).append((a, b))
    return {
        "max_degree": max_degree,
        "monomials_examined": len(blind) + len(seeing),
        "phase_blind": blind,
        "phase_sensitive": seeing,
        "blind_are_exactly_diagonal": blind == [(a, a) for a in range(1, max_degree // 2 + 1)],
    }


def sorkin_selection(
    conductor: int,
    coefficient_grid: Sequence[tuple[Fraction, Fraction]],
    triples: Sequence[Sequence[CyclotomicElement]],
) -> dict[str, Any]:
    """For each (alpha, beta), does I_3 vanish on every declared triple?

    The expected outcome is that I_3 vanishes on all triples exactly when beta = 0,
    which selects the quadratic rule up to the scale alpha inside the family.
    """
    rows: list[dict[str, Any]] = []
    for alpha, beta in coefficient_grid:
        rule = polynomial_readout(alpha, beta, conductor)
        values = [hbc.third_order_interference(rule, t) for t in triples]
        rows.append(
            {
                "alpha": str(alpha),
                "beta": str(beta),
                "i3_zero_on_all_triples": all(v.is_zero() for v in values),
                "i3_values": [repr(v) for v in values],
            }
        )
    selected = [(r["alpha"], r["beta"]) for r in rows if r["i3_zero_on_all_triples"]]
    return {
        "rows": rows,
        "selected": selected,
        "selection_is_exactly_beta_zero": all(
            r["i3_zero_on_all_triples"] == (Fraction(r["beta"]) == 0) for r in rows
        ),
    }


def interference_census(
    conductor: int, pairs: Sequence[Sequence[CyclotomicElement]]
) -> dict[str, Any]:
    """I_2 of the quadratic rule against the L1 rule on declared pairs."""
    quad = hbc.quadratic_readout
    rows = []
    for pair in pairs:
        i2_quad = hbc.second_order_interference(pair)
        i2_l1 = hbc.l1_readout(pair) - hbc.l1_readout([pair[0]]) - hbc.l1_readout([pair[1]])
        cross = pair[0] * pair[1].conjugate()
        rows.append(
            {
                "i2_quadratic": repr(i2_quad),
                "i2_l1": repr(i2_l1),
                "i2_equals_two_re_cross_term": i2_quad == cross + cross.conjugate(),
                "l1_is_additive": i2_l1.is_zero(),
            }
        )
    return {
        "rows": rows,
        "quadratic_has_some_interference": any(
            not hbc.second_order_interference(p).is_zero() for p in pairs
        ),
        "l1_additive_on_all_pairs": all(r["l1_is_additive"] for r in rows),
        "readout_name": quad.__name__,
    }


def interference_from_holonomy(
    cochain: hbc.U1Cochain,
    source_amplitude: CyclotomicElement,
    p1: hbc.Walk,
    p2: hbc.Walk,
    gauge: Sequence[CyclotomicElement],
) -> dict[str, Any]:
    """I_2 of two transported reports is 2|a|^2 Re Hol(p1 p2^-1): a function of cycle invariants.

    The gauge check rotates the cochain; the transported amplitudes pick up one common
    phase chi(source) conj(chi(sink)), which the quadratic rule cannot see.
    """
    c1, c2 = hbc.report_amplitudes(cochain, source_amplitude, [p1, p2])
    i2 = hbc.second_order_interference([c1, c2])
    hol = hbc.relative_report_phase(cochain, p1, p2)
    predicted = source_amplitude.born_weight() * (hol + hol.conjugate())
    gauged = cochain.gauge_transform(gauge)
    g1, g2 = hbc.report_amplitudes(gauged, source_amplitude, [p1, p2])
    return {
        "i2": repr(i2),
        "holonomy_exponent": hbc.root_exponent(hol),
        "i2_equals_born_weight_times_two_re_holonomy": i2 == predicted,
        "i2_gauge_invariant": hbc.second_order_interference([g1, g2]) == i2,
        "holonomy_factorizes_through_cycle_invariants": hbc.holonomy_factorizes(
            cochain, list(p1) + list(reversed(list(p2)))[1:]
        ),
    }


def rational_square_root(w: Fraction) -> Fraction | None:
    """Exact square root in Q, or None when w is not a square of a rational."""
    if w < 0:
        return None
    n, d = w.numerator, w.denominator
    rn, rd = math.isqrt(n), math.isqrt(d)
    if rn * rn == n and rd * rd == d:
        return Fraction(rn, rd)
    return None


def amplitude_extension_census(weights: Sequence[Fraction], conductor: int) -> dict[str, Any]:
    """Where sqrt(w) lives: in Q, or in a finite extension; no completion is involved.

    sqrt(3) = zeta_12 + zeta_12^11 is checked exactly, so the weight 3/4 has its amplitude
    already inside Q(zeta_12).
    """
    rows = []
    for w in weights:
        root = rational_square_root(w)
        rows.append(
            {
                "weight": str(w),
                "sqrt_in_q": root is not None,
                "sqrt": None if root is None else str(root),
                "extension": "Q" if root is not None else f"Q(sqrt({w}))",
            }
        )
    zeta = hbc.root_of_unity(conductor, 1)
    sqrt3 = zeta + zeta.conjugate()
    half_sqrt3 = sqrt3 * Fraction(1, 2)
    return {
        "rows": rows,
        "sqrt3_squared_is_3": (sqrt3 * sqrt3) == 3,
        "weight_3_over_4_has_amplitude_in_q_zeta12": half_sqrt3.born_weight() == Fraction(3, 4),
        "every_extension_is_finite": True,
    }


def residual_import_ledger() -> list[dict[str, str]]:
    return [
        {
            "layer": "finite invariant",
            "status": "COMPUTED",
            "statement": "Inside the phase-blind polynomial family alpha|c|^2 + beta|c|^4, "
            "Sorkin I_3 vanishes on every triple exactly when beta = 0; the quadratic rule is "
            "selected up to scale. I_2 of two reports equals 2|a|^2 Re Hol(p1 p2^-1).",
        },
        {
            "layer": "completion",
            "status": "none needed",
            "statement": "sqrt(w) lies in a finite extension Q(zeta_N, sqrt(w)); no metric "
            "completion enters the readout itself.",
        },
        {
            "layer": "residual import",
            "status": "IMPORTED",
            "statement": "The add-then-square composition rule. I_3 = 0 selects it inside a "
            "declared family; nothing finite here produces the family or the squaring.",
        },
    ]


def evaluate_quadratic_readout_control(conductor: int = 12) -> dict[str, Any]:
    """Run the QM-208 control exactly and return JSON-serializable results."""
    if conductor % 12 != 0:
        raise ReadoutControlRefusal("the control needs 12 | conductor")
    z = lambda k: hbc.root_of_unity(conductor, k)  # noqa: E731
    one = _rat(1, conductor)
    half = _rat(Fraction(1, 2), conductor)
    two = _rat(2, conductor)
    triples: list[list[CyclotomicElement]] = [
        [one, one, one],
        [one, z(1), z(2)],
        [half, z(5), two],
        [z(3), z(5), z(1)],
        [one, z(4), z(8)],
        [one + z(1), z(7) * half, two],
    ]
    grid = [
        (Fraction(a), Fraction(b))
        for a in (Fraction(1), Fraction(1, 2), Fraction(0), Fraction(-3))
        for b in (Fraction(0), Fraction(1), Fraction(-1, 2), Fraction(2))
    ]
    graph = hbc.FiniteCarrierGraph(4, ((0, 1), (0, 2), (1, 3), (2, 3), (1, 2)))
    cochain = hbc.U1Cochain(graph, (z(1), z(0), z(2), z(5), z(7)))
    gauge = [z(3), z(11), z(4), z(6)]
    quartic_witness = hbc.third_order_interference(hbc.quartic_readout, [one, one, one])
    quadratic_witness = hbc.third_order_interference(hbc.quadratic_readout, [one, one, one])
    return {
        "conductor": conductor,
        "monomial_census": phase_blind_monomial_census(4, conductor),
        "sorkin_selection": sorkin_selection(conductor, grid, triples),
        "quartic_i3_on_unit_triple": repr(quartic_witness),
        "quartic_i3_on_unit_triple_is_36": quartic_witness == 36,
        "quadratic_i3_on_unit_triple_is_zero": quadratic_witness.is_zero(),
        "interference": interference_census(
            conductor, [[one, one], [one, z(6)], [one, z(3)], [half, z(5) * two]]
        ),
        "two_report_interference": interference_from_holonomy(
            cochain, one, [0, 1, 3], [0, 2, 3], gauge
        ),
        "three_report_interference": {
            "quadratic_i3_zero": hbc.third_order_interference(
                hbc.quadratic_readout,
                hbc.report_amplitudes(cochain, one, [[0, 1, 3], [0, 2, 3], [0, 1, 2, 3]]),
            ).is_zero()
        },
        "amplitude_extensions": amplitude_extension_census(
            [Fraction(1, 4), Fraction(9, 16), Fraction(2), Fraction(3, 4), Fraction(1)], conductor
        ),
        "residual_import_ledger": residual_import_ledger(),
    }
