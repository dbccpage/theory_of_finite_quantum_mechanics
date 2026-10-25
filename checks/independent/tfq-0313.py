"""Independent check for the narrowed TFQ-0313 fragment.

Carrier: (Z/4Z)^2. No repository imports. AuthorityEffect: None.
"""

from __future__ import annotations


def add(a: int, b: int) -> int:
    return (a + b) % 4


def sub(a: int, b: int) -> int:
    return (a - b) % 4


def mul(a: int, b: int) -> int:
    return (a * b) % 4


def mmul(p, q):
    a, b, c, d = p
    e, f, g, h = q
    return (
        add(mul(a, e), mul(b, g)),
        add(mul(a, f), mul(b, h)),
        add(mul(c, e), mul(d, g)),
        add(mul(c, f), mul(d, h)),
    )


def msub(p, q):
    return tuple(sub(x, y) for x, y in zip(p, q))


def apply(m, v):
    a, b, c, d = m
    x, y = v
    return (add(mul(a, x), mul(b, y)), add(mul(c, x), mul(d, y)))


def vadd(v, w):
    return (add(v[0], w[0]), add(v[1], w[1]))


def vsub(v, w):
    return (sub(v[0], w[0]), sub(v[1], w[1]))


def vsmul(s, v):
    return (mul(s, v[0]), mul(s, v[1]))


A = (0, 1, 0, 0)
B = (0, 0, 1, 0)
D = (1, 0, 0, 2)
E = (3, 0, 0, 1)
VECTORS = [(x, y) for x in range(4) for y in range(4)]
SCALARS = (0, 1, 2, 3)


def main() -> None:
    failures = 0
    checked = 0

    def expect(name: str, got, want) -> None:
        nonlocal failures, checked
        checked += 1
        if got != want:
            failures += 1
            print(f"FAIL {name}: got {got}, want {want}")

    expect("AB", mmul(A, B), (1, 0, 0, 0))
    expect("BA", mmul(B, A), (0, 0, 0, 1))
    expect("AB-BA", msub(mmul(A, B), mmul(B, A)), (1, 0, 0, 3))
    expect("AB-ne-BA", mmul(A, B) != mmul(B, A), True)
    expect("DE", mmul(D, E), (3, 0, 0, 2))
    expect("ED", mmul(E, D), (3, 0, 0, 2))
    expect("DE-eq-ED", mmul(D, E) == mmul(E, D), True)
    expect("char", (add(add(add(1, 1), 1), 1), 1 != 0), (0, True))
    expect("carrier-count", len(VECTORS), 16)
    expect("carrier-distinct", len(set(VECTORS)), 16)

    for s in SCALARS:
        checked += 1
        if A == (s, 0, 0, s):
            failures += 1
            print(f"FAIL A-not-scalar at {s}")

    e0 = (1, 0)
    left = apply(A, apply(B, e0))
    right = apply(B, apply(A, e0))
    expect("left-e0", left, (1, 0))
    expect("right-e0", right, (0, 0))
    expect("actions-differ", left != right, True)
    expect("commutator-e0", vsub(left, right), (1, 0))

    for v in VECTORS:
        expect(f"A-on-{v}", apply(A, v), (v[1], 0))
        expect(f"B-on-{v}", apply(B, v), (0, v[0]))
        expect(f"AB-comp-{v}", apply(mmul(A, B), v), apply(A, apply(B, v)))
        expect(f"BA-comp-{v}", apply(mmul(B, A), v), apply(B, apply(A, v)))
        for w in VECTORS:
            expect(f"A-add-{v}-{w}", apply(A, vadd(v, w)), vadd(apply(A, v), apply(A, w)))
            expect(f"B-add-{v}-{w}", apply(B, vadd(v, w)), vadd(apply(B, v), apply(B, w)))
        for s in SCALARS:
            expect(f"A-hom-{s}-{v}", apply(A, vsmul(s, v)), vsmul(s, apply(A, v)))
            expect(f"B-hom-{s}-{v}", apply(B, vsmul(s, v)), vsmul(s, apply(B, v)))

    if failures:
        print(f"checked {checked} conditions, {failures} failures")
        raise SystemExit(1)
    print(f"checked {checked} conditions, 0 failures")
    print("AB=[[1,0],[0,0]] BA=[[0,0],[0,1]] AB-BA=[[1,0],[0,3]]")
    print("diag(1,2)*diag(3,1)=diag(3,2) and the two diagonal matrices commute")
    print("carrier (Z/4Z)^2 has 16 vectors; 1+1+1+1=0 and 1!=0")


if __name__ == "__main__":
    main()
