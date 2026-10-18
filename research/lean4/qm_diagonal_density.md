import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Tactic

/-!
# DiagonalDensity — rung 2 (QM_038) mechanization (PL-QM038-1)

Mechanizes the load-bearing facts of QM_038 / ENC-1126: a finite residual-weight
distribution placed on the diagonal is a valid density operator, and its purity is
`∑ pᵢ²`, which lies in `(0,1]`, equal to `1` exactly on a single sector (pure).

Modeled over `ℚ` with `p : Fin n → ℚ`, `0 ≤ pᵢ`, `∑ pᵢ = 1`. "PSD" is the genuine
quadratic-form criterion for the diagonal operator: `⟨x, diag(p) x⟩ = ∑ pᵢ xᵢ² ≥ 0`.
Mathlib-light (ordered `Finset.sum`); no Born rule, Hilbert space, or authority.
-/

namespace QM
namespace DiagonalDensity

open Finset

variable {n : ℕ} (p : Fin n → ℚ)

/-- The trace of the diagonal density `diag(p)` is `∑ pᵢ`. -/
def trace : ℚ := ∑ i, p i

/-- The purity `tr(ρ²) = ∑ pᵢ²`. -/
def purity : ℚ := ∑ i, (p i) ^ 2

/-- **Trace one.** `tr(diag p) = 1` for a normalized distribution. -/
theorem diag_density_trace_one (hsum : ∑ i, p i = 1) : trace p = 1 := hsum

/-- **PSD (quadratic-form criterion).** The diagonal density with nonnegative entries
is positive semidefinite: its quadratic form `⟨x, diag(p) x⟩ = ∑ pᵢ xᵢ²` is `≥ 0` for
every `x`. -/
theorem diag_density_psd (hnn : ∀ i, 0 ≤ p i) (x : Fin n → ℚ) :
    0 ≤ ∑ i, p i * (x i) ^ 2 :=
  Finset.sum_nonneg fun i _ => mul_nonneg (hnn i) (sq_nonneg _)

/-- Each weight is at most one. -/
theorem le_one (hnn : ∀ i, 0 ≤ p i) (hsum : ∑ i, p i = 1) (i : Fin n) : p i ≤ 1 := by
  calc p i ≤ ∑ j, p j := Finset.single_le_sum (fun j _ => hnn j) (Finset.mem_univ i)
    _ = 1 := hsum

/-- **Purity ≤ 1.** Since `0 ≤ pᵢ ≤ 1`, `∑ pᵢ² ≤ ∑ pᵢ = 1`. -/
theorem purity_le_one (hnn : ∀ i, 0 ≤ p i) (hsum : ∑ i, p i = 1) :
    purity p ≤ 1 := by
  have hstep : ∀ i ∈ (Finset.univ : Finset (Fin n)), (p i) ^ 2 ≤ p i := by
    intro i _
    rw [sq]
    exact mul_le_of_le_one_right (hnn i) (le_one p hnn hsum i)
  calc purity p = ∑ i, (p i) ^ 2 := rfl
    _ ≤ ∑ i, p i := Finset.sum_le_sum hstep
    _ = 1 := hsum

/-- A weight is nonnegative and ≤ 1, so `pᵢ(1 − pᵢ) ≥ 0`. -/
theorem mul_one_sub_nonneg (hnn : ∀ i, 0 ≤ p i) (hsum : ∑ i, p i = 1) (i : Fin n) :
    0 ≤ p i * (1 - p i) :=
  mul_nonneg (hnn i) (by linarith [le_one p hnn hsum i])

/-- **Pure ⇒ purity one.** If some sector carries all the weight (`p j = 1`), the
density is pure: `purity = 1`. -/
theorem purity_one_of_pure (hnn : ∀ i, 0 ≤ p i) (hsum : ∑ i, p i = 1)
    (j : Fin n) (hj : p j = 1) : purity p = 1 := by
  -- every other sector is zero
  have hzero : ∀ i, i ≠ j → p i = 0 := by
    intro i hij
    by_contra hne
    have hpos : 0 < p i := lt_of_le_of_ne (hnn i) (Ne.symm hne)
    have : p j + p i ≤ ∑ k, p k := by
      have := Finset.add_le_sum (s := (Finset.univ : Finset (Fin n)))
        (f := p) (fun k _ => hnn k) (Finset.mem_univ j) (Finset.mem_univ i) (Ne.symm hij)
      simpa using this
    rw [hsum, hj] at this
    linarith
  have : purity p = (p j) ^ 2 := by
    unfold purity
    rw [Finset.sum_eq_single j]
    · intro i _ hij; rw [hzero i hij]; ring
    · intro h; exact absurd (Finset.mem_univ j) h
  rw [this, hj]; ring

/-- **Purity one ⇒ pure.** If `purity = 1`, the weight is concentrated on one sector. -/
theorem pure_of_purity_one (hnn : ∀ i, 0 ≤ p i) (hsum : ∑ i, p i = 1)
    (h : purity p = 1) : ∃ j, p j = 1 := by
  -- ∑ pᵢ(1−pᵢ) = ∑ pᵢ − ∑ pᵢ² = 0, each term ≥ 0 ⇒ each = 0 ⇒ pᵢ ∈ {0,1}
  have hsumzero : ∑ i, p i * (1 - p i) = 0 := by
    have : ∑ i, p i * (1 - p i) = (∑ i, p i) - ∑ i, (p i) ^ 2 := by
      rw [← Finset.sum_sub_distrib]; apply Finset.sum_congr rfl; intro i _; ring
    rw [this, hsum]; unfold purity at h; rw [h]; ring
  have heach : ∀ i ∈ (Finset.univ : Finset (Fin n)), p i * (1 - p i) = 0 :=
    (Finset.sum_eq_zero_iff_of_nonneg
      (fun i _ => mul_one_sub_nonneg p hnn hsum i)).mp hsumzero
  have hdich : ∀ i, p i = 0 ∨ p i = 1 := by
    intro i
    rcases mul_eq_zero.mp (heach i (Finset.mem_univ i)) with h0 | h1
    · exact Or.inl h0
    · exact Or.inr (by linarith)
  -- not all zero (else ∑ = 0 ≠ 1), so some pⱼ = 1
  by_contra hcon
  simp only [not_exists] at hcon
  have hallzero : ∀ i, p i = 0 := by
    intro i; rcases hdich i with h0 | h1
    · exact h0
    · exact absurd h1 (hcon i)
  have : (∑ i, p i) = 0 := Finset.sum_eq_zero fun i _ => hallzero i
  rw [hsum] at this; exact one_ne_zero this

/-- **Purity = 1 iff pure.** The diagonal density is pure exactly when its weight sits
on a single sector. -/
theorem purity_one_iff_pure (hnn : ∀ i, 0 ≤ p i) (hsum : ∑ i, p i = 1) :
    purity p = 1 ↔ ∃ j, p j = 1 := by
  constructor
  · exact pure_of_purity_one p hnn hsum
  · rintro ⟨j, hj⟩; exact purity_one_of_pure p hnn hsum j hj

/-! ## Firewall — derived ⇏ authority -/

def IsAuth (_carrier : Type) : Prop := False

theorem structure_not_auth (C : Type) : ¬ IsAuth C := fun h => h

end DiagonalDensity
end QM

#print axioms QM.DiagonalDensity.diag_density_trace_one
#print axioms QM.DiagonalDensity.diag_density_psd
#print axioms QM.DiagonalDensity.purity_le_one
#print axioms QM.DiagonalDensity.purity_one_iff_pure
