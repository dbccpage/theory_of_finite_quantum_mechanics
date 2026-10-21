import OAI.Analysis.MutuallyUnbiased.Model
import Conjecture2GeneralMechanization
import MubMonomialTransport

/-!
# Bridge from OpenAI's mutually-unbiased-bases model to this repository's matrix types

AuthorityEffect: None.

BUILD STATUS (2026-10-21): PENDING. This file was written and partly type-checked against Lean 4.35.0 and
Mathlib v4.35.0 (the first run reported two parse errors (misplaced parentheses) and the errors that followed from them;
the parentheses are fixed here but the file has not been re-run). The machine ran out of disk, so no complete build and no `#print axioms` output exists. The file is
deliberately not a lake root and is not part of the default target.

It imports `OAI.Analysis.MutuallyUnbiased.Model` from OpenAI's repository, which is NOT vendored here:
https://github.com/openai/math, commit 1581d4cbdd69a0faf34b2089614fe2a814316a6a (Apache-2.0), path
`lean/OAI/Analysis/MutuallyUnbiased/Model.lean` (`lean-toolchain` v4.34.1, Mathlib pinned at
d13f23b723b8a846827a245b89c10fc7d3f11612). `Model.lean` alone (1.7 kB) compiled without messages under this
repository's Lean 4.35.0 / Mathlib v4.35.0, so the model layer has no toolchain mismatch. See
`papers/core/mub6/documentation/openai_mub6_le5_external_import.md`.

`OAI.MUB6.Attainable n` says that there are `n` orthonormal bases `OrthonormalBasis (Fin 6) ℂ
(EuclideanSpace ℂ (Fin 6))` that are pairwise mutually unbiased. This repository states MU families as
unitary `6 × 6` complex matrices (`ConcreteMubPolynomialSystem.Candidate`, `SzollosiQuartetSystem.Quartet`,
`MonomialTransport.RawMU`). This file contains

* `attainable_iff`: the two notions coincide, for every `n`;
* `rawMU_iff_pairMU`: the repository's raw (Hadamard, unnormalised) overlap `6` is the normalised `1/6`;
* `mub6_family_le_five`: every pairwise MU family of unitary `6 × 6` matrices has at most five members,
  *given* `OpenAIFamilyBound`, the exact statement of the upstream theorem `OAI.MUB6.family_size_le_five`.
  The upstream proof (3381 files, about 205 MB of Lean source) is not imported here, so the bound is an
  external, imported theorem and the conclusion is conditional on it;
* `tao_phase_bridge`: the repository's Tao phase table `phaseTable` is OpenAI's `taoExponent` after the
  index involution `taoPerm = (3 5)`, so the `taoNormSq = 9` evaluation concerns the very matrix that
  OpenAI's Fourier-vanishing theorem singles out as the exception. An exact search over all index
  permutations found 20 (permutation, sign) solutions; `taoPerm` is one of them.
-/

namespace MUB.OpenAIBridge

open scoped BigOperators ComplexConjugate

/-- A candidate basis: a complex `6 × 6` matrix (the repository's `Candidate`). -/
abbrev Cand := Matrix (Fin 6) (Fin 6) ℂ

/-- Pairwise MU family of unitary matrices, in the form used by `SzollosiQuartetSystem.Quartet`:
`Bᵃᴴ Bᵃ = 1` and `|(Bᵃᴴ Bᵇ)ᵢⱼ|² = 1/6` for `a ≠ b`. -/
def MatrixMUBFamily {n : ℕ} (B : Fin n → Cand) : Prop :=
  (∀ a, (B a).conjTranspose * B a = 1) ∧
    ∀ a b, a ≠ b → ∀ i j, Complex.normSq (((B a).conjTranspose * B b) i j) = 1 / 6

/-! ## Matrices versus orthonormal bases -/

/-- Column `j` of a matrix as a vector of `EuclideanSpace ℂ (Fin 6)`. -/
def colVec (M : Cand) (j : Fin 6) : OAI.MUB6.Space :=
  WithLp.toLp 2 (fun k => M k j)

/-- The matrix whose column `j` is the vector `b j`. -/
def mat (b : Fin 6 → OAI.MUB6.Space) : Cand := fun k j => b j k

theorem inner_colVec (M N : Cand) (i j : Fin 6) :
    inner ℂ (colVec M i) (colVec N j) = (M.conjTranspose * N) i j := by
  simp [colVec, PiLp.inner_apply, Matrix.mul_apply, Matrix.conjTranspose_apply, mul_comm]

theorem colVec_mat (b : Fin 6 → OAI.MUB6.Space) (j : Fin 6) : colVec (mat b) j = b j := by
  ext k
  simp [colVec, mat]

theorem inner_eq_mat (b b' : Fin 6 → OAI.MUB6.Space) (i j : Fin 6) :
    inner ℂ (b i) (b' j) = ((mat b).conjTranspose * mat b') i j := by
  rw [← inner_colVec, colVec_mat, colVec_mat]

/-- A unitary matrix gives an orthonormal basis (its columns). -/
noncomputable def basisOfUnitary (M : Cand) (h : M.conjTranspose * M = 1) : OAI.MUB6.Basis :=
  have hon : Orthonormal ℂ (colVec M) := by
    rw [orthonormal_iff_ite]
    intro i j
    rw [inner_colVec, h]
    simp [Matrix.one_apply]
  (basisOfOrthonormalOfCardEqFinrank hon (by simp)).toOrthonormalBasis (by simpa using hon)

theorem basisOfUnitary_apply (M : Cand) (h : M.conjTranspose * M = 1) (j : Fin 6) :
    basisOfUnitary M h j = colVec M j := by
  simp [basisOfUnitary]

/-- The matrix of an orthonormal basis is unitary. -/
theorem mat_unitary (b : OAI.MUB6.Basis) :
    (mat (fun j => b j)).conjTranspose * mat (fun j => b j) = 1 := by
  ext i j
  rw [← inner_eq_mat, b.inner_eq_ite]
  simp [Matrix.one_apply]

/-- **Model equivalence.** OpenAI's `Attainable n` is exactly the existence of an `n`-member pairwise MU
family of unitary `6 × 6` matrices. -/
theorem attainable_iff (n : ℕ) :
    OAI.MUB6.Attainable n ↔ ∃ B : Fin n → Cand, MatrixMUBFamily B := by
  constructor
  · rintro ⟨B, hB⟩
    refine ⟨fun a => mat (fun j => B a j), fun a => mat_unitary (B a), ?_⟩
    intro a b hab i j
    rw [← inner_eq_mat]
    exact hB a b hab i j
  · rintro ⟨B, hU, hMU⟩
    refine ⟨fun a => basisOfUnitary (B a) (hU a), ?_⟩
    intro a b hab i j
    rw [basisOfUnitary_apply, basisOfUnitary_apply, inner_colVec]
    exact hMU a b hab i j

/-! ## Raw (Hadamard, unnormalised) form -/

/-- Normalisation `H ↦ H / √6`. -/
noncomputable def scale (H : Cand) : Cand := (((Real.sqrt 6 : ℝ) : ℂ)⁻¹) • H

private theorem sqrt6_sq : (((Real.sqrt 6 : ℝ) : ℂ)) ^ 2 = 6 := by
  have h : Real.sqrt 6 ^ 2 = 6 := Real.sq_sqrt (by norm_num)
  exact_mod_cast h

private theorem star_inv_mul_inv :
    star (((Real.sqrt 6 : ℝ) : ℂ)⁻¹) * (((Real.sqrt 6 : ℝ) : ℂ)⁻¹) = 1 / 6 := by
  have hne : (((Real.sqrt 6 : ℝ) : ℂ)) ≠ 0 := by
    have : (0 : ℝ) < Real.sqrt 6 := Real.sqrt_pos.mpr (by norm_num)
    exact_mod_cast this.ne'
  rw [star_inv₀, Complex.star_def, Complex.conj_ofReal, ← mul_inv, ← sq, sqrt6_sq]
  simp

theorem scale_gram (H K : Cand) :
    (scale H).conjTranspose * scale K = (1 / 6 : ℂ) • (H.conjTranspose * K) := by
  ext i j
  simp only [scale, Matrix.mul_apply, Matrix.conjTranspose_apply, Matrix.smul_apply, smul_eq_mul,
    Matrix.smul_apply]
  calc
    ∑ k, star (((Real.sqrt 6 : ℝ) : ℂ)⁻¹ * H k i) * (((Real.sqrt 6 : ℝ) : ℂ)⁻¹ * K k j)
        = ∑ k, (star (((Real.sqrt 6 : ℝ) : ℂ)⁻¹) * (((Real.sqrt 6 : ℝ) : ℂ)⁻¹)) *
            (star (H k i) * K k j) := by
          refine Finset.sum_congr rfl fun k _ => ?_
          rw [star_mul']; ring
    _ = (1 / 6 : ℂ) * ∑ k, star (H k i) * K k j := by
          rw [star_inv_mul_inv, Finset.mul_sum]
    _ = _ := rfl

/-- `RawMU` (squared overlap `6` on unnormalised matrices) is the normalised `1/6` overlap condition. -/
theorem rawMU_iff_pairMU (H U : Cand) :
    MonomialTransport.RawMU H U ↔
      ∀ i j, Complex.normSq (((scale H).conjTranspose * scale U) i j) = 1 / 6 := by
  have hc : Fintype.card (Fin 6) = 6 := by simp
  constructor
  · intro h i j
    rw [scale_gram, Matrix.smul_apply, smul_eq_mul, map_mul]
    have := h i j
    simp only [hc] at this
    rw [this]
    have : Complex.normSq (1 / 6 : ℂ) = 1 / 36 := by
      rw [show (1 / 6 : ℂ) = ((1 / 6 : ℝ) : ℂ) by push_cast; ring, Complex.normSq_ofReal]; norm_num
    rw [this]; norm_num
  · intro h i j
    have h' := h i j
    rw [scale_gram, Matrix.smul_apply, smul_eq_mul, map_mul] at h'
    have : Complex.normSq (1 / 6 : ℂ) = 1 / 36 := by
      rw [show (1 / 6 : ℂ) = ((1 / 6 : ℝ) : ℂ) by push_cast; ring, Complex.normSq_ofReal]; norm_num
    rw [this] at h'
    simp only [hc]
    push_cast
    linarith

theorem scale_unitary {H : Cand} (hH : MonomialTransport.RawHadamard H) :
    (scale H).conjTranspose * scale H = 1 := by
  have hc : (Fintype.card (Fin 6) : ℂ) = 6 := by simp
  rw [scale_gram, hH.2, hc]
  ext i j
  simp [Matrix.one_apply]

theorem scale_one_overlap {H : Cand} (hH : MonomialTransport.RawHadamard H) (i j : Fin 6) :
    Complex.normSq (((1 : Cand).conjTranspose * scale H) i j) = 1 / 6 := by
  have h1 := hH.1 i j
  simp only [Matrix.conjTranspose_one, Matrix.one_mul, scale, Matrix.smul_apply, smul_eq_mul,
    map_mul]
  have hs : Complex.normSq (((Real.sqrt 6 : ℝ) : ℂ)⁻¹) = 1 / 6 := by
    rw [map_inv₀, Complex.normSq_ofReal, Real.mul_self_sqrt (by norm_num)]
    norm_num
  rw [hs, h1]; norm_num

/-! ## The imported bound -/

/-- The exact statement of the upstream theorem `OAI.MUB6.family_size_le_five`
(`lean/OAI/Analysis/MutuallyUnbiased/Results/Bounds.lean`, commit
`1581d4cbdd69a0faf34b2089614fe2a814316a6a`): every family of pairwise mutually unbiased orthonormal bases of
`ℂ⁶` has at most five members. It is an external, imported theorem here, not a hypothesis proved in this
repository. -/
def OpenAIFamilyBound : Prop := ∀ n : ℕ, OAI.MUB6.Attainable n → n ≤ 5

/-- `N(6) ≤ 5` for the repository's matrix types, given the imported bound. -/
theorem mub6_family_le_five (h : OpenAIFamilyBound) {n : ℕ} (B : Fin n → Cand)
    (hB : MatrixMUBFamily B) : n ≤ 5 :=
  h n ((attainable_iff n).2 ⟨B, hB⟩)

/-- The same bound for finite sets of unitary matrices that are pairwise MU. -/
theorem mub6_card_le_five (h : OpenAIFamilyBound) (S : Finset Cand)
    (hU : ∀ M ∈ S, M.conjTranspose * M = 1)
    (hMU : ∀ M ∈ S, ∀ N ∈ S, M ≠ N →
      ∀ i j, Complex.normSq ((M.conjTranspose * N) i j) = 1 / 6) :
    S.card ≤ 5 := by
  refine mub6_family_le_five h (n := S.card) (fun a => ((S.equivFin.symm a : S) : Cand)) ⟨?_, ?_⟩
  · intro a
    exact hU _ (S.equivFin.symm a).2
  · intro a b hab i j
    exact hMU _ (S.equivFin.symm a).2 _ (S.equivFin.symm b).2
      (fun h' => hab (S.equivFin.symm.injective (Subtype.ext h'))) i j

/-! ## The Tao phase table -/

/-- The index involution `(3 5)` relating the repository's phase table to OpenAI's `taoExponent`. -/
def taoPerm : Fin 6 → Fin 6 := ![0, 1, 2, 5, 4, 3]

/-- The repository's recorded Tao phase table (`Conjecture2GeneralMechanization.phaseTable`) is OpenAI's
`taoExponent` after reindexing rows and columns by `taoPerm`. -/
theorem tao_phase_bridge (i j : Fin 6) :
    Conjecture2GeneralMechanization.phaseTable (taoPerm i).val (taoPerm j).val =
      (OAI.MUB6.taoExponent i j : ℤ) := by
  fin_cases i <;> fin_cases j <;>
    first
    | rfl
    | simp [taoPerm, OAI.MUB6.taoExponent, Conjecture2GeneralMechanization.phaseTable]

end MUB.OpenAIBridge
