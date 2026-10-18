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
from itertools import combinations
from typing import Any, Dict, List, NamedTuple, Sequence

# Unnormalized, real Tiles product factors. Projectors divide by squared norms.
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


def tiles_upb_certificate(factors=TILES_FACTORS) -> Dict[str, Any]:
    """Finite exact certificate, under the declared UPB-complement criterion.

    The rank test covers all 32 assignments of five orthogonality conditions
    to the two local factors. Rank three on at least one side excludes a
    nonzero product vector. This is computation, not a Lean theorem or a
    generic classifier of bipartite entanglement.
    """
    if len(factors) != 5 or any(len(a) != 3 or len(b) != 3 for a, b in factors):
        raise ValueError("five pairs of three-coordinate factors are required")
    vectors = [tuple(x*y for x in a for y in b) for a, b in factors]
    norms = [sum(x*x for x in v) for v in vectors]
    if any(n == 0 for n in norms):
        raise ValueError("zero product vector")
    if any(sum(x*y for x, y in zip(vectors[i], vectors[j])) != 0
           for i in range(5) for j in range(i)):
        raise ValueError("product vectors are not mutually orthogonal")
    partitions = [
        _spans_three([factors[k][0] for k in range(5) if mask & (1 << k)])
        or _spans_three([factors[k][1] for k in range(5) if not mask & (1 << k)])
        for mask in range(32)
    ]
    rho = [[(Fraction(int(i == j)) - sum(Fraction(v[i]*v[j], n)
             for v, n in zip(vectors, norms))) / 4 for j in range(9)] for i in range(9)]
    trace = sum(rho[i][i] for i in range(9))
    scaled_projector = all(
        4 * sum(rho[i][k] * rho[k][j] for k in range(9)) == rho[i][j]
        for i in range(9) for j in range(9))
    # rho = 4 rho^T rho gives a rational sum-of-squares PSD certificate.
    symmetric = all(rho[i][j] == rho[j][i] for i in range(9) for j in range(9))
    pt = [[rho[3*(i//3) + j%3][3*(j//3) + i%3] for j in range(9)] for i in range(9)]
    ppt = symmetric and scaled_projector and pt == rho
    return {
        "name": "Tiles 3x3 UPB complement",
        "dimension": 9, "bipartite_dims": (3, 3), "trace": str(trace),
        "carrier_field": "Q", "declared_conductor": 1, "embeds_in_120": True,
        "factors": factors, "squared_norms": norms,
        "density_matrix": [[str(x) for x in row] for row in rho],
        "orthogonality_checked": True, "partition_count": len(partitions),
        "unextendible_by_rank_cover": all(partitions),
        "scaled_projector_identity": scaled_projector,
        "partial_transpose_equals_state": pt == rho,
        "is_ppt": ppt,
        "is_bound_entangled": trace == 1 and ppt and all(partitions),
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
        # Extract squarefree part of d
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

        # 1. 3-qubit GHZ state: (|000> + |111>) / sqrt(2)
        # Amplitudes in Q(sqrt(2)) -> conductor 8 (since 8 | 120).
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

        # 2. 3-qubit W state: (|001> + |010> + |100>) / sqrt(3)
        # Amplitudes in Q(sqrt(3)) -> conductor 12 (since 12 | 120).
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

        # 3. 5-qubit code [[5, 1, 3]] (Smallest 1-qubit ECC)
        # Stabilizer generators: cyclic shifts of XZZXI.
        # Projector P = (1/16) * prod(I + g_i) in M_32(Q(i)). Conductor 4.
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

        # 4. 7-qubit Steane code [[7, 1, 3]] (CSS code)
        # Generators are purely real Pauli X and Z operators. Conductor 1.
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
            # Complete MUB system in prime dimension p requires:
            # - Clock operator Z_p with eigenvalue omega_p = zeta_p (conductor p)
            # - Discrete Fourier transform F_p with normalization 1/sqrt(p)
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
            # Bob's measurement setting phase offsets beta = +-1/4 require relative phases zeta_{4d}
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
