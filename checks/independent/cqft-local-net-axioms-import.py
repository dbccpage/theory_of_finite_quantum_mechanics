"""Independent check for CQFT-LOCAL-NET-AXIOMS-IMPORT.

Pair counts on one four-point order, and products of four integer matrices,
are recomputed with plain integers. This file imports no repository code.
"""


def rel(i, j):
    return (i == 0 and j == 2) or (i == 1 and j == 2) or (i == 1 and j == 3)


def spacelike(i, j):
    return i != j and not rel(i, j) and not rel(j, i)


def mm(x, y):
    a, b, c, d = x
    e, f, g, h = y
    return (a * e + b * g, a * f + b * h, c * e + d * g, c * f + d * h)


def add2(x, y):
    return tuple(p + q for p, q in zip(x, y))


def trp(x):
    a, b, c, d = x
    return (a, c, b, d)


def det2(x):
    a, b, c, d = x
    return a * d - b * c


def mm4(p, q):
    out = []
    for i in range(4):
        row = []
        for j in range(4):
            row.append(sum(p[i][k] * q[k][j] for k in range(4)))
        out.append(row)
    return out


def flat(m):
    return tuple(v for row in m for v in row)


def main():
    points = range(4)
    if any(rel(i, i) for i in points):
        raise SystemExit("reflexive relation")
    for x in points:
        for y in points:
            for z in points:
                if rel(x, y) and rel(y, z) and not rel(x, z):
                    raise SystemExit(f"transitivity {x} {y} {z}")
    relations = [(i, j) for i in points for j in points if rel(i, j)]
    unordered = [(i, j) for i in points for j in points if i < j and spacelike(i, j)]
    if relations != [(0, 2), (1, 2), (1, 3)]:
        raise SystemExit(f"relations {relations}")
    if unordered != [(0, 1), (0, 3), (2, 3)]:
        raise SystemExit(f"spacelike {unordered}")
    if not spacelike(1, 0) or spacelike(1, 3):
        raise SystemExit("spacelike flags")

    ident = (1, 0, 0, 1)
    xmat = (0, 1, 1, 0)
    zmat = (1, 0, 0, -1)
    amat = (1, 2, 3, 4)
    bmat = (5, 6, 7, 8)
    for mat in (amat, bmat, xmat, zmat):
        if mm(ident, mat) != mat or mm(mat, ident) != mat:
            raise SystemExit(f"unit {mat}")
    xz = mm(xmat, zmat)
    zx = mm(zmat, xmat)
    if xz != (0, -1, 1, 0) or zx != (0, 1, -1, 0):
        raise SystemExit(f"pauli {xz} {zx}")
    if add2(xz, zx) != (0, 0, 0, 0) or xz == zx:
        raise SystemExit("anticommutator")
    ab = mm(amat, bmat)
    if trp(trp(amat)) != amat or trp(ab) != mm(trp(bmat), trp(amat)):
        raise SystemExit("transpose")
    dets = (det2(amat), det2(bmat), det2(xmat), det2(zmat))
    if dets != (-2, -2, -1, -1):
        raise SystemExit(f"dets {dets}")

    eye = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
    # Kronecker by blocks, written out so the index formula above is not the only route.
    def kron_blocks(p, q):
        a, b, c, d = p
        e, f, g, h = q
        return [
            [a * e, a * f, b * e, b * f],
            [a * g, a * h, b * g, b * h],
            [c * e, c * f, d * e, d * f],
            [c * g, c * h, d * g, d * h],
        ]

    left = kron_blocks(amat, ident)
    right = kron_blocks(ident, bmat)
    both = kron_blocks(amat, bmat)
    if mm4(left, right) != both or mm4(right, left) != both:
        raise SystemExit("disjoint-site products differ")
    total = sum(sum(row) for row in both)
    if total != 260:
        raise SystemExit(f"sum {total}")
    same_l = mm4(kron_blocks(xmat, ident), kron_blocks(zmat, ident))
    same_r = mm4(kron_blocks(zmat, ident), kron_blocks(xmat, ident))
    if same_l == same_r or same_l[0][2] != -1 or same_r[0][2] != 1:
        raise SystemExit(f"same-site {same_l[0][2]} {same_r[0][2]}")
    if flat(both)[0] != 5 or flat(both)[-1] != 32:
        raise SystemExit("corner entries")
    if eye[0][0] != 1:
        raise SystemExit("identity sentinel")
    print("four-point order: 3 relations (0,2), (1,2), (1,3); 3 spacelike pairs (0,1), (0,3), (2,3)")
    print("disjoint-site products equal A tensor B; entry sum 260")
    print("same-site (0,2) entries -1 and 1; XZ+ZX is zero; dets -2, -2, -1, -1")
    print("checked: pair counts, unit, transpose, disjoint-site commutation, same-site inequality")


if __name__ == "__main__":
    main()
