import Mathlib.Tactic

/-!
# Entanglement as a Separability Obstruction (QM Pilot-B)

Finite, rational. Relative to a DECLARED finite family of product states `P`, a
joint state `w` is "separable" iff it is a convex combination of them.
Entanglement is the NON-existence of such a decomposition, certified by a
separating linear functional (an entanglement witness): if `φ ≥ t` on every
declared product state but `φ(w) < t`, then `w` is not P-separable. This is the
finite obstruction-calculus form of the entanglement-witness theorem. It does
NOT solve the general (continuous) separability problem; it classifies relative
to the declared family.
-/

namespace QM.SeparabilityObstruction

open scoped BigOperators

variable {ι : Type*} [Fintype ι]   -- carrier coordinates (e.g. real params of a density matrix)
variable {κ : Type*} [Fintype κ]   -- declared product-state family index

/-- A finite rational state vector over the carrier coordinates. -/
abbrev State (ι : Type*) := ι → ℚ

/-- Linear functional given by a coefficient vector (an entanglement-witness operator). -/
def applyφ (φ : ι → ℚ) (w : State ι) : ℚ := ∑ i, φ i * w i

/-- `w` is P-separable: a convex combination of the declared product states `P`. -/
def Separable (P : κ → State ι) (w : State ι) : Prop :=
  ∃ lam : κ → ℚ, (∀ k, 0 ≤ lam k) ∧ (∑ k, lam k) = 1 ∧ (∀ i, w i = ∑ k, lam k * P k i)

/-- A witness functional is additive over a convex combination of states. -/
theorem applyφ_convex (φ : ι → ℚ) (P : κ → State ι) (lam : κ → ℚ) (w : State ι)
    (hdec : ∀ i, w i = ∑ k, lam k * P k i) :
    applyφ φ w = ∑ k, lam k * applyφ φ (P k) := by
  unfold applyφ
  simp_rw [hdec, Finset.mul_sum]
  rw [Finset.sum_comm]
  refine Finset.sum_congr rfl ?_
  intro k _
  refine Finset.sum_congr rfl ?_
  intro i _
  ring

/-- **Headline — entanglement-witness soundness.** A separating functional
    certifies non-separability: if `t ≤ φ(P k)` for every declared product state
    and `φ(w) < t`, then `w` is not P-separable. -/
theorem witness_certifies_not_separable
    (P : κ → State ι) (w : State ι) (φ : ι → ℚ) (t : ℚ)
    (hP : ∀ k, t ≤ applyφ φ (P k))
    (hw : applyφ φ w < t) :
    ¬ Separable P w := by
  rintro ⟨lam, hnn, hsum, hdec⟩
  have hlin : applyφ φ w = ∑ k, lam k * applyφ φ (P k) := applyφ_convex φ P lam w hdec
  have hge : t ≤ applyφ φ w := by
    rw [hlin]
    calc t = ∑ k, lam k * t := by rw [← Finset.sum_mul, hsum, one_mul]
      _ ≤ ∑ k, lam k * applyφ φ (P k) := by
            refine Finset.sum_le_sum ?_
            intro k _
            exact mul_le_mul_of_nonneg_left (hP k) (hnn k)
  linarith

/-- Declared 2-element product family over `Bool`: the unit states `(1,0)` and `(0,1)`. -/
def Punit : Bool → State Bool := fun k i => if k = i then 1 else 0

/-- A uniform mixture of the two unit states is separable. -/
theorem uniform_separable :
    Separable Punit (fun _ => (1/2 : ℚ)) := by
  refine ⟨fun _ => (1/2 : ℚ), by intro k; norm_num, by simp, ?_⟩
  intro i
  simp [Punit]

/-- The all-zero vector is NOT P-separable: the all-ones functional separates it
    (φ = 1 on each unit state, t = 1, but φ(0) = 0 < 1). A finite entanglement
    witness certifies non-membership in the declared product hull. -/
theorem zero_not_separable :
    ¬ Separable Punit (fun _ => (0 : ℚ)) := by
  refine witness_certifies_not_separable Punit (fun _ => 0) (fun _ => 1) 1 ?_ ?_
  · intro k
    simp [applyφ, Punit]
  · simp [applyφ]
