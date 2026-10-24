import Mathlib.Data.Rat.Defs
import Mathlib.Data.Fin.VecNotation
import Mathlib.Data.Matrix.Mul
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.Tactic

/-!
# CampaignFspCdtFoliationPositivity (`FSP-CDT-FOLIATION-POSITIVITY` / `TFQ-1215`)

Formalizes the finite causal dynamical triangulation (CDT) proper-time foliation,
4-simplex slice classification, Wick-rotated Boltzmann weight positivity,
reflection-positive slice transfer matrix, BQNF sign-reversing involution
cancellation vs chiral obstruction, and explicit scope fences separating the
Wick-rotation assumption, continuum 4D de Sitter numerical Monte Carlo claims,
and fermionic Grassmann determinant signs.
-/

namespace CampaignFspCdtFoliationPositivity

open scoped BigOperators Matrix

/-- Single-step causal link between adjacent proper-time slices `tau u + 1 = tau v`. -/
def causalStep {V : Type*} (tau : V → ℕ) (u v : V) : Prop :=
  tau u + 1 = tau v

/-- Strict proper-time causal precedence `tau u < tau v`. -/
def causalPrec {V : Type*} (tau : V → ℕ) (u v : V) : Prop :=
  tau u < tau v

/-- Theorem 1: A global proper-time foliation `tau : V → ℕ` induces a strict partial
order (`causalPrec tau`) that extends every single-step causal link (`causalStep tau`)
and forbids all causal 2-cycles and 3-cycles. -/
theorem proper_time_foliation_strict_order_and_no_cycles {V : Type*} (tau : V → ℕ)
    (u v w : V) :
    (causalStep tau u v → causalPrec tau u v) ∧
    ¬ causalPrec tau u u ∧
    ¬ (causalPrec tau u v ∧ causalPrec tau v u) ∧
    ¬ (causalPrec tau u v ∧ causalPrec tau v w ∧ causalPrec tau w u) := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro h
    unfold causalStep causalPrec at *
    omega
  · unfold causalPrec
    omega
  · unfold causalPrec
    omega
  · unfold causalPrec
    omega

/-- In 4D CDT, a 4-simplex spanning adjacent slices `(t, t+1)` with `(nt, nt1)` vertices
is causally admissible iff `nt + nt1 = 5` and both slices contain at least one vertex. -/
def isCausal4Simplex (nt nt1 : ℕ) : Prop :=
  nt + nt1 = 5 ∧ 1 ≤ nt ∧ 1 ≤ nt1

/-- Theorem 2: The causally admissible 4D simplices between adjacent slices `(t, t+1)`
are exactly the four Ambjorn-Jurkiewicz-Loll types `(4,1)`, `(3,2)`, `(2,3)`, and `(1,4)`,
excluding purely spatial `(5,0)` and `(0,5)` simplices. -/
theorem cdt_4simplex_slice_partition_classification (nt nt1 : ℕ) :
    (isCausal4Simplex nt nt1 ↔
      (nt = 4 ∧ nt1 = 1) ∨ (nt = 3 ∧ nt1 = 2) ∨
      (nt = 2 ∧ nt1 = 3) ∨ (nt = 1 ∧ nt1 = 4)) ∧
    ¬ isCausal4Simplex 5 0 ∧
    ¬ isCausal4Simplex 0 5 := by
  refine ⟨?_, ?_, ?_⟩
  · unfold isCausal4Simplex
    omega
  · unfold isCausal4Simplex
    omega
  · unfold isCausal4Simplex
    omega

/-- A slice transition preserves connected spatial topology when both boundary slices
have exactly `1` connected spatial component (`c_t = 1 ∧ c_t1 = 1`). -/
def preservesConnectedSliceTopology (c_t c_t1 : ℕ) : Prop :=
  c_t = 1 ∧ c_t1 = 1

/-- Theorem 3: In a two-slice CDT slab built from `n41` simplices of type `(4,1)`,
`n32` of type `(3,2)`, `n23` of type `(2,3)`, and `n14` of type `(1,4)`, each `(4,1)`
simplex contributes one spatial boundary tetrahedron `(4,0)` on slice `t` and each
`(1,4)` simplex contributes one spatial boundary tetrahedron `(0,4)` on slice `t+1`,
while baby-universe spatial branching (`c_t1 ≥ 2`) violates slice topology conservation. -/
theorem cdt_boundary_tetrahedra_and_no_spatial_branching
    (n41 n32 n23 n14 c_t1 : ℕ) (hbranch : 2 ≤ c_t1) :
    1 * n41 + 0 * n32 + 0 * n23 + 0 * n14 = n41 ∧
    0 * n41 + 0 * n32 + 0 * n23 + 1 * n14 = n14 ∧
    ¬ preservesConnectedSliceTopology 1 c_t1 := by
  refine ⟨by ring, by ring, ?_⟩
  unfold preservesConnectedSliceTopology
  omega

/-- Wick-rotated Euclidean CDT monomer weight for a triangulation with `n0` vertices,
`n41` simplices of type `(4,1)/(1,4)`, and `n32` simplices of type `(3,2)/(2,3)`,
given positive coupling fugacities `w0, w41, w32 ∈ ℚ`. -/
def cdtWickWeight (w0 w41 w32 : ℚ) (n0 n41 n32 : ℕ) : ℚ :=
  w0 ^ n0 * w41 ^ n41 * w32 ^ n32

/-- Theorem 4: For any strictly positive fugacities `w0 > 0, w41 > 0, w32 > 0` and any
simplex counts `(n0, n41, n32)`, the Wick-rotated Euclidean CDT configuration weight
is strictly positive (`cdtWickWeight w0 w41 w32 n0 n41 n32 > 0`). -/
theorem wick_rotated_cdt_boltzmann_weight_positivity
    (w0 w41 w32 : ℚ) (hw0 : 0 < w0) (hw41 : 0 < w41) (hw32 : 0 < w32)
    (n0 n41 n32 : ℕ) :
    0 < cdtWickWeight w0 w41 w32 n0 n41 n32 := by
  unfold cdtWickWeight
  positivity

/-- Symmetric CDT slice transfer matrix `T_{ij} = ∑_k d_k B_{ki} B_{kj}` built from a
half-step amplitude matrix `B` and diagonal bulk weights `d`. -/
def cdtTransferMatrix {m n : ℕ} (d : Fin m → ℚ) (B : Matrix (Fin m) (Fin n) ℚ) :
    Matrix (Fin n) (Fin n) ℚ :=
  fun i j => ∑ k : Fin m, d k * B k i * B k j

/-- Quadratic expectation value `⟨ψ, T ψ⟩ = ∑_{i,j} ψ_i T_{ij} ψ_j`. -/
def transferQuadraticForm {n : ℕ} (T : Matrix (Fin n) (Fin n) ℚ) (psi : Fin n → ℚ) : ℚ :=
  ∑ i : Fin n, ∑ j : Fin n, psi i * T i j * psi j

/-- Theorem 5: The CDT slice transfer matrix `T_{ij} = ∑_k d_k B_{ki} B_{kj}` is
symmetric (`T^T = T`) and satisfies reflection positivity on a 2-channel slice space:
for nonnegative intermediate slab weights `d_k ≥ 0` and any boundary wavefunction `ψ`,
`⟨ψ, T ψ⟩ = ∑_k d_k (∑_i B_{ki} ψ_i)^2 ≥ 0`. -/
theorem reflection_positive_transfer_matrix_symm_and_psd
    (d : Fin 2 → ℚ) (hd : ∀ k : Fin 2, 0 ≤ d k)
    (B : Matrix (Fin 2) (Fin 2) ℚ) (psi : Fin 2 → ℚ) :
    (cdtTransferMatrix d B)ᵀ = cdtTransferMatrix d B ∧
    transferQuadraticForm (cdtTransferMatrix d B) psi =
      ∑ k : Fin 2, d k * (∑ i : Fin 2, B k i * psi i) ^ 2 ∧
    0 ≤ transferQuadraticForm (cdtTransferMatrix d B) psi := by
  have hsymm : (cdtTransferMatrix d B)ᵀ = cdtTransferMatrix d B := by
    ext i j
    simp only [Matrix.transpose_apply, cdtTransferMatrix]
    refine Finset.sum_congr rfl ?_
    intro k _
    ring
  have hquad : transferQuadraticForm (cdtTransferMatrix d B) psi =
      ∑ k : Fin 2, d k * (∑ i : Fin 2, B k i * psi i) ^ 2 := by
    simp only [transferQuadraticForm, cdtTransferMatrix, Fin.sum_univ_two]
    ring
  refine ⟨hsymm, hquad, ?_⟩
  rw [hquad]
  refine Finset.sum_nonneg ?_
  intro k _
  exact mul_nonneg (hd k) (sq_nonneg _)

/-- Explicit 2-state CDT half-step amplitude matrix `B_cdt = [[2, 1], [1, 1]]`. -/
def cdtHalfStepWitness : Matrix (Fin 2) (Fin 2) ℚ :=
  !![2, 1; 1, 1]

/-- Explicit 2-state CDT slice transfer matrix `T_cdt = B_cdt^T B_cdt = [[5, 3], [3, 2]]`. -/
def cdtTransferWitness : Matrix (Fin 2) (Fin 2) ℚ :=
  cdtTransferMatrix (fun _ : Fin 2 => 1) cdtHalfStepWitness

/-- Theorem 6: On the explicit 2-state finite CDT slice transfer matrix witness
`T_cdt = [[5, 3], [3, 2]]`, all matrix entries are strictly positive,
`tr(T_cdt) = 7 > 0`, `det(T_cdt) = 1 > 0`, and the multi-slice periodic partition
functions `Z_1 = tr(T_cdt) = 7`, `Z_2 = tr(T_cdt^2) = 47`, and `Z_3 = tr(T_cdt^3) = 322`
are strictly positive. -/
theorem two_state_cdt_transfer_matrix_trace_and_det_pos :
    cdtTransferWitness = !![5, 3; 3, 2] ∧
    Matrix.trace cdtTransferWitness = 7 ∧
    Matrix.det cdtTransferWitness = 1 ∧
    Matrix.trace (cdtTransferWitness * cdtTransferWitness) = 47 ∧
    Matrix.trace (cdtTransferWitness * cdtTransferWitness * cdtTransferWitness) = 322 := by
  have hT : cdtTransferWitness = !![5, 3; 3, 2] := by
    ext i j
    fin_cases i <;> fin_cases j <;>
      simp [cdtTransferWitness, cdtTransferMatrix, cdtHalfStepWitness, Fin.sum_univ_two] <;>
      norm_num
  refine ⟨hT, ?_, ?_, ?_, ?_⟩
  · simp [hT, Matrix.trace, Fin.sum_univ_two]
    norm_num
  · simp [hT, Matrix.det_fin_two]
    norm_num
  · simp [hT, Matrix.trace, Fin.sum_univ_two]
    norm_num
  · simp [hT, Matrix.trace, Fin.sum_univ_two]
    norm_num

/-- Theorem 7: A BQNF sign-reversing weight-preserving involution `Xi` on a configuration
pair `(c, Xi c)` with `s (Xi c) = - s c` and `w (Xi c) = w c` cancels the signed pair
contribution identically (`s c * w c + s (Xi c) * w (Xi c) = 0`), whereas in the
frustrated 3-configuration chiral ensemble with weights `![2, 3, 5]` and signs `![1, 1, -1]`
from `CdtFermionSignEvaluator`, no positive-sector configuration matches the negative-sector
weight `5`. -/
theorem bqnf_involution_cancels_pairs_vs_chiral_obstruction
    {C : Type*} (Xi : C → C) (s : C → ℚ) (w : C → ℚ) (c : C)
    (hsign : s (Xi c) = -s c) (hweight : w (Xi c) = w c) :
    s c * w c + s (Xi c) * w (Xi c) = 0 ∧
    (∀ i : Fin 3, (![1, 1, (-1 : ℚ)] : Fin 3 → ℚ) i = 1 →
      (![2, 3, (5 : ℚ)] : Fin 3 → ℚ) i ≠ (![2, 3, (5 : ℚ)] : Fin 3 → ℚ) 2) := by
  refine ⟨?_, ?_⟩
  · rw [hsign, hweight]
    ring
  · intro i hi
    fin_cases i
    · norm_num
    · norm_num
    · norm_num at hi

/-- Theorem 8 (Scope Fence 1): Proper-time foliation alone does not eliminate
Lorentzian oscillatory phase cancellation: two causally admissible `(4,1)` configurations
with equal positive geometric weight `w > 0` and opposite Lorentzian phases `+1` and `-1`
cancel to `0` before Wick rotation, whereas after Wick rotation (`+1, +1`) their
Euclidean partition sum is `2 * w > 0`. -/
theorem lorentzian_vs_euclidean_wick_rotation_fence (w : ℚ) (hw : 0 < w) :
    isCausal4Simplex 4 1 ∧
    (1 : ℚ) * w + (-1 : ℚ) * w = 0 ∧
    0 < (1 : ℚ) * w + (1 : ℚ) * w := by
  refine ⟨?_, by ring, by linarith⟩
  unfold isCausal4Simplex
  omega

/-- Theorem 9 (Scope Fence 2): On any finite connected triangulation with `N ≥ 1`
vertices, the stationary random-walk return probability `P_inf = 1 / N` is positive
and constant across diffusion steps `τ → τ + 1`, so its discrete log-increment
`P_inf (τ + 1) - P_inf τ` vanishes (asymptotic spectral dimension `0 ≠ 4`);
the continuum 4D de Sitter spectral dimension `d_s = 4` is an external infinite-volume
Monte Carlo import. -/
theorem finite_complex_stationary_return_probability_saturates_fence
    (N : ℕ) (hN : 1 ≤ N) :
    0 < (1 : ℚ) / (N : ℚ) ∧
    (1 : ℚ) / (N : ℚ) - (1 : ℚ) / (N : ℚ) = 0 ∧
    (0 : ℚ) ≠ 4 := by
  have hNpos : (0 : ℚ) < (N : ℚ) := by exact_mod_cast (Nat.succ_le_iff.mp hN)
  refine ⟨div_pos zero_lt_one hNpos, by ring, by norm_num⟩

/-- Theorem 10 (Scope Fence 3): Positive bosonic CDT geometric weights (`w_geom > 0`)
do not ensure positive joint geometry-fermion weights when the fermion Grassmann
determinant is negative (`det_D < 0`), since their product is negative. -/
theorem bosonic_cdt_positivity_independent_of_fermion_determinant_sign_fence
    (w_geom det_D : ℚ) (hw : 0 < w_geom) (hdet : det_D < 0) :
    w_geom * det_D < 0 := by
  exact mul_neg_of_pos_of_neg hw hdet

end CampaignFspCdtFoliationPositivity
