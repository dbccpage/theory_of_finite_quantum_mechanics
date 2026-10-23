"""Independent check for DFM-GRIBOV-CONTINUUM-FENCE.

Three-by-three rational matrices, two generator squares, and the traces
Tr(Omega1 H^2) are recomputed with fractions.Fraction. This file imports
no repository code.
"""

from fractions import Fraction


def exact(value):
    if isinstance(value, Fraction):
        return value
    if type(value) is int:
        return Fraction(value)
    raise TypeError("expected an int or Fraction (not bool, float, or text)")


def mat(rows):
    return tuple(tuple(exact(x) for x in row) for row in rows)


def mul(a, b):
    return tuple(
        tuple(sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3))
        for i in range(3)
    )


def trace(a):
    return a[0][0] + a[1][1] + a[2][2]


def diag(x, y, z):
    return mat(((x, 0, 0), (0, y, 0), (0, 0, z)))


def main():
    eye = diag(1, 1, 1)
    omega1 = diag(1, -1, -1)
    h23 = mat(((0, 0, 0), (0, 0, 1), (0, 1, 0)))
    h12 = mat(((0, 1, 0), (1, 0, 0), (0, 0, 0)))
    if mul(h23, h23) != diag(0, 1, 1):
        raise SystemExit("H23 square")
    if mul(h12, h12) != diag(1, 1, 0):
        raise SystemExit("H12 square")
    if mul(omega1, omega1) != eye:
        raise SystemExit("omega1 square")
    if omega1[0][0] * omega1[1][1] * omega1[2][2] != 1:
        raise SystemExit("diagonal product")
    if trace(eye) != 3 or trace(omega1) != -1:
        raise SystemExit("traces")
    q_id = trace(mul(eye, mul(h23, h23)))
    q23 = trace(mul(omega1, mul(h23, h23)))
    q12 = trace(mul(omega1, mul(h12, h12)))
    if (q_id, q23, q12) != (2, -2, 0):
        raise SystemExit(f"forms {q_id} {q23} {q12}")
    if q23 == q12:
        raise SystemExit("forms should differ")
    print("H23^2 = diag(0,1,1); H12^2 = diag(1,1,0)")
    print("Tr(I) = 3; Tr(Omega1) = -1; Omega1^2 = I; diagonal product 1")
    print("Tr(I H23^2) = 2; Tr(Omega1 H23^2) = -2; Tr(Omega1 H12^2) = 0")
    print("checked: generator squares, involution, two quadratic forms")


if __name__ == "__main__":
    main()
