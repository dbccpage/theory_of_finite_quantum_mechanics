# QM-211 Continuous Unitary Dynamics: the Finite Map

**Scope:** research note for `finite_quantum_mechanics`; not part of the manuscript, not a claim promotion. Companion to `phase_fiber_holonomy_bridge_finite_map.md`.
**Code:** `python/finite_qm/use_cases/clock_tower_control.py`, tests in `tests/e2e/test_e2e_clock_tower_control.py` (6 tests).
**Status marks used:** PROVED (argument given here, finite and checkable), COMPUTED (exact arithmetic in Q(ζ₂₄), replayable), IMPORTED (added structure that nothing finite here produces), CONJECTURED (none in this note).

Authority status: none. This note changes no admitted claim.

## 1. The question

QM-211 names the fifth import: continuous unitary time evolution, a one-parameter group t ↦ U(t) = exp(−itH) with a self-adjoint generator, Stone's theorem in the infinite-dimensional theory. The task is to research and discover the finite map to this problem.

The finite map is a tower of clocks. A unitary of finite order over a cyclotomic field splits exactly into spectral projectors built from its own powers; its generator is an exponent vector with entries in Z/m, a class and not a number; refinement of the clock is possible exactly along divisibility of the orders. The completion step is the direct limit of the clocks to Q/Z-valued phase (algebraic), then the metric completion to R/Z and the passage to a one-parameter group. The residual import is strong continuity together with the unit that turns an exponent into an energy.

## 2. What ℓ¹ provides

Discrete stochastic steps on weights: a Markov matrix applied once per step. The swap S on two loci is both stochastic and unitary, so it is a clock of order 2 in either reading, and it separates the two readings at the first refinement.

**Theorem 2.1 (the stochastic clock has no half step; the unitary one does). PROVED.** Any R with R² = S commutes with S, and S has the distinct eigenvalues 1 and −1, so R = aI + bS; then R² = (a² + b²)I + 2ab S = S forces a² + b² = 0 and 2ab = 1. Eliminating b gives 4a⁴ + 1 = 0, which has no real root (even powers, nonnegative coefficients, constant term 1). For a row-stochastic R = [[p, 1−p], [q, 1−q]], the (1, 1) entry of R² is p² + (1−p)q, a sum of nonnegative terms, so R² = S forces p = q = 0, and the one candidate [[0, 1], [0, 1]] squares to itself, not to S. Over Q(i), V = ((1 + i)I + (1 − i)S)/2 is unitary and V² = S. COMPUTED: all six rational-root candidates ±1, ±1/2, ±1/4 of 4a⁴ + 1 are nonzero; V is unitary, V² = S, V has non-real entries; the forced stochastic candidate does not square to S.

So the ℓ¹ dynamics refines nowhere here, and the first refinement already needs the QM-207 fiber (the entries of V lie in Q(i)).

## 3. The finite invariant

Fix N = 24 and work in Q(ζ₂₄).

**Theorem 3.1 (finite spectral theorem). PROVED.** Let U be unitary with U^m = I, m | N. Put P_k = (1/m) Σ_{j=0}^{m−1} ζ_m^{−kj} U^j for k ∈ Z/m. Then the P_k are orthogonal idempotents summing to I, U P_k = ζ_m^k P_k, and U^t = Σ_k ζ_m^{kt} P_k for every t ∈ Z/m. Proof: the geometric sums Σ_j ζ_m^{(l−k)j} are m·[l = k], which gives P_k P_l = [k = l] P_k and Σ_k P_k = I; U P_k = ζ_m^k P_k by shifting the index j. The "Hermitian generator" is the exponent vector (k on the range of P_k), an element of (Z/m)^d: it is determined modulo m per eigenspace and not as an integer. COMPUTED: the Fourier matrix F₄ has order 4 and multiplicities [2, 1, 1, 0] on the exponents [0, 1, 2, 3] (eigenvalues 1, i, −1, −i with trace 1 + i); the shift X₄ has [1, 1, 1, 1]; the clock Z₃ has order 3 and [1, 1, 1]. For all three, the projectors sum to I, are orthogonal and idempotent, the multiplicities sum to the dimension, and the rebuilt U^t agrees with the matrix power for every t.

**Theorem 3.2 (square roots inside the algebra of U). PROVED.** With 2m | N, the square roots of U in Q(ζ_N)[U] are Σ_k ε_k ζ_{2m}^k P_k with ε_k = ±1 on each occupied eigenspace, so their number is 2^{occupied}, all unitary and distinct. COMPUTED: 8 roots for F₄ (three occupied eigenspaces), 16 for X₄ (four), 8 for Z₃ (three); each squares to U and is unitary. The control refuses a conductor that does not contain the half step.

**Theorem 3.3 (refinement along divisibility only). PROVED.** A clock of order m′ with the same eigenspace structure refines a clock of order m, meaning some power of it equals the coarser clock on each eigenspace, exactly when m | m′, with step k = m′/m. COMPUTED: ζ₄ and ζ₃ refine neither the other; ζ₁₂ refines ζ₃ with k = 4 and ζ₄ with k = 3; ζ₂₄ refines ζ₁₂ with k = 2 (`chain_condition_is_divisibility`). The existing refinement tower of orders 3, 6, 12 is exact: each clock has its stated order and no smaller one, and each half step squares to the previous clock; eigenphase exponents [0, 1, 2], [0, …, 5], [0, …, 11].

Reading. The finite invariant of QM-211 is a consistent tower of cyclic clocks, each a μ_m-valued eigenphase assignment, with the exponent vector as the finite stand-in for a generator. It is a cycle invariant of each clock's own cyclic group, which is why it sits beside the other holonomies in the QM-207 table.

## 4. Completion step

Two steps, both imported. First, the direct limit of the clocks along divisibility, lim (1/m)Z/Z = Q/Z, which is algebraic and needs no topology: every finite tower lives in some Q(ζ_N). Second, the metric completion Q/Z → R/Z and the passage from a consistent tower to a one-parameter group t ↦ U(t) with t ∈ R; Stone's theorem then identifies strongly continuous one-parameter unitary groups with self-adjoint generators. The second step is the Cauchy completion of the QM-207 note applied to the phase of the clock. IMPORTED.

## 5. Residual import

Strong continuity of t ↦ U(t), and the action unit. The exponent vector of Theorem 3.1 carries no unit; turning k/m ∈ Q/Z into an energy needs a scale that no finite datum fixes. A second residual is the branch choice: each refinement picks one of 2^{occupied} square roots (Theorem 3.2), so the tower is extra data beyond U, and the generator is defined only once the tower is.

## 6. Three-layer table

| Layer | Status | Content |
| --- | --- | --- |
| finite invariant | COMPUTED | spectral projectors from powers of U; multiplicities [2, 1, 1, 0], [1, 1, 1, 1], [1, 1, 1]; U^t rebuilt for all t ∈ Z/m; 2^{occupied} square roots (8, 16, 8); refinement iff m | m′ (ζ₄ ∤ ζ₃, ζ₁₂ over ζ₃ and ζ₄, ζ₂₄ over ζ₁₂); tower 3, 6, 12 exact |
| completion | IMPORTED | direct limit to Q/Z (algebraic), then metric completion to R/Z and the one-parameter group; Stone adds strong continuity |
| residual import | IMPORTED | strong continuity and the action unit; the branch choice at each refinement |

## 7. Negative controls

- The stochastic swap: no real square root (4a⁴ + 1 has no rational root among its candidates and is at least 1 on the reals), no stochastic square root (the forced candidate squares to itself), one unitary square root over Q(i) displayed.
- Refusals: `matrix_order` refuses when no order up to the bound is found (the shift of order 4 with bound 3); `finite_spectral_theorem` refuses a non-unitary input (twice the identity); `clock_square_roots` refuses when 2m does not divide the conductor (the shift of order 4 in Q(ζ₁₂) is accepted as a clock but refused for roots at conductor 12); `refines` refuses orders that do not divide the conductor; the evaluation refuses a conductor not divisible by 24.

## 8. What the control does not show

- No Hamiltonian is derived and no continuity is established. The exponent vector is a class in (Z/m)^d, and the passage to a real generator is the imported completion.
- The tower is a choice. Nothing finite here prefers one square root over another.
- The manuscript's discrete dynamics (finite clocks, Z/m steps) are not changed; the control agrees with the existing `clock_refinement_tower` and adds the spectral and root census.
- Independence from the other imports is not shown; the first refinement of the stochastic clock already uses the QM-207 fiber.

## 9. Manuscript passage this bears on

Section 13.8, where complex phase and continuous dynamics are said to belong to the larger theory and not to the static Bell minimum. The control agrees: the finite dynamics is a clock tower with exact spectral data, and continuity enters only through the imported completion. Nothing in the manuscript is edited by this note.

## 10. Claim envelope

- Supports: over Q(ζ₂₄), the finite spectral theorem holds exactly for F₄, X₄ and Z₃ with the stated multiplicities; the square roots in the algebra of U number 2^{occupied}; clocks refine exactly along divisibility; the stochastic swap has a unitary half step over Q(i) and no real or stochastic one.
- Does not support: Stone's theorem; any derivation of continuity, of a generator with a unit, or of a preferred tower; independence of QM-211.
- Narrowest claim: on the declared finite carriers the QM-211 import splits into an exactly computed clock tower, an imported two-step completion (direct limit, then metric), and the imported strong continuity and unit.
- Next test: `cd sources/atlas/papers/finite_quantum_mechanics && PYTHONPATH=python python3 -m pytest tests/e2e/test_e2e_clock_tower_control.py -q -p no:cacheprovider` (expect 6 passed).
