Status: AI-drafted, awaiting human review.

# Derivation Note: CT-LOCAL-MEDIATOR-ENTANGLEMENT-IMPORT

**Target Node:** `CT-LOCAL-MEDIATOR-ENTANGLEMENT-IMPORT` (Stage `CONSTRUCTOR_THEORY`, UUID `386edbd6-7df4-5ef3-9d65-53c4e3738576`)  
**Prior and current status:** `IMPORTED_ASSUMPTION` (unchanged)  
**Campaign outcome class:** Narrowed (a finite shadow is stated in Lean; the imported inference is not reduced to it and is not proved)  
**AuthorityEffect:** None.  
**Lean module:** `lean4/ConstructorTheoryMediatorEntanglement.lean`  
**Independent check:** `checks/independent/ct-local-mediator-entanglement-import.py`

---

## 1. Context

The node records the central inference of two 2017 proposals for testing the quantum nature of gravity:

1. C. Marletto and V. Vedral, Phys. Rev. Lett. 119, 240402 (2017), arXiv:1707.06036 (pp. 2-3).
2. S. Bose et al., Phys. Rev. Lett. 119, 240401 (2017), arXiv:1707.06050 (pp. 1-2).

The inference: if two quantum systems Q1 and Q2 start in a separable state, interact only locally through a mediating system M (no direct Q1-Q2 interaction), and end entangled, then M cannot be a classical medium. Marletto and Vedral define a classical medium in constructor theory (an information medium whose observables are compatible); Bose et al. argue that a mediator modelled by local operations and classical communication (LOCC) cannot create entanglement.

The repository has no gravity model and no model of the mediating system M. This note and the Lean module do not formalise the inference. They record a finite shadow that the inference uses: local linear operations do not raise Schmidt rank.

---

## 2. The finite shadow

### 2.1 Coefficient matrix and Schmidt rank

A pure bipartite vector with coefficients `c_ij` in a field K is stored as the matrix `M = (c_ij)`. Its Schmidt rank is the rank of `M`. For two qubits, `M` is 2x2 and `M` has rank at most 1 exactly when `det M = 0`, exactly when `M = a b^T`, a product vector.

### 2.2 One local linear map does not raise Schmidt rank (any finite dimension)

A linear map `A (x) B` on the pair acts on the coefficient matrix as `M -> A M B^T` (row-major vectorisation; the independent check verifies `(A (x) B) vec(M) = vec(A M B^T)` symbolically for 2x2). Since `rank(XY) <= rank(X)` and `rank(XY) <= rank(Y)`,

`rank(A M B^T) <= rank(A M) <= rank(M)`.

So a vector of Schmidt rank at most `r` is sent to a vector of Schmidt rank at most `r`, and a target of strictly larger Schmidt rank is not the image of `M` under any single pair `(A, B)`. This holds for every field and every finite index sets, rectangular `A`, `B` included.

### 2.3 Two qubits over Q(i): determinant and concurrence

For 2x2 matrices over the Gaussian rationals `Q(i)`: `det(A M B^T) = det(A) det(M) det(B)`. Hence `det M = 0` gives `det(A M B^T) = 0`.

With the squared concurrence defined as `C^2(M) = 4 |det M|^2` (the repository's definition, `FrontierEntanglingPhase.concurrenceSq`; for a normalised vector this is the usual concurrence squared, and the Lean definition is applied to every matrix):

- `psi_u = (1,1,1,u)/2` has `M_u = [[1,1],[1,u]]/2`, `det M_u = (u-1)/4`, `C^2 = |u-1|^2 / 4`.
- `u = 1` is the product vector `(1,1,1,1)/2`, `C^2 = 0`.
- For `u = (3+4i)/5`: `|u|^2 = 9/25 + 16/25 = 1`, `u - 1 = (-2+4i)/5`, `|u-1|^2 = 20/25 = 4/5`, `C^2 = (4/5)/4 = 1/5`.

Therefore no pair `(A, B)` of 2x2 matrices over `Q(i)` satisfies `A M_1 B^T = M_u` for `u != 1`, and for `u = (3+4i)/5` the concurrence gap between target and image is exactly 1/5.

---

## 3. What is proved

All Lean declarations compile under Lean 4.35.0 with only `propext`, `Classical.choice`, `Quot.sound` (rebuilt by the reviewer; see `dag/research/campaign_ct-local-mediator-entanglement-import_lean_replay.json`).

1. `schmidtRank_local_le`: for a field K, finite index types and matrices A, M, B, `rank(A M B^T) <= rank M`. `schmidtRank_le_one_preserved` and `schmidtRank_not_reachable` are corollaries. Scope: one linear local map applied to one pure bipartite vector.
2. `applyLocalOp_det`: `det(A M B^T) = det A * det M * det B` for 2x2 over `Q(i)`.
3. `local_op_preserves_product_det`, `local_op_concurrence_zero_of_separable`: a zero-determinant 2x2 matrix stays zero-determinant, with zero squared concurrence.
4. `M_entangled_concurrence`: squared concurrence of `psi_u` at `u = (3+4i)/5` is exactly 1/5. `M_entangled_det_nonzero`, `M_entangled_not_product`.
5. `no_local_op_produces_entangled_state`, `no_local_op_produces_phase_entangled_state`, `concurrence_gap_under_local_op`: no `(A, B)` maps `psi_1` to `psi_u` for `u != 1`; gap exactly 1/5 at the Pythagorean phase.
6. `classical_mediator_cannot_produce_entangled_state`: the same for a `ClassicalMediatorBranch`. This structure is, by definition, a pair of local operators `(A, B)`. The name is a label.
7. `reduction_of_mediated_entanglement_inference`: a map that is assumed (as a structure field) to preserve zero determinant does not send a zero-determinant matrix to a nonzero-determinant one. This restates the hypothesis. It is not evidence that any physical mediator satisfies it.

## 4. What is assumed (imported, not proved here)

1. Locality of the mediated interaction (Principle I) and the information-theoretic definition of a classical mediator.
2. That a classical mediator acts on Q1 + Q2 as LOCC. The Lean model of a "classical mediator branch" is a single deterministic pair of local operators; a real LOCC protocol has mixtures, conditioning and classical communication.
3. That the mediated interaction is described as in the cited papers (a gravitational phase gate in the proposal). No gravity model exists in the repository.

## 5. What is open

1. Mixed states: entanglement of a mixed state is not Schmidt rank; separability of a density matrix and its preservation under LOCC is not formalised.
2. Completely positive maps with ancillas, mixtures of branches, conditioning on classical communication.
3. The mediating system M: a global unitary on Q1 + M + Q2 and the reduced dynamics on Q1 + Q2. Nothing in the module relates a mediator to the local operations `(A, B)`.
4. The Marletto-Vedral constructor-theoretic statement (non-commuting observables whose union is not an information variable).
5. The link to `TFQ-0084` (gap route `FRO-R-BACK-CT-MEDIATOR-TO-TFQ0084`).
6. The unitary/trace-preserving restriction: the Lean statements allow arbitrary matrices, including non-invertible ones; normalisation is not tracked.
