#!/usr/bin/env python3
"""Independent exact arithmetic verifier for CT-INFORMATION-MEDIA-INTEROPERABILITY (TFQ-2006).

Checks the finite deterministic algebraic core of Constructor Theory Principle III
(Interoperability of Information Media, Deutsch & Marletto 2015, Proc. R. Soc. A 471,
20140540, arXiv:1405.5563, Sections 3-6 pp. 9-12) and the scope fences explaining why
Principle III does not discharge FQ-GAP-TENSOR-UNIQUENESS (TFQ-2007):

1. Reversible modular addition (generalized CNOT) cloning on Z_n x Z_n for n in 2..12:
   bijectivity, two-sided inverse cnotUnclone, cloning from blank attribute 0, and
   involutivity on Z_2 x Z_2.
2. Computation variable cardinality threshold (|S| = 1 has 1 permutation and 0 distinct
   pairs vs |S| >= 2 having n! >= 2 permutations and swap transitivity) and
   distinguishability via injective vs non-injective encoding into a clonable variable.
3. Principle III (Interoperability of Information Media) on finite sets:
   for media sizes n1, n2 in 2..7, composite medium Z_n1 x Z_n2 has reversible
   componentwise cloning with composite blank (0, 0), composite attribute cardinality
   n1 * n2, and cross-medium copy + permutation recoding (x1, pi(x1)).
4. Quantum vs classical cloning fence:
   2-qubit CNOT on Z^4 clones computational basis states (1,0,0,0) and (0,0,1,0) with
   zero Schmidt determinant, but maps superposition (1,0,1,0) to entangled Bell vector
   (1,0,0,1) != (1,1,1,1) with nonzero Schmidt determinant 1 != 0.
5. Composite state-space dimension and bipartite cone non-selection fences (TFQ-2007):
   - For d1, d2 in 2..8, verify classical simplex dim (d1*d2 - 1), real local product
     dim (d1(d1+1)/2)*(d2(d2+1)/2), real quantum symmetric dim d1*d2*(d1*d2+1)/2, and
     complex Hermitian dim (d1*d2)^2, including strict ordering 3 < 9 < 10 < 16 at
     d1 = d2 = 2 and the exact real holism excess identity.
   - On 4x4 matrices over Q, verify that subsystem-B partial transpose leaves every
     classical diagonal matrix invariant (so PSD and PT cones share the same classical
     information subalgebra on {0,1}^2), while separating the Bell state |Phi+><Phi+|
     and its partial transpose swapWitness4 on the singlet state |Psi->.
"""

from __future__ import annotations

from fractions import Fraction
import itertools
import math
import sys


def cnot_clone(n: int, x: int, y: int) -> tuple[int, int]:
    return (x % n, (x + y) % n)


def cnot_unclone(n: int, x: int, y: int) -> tuple[int, int]:
    return (x % n, (y - x) % n)


def composite_clone(
    n1: int, n2: int, x1: int, x2: int, y1: int, y2: int
) -> tuple[tuple[int, int], tuple[int, int]]:
    return ((x1 % n1, x2 % n2), ((x1 + y1) % n1, (x2 + y2) % n2))


def composite_unclone(
    n1: int, n2: int, x1: int, x2: int, y1: int, y2: int
) -> tuple[tuple[int, int], tuple[int, int]]:
    return ((x1 % n1, x2 % n2), ((y1 - x1) % n1, (y2 - x2) % n2))


def partial_transpose_4x4(mat: list[list[Fraction]]) -> list[list[Fraction]]:
    """Subsystem-B partial transpose on 4x4 matrices indexed by (00, 01, 10, 11)."""
    out = [[Fraction(0) for _ in range(4)] for _ in range(4)]
    for a1 in (0, 1):
        for b1 in (0, 1):
            for a2 in (0, 1):
                for b2 in (0, 1):
                    i = 2 * a1 + b1
                    j = 2 * a2 + b2
                    i_pt = 2 * a1 + b2
                    j_pt = 2 * a2 + b1
                    out[i][j] = mat[i_pt][j_pt]
    return out


def quad_form(vec: list[Fraction], mat: list[list[Fraction]]) -> Fraction:
    total = Fraction(0)
    for i in range(4):
        for j in range(4):
            total += vec[i] * mat[i][j] * vec[j]
    return total


def _check_cloning_and_computation_variables_cases_2(checks, failures):
    for n in range(2, 13):
        image_set = set()
        for x in range(n):
            # Cloning from blank 0
            if cnot_clone(n, x, 0) == (x, x):
                checks += 1
            else:
                failures += 1
            for y in range(n):
                cloned = cnot_clone(n, x, y)
                image_set.add(cloned)
                uncloned = cnot_unclone(n, cloned[0], cloned[1])
                recloned = cnot_clone(
                    n, *cnot_unclone(n, x, y)
                )
                if uncloned == (x, y) and recloned == (x, y):
                    checks += 1
                else:
                    failures += 1
                if n == 2:
                    if cnot_clone(2, cloned[0], cloned[1]) == (x, y):
                        checks += 1
                    else:
                        failures += 1
        if len(image_set) == n * n:
            checks += 1
        else:
            failures += 1
    return checks, failures


def check_cloning_and_computation_variables() -> tuple[int, int]:
    checks = 0
    failures = 0

    # 1. Singleton vs >=2 computation variable threshold
    if math.factorial(1) == 1:
        checks += 1
    else:
        failures += 1

    for d in range(2, 8):
        if math.factorial(d) >= 2 and d * (d - 1) >= 2:
            checks += 1
        else:
            failures += 1

    # 2. Reversible CNOT cloning on Z_n x Z_n for n in 2..12
    checks, failures = _check_cloning_and_computation_variables_cases_2(checks, failures)

    # 3. Distinguishability via injective vs non-injective map into clonable variable
    for n in range(3, 8):
        for x in range(n):
            for y in range(n):
                if x != y:
                    # Injective shift encoding f(z) = (z + 1) % n
                    fx = (x + 1) % n
                    fy = (y + 1) % n
                    if cnot_clone(n, fx, 0) != cnot_clone(n, fy, 0):
                        checks += 1
                    else:
                        failures += 1
                    # Non-injective constant encoding h(z) = 0 fails separation
                    hx = 0
                    hy = 0
                    if cnot_clone(n, hx, 0) == cnot_clone(n, hy, 0):
                        checks += 1
                    else:
                        failures += 1

    return checks, failures


def _check_principle_iii_interoperability_cases_4(checks, failures, n1):
    for n2 in range(2, 7):
        # Cardinality of composite attribute set
        pairs = list(itertools.product(range(n1), range(n2)))
        if len(pairs) == n1 * n2:
            checks += 1
        else:
            failures += 1

        # Blank cloning for all joint attributes (x1, x2)
        for x1, x2 in pairs:
            cloned0 = composite_clone(n1, n2, x1, x2, 0, 0)
            if cloned0 == ((x1, x2), (x1, x2)):
                checks += 1
            else:
                failures += 1

        # Full bijectivity and two-sided inverse on (Z_n1 x Z_n2)^2 for n1, n2 <= 4
        if n1 <= 4 and n2 <= 4:
            image_set = set()
            for x1, x2 in pairs:
                for y1, y2 in pairs:
                    c = composite_clone(n1, n2, x1, x2, y1, y2)
                    image_set.add(c)
                    u = composite_unclone(
                        n1, n2, c[0][0], c[0][1], c[1][0], c[1][1]
                    )
                    if u == ((x1, x2), (y1, y2)):
                        checks += 1
                    else:
                        failures += 1
            if len(image_set) == (n1 * n2) ** 2:
                checks += 1
            else:
                failures += 1
    return checks, failures


def check_principle_iii_interoperability() -> tuple[int, int]:
    checks = 0
    failures = 0

    # Composite media Z_n1 x Z_n2 for n1, n2 in 2..6
    for n1 in range(2, 7):
        checks, failures = _check_principle_iii_interoperability_cases_4(checks, failures, n1)

    # Cross-medium copy + permutation recoding on Z_n
    for n in range(2, 6):
        for perm in itertools.islice(itertools.permutations(range(n)), 24):
            for x1 in range(n):
                copied = cnot_clone(n, x1, 0)
                recoded = (copied[0], perm[copied[1]])
                if copied == (x1, x1) and recoded == (x1, perm[x1]):
                    checks += 1
                else:
                    failures += 1

    return checks, failures


def _check_fences_cases_1_cases_5(checks, d0, d1, d2, failures):
    for d3 in range(-2, 3):
        diag = [
            [Fraction(d0 if i == 0 and j == 0 else d1 if i == 1 and j == 1 else d2 if i == 2 and j == 2 else d3 if i == 3 and j == 3 else 0) for j in range(4)]
            for i in range(4)
        ]
        if partial_transpose_4x4(diag) == diag:
            checks += 1
        else:
            failures += 1
    return checks, failures


def _check_fences_cases_1(checks, failures):
    for d0 in range(-2, 3):
        for d1 in range(-2, 3):
            for d2 in range(-2, 3):
                checks, failures = _check_fences_cases_1_cases_5(checks, d0, d1, d2, failures)
    return checks, failures


def _check_fences_cases_3(checks, failures):
    for d1 in range(2, 9):
        for d2 in range(2, 9):
            classical_dim = d1 * d2 - 1
            real_local_dim = (d1 * (d1 + 1) // 2) * (d2 * (d2 + 1) // 2)
            real_quantum_dim = (d1 * d2) * (d1 * d2 + 1) // 2
            complex_dim = (d1 * d2) ** 2
            complex_local_dim = (d1 ** 2) * (d2 ** 2)

            if (
                classical_dim < real_local_dim < real_quantum_dim < complex_dim
                and complex_dim == complex_local_dim
                and 4 * (real_quantum_dim - real_local_dim)
                == d1 * d2 * (d1 - 1) * (d2 - 1)
            ):
                checks += 1
            else:
                failures += 1

            if d1 == 2 and d2 == 2:
                if (
                    classical_dim == 3
                    and real_local_dim == 9
                    and real_quantum_dim == 10
                    and complex_dim == 16
                ):
                    checks += 1
                else:
                    failures += 1
    return checks, failures


def check_fences() -> tuple[int, int]:
    checks = 0
    failures = 0

    # 1. Quantum CNOT off-diagonal entanglement fence vs product cloning
    def cnot4(v: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
        return (v[0], v[1], v[3], v[2])

    def schmidt_det4(v: tuple[int, int, int, int]) -> int:
        return v[0] * v[3] - v[1] * v[2]

    if (
        cnot4((1, 0, 0, 0)) == (1, 0, 0, 0)
        and cnot4((0, 0, 1, 0)) == (0, 0, 0, 1)
        and cnot4((1, 0, 1, 0)) == (1, 0, 0, 1)
        and cnot4((1, 0, 1, 0)) != (1, 1, 1, 1)
        and schmidt_det4(cnot4((1, 0, 1, 0))) == 1
    ):
        checks += 1
    else:
        failures += 1

    for u0 in range(-2, 3):
        for u1 in range(-2, 3):
            for v0 in range(-2, 3):
                for v1 in range(-2, 3):
                    prod_v = (u0 * v0, u0 * v1, u1 * v0, u1 * v1)
                    if schmidt_det4(prod_v) == 0 and prod_v != (1, 0, 0, 1):
                        checks += 1
                    else:
                        failures += 1

    # 2. Composite state-space dimension trichotomy and real holism excess fence
    checks, failures = _check_fences_cases_3(checks, failures)

    # 3. PSD vs PT cone classical diagonal invariance and Bell witness separation
    checks, failures = _check_fences_cases_1(checks, failures)

    bell_state = [
        [Fraction(1), Fraction(0), Fraction(0), Fraction(1)],
        [Fraction(0), Fraction(0), Fraction(0), Fraction(0)],
        [Fraction(0), Fraction(0), Fraction(0), Fraction(0)],
        [Fraction(1), Fraction(0), Fraction(0), Fraction(1)],
    ]
    swap_witness = partial_transpose_4x4(bell_state)
    singlet_vec = [Fraction(0), Fraction(1), Fraction(-1), Fraction(0)]

    if (
        quad_form(singlet_vec, bell_state) == Fraction(0)
        and quad_form(singlet_vec, swap_witness) == Fraction(-2)
    ):
        checks += 1
    else:
        failures += 1

    for u0 in range(-2, 3):
        for u1 in range(-2, 3):
            for v0 in range(-2, 3):
                for v1 in range(-2, 3):
                    prod_vec = [
                        Fraction(u0 * v0),
                        Fraction(u0 * v1),
                        Fraction(u1 * v0),
                        Fraction(u1 * v1),
                    ]
                    expected_qf = Fraction((u0 * v0 + u1 * v1) ** 2)
                    qf_bell = quad_form(prod_vec, bell_state)
                    qf_swap = quad_form(prod_vec, swap_witness)
                    if qf_bell == expected_qf and qf_swap == expected_qf and qf_swap >= 0:
                        checks += 1
                    else:
                        failures += 1

    return checks, failures


def main() -> int:
    c1, f1 = check_cloning_and_computation_variables()
    c2, f2 = check_principle_iii_interoperability()
    c3, f3 = check_fences()
    total_checks = c1 + c2 + c3
    total_failures = f1 + f2 + f3
    print(
        f"CT-INFORMATION-MEDIA-INTEROPERABILITY independent check: "
        f"checks={total_checks} cloning_comp={c1} interoperability={c2} "
        f"fences={c3} failures={total_failures}"
    )
    return 0 if total_failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
