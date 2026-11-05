"""Exact matrix audit of a declared finite-dimensional constraint and its kernel projector."""
from itertools import product
import sympy as sp


def main() -> None:
    constraint = sp.diag(0, 2, -1)
    projector = sp.diag(1, 0, 0)
    basis = [sp.eye(3)[:, i] for i in range(3)]
    if constraint.T != constraint or constraint.nullspace() != [basis[0]]:
        raise SystemExit("symmetry or kernel computation failed")
    if constraint.eigenvals() != {0: 1, 2: 1, -1: 1}:
        raise SystemExit("exact spectrum mismatch")
    if projector * projector != projector or constraint * projector != sp.zeros(3):
        raise SystemExit("kernel projector identities failed")
    if constraint * constraint == constraint:
        raise SystemExit("constraint unexpectedly idempotent")
    x, y, z, t = sp.symbols("x y z t")
    vector = sp.Matrix((x, y, z))
    kernel_vector = sp.Matrix((t, 0, 0))
    if ((vector - projector * vector).T * kernel_vector)[0] != 0:
        raise SystemExit("projection residual is not orthogonal to kernel")
    cases = 0
    for values in product(range(-2, 3), repeat=3):
        vector = sp.Matrix(values)
        in_kernel = constraint * vector == sp.zeros(3, 1)
        if in_kernel != (values[1] == 0 and values[2] == 0):
            raise SystemExit("kernel coordinate characterization failed")
        if (projector * vector == vector) != in_kernel:
            raise SystemExit("projector fixed-point characterization failed")
        cases += 1
    positive = (basis[1].T * constraint * basis[1])[0]
    negative = (basis[2].T * constraint * basis[2])[0]
    if positive != 2 or negative != -1:
        raise SystemExit("indefinite quadratic-form witnesses failed")
    print(f"vectors={cases} rank={constraint.rank()} kernel_dimension=1 "
          f"quadratic_values=({positive},{negative}) nonprojector=True failures=0")


if __name__ == "__main__":
    main()
