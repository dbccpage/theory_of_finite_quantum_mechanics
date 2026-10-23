"""Finite controls and manuscript/archive checks for PLAN-WDP-EDITORIAL (E1-E12).

AuthorityEffect: None.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[3]


def check_e1_nonsurjective_factor_and_section(answer_cardinality: int) -> dict[str, int | bool]:
    """E1: q: {0,1} -> {0,1} with q(x)=0 has no section; factor count is |A|^1."""
    if type(answer_cardinality) is not int or answer_cardinality < 1:
        raise ValueError("answer_cardinality must be a positive integer")
    domain = (0, 1)
    presentations = (0, 1)
    q_map = {0: 0, 1: 0}
    answers = tuple(range(answer_cardinality))
    target_d = {0: 0, 1: 0}
    factors = [
        bar_d
        for bar_d in product(answers, repeat=len(presentations))
        if all(bar_d[q_map[x]] == target_d[x] for x in domain)
    ]
    sections = [
        sec
        for sec in product(domain, repeat=len(presentations))
        if all(q_map[sec[p]] == p for p in presentations)
    ]
    return {
        "factor_count": len(factors),
        "unique_factor": len(factors) == 1,
        "section_count": len(sections),
    }


def check_e2_mixed_sign_weights(w1: int, w2: int, x: int = 3) -> dict[str, Fraction | bool]:
    """E2: Evaluate (w1 + w2) * |x + u| over u in [-6, 6] for Dx=(x,x), Au=(u,u)."""
    if type(w1) is not int or type(w2) is not int or type(x) is not int:
        raise ValueError("weights and state must be integers")
    coeff = Fraction(w1 + w2)
    grid = tuple(range(-6, 7))
    values = [coeff * abs(x + u) for u in grid]
    return {
        "net_weight": coeff,
        "min_on_grid": min(values),
        "bounded_below": coeff >= 0,
        "attains_zero_at_minus_x": (coeff * abs(x + (-x))) == 0,
    }


def check_e3_chsh_bit_vs_sign() -> dict[str, tuple[int, ...] | bool]:
    """E3: Compare raw bit expression in {0,1} with sign conversion in {-1,+1}."""
    raw_values = set()
    sign_values = set()
    for a0, a1, b0, b1 in product((0, 1), repeat=4):
        raw_values.add(a0 * (b0 + b1) + a1 * (b0 - b1))
        sa0 = 1 if a0 == 0 else -1
        sa1 = 1 if a1 == 0 else -1
        sb0 = 1 if b0 == 0 else -1
        sb1 = 1 if b1 == 0 else -1
        sign_values.add(sa0 * (sb0 + sb1) + sa1 * (sb0 - sb1))
    return {
        "raw_bit_values": tuple(sorted(raw_values)),
        "sign_values": tuple(sorted(sign_values)),
        "sign_Always_pm2": sign_values == {-2, 2},
        "raw_bits_fail_pm2": raw_values != {-2, 2},
    }


def check_e4_vector_adapter_descent() -> dict[str, tuple[Fraction, Fraction] | bool]:
    """E4: Vector-valued adapter A: C^1 -> W where W is 2D."""
    # v = (1, -1, 1, -1) in B = span(v); W spanned by e1=(1,1,0,0), e2=(0,0,1,0)
    # Orthogonal projection onto e1 and e2 in Q^4:
    v = (Fraction(1), Fraction(-1), Fraction(1), Fraction(-1))
    norm_v_sq = sum(c * c for c in v)

    def proj_b(x: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
        dot = sum(xi * vi for xi, vi in zip(x, v))
        scale = dot / norm_v_sq
        return tuple(scale * vi for vi in v)

    def pi_w(x: tuple[Fraction, ...]) -> tuple[Fraction, Fraction]:
        # Coordinate 0: mean on first two sites; Coordinate 1: value on site 2
        return ((x[0] + x[1]) / 2, x[2])

    raw_on_v = pi_w(v)
    reduced_v = tuple(vi - pbi for vi, pbi in zip(v, proj_b(v)))
    filtered_on_v = pi_w(reduced_v)
    sample_x = (Fraction(2), Fraction(0), Fraction(1), Fraction(1))
    sample_plus_v = tuple(xi + vi for xi, vi in zip(sample_x, v))
    filtered_x = pi_w(tuple(xi - pbi for xi, pbi in zip(sample_x, proj_b(sample_x))))
    filtered_xv = pi_w(
        tuple(xi - pbi for xi, pbi in zip(sample_plus_v, proj_b(sample_plus_v)))
    )
    return {
        "raw_on_b": raw_on_v,
        "filtered_on_b": filtered_on_v,
        "raw_kills_b": raw_on_v == (Fraction(0), Fraction(0)),
        "filtered_kills_b": filtered_on_v == (Fraction(0), Fraction(0)),
        "filtered_well_defined_on_coset": filtered_x == filtered_xv,
    }


def check_e11_switching_probability() -> dict[str, Fraction | bool]:
    """E11: Repeatability switching sum restricts to distinct outcomes j != o."""
    # Two-outcome projective instrument on rho = I/2: tr(K_j K_o rho K_o^* K_j^*)
    # equals 1/2 when j == o and 0 when j != o.
    cross_outcome_sum = Fraction(0)
    unrestricted_sum = Fraction(0)
    for j in (0, 1):
        for o in (0, 1):
            term = Fraction(1, 2) if j == o else Fraction(0)
            unrestricted_sum += term
            if j != o:
                cross_outcome_sum += term
    return {
        "cross_outcome_sum": cross_outcome_sum,
        "unrestricted_sum": unrestricted_sum,
        "repeatability_holds_on_distinct_outcomes": cross_outcome_sum == 0,
    }


def check_manuscript_and_archives(root: Path = PACKAGE_ROOT) -> dict[str, int | bool]:
    """E5-E10, E12: Verify manuscript anchors, Lean count, and archive manifest links."""
    manuscript_path = root / "witnessed_difference_programme.md"
    if not manuscript_path.is_file():
        raise ValueError("missing witnessed_difference_programme.md")
    text = manuscript_path.read_text(encoding="utf-8")
    idx_10_8 = text.index("### 10.8 Question-preserving encodings")
    idx_ch11_anchor = text.index('<a id="chapter-11"></a>')
    idx_ch11_heading = text.index("## Chapter 11 — Intersubjective presentation")
    lean_files = list((root / "lean4").rglob("*.lean"))
    wd_lean_files = list((root / "lean4" / "WitnessedDifference").glob("*.lean"))
    s_manifest = root / "docs/source_archive/appendix_s_review/source_manifest.json"
    loc_manifest = root / "docs/source_archive/locality_and_smearing/source_manifest.json"
    return {
        "lean_total": len(lean_files),
        "lean_submodule_total": len(wd_lean_files),
        "chapter_11_anchor_ordered": idx_10_8 < idx_ch11_anchor < idx_ch11_heading,
        "no_duplicate_ordered_pair": "proper subset, or an ordered pair is" not in text,
        "pauli_quotient_named": "logical Pauli/error class quotient" in text,
        "distinct_outcomes_j_ne_o_named": "distinct outcomes $j\\ne o$" in text,
        "no_bare_directory_links": (
            "](docs/source_archive/appendix_s_review/)" not in text
            and "](docs/source_archive/locality_and_smearing/)" not in text
        ),
        "archive_manifests_exist": s_manifest.is_file() and loc_manifest.is_file(),
    }


def witness() -> dict[str, object]:
    e1_two = check_e1_nonsurjective_factor_and_section(2)
    e1_singleton = check_e1_nonsurjective_factor_and_section(1)
    e2_bounded = check_e2_mixed_sign_weights(-1, 2)
    e2_unbounded = check_e2_mixed_sign_weights(-2, 1)
    e3 = check_e3_chsh_bit_vs_sign()
    e4 = check_e4_vector_adapter_descent()
    e11 = check_e11_switching_probability()
    doc = check_manuscript_and_archives()
    if (
        e1_two["factor_count"] != 2
        or not e1_singleton["unique_factor"]
        or e1_singleton["section_count"] != 0
        or not e2_bounded["bounded_below"]
        or e2_unbounded["bounded_below"]
        or not e3["sign_Always_pm2"]
        or not e3["raw_bits_fail_pm2"]
        or e4["raw_kills_b"]
        or not e4["filtered_kills_b"]
        or not e4["filtered_well_defined_on_coset"]
        or not e11["repeatability_holds_on_distinct_outcomes"]
        or not doc["chapter_11_anchor_ordered"]
        or not doc["no_bare_directory_links"]
        or not doc["archive_manifests_exist"]
    ):
        raise RuntimeError("PLAN-WDP-EDITORIAL control invariant failed")
    return {
        "e1_two_target_factors": e1_two["factor_count"],
        "e1_singleton_factors": e1_singleton["factor_count"],
        "e1_sections": e1_singleton["section_count"],
        "e2_bounded_min": e2_bounded["min_on_grid"],
        "e2_unbounded_min": e2_unbounded["min_on_grid"],
        "e3_sign_values": e3["sign_values"],
        "e3_raw_bit_values": e3["raw_bit_values"],
        "e4_raw_on_b": e4["raw_on_b"],
        "e4_filtered_on_b": e4["filtered_on_b"],
        "e11_cross_outcome_sum": e11["cross_outcome_sum"],
        "e11_unrestricted_sum": e11["unrestricted_sum"],
        "lean_total": doc["lean_total"],
        "lean_submodule_total": doc["lean_submodule_total"],
        "chapter_11_anchor_ordered": doc["chapter_11_anchor_ordered"],
        "no_bare_directory_links": doc["no_bare_directory_links"],
    }
