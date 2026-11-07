"""Exact finite obstruction to extending the existing Q^3 exotic to Q(i)^3.

This checker imports no repository code. It verifies every frame and every
prescribed real-ray value, then checks an integer linear combination giving
0 = 32 for g = 3*f - 1. No positivity, regularity or symmetry is assumed.
It does not classify other Gaussian-rational frame functions.
"""
from __future__ import annotations

import argparse
import copy
import json
from collections import Counter
from math import gcd
from pathlib import Path


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def integers(value: object, length: int, label: str) -> list[int]:
    require(isinstance(value, list), f"{label}: expected list")
    require(len(value) == length, f"{label}: wrong length")
    require(all(type(x) is int for x in value), f"{label}: expected integers")
    return value


def inner(u: list[int], v: list[int]) -> tuple[int, int]:
    return (
        sum(u[k] * v[k] + u[k + 1] * v[k + 1] for k in (0, 2, 4)),
        sum(u[k] * v[k + 1] - u[k + 1] * v[k] for k in (0, 2, 4)),
    )


def exotic_sign(v: list[int]) -> int:
    require(all(v[k] == 0 for k in (1, 3, 5)), "prescribed ray must be real")
    coordinates = v[::2]
    require(gcd(*coordinates) == 1, "real representative must be primitive")
    odd = [x for x in coordinates if x % 2]
    require(bool(odd), "real representative must not be all even")
    if len(odd) != 2:
        return 0
    return -1 if (odd[0] - odd[1]) % 4 == 0 else 1


def verify(data: dict) -> dict[str, int]:
    rays = [integers(v, 6, "ray") for v in data["rays"]]
    require(bool(rays), "empty ray list")
    require(len({tuple(v) for v in rays}) == len(rays), "duplicate ray")
    for v in rays:
        require(any(v), "zero vector")
        require(gcd(*v) == 1, "representative must have integer content one")
    coefficients: Counter[int] = Counter()
    rhs = 0
    frame_weight = 0
    real_weight = 0
    real_signs: set[int] = set()

    def index(i: int) -> list[int]:
        require(0 <= i < len(rays), "ray index out of range")
        return rays[i]

    for record in data["frames"]:
        a, b, c, weight = integers(record, 4, "frame")
        require(weight != 0, "zero frame coefficient")
        u, v, w = index(a), index(b), index(c)
        require(inner(u, v) == inner(u, w) == inner(v, w) == (0, 0),
                "frame is not pairwise Hermitian orthogonal")
        for i in (a, b, c):
            coefficients[i] += weight
        frame_weight += weight

    for record in data["real_values"]:
        i, sign, weight = integers(record, 3, "real value")
        require(weight != 0, "zero real-value coefficient")
        require(sign == exotic_sign(index(i)), "wrong exotic real-ray value")
        coefficients[i] += weight
        rhs += weight * sign
        real_weight += weight
        real_signs.add(sign)

    require(not any(coefficients.values()), "linear combination leaves a variable")
    require(type(data["contradiction_rhs"]) is int, "noninteger claimed right side")
    require(rhs == data["contradiction_rhs"] == 32, "wrong contradiction right side")
    require(3 * frame_weight + real_weight == 0, "constant terms fail to cancel")
    require(real_signs == {-1, 0, 1}, "missing prescribed exotic value")
    return {"rays": len(rays), "frames": len(data["frames"]),
            "real_values": len(data["real_values"]), "contradiction_rhs": rhs}


def self_test(data: dict) -> None:
    """Reject independently corrupted geometric and algebraic evidence."""
    cases = []
    changed = copy.deepcopy(data)
    changed["frames"][0][3] += 1
    cases.append(("frame coefficient", changed, "linear combination leaves a variable"))
    changed = copy.deepcopy(data)
    a, b, _, _ = changed["frames"][0]
    changed["rays"][a] = [x + y for x, y in zip(changed["rays"][a], changed["rays"][b])]
    cases.append(("nonorthogonal vector", changed, "frame is not pairwise Hermitian orthogonal"))
    changed = copy.deepcopy(data)
    changed["real_values"][0][1] += 1
    cases.append(("exotic value", changed, "wrong exotic real-ray value"))
    changed = copy.deepcopy(data)
    changed["rays"][0][0] = True
    cases.append(("Boolean coordinate", changed, "ray: expected integers"))
    for label, corrupted, expected in cases:
        try:
            verify(corrupted)
        except ValueError as error:
            require(str(error) == expected, f"{label}: unexpected rejection: {error}")
        else:
            raise ValueError(f"{label}: corrupted certificate was accepted")
        print(f"Negative control rejected: {label}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certificate", type=Path,
                        default=Path(__file__).parent / "data" / "fq_gleason_qi3_extension.json")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    data = json.loads(args.certificate.read_text(encoding="utf-8"))
    result = verify(data)
    print(json.dumps(result, sort_keys=True))
    print("Exact certificate: 0 = 32 for g=3*f-1. No signed extension of the prescribed exotic.")
    print("Not established: classification or existence of other nonquadratic Q(i)^3 frame functions.")
    if args.self_test:
        self_test(data)


if __name__ == "__main__":
    main()
