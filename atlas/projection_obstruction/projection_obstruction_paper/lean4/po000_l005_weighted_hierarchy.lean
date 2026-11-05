/-
  PO-000 Theorem 4.2 items 2-3: the weighted-hierarchy algebraic cores, and
  the §4.5 counterexample instances.

  * D3 core (Theorem 4.2 item 2): on a singleton, positive homogeneity of the
    diagnostic together with magnitude sufficiency (`J = A ∘ j`) and the full
    nonnegative range of a faithful positively homogeneous local gauge force
    the singleton aggregator to be linear, `A(u) = A(1) · u`, with `A(1) > 0`
    from faithfulness.  Substituted into the RE3 singleton decomposition
    (mechanized in `ReplicaHierarchy.sum_singletons_of_replicaAdditive`), this
    is the weighted `ℓ¹` representation `J_E(x) = ∑_e c_e j_e(x_e)`.
  * D4 core (Theorem 4.2 item 3): a declared gauge-preserving fiber
    identification between two edges under RE4 singleton invariance equalizes
    the two weights.
  * D6 instances (§4.5): the two-edge `ℓ²` combination is singleton-calibrated
    but not disjoint-replica additive (`√2 ≠ 2`), and the doubled sum is
    additive but not singleton-calibrated (`2 ≠ 1`).

  Scope honesty: these are the exact singleton-level algebraic cores the prose
  proof of Theorem 4.2 consumes, over an arbitrary real vector space fiber.
  The full RE1/RE2/RE4 axioms carry more structure (subadditivity, the whole
  labelled-edge-type observer class) than these cores use; nothing here
  upgrades the axioms themselves from declarations to theorems, and nothing
  here mechanizes the quantum results of §5.  AuthorityEffect: None.
-/
import Mathlib

namespace PO000.WeightedHierarchy

variable {Vv : Type*} [AddCommGroup Vv] [Module ℝ Vv]

/-- D3 core, linearity half: if the local gauge `j` is positively homogeneous
with some strictly positive value, the singleton diagnostic `Jd` is positively
homogeneous, and `Jd` factors through `j` via the singleton aggregator `Aagg`
(magnitude sufficiency), then the aggregator is linear on the gauge's range:
`Aagg u = Aagg 1 * u` for every `u ≥ 0`. -/
theorem singleton_aggregator_linear
    (j Jd : Vv → ℝ) (Aagg : ℝ → ℝ)
    (hj_hom : ∀ (c : ℝ), 0 ≤ c → ∀ v, j (c • v) = c * j v)
    (hJ_hom : ∀ (c : ℝ), 0 ≤ c → ∀ v, Jd (c • v) = c * Jd v)
    (hfactor : ∀ v, Jd v = Aagg (j v))
    (v₀ : Vv) (hv₀ : 0 < j v₀) :
    ∀ u : ℝ, 0 ≤ u → Aagg u = Aagg 1 * u := by
  intro u hu
  set w : Vv := (j v₀)⁻¹ • v₀ with hw
  have hjw : j w = 1 := by
    rw [hw, hj_hom _ (by positivity) v₀]
    field_simp
  have h1 : Aagg u = Jd (u • w) := by
    rw [hfactor, hj_hom _ hu w, hjw, mul_one]
  have h2 : Jd (u • w) = u * Jd w := hJ_hom _ hu w
  have h3 : Jd w = Aagg 1 := by rw [hfactor, hjw]
  rw [h1, h2, h3]
  ring

/-- D3 core, positivity half: with faithfulness of the singleton diagnostic
(`Jd v = 0 → v = 0`), nonnegativity, and a gauge-one vector, the weight
`Aagg 1` is strictly positive. -/
theorem singleton_weight_pos
    (j Jd : Vv → ℝ) (Aagg : ℝ → ℝ)
    (hj_hom : ∀ (c : ℝ), 0 ≤ c → ∀ v, j (c • v) = c * j v)
    (hfactor : ∀ v, Jd v = Aagg (j v))
    (hJ_nonneg : ∀ v, 0 ≤ Jd v)
    (hJ_faithful : ∀ v, Jd v = 0 → v = 0)
    (v₀ : Vv) (hv₀ : 0 < j v₀) :
    0 < Aagg 1 := by
  set w : Vv := (j v₀)⁻¹ • v₀ with hw
  have hjw : j w = 1 := by
    rw [hw, hj_hom _ (by positivity) v₀]
    field_simp
  have hne : w ≠ 0 := by
    intro h
    have hj0 : j (0 : Vv) = 0 := by
      have := hj_hom 0 le_rfl (0 : Vv)
      simpa using this
    rw [h, hj0] at hjw
    norm_num at hjw
  have hAw : Jd w = Aagg 1 := by rw [hfactor, hjw]
  rcases lt_or_eq_of_le (hJ_nonneg w) with h | h
  · rw [← hAw]; exact h
  · exact absurd (hJ_faithful w h.symm) hne

/-- D4 core (Theorem 4.2 item 3): a gauge-preserving fiber identification
`τ` between two edges, RE4 singleton invariance, and the two weighted
singleton representations equalize the weights, provided the source gauge
attains the value `1`. -/
theorem orbit_weights_equal
    {Vw : Type*}
    (j₁ : Vv → ℝ) (j₂ : Vw → ℝ) (J₁ : Vv → ℝ) (J₂ : Vw → ℝ)
    (c₁ c₂ : ℝ) (τ : Vv → Vw)
    (hτ : ∀ v, j₂ (τ v) = j₁ v)
    (hJ₁ : ∀ v, J₁ v = c₁ * j₁ v)
    (hJ₂ : ∀ w, J₂ w = c₂ * j₂ w)
    (hRE4 : ∀ v, J₂ (τ v) = J₁ v)
    (v₁ : Vv) (hv₁ : j₁ v₁ = 1) :
    c₁ = c₂ := by
  have h := hRE4 v₁
  rw [hJ₂, hτ, hv₁, mul_one, hJ₁, hv₁, mul_one] at h
  linarith

/-- D6, RE3-drop instance (§4.5): the two-edge `ℓ²` combination has the
calibrated singleton values but is not additive on disjoint nonzero
replicas: at unit magnitudes it returns `√2`, not `1 + 1`. -/
theorem l2_combination_not_additive :
    Real.sqrt ((1 : ℝ) ^ 2 + (1 : ℝ) ^ 2) ≠ 1 + 1 := by
  intro h
  have h2 : Real.sqrt 2 = 2 := by
    have : ((1 : ℝ) ^ 2 + (1 : ℝ) ^ 2) = 2 := by norm_num
    rw [this] at h
    linarith
  have := Real.sq_sqrt (by norm_num : (2 : ℝ) ≥ 0)
  rw [h2] at this
  norm_num at this

/-- D6, RE3-drop instance, singleton calibration half: on a singleton the
`ℓ²` combination degenerates to the declared local gauge. -/
theorem l2_combination_calibrated (u : ℝ) (hu : 0 ≤ u) :
    Real.sqrt (u ^ 2) = u := by
  rw [Real.sqrt_sq hu]

/-- D6, RE5-drop instance (§4.5): the doubled sum is additive... -/
theorem doubled_sum_additive (x y : ℝ) :
    (2 : ℝ) * (x + y) = 2 * x + 2 * y := by ring

/-- ...but violates singleton calibration: at unit gauge it returns `2`,
not the calibrated `1`. -/
theorem doubled_sum_not_calibrated : (2 : ℝ) * 1 ≠ 1 := by norm_num

end PO000.WeightedHierarchy

#print axioms PO000.WeightedHierarchy.singleton_aggregator_linear
#print axioms PO000.WeightedHierarchy.singleton_weight_pos
#print axioms PO000.WeightedHierarchy.orbit_weights_equal
#print axioms PO000.WeightedHierarchy.l2_combination_not_additive
#print axioms PO000.WeightedHierarchy.l2_combination_calibrated
#print axioms PO000.WeightedHierarchy.doubled_sum_additive
#print axioms PO000.WeightedHierarchy.doubled_sum_not_calibrated
