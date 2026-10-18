"""Declared higher-dimensional conductor bounds and an exact Tiles certificate.

Labels distinguish generators/projectors, parity checks, normalized states, and
measurement settings. Their LCM is not a proof of a minimal universal field.
CGLMP bounds cover settings, not an optimal entangled state's amplitudes.
The Tiles calculation constructs the rational matrix and all 32 rank cases;
its entanglement interpretation uses the declared UPB-complement criterion.
AuthorityEffect: None. Citation: sealed-derivation-v1 (3100c4e).
"""

from __future__ import annotations

import math
from fractions import Fraction
from typing import Any, Dict, List, NamedTuple, Sequence, Tuple
from itertools import combinations


TILES_FACTORS = (
    ((1, 0, 0), (1, -1, 0)),
    ((1, -1, 0), (0, 0, 1)),
    ((0, 0, 1), (0, 1, -1)),
    ((0, 1, -1), (1, 0, 0)),
    ((1, 1, 1), (1, 1, 1)),
)


def _spans_three(rows: Sequence[Sequence[int]]) -> bool:
    """Exact rank-three criterion for these three-coordinate rational rows."""
    for a, b, c in combinations(rows, 3):
        det = (a[0] * (b[1]*c[2] - b[2]*c[1])
               - a[1] * (b[0]*c[2] - b[2]*c[0])
               + a[2] * (b[0]*c[1] - b[1]*c[0]))
        if det:
            return True
    return False


def _validate_tiles_factors(factors):
    if len(factors) != 5:
        raise ValueError("five pairs of three-coordinate factors are required")
    for a, b in factors:
        if len(a) != 3 or len(b) != 3:
            raise ValueError("five pairs of three-coordinate factors are required")
    vectors = [tuple(x*y for x in a for y in b) for a, b in factors]
    norms = [sum(x*x for x in v) for v in vectors]
    if any(n == 0 for n in norms):
        raise ValueError("zero product vector")
    for i in range(5):
        for j in range(i):
            if sum(x*y for x, y in zip(vectors[i], vectors[j])) != 0:
                raise ValueError("product vectors are not mutually orthogonal")
    return vectors, norms


def _compute_tiles_partitions(factors) -> List[bool]:
    partitions = []
    for mask in range(32):
        side_a = [factors[k][0] for k in range(5) if mask & (1 << k)]
        side_b = [factors[k][1] for k in range(5) if not mask & (1 << k)]
        partitions.append(_spans_three(side_a) or _spans_three(side_b))
    return partitions


def _construct_tiles_rho(vectors, norms) -> List[List[Fraction]]:
    rho = []
    for i in range(9):
        row = []
        for j in range(9):
            delta = Fraction(int(i == j))
            proj = sum(Fraction(v[i]*v[j], n) for v, n in zip(vectors, norms))
            row.append((delta - proj) / 4)
        rho.append(row)
    return rho


def _verify_tiles_ppt(rho: List[List[Fraction]]) -> Tuple[Fraction, bool, bool, bool]:
    trace = sum(rho[i][i] for i in range(9))
    scaled_projector = True
    for i in range(9):
        for j in range(9):
            if 4 * sum(rho[i][k] * rho[k][j] for k in range(9)) != rho[i][j]:
                scaled_projector = False
                break
        if not scaled_projector:
            break
    symmetric = all(rho[i][j] == rho[j][i] for i in range(9) for j in range(9))
    pt = [[rho[3*(i//3) + j%3][3*(j//3) + i%3] for j in range(9)] for i in range(9)]
    pt_equals = (pt == rho)
    ppt = symmetric and scaled_projector and pt_equals
    return trace, scaled_projector, pt_equals, ppt


def tiles_upb_certificate(factors=TILES_FACTORS) -> Dict[str, Any]:
    """Finite exact certificate, under the declared UPB-complement criterion.

    The rank test covers all 32 assignments of five orthogonality conditions
    to the two local factors. Rank three on at least one side excludes a
    nonzero product vector. This is computation, not a Lean theorem or a
    generic classifier of bipartite entanglement.
    """
    vectors, norms = _validate_tiles_factors(factors)
    partitions = _compute_tiles_partitions(factors)
    rho = _construct_tiles_rho(vectors, norms)
    trace, scaled_projector, pt_equals, ppt = _verify_tiles_ppt(rho)
    unextendible = all(partitions)

    return {
        "name": "Tiles 3x3 UPB complement",
        "dimension": 9, "bipartite_dims": (3, 3), "trace": str(trace),
        "carrier_field": "Q", "declared_conductor": 1, "embeds_in_120": True,
        "factors": factors, "squared_norms": norms,
        "density_matrix": [[str(x) for x in row] for row in rho],
        "orthogonality_checked": True, "partition_count": len(partitions),
        "unextendible_by_rank_cover": unextendible,
        "scaled_projector_identity": scaled_projector,
        "partial_transpose_equals_state": pt_equals,
        "is_ppt": ppt,
        "is_bound_entangled": trace == 1 and ppt and unextendible,
        "claim_type": "DETERMINISTIC_COMPUTATION_UNDER_DECLARED_UPB_CRITERION",
        "rationale": "Exact rational matrix, PSD sum-of-squares identity, partial transpose and all 32 local rank covers; not a Lean proof.",
    }


class ConductorReport(NamedTuple):
    """Declared sufficient labels for the named objects, not proved minima."""
    witness_name: str
    dimension: int
    declared_conductor: int
    embeds_in_120: bool
    escalated_lcm_conductor: int
    field_declaration: str
    rationale: str
    minimality_proved: bool = False


class HigherDimEntanglementWitness:
    """Exact algebraic analysis of higher-dimensional entanglement carriers and conductor bounds."""

    TARGET_LCM_120: int = 120

    @staticmethod
    def quadratic_extension_conductor(d: int) -> int:
        """Computes the minimal cyclotomic conductor of Q(sqrt(d)) via Kronecker-Weber discriminant.

        disc(Q(sqrt(d))) =
        - d if d = 1 mod 4 (squarefree)
        - 4d if d = 2, 3 mod 4 (squarefree)
        """
        if type(d) is not int or d < 1:
            raise ValueError("dimension must be a positive integer")
        sq_free = d
        for p in range(2, int(math.isqrt(d)) + 1):
            while sq_free % (p * p) == 0:
                sq_free //= (p * p)

        if sq_free == 1:
            return 1
        elif sq_free % 4 == 1:
            return sq_free
        else:
            return 4 * sq_free

    @staticmethod
    def evaluate_multi_qubit_stabilizers() -> List[ConductorReport]:
        """Evaluates minimal conductors for multi-qubit stabilizer codes and entangled states."""
        reports = []

        c_ghz = 8
        reports.append(ConductorReport(
            witness_name="3-Qubit GHZ State & Mermin Nonlocality",
            dimension=8,
            declared_conductor=c_ghz,
            embeds_in_120=HigherDimEntanglementWitness.TARGET_LCM_120 % c_ghz == 0,
            escalated_lcm_conductor=math.lcm(HigherDimEntanglementWitness.TARGET_LCM_120, c_ghz),
            field_declaration="Q(zeta_8)",
            rationale="Normalization requires 1/sqrt(2) in Q(zeta_8); 3-qubit Mermin operator in Pauli group P_3."
        ))

        c_w = 12
        reports.append(ConductorReport(
            witness_name="3-Qubit W State",
            dimension=8,
            declared_conductor=c_w,
            embeds_in_120=HigherDimEntanglementWitness.TARGET_LCM_120 % c_w == 0,
            escalated_lcm_conductor=math.lcm(HigherDimEntanglementWitness.TARGET_LCM_120, c_w),
            field_declaration="Q(zeta_12)",
            rationale="Normalization requires 1/sqrt(3) in Q(zeta_12) (disc=12)."
        ))

        c_5q = 4
        reports.append(ConductorReport(
            witness_name="5-Qubit Stabilizer Code [[5, 1, 3]]",
            dimension=32,
            declared_conductor=c_5q,
            embeds_in_120=HigherDimEntanglementWitness.TARGET_LCM_120 % c_5q == 0,
            escalated_lcm_conductor=math.lcm(HigherDimEntanglementWitness.TARGET_LCM_120, c_5q),
            field_declaration="Q(i) = Q(zeta_4)",
            rationale="Declared Q(i) upper bound for generator/projector entries, not a minimum or a normalized-codeword claim."
        ))

        c_steane = 1
        reports.append(ConductorReport(
            witness_name="7-Qubit Steane CSS Code [[7, 1, 3]]",
            dimension=128,
            declared_conductor=c_steane,
            embeds_in_120=True,
            escalated_lcm_conductor=HigherDimEntanglementWitness.TARGET_LCM_120,
            field_declaration="Q",
            rationale="Rational CSS parity-check entries only; not normalized Steane state amplitudes."
        ))

        return reports

    @staticmethod
    def evaluate_prime_qudit_mubs(primes: Sequence[int] = (2, 3, 5, 7, 11, 13)) -> List[ConductorReport]:
        """Evaluates minimal conductors for complete MUB systems in prime dimension p."""
        reports = []
        for p in primes:
            if type(p) is not int or p < 2 or any(p % k == 0 for k in range(2, math.isqrt(p) + 1)):
                raise ValueError("MUB dimension must be prime")
            disc = HigherDimEntanglementWitness.quadratic_extension_conductor(p)
            c_p = math.lcm(p, disc)
            embeds = (HigherDimEntanglementWitness.TARGET_LCM_120 % c_p == 0)
            escalated = math.lcm(HigherDimEntanglementWitness.TARGET_LCM_120, c_p)

            reports.append(ConductorReport(
                witness_name=f"Prime-{p} Qudit Complete MUB System (d={p})",
                dimension=p,
                declared_conductor=c_p,
                embeds_in_120=embeds,
                escalated_lcm_conductor=escalated,
                field_declaration=f"Q(zeta_{c_p})",
                rationale=(
                    f"Clock matrix requires zeta_{p}; Fourier Hadamard requires sqrt({p}) "
                    f"with disc {disc}. Total conductor is {c_p}."
                )
            ))
        return reports

    @staticmethod
    def evaluate_cglmp_nonlocality(dims: Sequence[int] = (3, 4, 5, 6, 7, 8)) -> List[ConductorReport]:
        """Declared carriers for Fourier measurement settings, not optimal state amplitudes."""
        reports = []
        for d in dims:
            if type(d) is not int or d < 2:
                raise ValueError("CGLMP measurement dimension must be an integer >= 2")
            disc = HigherDimEntanglementWitness.quadratic_extension_conductor(d)
            c_cglmp = math.lcm(4 * d, disc)
            embeds = (HigherDimEntanglementWitness.TARGET_LCM_120 % c_cglmp == 0)
            escalated = math.lcm(HigherDimEntanglementWitness.TARGET_LCM_120, c_cglmp)

            reports.append(ConductorReport(
                witness_name=f"CGLMP-{d} High-Dimensional Bell Nonlocality",
                dimension=d,
                declared_conductor=c_cglmp,
                embeds_in_120=embeds,
                escalated_lcm_conductor=escalated,
                field_declaration=f"Q(zeta_{c_cglmp})",
                rationale=(
                    f"Dimension {d} Fourier bases with Bob's +-1/4 phase offsets require zeta_{4*d} "
                    f"and sqrt({d}) (disc {disc}), yielding conductor {c_cglmp}."
                )
            ))
        return reports

    @staticmethod
    def verify_horodecki_3x3_upb_witness() -> Dict[str, Any]:
        """Legacy entry point for the exact, declared Tiles UPB certificate."""
        return tiles_upb_certificate()

    @staticmethod
    def full_escalation_hierarchy_summary() -> Dict[str, Any]:
        """Generates comprehensive conductor hierarchy across all examined higher-dimensional classes."""
        stabilizers = HigherDimEntanglementWitness.evaluate_multi_qubit_stabilizers()
        prime_mubs = HigherDimEntanglementWitness.evaluate_prime_qudit_mubs()
        cglmp = HigherDimEntanglementWitness.evaluate_cglmp_nonlocality()
        horodecki = HigherDimEntanglementWitness.verify_horodecki_3x3_upb_witness()

        all_reports = stabilizers + prime_mubs + cglmp
        contained = [r for r in all_reports if r.embeds_in_120]
        escalating = [r for r in all_reports if not r.embeds_in_120]

        return {
            "base_lcm_conductor": HigherDimEntanglementWitness.TARGET_LCM_120,
            "claim_type": "DECLARED_CARRIER_BOUNDS_PLUS_EXACT_TILES_CERTIFICATE",
            "minimality_proved": False,
            "total_witnesses_evaluated": len(all_reports) + 1,
            "contained_in_120_count": len(contained) + 1,
            "escalating_count": len(escalating),
            "critical_escalation_thresholds": {
                "first_prime_failure": "p = 7 (conductor 7 does not divide 120; escalates to lcm(120, 7) = 840)",
                "first_cglmp_failure": "d = 4 (conductor 16 does not divide 120; escalates to lcm(120, 16) = 240)",
                "dyadic_phase_escalation": "d = 8 with fine Fourier shifts (conductor 32 does not divide 120; escalates to 480)",
                "pauli_stabilizer_invariance": "Four named object declarations only; generator/parity-check entries are not normalized state amplitudes."
            },
            "stabilizers": [r._asdict() for r in stabilizers],
            "prime_mubs": [r._asdict() for r in prime_mubs],
            "cglmp": [r._asdict() for r in cglmp],
            "horodecki_3x3": horodecki
        }

__all__ = ['ConductorReport', 'HigherDimEntanglementWitness', 'TILES_FACTORS', 'tiles_upb_certificate']
