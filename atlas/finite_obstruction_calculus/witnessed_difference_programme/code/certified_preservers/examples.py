"""Explicit inputs and finite exploration pockets, not universal proof tests."""

from __future__ import annotations

from itertools import combinations

from state_effect_readout.model import identity, matmul

from .model import (
    ONE,
    ZERO,
    Carrier,
    G,
    I,
    Q,
    apply,
    basis_unit,
    canonical_ray,
    matrix,
    scale,
    subtract,
    vector,
    wire,
)


def task(kind: str, gram, **inputs) -> dict:
    return wire(
        {"schema": "wdp.preserver.task.v1", "field": "Q(i)", "kind": kind, "gram": gram, **inputs}
    )


def hadamard():
    z = G.of(Q(1, 2), Q(1, 2))
    return ((z, z), (z, -z))


def similarity_four():
    return matrix([[1, -1, -1, 0], [1, 1, 0, 1], [1, 0, 1, -1], [0, -1, 1, 1]])


def reference_problems() -> dict[str, dict]:
    delta_h = matrix([[1, 0], [0, -1]])
    s = scale(-I, delta_h)
    table = [
        subtract(matmul(s, basis_unit(2, j, k)), matmul(basis_unit(2, j, k), s))
        for j in range(2)
        for k in range(2)
    ]
    return {
        "hadamard": task(
            "preserver", identity(2), frame=identity(2), images=tuple(zip(*hadamard(), strict=True))
        ),
        "even_similarity": task(
            "preserver",
            identity(4),
            frame=identity(4),
            images=tuple(zip(*similarity_four(), strict=True)),
        ),
        "reachable": task("reachability", identity(3), source=[1, 0, 0], target=[1, 1, 0]),
        "norm_obstruction": task("reachability", identity(3), source=[1, 0, 0], target=[1, 1, 1]),
        "luders": task("luders", identity(3), source=[1, 0, 0], target=[1, 1, 1]),
        "zero_branch": task("luders", identity(2), source=[1, 0], target=[0, 1]),
        "nonstandard_gram": task(
            "reachability", matrix([[2, I], [-I, 2]]), source=[1, 0], target=[0, 1]
        ),
        "generator": task("generator", identity(2), derivation=table),
    }


def graph_pocket(dimension: int) -> dict:
    """The d^2 tomography rays and all pair probabilities on that finite set."""
    if type(dimension) is not int or dimension < 2:
        raise ValueError("pocket dimension must be at least two")
    rays = list(identity(dimension))
    for j, k in combinations(range(dimension), 2):
        for phase in (ONE, I):
            rays.append(
                tuple(ONE if a == j else phase if a == k else ZERO for a in range(dimension))
            )
    carrier = Carrier(identity(dimension))
    h = identity(dimension)
    small_h = hadamard()
    h = tuple(
        tuple(small_h[j][k] if j < 2 and k < 2 else h[j][k] for k in range(dimension))
        for j in range(dimension)
    )
    images = [apply(h, ray) for ray in rays]
    orthogonal = []
    comparisons = 0
    for j, k in combinations(range(len(rays)), 2):
        before = carrier.probability(rays[j], rays[k])
        after = carrier.probability(images[j], images[k])
        if before != after:
            raise ValueError("pocket probability changed under the Gaussian Hadamard")
        if before == 0:
            orthogonal.append([j, k])
        comparisons += 1
    return wire(
        {
            "dimension": dimension,
            "rays": rays,
            "images": images,
            "orthogonal_pairs": orthogonal,
            "probability_comparisons": comparisons,
            "scope": "finite tomography pocket only",
        }
    )


def qubit_countermodel() -> dict:
    rays = tuple(vector(x) for x in ([1, 0], [0, 1], [1, 1], [1, -1], [1, 2], [2, -1]))
    permutation = (1, 0, 4, 5, 2, 3)
    carrier = Carrier(identity(2))
    if sorted(permutation) != list(range(6)):
        raise ValueError("countermodel is not a permutation")
    for j, ray in enumerate(rays):
        perpendicular = canonical_ray((-ray[1].conjugate(), ray[0].conjugate()))
        if perpendicular not in tuple(canonical_ray(x) for x in rays):
            raise ValueError("finite support not closed under orthogonal complement")
        for k, other in enumerate(rays):
            if (carrier.inner(ray, other) == ZERO) != (
                carrier.inner(rays[permutation[j]], rays[permutation[k]]) == ZERO
            ):
                raise ValueError("countermodel failed orthogonality preservation")
    before, after = carrier.probability(rays[0], rays[2]), carrier.probability(rays[1], rays[4])
    if before == after:
        raise ValueError("countermodel no longer separates probability preservation")
    return wire(
        {
            "rays": rays,
            "permutation": permutation,
            "before": before,
            "after": after,
            "global_extension": "identity outside the complement-closed six-ray support",
        }
    )
