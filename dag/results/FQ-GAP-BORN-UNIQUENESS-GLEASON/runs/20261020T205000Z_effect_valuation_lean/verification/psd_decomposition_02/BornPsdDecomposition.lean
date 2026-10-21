import BornMatrixCarrier
import Mathlib.Algebra.Order.Field.Rat
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Data.Matrix.Mul
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring
import Mathlib.Tactic.LinearCombination

/-
Trace positivity for rational positive-semidefinite matrices via a rational Gram (LDLᵀ)
decomposition.  AuthorityEffect: None.  No physical claim.

Scope.  All matrices are `Matrix (Fin n) (Fin n) ℚ` for an arbitrary `n : ℕ`.  The quadratic
form `qf A x := x ⬝ᵥ (A *ᵥ x)` and "positive semidefinite" (`PsdQ A := ∀ x, 0 ≤ qf A x`) are the
ones of the matrix carrier `BornFable.MatrixCarrier` (imported from `BornMatrixCarrier`), so a
single PSD notion is used across the run: nonnegativity on every *rational* vector `x`, the exact
finite notion, tested on rational vectors only.  No real closure, no eigenvalues, no square roots
and no spectral theorem are used anywhere.

Main results (general `n`).
* `gram_of_psd`: every symmetric `PsdQ` matrix `E` is a finite sum
  `E = ∑ k, d k • vecMulVec (w k) (w k)` with rational `d k ≥ 0` and rational vectors `w k`
  (a Gram / LDLᵀ decomposition over ℚ).  It is obtained by Schur-complement elimination on a
  `Finset` of "active" indices of the fixed type `Fin n`, so no reindexing of `Fin` is needed.
* `trace_mul_nonneg`: if `ρ` is `PsdQ` (no symmetry hypothesis on `ρ`) and `E` is symmetric and
  `PsdQ`, then `0 ≤ Matrix.trace (ρ * E)`.
* Converse facts: `psd_zero`, `psd_add`, `psd_smul`, `psd_vecMulVec`, `psd_of_gram`, and the
  characterisation `psd_iff_hasGram` for symmetric matrices.

Dependencies.  This module imports `BornMatrixCarrier` (hence, transitively,
`BornEffectValuation`) and reuses its `qf`, `PsdQ`, `qf_vecMulVec` and `qf_eq_trace'`; it does not
import the other modules of this run.
-/

namespace BornFable.PsdDecomposition

open Matrix
open BornFable.MatrixCarrier (qf PsdQ)

variable {n : ℕ}

/-- `E` is a finite nonnegative rational combination of rational rank-one squares. -/
def HasGram (E : Matrix (Fin n) (Fin n) ℚ) : Prop :=
  ∃ (m : ℕ) (d : Fin m → ℚ) (w : Fin m → Fin n → ℚ),
    (∀ k, 0 ≤ d k) ∧ E = ∑ k, d k • vecMulVec (w k) (w k)

/-! ### Elementary algebra of the quadratic form -/

theorem qf_add (A : Matrix (Fin n) (Fin n) ℚ) (u v : Fin n → ℚ) :
    qf A (u + v) = qf A u + u ⬝ᵥ (A *ᵥ v) + v ⬝ᵥ (A *ᵥ u) + qf A v := by
  simp only [qf, mulVec_add, dotProduct_add, add_dotProduct]
  ring

theorem mulVec_apply' (A : Matrix (Fin n) (Fin n) ℚ) (x : Fin n → ℚ) (a : Fin n) :
    (A *ᵥ x) a = A a ⬝ᵥ x := rfl

theorem mulVec_single_one' (A : Matrix (Fin n) (Fin n) ℚ) (a : Fin n) :
    A *ᵥ Pi.single a (1 : ℚ) = Aᵀ a :=
  mulVec_single_one A a

theorem dotProduct_mulVec_single (A : Matrix (Fin n) (Fin n) ℚ) (x : Fin n → ℚ) (a : Fin n)
    (t : ℚ) : x ⬝ᵥ (A *ᵥ (t • Pi.single a (1 : ℚ))) = t * (x ⬝ᵥ Aᵀ a) := by
  rw [mulVec_smul, mulVec_single_one', dotProduct_smul, smul_eq_mul]

theorem single_dotProduct_mulVec (A : Matrix (Fin n) (Fin n) ℚ) (x : Fin n → ℚ) (a : Fin n)
    (t : ℚ) : (t • Pi.single a (1 : ℚ)) ⬝ᵥ (A *ᵥ x) = t * (A a ⬝ᵥ x) := by
  rw [smul_dotProduct, single_dotProduct, one_mul, smul_eq_mul, mulVec_apply']

theorem qf_single (A : Matrix (Fin n) (Fin n) ℚ) (a : Fin n) (t : ℚ) :
    qf A (t • Pi.single a (1 : ℚ)) = t * t * A a a := by
  rw [qf, dotProduct_mulVec_single, smul_dotProduct, single_dotProduct, transpose_apply,
    smul_eq_mul, one_mul]
  ring

theorem qf_add_single (A : Matrix (Fin n) (Fin n) ℚ) (x : Fin n → ℚ) (a : Fin n) (t : ℚ) :
    qf A (x + t • Pi.single a (1 : ℚ)) =
      qf A x + t * (x ⬝ᵥ Aᵀ a) + t * (A a ⬝ᵥ x) + t * t * A a a := by
  rw [qf_add, dotProduct_mulVec_single, single_dotProduct_mulVec, qf_single]

theorem symm_apply {A : Matrix (Fin n) (Fin n) ℚ} (hAs : Aᵀ = A) (i j : Fin n) :
    A i j = A j i := by
  have h := congrFun (congrFun hAs j) i
  rwa [transpose_apply] at h

theorem qf_add_single_of_symm {A : Matrix (Fin n) (Fin n) ℚ} (hAs : Aᵀ = A) (x : Fin n → ℚ)
    (a : Fin n) (t : ℚ) :
    qf A (x + t • Pi.single a (1 : ℚ)) = qf A x + 2 * t * (A a ⬝ᵥ x) + t * t * A a a := by
  rw [qf_add_single, hAs, dotProduct_comm x (A a)]
  ring

/-! ### Closure properties of `PsdQ` (the easy direction) -/

theorem psd_zero : PsdQ (0 : Matrix (Fin n) (Fin n) ℚ) := fun x =>
  le_of_eq (by rw [qf, zero_mulVec, dotProduct_zero])

theorem psd_add {A B : Matrix (Fin n) (Fin n) ℚ} (hA : PsdQ A) (hB : PsdQ B) :
    PsdQ (A + B) := fun x => by
  have h : qf (A + B) x = qf A x + qf B x := by
    simp only [qf, add_mulVec, dotProduct_add]
  rw [h]
  exact add_nonneg (hA x) (hB x)

theorem psd_smul {A : Matrix (Fin n) (Fin n) ℚ} {c : ℚ} (hc : 0 ≤ c) (hA : PsdQ A) :
    PsdQ (c • A) := fun x => by
  have h : qf (c • A) x = c * qf A x := by
    simp only [qf, smul_mulVec, dotProduct_smul, smul_eq_mul]
  rw [h]
  exact mul_nonneg hc (hA x)

theorem psd_vecMulVec (w : Fin n → ℚ) : PsdQ (vecMulVec w w) := fun x => by
  rw [MatrixCarrier.qf_vecMulVec]
  exact sq_nonneg _

theorem psd_of_gram {m : ℕ} (d : Fin m → ℚ) (w : Fin m → Fin n → ℚ) (hd : ∀ k, 0 ≤ d k) :
    PsdQ (∑ k, d k • vecMulVec (w k) (w k)) :=
  Finset.sum_induction _ PsdQ (fun _ _ hA hB => psd_add hA hB) psd_zero
    (fun k _ => psd_smul (hd k) (psd_vecMulVec (w k)))

theorem diag_nonneg {A : Matrix (Fin n) (Fin n) ℚ} (hA : PsdQ A) (a : Fin n) : 0 ≤ A a a := by
  have h := hA ((1 : ℚ) • Pi.single a (1 : ℚ))
  rwa [qf_single, one_mul, one_mul] at h

/-! ### Trace against a Gram sum (via the carrier's `qf_eq_trace'`) -/

theorem trace_mul_nonneg_of_gram (ρ : Matrix (Fin n) (Fin n) ℚ) {m : ℕ} (d : Fin m → ℚ)
    (w : Fin m → Fin n → ℚ) (hd : ∀ k, 0 ≤ d k) (hρ : PsdQ ρ) :
    0 ≤ Matrix.trace (ρ * ∑ k, d k • vecMulVec (w k) (w k)) := by
  rw [Matrix.mul_sum, trace_sum]
  refine Finset.sum_nonneg fun k _ => ?_
  rw [Matrix.mul_smul, trace_smul, ← MatrixCarrier.qf_eq_trace', smul_eq_mul]
  exact mul_nonneg (hd k) (hρ (w k))

/-! ### Building Gram decompositions -/

theorem hasGram_zero : HasGram (0 : Matrix (Fin n) (Fin n) ℚ) :=
  ⟨0, Fin.elim0, Fin.elim0, fun k => k.elim0, by simp⟩

theorem hasGram_add_smul_vecMulVec {E : Matrix (Fin n) (Fin n) ℚ} (hE : HasGram E) {c : ℚ}
    (hc : 0 ≤ c) (r : Fin n → ℚ) : HasGram (E + c • vecMulVec r r) := by
  obtain ⟨m, d, w, hd, rfl⟩ := hE
  refine ⟨m + 1, Fin.cons c d, Fin.cons r w, ?_, ?_⟩
  · intro k
    refine Fin.cases ?_ (fun i => ?_) k
    · rw [Fin.cons_zero]
      exact hc
    · rw [Fin.cons_succ]
      exact hd i
  · rw [Fin.sum_univ_succ]
    simp only [Fin.cons_zero, Fin.cons_succ]
    exact add_comm _ _

/-- If a diagonal entry of a symmetric `PsdQ` matrix vanishes, so does its whole row.
Witness: the rational vector `(E j j + 1) • e_a - (E a j) • e_j` would otherwise have negative
quadratic form `-(E a j)^2 * (E j j + 2)`. -/
theorem row_eq_zero_of_diag_eq_zero {E : Matrix (Fin n) (Fin n) ℚ} (hEs : Eᵀ = E) (hE : PsdQ E)
    {a : Fin n} (ha : E a a = 0) (j : Fin n) : E a j = 0 := by
  by_contra hb
  have hc : 0 ≤ E j j := diag_nonneg hE j
  have hx := hE ((E j j + 1) • Pi.single a (1 : ℚ) + (-E a j) • Pi.single j (1 : ℚ))
  rw [qf_add_single_of_symm hEs, qf_single, ha, mul_zero, dotProduct_smul, dotProduct_single,
    mul_one, symm_apply hEs j a, smul_eq_mul] at hx
  have hb2 : 0 < E a j * E a j := mul_self_pos.mpr hb
  nlinarith [mul_nonneg hb2.le hc, hb2, hx]

/-- Schur-complement elimination on a `Finset` of active indices: a symmetric `PsdQ` matrix
whose rows outside `S` vanish has a Gram decomposition. -/
theorem hasGram_of_support (S : Finset (Fin n)) :
    ∀ E : Matrix (Fin n) (Fin n) ℚ, Eᵀ = E → PsdQ E →
      (∀ i j, i ∉ S → E i j = 0) → HasGram E := by
  refine Finset.induction_on S ?_ ?_
  · intro E _ _ hsupp
    have hE0 : E = 0 := Matrix.ext fun i j => hsupp i j (Finset.notMem_empty i)
    rw [hE0]
    exact hasGram_zero
  · intro a s _ ih E hEs hE hsupp
    by_cases hα : E a a = 0
    · -- the pivot vanishes: the whole row `a` vanishes and the support shrinks to `s`
      refine ih E hEs hE fun i j hi => ?_
      by_cases hia : i = a
      · rw [hia]
        exact row_eq_zero_of_diag_eq_zero hEs hE hα j
      · exact hsupp i j fun h => (Finset.mem_insert.mp h).elim hia hi
    · -- positive pivot: split off `(1 / E a a) • (row a)(row a)ᵀ` and recurse on the Schur complement
      have hα' : E a a ≠ 0 := hα
      have hαpos : 0 < E a a := lt_of_le_of_ne (diag_nonneg hE a) (Ne.symm hα)
      obtain ⟨E', hE'⟩ : ∃ E' : Matrix (Fin n) (Fin n) ℚ,
          E' = E - (1 / E a a) • vecMulVec (E a) (E a) := ⟨_, rfl⟩
      have hE's : E'ᵀ = E' := by
        rw [hE', transpose_sub, transpose_smul, transpose_vecMulVec, hEs]
      have hE'psd : PsdQ E' := by
        intro x
        obtain ⟨t, ht⟩ : ∃ t : ℚ, t = -(E a ⬝ᵥ x) / E a a := ⟨_, rfl⟩
        have hx := hE (x + t • Pi.single a (1 : ℚ))
        rw [qf_add_single_of_symm hEs] at hx
        have h1 : qf E' x = qf E x - 1 / E a a * qf (vecMulVec (E a) (E a)) x := by
          simp only [hE', qf, sub_mulVec, smul_mulVec, dotProduct_sub, dotProduct_smul,
            smul_eq_mul]
        have hkey : 2 * t * (E a ⬝ᵥ x) + t * t * E a a =
            -(1 / E a a * (E a ⬝ᵥ x) ^ 2) := by
          rw [ht]
          linear_combination ((E a ⬝ᵥ x) ^ 2 * (E a a)⁻¹) * mul_inv_cancel₀ hα'
        rw [h1, MatrixCarrier.qf_vecMulVec]
        linarith
      have hE'supp : ∀ i j, i ∉ s → E' i j = 0 := by
        intro i j hi
        rw [hE', Matrix.sub_apply, Matrix.smul_apply, vecMulVec_apply, smul_eq_mul]
        by_cases hia : i = a
        · rw [hia, ← mul_assoc, one_div_mul_cancel hα', one_mul, sub_self]
        · have hi' : i ∉ insert a s := fun h => (Finset.mem_insert.mp h).elim hia hi
          rw [hsupp i j hi', symm_apply hEs a i, hsupp i a hi', zero_mul, mul_zero, sub_zero]
      have hdecomp : E = E' + (1 / E a a) • vecMulVec (E a) (E a) := by
        rw [hE', sub_add_cancel]
      rw [hdecomp]
      exact hasGram_add_smul_vecMulVec (ih E' hE's hE'psd hE'supp)
        (div_nonneg zero_le_one hαpos.le) (E a)

/-- Every symmetric rational `PsdQ` matrix is a nonnegative rational combination of rational
rank-one squares (Gram / LDLᵀ decomposition over ℚ). -/
theorem gram_of_psd (E : Matrix (Fin n) (Fin n) ℚ) (hEs : Eᵀ = E) (hE : PsdQ E) :
    HasGram E :=
  hasGram_of_support Finset.univ E hEs hE fun i _ hi => absurd (Finset.mem_univ i) hi

theorem psd_iff_hasGram {E : Matrix (Fin n) (Fin n) ℚ} (hEs : Eᵀ = E) :
    PsdQ E ↔ HasGram E := by
  refine ⟨gram_of_psd E hEs, ?_⟩
  rintro ⟨m, d, w, hd, hEeq⟩
  rw [hEeq]
  exact psd_of_gram d w hd

/-! ### Main theorem -/

/-- Trace positivity: `ρ` `PsdQ` (no symmetry needed), `E` symmetric and `PsdQ`, both tested on
rational vectors only. -/
theorem trace_mul_nonneg (ρ E : Matrix (Fin n) (Fin n) ℚ) (hρ : PsdQ ρ) (hE : PsdQ E)
    (hEs : Eᵀ = E) : 0 ≤ Matrix.trace (ρ * E) := by
  obtain ⟨m, d, w, hd, hEeq⟩ := gram_of_psd E hEs hE
  rw [hEeq]
  exact trace_mul_nonneg_of_gram ρ d w hd hρ

end BornFable.PsdDecomposition

#print axioms BornFable.PsdDecomposition.qf_add
#print axioms BornFable.PsdDecomposition.mulVec_apply'
#print axioms BornFable.PsdDecomposition.mulVec_single_one'
#print axioms BornFable.PsdDecomposition.dotProduct_mulVec_single
#print axioms BornFable.PsdDecomposition.single_dotProduct_mulVec
#print axioms BornFable.PsdDecomposition.symm_apply
#print axioms BornFable.PsdDecomposition.qf_single
#print axioms BornFable.PsdDecomposition.qf_add_single
#print axioms BornFable.PsdDecomposition.qf_add_single_of_symm
#print axioms BornFable.PsdDecomposition.psd_zero
#print axioms BornFable.PsdDecomposition.psd_add
#print axioms BornFable.PsdDecomposition.psd_smul
#print axioms BornFable.PsdDecomposition.psd_vecMulVec
#print axioms BornFable.PsdDecomposition.psd_of_gram
#print axioms BornFable.PsdDecomposition.diag_nonneg
#print axioms BornFable.PsdDecomposition.trace_mul_nonneg_of_gram
#print axioms BornFable.PsdDecomposition.hasGram_zero
#print axioms BornFable.PsdDecomposition.hasGram_add_smul_vecMulVec
#print axioms BornFable.PsdDecomposition.row_eq_zero_of_diag_eq_zero
#print axioms BornFable.PsdDecomposition.hasGram_of_support
#print axioms BornFable.PsdDecomposition.gram_of_psd
#print axioms BornFable.PsdDecomposition.psd_iff_hasGram
#print axioms BornFable.PsdDecomposition.trace_mul_nonneg
