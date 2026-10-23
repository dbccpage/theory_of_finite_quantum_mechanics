/-!
# Component repair: raw versus quotient defect, and the 4/3 projection floor

Lean-core statements for the finite parts of the derivation proposals DP-3
and DP-4 (`coda_wdp_derivations_20261006`). Only `Init` is imported; rational
arithmetic is Lean core `Rat` with a local absolute value.

* DP-3. Weak duality in its general form: if `u = 0` is admissible, every
  lower bound of `u ↦ ‖Dx + Au‖` is at most the raw value `‖Dx‖`. The
  countermodel `n = 1`, `m = 2`, `Dx = (x,x)`, `Au = (u,0)`, weights `(1,1)`
  has equal zero tests (`Dx = 0` iff `Dx ∈ im A` iff `x = 0`) but
  `Γraw(1) = 2` and `Γquot(1) = 1`, attained at `u = -1` and certified by the
  dual vector `z = (0,1)`. With weights `(2,3)` the values are `5` and `3`.
* DP-4. Every rank-one projector `C = e aᵀ` onto `R = span(1,1,1)` in
  `ℓ¹³` (`a₁ + a₂ + a₃ = 1`) leaves `I - C` with some column of `ℓ¹` norm at
  least `4/3`; the value `4/3` is attained at `a = (1/3,1/3,1/3)`. For
  `x = (1,0,0)` the repaired vector has norm `4/3` while the quotient distance
  of `x` to `R` is `1` (dual `z = (1,-1,0)`). A two-dimensional control has
  ratio one.

Scope: the operator norm of `I - C` on `ℓ¹` is read as the maximum column
`ℓ¹` norm; that identification is standard finite linear algebra and is not
formalized here. Only rank-one projectors `e aᵀ` are covered; general
(non-rank-one or non-linear) repair maps are a residual. AuthorityEffect: None.
-/
namespace WitnessedDifference.ComponentRepair

/-- Absolute value on `Rat`. -/
def qabs (x : Rat) : Rat := if x < 0 then -x else x

theorem qabs_nonneg (x : Rat) : 0 ≤ qabs x := by
  unfold qabs; split <;> grind

theorem le_qabs (x : Rat) : x ≤ qabs x := by
  unfold qabs; split <;> grind

theorem neg_le_qabs (x : Rat) : -x ≤ qabs x := by
  unfold qabs; split <;> grind

/-! ## DP-3: raw versus quotient defect -/

/-- `v` is the attained minimum of `f`. -/
def IsMinValue {U : Type} (f : U → Rat) (v : Rat) : Prop :=
  (∃ u, f u = v) ∧ ∀ u, v ≤ f u

/-- DP-3 weak duality, general form: every lower bound of an objective that
admits `u = 0` is at most its value at `0`. -/
theorem lower_bound_le_raw {U : Type} [Zero U] (f : U → Rat) (m : Rat)
    (hm : ∀ u, m ≤ f u) : m ≤ f 0 :=
  hm 0

/-- DP-3: the quotient minimum never exceeds the raw value. -/
theorem quot_le_raw {U : Type} [Zero U] (f : U → Rat) (v : Rat)
    (hv : IsMinValue f v) : v ≤ f 0 :=
  hv.2 0

/-- The weighted `ℓ¹` norm of `Dx + Au = (x + u, x)` with weights `(w₁,w₂)`. -/
def residual (w₁ w₂ x u : Rat) : Rat := w₁ * qabs (x + u) + w₂ * qabs x

/-- DP-3 countermodel, weights `(1,1)`: `Γraw(1) = 2`. -/
theorem countermodel_raw : residual 1 1 1 0 = 2 := by
  unfold residual qabs; grind

/-- DP-3 countermodel, weights `(1,1)`: `Γquot(1) = 1`, attained at `u = -1`;
the lower bound is the dual vector `z = (0,1)`, which annihilates `im A`. -/
theorem countermodel_quot : IsMinValue (residual 1 1 1) 1 := by
  refine ⟨⟨-1, ?_⟩, ?_⟩
  · unfold residual qabs; grind
  · intro u
    have := qabs_nonneg (1 + u)
    unfold residual
    have h1 : qabs 1 = 1 := by unfold qabs; grind
    grind

/-- DP-3: the dual vector `z = (0,1)` annihilates `Au = (u,0)` and pairs to
`1` with `Dx = (1,1)`. -/
theorem countermodel_dual (u : Rat) : 0 * u + 1 * 0 = (0 : Rat) ∧
    0 * (1 : Rat) + 1 * 1 = 1 := by
  constructor <;> grind

/-- DP-3: the zero tests agree on the countermodel. `Dx = 0` iff `x = 0`, and
`Dx = Au` for some `u` iff `x = 0`. -/
theorem countermodel_zero_tests (x : Rat) :
    ((x, x) = ((0 : Rat), (0 : Rat)) ↔ x = 0) ∧
      ((∃ u : Rat, (x, x) = (u, (0 : Rat))) ↔ x = 0) := by
  constructor
  · constructor
    · intro h; exact congrArg Prod.fst h
    · intro h; rw [h]
  · constructor
    · rintro ⟨u, h⟩; exact congrArg Prod.snd h
    · intro h; exact ⟨0, by rw [h]⟩

/-- DP-3: the raw and quotient values differ although the zero tests agree. -/
theorem countermodel_values_differ :
    residual 1 1 1 0 = 2 ∧ IsMinValue (residual 1 1 1) 1 ∧ (1 : Rat) < 2 :=
  ⟨countermodel_raw, countermodel_quot, by grind⟩

/-- DP-3: weights `(2,3)` give raw value `5` and quotient value `3`. -/
theorem weighted_countermodel :
    residual 2 3 1 0 = 5 ∧ IsMinValue (residual 2 3 1) 3 := by
  refine ⟨?_, ⟨-1, ?_⟩, ?_⟩
  · unfold residual qabs; grind
  · unfold residual qabs; grind
  · intro u
    have := qabs_nonneg (1 + u)
    have h1 : qabs 1 = 1 := by unfold qabs; grind
    unfold residual
    grind

/-! ## DP-4: the 4/3 floor for rank-one projectors onto `span(1,1,1)` -/

/-- The `ℓ¹` norm of column `j` of `I - e aᵀ`: `|1 - a_j| + 2|a_j|`. -/
def colNorm (aj : Rat) : Rat := qabs (1 - aj) + 2 * qabs aj

/-- DP-4: each column norm is at least `1 + a_j`. -/
theorem colNorm_ge (aj : Rat) : 1 + aj ≤ colNorm aj := by
  have h1 := le_qabs (1 - aj)
  have h2 := le_qabs aj
  unfold colNorm
  grind

/-- DP-4: some column of `I - e aᵀ` has `ℓ¹` norm at least `4/3`. -/
theorem some_column_ge_four_thirds (a₁ a₂ a₃ : Rat) (hsum : a₁ + a₂ + a₃ = 1) :
    4 / 3 ≤ colNorm a₁ ∨ 4 / 3 ≤ colNorm a₂ ∨ 4 / 3 ≤ colNorm a₃ := by
  have h1 := colNorm_ge a₁
  have h2 := colNorm_ge a₂
  have h3 := colNorm_ge a₃
  grind

/-- DP-4: the floor `4/3` is attained at `a = (1/3,1/3,1/3)`. -/
theorem uniform_column_norm : colNorm (1 / 3) = 4 / 3 := by
  unfold colNorm qabs; grind

/-- The `ℓ¹` norm of a vector of `Rat³`. -/
def norm3 (v₁ v₂ v₃ : Rat) : Rat := qabs v₁ + qabs v₂ + qabs v₃

/-- DP-4: for `x = (1,0,0)` and the uniform projector, `Lx = x - (1/3)·e`
is `(2/3,-1/3,-1/3)`, of norm `4/3`. -/
theorem repaired_example_norm :
    norm3 (1 - 1 / 3) (0 - 1 / 3) (0 - 1 / 3) = 4 / 3 := by
  unfold norm3 qabs; grind

/-- DP-4: the distance of `x = (1,0,0)` to `R` is `1`, attained at `t = 0`;
the lower bound is the dual `z = (1,-1,0)`, which annihilates `e`. -/
theorem example_distance_to_R :
    IsMinValue (fun t : Rat => norm3 (1 - t) (0 - t) (0 - t)) 1 := by
  refine ⟨⟨0, ?_⟩, ?_⟩
  · unfold norm3 qabs; grind
  · intro t
    have h1 := le_qabs (1 - t)
    have h2 := neg_le_qabs (0 - t)
    have h3 := qabs_nonneg (0 - t)
    show 1 ≤ norm3 (1 - t) (0 - t) (0 - t)
    unfold norm3
    grind

/-- DP-4: on the example the repair increases the defect by the factor
`4/3` relative to the quotient distance. -/
theorem example_ratio :
    norm3 (1 - 1 / 3) (0 - 1 / 3) (0 - 1 / 3) = (4 / 3) * 1 :=
  by rw [repaired_example_norm]; grind

/-- DP-4 two-dimensional control: `C = (1/2)[[1,1],[1,1]]`, `x = (3,1)`,
`Lx = (1,-1)` has norm `2`, equal to the distance of `x` to `span(1,1)`. -/
theorem planar_control :
    qabs (3 - (3 + 1) / 2) + qabs (1 - (3 + 1) / 2) = 2 ∧
      IsMinValue (fun t : Rat => qabs (3 - t) + qabs (1 - t)) 2 := by
  refine ⟨?_, ⟨1, ?_⟩, ?_⟩
  · unfold qabs; grind
  · unfold qabs; grind
  · intro t
    have h1 := le_qabs (3 - t)
    have h2 := neg_le_qabs (1 - t)
    grind

end WitnessedDifference.ComponentRepair
