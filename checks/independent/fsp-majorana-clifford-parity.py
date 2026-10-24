"""Exact, bounded Jordan-Wigner audit; imports no repository code.

AuthorityEffect: None. This is not an all-mode proof, a construction from the
repository's primitives, or a physical parity-superselection theorem.
"""

from itertools import product
import json

import sympy as s


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def equal(left: s.MatrixBase, right: s.MatrixBase, label: str) -> None:
    require(left.shape == right.shape and left == right, label)


def tensor(factors: list[s.MatrixBase]) -> s.MatrixBase:
    result = s.eye(1)
    for factor in factors:
        result = s.kronecker_product(result, factor)
    return result


def family(modes: int, *, strings: bool = True) -> list[s.MatrixBase]:
    require(type(modes) is int and 0 <= modes <= 4, "mode bound: integer 0..4")
    identity, z = s.eye(2), s.diag(1, -1)
    lower = s.Matrix([[0, 1], [0, 0]])
    return [
        tensor([z if strings else identity] * j + [lower] + [identity] * (modes - j - 1))
        for j in range(modes)
    ]


def anticommutator(a: s.MatrixBase, b: s.MatrixBase) -> s.MatrixBase:
    return a * b + b * a


def matrix_product(factors: list[s.MatrixBase], dimension: int) -> s.MatrixBase:
    result = s.eye(dimension)
    for factor in factors:
        result *= factor
    return result


def audit(modes: int) -> dict:
    annihilators = family(modes)
    dimension = 2**modes
    identity, zero = s.eye(dimension), s.zeros(dimension)
    for j, a in enumerate(annihilators):
        for k, b in enumerate(annihilators):
            equal(anticommutator(a, b), zero, "CAR aa")
            equal(anticommutator(a, b.H), identity if j == k else zero, "CAR mixed")
    gammas = [g for a in annihilators for g in (a + a.H, -s.I * (a - a.H))]
    for j, g in enumerate(gammas):
        equal(g.H, g, "Majorana adjoint")
        for k, h in enumerate(gammas):
            equal(anticommutator(g, h), 2 * identity if j == k else zero, "Clifford relation")
    for j, a in enumerate(annihilators):
        even, odd = gammas[2*j:2*j + 2]
        equal((even + s.I * odd) / 2, a, "recover c")
        equal((even - s.I * odd) / 2, a.H, "recover c adjoint")
    number = [a.H * a for a in annihilators]
    local = [-s.I * gammas[2*j] * gammas[2*j + 1] for j in range(modes)]
    for n, q in zip(number, local):
        equal(n * n, n, "occupation idempotent")
        equal(q, identity - 2*n, "local parity sign")
        equal(q.H, q, "local parity adjoint")
        equal(q * q, identity, "local parity square")
    for q in local:
        for r in local:
            equal(q * r, r * q, "local parities commute")
    parity = matrix_product(local, dimension)
    occupations = list(product((0, 1), repeat=modes))
    count = sum(number, zero)
    equal(count, s.diag(*[sum(bits) for bits in occupations]), "number eigenvalues")
    expected = [(-1)**sum(bits) for bits in occupations]
    equal(parity, s.diag(*expected), "parity eigenvalues")
    equal(parity.H, parity, "global parity adjoint")
    equal(parity * parity, identity, "global parity square")
    for a in annihilators + gammas:
        equal(anticommutator(parity, a), zero, "parity anticommutes with odd generators")
    # Exact rank of every ordered Clifford monomial, only within this smaller bound.
    span_rank = None
    if modes <= 3:
        monomials = [matrix_product([g for bit, g in zip(mask, gammas) if bit], dimension)
                     for mask in product((0, 1), repeat=len(gammas))]
        columns = s.Matrix.hstack(*[m.reshape(dimension**2, 1) for m in monomials])
        span_rank = columns.rank()
        require(span_rank == dimension**2 == 4**modes, "bounded Clifford span")
    for matrix in annihilators + gammas + local + [parity, count]:
        for entry in matrix:
            s.QQ_I.from_sympy(entry)  # Refuse any non-Gaussian-rational certificate entry.
    return {"modes": modes, "dimension": dimension, "majoranas": len(gammas),
            "parity_diagonal": expected, "clifford_span_rank": span_rank}


def counterexamples() -> dict:
    a = family(1)[0]
    g0, g1 = a + a.H, -s.I*(a - a.H)
    parity = -s.I*g0*g1
    rho = s.ones(2) / 2
    equal(rho.H, rho, "rho Hermitian")
    equal(rho*rho, rho, "rho idempotent")
    require(s.trace(rho) == 1, "rho trace")
    # Gram factorization certifies positive semidefiniteness with rational entries.
    gram = s.Matrix([[1, 0], [1, 0]])
    equal(rho, gram * gram.H / 2, "rho positive Gram factorization")
    commutator = parity*rho - rho*parity
    equal(commutator, s.Matrix([[0, 1], [-1, 0]]), "non-superselected state")
    require(commutator != s.zeros(2), "CAR does not require parity superselection")
    bad = family(2, strings=False)
    mutations = {
        "wrong_parity_sign": s.I*g0*g1 != parity,
        "missing_majorana_phase": (a - a.H)**2 != s.eye(2),
        "missing_jordan_wigner_string": anticommutator(*bad) != s.zeros(4),
    }
    for label, detected in mutations.items():
        require(detected, "undetected mutation: " + label)
    refused = 0
    for bad_modes in (True, -1, 5, "2", s.Rational(1, 2)):
        try:
            family(bad_modes)
        except ValueError:
            refused += 1
        else:
            raise ValueError("invalid bound was accepted")
    return {"rho_trace": str(s.trace(rho)), "commutator_01": str(commutator[0, 1]),
            "mutations_rejected": list(mutations), "mutation_count": len(mutations),
            "invalid_bounds_refused": refused}


def main() -> None:
    print(json.dumps({"AuthorityEffect": "None", "field": "Q(i)",
                      "cases": [audit(n) for n in range(5)],
                      "counterexamples": counterexamples(),
                      "scope": "CAR/parity N=0..4; Clifford span N=0..3; no unbounded rank claim"},
                     sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
