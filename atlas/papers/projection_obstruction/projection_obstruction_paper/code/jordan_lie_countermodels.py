"""Finite examples and separately labelled theory summaries for Appendix E.

The calculations check specified octonion/Jordan identities, dimension
obstructions, a real purification, and a central-weight obstruction. They do
not verify an operational theory's complete axiom set. In particular,
octonion nonassociativity is not a proof of the Albert algebra's exceptionality,
quaternions are associative, and real quantum theory admits purification.
The B1--B4 classification and its state-space assumptions are written proofs.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Sequence


def _to_fraction(value: object) -> Fraction:
    """Accept explicitly exact scalars; never approximate a float as rational."""
    if isinstance(value, Fraction):
        return value
    if type(value) is int:
        return Fraction(value, 1)
    if isinstance(value, str):
        return Fraction(value)
    raise TypeError("exact scalars must be integers, Fraction objects, or rational strings")


@dataclass(frozen=True)
class WeakJordanLiePremises:
    """The candidate W1--W4 formulation; this text is not an axiom verifier."""

    W1_spectral_jordan_algebra: str = (
        "A finite-dimensional unital real Jordan algebra with an admitted real spectral "
        "decomposition into mutually orthogonal nonzero idempotents."
    )
    W2_reversible_lie_dynamics: str = (
        "A real Lie bracket satisfies Jacobi and acts by derivations of the Jordan product."
    )
    W3_associator_compatibility: str = (
        "The Jordan associator equals lambda times {b, {c, a}} for a supplied lambda > 0. "
        "This sign and compatibility are premises, not consequences of an uncertainty slogan."
    )
    W4_composition_and_purification: str = (
        "Composite systems are locally tomographic and every state admits a pure-state purification."
    )
    conditional_derivation_status: str = (
        "The operational reconstruction is proved under B1-B4 plus purification. W1-W4 alone "
        "does not specify all states, effects, compatible local algebra embeddings, corners, "
        "or full process availability. A full reconstruction from this candidate remains open."
    )


# ---------------------------------------------------------------------------
# 1. Exceptional Albert Algebra h_3(O) (imported obstruction to full B1)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Octonion:
    """A rational-coordinate octonion with the declared Fano multiplication."""

    c0: Fraction
    c1: Fraction
    c2: Fraction
    c3: Fraction
    c4: Fraction
    c5: Fraction
    c6: Fraction
    c7: Fraction

    def __post_init__(self) -> None:
        for index, value in enumerate(self.coeffs):
            object.__setattr__(self, f"c{index}", _to_fraction(value))

    @classmethod
    def from_coeffs(cls, coeffs: Sequence[object]) -> Octonion:
        if len(coeffs) != 8:
            raise ValueError(f"Octonion requires 8 coefficients, got {len(coeffs)}")
        fracs = [_to_fraction(c) for c in coeffs]
        return cls(*fracs)

    @classmethod
    def zero(cls) -> Octonion:
        z = Fraction(0)
        return cls(z, z, z, z, z, z, z, z)

    @classmethod
    def unit(cls, index: int) -> Octonion:
        if type(index) is not int or not (0 <= index < 8):
            raise IndexError("Octonion unit index must be 0..7")
        coeffs = [Fraction(0)] * 8
        coeffs[index] = Fraction(1)
        return cls(*coeffs)

    @property
    def coeffs(self) -> tuple[Fraction, ...]:
        return (self.c0, self.c1, self.c2, self.c3, self.c4, self.c5, self.c6, self.c7)

    def is_zero(self) -> bool:
        return all(c == Fraction(0) for c in self.coeffs)

    def is_real(self) -> bool:
        return all(c == Fraction(0) for c in self.coeffs[1:])

    def conjugate(self) -> Octonion:
        return Octonion(
            self.c0,
            -self.c1,
            -self.c2,
            -self.c3,
            -self.c4,
            -self.c5,
            -self.c6,
            -self.c7,
        )

    def __add__(self, other: Octonion) -> Octonion:
        return Octonion(
            self.c0 + other.c0,
            self.c1 + other.c1,
            self.c2 + other.c2,
            self.c3 + other.c3,
            self.c4 + other.c4,
            self.c5 + other.c5,
            self.c6 + other.c6,
            self.c7 + other.c7,
        )

    def __sub__(self, other: Octonion) -> Octonion:
        return Octonion(
            self.c0 - other.c0,
            self.c1 - other.c1,
            self.c2 - other.c2,
            self.c3 - other.c3,
            self.c4 - other.c4,
            self.c5 - other.c5,
            self.c6 - other.c6,
            self.c7 - other.c7,
        )

    def scale(self, scalar: object) -> Octonion:
        s = _to_fraction(scalar)
        return Octonion(
            self.c0 * s,
            self.c1 * s,
            self.c2 * s,
            self.c3 * s,
            self.c4 * s,
            self.c5 * s,
            self.c6 * s,
            self.c7 * s,
        )

    def __mul__(self, other: Octonion) -> Octonion:
        """Octonionic multiplication based on Fano plane orientation.

        Fano plane oriented lines (e_i * e_j = e_k):
        (1, 2, 3), (1, 4, 5), (1, 7, 6), (2, 4, 6), (2, 5, 7), (3, 4, 7), (3, 6, 5)
        """
        # Multiplicative table between basis elements e_i and e_j (1 <= i, j <= 7)
        fano_triplets = [
            (1, 2, 3),
            (1, 4, 5),
            (1, 7, 6),
            (2, 4, 6),
            (2, 5, 7),
            (3, 4, 7),
            (3, 6, 5),
        ]
        # Build lookup table for e_i * e_j
        mult_table: dict[tuple[int, int], tuple[int, int]] = {}
        for i in range(1, 8):
            mult_table[(i, i)] = (-1, 0)
        for a, b, c in fano_triplets:
            mult_table[(a, b)] = (1, c)
            mult_table[(b, a)] = (-1, c)
            mult_table[(b, c)] = (1, a)
            mult_table[(c, b)] = (-1, a)
            mult_table[(c, a)] = (1, b)
            mult_table[(a, c)] = (-1, b)

        res = [Fraction(0)] * 8
        a_coeffs = self.coeffs
        b_coeffs = other.coeffs

        # Real unit e0 * e0
        res[0] += a_coeffs[0] * b_coeffs[0]
        # Real unit * imaginary
        for i in range(1, 8):
            res[i] += a_coeffs[0] * b_coeffs[i] + a_coeffs[i] * b_coeffs[0]

        # Imaginary * imaginary
        for i in range(1, 8):
            for j in range(1, 8):
                sign, k = mult_table[(i, j)]
                prod_val = a_coeffs[i] * b_coeffs[j]
                if sign == 1:
                    res[k] += prod_val
                else:
                    res[k] -= prod_val

        return Octonion(*res)


@dataclass(frozen=True)
class AlbertMatrix:
    """A 3x3 Octonionic Hermitian matrix in h_3(O).

    Representation:
    diag: 3 real Fractions (d0, d1, d2)
    off_diag: 3 Octonions (x01, x02, x12)
    where:
    A[0, 0] = d0, A[1, 1] = d1, A[2, 2] = d2
    A[0, 1] = x01, A[1, 0] = x01^*
    A[0, 2] = x02, A[2, 0] = x02^*
    A[1, 2] = x12, A[2, 1] = x12^*
    """

    d0: Fraction
    d1: Fraction
    d2: Fraction
    x01: Octonion
    x02: Octonion
    x12: Octonion

    def __post_init__(self) -> None:
        for name in ("d0", "d1", "d2"):
            object.__setattr__(self, name, _to_fraction(getattr(self, name)))
        if not all(isinstance(value, Octonion) for value in (self.x01, self.x02, self.x12)):
            raise TypeError("off-diagonal entries must be Octonion objects")

    @classmethod
    def zero(cls) -> AlbertMatrix:
        z = Fraction(0)
        oz = Octonion.zero()
        return cls(z, z, z, oz, oz, oz)

    def get_element(self, row: int, col: int) -> Octonion:
        if row == col:
            d = (self.d0, self.d1, self.d2)[row]
            return Octonion.from_coeffs((d, 0, 0, 0, 0, 0, 0, 0))
        if row == 0 and col == 1:
            return self.x01
        if row == 1 and col == 0:
            return self.x01.conjugate()
        if row == 0 and col == 2:
            return self.x02
        if row == 2 and col == 0:
            return self.x02.conjugate()
        if row == 1 and col == 2:
            return self.x12
        if row == 2 and col == 1:
            return self.x12.conjugate()
        raise IndexError("Matrix index out of bounds")

    def __add__(self, other: AlbertMatrix) -> AlbertMatrix:
        return AlbertMatrix(
            self.d0 + other.d0,
            self.d1 + other.d1,
            self.d2 + other.d2,
            self.x01 + other.x01,
            self.x02 + other.x02,
            self.x12 + other.x12,
        )

    def __sub__(self, other: AlbertMatrix) -> AlbertMatrix:
        return AlbertMatrix(
            self.d0 - other.d0,
            self.d1 - other.d1,
            self.d2 - other.d2,
            self.x01 - other.x01,
            self.x02 - other.x02,
            self.x12 - other.x12,
        )

    def scale(self, scalar: object) -> AlbertMatrix:
        s = _to_fraction(scalar)
        return AlbertMatrix(
            self.d0 * s,
            self.d1 * s,
            self.d2 * s,
            self.x01.scale(s),
            self.x02.scale(s),
            self.x12.scale(s),
        )

    def is_zero(self) -> bool:
        return (
            self.d0 == Fraction(0)
            and self.d1 == Fraction(0)
            and self.d2 == Fraction(0)
            and self.x01.is_zero()
            and self.x02.is_zero()
            and self.x12.is_zero()
        )

    def jordan_product(self, other: AlbertMatrix) -> AlbertMatrix:
        """Compute the Jordan product A o B = (1 / 2) * (A B + B A).

        In h_3(O), for Hermitian matrices, A B + B A is also Hermitian.
        """
        # Compute row-col matrix products for elements of (A B + B A) / 2
        def entry_AB_plus_BA_half(r: int, c: int) -> Octonion:
            sum_prod = Octonion.zero()
            for k in range(3):
                p1 = self.get_element(r, k) * other.get_element(k, c)
                p2 = other.get_element(r, k) * self.get_element(k, c)
                sum_prod = sum_prod + (p1 + p2)
            return sum_prod.scale(Fraction(1, 2))

        d0 = entry_AB_plus_BA_half(0, 0).c0
        d1 = entry_AB_plus_BA_half(1, 1).c0
        d2 = entry_AB_plus_BA_half(2, 2).c0
        x01 = entry_AB_plus_BA_half(0, 1)
        x02 = entry_AB_plus_BA_half(0, 2)
        x12 = entry_AB_plus_BA_half(1, 2)

        return AlbertMatrix(d0, d1, d2, x01, x02, x12)


def check_albert_algebra_properties() -> dict[str, Any]:
    """Check one Jordan identity and associator; label exceptionality as imported."""
    # 1. Dimension calculation
    real_dim = 3
    octonion_off_diag_dim = 3 * 8
    total_dim = real_dim + octonion_off_diag_dim  # 27

    # 2. Test octonionic associator on basis elements e1, e2, e4
    e1 = Octonion.unit(1)
    e2 = Octonion.unit(2)
    e4 = Octonion.unit(4)
    p_12_4 = (e1 * e2) * e4
    p_1_24 = e1 * (e2 * e4)
    associator = p_12_4 - p_1_24
    octonion_is_non_associative = not associator.is_zero()

    # 3. Test Jordan identity on explicit h_3(O) elements
    A = AlbertMatrix(
        d0=Fraction(1),
        d1=Fraction(2),
        d2=Fraction(-1),
        x01=Octonion.unit(1),
        x02=Octonion.unit(4),
        x12=Octonion.unit(2),
    )
    B = AlbertMatrix(
        d0=Fraction(3),
        d1=Fraction(0),
        d2=Fraction(1),
        x01=Octonion.unit(3),
        x02=Octonion.unit(6),
        x12=Octonion.unit(5),
    )

    A2 = A.jordan_product(A)
    AoB = A.jordan_product(B)
    lhs = AoB.jordan_product(A2)
    BoA2 = B.jordan_product(A2)
    rhs = A.jordan_product(BoA2)
    diff = lhs - rhs
    jordan_identity_holds = diff.is_zero()

    # Exceptionality is a separate general theorem, not a consequence of this
    # one octonion associator or the one checked Jordan identity.
    return {
        "algebra_name": "Albert Algebra h_3(O)",
        "dimension": total_dim,
        "selected_jordan_identity_holds": jordan_identity_holds,
        "octonion_non_associative": octonion_is_non_associative,
        "associator_witness": associator.coeffs,
        "special_embedding_status": "imported_exceptionality_theorem",
        "computed_scope": "one Jordan-identity pair and one octonion associator",
        "excluded_by": "Axiom B1 (Special/Associative Jordan-Lie Compatibility)",
    }


# ---------------------------------------------------------------------------
# 2. Real Quantum Mechanics (dimension obstruction to B2 / W4)
# ---------------------------------------------------------------------------


def check_real_qm_countermodel() -> dict[str, Any]:
    """Demonstrate failure of local tomography (composite dimension mismatch) in Real QM."""
    # Single 2-level real quantum system: observables are 2x2 real symmetric matrices
    # S_2(R) basis: [ [1,0],[0,0] ], [ [0,0],[0,1] ], [ [0,1],[1,0] ] (or I, X, Z)
    dim_single = 3  # n(n+1)/2 for n=2

    # Product of two single systems under local tomography premise:
    dim_product = dim_single * dim_single  # 3 * 3 = 9

    # True composite 2-qubit real system: observables are 4x4 real symmetric matrices
    # S_4(R):
    dim_composite = (4 * 5) // 2  # 10

    dimension_gap = dim_composite - dim_product  # 10 - 9 = 1

    # Explicit missing observable: W = Y (x) Y
    # Note: Y = [[0, -1], [1, 0]] is skew-symmetric, not an observable in S_2(R).
    # But W = Y (x) Y satisfies W^T = (Y^T) (x) (Y^T) = (-Y) (x) (-Y) = Y (x) Y,
    # so W is real symmetric, hence in S_4(R)!
    # Yet W is orthogonal to every product A (x) B with A, B in S_2(R).
    # Proof: tr(W * (A (x) B)) = tr(Y A) * tr(Y B) = 0 * 0 = 0, because Y is skew-symmetric
    # and A, B are symmetric.
    local_tomography_fails = dim_composite != dim_product

    # A real pure state with a mixed real marginal. The general existence
    # theorem uses a real spectral decomposition, as explained in Appendix E.
    vector = (Fraction(3, 5), Fraction(0), Fraction(0), Fraction(4, 5))
    joint = tuple(tuple(a * b for b in vector) for a in vector)
    marginal = tuple(
        tuple(sum(joint[2 * i + k][2 * j + k] for k in range(2)) for j in range(2))
        for i in range(2)
    )
    joint_purity = sum(joint[i][j] * joint[j][i] for i in range(4) for j in range(4))

    return {
        "theory_name": "Real Quantum Mechanics (RQM)",
        "single_system_observable_dim": dim_single,
        "product_observable_dim": dim_product,
        "composite_observable_dim": dim_composite,
        "dimension_gap": dimension_gap,
        "local_tomography_fails": local_tomography_fails,
        "missing_observable_witness": "Y (x) Y in S_4(R) orthogonal to S_2(R) (x) S_2(R)",
        "purification_vector": vector,
        "purification_joint": joint,
        "purification_marginal": marginal,
        "purification_joint_purity": joint_purity,
        "computed_scope": "declared dimension count and one exact real purification",
        "excluded_by": "Axiom B2 (Locally Tomographic Composition)",
    }


# ---------------------------------------------------------------------------
# 3. Quaternionic Quantum Mechanics (dimension obstruction to B2 / W4)
# ---------------------------------------------------------------------------


def check_quaternionic_qm_countermodel() -> dict[str, Any]:
    """Rule out the proposed H_4(H) composite by a dimension obstruction.

    This does not construct quaternionic composition or test an associator.
    Quaternion multiplication itself is associative.
    """
    # Single quaternionic qubit: 2x2 Quaternionic Hermitian matrices H_2(H)
    # Basis: 2 real diagonal + 1 off-diagonal quaternion (4 real parameters) = 2 + 4 = 6
    dim_single = 6

    # Product space dimension if local tomography held:
    dim_product = dim_single * dim_single  # 36

    # Composite 2-qubit quaternionic system: 4x4 Quaternionic Hermitian matrices H_4(H)
    # Basis: 4 real diagonal + 6 off-diagonal quaternions (6 * 4 = 24 parameters) = 4 + 24 = 28
    dim_composite = 28

    dimension_defect = dim_product - dim_composite  # 36 - 28 = 8

    # A real-linear isomorphism from the 36-dimensional product observable
    # space to this proposed 28-dimensional composite cannot exist.
    local_tomography_fails = dim_composite != dim_product

    return {
        "theory_name": "Quaternionic Quantum Mechanics (QQM)",
        "single_system_observable_dim": dim_single,
        "product_observable_dim": dim_product,
        "composite_observable_dim": dim_composite,
        "dimension_defect": dimension_defect,
        "local_tomography_fails": local_tomography_fails,
        "computed_scope": "dimension obstruction for the proposed H_4(H) composite only",
        "excluded_by": "Axiom B2 (Locally Tomographic Composition)",
    }


# ---------------------------------------------------------------------------
# 4. Superselection sectors (a deletion model for the purification selector)
# ---------------------------------------------------------------------------


def central_weight_bounds(weights: Sequence[object]) -> dict[str, Any]:
    """Compute the conditional bounds of Proposition E.7 from a central report.

    The standard block tensor product and the stated ancilla availability
    are mathematical premises. A weight vector does not certify either one.
    """
    exact = tuple(_to_fraction(weight) for weight in weights)
    if not exact or any(weight < 0 for weight in exact) or sum(exact) != 1:
        raise ValueError("central weights must be nonnegative and sum exactly to one")
    return {
        "central_weights": exact,
        "maximum_extension_purity": sum(weight * weight for weight in exact),
        "minimum_pure_marginal_distance": 1 - max(exact),
        "scope": "standard block tensor product; attainment needs the stated ancilla",
    }


def check_superselection_countermodel() -> dict[str, Any]:
    """Demonstrate superselection sector algebra satisfying B1-B4 and failing purification.

    In Appendix E (Lemma E.2), the direct sum algebra A = M_2(C) (+) M_2(C) with non-trivial
    center Z(A) = C (+) C satisfies all four base axioms B1-B4:
    - B1: Jordan-Lie product and bracket hold blockwise and on the direct sum.
    - B2: Locally tomographic composition holds under tensor product of direct sums.
    - B3: Compression U_p(A) is well-defined for all idempotents.
    - B4: Completely positive operations and channels are fully available.

    Superselection sectors are excluded exclusively by the Purification Selector:
    A mixed state with non-zero entropy on the center, e.g. rho = 1/2 rho_1 (+) 1/2 rho_2,
    cannot be purified into an entangled pure state on A (x) B within the superselection
    theory, because pure states in direct sums are rank-one in a single sector and vanish
    in all other sectors (Appendix E, Lemma E.2).
    """
    weights = (Fraction(1, 2), Fraction(1, 2))
    pure_central_reports = ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1)))
    distances = tuple(
        sum(abs(p - q) for p, q in zip(weights, vertex, strict=True)) / 2
        for vertex in pure_central_reports
    )
    return {
        "theory_name": "Superselection Sectors A = M_2(C) (+) M_2(C)",
        "center_dimension": 2,
        "base_classification_source": "written Theorem E.4, not verified by this function",
        "central_weights": weights,
        "pure_central_reports": pure_central_reports,
        "distances_to_pure_reports": distances,
        "minimum_central_distance": min(distances),
        "purification_of_this_central_mixture_fails": min(distances) > 0,
        "computed_scope": "distance from the fair central report to both pure central reports",
        "excluded_by": "Purification Selector (Theorem E.5)",
    }


def get_axiom_satisfaction_table() -> dict[str, dict[str, Any]]:
    """Return a written-theorem summary, not a computed satisfaction certificate.

    None means that no complete operational theory/composition is specified
    here for that cell. Failure of B1 or B2 does not imply failure of P.
    The boolean entries summarize the written arguments in Appendix E:
    - B1: Jordan-Lie positive observables & associative C*-embedding
    - B2: Locally tomographic composition
    - B3: Idempotent compression & nontrivial distinguishability
    - B4: Full process availability
    - Purification: Pure-state purification for all states (selector for simple B(H))
    """
    return {
        "albert_algebra": {
            "name": "Exceptional Albert Algebra h_3(O)",
            "B1": False,  # Non-special; fails associative embedding
            "B2": None,
            "B3": None,
            "B4": None,
            "purification": None,
            "verdict": "Excluded by B1 (imported exceptionality theorem)",
        },
        "real_qm": {
            "name": "Real Quantum Mechanics S_n(R)",
            "B1": False,  # Standard real symmetric observable family is outside Lemma E.2.
            "B2": False,  # Fails local tomography: dim(S_2 x S_2) = 9 != dim(S_4) = 10 (gap 1)
            "B3": True,   # Compressions exist
            "B4": None,   # The B2-based amplification structure is not satisfied.
            "purification": True,  # Real spectral decomposition supplies a real purification.
            "verdict": "Excluded by B2 (fails local tomography; missing Y x Y observable)",
        },
        "quaternionic_qm": {
            "name": "Quaternionic Quantum Mechanics H_n(H)",
            "B1": False,  # The full quaternionic family is outside Lemma E.2.
            "B2": False,  # Only the proposed H_4(H) composite is evaluated here.
            "B3": None,
            "B4": None,
            "purification": None,
            "verdict": "Proposed H_4(H) composite excluded by B2 dimension mismatch",
        },
        "superselection": {
            "name": "Superselection Sectors (+) M_{n_alpha}(C)",
            "B1": True,   # Satisfies Jordan-Lie axioms
            "B2": True,   # Satisfies locally tomographic composition
            "B3": True,   # Satisfies idempotent compression
            "B4": True,   # Satisfies full process availability
            "purification": False,  # FAILS purification on central sector mixtures!
            "verdict": "Satisfies B1-B4 base; excluded uniquely by the Purification Selector",
        },
        "complex_qm": {
            "name": "Standard Complex Quantum Mechanics M_n(C)",
            "B1": True,
            "B2": True,
            "B3": True,
            "B4": True,
            "purification": True,
            "verdict": "Admitted: standard complex Hilbert space quantum mechanics",
        },
    }


# ---------------------------------------------------------------------------
# Finite replay summary
# ---------------------------------------------------------------------------


def verify_jordan_lie_countermodels() -> dict[str, dict]:
    """Replay the finite calculations, refusing failed fixture identities.

    General exceptionality and operational classification are not verified.
    """
    albert_receipt = check_albert_algebra_properties()
    real_receipt = check_real_qm_countermodel()
    quaternion_receipt = check_quaternionic_qm_countermodel()
    superselection_receipt = check_superselection_countermodel()
    checks = (
        albert_receipt["selected_jordan_identity_holds"],
        albert_receipt["octonion_non_associative"],
        real_receipt["local_tomography_fails"],
        real_receipt["purification_joint_purity"] == 1,
        real_receipt["purification_marginal"]
        == ((Fraction(9, 25), Fraction(0)), (Fraction(0), Fraction(16, 25))),
        quaternion_receipt["local_tomography_fails"],
        superselection_receipt["purification_of_this_central_mixture_fails"],
    )
    if not all(checks):
        raise ValueError("a declared finite countermodel check failed")

    return {
        "albert_algebra": {
            "general_exclusion": "imported_exceptionality_theorem",
            "dimension": albert_receipt["dimension"],
            "selected_jordan_identity_holds": albert_receipt["selected_jordan_identity_holds"],
            "non_associative_witness": albert_receipt["octonion_non_associative"],
            "status": "finite_identity_checks",
        },
        "real_qm": {
            "axiom_tested": "B2",
            "excluded_property": "local_tomography",
            "single_dim": real_receipt["single_system_observable_dim"],
            "product_dim": real_receipt["product_observable_dim"],
            "composite_dim": real_receipt["composite_observable_dim"],
            "dimension_gap": real_receipt["dimension_gap"],
            "missing_observable_witness": real_receipt["missing_observable_witness"],
            "purification_joint_purity": real_receipt["purification_joint_purity"],
            "status": "exact_finite_witness",
        },
        "quaternionic_qm": {
            "axiom_tested": "B2",
            "excluded_property": "local_tomography_of_proposed_composite",
            "single_dim": quaternion_receipt["single_system_observable_dim"],
            "product_dim": quaternion_receipt["product_observable_dim"],
            "composite_dim": quaternion_receipt["composite_observable_dim"],
            "dimension_defect": quaternion_receipt["dimension_defect"],
            "status": "exact_dimension_obstruction",
        },
        "superselection": {
            "axiom_tested": "purification_selector",
            "excluded_property": "pure_state_purification_of_central_mixtures",
            "center_dimension": superselection_receipt["center_dimension"],
            "minimum_central_distance": superselection_receipt["minimum_central_distance"],
            "purification_fails": superselection_receipt["purification_of_this_central_mixture_fails"],
            "status": "exact_central_weight_obstruction",
        },
    }
