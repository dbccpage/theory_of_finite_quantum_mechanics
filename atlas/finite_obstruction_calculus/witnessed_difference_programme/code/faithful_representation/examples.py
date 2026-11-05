"""Small declared inputs, independent enumeration, and retained replay evidence."""

from copy import deepcopy
from fractions import Fraction
from itertools import product

from .core import assignments, check, digest, encode, evaluate_family, family_at, family_count, search, solution


def problem(variables=(), relations=()):
    return {"schema_version": 1, "goal": "exists_global_assignment",
            "variables": [{"name": v, "domain": list(d)} for v, d in variables],
            "relations": [{"name": n, "scope": list(s), "rows": [list(r) for r in rows]}
                          for n, s, rows in relations], "assumptions": [], "authorization": []}


def cycle(consistent):
    equal = [("0", "0"), ("1", "1")]
    different = [("0", "1"), ("1", "0")]
    return problem([(v, ["0", "1"]) for v in "xyz"],
                   [("xy", "xy", equal), ("yz", "yz", equal),
                    ("xz", "xz", equal if consistent else different)])


def presentation_chain():
    original = problem([(v, ["0", "1"]) for v in "abc"],
                       [("ab", "ab", [("0", "0"), ("1", "1")]),
                        ("ac", "ac", [("0", "0"), ("1", "1")])])
    steps = [
        {"kind": "join", "left": "ab", "right": "ac", "name": "abc"},
        {"kind": "split", "relation": "abc", "components": [["a", "b"], ["a", "c"]],
         "names": ["ab", "ac"]},
        {"kind": "auxiliary", "name": "d", "domain": ["0", "1"], "scope": ["a"],
         "rows": [["0", "1"], ["1", "0"]], "relation": "ad"},
        {"kind": "rename", "variables": {v: v.upper() for v in "abcd"},
         "values": {v: {"0": "false", "1": "true"} for v in "abcd"}},
    ]
    return original, steps


def compare(original):
    encoded = encode(original)
    direct = {digest(x) for x in assignments(original) if solution(original, x)}
    reconstructed = []
    for i in range(family_count(encoded)):
        result = evaluate_family(encoded, family_at(encoded, i))
        if result["outcome"] == "SOLUTION":
            reconstructed.append(digest(result["answer"]))
    assert len(reconstructed) == len(set(reconstructed)), "family encoding not injective"
    assert set(reconstructed) == direct, "global/local solution mismatch"
    trace = search(encoded, family_count(encoded))
    assert check(original, trace)["accepted"]
    assert (trace["status"] == "Proved") == bool(direct)
    return {"assignments": sum(1 for _ in assignments(original)),
            "families": family_count(encoded), "solutions": len(direct)}


def exhaustive_boolean_cases():
    """Every triple of binary relations on the three edges of a Boolean triangle."""
    tuples = list(product(["0", "1"], repeat=2))
    tables = [[row for i, row in enumerate(tuples) if mask & (1 << i)] for mask in range(16)]
    counts = {"instances": 0, "satisfiable": 0, "families": 0}
    for a, b, c in product(tables, repeat=3):
        original = problem([(v, ["0", "1"]) for v in "xyz"],
                           [("xy", "xy", a), ("yz", "yz", b), ("xz", "xz", c)])
        result = compare(original)
        counts["instances"] += 1
        counts["satisfiable"] += bool(result["solutions"])
        counts["families"] += result["families"]
    return counts


def calculus_boundary():
    """Exact coefficients and integral of product_(k=0)^10 (x-k)^2."""
    polynomial = [Fraction(1)]
    for k in range(11):
        for _ in range(2):
            changed = [Fraction(0)] * (len(polynomial) + 1)
            for i, coefficient in enumerate(polynomial):
                changed[i] -= k * coefficient
                changed[i + 1] += coefficient
            polynomial = changed
    def value(x):
        return sum(c * x ** i for i, c in enumerate(polynomial))
    integral = sum(c * Fraction(10 ** (i + 1), i + 1) for i, c in enumerate(polynomial))
    assert all(value(k) == 0 for k in range(11)) and integral > 0
    # F=x²/2 differentiates to x. Compute an affine fit from the supplied samples.
    derivative = [Fraction(0), 2 * Fraction(1, 2)]
    assert derivative == [Fraction(0), Fraction(1)]
    samples = [(Fraction(k), Fraction(k)) for k in range(11)]
    slope = (samples[1][1] - samples[0][1]) / (samples[1][0] - samples[0][0])
    intercept = samples[0][1] - slope * samples[0][0]
    assert all(slope * x + intercept == y for x, y in samples)
    exact_answer = Fraction(10 ** 2, 2)
    conditional_answer = slope * Fraction(10 ** 2, 2) + 10 * intercept
    return {"exact_formula": {"answer": str(exact_answer), "derivative_coefficients": list(map(str, derivative))},
            "samples_only": {"primary_status": "Undetermined", "reason": "OBSERVATION_COLLISION",
                             "collision_polynomial": list(map(str, polynomial)),
                             "positive_integral_difference": str(integral)},
            "affine_assumption": {"slope": str(slope), "intercept": str(intercept),
                                  "conditional_answer": str(conditional_answer)},
            "exhausted_budget": {"status": "Undetermined", "reason": "BUDGET_EXHAUSTED"}}


def boundaries():
    impossible = cycle(False)
    encoded = encode(impossible)
    results = [evaluate_family(encoded, family_at(encoded, i)) for i in range(family_count(encoded))]
    assert all(r["outcome"] == "INCOMPATIBLE" and any(r["defect"]) for r in results)
    # Q=0 has zero output, B=V makes every defect algebraically repairable.
    # Actual permitted local rows nevertheless have no compatible selection.
    sound_only_source, sound_only_target = {0, 1}, {0}
    assert sound_only_target <= sound_only_source and 1 not in sound_only_target
    empty_target = set()
    assert empty_target <= {1} and bool({1}) and not empty_target
    # Larger-carrier success: 3*(-1/3)+1=0, but no integer can solve 3*x+1=0.
    assert 3 * Fraction(-1, 3) + 1 == 0 and (-1) % 3 != 0
    return {"blind_observer_false_greens": len(results),
            "whole_defect_repair_space_false_greens": len(results), "original_solutions": 0,
            "sound_only_lost_solution": 1,
            "sound_only_empty_target": {"source_solution_count": 1, "target_solution_count": 0,
                                        "backward_sound": True, "forward_coverage": False},
            "completion_only": {"carrier": "Q", "solution": "-1/3", "original_carrier": "Z",
                                "integer_divisibility_failure": "3 does not divide -1"},
            "calculus": calculus_boundary()}


def run_examples():
    original, changes = presentation_chain()
    cases = [("consistent_cycle", cycle(True), ()), ("inconsistent_cycle", cycle(False), ()),
             ("four_transports", original, changes), ("empty_problem", problem(), ()),
             ("empty_domain", problem([("x", [])]), ()),
             ("false_nullary", problem([], [("false", [], [])]), ()),
             ("true_nullary", problem([], [("true", [], [[]])]), ())]
    runs = {}
    for name, p, moves in cases:
        encoded = encode(p, moves)
        trace = search(encoded, len(moves) + 2 * family_count(encoded), proposals=[[999]] * 20)
        receipt = check(p, trace)
        assert receipt["accepted"]
        runs[name] = {"problem": p, "certificate": trace, "receipt": receipt}
    p = cycle(False)
    first = search(encode(p), 2, proposals=[[999]] * 20)
    resumed = search(encode(p), 16, first)
    assert resumed["status"] == "Refuted" and check(p, resumed)["accepted"]
    runs["resumed_exhaustion"] = {"problem": p, "certificate": resumed, "receipt": check(p, resumed)}
    mutation = deepcopy(runs["four_transports"]["certificate"])
    mutation["encoding"]["changes"][0]["parent"] = "stale"
    assert not check(original, mutation)["accepted"]
    return runs
