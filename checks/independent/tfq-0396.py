"""Independent exact Genesis-to-finite-obstruction carrier audit.

AuthorityEffect: None. No repository imports. Every bound and output count is
computed here; the general zero-law and term-map proofs are in Lean.
"""
from __future__ import annotations

from itertools import product
import json
from typing import TypeAlias

import sympy as sp  # type: ignore[import-untyped]

Instance: TypeAlias = tuple[int, tuple[int, ...]]
Context: TypeAlias = tuple[int, tuple[int | None, ...]]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def audit(n: int, forms: tuple[int, ...], facts: frozenset[Instance], rules: frozenset[int]) -> dict[str, object]:
    contexts: tuple[Context, ...] = tuple((f, xs) for f, arity in enumerate(forms)
        for xs in product((None, *range(n)), repeat=arity) if None in xs)
    profiles = tuple(tuple(f in rules or (f, tuple(d if x is None else x for x in xs)) in facts
                           for f, xs in contexts) for d in range(n))
    # A separate equivalence computation uses all hole masks, not the profile helper.
    equivalent = [[True for _ in range(n)] for _ in range(n)]
    for f, arity in enumerate(forms):
        for mask in range(1, 1 << arity):
            fixed_positions = tuple(k for k in range(arity) if not mask & (1 << k))
            for fixed_values in product(range(n), repeat=len(fixed_positions)):
                binding = dict(zip(fixed_positions, fixed_values))
                for i, j in product(range(n), repeat=2):
                    left = tuple(i if mask & (1 << k) else binding[k] for k in range(arity))
                    right = tuple(j if mask & (1 << k) else binding[k] for k in range(arity))
                    a = f in rules or (f, left) in facts
                    b = f in rules or (f, right) in facts
                    equivalent[i][j] = equivalent[i][j] and (a == b)
    require(all(equivalent[i][j] == (profiles[i] == profiles[j]) for i, j in product(range(n), repeat=2)),
            "canonical quotient disagrees with source contextual relation")
    matrix = sp.Matrix(n, n, lambda i, j: int(equivalent[int(i)][int(j)]))
    require(matrix == matrix.T, "zero symmetry")
    require(all(matrix[i, i] == 1 for i in range(n)), "zero reflexivity")
    composed = matrix * matrix
    require(all(composed[i, j] == 0 or matrix[i, j] == 1 for i, j in product(range(n), repeat=2)),
            "zero transitivity")
    # Build the class map by representatives, independently of set(profiles).
    representatives: list[int] = []
    image: list[int] = []
    for d in range(n):
        found = next((k for k, rep in enumerate(representatives) if equivalent[d][rep]), None)
        if found is None:
            found = len(representatives)
            representatives.append(d)
        image.append(found)
    require(len(representatives) == len(set(profiles)), "quotient cardinality")
    require(all((image[i] == image[j]) == equivalent[i][j] for i, j in product(range(n), repeat=2)),
            "term-map kernel")
    require(set(image) == set(range(len(representatives))), "term-map surjectivity")
    return {"data": n, "forms": forms, "contexts": len(contexts), "class_map": image,
            "classes": len(representatives), "zero_matrix": [list(map(int, matrix.row(i))) for i in range(n)]}


def main() -> None:
    count = 0
    histogram: dict[str, int] = {}
    for n, forms in product(range(4), ((), (1,), (2,), (1, 2))):
        atoms = tuple((f, xs) for f, arity in enumerate(forms) for xs in product(range(n), repeat=arity))
        for fact_bits, rule_bits in product(range(1 << len(atoms)), range(1 << len(forms))):
            facts = frozenset(p for k, p in enumerate(atoms) if fact_bits & (1 << k))
            rules = frozenset(f for f in range(len(forms)) if rule_bits & (1 << f))
            answer = audit(n, forms, facts, rules)
            key = str(answer["classes"])
            histogram[key] = histogram.get(key, 0) + 1
            count += 1
    expected = sum(sp.Integer(2)**(sum(sp.Integer(n)**a for a in forms) + len(forms))
                   for n, forms in product(range(4), ((), (1,), (2,), (1, 2))))
    require(count == expected, "regime census")
    empty = audit(0, (), frozenset(), frozenset())
    initial = audit(2, (), frozenset(), frozenset())
    separated = audit(2, (1,), frozenset({(0, (0,))}), frozenset())
    ruled = audit(2, (1,), frozenset({(0, (0,))}), frozenset({0}))
    require((empty["classes"], initial["classes"], separated["classes"], ruled["classes"]) == (0, 1, 2, 1),
            "explicit sealed crossing and controls")
    # Exact factorization criterion, exhaustive over every finite two-point map.
    factors = 0
    refusals = 0
    for before, after in product((initial, separated), repeat=2):
        a = before["class_map"]
        b = after["class_map"]
        if not isinstance(a, list) or not isinstance(b, list):
            raise RuntimeError("class-map fixture")
        before_count, after_count = before["classes"], after["classes"]
        if not isinstance(before_count, int) or not isinstance(after_count, int):
            raise RuntimeError("class-count fixture")
        for f in product(range(2), repeat=2):
            respects = all(a[i] != a[j] or b[f[i]] == b[f[j]] for i, j in product(range(2), repeat=2))
            # A function on quotient classes exists iff class outputs are consistent.
            candidates = tuple(product(range(after_count), repeat=before_count))
            exists = any(all(F[a[i]] == b[f[i]] for i in range(2)) for F in candidates)
            require(respects == exists, "factorization criterion")
            factors += exists
            refusals += not exists
    return_data = {"node": "TFQ-0396", "authority_effect": "None", "regimes_checked": count,
        "datum_bound": 3, "signatures": [[], [1], [2], [1, 2]], "class_count_histogram": histogram,
        "fixtures": {"inert": empty, "unseparated_marks": initial, "sealed_response": separated, "uniform_rule": ruled},
        "factorizations": factors, "refused_factorizations": refusals,
        "negative_controls_checked": 4,
        "mutation_coverage": "not measured by fixed regression fixtures"}
    # Four fixed negative controls, each contradicted by an exact fixture.
    require(initial["classes"] != 2, "inequality-of-labels as internal distinction")
    require(separated["classes"] != 1, "constant term map")
    require(ruled["classes"] != separated["classes"], "ignore uniform coverage")
    require(refusals > 0, "all maps factor through collapse")
    print(json.dumps(return_data, indent=2))


if __name__ == "__main__":
    main()
