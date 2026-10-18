import Mathlib.Tactic

/-!
# Product Non-Factorization as a Bipartite Obstruction (QM Pilot-A)

Finite, rational, phase-blind. The joint weight table either factors through its
marginals or it does not; `Phi = 0` iff it factors. This detects non-product
*correlation*, NOT entanglement (Bell and the classical mixture share a table).
-/

namespace QM.ProductNonFactorization

open scoped BigOperators

variable {A B : Type*} [Fintype A] [Fintype B]

/-- Total mass of a finite rational joint weight table. -/
def total (w : A → B → ℚ) : ℚ := ∑ a, ∑ b, w a b

/-- A-marginal. -/
def margA (w : A → B → ℚ) (a : A) : ℚ := ∑ b, w a b

/-- B-marginal. -/
def margB (w : A → B → ℚ) (b : B) : ℚ := ∑ a, w a b

/-- The canonical marginal product at `(a,b)`. -/
def prodAB (w : A → B → ℚ) (a : A) (b : B) : ℚ :=
  margA w a * margB w b / total w

/-- Primitive difference: joint minus canonical marginal product. -/
def deltaProd (w : A → B → ℚ) (a : A) (b : B) : ℚ :=
  w a b - prodAB w a b

/-- Obstruction mass: the L1 norm of the product defect. -/
def Phi (w : A → B → ℚ) : ℚ := ∑ a, ∑ b, |deltaProd w a b|

/-- `w` factors through its marginals (the canonical product form). -/
def FactorsThroughMarginals (w : A → B → ℚ) : Prop :=
  ∀ a b, w a b = prodAB w a b

/-- The product defect vanishes everywhere iff the table factors through its marginals. -/
theorem deltaProd_zero_iff_factors (w : A → B → ℚ) :
    (∀ a b, deltaProd w a b = 0) ↔ FactorsThroughMarginals w := by
  constructor
  · intro h a b
    have hab := h a b
    have : w a b - prodAB w a b = 0 := hab
    linarith
  · intro h a b
    have hab := h a b
    simp only [deltaProd, hab, sub_self]

/-- A finite sum of absolute values is zero iff each argument is zero. -/
theorem Phi_zero_iff_deltaProd_zero (w : A → B → ℚ) :
    Phi w = 0 ↔ ∀ a b, deltaProd w a b = 0 := by
  unfold Phi
  rw [Finset.sum_eq_zero_iff_of_nonneg (by intro a _; positivity)]
  constructor
  · intro h a b
    have ha := h a (Finset.mem_univ a)
    rw [Finset.sum_eq_zero_iff_of_nonneg (by intro b _; positivity)] at ha
    exact abs_eq_zero.mp (ha b (Finset.mem_univ b))
  · intro h a _
    rw [Finset.sum_eq_zero_iff_of_nonneg (by intro b _; positivity)]
    intro b _
    rw [abs_eq_zero]; exact h a b

/-- **Headline.** The obstruction mass is zero iff the joint table factors through its marginals. -/
theorem Phi_zero_iff_factors (w : A → B → ℚ) :
    Phi w = 0 ↔ FactorsThroughMarginals w :=
  (Phi_zero_iff_deltaProd_zero w).trans (deltaProd_zero_iff_factors w)

/-- The bipartite carrier `w(a,b) = ½` on the diagonal, `0` off-diagonal, over `Bool × Bool`.
    Both marginals are uniform `(½,½)` (locally green), but the joint is non-product:
    `Phi > 0` (globally red). The Bell state |Φ⁺⟩ and the classical mixture
    ½|00⟩⟨00|+½|11⟩⟨11| descend to THIS SAME table — so this obstruction is productness,
    not entanglement. -/
def diagHalf : Bool → Bool → ℚ := fun a b => if a = b then 1/2 else 0

theorem diagHalf_total : total diagHalf = 1 := by
  simp [total, diagHalf]

theorem diagHalf_not_factors : ¬ FactorsThroughMarginals diagHalf := by
  intro h
  have := h true false
  simp [diagHalf, prodAB, margA, margB, total] at this

theorem diagHalf_Phi_pos : 0 < Phi diagHalf := by
  have h := diagHalf_not_factors
  rw [← Phi_zero_iff_factors] at h
  have hnonneg : 0 ≤ Phi diagHalf := by unfold Phi; positivity
  exact lt_of_le_of_ne hnonneg (Ne.symm h)

/-- A product carrier (uniform `¼`) has zero obstruction. -/
def uniformQuarter : Bool → Bool → ℚ := fun _ _ => 1/4

theorem uniformQuarter_Phi_zero : Phi uniformQuarter = 0 := by
  rw [Phi_zero_iff_factors]
  intro a b
  simp [uniformQuarter, prodAB, margA, margB, total]
  norm_num

end QM.ProductNonFactorization
