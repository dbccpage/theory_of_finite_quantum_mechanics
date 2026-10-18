# QM-209 Non-Commutative Operator Algebra: the Finite Map

**Scope:** research note for `006_finite_qm`; not part of the manuscript, not a claim promotion. Companion to `phase_fiber_holonomy_bridge_finite_map.md`.
**Code:** `python/finite_qm/use_cases/context_parity_control.py`, tests in `tests/e2e/test_e2e_context_parity_control.py` (7 tests).
**Status marks used:** PROVED (argument given here, finite and checkable), COMPUTED (exact arithmetic in Q(ζ₁₂) or F₂, replayable), IMPORTED (added structure that nothing finite here produces), CONJECTURED (none in this note).

Authority status: none. This note changes no admitted claim.

## 1. The question

QM-209 names the third import: a noncommutative algebra of observables, B(H) in the infinite-dimensional theory, so that no single context (one diagonal) carries every observable. The task is to research and discover the finite map to this problem.

The finite map has two parts that live in different coefficient groups. The commutator of two contexts is a central root of unity, a μ_d-valued holonomy of the context square. The consequence that matters for value assignments, that no deterministic assignment exists across overlapping contexts, is an F₂-valued holonomy of the context graph. Both are computed exactly. The completion step and the residual import are named in sections 4 and 5.

## 2. What ℓ¹ provides

One context. The weights are a function on the loci, so the algebra they see is the diagonal algebra Qⁿ (or Q(ζ_N)ⁿ once the QM-207 fiber is on), and every element of it commutes with every other. The phase cochain of QM-207 is itself diagonal.

**Theorem 2.1 (the fiber adds no second context). PROVED.** A diagonal phase matrix D commutes with the clock Z, which is diagonal; so the commutator holonomy of the pair (D, Z) is the identity. COMPUTED: `diagonal_pair_has_trivial_holonomy` is true. Likewise Z and Z² commute (`commuting_powers_have_trivial_holonomy`).

So weights plus fiber give a commutative algebra. Nothing in them produces a non-diagonal frame.

## 3. The finite invariant

**Theorem 3.1 (Weyl commutator holonomy). PROVED.** Let X be the shift and Z the clock on Q(ζ_N)^d, with ω = ζ_d. Then X^a Z^b X^{−a} Z^{−b} = ω^{−ab} · I. The value is central, a d-th root of unity, and equals I exactly when d | ab. Proof: Z X = ω X Z gives Z^b X^a = ω^{ab} X^a Z^b, so X^a Z^b X^{−a} Z^{−b} = ω^{−ab} I. COMPUTED: for d = 3 the exponents of the holonomy in μ₁₂ are [[0, 0, 0], [0, 8, 4], [0, 4, 8]]; for d = 4 they are [[0, 0, 0, 0], [0, 9, 6, 3], [0, 6, 0, 6], [0, 3, 6, 9]]; `trivial_exactly_when_d_divides_ab` and `values_are_dth_roots` are true in both dimensions.

In the language of the QM-207 note this is the holonomy of the 4-cycle of context transitions X-frame → Z-frame → X-frame → Z-frame, valued in the center μ_d.

**Theorem 3.2 (the invariant belongs to the pair, not to a frame). PROVED.** For any unitary V, (V X V†)(V Z V†)(V X V†)⁻¹(V Z V†)⁻¹ = V (X Z X⁻¹ Z⁻¹) V† = ω^{−1} I. COMPUTED for d = 4: base exponent 9 (ζ₁₂⁹ = −i), unchanged under conjugation by the Fourier matrix and by diagonal phases. The control refuses a non-unitary conjugating frame.

**Theorem 3.3 (Peres–Mermin parity obstruction). PROVED.** Take the nine two-qubit Pauli products IX, IZ, XI, XX, XZ, YY, ZI, ZX, ZZ and the six contexts (three rows, three columns of the magic square). Each observable lies in exactly one row and exactly one column, so the context–observable incidence matrix over F₂ is the vertex–edge incidence matrix of the complete bipartite graph K₃,₃ (contexts are vertices, observables are edges). K₃,₃ is connected, so that matrix has rank 6 − 1 = 5 and cokernel F₂ = H₀(K₃,₃; F₂); the cokernel map sends a vector of context parities to its total parity. A deterministic ±1 assignment to the nine observables, consistent with every context product, exists exactly when the total parity of the six context signs is 0, that is, when the product of the six signs is +1. The Peres–Mermin signs are [1, 1, 1, 1, 1, −1], product −1, parity 1: no assignment exists. COMPUTED over Q(i) and F₂: all six contexts commute, the signs and the product are as stated, rank 5, cokernel dimension 1, `assignment_exists` false, `obstruction_class_total_parity` 1. Even control: flipping one sign makes the F₂ system consistent and `f2_apply` reproduces the right-hand side from the returned solution.

Reading. Theorem 3.1 is the finite form of noncommutativity itself; Theorem 3.3 is the finite form of its consequence for values, and its coefficient group is Z/2, the same mechanism as the Kochen–Specker parity of the QM-210 note (every element in two contexts, odd sign total). That is a connection between two imports, not a reduction of one to the other.

## 4. Completion step

In finite dimension there is none: Theorems 3.1 to 3.3 are algebraic over Q(ζ₁₂), and the Peres–Mermin contexts need only Q(i). The completion that QM-209 names is topological. Density of the unitaries with entries in ∪_N Q(ζ_N) inside U(d) uses the topology of U(d); in infinite dimension the norm closure that makes B(H) a C*-algebra is a further import. Both are IMPORTED.

## 5. Residual import

A second, non-diagonal context. Theorem 2.1 shows that the weights and the fiber supply only the diagonal; once a non-diagonal frame such as the Fourier matrix is declared, the holonomy of Theorem 3.1 and the parity of Theorem 3.3 are computed. The declaration is the import. In the Peres–Mermin form the invariant also uses the two-qubit tensor product, so it depends on bipartite composition, which the manuscript already notes is absent from the five-item cascade; the Weyl form on one d-level system does not.

## 6. Three-layer table

| Layer | Status | Content |
| --- | --- | --- |
| finite invariant | COMPUTED | X^a Z^b X^{−a} Z^{−b} = ω^{−ab} I, trivial iff d | ab, conjugation invariant (d = 3, 4); Peres–Mermin F₂ system of rank 5 with cokernel H₀(K₃,₃; F₂), obstruction class the total parity 1, no assignment; even control solvable |
| completion | IMPORTED | density of ∪_N U(d; Q(ζ_N)) in U(d); norm closure of B(H) in infinite dimension |
| residual import | IMPORTED | a second, non-diagonal context; weights and fiber give one diagonal |

## 7. Negative controls

- Diagonal pair (D, Z) and the pair (Z, Z²): trivial holonomy, so commuting contexts read as the identity.
- Even Peres–Mermin control: one sign flipped, the F₂ system is consistent and the returned assignment checks against every context.
- Refusals: `f2_eliminate` refuses an entry outside {0, 1}; `conjugation_invariance` refuses a non-unitary frame.

## 8. What the control does not show

- No derivation of B(H), of infinite dimension, or of the specific contexts. The Fourier frame and the Pauli square are declared.
- The Peres–Mermin obstruction rules out deterministic noncontextual assignments on this finite set; it does not produce the quantum algebra from the obstruction.
- Independence from the other imports is not shown. The Peres–Mermin form uses composition; the Weyl form uses the fiber of QM-207 (ω is a root of unity).

## 9. Manuscript passage this bears on

Section 13.8, where same-party noncommutativity is called load-bearing for the maximal CHSH construction while cross-party observables commute. The finite invariant of same-party noncommutativity is the central root of unity of Theorem 3.1; the finite invariant of its consequence for values is the F₂ class of Theorem 3.3. Nothing in the manuscript is edited by this note.

## 10. Claim envelope

- Supports: on Q(ζ₁₂)^d for d = 3, 4, the Weyl commutator holonomy is ω^{−ab} I, trivial iff d | ab, and conjugation invariant; over F₂ the Peres–Mermin assignment system has rank 5, cokernel of dimension 1, and total parity 1, so no deterministic assignment exists, while flipping one sign makes it solvable; a diagonal phase cochain supplies no second context.
- Does not support: any derivation of a noncommutative algebra from weights; infinite-dimensional statements; independence of QM-209.
- Narrowest claim: on the declared finite carriers the QM-209 import splits into two exactly computed cycle invariants (μ_d and Z/2), an imported topological completion, and the imported second context.
- Next test: `cd omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm && PYTHONPATH=python python3 -m pytest tests/e2e/test_e2e_context_parity_control.py -q -p no:cacheprovider` (expect 7 passed).
