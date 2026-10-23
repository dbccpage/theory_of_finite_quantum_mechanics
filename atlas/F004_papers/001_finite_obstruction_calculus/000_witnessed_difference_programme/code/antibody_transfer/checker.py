"""Bounded exact checks for ANT-P01--P06; no policy or learned runtime engine.

The finite acceptance sets are declared mathematical input, not an assertion
that an external evaluator was verified. Polynomial/dual examples additionally
compute their own predicates. Cost rates are declared units, not benchmarks.
"""
from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path


class Refused(ValueError):
    """Malformed input or a submitted certificate failing independent replay."""


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise Refused(reason)


def encoded(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value: object) -> str:
    return hashlib.sha256(encoded(value).encode()).hexdigest()


def fields(value: object, expected: set[str], name: str) -> None:
    require(type(value) is dict and set(value) == expected, f"{name}: incorrect fields")


def read_json(path: Path) -> dict:
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, "duplicate JSON key")
            result[key] = value
        return result

    def nonexact(value):
        raise Refused(f"nonexact JSON scalar: {value}")

    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=pairs,
                      parse_float=nonexact, parse_constant=nonexact)


def rational(value: object) -> Fraction:
    require(type(value) is str and len(value) <= 200, "canonical rational string required")
    try:
        result = Fraction(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise Refused("invalid rational") from exc
    require(str(result) == value, "noncanonical rational")
    return result


def natural(value: object, cap: int, name: str) -> int:
    require(type(value) is int and 0 <= value <= cap, f"{name}: exact bounded natural required")
    return value


def names(value: object, name: str, distinct: bool = True) -> list[str]:
    require(type(value) is list and len(value) <= (128 if distinct else 10000), f"{name}: finite array cap")
    require(all(type(v) is str and 0 < len(v) <= 128 for v in value), f"{name}: invalid name")
    require(not distinct or len(set(value)) == len(value), f"{name}: duplicate name")
    return value


def task(value: dict) -> tuple[set[str], set[str]]:
    fields(value, {"id", "carrier", "valid", "profile"}, "task")
    require(type(value["id"]) is str and bool(value["id"]), "task identity required")
    require(type(value["profile"]) is dict, "profile bindings must be object")
    carrier, valid = set(names(value["carrier"], "carrier")), set(names(value["valid"], "valid set"))
    require(valid <= carrier, "valid set outside carrier")
    return carrier, valid


def transfer(problem: dict) -> dict:
    fields(problem, {"source", "target", "adapter", "outside_domain", "rules", "pool"}, "transfer problem")
    source, source_valid = task(problem["source"])
    target, target_valid = task(problem["target"])
    adapter = problem["adapter"]
    require(type(adapter) is dict and set(adapter) <= target, "adapter domain outside target carrier")
    require(all(type(x) is str and x in source for x in adapter.values()), "adapter image outside source carrier")
    require(problem["outside_domain"] == "not_applicable", "unsupported out-of-domain handling policy")
    pool = names(problem["pool"], "pool", distinct=False)
    require(set(pool) <= target, "pool outside target carrier")
    rules = problem["rules"]
    require(type(rules) is list and len(rules) <= 128, "rule family cap")
    audit_failures = sorted(y for y in target_valid & set(adapter) if adapter[y] not in source_valid)
    records, active, rejected, ids = [], [], set(), set()
    for rule in rules:
        fields(rule, {"id", "rejects"}, "rule")
        require(type(rule["id"]) is str and rule["id"] and rule["id"] not in ids, "duplicate/invalid rule ID")
        ids.add(rule["id"])
        rejection = set(names(rule["rejects"], "rejection set"))
        require(rejection <= source, "rejection outside source carrier")
        source_failures = sorted(rejection & source_valid)
        image = {y for y, x in adapter.items() if x in rejection}
        transfer_failures = sorted(image & target_valid)
        admitted = not source_failures and not transfer_failures
        if admitted:
            active.append(rule["id"])
            rejected |= image
        records.append({"id": rule["id"], "source_sound": not source_failures,
                        "source_counterexamples": source_failures, "transfer_safe": not transfer_failures,
                        "target_counterexamples": transfer_failures, "transferred_rejection": sorted(image),
                        "admitted": admitted})
    require(not rejected & target_valid, "internal accumulation safety failure")
    return {"input_sha256": digest(problem), "adapter_safe": not audit_failures,
            "adapter_counterexamples": audit_failures, "valid_inputs_outside_domain": sorted(target_valid - set(adapter)),
            "rules": records, "active_rules": active, "rejected": sorted(rejected),
            "retained": sorted(target - rejected), "pool_occurrences": len(pool),
            "hits": sum(y in rejected for y in pool), "valid_occurrences": sum(y in target_valid for y in pool),
            "out_of_domain_occurrences": sum(y not in adapter for y in pool),
            "accumulation_sound": True, "authority_effect": "None"}


def polynomial(value: object) -> tuple[Fraction, ...]:
    require(type(value) is list and 1 <= len(value) <= 17, "polynomial degree cap: 16")
    result = tuple(rational(x) for x in value)
    require(len(result) == 1 or result[-1] != 0, "polynomial must omit trailing zero coefficients")
    return result


def derivative(value: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    return tuple(i * value[i] for i in range(1, len(value))) or (Fraction(0),)


def truncate(value: tuple[Fraction, ...], degree: int) -> tuple[Fraction, ...]:
    out = value[:degree + 1]
    while len(out) > 1 and out[-1] == 0:
        out = out[:-1]
    return out


def polynomial_binding(problem: dict) -> dict:
    fields(problem, {"candidates", "source_integrand", "target_integrand", "truncate_degree"}, "polynomial problem")
    candidates = problem["candidates"]
    require(type(candidates) is dict and len(candidates) <= 128, "polynomial pool cap")
    names(list(candidates), "polynomial candidate IDs")
    source, target = polynomial(problem["source_integrand"]), polynomial(problem["target_integrand"])
    degree = problem["truncate_degree"]
    if degree is not None:
        natural(degree, 16, "truncation degree")
    rows = []
    for name in sorted(candidates):
        coefficients = candidates[name]
        value = polynomial(coefficients)
        mapped = value if degree is None else truncate(value, degree)
        before, after = derivative(value), derivative(mapped)
        rows.append({"id": name, "derivative": list(map(str, before)), "mapped_derivative": list(map(str, after)),
                     "target_valid": before == target, "source_accepts_mapped": after == source,
                     "transferred_guard_rejects": after != source, "commutes": before == after})
    return {"input_sha256": digest(problem), "rows": rows, "identity_data_binding": source == target,
            "adapter_safe": all(not r["target_valid"] or r["source_accepts_mapped"] for r in rows),
            "commutes_on_target_valid": all(not r["target_valid"] or r["commutes"] for r in rows),
            "scope": "listed exact rational polynomials; not a symbolic universal proof"}


def circulation(problem: dict) -> dict:
    fields(problem, {"d0", "weights", "dual", "queries", "tolerance"}, "circulation problem")
    matrix = problem["d0"]
    require(type(matrix) is list and 1 <= len(matrix) <= 8 and type(matrix[0]) is list, "matrix row bound")
    columns = len(matrix[0])
    require(columns <= 8 and all(type(row) is list and len(row) == columns for row in matrix), "matrix shape")
    matrix = [[rational(x) for x in row] for row in matrix]
    weights, dual = problem["weights"], problem["dual"]
    require(type(weights) is list and type(dual) is list and len(weights) == len(dual) == len(matrix), "dual/weight shape")
    weights, dual = list(map(rational, weights)), list(map(rational, dual))
    require(all(w > 0 for w in weights), "weights must be strictly positive")
    require(all(abs(y) <= w for y, w in zip(dual, weights)), "dual capacity exceeded")
    annihilator = [sum(row[j] * y for row, y in zip(matrix, dual)) for j in range(columns)]
    require(all(x == 0 for x in annihilator), "dual does not annihilate repair image")
    tolerance = rational(problem["tolerance"])
    require(tolerance >= 0, "negative tolerance")
    queries = problem["queries"]
    require(type(queries) is dict and len(queries) <= 128, "query cap")
    names(list(queries), "query IDs")
    evaluated = []
    for name in sorted(queries):
        values = queries[name]
        require(type(values) is list and len(values) == len(matrix), "query vector shape")
        score = sum(y * rational(x) for y, x in zip(dual, values))
        evaluated.append({"id": name, "score": str(score), "lower_bound": str(abs(score)),
                          "rejects": abs(score) > tolerance})
    return {"input_sha256": digest(problem), "annihilator": list(map(str, annihilator)), "queries": evaluated,
            "tolerance": str(tolerance), "sound_for": "acceptance by weighted distance to any subset of the declared repair image"}


def cost(problem: dict, transfer_problem: dict) -> dict:
    fields(problem, {"setup", "guard", "evaluation", "units"}, "cost model")
    require(type(problem["units"]) is str and bool(problem["units"]), "cost units required")
    setup, guard, evaluation = (rational(problem[k]) for k in ("setup", "guard", "evaluation"))
    require(min(setup, guard, evaluation) >= 0, "negative cost")
    checked = transfer(transfer_problem)
    n, h = checked["pool_occurrences"], checked["hits"]
    bare = n * evaluation
    guarded = setup + n * guard + (n - h) * evaluation
    return {"model_sha256": digest(problem), "transfer_sha256": digest(transfer_problem), "N": n, "h": h,
            "bare": str(bare), "guarded": str(guarded), "saving": str(bare - guarded), "profitable": bare > guarded,
            "hit_threshold": str((n * guard + setup) / evaluation) if evaluation else None,
            "fraction_threshold": str(guard / evaluation + setup / (n * evaluation)) if n and evaluation else None,
            "units": problem["units"], "cost_evidence": "declared rates; exact count on supplied target occurrence pool"}


def audit_cost(problem: dict) -> dict:
    fields(problem, {"adapter", "source_per_rule", "combined_per_rule", "rules"}, "audit cost model")
    adapter, source, combined = (rational(problem[k]) for k in ("adapter", "source_per_rule", "combined_per_rule"))
    require(min(adapter, source, combined) >= 0, "negative audit cost")
    rules = natural(problem["rules"], 1000000, "number of rules")
    left, right, difference = adapter + rules * source, rules * combined, combined - source
    return {"input_sha256": digest(problem), "reusable": str(left), "per_rule": str(right),
            "no_more_expensive": left <= right, "strict_saving": left < right,
            "rate_regime": "higher" if difference > 0 else "equal" if difference == 0 else "lower",
            "rule_threshold": str(adapter / difference) if difference > 0 else None,
            "scope": "arithmetic for declared costs of the same obligations"}


def evaluate(problem: dict) -> dict:
    fields(problem, {"schema", "transfer", "polynomial", "circulation", "cost", "audit_cost"}, "bundle")
    require(problem["schema"] == "wdp-antibody-input-v1", "unknown input schema")
    require(type(problem["polynomial"]) is list and len(problem["polynomial"]) <= 32, "polynomial case cap")
    require(type(problem["audit_cost"]) is list and len(problem["audit_cost"]) <= 32, "cost case cap")
    return {"schema": "wdp-antibody-receipt-v1", "authority_effect": "None", "input_sha256": digest(problem),
            "transfer": transfer(problem["transfer"]),
            "polynomial": [polynomial_binding(p) for p in problem["polynomial"]],
            "circulation": circulation(problem["circulation"]), "cost": cost(problem["cost"], problem["transfer"]),
            "audit_cost": [audit_cost(p) for p in problem["audit_cost"]]}


def verify(problem: dict, submitted: dict) -> dict:
    require(encoded(submitted) == encoded(evaluate(problem)), "submitted receipt differs from independent evaluation")
    return {"status": "PASS", "authority_effect": "None", "input_sha256": digest(problem),
            "receipt_sha256": digest(submitted), "scope": "listed finite tables, exact queries and declared cost arithmetic"}
