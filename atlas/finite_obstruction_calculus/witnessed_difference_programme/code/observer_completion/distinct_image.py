"""Sharp observer completion with distinct realization and repair images.

Finite-dimensional rational matrices. Producers build witnesses. Checkers
replay a submitted witness and do not call a model or replace a bad witness
with a repaired one.

R = im D_s is the realizable defect space.
B = im D_r is the algebraic repair space.
Q : V -> Y is the existing observer.
E : V -> Q^m is an additional row map, and A = (Q, E).

Raw sufficiency means R ∩ ker A = {0}.
Quotient sufficiency means ker A ⊆ B, which is exactly when the induced map
V/B -> (Y ⊕ Q^m)/A(B) is injective.
"""

from __future__ import annotations

from fractions import Fraction as F
from itertools import combinations

from observer_completion.observer_completion import (
    M,
    basis,
    eye,
    extend,
    hc,
    inverse,
    null,
    rank,
    require,
    rational,
    vc,
)

TASK = "sharp-distinct-image-completion"
SOURCE = "witnessed_difference_programme.md#WDP-DIM-1"
FIELD = "rational"


def _positive_rational(value: object) -> bool:
    if isinstance(value, bool) or isinstance(value, float):
        return False
    if type(value) is int or type(value) is F:
        return value > 0
    return False


def _zero_columns(rows: int) -> M:
    return M([[] for _ in range(rows)], 0)


def image_basis(matrix: M) -> M:
    if matrix.c == 0 or matrix.r == 0:
        return _zero_columns(matrix.r)
    return basis(matrix)


def intersection_basis(left: M, right: M) -> M:
    """Column basis of im(left) ∩ im(right)."""
    require(left.r == right.r, "intersection shape")
    if left.c == 0 or right.c == 0:
        return _zero_columns(left.r)
    joint = hc(left, -right)
    coefficients = null(joint)
    if coefficients.c == 0:
        return _zero_columns(left.r)
    return image_basis(left @ coefficients.rows(range(left.c)))


def _same_space(left: M, right: M) -> bool:
    if left.c != right.c:
        return False
    if left.c == 0:
        return True
    return rank(hc(left, right)) == left.c


def _contained(columns: M, space: M) -> bool:
    """True when every column of `columns` lies in the column span of `space`."""
    if columns.c == 0:
        return True
    if space.c == 0:
        return False
    return rank(hc(space, columns)) == space.c


def analyze(source: M, repair: M, observer: M) -> dict:
    """Dimensions of the distinct-image completion problem.

    source is D_s, repair is D_r, observer is Q.
    """
    require(source.r == repair.r == observer.c, "carrier shape")
    realizable = image_basis(source)
    algebraic = image_basis(repair)
    invisible = null(observer)
    raw_space = intersection_basis(realizable, invisible)
    repairable_invisible = intersection_basis(invisible, algebraic)
    shared = intersection_basis(raw_space, algebraic)
    raw_minimum = raw_space.c
    quotient_minimum = invisible.c - repairable_invisible.c
    joint_minimum = quotient_minimum + shared.c
    return {
        "ambient": source.r,
        "R": realizable,
        "B": algebraic,
        "K": invisible,
        "RK": raw_space,
        "KB": repairable_invisible,
        "RKB": shared,
        "raw_minimum": raw_minimum,
        "quotient_minimum": quotient_minimum,
        "joint_minimum": joint_minimum,
        "separate_sum": raw_minimum + quotient_minimum,
        "images_equal": _same_space(realizable, algebraic),
    }


def _complement_in(subspace: M, ambient_space: M) -> M:
    """A column complement of im(subspace) inside im(ambient_space)."""
    require(subspace.r == ambient_space.r, "complement shape")
    if ambient_space.c == 0:
        return _zero_columns(ambient_space.r)
    pieces = []
    current = subspace
    for index in range(ambient_space.c):
        column = ambient_space.cols([index])
        if rank(hc(current, column)) > current.c:
            pieces.append(column)
            current = column if current.c == 0 else hc(current, column)
    if not pieces:
        return _zero_columns(ambient_space.r)
    return hc(*pieces) if len(pieces) > 1 else pieces[0]


def _dual_rows(separated: M, ambient: int, annihilated: M | None = None) -> M:
    if separated.c == 0:
        return M([], ambient)
    leading = separated if annihilated is None or annihilated.c == 0 else hc(separated, annihilated)
    require(rank(leading) == leading.c, "separated and retained directions overlap")
    adapted = extend(leading, eye(ambient))
    require(adapted.c == ambient and rank(adapted) == ambient, "adapted basis")
    coordinates = inverse(adapted)
    return coordinates.rows(range(separated.c))


def _rows_for(target: str, facts: dict) -> M:
    ambient = facts["ambient"]
    if target == "raw":
        return _dual_rows(facts["RK"], ambient)
    if target == "quotient":
        outside = _complement_in(facts["KB"], facts["K"])
        return _dual_rows(outside, ambient, facts["KB"])
    if target == "both":
        outside = _complement_in(facts["KB"], facts["K"])
        if facts["RKB"].c == 0:
            separated = outside
        elif outside.c == 0:
            separated = facts["RKB"]
        else:
            separated = hc(facts["RKB"], outside)
        retained = _complement_in(facts["RKB"], facts["KB"])
        return _dual_rows(separated, ambient, retained)
    raise ValueError("unknown target")


def produce_completion(source: M, repair: M, observer: M, target: str) -> dict:
    require(target in ("raw", "quotient", "both"), "unknown target")
    facts = analyze(source, repair, observer)
    rows = _rows_for(target, facts)
    minimum = {
        "raw": facts["raw_minimum"],
        "quotient": facts["quotient_minimum"],
        "both": facts["joint_minimum"],
    }[target]
    require(rows.r == minimum, "construction missed the minimum")
    return {
        "schema": "wdp-distinct-image-replay-v1",
        "task": TASK,
        "source": SOURCE,
        "field": FIELD,
        "target": target,
        "E": rows.encode(),
        "minimum": minimum,
        "dimensions": {
            "ambient": facts["ambient"],
            "raw_minimum": facts["raw_minimum"],
            "quotient_minimum": facts["quotient_minimum"],
            "joint_minimum": facts["joint_minimum"],
            "separate_sum": facts["separate_sum"],
        },
        "lower_columns": {
            "raw": facts["RK"],
            "quotient": _complement_in(facts["KB"], facts["K"]),
            "both": _obligation_columns(facts),
        }[target].encode(),
        "assumes_equal_images": False,
        "solves_original": False,
    }


def _obligation_columns(facts: dict) -> M:
    outside = _complement_in(facts["KB"], facts["K"])
    if facts["RKB"].c == 0:
        return outside
    if outside.c == 0:
        return facts["RKB"]
    return hc(facts["RKB"], outside)


def raw_holds(source: M, observer: M, rows: M) -> bool:
    facts_kernel = intersection_basis(image_basis(source), null(vc(observer, rows)))
    return facts_kernel.c == 0


def quotient_holds(repair: M, observer: M, rows: M) -> bool:
    algebraic = image_basis(repair)
    kernel = null(vc(observer, rows))
    if kernel.c == 0:
        return True
    if algebraic.c == 0:
        return False
    return rank(hc(algebraic, kernel)) == algebraic.c


def check_completion(source: M, repair: M, observer: M, witness: dict) -> dict:
    """Replay a submitted completion witness. Raises ValueError on rejection."""
    require(witness.get("schema") == "wdp-distinct-image-replay-v1", "wrong_task_or_stale_witness")
    require(witness.get("task") == TASK and witness.get("source") == SOURCE,
            "wrong_task_or_stale_witness")
    require(witness.get("field") == FIELD, "wrong_coefficient_field")
    target = witness.get("target")
    require(target in ("raw", "quotient", "both"), "wrong_task_or_stale_witness")
    rows = M.decode(witness["E"])
    require(rows.c == source.r, "row shape")
    facts = analyze(source, repair, observer)
    require(type(witness.get("assumes_equal_images")) is bool, "equal-image flag type")
    dimensions = witness.get("dimensions")
    expected_dimensions = {key: facts[key] for key in (
        "ambient", "raw_minimum", "quotient_minimum", "joint_minimum", "separate_sum"
    )}
    require(type(dimensions) is dict and dimensions.keys() == expected_dimensions.keys()
            and all(type(value) is int for value in dimensions.values())
            and dimensions == expected_dimensions, "dimension claims do not match the input")
    if witness["assumes_equal_images"] and not facts["images_equal"]:
        raise ValueError("r_and_b_conflated")
    _check_solution_claim(source, repair, witness)
    claimed = witness.get("minimum")
    require(type(claimed) is int and claimed >= 0, "minimum type")
    sharp = {
        "raw": facts["raw_minimum"],
        "quotient": facts["quotient_minimum"],
        "both": facts["joint_minimum"],
    }[target]
    if (
        target == "both"
        and claimed == facts["separate_sum"]
        and facts["separate_sum"] != facts["joint_minimum"]
    ):
        raise ValueError("optima_incorrectly_added")
    raw_ok = raw_holds(source, observer, rows)
    quotient_ok = quotient_holds(repair, observer, rows)
    if target in ("raw", "both") and not raw_ok:
        if target == "both" and quotient_ok:
            raise ValueError("quotient_without_raw")
        raise ValueError("blind_realizable_defect")
    if target == "quotient" and not quotient_ok:
        raise ValueError("quotient_failed")
    if target == "both" and raw_ok and not quotient_ok:
        raise ValueError("raw_without_quotient")
    require(claimed == sharp and rows.r == sharp, "minimum mismatch")
    lower = M.decode(witness["lower_columns"])
    require(_is_obstruction_basis(target, facts, lower), "lower certificate")
    return {
        "accepted": True,
        "target": target,
        "minimum": sharp,
        "separate_sum": facts["separate_sum"],
        "raw_holds": raw_ok,
        "quotient_holds": quotient_ok,
        "provider_calls": 0,
    }


def _is_obstruction_basis(target: str, facts: dict, lower: M) -> bool:
    """Accept `lower` only as an obstruction basis for the claimed target.

    Width and rank equal to the sharp count are required and are not enough.
    Raw columns are a basis of R∩K. Quotient columns lie in K and meet B only
    at 0. Joint columns lie in K and meet K∩B only inside T. The empty matrix
    is the basis when the sharp count is 0.
    """
    sharp = {
        "raw": facts["raw_minimum"],
        "quotient": facts["quotient_minimum"],
        "both": facts["joint_minimum"],
    }[target]
    if lower.r != facts["ambient"] or lower.c != sharp or rank(lower) != sharp:
        return False
    if target == "raw":
        return _same_space(lower, facts["RK"])
    if not _contained(lower, facts["K"]):
        return False
    if target == "quotient":
        return intersection_basis(lower, facts["B"]).c == 0
    meet = intersection_basis(lower, facts["KB"])
    if meet.c == 0:
        return True
    return _contained(meet, facts["RKB"])


def _check_solution_claim(source: M, repair: M, witness: dict) -> None:
    require(type(witness.get("solves_original")) is bool, "solution flag type")
    require(not witness["solves_original"], "observation_completion_does_not_certify_repairs")
    require("admissible_operation" not in witness, "repair_operation_requires_separate_checker")


def _annihilator_rows(separated: M, algebraic: M, ambient: int) -> M:
    """Dual coordinates of `separated` in a basis that begins with B.

    The rows vanish on B. `separated` must meet B only at zero.
    """
    if separated.c == 0:
        return M([], ambient)
    leading = algebraic if algebraic.c else separated
    if algebraic.c and separated.c:
        leading = hc(algebraic, separated)
    adapted = extend(leading, eye(ambient))
    coordinates = inverse(adapted)
    start = algebraic.c
    return coordinates.rows(range(start, start + separated.c))


def annihilator_status(source: M, repair: M, observer: M, target: str) -> dict:
    """Rows restricted to the annihilator of B.

    Raw or joint completion is impossible when R ∩ K ∩ B is nonzero, because
    every such row vanishes on that space. The obstruction vector is returned.
    When the obstruction is zero, joint completion has the quotient minimum:
    the quotient rows already separate the realizable invisible defects.
    """
    facts = analyze(source, repair, observer)
    blocked = facts["RKB"].c > 0 and target in ("raw", "both")
    if blocked:
        return {
            "feasible": False,
            "reason": "annihilator_menu_impossible",
            "obstruction": facts["RKB"].cols([0]).encode(),
        }
    if target == "raw":
        separated = facts["RK"]
        minimum = facts["raw_minimum"]
    elif target == "quotient":
        separated = _complement_in(facts["KB"], facts["K"])
        minimum = facts["quotient_minimum"]
    elif target == "both":
        separated = _complement_in(facts["KB"], facts["K"])
        minimum = facts["quotient_minimum"]
    else:
        raise ValueError("unknown target")
    rows = _annihilator_rows(separated, facts["B"], facts["ambient"])
    if rows.r and facts["B"].c:
        zero_image = M([[F(0)] * facts["B"].c for _ in range(rows.r)], facts["B"].c)
        require(rows @ facts["B"] == zero_image, "constructed row failed to annihilate B")
    return {"feasible": True, "minimum": minimum, "E": rows.encode()}


def _selected_rows(shelf: tuple, chosen: tuple) -> M:
    if not chosen:
        return M([], shelf[0].c if shelf else 0)
    return vc(*[shelf[index] for index in chosen])


def suite_is_sufficient(source: M, repair: M, observer: M, rows: M, target: str) -> bool:
    raw_ok = raw_holds(source, observer, rows)
    quotient_ok = quotient_holds(repair, observer, rows)
    if target == "raw":
        return raw_ok
    if target == "quotient":
        return quotient_ok
    if target == "both":
        return raw_ok and quotient_ok
    raise ValueError("unknown target")


def produce_shelf(source: M, repair: M, observer: M, shelf: tuple, costs: tuple, target: str) -> dict:
    """Exact minimum positive-cost subset. Empty shelf is allowed."""
    require(
        len(shelf) == len(costs) and all(_positive_rational(cost) for cost in costs),
        "positive costs",
    )
    best = None
    best_cost = None
    for size in range(len(shelf) + 1):
        for chosen in combinations(range(len(shelf)), size):
            rows = _selected_rows(shelf, chosen) if chosen else M([], observer.c)
            if not suite_is_sufficient(source, repair, observer, rows, target):
                continue
            cost = sum((costs[index] for index in chosen), F(0))
            if best_cost is None or cost < best_cost:
                best = chosen
                best_cost = cost
    if best is None:
        whole = _selected_rows(shelf, tuple(range(len(shelf)))) if shelf else M([], observer.c)
        return {
            "feasible": False,
            "reason": "shelf_impossible",
            "obstruction_accepted": not suite_is_sufficient(
                source, repair, observer, whole, target
            ),
        }
    return {
        "feasible": True,
        "indices": best,
        "cost": best_cost,
        "E": _selected_rows(shelf, best).encode() if best else M([], observer.c).encode(),
    }


def check_shelf(source: M, repair: M, observer: M, shelf: tuple, costs: tuple,
                target: str, witness: dict) -> dict:
    """Independent exhaustive optimality check of a submitted suite."""
    require(
        len(shelf) == len(costs) and all(_positive_rational(cost) for cost in costs),
        "positive costs",
    )
    feasible = witness.get("feasible")
    require(type(feasible) is bool, "feasible flag")
    if not feasible:
        whole = _selected_rows(shelf, tuple(range(len(shelf)))) if shelf else M([], observer.c)
        require(not suite_is_sufficient(source, repair, observer, whole, target),
                "false shelf impossibility")
        return {"accepted": True, "feasible": False}
    chosen = tuple(witness["indices"])
    require(all(type(index) is int and 0 <= index < len(shelf) for index in chosen),
            "shelf indices must be in-range integers")
    require(len(set(chosen)) == len(chosen), "duplicate shelf index")
    rows = _selected_rows(shelf, chosen) if chosen else M([], observer.c)
    require(M.decode(witness["E"]) == rows, "submitted rows do not match the chosen instruments")
    require(suite_is_sufficient(source, repair, observer, rows, target), "insufficient suite")
    cost = sum((costs[index] for index in chosen), F(0))
    require(cost == rational(witness["cost"]), "cost mismatch")
    for size in range(len(shelf) + 1):
        for other in combinations(range(len(shelf)), size):
            other_rows = _selected_rows(shelf, other) if other else M([], observer.c)
            other_cost = sum((costs[index] for index in other), F(0))
            if other_cost < cost and suite_is_sufficient(
                source, repair, observer, other_rows, target
            ):
                raise ValueError("suite is not minimum cost")
    return {"accepted": True, "feasible": True, "cost": cost, "provider_calls": 0}


def inclusion_examples() -> dict:
    """R ⊂ B, B ⊂ R, and neither, with a joint minimum below the separate sum."""

    def column(*entries):
        return M([[entry] for entry in entries], 1)

    def pack(columns):
        return hc(*columns)

    proper = {
        "name": "R_subset_B",
        "Ds": column(1, 0, 0),
        "Dr": pack([column(1, 0, 0), column(0, 1, 0)]),
        "Q": M([[0, 0, 1]], 3),
    }
    reverse = {
        "name": "B_subset_R",
        "Ds": pack([column(1, 0, 0), column(0, 1, 0)]),
        "Dr": column(1, 0, 0),
        "Q": M([[0, 0, 1]], 3),
    }
    neither = {
        "name": "neither_inclusion",
        "Ds": pack([column(0, 1, 0, 0), column(0, 0, 1, 0)]),
        "Dr": pack([column(1, 0, 0, 0), column(0, 1, 0, 0)]),
        "Q": M([[0, 0, 0, 1]], 4),
    }
    out = {}
    for item in (proper, reverse, neither):
        facts = analyze(item["Ds"], item["Dr"], item["Q"])
        out[item["name"]] = {
            "raw_minimum": facts["raw_minimum"],
            "quotient_minimum": facts["quotient_minimum"],
            "joint_minimum": facts["joint_minimum"],
            "separate_sum": facts["separate_sum"],
            "R_in_B": _same_space(intersection_basis(facts["R"], facts["B"]), facts["R"]),
            "B_in_R": _same_space(intersection_basis(facts["R"], facts["B"]), facts["B"]),
        }
    return out
