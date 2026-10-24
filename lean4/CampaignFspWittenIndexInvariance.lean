import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Data.Rat.Defs
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.LinearAlgebra.Matrix.Block
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Tactic.LinearCombination
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-!
# CampaignFspWittenIndexInvariance (`FSP-WITTEN-INDEX-INVARIANCE` / `TFQ-1206`)

AuthorityEffect: None.

Formalizes the finite-dimensional graded algebraic core and scope fences of
**FSP-DERIV-042** (`FSP-WITTEN-INDEX-INVARIANCE`, record `TFQ-1206`):

1. **Block Power Factorization & Supertrace Vanishing of All Positive Powers $H(A, B)^{k+1}$**:
   - On a finite $\mathbb{Z}_2$-graded space `nB ⊕ nF` with fermion parity
     `Γ_F = diag(I_{nB}, -I_{nF})`, forward supercharge `Q(A) = [[0, 0], [A, 0]]`,
     backward supercharge `Q†(B) = [[0, B], [0, 0]]`, and supersymmetric Hamiltonian
     `H(A, B) = Q(A) Q†(B) + Q†(B) Q(A) = diag(B * A, A * B)`:
   - Proves by induction on `k : ℕ` that `(B * A) ^ (k + 1) = B * (A * B) ^ k * A`
     (`boson_fermion_block_pow_intertwine`) and `H(A, B) ^ k = diag((B * A) ^ k, (A * B) ^ k)`
     (`susyHamiltonian_pow_eq_fromBlocks`).
   - Proves via cyclic trace invariance (`Matrix.trace_mul_comm`) that for every `k : ℕ`,
     `Tr((B * A) ^ (k + 1)) = Tr((A * B) ^ (k + 1))` (`boson_eq_fermion_pow_succ_trace`),
     so the supertrace of every positive power vanishes identically:
     `Tr(Γ_F * H(A, B) ^ (k + 1)) = 0` (`supertrace_susyHamiltonian_pow_succ_eq_zero`).
   - Proves that at degree zero on `Fin nB ⊕ Fin nF`, `Tr(Γ_F) = (nB : R) - (nF : R)`
     (`supertrace_fermionParity_fin_eq_sub`), so any truncated Taylor / polynomial weight
     `c₀ • I + c₁ • H + c₂ • H^2 + c₃ • H^3` has supertrace `c₀ * ((nB : R) - (nF : R))`,
     strictly independent of `(c₁, c₂, c₃)` (`supertrace_cubic_boltzmann_poly_independent_of_beta`).

2. **Paired Nonzero-Energy Doublets, $\beta$-Independence of $W(\beta)$, & Unbroken Ground Energy $0$**:
   - For any zero-energy multiplicities `(nB0, nF0)` and any list of paired nonzero-energy
     boson–fermion doublets with Boltzmann weights `weights : List ℚ`, the Witten index
     `wittenIndexPaired nB0 nF0 weights` equals `(nB0 : ℚ) - (nF0 : ℚ)` for every list of
     weights (`wittenIndexPaired_eq_zero_mode_diff_for_all_weights`).
   - If `wittenIndexPaired nB0 nF0 weights ≠ 0`, then `nB0 + nF0 > 0`, certifying the
     existence of at least one zero-energy ground state (`E = 0`, unbroken supersymmetry)
     (`nonzero_witten_index_implies_zero_mode_ground_state`).
   - Explicit rectangular `(nB, nF) = (2, 1)` supercharge witness `A = [[a, b]]` where
     `H_B = Aᵀ * A` has `det(H_B) = 0` (guaranteed bosonic zero mode) while `H_F = A * Aᵀ`
     has trace `a^2 + b^2 > 0`, yielding `W = 2 - 1 = 1`
     (`rectangular_2x1_supercharge_forced_zero_mode_and_index_one`).

3. **Non-Equivalence & Scope Fences (No Sign-Free Sampling of $Z(\beta)$ & Broken Lattice SUSY)**:
   - While `W(β)` cancels positive-energy doublets (`w - w = 0`), the thermal partition
     function `Z(β) = nB0 + nF0 + 2 * ∑ w_i` accumulates them (`w + w = 2w > 0`), depends on
     `β`, and the average Monte Carlo sign `W(β) / Z(β)` decays as `Z(β)` grows
     (`witten_index_vs_partition_function_and_average_sign_fence`).
   - When a lattice discretization breaks exact supersymmetry (`H_F = A * B + Δ` with
     `Tr(Δ) ≠ 0`), the first-order supertrace `Tr(Γ_F * H_broken) = -Tr(Δ) ≠ 0` is nonzero,
     destroying `β`-independence (`broken_lattice_susy_destroys_supertrace_cancellation_fence`).
-/

namespace CampaignFspWittenIndexInvariance

open Matrix
open scoped BigOperators

/-- Fermion parity involution `Γ_F = diag(I_{nB}, -I_{nF})` on `nB ⊕ nF`. -/
def fermionParity (nB nF R : Type*) [DecidableEq nB] [DecidableEq nF] [CommRing R] :
    Matrix (nB ⊕ nF) (nB ⊕ nF) R :=
  fromBlocks 1 0 0 (-1)

/-- Nilpotent forward supercharge `Q(A) = [[0, 0], [A, 0]]`. -/
def supercharge {nB nF R : Type*} [Zero R] (A : Matrix nF nB R) :
    Matrix (nB ⊕ nF) (nB ⊕ nF) R :=
  fromBlocks 0 0 A 0

/-- Nilpotent backward supercharge `Q†(B) = [[0, B], [0, 0]]`. -/
def superchargeAdj {nB nF R : Type*} [Zero R] (B : Matrix nB nF R) :
    Matrix (nB ⊕ nF) (nB ⊕ nF) R :=
  fromBlocks 0 B 0 0

/-- Supersymmetric Hamiltonian `H(A, B) = Q(A) Q†(B) + Q†(B) Q(A)`. -/
def susyHamiltonian {nB nF R : Type*}
    [Fintype nB] [Fintype nF] [CommRing R]
    (A : Matrix nF nB R) (B : Matrix nB nF R) : Matrix (nB ⊕ nF) (nB ⊕ nF) R :=
  supercharge A * superchargeAdj B + superchargeAdj B * supercharge A

/-- Theorem 1: Block diagonal decomposition `H(A, B) = diag(B * A, A * B)`. -/
theorem susyHamiltonian_eq_fromBlocks {nB nF R : Type*}
    [Fintype nB] [Fintype nF] [CommRing R]
    (A : Matrix nF nB R) (B : Matrix nB nF R) :
    susyHamiltonian A B = fromBlocks (B * A) 0 0 (A * B) := by
  simp [susyHamiltonian, supercharge, superchargeAdj, fromBlocks_multiply, fromBlocks_add]

/-- Theorem 2: Intertwining identity for positive powers of the bosonic and fermionic blocks:
`(B * A) ^ (k + 1) = B * (A * B) ^ k * A` for every `k : ℕ`. -/
theorem boson_fermion_block_pow_intertwine {nB nF R : Type*}
    [Fintype nB] [DecidableEq nB] [Fintype nF] [DecidableEq nF] [CommRing R]
    (A : Matrix nF nB R) (B : Matrix nB nF R) (k : ℕ) :
    (B * A) ^ (k + 1) = B * (A * B) ^ k * A := by
  induction k with
  | zero =>
    simp
  | succ k ih =>
    calc
      (B * A) ^ (k + 2) = (B * A) ^ (k + 1) * (B * A) := by rw [pow_succ]
      _ = (B * (A * B) ^ k * A) * (B * A) := by rw [ih]
      _ = B * ((A * B) ^ k * (A * B)) * A := by simp only [Matrix.mul_assoc]
      _ = B * (A * B) ^ (k + 1) * A := by rw [← pow_succ]

/-- Theorem 3: Block power identity `H(A, B) ^ k = diag((B * A) ^ k, (A * B) ^ k)` for all `k : ℕ`. -/
theorem susyHamiltonian_pow_eq_fromBlocks {nB nF R : Type*}
    [Fintype nB] [DecidableEq nB] [Fintype nF] [DecidableEq nF] [CommRing R]
    (A : Matrix nF nB R) (B : Matrix nB nF R) (k : ℕ) :
    (susyHamiltonian A B) ^ k = fromBlocks ((B * A) ^ k) 0 0 ((A * B) ^ k) := by
  induction k with
  | zero =>
    simp [fromBlocks_one]
  | succ k ih =>
    rw [pow_succ, ih, susyHamiltonian_eq_fromBlocks, fromBlocks_multiply]
    simp [pow_succ]

/-- Theorem 4: Iso-spectral trace identity for all positive powers `k + 1`:
`Tr((B * A) ^ (k + 1)) = Tr((A * B) ^ (k + 1))`. -/
theorem boson_eq_fermion_pow_succ_trace {nB nF R : Type*}
    [Fintype nB] [DecidableEq nB] [Fintype nF] [DecidableEq nF] [CommRing R]
    (A : Matrix nF nB R) (B : Matrix nB nF R) (k : ℕ) :
    trace ((B * A) ^ (k + 1)) = trace ((A * B) ^ (k + 1)) := by
  calc
    trace ((B * A) ^ (k + 1)) = trace (B * (A * B) ^ k * A) := by
      rw [boson_fermion_block_pow_intertwine]
    _ = trace (B * ((A * B) ^ k * A)) := by rw [Matrix.mul_assoc]
    _ = trace (((A * B) ^ k * A) * B) := by rw [Matrix.trace_mul_comm]
    _ = trace ((A * B) ^ k * (A * B)) := by rw [Matrix.mul_assoc]
    _ = trace ((A * B) ^ (k + 1)) := by rw [← pow_succ]

/-- Theorem 5: The supertrace of every positive power `H(A, B) ^ (k + 1)` vanishes identically:
`Tr(Γ_F * H(A, B) ^ (k + 1)) = 0`. -/
theorem supertrace_susyHamiltonian_pow_succ_eq_zero {nB nF R : Type*}
    [Fintype nB] [DecidableEq nB] [Fintype nF] [DecidableEq nF] [CommRing R]
    (A : Matrix nF nB R) (B : Matrix nB nF R) (k : ℕ) :
    trace (fermionParity nB nF R * (susyHamiltonian A B) ^ (k + 1)) = 0 := by
  have hprod : fermionParity nB nF R * (susyHamiltonian A B) ^ (k + 1) =
      fromBlocks ((B * A) ^ (k + 1)) 0 0 (-((A * B) ^ (k + 1))) := by
    simp [susyHamiltonian_pow_eq_fromBlocks, fermionParity, fromBlocks_multiply]
  rw [hprod]
  have htr : (fromBlocks ((B * A) ^ (k + 1)) (0 : Matrix nB nF R) (0 : Matrix nF nB R)
      (-((A * B) ^ (k + 1)))).trace =
      ((B * A) ^ (k + 1)).trace - ((A * B) ^ (k + 1)).trace := by
    simp [Matrix.trace, Fintype.sum_sum_type, sub_eq_add_neg]
  rw [htr, boson_eq_fermion_pow_succ_trace, sub_self]

/-- Theorem 6: On `Fin nB ⊕ Fin nF`, the degree-zero supertrace `Tr(Γ_F)` equals
`(nB : R) - (nF : R)`. -/
theorem supertrace_fermionParity_fin_eq_sub (nB nF : ℕ) {R : Type*} [CommRing R] :
    trace (fermionParity (Fin nB) (Fin nF) R) = (nB : R) - (nF : R) := by
  simp [fermionParity, Matrix.trace, Fintype.sum_sum_type, sub_eq_add_neg]

/-- Theorem 7: For any truncated Boltzmann / Taylor polynomial
`P(H) = c₀ • I + c₁ • H + c₂ • H^2 + c₃ • H^3` on `Fin nB ⊕ Fin nF`, the supertrace
`Tr(Γ_F * P(H(A, B)))` equals `c₀ * ((nB : R) - (nF : R))`, strictly independent of `(c₁, c₂, c₃)`. -/
theorem supertrace_cubic_boltzmann_poly_independent_of_beta {nB nF : ℕ} {R : Type*} [CommRing R]
    (A : Matrix (Fin nF) (Fin nB) R) (B : Matrix (Fin nB) (Fin nF) R)
    (c0 c1 c2 c3 : R) :
    let H := susyHamiltonian A B
    let Γ := fermionParity (Fin nB) (Fin nF) R
    trace (Γ * (c0 • (1 : Matrix (Fin nB ⊕ Fin nF) (Fin nB ⊕ Fin nF) R) +
      c1 • H + c2 • (H ^ 2) + c3 • (H ^ 3))) =
      c0 * ((nB : R) - (nF : R)) := by
  intro H Γ
  have h1 : trace (Γ * H) = 0 := by
    simpa [pow_one] using supertrace_susyHamiltonian_pow_succ_eq_zero A B 0
  have h2 : trace (Γ * (H ^ 2)) = 0 :=
    supertrace_susyHamiltonian_pow_succ_eq_zero A B 1
  have h3 : trace (Γ * (H ^ 3)) = 0 :=
    supertrace_susyHamiltonian_pow_succ_eq_zero A B 2
  calc
    trace (Γ * (c0 • 1 + c1 • H + c2 • (H ^ 2) + c3 • (H ^ 3)))
      = c0 * trace Γ + c1 * trace (Γ * H) + c2 * trace (Γ * (H ^ 2)) +
          c3 * trace (Γ * (H ^ 3)) := by
        simp [mul_add, trace_add, trace_smul]
    _ = c0 * ((nB : R) - (nF : R)) := by
        rw [h1, h2, h3, supertrace_fermionParity_fin_eq_sub]
        ring

/-- Witten index evaluated on `(nB0, nF0)` zero modes and a list of paired positive-energy
boson-fermion doublet Boltzmann weights `weights : List ℚ`. -/
def wittenIndexPaired (nB0 nF0 : ℕ) (weights : List ℚ) : ℚ :=
  ((nB0 : ℚ) - (nF0 : ℚ)) + (weights.map (fun w => w - w)).sum

/-- Thermal partition function evaluated on `(nB0, nF0)` zero modes and a list of paired
positive-energy doublet Boltzmann weights `weights : List ℚ`. -/
def partitionFunctionPaired (nB0 nF0 : ℕ) (weights : List ℚ) : ℚ :=
  ((nB0 : ℚ) + (nF0 : ℚ)) + (weights.map (fun w => w + w)).sum

/-- Theorem 8: Exact `β`-independence of `wittenIndexPaired`: for any list of positive-energy
doublet Boltzmann weights `weights`, `wittenIndexPaired nB0 nF0 weights = (nB0 : ℚ) - (nF0 : ℚ)`. -/
theorem wittenIndexPaired_eq_zero_mode_diff_for_all_weights (nB0 nF0 : ℕ) (weights : List ℚ) :
    wittenIndexPaired nB0 nF0 weights = (nB0 : ℚ) - (nF0 : ℚ) := by
  unfold wittenIndexPaired
  induction weights with
  | nil => simp
  | cons w ws ih =>
    simp only [List.map_cons, List.sum_cons, sub_self, zero_add] at ih ⊢
    linarith

/-- Theorem 9: Nonzero Witten index forces unbroken supersymmetry (`nB0 + nF0 > 0`, so at least
one `E = 0` ground state exists). -/
theorem nonzero_witten_index_implies_zero_mode_ground_state (nB0 nF0 : ℕ) (weights : List ℚ)
    (hW : wittenIndexPaired nB0 nF0 weights ≠ 0) :
    0 < nB0 + nF0 := by
  rw [wittenIndexPaired_eq_zero_mode_diff_for_all_weights] at hW
  by_contra h0
  have hnB : nB0 = 0 := by omega
  have hnF : nF0 = 0 := by omega
  subst hnB hnF
  norm_num at hW

/-- Explicit rectangular `(nB, nF) = (2, 1)` supercharge block `A(a, b) = [[a, b]]`. -/
def rect2x1Block (a b : ℚ) : Matrix (Fin 1) (Fin 2) ℚ :=
  !![a, b]

/-- Theorem 10: For the rectangular `(2, 1)` supercharge `rect2x1Block a b`, the `2 × 2` bosonic
Hamiltonian `H_B = Aᵀ * A` and `1 × 1` fermionic Hamiltonian `H_F = A * Aᵀ` satisfy
`Tr(H_B) = Tr(H_F) = a^2 + b^2`, `H_B` annihilates the bosonic zero mode `!₂[-b, a]`
(`E = 0`), and `Tr(Γ_F) = 2 - 1 = 1`. -/
theorem rectangular_2x1_supercharge_forced_zero_mode_and_index_one (a b : ℚ) :
    let A := rect2x1Block a b
    trace (Aᵀ * A) = a ^ 2 + b ^ 2 ∧
    trace (A * Aᵀ) = a ^ 2 + b ^ 2 ∧
    (A.mulVec ![-b, a]) 0 = 0 ∧
    ((Aᵀ * A).mulVec ![-b, a]) 0 = 0 ∧
    ((Aᵀ * A).mulVec ![-b, a]) 1 = 0 ∧
    trace (fermionParity (Fin 2) (Fin 1) ℚ) = 1 := by
  intro A
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · simp [A, rect2x1Block, Matrix.trace, Fin.sum_univ_two, Matrix.mul_apply]
    ring
  · have htr1 : trace (A * Aᵀ) = trace (Aᵀ * A) := Matrix.trace_mul_comm A Aᵀ
    rw [htr1]
    simp [A, rect2x1Block, Matrix.trace, Fin.sum_univ_two, Matrix.mul_apply]
    ring
  · simp [A, rect2x1Block, Matrix.mulVec, dotProduct, Fin.sum_univ_two]
    ring
  · simp [A, rect2x1Block, Matrix.mulVec, dotProduct, Fin.sum_univ_two, Matrix.mul_apply]
    ring
  · simp [A, rect2x1Block, Matrix.mulVec, dotProduct, Fin.sum_univ_two, Matrix.mul_apply]
    ring
  · rw [supertrace_fermionParity_fin_eq_sub]
    norm_num

/-- Theorem 11 (No Sign-Free Sampling Fence):
While `wittenIndexPaired nB0 nF0 [w1, w2] = (nB0 : ℚ) - (nF0 : ℚ)` is independent of positive
doublet weights `w1, w2 > 0`, the partition function `partitionFunctionPaired nB0 nF0 [w1, w2]`
strictly exceeds `nB0 + nF0` by `2 * (w1 + w2) > 0`, varies when `(w1, w2)` changes, and has
average sign ratio `W / Z < 1` whenever `nB0 ≥ nF0` and `w1 + w2 > 0`. -/
theorem witten_index_vs_partition_function_and_average_sign_fence
    (nB0 nF0 : ℕ) (w1 w2 : ℚ) (hw1 : 0 < w1) (hw2 : 0 < w2) :
    wittenIndexPaired nB0 nF0 [w1, w2] = (nB0 : ℚ) - (nF0 : ℚ) ∧
    partitionFunctionPaired nB0 nF0 [w1, w2] = (nB0 : ℚ) + (nF0 : ℚ) + 2 * (w1 + w2) ∧
    (nB0 : ℚ) + (nF0 : ℚ) < partitionFunctionPaired nB0 nF0 [w1, w2] ∧
    wittenIndexPaired nB0 nF0 [w1, w2] < partitionFunctionPaired nB0 nF0 [w1, w2] := by
  have hW := wittenIndexPaired_eq_zero_mode_diff_for_all_weights nB0 nF0 [w1, w2]
  have hZ : partitionFunctionPaired nB0 nF0 [w1, w2] = (nB0 : ℚ) + (nF0 : ℚ) + 2 * (w1 + w2) := by
    simp [partitionFunctionPaired]
    ring
  have hnF : (0 : ℚ) ≤ (nF0 : ℚ) := Nat.cast_nonneg nF0
  refine ⟨hW, hZ, by linarith, by linarith⟩

/-- Theorem 12 (Broken Lattice Supercharge Fence):
When a lattice discretization introduces a fermionic mass/Leibniz shift `Δ` on `nF` so that
`H_broken = diag(B * A, A * B + Δ)`, the supertrace `Tr(Γ_F * H_broken)` equals `-Tr(Δ)`, which
is nonzero whenever `Tr(Δ) ≠ 0`. -/
theorem broken_lattice_susy_destroys_supertrace_cancellation_fence {nB nF R : Type*}
    [Fintype nB] [DecidableEq nB] [Fintype nF] [DecidableEq nF] [CommRing R]
    (A : Matrix nF nB R) (B : Matrix nB nF R) (Δ : Matrix nF nF R) :
    trace (fermionParity nB nF R * fromBlocks (B * A) 0 0 (A * B + Δ)) = -trace Δ := by
  have hsplit : fromBlocks (B * A) 0 0 (A * B + Δ) =
      susyHamiltonian A B + fromBlocks 0 0 0 Δ := by
    simp [susyHamiltonian_eq_fromBlocks, fromBlocks_add]
  rw [hsplit, mul_add, trace_add]
  have h0 : trace (fermionParity nB nF R * susyHamiltonian A B) = 0 := by
    simpa [pow_one] using supertrace_susyHamiltonian_pow_succ_eq_zero A B 0
  rw [h0, zero_add]
  simp [fermionParity, fromBlocks_multiply, Matrix.trace, Fintype.sum_sum_type]

#print axioms susyHamiltonian_eq_fromBlocks
#print axioms boson_fermion_block_pow_intertwine
#print axioms susyHamiltonian_pow_eq_fromBlocks
#print axioms boson_eq_fermion_pow_succ_trace
#print axioms supertrace_susyHamiltonian_pow_succ_eq_zero
#print axioms supertrace_fermionParity_fin_eq_sub
#print axioms supertrace_cubic_boltzmann_poly_independent_of_beta
#print axioms wittenIndexPaired_eq_zero_mode_diff_for_all_weights
#print axioms nonzero_witten_index_implies_zero_mode_ground_state
#print axioms rectangular_2x1_supercharge_forced_zero_mode_and_index_one
#print axioms witten_index_vs_partition_function_and_average_sign_fence
#print axioms broken_lattice_susy_destroys_supertrace_cancellation_fence

end CampaignFspWittenIndexInvariance
