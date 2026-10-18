"""Campaign C500 Block 03: Finite Heisenberg Representation Classification.

Computes the odd-prime group law and exact monomial representation actions.
The dimension census is a declared finite Stone-von Neumann input; the
sum-of-squares identity does not establish classification or uniqueness.
Commutant, intertwiner, and general representation classification proofs remain open here.

AuthorityEffect: None.
Citation: sealed-derivation-v1 (3100c4e).
"""

from __future__ import annotations

import json
from functools import lru_cache
from math import isqrt
from typing import Any, Dict, List, Tuple


@lru_cache(maxsize=128)
def _require_odd_prime(p: int) -> None:
    if type(p) is not int or p < 3 or p % 2 == 0 or any(
        p % k == 0 for k in range(3, isqrt(p) + 1, 2)
    ):
        raise ValueError("The symmetric cocycle requires an odd prime modulus.")


def _require_element(g: Tuple[int, int, int], p: int) -> None:
    if len(g) != 3 or any(type(x) is not int or not 0 <= x < p for x in g):
        raise ValueError("Group coordinates must be integer representatives in [0, p).")


def heisenberg_group_elements(p: int) -> List[Tuple[int, int, int]]:
    """Return all p^3 elements (q, p', z) in H(F_p)."""
    _require_odd_prime(p)
    elements = []
    for q in range(p):
        for p_prime in range(p):
            for z in range(p):
                elements.append((q, p_prime, z))
    return elements


def heisenberg_group_multiply(
    g1: Tuple[int, int, int],
    g2: Tuple[int, int, int],
    p: int,
) -> Tuple[int, int, int]:
    """Multiply two elements in H(F_p) using the exact cocycle (1/2)*omega(v1, v2).

    omega((q1, p1), (q2, p2)) = q1*p2 - p1*q2 mod p.
    inv2 = (p + 1) // 2.
    """
    _require_odd_prime(p)
    _require_element(g1, p)
    _require_element(g2, p)
    q1, p1, z1 = g1
    q2, p2, z2 = g2
    inv2 = (p + 1) // 2
    omega = (q1 * p2 - p1 * q2) % p
    cocycle = (inv2 * omega) % p
    return ((q1 + q2) % p, (p1 + p2) % p, (z1 + z2 + cocycle) % p)


def schroedinger_basis_action(
    g: Tuple[int, int, int], x: int, p: int, c: int = 1
) -> Tuple[int, int]:
    """Return (basis index, zeta_p exponent) for U_c(g)|x>.

    U_c(q,r,z)|x> = zeta_p**(c*(z-r*x-q*r/2)) |x+q>.
    Exponents are exact residues, so equality needs no floating-point tolerance.
    The c=0 action obeys the group law but need not be irreducible.
    """
    _require_odd_prime(p)
    _require_element(g, p)
    if any(type(v) is not int or not 0 <= v < p for v in (x, c)):
        raise ValueError("Basis index and central character must lie in [0, p).")
    q, r, z = g
    return ((x + q) % p, (c * (z - r * x - ((p + 1) // 2) * q * r)) % p)


def check_schroedinger_representation_law(p: int, c: int = 1) -> bool:
    """Exhaustively compare both monomial actions for all pairs and basis vectors.

    This finite check costs O(p^7); receipts run it only for p=3 and p=5.
    It checks the representation law, not an irreducibility/uniqueness theorem.
    """
    elements = heisenberg_group_elements(p)
    actions = {g: [schroedinger_basis_action(g, x, p, c) for x in range(p)] for g in elements}
    for g1 in elements:
        for g2 in elements:
            product = actions[heisenberg_group_multiply(g1, g2, p)]
            for x in range(p):
                y, e2 = actions[g2][x]
                z, e1 = actions[g1][y]
                if product[x] != (z, (e1 + e2) % p):
                    return False
    return True


def verify_central_character_classification(p: int) -> Dict[str, Any]:
    """Evaluate the declared finite Stone-von Neumann census formula for F_p:

    Order of H(F_p) = p^3.
    Number of conjugacy classes:
    - Center Z(H) has p classes of size 1 (z != 0 in center).
    - Each of the p^2 - 1 nonzero vectors in F_p^2 indexes one class of size p.
      Number of non-central classes = (p^3 - p) / p = p^2 - 1.
    Total classes = p + (p^2 - 1) = p^2 + p - 1.

    Irreducible representations:
    - 1-dimensional representations: character vanishes on center, factoring through H/Z = F_p^2.
      Count = p^2 irreps of dimension 1.
    - Higher dimensional representations:
      Remaining sum of squares: p^3 - p^2 * 1^2 = p^3 - p^2 = (p - 1) * p^2.
      Number of non-trivial central characters = p - 1.
      Each non-trivial character c in {1, ..., p-1} has EXACTLY ONE irrep of dimension p!
      Total irreps = p^2 + (p - 1) = p^2 + p - 1 = number of conjugacy classes!
    """
    _require_odd_prime(p)
    num_1d_irreps = p * p
    num_p_dim_irreps = p - 1
    total_irreps = num_1d_irreps + num_p_dim_irreps
    total_dim_sq = num_1d_irreps * (1**2) + num_p_dim_irreps * (p**2)

    assert total_dim_sq == p**3, f"Sum of squared dimensions {total_dim_sq} != p^3 {p**3}"

    return {
        "prime": p,
        "group_order": p**3,
        "center_order": p,
        "num_conjugacy_classes": p**2 + p - 1,
        "num_1d_irreps": num_1d_irreps,
        "num_higher_irreps": num_p_dim_irreps,
        "higher_irrep_dimension": p,
        "uniqueness_per_nontrivial_character": True,
        "classification_evidence": "DECLARED_THEOREM_INPUT_NOT_PROVED_HERE",
        "sum_of_squares": total_dim_sq,
    }


def generate_canonical_block03_receipt() -> Dict[str, Any]:
    """Generate exact finite action checks with an explicitly declared census input."""
    census = [
        verify_central_character_classification(p)
        for p in [3, 5, 7, 11]
    ]

    return {
        "authority_effect": "None",
        "citation": "sealed-derivation-v1 (3100c4e)",
        "campaign": "C500",
        "block": "block_03",
        "global_targets": "C500-T351..C500-T375",
        "terminal_outcome": "FINITE_REPRESENTATION_CHECKS_WITH_DECLARED_CENSUS",
        "predecessor_binding_status": "NOT_VERIFIED_BY_KERNEL",
        "cited_source": {
            "source_id": "S1",
            "theorem": "Finite Stone-von Neumann Theorem for odd prime finite fields F_p",
            "hypothesis_table": {
                "base_ring": "Finite field F_p with p odd prime",
                "symplectic_form": "Standard non-degenerate alternating bilinear form",
                "central_character": "Non-trivial character chi_c with c in {1, ..., p-1}",
                "uniqueness_assertion": "Unique irreducible representation of dimension p up to unitary equivalence",
            },
        },
        "central_character_census": census,
        "representation_law_checks": [
            {"prime": p, "central_character": c, "all_pairs_and_basis": True,
             "passed": check_schroedinger_representation_law(p, c)}
            for p in (3, 5) for c in range(p)
        ],
        "open_obligations": ["irreducibility", "intertwiner uniqueness", "general classification proof or exact theorem import"],
        "characteristic_two_separation": {
            "prime": 2,
            "inv2_exists": False,
            "obstacle": "2 = 0 in F_2 prevents division by 2 in the cocycle (1/2)*omega",
            "resolution": "An ordered cocycle defines a Heisenberg group in characteristic two; its classification is not checked here.",
            "status": "EXCLUDED_FROM_THIS_COCYCLE_IMPLEMENTATION",
        },
        "composite_modulus_analysis": {
            "modulus": 6,
            "crt_decomposition": "H(Z_6) = H(Z_2) x H(Z_3)",
            "inherited_obstruction": "Inherits characteristic 2 parity obstacle from Z_2 component",
            "status": "SPLITS_BY_CRT_COMPONENTS",
        },
        "machine_bet_clauses": {
            "odd_prime_fixed_character_uniqueness": "DECLARED_THEOREM_INPUT_OPEN_VERIFICATION",
            "nontrivial_central_character_is_required": True,
            "characteristic_two_handled_separately": False,
            "composite_modulus_status": "SPLITS_BY_BASE_RING",
            "cited_theorem_hypotheses_are_machine_mapped": False,
        },
    }


if __name__ == "__main__":
    receipt = generate_canonical_block03_receipt()
    print(json.dumps(receipt, indent=2))

__all__ = ['check_schroedinger_representation_law', 'generate_canonical_block03_receipt', 'heisenberg_group_elements', 'heisenberg_group_multiply', 'schroedinger_basis_action', 'verify_central_character_classification']
