import BornHermitianCarrier
import Mathlib.Algebra.Order.Field.Rat
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Algebra.Star.Pi
import Mathlib.Data.Matrix.Mul
import Mathlib.LinearAlgebra.Matrix.ConjTranspose
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.LinearCombination
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-
Trace positivity for Gaussian-rational Hermitian positive-semidefinite matrices via a Gram (LDL*)
decomposition over ℚ(i) with real (rational) pivots.  AuthorityEffect: None.  No physical claim.

Scope.  All matrices are `Matrix (Fin n) (Fin n) GaussRat` for an arbitrary `n : ℕ`, where
`GaussRat = ℚ(i)` is the concrete pair type of `BornGaussRat`.  The Hermitian form
`hf A x := (star x ⬝ᵥ (A *ᵥ x)).re` (the real part of `x* A x`, `star` taken componentwise) and
"positive semidefinite" (`PsdH A := ∀ x, 0 ≤ hf A x`) are those of the Hermitian carrier
`BornFable.HermitianCarrier` (imported from `BornHermitianCarrier`), so a single PSD notion is used
across the run: rational-PSD tested on Gaussian-rational vectors only, the exact finite notion.  No
real or complex closure, no eigenvalues, no square roots and no spectral theorem are used anywhere.

Main results (general `n`).
* `gram_of_psd`: every Hermitian (`Eᴴ = E`) `PsdH` matrix `E` is a finite sum
  `E = ∑ k, d k • vecMulVec (w k) (star (w k))` with rational `d k ≥ 0` and Gaussian-rational
  vectors `w k` (a Gram / LDL* decomposition over ℚ(i)).  It is obtained by Schur-complement
  elimination on a `Finset` of "active" indices of the fixed type `Fin n`; every pivot is the
  rational number `(E a a).re`, because the diagonal of a Hermitian matrix is real
  (`diag_real_of_hermitian`), so no reindexing of `Fin` and no complex division are needed.
* `trace_mul_nonneg`: if `ρ` is `PsdH` (no Hermitian hypothesis on `ρ`) and `E` is Hermitian and
  `PsdH`, then `0 ≤ (Matrix.trace (ρ * E)).re`.
* Converse facts: `psd_zero`, `psd_add`, `psd_smul`, `psd_vecMulVec_star`, `psd_of_gram`, and the
  characterisation `psd_iff_hasGram` for Hermitian matrices.

Dependencies.  This module imports `BornHermitianCarrier` (hence, transitively, `BornGaussRat`)
and reuses its `hf`, `PsdH`, `hf_add`, `hf_sub`, `hf_smul`, `hf_zero`, `hf_vecMulVec_star` and
`hf_eq_re_trace`; nothing from the carrier is redefined here.
-/

namespace BornFable.HermitianPsd

open Matrix BornFable BornFable.HermitianCarrier
open BornFable.GaussRat (normSq)

variable {n : ℕ}

/-- `E` is a finite nonnegative rational combination of Gaussian-rational rank-one Hermitian
squares `w w*`. -/
def HasGramH (E : Matrix (Fin n) (Fin n) GaussRat) : Prop :=
  ∃ (m : ℕ) (d : Fin m → ℚ) (w : Fin m → Fin n → GaussRat),
    (∀ k, 0 ≤ d k) ∧ E = ∑ k, d k • vecMulVec (w k) (star (w k))

/-! ### Elementary algebra of the Hermitian form -/

theorem normSq_one : normSq (1 : GaussRat) = 1 := by
  norm_num [GaussRat.normSq]

theorem re_mul_star (z w : GaussRat) : (z * star w).re = (star z * w).re := by
  simp only [GaussRat.re_mul, GaussRat.re_star, GaussRat.im_star]
  ring

theorem mulVec_apply_dot (A : Matrix (Fin n) (Fin n) GaussRat) (x : Fin n → GaussRat)
    (a : Fin n) : (A *ᵥ x) a = A a ⬝ᵥ x := rfl

theorem mulVec_single' (A : Matrix (Fin n) (Fin n) GaussRat) (a : Fin n) (t : GaussRat) :
    A *ᵥ Pi.single a t = t • Aᵀ a := by
  funext i
  rw [mulVec_apply_dot, dotProduct_single, Pi.smul_apply, smul_eq_mul, transpose_apply, mul_comm]

theorem hf_add_vec (A : Matrix (Fin n) (Fin n) GaussRat) (u v : Fin n → GaussRat) :
    hf A (u + v) = hf A u + (star u ⬝ᵥ (A *ᵥ v)).re + (star v ⬝ᵥ (A *ᵥ u)).re + hf A v := by
  simp only [hf, star_add, mulVec_add, dotProduct_add, add_dotProduct, GaussRat.re_add]
  ring

theorem hf_single (A : Matrix (Fin n) (Fin n) GaussRat) (a : Fin n) (t : GaussRat) :
    hf A (Pi.single a t) = normSq t * (A a a).re := by
  unfold hf
  rw [Pi.star_single, mulVec_single', single_dotProduct, Pi.smul_apply, smul_eq_mul,
    transpose_apply, ← mul_assoc, GaussRat.star_mul_self, GaussRat.re_algebraMap_mul]

theorem hf_add_single (A : Matrix (Fin n) (Fin n) GaussRat) (x : Fin n → GaussRat) (a : Fin n)
    (t : GaussRat) :
    hf A (x + Pi.single a t) = hf A x + (t * (star x ⬝ᵥ Aᵀ a)).re + (star t * (A a ⬝ᵥ x)).re +
      normSq t * (A a a).re := by
  rw [hf_add_vec, hf_single, mulVec_single', dotProduct_smul, smul_eq_mul, Pi.star_single,
    single_dotProduct, mulVec_apply_dot]

theorem hermitian_apply {A : Matrix (Fin n) (Fin n) GaussRat} (hAs : Aᴴ = A) (i j : Fin n) :
    star (A i j) = A j i := by
  rw [← conjTranspose_apply, hAs]

theorem transpose_row_of_hermitian {A : Matrix (Fin n) (Fin n) GaussRat} (hAs : Aᴴ = A)
    (a : Fin n) : Aᵀ a = star (A a) := by
  funext i
  rw [Pi.star_apply, transpose_apply, hermitian_apply hAs]

theorem star_transpose_row_of_hermitian {A : Matrix (Fin n) (Fin n) GaussRat} (hAs : Aᴴ = A)
    (a : Fin n) : star (Aᵀ a) = A a := by
  rw [transpose_row_of_hermitian hAs, star_star]

theorem diag_real_of_hermitian {A : Matrix (Fin n) (Fin n) GaussRat} (hA : Aᴴ = A) (a : Fin n) :
    (A a a).im = 0 := by
  have h := congrArg GaussRat.im (hermitian_apply hA a a)
  rw [GaussRat.im_star] at h
  linarith

/-- The Hermitian form along a coordinate direction: for `Aᴴ = A`,
`(x + t e_a)* A (x + t e_a) = x* A x + 2 Re(conj t · (A x)_a) + |t|² A_aa`. -/
theorem hf_add_single_of_hermitian {A : Matrix (Fin n) (Fin n) GaussRat} (hAs : Aᴴ = A)
    (x : Fin n → GaussRat) (a : Fin n) (t : GaussRat) :
    hf A (x + Pi.single a t) =
      hf A x + 2 * (star t * (A a ⬝ᵥ x)).re + normSq t * (A a a).re := by
  rw [hf_add_single, transpose_row_of_hermitian hAs, star_dotProduct_star, re_mul_star]
  ring

/-! ### Closure properties of `PsdH` (the easy direction) -/

theorem psd_zero : PsdH (0 : Matrix (Fin n) (Fin n) GaussRat) := fun x =>
  le_of_eq (hf_zero x).symm

theorem psd_add {A B : Matrix (Fin n) (Fin n) GaussRat} (hA : PsdH A) (hB : PsdH B) :
    PsdH (A + B) := fun x => by
  rw [hf_add]
  exact add_nonneg (hA x) (hB x)

theorem psd_smul {A : Matrix (Fin n) (Fin n) GaussRat} {c : ℚ} (hc : 0 ≤ c) (hA : PsdH A) :
    PsdH (c • A) := fun x => by
  rw [hf_smul]
  exact mul_nonneg hc (hA x)

theorem psd_vecMulVec_star (w : Fin n → GaussRat) : PsdH (vecMulVec w (star w)) := fun x => by
  rw [hf_vecMulVec_star]
  exact GaussRat.normSq_nonneg _

theorem psd_of_gram {m : ℕ} (d : Fin m → ℚ) (w : Fin m → Fin n → GaussRat)
    (hd : ∀ k, 0 ≤ d k) : PsdH (∑ k, d k • vecMulVec (w k) (star (w k))) :=
  Finset.sum_induction _ PsdH (fun _ _ hA hB => psd_add hA hB) psd_zero
    (fun k _ => psd_smul (hd k) (psd_vecMulVec_star (w k)))

theorem diag_nonneg {A : Matrix (Fin n) (Fin n) GaussRat} (hA : PsdH A) (a : Fin n) :
    0 ≤ (A a a).re := by
  have h := hA (Pi.single a 1)
  rwa [hf_single, normSq_one, one_mul] at h

/-! ### Trace against a Gram sum (via the carrier's `hf_eq_re_trace`) -/

theorem trace_mul_nonneg_of_gram (ρ : Matrix (Fin n) (Fin n) GaussRat) {m : ℕ} (d : Fin m → ℚ)
    (w : Fin m → Fin n → GaussRat) (hd : ∀ k, 0 ≤ d k) (hρ : PsdH ρ) :
    0 ≤ (Matrix.trace (ρ * ∑ k, d k • vecMulVec (w k) (star (w k)))).re := by
  rw [Matrix.mul_sum, trace_sum, GaussRat.re_sum]
  refine Finset.sum_nonneg fun k _ => ?_
  rw [Matrix.mul_smul, trace_smul, GaussRat.re_smul, ← hf_eq_re_trace]
  exact mul_nonneg (hd k) (hρ (w k))

/-! ### Building Gram decompositions -/

theorem hasGram_zero : HasGramH (0 : Matrix (Fin n) (Fin n) GaussRat) :=
  ⟨0, Fin.elim0, Fin.elim0, fun k => k.elim0, by simp⟩

theorem hasGram_add_smul_vecMulVec {E : Matrix (Fin n) (Fin n) GaussRat} (hE : HasGramH E)
    {c : ℚ} (hc : 0 ≤ c) (r : Fin n → GaussRat) : HasGramH (E + c • vecMulVec r (star r)) := by
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

/-- If a diagonal entry of a Hermitian `PsdH` matrix vanishes, so does its whole row.
Witness: with `c := E a j ≠ 0` and `m := (E j j).re ≥ 0`, the (division-free) Gaussian-rational
vector `-(star c) • e_j + (m + 1) • e_a` would have Hermitian form `-(normSq c) * (m + 2) < 0`. -/
theorem row_eq_zero_of_diag_eq_zero {E : Matrix (Fin n) (Fin n) GaussRat} (hEs : Eᴴ = E)
    (hE : PsdH E) {a : Fin n} (ha : (E a a).re = 0) (j : Fin n) : E a j = 0 := by
  by_contra hb
  have hm : 0 ≤ (E j j).re := diag_nonneg hE j
  have hN : 0 < normSq (E a j) :=
    lt_of_le_of_ne (GaussRat.normSq_nonneg _)
      fun h => hb ((GaussRat.normSq_eq_zero_iff _).mp h.symm)
  have hx := hE (Pi.single j (-star (E a j)) + Pi.single a (⟨(E j j).re + 1, 0⟩ : GaussRat))
  rw [hf_add_single_of_hermitian hEs, hf_single, dotProduct_single, ha, mul_zero, add_zero] at hx
  simp only [GaussRat.normSq, GaussRat.re_mul, GaussRat.im_mul, GaussRat.re_neg, GaussRat.im_neg,
    GaussRat.re_star, GaussRat.im_star] at hx hN
  nlinarith [mul_nonneg hN.le hm, hN, hx]

/-- Schur-complement elimination on a `Finset` of active indices: a Hermitian `PsdH` matrix whose
rows outside `S` vanish has a Gram decomposition.  The pivot is the real rational diagonal entry
`(E a a).re`; the rank-one piece split off is `(1 / (E a a).re) • (col a)(col a)*`, where
`col a = Eᵀ a = fun i => E i a` is column `a` and `star (col a) = E a` is row `a`. -/
theorem hasGram_of_support (S : Finset (Fin n)) :
    ∀ E : Matrix (Fin n) (Fin n) GaussRat, Eᴴ = E → PsdH E →
      (∀ i j, i ∉ S → E i j = 0) → HasGramH E := by
  refine Finset.induction_on S ?_ ?_
  · intro E _ _ hsupp
    have hE0 : E = 0 := Matrix.ext fun i j => hsupp i j (Finset.notMem_empty i)
    rw [hE0]
    exact hasGram_zero
  · intro a s _ ih E hEs hE hsupp
    by_cases hα : (E a a).re = 0
    · -- the pivot vanishes: the whole row `a` vanishes and the support shrinks to `s`
      refine ih E hEs hE fun i j hi => ?_
      by_cases hia : i = a
      · rw [hia]
        exact row_eq_zero_of_diag_eq_zero hEs hE hα j
      · exact hsupp i j fun h => (Finset.mem_insert.mp h).elim hia hi
    · -- positive pivot: split off `(1 / (E a a).re) • (col a)(col a)*` and recurse on the
      -- Schur complement
      have hαpos : 0 < (E a a).re := lt_of_le_of_ne (diag_nonneg hE a) (Ne.symm hα)
      have him : (E a a).im = 0 := diag_real_of_hermitian hEs a
      obtain ⟨E', hE'⟩ : ∃ E' : Matrix (Fin n) (Fin n) GaussRat,
          E' = E - (1 / (E a a).re) • vecMulVec (Eᵀ a) (star (Eᵀ a)) := ⟨_, rfl⟩
      have hE's : E'ᴴ = E' := by
        rw [hE', conjTranspose_sub, conjTranspose_rat_smul, conjTranspose_vecMulVec, star_star,
          hEs]
      have hE'psd : PsdH E' := by
        intro x
        obtain ⟨c, hc⟩ : ∃ c : GaussRat, c = E a ⬝ᵥ x := ⟨_, rfl⟩
        obtain ⟨t, ht⟩ : ∃ t : GaussRat, t = (-(1 / (E a a).re)) • c := ⟨_, rfl⟩
        have hx := hE (x + Pi.single a t)
        rw [hf_add_single_of_hermitian hEs, ← hc] at hx
        have h1 : hf E' x = hf E x - 1 / (E a a).re * normSq c := by
          rw [hE', hf_sub, hf_smul, hf_vecMulVec_star, star_transpose_row_of_hermitian hEs, hc]
        have hkey : 2 * (star t * c).re + normSq t * (E a a).re =
            -(1 / (E a a).re * normSq c) := by
          rw [ht]
          simp only [GaussRat.re_star_mul, GaussRat.normSq, GaussRat.re_smul, GaussRat.im_smul]
          linear_combination (1 / (E a a).re * (c.re ^ 2 + c.im ^ 2)) * one_div_mul_cancel hα
        rw [h1]
        linarith
      have hE'supp : ∀ i j, i ∉ s → E' i j = 0 := by
        intro i j hi
        rw [hE', Matrix.sub_apply, Matrix.smul_apply, vecMulVec_apply,
          star_transpose_row_of_hermitian hEs, transpose_apply]
        by_cases hia : i = a
        · rw [hia]
          ext
          · simp only [GaussRat.re_sub, GaussRat.re_smul, GaussRat.re_mul, him, GaussRat.re_zero]
            linear_combination (-(E a j).re) * one_div_mul_cancel hα
          · simp only [GaussRat.im_sub, GaussRat.im_smul, GaussRat.im_mul, him, GaussRat.im_zero]
            linear_combination (-(E a j).im) * one_div_mul_cancel hα
        · have hi' : i ∉ insert a s := fun h => (Finset.mem_insert.mp h).elim hia hi
          rw [hsupp i j hi', hsupp i a hi', zero_mul, smul_zero, sub_zero]
      have hdecomp : E = E' + (1 / (E a a).re) • vecMulVec (Eᵀ a) (star (Eᵀ a)) := by
        rw [hE', sub_add_cancel]
      rw [hdecomp]
      exact hasGram_add_smul_vecMulVec (ih E' hE's hE'psd hE'supp)
        (div_nonneg zero_le_one hαpos.le) (Eᵀ a)

/-- Every Hermitian Gaussian-rational `PsdH` matrix is a nonnegative rational combination of
Gaussian-rational rank-one Hermitian squares (Gram / LDL* decomposition over ℚ(i)). -/
theorem gram_of_psd (E : Matrix (Fin n) (Fin n) GaussRat) (hEs : Eᴴ = E) (hE : PsdH E) :
    HasGramH E :=
  hasGram_of_support Finset.univ E hEs hE fun i _ hi => absurd (Finset.mem_univ i) hi

theorem psd_iff_hasGram {E : Matrix (Fin n) (Fin n) GaussRat} (hEs : Eᴴ = E) :
    PsdH E ↔ HasGramH E := by
  refine ⟨gram_of_psd E hEs, ?_⟩
  rintro ⟨m, d, w, hd, hEeq⟩
  rw [hEeq]
  exact psd_of_gram d w hd

/-! ### Main theorem -/

/-- Trace positivity: `ρ` `PsdH` (no Hermitian hypothesis needed), `E` Hermitian and `PsdH`, both
tested on Gaussian-rational vectors only. -/
theorem trace_mul_nonneg (ρ E : Matrix (Fin n) (Fin n) GaussRat) (hρ : PsdH ρ) (hE : PsdH E)
    (hEs : Eᴴ = E) : 0 ≤ (Matrix.trace (ρ * E)).re := by
  obtain ⟨m, d, w, hd, hEeq⟩ := gram_of_psd E hEs hE
  rw [hEeq]
  exact trace_mul_nonneg_of_gram ρ d w hd hρ

end BornFable.HermitianPsd

#print axioms BornFable.HermitianPsd.HasGramH
#print axioms BornFable.HermitianPsd.normSq_one
#print axioms BornFable.HermitianPsd.re_mul_star
#print axioms BornFable.HermitianPsd.mulVec_apply_dot
#print axioms BornFable.HermitianPsd.mulVec_single'
#print axioms BornFable.HermitianPsd.hf_add_vec
#print axioms BornFable.HermitianPsd.hf_single
#print axioms BornFable.HermitianPsd.hf_add_single
#print axioms BornFable.HermitianPsd.hermitian_apply
#print axioms BornFable.HermitianPsd.transpose_row_of_hermitian
#print axioms BornFable.HermitianPsd.star_transpose_row_of_hermitian
#print axioms BornFable.HermitianPsd.diag_real_of_hermitian
#print axioms BornFable.HermitianPsd.hf_add_single_of_hermitian
#print axioms BornFable.HermitianPsd.psd_zero
#print axioms BornFable.HermitianPsd.psd_add
#print axioms BornFable.HermitianPsd.psd_smul
#print axioms BornFable.HermitianPsd.psd_vecMulVec_star
#print axioms BornFable.HermitianPsd.psd_of_gram
#print axioms BornFable.HermitianPsd.diag_nonneg
#print axioms BornFable.HermitianPsd.trace_mul_nonneg_of_gram
#print axioms BornFable.HermitianPsd.hasGram_zero
#print axioms BornFable.HermitianPsd.hasGram_add_smul_vecMulVec
#print axioms BornFable.HermitianPsd.row_eq_zero_of_diag_eq_zero
#print axioms BornFable.HermitianPsd.hasGram_of_support
#print axioms BornFable.HermitianPsd.gram_of_psd
#print axioms BornFable.HermitianPsd.psd_iff_hasGram
#print axioms BornFable.HermitianPsd.trace_mul_nonneg
