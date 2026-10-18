"""QM-209 finite map: noncommuting contexts and the parity obstruction.

AuthorityEffect: None.

What the L1 shadow provides: one diagonal, and diagonal operators commute. The import
named QM-209 is a second context in which the first is not diagonal. This control
computes exactly over Q(i) and Q(zeta_12): the Peres-Mermin sign table from Pauli
products, the F_2 cokernel in which the value-assignment obstruction lives, the Weyl
commutator census (which pairs of contexts carry a nontrivial central holonomy), the
conjugation invariance of that holonomy, and the finite statement that a diagonal
phase cochain supplies no second context. Nothing here produces a second context from
weights.
"""

from __future__ import annotations

from typing import Any, Sequence

from ..domain.cyclotomic_tower import CyclotomicElement
from . import holonomy_bridge as hbc

Matrix = hbc.Matrix


class ContextControlRefusal(ValueError):
    """Typed refusal for malformed context-control inputs."""


def f2_eliminate(rows: Sequence[Sequence[int]], rhs: Sequence[int]) -> dict[str, Any]:
    """Gaussian elimination over F_2 on the augmented system; returns rank and a solution or None."""
    m = [list(r) + [b] for r, b in zip(rows, rhs)]
    if any(any(x not in (0, 1) for x in r) for r in m):
        raise ContextControlRefusal("F_2 systems take entries 0 and 1 only")
    ncols = len(rows[0])
    pivots: list[int] = []
    row = 0
    for col in range(ncols):
        pivot = next((r for r in range(row, len(m)) if m[r][col] == 1), None)
        if pivot is None:
            continue
        m[row], m[pivot] = m[pivot], m[row]
        for r in range(len(m)):
            if r != row and m[r][col] == 1:
                m[r] = [(x + y) % 2 for x, y in zip(m[r], m[row])]
        pivots.append(col)
        row += 1
    consistent = all(any(r[:-1]) or r[-1] == 0 for r in m)
    solution: list[int] | None = None
    if consistent:
        solution = [0] * ncols
        for r, col in zip(m, pivots):
            solution[col] = r[-1]
    return {"rank": len(pivots), "consistent": consistent, "solution": solution}


def f2_apply(rows: Sequence[Sequence[int]], v: Sequence[int]) -> list[int]:
    return [sum(a * b for a, b in zip(r, v)) % 2 for r in rows]


PERES_MERMIN_CONTEXTS: tuple[tuple[str, ...], ...] = (
    ("XI", "IX", "XX"),
    ("IZ", "ZI", "ZZ"),
    ("XZ", "ZX", "YY"),
    ("XI", "IZ", "XZ"),
    ("IX", "ZI", "ZX"),
    ("XX", "ZZ", "YY"),
)


def context_sign(paulis: dict[str, Matrix], context: Sequence[str]) -> int:
    """The product of a commuting context is +I or -I; return +1 or -1, refuse otherwise."""
    prod = paulis[context[0]]
    for name in context[1:]:
        prod = hbc.matmul(prod, paulis[name])
    c = hbc.scalar_multiple_of_identity(prod)
    if c == 1:
        return 1
    if c == -1:
        return -1
    raise ContextControlRefusal("a context product that is not +I or -I")


def commuting_context(paulis: dict[str, Matrix], context: Sequence[str]) -> bool:
    return all(
        hbc.mat_eq(hbc.matmul(paulis[a], paulis[b]), hbc.matmul(paulis[b], paulis[a]))
        for a in context
        for b in context
    )


def peres_mermin_cokernel(conductor: int) -> dict[str, Any]:
    """The value-assignment obstruction as a class in the F_2 cokernel of the context incidence.

    Contexts are vertices, observables are edges (each observable lies in exactly one row
    and one column), so the incidence matrix is the vertex-edge matrix of K_{3,3} over F_2.
    A deterministic assignment v exists exactly when the sign vector s is in its image;
    the cokernel is H_0(K_{3,3}; F_2) = F_2 and the class of s is its total parity.
    """
    paulis = hbc.pauli_2qubit(conductor)
    observables = sorted({o for ctx in PERES_MERMIN_CONTEXTS for o in ctx})
    signs = [context_sign(paulis, ctx) for ctx in PERES_MERMIN_CONTEXTS]
    rows = [[1 if o in ctx else 0 for o in observables] for ctx in PERES_MERMIN_CONTEXTS]
    s = [0 if sg == 1 else 1 for sg in signs]
    system = f2_eliminate(rows, s)
    even = list(s)
    even[0] ^= 1
    control = f2_eliminate(rows, even)
    column_weights = [sum(r[j] for r in rows) for j in range(len(observables))]
    return {
        "observables": observables,
        "contexts": [list(c) for c in PERES_MERMIN_CONTEXTS],
        "all_contexts_commute": all(commuting_context(paulis, c) for c in PERES_MERMIN_CONTEXTS),
        "context_signs": signs,
        "sign_product": 1 if sum(s) % 2 == 0 else -1,
        "incidence_rank_f2": system["rank"],
        "cokernel_dimension": len(rows) - system["rank"],
        "every_observable_in_two_contexts": all(w == 2 for w in column_weights),
        "assignment_exists": system["consistent"],
        "obstruction_class_total_parity": sum(s) % 2,
        "even_control_assignment_exists": control["consistent"],
        "even_control_solution_checks": control["solution"] is not None
        and f2_apply(rows, control["solution"]) == even,
    }


def mat_pow(a: Matrix, k: int) -> Matrix:
    out = hbc.identity(len(a), a[0][0].conductor)
    for _ in range(k):
        out = hbc.matmul(out, a)
    return out


def weyl_commutator_census(d: int, conductor: int) -> dict[str, Any]:
    """Central holonomy of (X^a, Z^b) for all a, b in Z/d: trivial exactly when d | ab."""
    x = hbc.weyl_shift(d, conductor)
    zc = hbc.weyl_clock(d, conductor)
    table: list[list[int]] = []
    trivial_iff_divisible = True
    for a in range(d):
        row = []
        for b in range(d):
            hol = hbc.commutator_holonomy(mat_pow(x, a), mat_pow(zc, b))
            row.append(hbc.root_exponent(hol))
            trivial_iff_divisible &= hol.is_one() == ((a * b) % d == 0)
        table.append(row)
    return {
        "dimension": d,
        "holonomy_exponents_mod_conductor": table,
        "trivial_exactly_when_d_divides_ab": trivial_iff_divisible,
        "values_are_dth_roots": all((e * d) % conductor == 0 for row in table for e in row),
    }


def conjugation_invariance(conductor: int) -> dict[str, Any]:
    """The commutator holonomy is unchanged by any unitary relabelling of both contexts."""
    d = 4
    x = hbc.weyl_shift(d, conductor)
    zc = hbc.weyl_clock(d, conductor)
    base = hbc.commutator_holonomy(x, zc)
    frames = {
        "fourier": hbc.fourier_matrix_d4(conductor),
        "diagonal_phases": [
            [
                hbc.root_of_unity(conductor, (3 * j + 1) % conductor)
                if j == k
                else CyclotomicElement.rational(0, conductor)
                for k in range(d)
            ]
            for j in range(d)
        ],
    }
    results = {}
    for name, u in frames.items():
        if not hbc.is_unitary(u):
            raise ContextControlRefusal(f"frame {name} is not unitary")
        conj = lambda m: hbc.matmul(hbc.matmul(u, m), hbc.dagger(u))  # noqa: E731
        results[name] = hbc.commutator_holonomy(conj(x), conj(zc)) == base
    diag = frames["diagonal_phases"]
    return {
        "base_holonomy_exponent": hbc.root_exponent(base),
        "invariant_under": results,
        "diagonal_pair_has_trivial_holonomy": hbc.commutator_holonomy(diag, zc).is_one(),
        "commuting_powers_have_trivial_holonomy": hbc.commutator_holonomy(
            zc, mat_pow(zc, 2)
        ).is_one(),
    }


def residual_import_ledger() -> list[dict[str, str]]:
    return [
        {
            "layer": "finite invariant",
            "status": "COMPUTED",
            "statement": "Peres-Mermin: six commuting contexts with sign product -1; the "
            "deterministic-assignment system over F_2 is inconsistent, its cokernel is "
            "H_0(K_{3,3}; F_2) = F_2 and the class is the total parity 1. Weyl pairs: the "
            "central holonomy of (X^a, Z^b) is a d-th root of unity, trivial exactly when "
            "d | ab, and invariant under conjugation of both contexts.",
        },
        {
            "layer": "completion",
            "status": "IMPORTED",
            "statement": "Density of the unitaries with entries in the union of Q(zeta_N) in "
            "U(d) uses the topology of U(d); in infinite dimension the norm closure of B(H) "
            "is a further import. In finite dimension everything above is algebraic.",
        },
        {
            "layer": "residual import",
            "status": "IMPORTED",
            "statement": "A second context. A diagonal phase cochain commutes with the "
            "diagonal and so supplies none (computed); nothing in the weights or the fiber "
            "produces a non-diagonal frame.",
        },
    ]


def evaluate_context_parity_control(conductor: int = 12) -> dict[str, Any]:
    """Run the QM-209 control exactly and return JSON-serializable results."""
    if conductor % 12 != 0:
        raise ContextControlRefusal("the control needs 12 | conductor")
    return {
        "conductor": conductor,
        "peres_mermin": peres_mermin_cokernel(conductor),
        "weyl_census": {d: weyl_commutator_census(d, conductor) for d in (3, 4)},
        "conjugation_invariance": conjugation_invariance(conductor),
        "residual_import_ledger": residual_import_ledger(),
    }
