import WitnessedDifference.Obstruction

/-!
# Growth of the repair cost under restriction and subdivision

This module reuses the weighted ℓ¹ residual `Σ_e w e * |δ e - (d0 f) e|` of
`WitnessedDifference.Obstruction` over a finite edge list.

- Restriction: for nonnegative weights on the added edges, the residual of a
  potential over `es` is at most its residual over `es ++ extra`; over an
  order-preserving sublist it is at most the residual over the full list.
  From the lower-bound half of the smaller infimum and the
  greatest-lower-bound half of the larger infimum, the smaller repair cost is
  at most the larger one.
- Subdivision: splitting an edge `u → v` of weight `w ≥ 0` into `u → m → v`
  with the same weight and cochain values `x1, x2` does not change the local
  minimum: every midpoint potential `fm` leaves residual at least
  `w * |x1 + x2 - (fv - fu)|`, and `fm = fu + x1` attains it. With the rest of
  the problem held fixed, the two infima coincide.

Infima are not constructed. Each theorem takes the halves of the infimum
characterization that it uses as named hypotheses. This file declares no
synthetic axioms.
-/

namespace WitnessedDifference.ComplexGrowth

open WitnessedDifference.Obstruction

/-! ## Finite sums and absolute values -/

theorem sumOver_append {E : Type} (es extra : List E) (g : E → ℚ) :
    sumOver (es ++ extra) g = sumOver es g + sumOver extra g := by
  induction es with
  | nil => simp only [List.nil_append, sumOver_nil]; grind
  | cons e es ih =>
    simp only [List.cons_append, sumOver_cons, ih]
    grind

theorem sumOver_nonneg {E : Type} (es : List E) (g : E → ℚ)
    (hnonneg : ∀ e ∈ es, 0 ≤ g e) :
    0 ≤ sumOver es g := by
  induction es with
  | nil => exact Rat.le_refl
  | cons e es ih =>
    simp only [sumOver_cons]
    have hhead := hnonneg e (List.mem_cons_self ..)
    have htail := ih (fun x hx => hnonneg x (List.mem_cons_of_mem _ hx))
    grind

/-- A sum over a sublist is at most the sum over the full list when the
summand is nonnegative on the full list. -/
theorem sumOver_le_of_sublist {E : Type} {es es' : List E}
    (hsub : List.Sublist es es') (g : E → ℚ)
    (hnonneg : ∀ e ∈ es', 0 ≤ g e) :
    sumOver es g ≤ sumOver es' g := by
  induction hsub with
  | slnil => exact Rat.le_refl
  | cons a _ ih =>
    simp only [sumOver_cons]
    have hhead := hnonneg a (List.mem_cons_self ..)
    have htail := ih (fun x hx => hnonneg x (List.mem_cons_of_mem _ hx))
    grind
  | cons_cons a _ ih =>
    simp only [sumOver_cons]
    have htail := ih (fun x hx => hnonneg x (List.mem_cons_of_mem _ hx))
    grind

theorem qabs_nonneg (x : ℚ) : 0 ≤ qabs x := by
  unfold qabs
  split <;> grind

theorem qabs_add_le (x y : ℚ) : qabs (x + y) ≤ qabs x + qabs y := by
  unfold qabs
  split <;> split <;> split <;> grind

theorem weight_mul_qabs_nonneg (w x : ℚ) (hw : 0 ≤ w) : 0 ≤ w * qabs x :=
  Rat.mul_nonneg hw (qabs_nonneg x)

/-! ## Restriction -/

/-- Restriction does not increase residual mass: for every potential `f`,
the weighted residual over `es` is at most the weighted residual over
`es ++ extra`, provided the weights on the added edges are nonnegative. -/
theorem restriction_mass_le {C0 E : Type}
    (es extra : List E) (w δ : E → ℚ) (d0 : C0 → E → ℚ)
    (hw : ∀ e ∈ extra, 0 ≤ w e) (f : C0) :
    sumOver es (fun e => w e * qabs (δ e - d0 f e)) ≤
      sumOver (es ++ extra) (fun e => w e * qabs (δ e - d0 f e)) := by
  rw [sumOver_append]
  have hextra := sumOver_nonneg extra (fun e => w e * qabs (δ e - d0 f e))
    (fun e he => weight_mul_qabs_nonneg (w e) (δ e - d0 f e) (hw e he))
  grind

/-- The sublist form of `restriction_mass_le`: an order-preserving sublist
`es` of `es'` carries no more residual mass than `es'` for every potential,
provided every weight on `es'` is nonnegative. -/
theorem restriction_mass_le_sublist {C0 E : Type} {es es' : List E}
    (hsub : List.Sublist es es') (w δ : E → ℚ) (d0 : C0 → E → ℚ)
    (hw : ∀ e ∈ es', 0 ≤ w e) (f : C0) :
    sumOver es (fun e => w e * qabs (δ e - d0 f e)) ≤
      sumOver es' (fun e => w e * qabs (δ e - d0 f e)) :=
  sumOver_le_of_sublist hsub (fun e => w e * qabs (δ e - d0 f e))
    (fun e he => weight_mul_qabs_nonneg (w e) (δ e - d0 f e) (hw e he))

/-- Repair-cost monotonicity from the infimum characterization, for arbitrary
repair spaces. If `Φs` is a lower bound of the smaller costs `Js`, every larger
repair `β` restricts to a smaller repair `ρ β` of no larger cost, and `Φl` is
the greatest lower bound of the larger costs `Jl`, then `Φs` is a lower bound
of every larger cost and `Φs ≤ Φl`. -/
theorem phi_le_of_restriction {As Al : Type}
    (Js : As → ℚ) (Jl : Al → ℚ) (ρ : Al → As) (Φs Φl : ℚ)
    (lower_small : ∀ α, Φs ≤ Js α)
    (restricts : ∀ β, Js (ρ β) ≤ Jl β)
    (glb_large : ∀ b : ℚ, (∀ β, b ≤ Jl β) → b ≤ Φl) :
    (∀ β, Φs ≤ Jl β) ∧ Φs ≤ Φl := by
  have hlower : ∀ β, Φs ≤ Jl β := fun β =>
    Rat.le_trans (lower_small (ρ β)) (restricts β)
  exact ⟨hlower, glb_large Φs hlower⟩

/-- Restriction monotonicity of the weighted ℓ¹ repair cost. `Φs` is a lower
bound of the residuals over `es`; `Φl` is the greatest lower bound of the
residuals over `es ++ extra`; the added edges carry nonnegative weight. Then
`Φs` is at most the larger residual of every potential, and `Φs ≤ Φl`. -/
theorem restriction_phi_le {C0 E : Type}
    (es extra : List E) (w δ : E → ℚ) (d0 : C0 → E → ℚ)
    (hw : ∀ e ∈ extra, 0 ≤ w e) (Φs Φl : ℚ)
    (lower_small : ∀ f, Φs ≤ sumOver es (fun e => w e * qabs (δ e - d0 f e)))
    (glb_large : ∀ b : ℚ,
      (∀ f, b ≤ sumOver (es ++ extra) (fun e => w e * qabs (δ e - d0 f e))) →
        b ≤ Φl) :
    (∀ f, Φs ≤ sumOver (es ++ extra) (fun e => w e * qabs (δ e - d0 f e)))
      ∧ Φs ≤ Φl :=
  phi_le_of_restriction
    (fun f => sumOver es (fun e => w e * qabs (δ e - d0 f e)))
    (fun f => sumOver (es ++ extra) (fun e => w e * qabs (δ e - d0 f e)))
    id Φs Φl lower_small (restriction_mass_le es extra w δ d0 hw) glb_large

/-! ## Subdivision -/

/-- Local subdivision identity. Replacing the edge `u → v` (weight `w ≥ 0`,
cochain value `x1 + x2`) by `u → m → v` (weights `w`, values `x1`, `x2`):
every midpoint potential `fm` leaves residual at least the unsubdivided
residual, and `fm = fu + x1` attains it. Hence the minimum over `fm` equals
`w * |x1 + x2 - (fv - fu)|`. -/
theorem subdivision_residual_eq (w x1 x2 fu fv : ℚ) (hw : 0 ≤ w) :
    (∀ fm : ℚ, w * qabs (x1 + x2 - (fv - fu)) ≤
        w * qabs (x1 - (fm - fu)) + w * qabs (x2 - (fv - fm)))
      ∧ w * qabs (x1 - ((fu + x1) - fu)) + w * qabs (x2 - (fv - (fu + x1))) =
        w * qabs (x1 + x2 - (fv - fu)) := by
  constructor
  · intro fm
    have hsplit : x1 + x2 - (fv - fu) = (x1 - (fm - fu)) + (x2 - (fv - fm)) := by
      grind
    rw [hsplit, ← Rat.mul_add]
    exact Rat.mul_le_mul_of_nonneg_left
      (qabs_add_le (x1 - (fm - fu)) (x2 - (fv - fm))) hw
  · have hzero : x1 - ((fu + x1) - fu) = 0 := by grind
    have hrest : x2 - (fv - (fu + x1)) = x1 + x2 - (fv - fu) := by grind
    have hqzero : qabs 0 = 0 := by
      unfold qabs
      split <;> grind
    rw [hzero, hrest, hqzero, Rat.mul_zero, Rat.zero_add]

/-- Subdivision invariance of the repair cost. The unsubdivided cost of a
potential `f` is `Jrest f + w * |x1 + x2 - (pv f - pu f)|`; the subdivided
cost of `(f, fm)` is `Jrest f + (w * |x1 - (fm - pu f)| + w * |x2 - (pv f - fm)|)`,
where `pu f` and `pv f` are the endpoint values of `f` and `Jrest` is the
unchanged remainder of the problem. If `Φ` and `Φ'` are the respective
infima (each given by its lower-bound and greatest-lower-bound halves), then
`Φ = Φ'`. -/
theorem subdivision_phi_eq {C0 : Type}
    (Jrest pu pv : C0 → ℚ) (w x1 x2 : ℚ) (hw : 0 ≤ w) (Φ Φ' : ℚ)
    (lower : ∀ f, Φ ≤ Jrest f + w * qabs (x1 + x2 - (pv f - pu f)))
    (glb : ∀ b : ℚ,
      (∀ f, b ≤ Jrest f + w * qabs (x1 + x2 - (pv f - pu f))) → b ≤ Φ)
    (lower' : ∀ f fm, Φ' ≤ Jrest f +
      (w * qabs (x1 - (fm - pu f)) + w * qabs (x2 - (pv f - fm))))
    (glb' : ∀ b : ℚ,
      (∀ f fm, b ≤ Jrest f +
        (w * qabs (x1 - (fm - pu f)) + w * qabs (x2 - (pv f - fm)))) → b ≤ Φ') :
    Φ = Φ' := by
  have hle : Φ ≤ Φ' := by
    apply glb' Φ
    intro f fm
    have hlocal := (subdivision_residual_eq w x1 x2 (pu f) (pv f) hw).1 fm
    have hphi := lower f
    grind
  have hge : Φ' ≤ Φ := by
    apply glb Φ'
    intro f
    have hattain := (subdivision_residual_eq w x1 x2 (pu f) (pv f) hw).2
    have hphi := lower' f (pu f + x1)
    rw [hattain] at hphi
    exact hphi
  exact Rat.le_antisymm hle hge

end WitnessedDifference.ComplexGrowth
