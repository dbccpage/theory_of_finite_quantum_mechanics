"""Independent check for DFM-RELATIONAL-TIME-FENCE.

The order-4 step, four clock blocks, and one rational vector are recomputed
with fractions.Fraction. This file imports no repository code.
"""

from fractions import Fraction


def mat(rows):
    return tuple(tuple(Fraction(x) for x in row) for row in rows)


def mul(a, b):
    return tuple(
        tuple(sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0])))
        for i in range(len(a))
    )


def transp(a):
    return tuple(tuple(a[j][i] for j in range(len(a))) for i in range(len(a[0])))


def apply(a, v):
    return tuple(sum(a[i][k] * v[k] for k in range(len(v))) for i in range(len(a)))


def main():
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
    if apply(u1, psi) == psi or apply(u2, psi) == psi:
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


if __name__ == "__main__":
    main()
