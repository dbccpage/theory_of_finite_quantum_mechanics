"""Independent check for DFM-RELATIONAL-TIME-FENCE.

The order-4 step, four clock blocks, and one rational vector are recomputed
with fractions.Fraction. This file imports no repository code.
"""

from fractions import Fraction
from itertools import permutations, product
from collections.abc import Sequence

Matrix = tuple[tuple[Fraction, ...], ...]
Perm = tuple[int, ...]


def mat(rows: Sequence[Sequence[int | Fraction]]) -> Matrix:
    return tuple(tuple(Fraction(x) for x in row) for row in rows)


def mul(a: Matrix, b: Matrix) -> Matrix:
    return tuple(
        tuple(sum((a[i][k] * b[k][j] for k in range(len(b))), Fraction(0)) for j in range(len(b[0])))
        for i in range(len(a))
    )


def transp(a: Matrix) -> Matrix:
    return tuple(tuple(a[j][i] for j in range(len(a))) for i in range(len(a[0])))


def apply(a: Matrix, v: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    return tuple(sum((a[i][k] * v[k] for k in range(len(v))), Fraction(0)) for i in range(len(a)))


def matrix_regression() -> None:
    eye = mat(((1, 0), (0, 1)))
    minus = mat(((-1, 0), (0, -1)))
    step = mat(((0, -1), (1, 0)))
    u0, u1 = eye, step
    u2 = mul(u1, step)
    u3 = mul(u2, step)
    u4 = mul(u3, step)
    if u2 != minus or u4 != eye or mul(transp(step), step) != eye:
        raise SystemExit("order")
    powers = (u0, u1, u2, u3, u4)
    for t in range(4):
        block = mul(mul(transp(powers[t + 1]), step), powers[t])
        if block != eye:
            raise SystemExit(f"block {t}")
    psi = (Fraction(3, 5), Fraction(4, 5))
    if psi[0] * psi[0] + psi[1] * psi[1] != 1:
        raise SystemExit("norm")
    for t in range(4):
        back = apply(transp(powers[t]), apply(powers[t], psi))
        if back != psi:
            raise SystemExit(f"recover {t} {back}")
    if apply(u1, psi)[0] == psi[0] or apply(u2, psi)[0] == psi[0]:
        raise SystemExit("order on psi")
    # Package the same blocks as an 8 by 8 product. Lean does not build this matrix.
    z = Fraction(0)
    w = [[z for _ in range(8)] for _ in range(8)]
    sc = [[z for _ in range(8)] for _ in range(8)]
    d = [[z for _ in range(8)] for _ in range(8)]
    dag = [[z for _ in range(8)] for _ in range(8)]
    for t in range(4):
        nxt = (t + 1) % 4
        for r in range(2):
            for c in range(2):
                w[2 * nxt + r][2 * t + c] = step[r][c]
                sc[2 * nxt + r][2 * t + c] = eye[r][c]
                d[2 * t + r][2 * t + c] = powers[t][r][c]
                dag[2 * t + r][2 * t + c] = transp(powers[t])[r][c]
    packed = mul(tuple(tuple(row) for row in dag), mul(tuple(tuple(row) for row in w), tuple(tuple(row) for row in d)))
    if packed != tuple(tuple(row) for row in sc):
        raise SystemExit("packed product")
    print("U^2 = -I; U^4 = I; U^T U = I")
    print("four blocks equal I; psi norm 1; four transports recover psi")
    print("U psi and U^2 psi differ from psi; packed 8x8 product matches the clock shift")
    print("checked: order-4 step, four blocks, one vector, packaged product")



def compose(a: Perm, b: Perm) -> Perm:
    return tuple(a[x] for x in b)


def inverse(a: Perm) -> Perm:
    return tuple(a.index(x) for x in range(len(a)))


def frames(links: tuple[Perm, ...]) -> tuple[Perm, ...]:
    out: list[Perm] = [(0, 1, 2)]
    for link in links:
        out.append(compose(link, out[-1]))
    return tuple(out)


def check(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def closure(links: tuple[Perm, ...]) -> str:
    if not links:
        return "emptyPeriod"
    if frames(links)[-1] != (0, 1, 2):
        return "nontrivialHolonomy"
    return "ok"


def gauge_regression(links: tuple[Perm, ...], g: tuple[Perm, ...]) -> None:
    f = frames(links)
    changed = tuple(compose(inverse(g[t + 1]), compose(u, g[t]))
                    for t, u in enumerate(links))
    changed_frames = frames(changed)
    for t in range(len(f)):
        expected = compose(inverse(g[t]), compose(f[t], g[0]))
        check(changed_frames[t] == expected, "frame covariance")
    for initial in range(3):
        history = tuple(a[initial] for a in f)
        coords = tuple(inverse(g[t])[x] for t, x in enumerate(history))
        check(all(g[t][x] == history[t] for t, x in enumerate(coords)), "history inverse")
        check(all(coords[t + 1] == u[coords[t]] for t, u in enumerate(changed)),
              "evolution covariance")
        stationary = tuple(inverse(f[t])[x] for t, x in enumerate(history))
        check(all(x == initial for x in stationary), "stationary coordinates")


def cycle_regression(links: tuple[Perm, ...]) -> None:
    f = frames(links)
    eye = (0, 1, 2)
    n = len(links)
    # Direct point application is the independent oracle for product order.
    for initial in range(3):
        x = initial
        for t, u in enumerate(links):
            x = u[x]
            check(f[t + 1][initial] == x, "chronological transport")
    for t, u in enumerate(links):
        block = compose(inverse(f[(t + 1) % n]), compose(u, f[t]))
        check(block == (eye if t + 1 < n else f[-1]), "seam normal form")
    check((closure(links) == "ok") == (f[-1] == eye), "closure decision")
    # Exhaust all possible initial frames; edge cancellation forces each later frame.
    for g0 in permutations(range(3)):
        g = tuple(compose(a, g0) for a in f)
        check((g[-1] == g[0]) == (f[-1] == eye), "periodic obstruction iff")
        gauge_regression(links, g)
    # Independently chosen nonstationary, nonperiodic frames exercise endpoint terms.
    ps = tuple(permutations(range(3)))
    for offset in range(6):
        gauge_regression(links, tuple(ps[(offset + t * 2) % 6] for t in range(n + 1)))


def fault_regression() -> None:
    a, b, eye = (1, 0, 2), (0, 2, 1), (0, 1, 2)
    # Four selected semantic mutants; each must disagree with the direct oracle.
    actual = tuple(b[a[x]] for x in range(3))
    check(compose(a, b) != actual, "mutant survived: reversed link order")
    check(eye != frames((a,))[-1], "mutant survived: erase closing seam")
    u = compose(b, a)
    check(compose(u, u) != eye, "mutant survived: omit inverse")
    check(closure(()) != "ok", "mutant survived: accept zero period")
    print("four incorrect candidate expressions rejected; witness checks, not a source mutation campaign")


def main() -> None:
    matrix_regression()
    ps = tuple(permutations(range(3)))
    check(closure(()) == "emptyPeriod", "zero period refusal")
    count = 0
    closed = 0
    for n in range(1, 5):
        for links in product(ps, repeat=n):
            cycle_regression(links)
            count += 1
            closed += closure(links) == "ok"
    # Constant-step specialization, including period zero as an algebraic boundary.
    for u in ps:
        for n in range(9):
            expected = tuple(range(3))
            for _ in range(n):
                expected = tuple(u[x] for x in expected)
            check(frames((u,) * n)[-1] == expected, "constant-step power")
    fault_regression()
    print(f"S3 schedules={count}; closed={closed}; nonclosing={count-closed}; zero-period rejected")
    print("checked: all seams, closure iff, 12 gauges and 3 histories per schedule, 54 powers")
    print("finite regression only; the arbitrary-group and arbitrary-period claims are Lean theorems")


if __name__ == "__main__":
    main()
