import WitnessedDifference.Core

/-!
# Degree-1 obstruction window

This module mechanizes the degree-1 obstruction window over exact rationals
and over the repair quotient `Q1 = C1 / im d0` itself.

- Closure descent: an additive `d1` with `d1 ∘ d0 = 0` descends to
  `kappa : Q1 → C2`.
- Exactness of `0 → H1 → Q1 → im d1 → 0` on the quotient, where `H1` is the
  kernel of `kappa` and closedness does not depend on the representative.
- The closure-ratio bound `Γ / Φ ≤ c` over `ℚ`, derived from an operator
  bound, repair invariance of `Γ`, and the greatest-lower-bound property of
  the repair cost `Φ`.
- Weak duality for a weighted ℓ¹ repair cost: a bounded dual vector that
  annihilates every coboundary certifies a lower bound for every repair.
- The filled-triangle signature: minimum residual mass `2`, closure charge
  `2`, closure ratio `1`, and ℓ¹-to-ℓ¹ operator norm `1` for the boundary row.
- Observer passivity from the fiberwise infimum characterization.

Infima are not constructed. Where `Φ` or `Φ_O` is an infimum, the theorem
takes the half of the infimum characterization that it uses as a hypothesis
and names it. This file declares no synthetic axioms.
-/

namespace WitnessedDifference.Obstruction

/-! ## Closure descent on the repair quotient -/

section ClosureDescent

variable {C0 C1 C2 : Type} [Add C1] [Add C2] [Zero C2]

/-- Two degree-1 cochains are repair-related when the second is the first
plus an exact repair `d0 α`. -/
def Repair (d0 : C0 → C1) : C1 → C1 → Prop :=
  fun h h' => ∃ α, h' = h + d0 α

/-- The repair quotient `Q1 = C1 / im d0`, built as the quotient by
`Repair d0`. -/
abbrev Q1 (d0 : C0 → C1) : Type :=
  Quot (Repair d0)

/-- An exact repair does not change the repair class. -/
theorem mk_repair (d0 : C0 → C1) (h : C1) (α : C0) :
    Quot.mk (Repair d0) (h + d0 α) = Quot.mk (Repair d0) h :=
  (Quot.sound ⟨α, rfl⟩).symm

/-- Closure charge is invariant under exact repair. -/
theorem kappa_well_defined
    (d0 : C0 → C1) (d1 : C1 → C2)
    (d1_add : ∀ x y : C1, d1 (x + y) = d1 x + d1 y)
    (d1_d0 : ∀ α : C0, d1 (d0 α) = 0)
    (add_zero_right : ∀ z : C2, z + 0 = z)
    (h h' : C1) (α : C0) (hrep : h' = h + d0 α) :
    d1 h' = d1 h := by
  rw [hrep, d1_add, d1_d0, add_zero_right]

/-- The descended closure map `kappa : Q1 → C2`. -/
def kappa
    (d0 : C0 → C1) (d1 : C1 → C2)
    (d1_add : ∀ x y : C1, d1 (x + y) = d1 x + d1 y)
    (d1_d0 : ∀ α : C0, d1 (d0 α) = 0)
    (add_zero_right : ∀ z : C2, z + 0 = z) :
    Q1 d0 → C2 :=
  Quot.lift d1 (fun h h' hrel =>
    match hrel with
    | ⟨α, hrep⟩ =>
      (kappa_well_defined d0 d1 d1_add d1_d0 add_zero_right h h' α hrep).symm)

theorem kappa_mk
    (d0 : C0 → C1) (d1 : C1 → C2)
    (d1_add : ∀ x y : C1, d1 (x + y) = d1 x + d1 y)
    (d1_d0 : ∀ α : C0, d1 (d0 α) = 0)
    (add_zero_right : ∀ z : C2, z + 0 = z)
    (h : C1) :
    kappa d0 d1 d1_add d1_d0 add_zero_right (Quot.mk (Repair d0) h) = d1 h :=
  rfl

/-- The degree-1 cohomology `H1`: repair classes with zero closure charge. -/
abbrev H1
    (d0 : C0 → C1) (d1 : C1 → C2)
    (d1_add : ∀ x y : C1, d1 (x + y) = d1 x + d1 y)
    (d1_d0 : ∀ α : C0, d1 (d0 α) = 0)
    (add_zero_right : ∀ z : C2, z + 0 = z) : Type :=
  {q : Q1 d0 // kappa d0 d1 d1_add d1_d0 add_zero_right q = 0}

/-- Exactness of `0 → H1 → Q1 → im d1 → 0` on the repair quotient:
(i) the inclusion `H1 → Q1` is injective; (ii) its image is exactly the
kernel of `kappa`; (iii) a class has zero closure charge exactly when every
representative is closed; (iv) `kappa` maps onto `im d1`. -/
theorem kappa_exact_sequence
    (d0 : C0 → C1) (d1 : C1 → C2)
    (d1_add : ∀ x y : C1, d1 (x + y) = d1 x + d1 y)
    (d1_d0 : ∀ α : C0, d1 (d0 α) = 0)
    (add_zero_right : ∀ z : C2, z + 0 = z) :
    _root_.Function.Injective
        (Subtype.val : H1 d0 d1 d1_add d1_d0 add_zero_right → Q1 d0)
      ∧ (∀ q : Q1 d0,
          kappa d0 d1 d1_add d1_d0 add_zero_right q = 0 ↔
            ∃ k : H1 d0 d1 d1_add d1_d0 add_zero_right, k.val = q)
      ∧ (∀ q : Q1 d0,
          kappa d0 d1 d1_add d1_d0 add_zero_right q = 0 ↔
            ∀ h : C1, Quot.mk (Repair d0) h = q → d1 h = 0)
      ∧ (∀ z : C2,
          (∃ h : C1, d1 h = z) ↔
            ∃ q : Q1 d0, kappa d0 d1 d1_add d1_d0 add_zero_right q = z) := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro a b hab
    exact Subtype.ext hab
  · intro q
    constructor
    · intro hq
      exact ⟨⟨q, hq⟩, rfl⟩
    · rintro ⟨k, rfl⟩
      exact k.property
  · intro q
    constructor
    · intro hq h hmk
      subst hmk
      exact hq
    · intro hall
      obtain ⟨h, rfl⟩ := Quot.exists_rep q
      exact hall h rfl
  · intro z
    constructor
    · rintro ⟨h, rfl⟩
      exact ⟨Quot.mk (Repair d0) h, rfl⟩
    · rintro ⟨q, hq⟩
      obtain ⟨h, rfl⟩ := Quot.exists_rep q
      exact ⟨h, hq⟩

end ClosureDescent

/-! ## Closure-ratio bound over `ℚ` -/

theorem closure_ratio_le_opnorm (Γ Φ c : ℚ) (hΦ : 0 < Φ) (h : Γ ≤ c * Φ) :
    Γ / Φ ≤ c := by
  apply Rat.le_of_mul_le_mul_right _ hΦ
  rw [Rat.div_mul_cancel (Rat.ne_of_gt hΦ)]
  exact h

theorem closure_ratio_nonneg (Γ Φ : ℚ) (hΓ : 0 ≤ Γ) (hΦ : 0 < Φ) :
    0 ≤ Γ / Φ := by
  rw [Rat.div_def]
  exact Rat.mul_nonneg hΓ (Rat.le_of_lt (Rat.inv_pos.mpr hΦ))

/-- Theorem E(4) from the infimum characterization. `Γ` is invariant under
exact repair, is bounded by `c` times the repair cost `J`, and `Φ` is the
greatest lower bound of the repair costs `J (h + d0 α)`. Then `Γ h ≤ c * Φ`.
No minimizing repair is assumed to exist. -/
theorem closure_charge_le_opnorm_mul_phi {C0 C1 : Type} [Add C1]
    (d0 : C0 → C1) (J Γ : C1 → ℚ) (Φ c : ℚ) (h : C1)
    (hc : 0 ≤ c)
    (descent : ∀ α, Γ (h + d0 α) = Γ h)
    (opbound : ∀ x, Γ x ≤ c * J x)
    (glb : ∀ b : ℚ, (∀ α, b ≤ J (h + d0 α)) → b ≤ Φ) :
    Γ h ≤ c * Φ := by
  by_cases hzero : c = 0
  · subst hzero
    have hbound := opbound h
    rw [Rat.zero_mul] at hbound ⊢
    exact hbound
  · have hpos : 0 < c := Rat.lt_of_le_of_ne hc (Ne.symm hzero)
    have hlower : ∀ α, Γ h / c ≤ J (h + d0 α) := by
      intro α
      apply Rat.le_of_mul_le_mul_right _ hpos
      rw [Rat.div_mul_cancel (Rat.ne_of_gt hpos), Rat.mul_comm (J (h + d0 α)) c,
        ← descent α]
      exact opbound (h + d0 α)
    have hphi : Γ h / c ≤ Φ := glb (Γ h / c) hlower
    have hscaled := Rat.mul_le_mul_of_nonneg_left hphi hc
    rw [Rat.mul_comm c (Γ h / c), Rat.div_mul_cancel (Rat.ne_of_gt hpos)] at hscaled
    exact hscaled

theorem closure_ratio_bound_of_infimum {C0 C1 : Type} [Add C1]
    (d0 : C0 → C1) (J Γ : C1 → ℚ) (Φ c : ℚ) (h : C1)
    (hc : 0 ≤ c) (hΦ : 0 < Φ)
    (descent : ∀ α, Γ (h + d0 α) = Γ h)
    (opbound : ∀ x, Γ x ≤ c * J x)
    (glb : ∀ b : ℚ, (∀ α, b ≤ J (h + d0 α)) → b ≤ Φ) :
    Γ h / Φ ≤ c :=
  closure_ratio_le_opnorm (Γ h) Φ c hΦ
    (closure_charge_le_opnorm_mul_phi d0 J Γ Φ c h hc descent opbound glb)

/-- Row WDP-CH04-P06 over ℚ-valued costs: with a nonnegative closure mass and a
positive quotient mass, the closure ratio lies between `0` and any operator
bound `c`, given the greatest-lower-bound half of the infimum property. -/
theorem closure_ratio_signature {C0 C1 : Type} [Add C1]
    (d0 : C0 → C1) (J Γ : C1 → ℚ) (Φ c : ℚ) (h : C1)
    (hc : 0 ≤ c) (hΦ : 0 < Φ) (hΓ : 0 ≤ Γ h)
    (descent : ∀ α, Γ (h + d0 α) = Γ h)
    (opbound : ∀ x, Γ x ≤ c * J x)
    (glb : ∀ b : ℚ, (∀ α, b ≤ J (h + d0 α)) → b ≤ Φ) :
    0 ≤ Γ h / Φ ∧ Γ h / Φ ≤ c :=
  ⟨closure_ratio_nonneg (Γ h) Φ hΓ hΦ,
   closure_ratio_bound_of_infimum d0 J Γ Φ c h hc hΦ descent opbound glb⟩

/-! ## Weak duality for a weighted ℓ¹ repair cost -/

/-- Absolute value on `ℚ`. -/
def qabs (x : ℚ) : ℚ := if x < 0 then -x else x

/-- Finite sum over an edge list. -/
def sumOver {E : Type} (es : List E) (g : E → ℚ) : ℚ :=
  es.foldr (fun e acc => g e + acc) 0

@[simp] theorem sumOver_nil {E : Type} (g : E → ℚ) : sumOver [] g = 0 := rfl

@[simp] theorem sumOver_cons {E : Type} (e : E) (es : List E) (g : E → ℚ) :
    sumOver (e :: es) g = g e + sumOver es g := rfl

theorem sumOver_add {E : Type} (es : List E) (g k : E → ℚ) :
    sumOver es (fun e => g e + k e) = sumOver es g + sumOver es k := by
  induction es with
  | nil => simp only [sumOver_nil]; grind
  | cons e es ih =>
    simp only [sumOver_cons, ih]
    grind

theorem sumOver_le {E : Type} (es : List E) (g k : E → ℚ)
    (hle : ∀ e ∈ es, g e ≤ k e) :
    sumOver es g ≤ sumOver es k := by
  induction es with
  | nil => exact Rat.le_refl
  | cons e es ih =>
    simp only [sumOver_cons]
    have hhead := hle e (List.mem_cons_self ..)
    have htail := ih (fun x hx => hle x (List.mem_cons_of_mem _ hx))
    grind

/-- A dual coefficient bounded by the weight pairs with any residual below the
weighted absolute residual. -/
theorem mul_le_weight_mul_qabs (y w r : ℚ) (hlo : -w ≤ y) (hhi : y ≤ w) :
    y * r ≤ w * qabs r := by
  unfold qabs
  split
  · have hnr : 0 ≤ -r := by grind
    have hflip := Rat.mul_le_mul_of_nonneg_right (show -y ≤ w by grind) hnr
    have hsign : -y * -r = y * r := by grind
    rw [hsign] at hflip
    exact hflip
  · have hnn : 0 ≤ r := by grind
    exact Rat.mul_le_mul_of_nonneg_right hhi hnn

/-- Weak duality: a dual vector `y` with `d0* y = 0` and `|y e| ≤ w e` pairs
with the defect `δ` below the weighted ℓ¹ residual of every repair. -/
theorem dual_certificate_lower_bound {C0 E : Type}
    (es : List E) (y w δ : E → ℚ) (d0 : C0 → E → ℚ)
    (annihilates : ∀ f, sumOver es (fun e => y e * d0 f e) = 0)
    (bounded : ∀ e ∈ es, -w e ≤ y e ∧ y e ≤ w e) :
    ∀ f, sumOver es (fun e => y e * δ e) ≤
      sumOver es (fun e => w e * qabs (δ e - d0 f e)) := by
  intro f
  have hsplit : sumOver es (fun e => y e * δ e) =
      sumOver es (fun e => y e * (δ e - d0 f e)) +
        sumOver es (fun e => y e * d0 f e) := by
    rw [← sumOver_add]
    exact congrArg (sumOver es) (funext fun e => by grind)
  rw [hsplit, annihilates f]
  have hmass := sumOver_le es (fun e => y e * (δ e - d0 f e))
    (fun e => w e * qabs (δ e - d0 f e))
    (fun e he => mul_le_weight_mul_qabs (y e) (w e) (δ e - d0 f e)
      (bounded e he).1 (bounded e he).2)
  grind

/-- A dual certificate whose pairing equals the residual of `fstar`
certifies that `fstar` is an optimal repair. -/
theorem matching_certificate_is_optimal {C0 E : Type}
    (es : List E) (y w δ : E → ℚ) (d0 : C0 → E → ℚ) (fstar : C0)
    (annihilates : ∀ f, sumOver es (fun e => y e * d0 f e) = 0)
    (bounded : ∀ e ∈ es, -w e ≤ y e ∧ y e ≤ w e)
    (pairing_eq : sumOver es (fun e => y e * δ e) =
      sumOver es (fun e => w e * qabs (δ e - d0 fstar e))) :
    ∀ f, sumOver es (fun e => w e * qabs (δ e - d0 fstar e)) ≤
      sumOver es (fun e => w e * qabs (δ e - d0 f e)) := by
  intro f
  rw [← pairing_eq]
  exact dual_certificate_lower_bound es y w δ d0 annihilates bounded f

/-! ## The filled triangle

Vertices `0, 1, 2`; edges ordered `(01, 12, 02)`; one filled face. -/

inductive TriEdge where
  | e01
  | e12
  | e02
  deriving DecidableEq

def triEdges : List TriEdge := [.e01, .e12, .e02]

/-- `d0 f = (f1 - f0, f2 - f1, f2 - f0)`. -/
def triD0 : ℚ × ℚ × ℚ → TriEdge → ℚ
  | (f0, f1, _), .e01 => f1 - f0
  | (_, f1, f2), .e12 => f2 - f1
  | (f0, _, f2), .e02 => f2 - f0

/-- `d1 (x01, x12, x02) = x01 + x12 - x02`. -/
def triD1 (x : TriEdge → ℚ) : ℚ :=
  x .e01 + x .e12 - x .e02

/-- The single row of `d1`, as coefficients `(1, 1, -1)`. -/
def triD1Row : TriEdge → ℚ
  | .e01 => 1
  | .e12 => 1
  | .e02 => -1

/-- The worked defect `δ = (1, 1, 0)`. -/
def triDefect : TriEdge → ℚ
  | .e01 => 1
  | .e12 => 1
  | .e02 => 0

/-- The dual certificate `y = (1, 1, -1)`. -/
def triDual : TriEdge → ℚ
  | .e01 => 1
  | .e12 => 1
  | .e02 => -1

def triUnitWeight : TriEdge → ℚ := fun _ => 1

/-- Unit-weight ℓ¹ residual `Σ_e |δ e - (d0 f) e|`. -/
def triResidualMass (f : ℚ × ℚ × ℚ) : ℚ :=
  sumOver triEdges (fun e => triUnitWeight e * qabs (triDefect e - triD0 f e))

/-- ℓ¹ norm of an edge cochain. -/
def triL1 (x : TriEdge → ℚ) : ℚ :=
  sumOver triEdges (fun e => qabs (x e))

/-- The unit edge cochain supported on edge `01`. -/
def triUnit01 : TriEdge → ℚ
  | .e01 => 1
  | .e12 => 0
  | .e02 => 0

theorem tri_d1_d0 (f0 f1 f2 : ℚ) : triD1 (triD0 (f0, f1, f2)) = 0 := by
  simp only [triD1, triD0]
  grind

theorem tri_dual_annihilates (f : ℚ × ℚ × ℚ) :
    sumOver triEdges (fun e => triDual e * triD0 f e) = 0 := by
  obtain ⟨f0, f1, f2⟩ := f
  simp only [triEdges, sumOver_cons, sumOver_nil, triDual, triD0]
  grind

theorem tri_dual_bounded :
    ∀ e ∈ triEdges, -triUnitWeight e ≤ triDual e ∧ triDual e ≤ triUnitWeight e := by
  intro e _
  cases e <;> simp only [triUnitWeight, triDual] <;> grind

theorem tri_dual_pairing :
    sumOver triEdges (fun e => triDual e * triDefect e) = 2 := by
  simp only [triEdges, sumOver_cons, sumOver_nil, triDual, triDefect]
  grind

/-- The lower bound `2 ≤ Φ` is obtained from the dual certificate. -/
theorem tri_residual_lower_bound (f0 f1 f2 : ℚ) :
    2 ≤ triResidualMass (f0, f1, f2) := by
  have hcert := dual_certificate_lower_bound triEdges triDual triUnitWeight
    triDefect triD0 tri_dual_annihilates tri_dual_bounded (f0, f1, f2)
  rw [tri_dual_pairing] at hcert
  exact hcert

theorem tri_residual_at_witness : triResidualMass (0, 1, 0) = 2 := by
  simp only [triResidualMass, triEdges, sumOver_cons, sumOver_nil,
    triUnitWeight, triDefect, triD0, qabs]
  grind

theorem tri_closure_charge : qabs (triD1 triDefect) = 2 := by
  simp only [qabs, triD1, triDefect]
  grind

theorem tri_dual_linf (e : TriEdge) : qabs (triDual e) ≤ 1 := by
  cases e <;> simp only [qabs, triDual] <;> grind

theorem tri_closure_ratio :
    qabs (triD1 triDefect) / triResidualMass (0, 1, 0) = 1 := by
  rw [tri_closure_charge, tri_residual_at_witness, Rat.div_def]
  exact Rat.mul_inv_cancel 2 (by grind)

theorem tri_d1_row (x : TriEdge → ℚ) :
    triD1 x = sumOver triEdges (fun e => triD1Row e * x e) := by
  simp only [triD1, triEdges, sumOver_cons, sumOver_nil, triD1Row]
  grind

theorem tri_d1_row_bounded (e : TriEdge) : qabs (triD1Row e) ≤ 1 := by
  cases e <;> simp only [qabs, triD1Row] <;> grind

theorem tri_d1_opbound (x : TriEdge → ℚ) : qabs (triD1 x) ≤ 1 * triL1 x := by
  simp only [qabs, triD1, triL1, triEdges, sumOver_cons, sumOver_nil]
  grind

theorem tri_d1_opnorm_least (c : ℚ) (hc : ∀ x, qabs (triD1 x) ≤ c * triL1 x) :
    1 ≤ c := by
  have hcharge : qabs (triD1 triUnit01) = 1 := by
    simp only [qabs, triD1, triUnit01]
    grind
  have hnorm : triL1 triUnit01 = 1 := by
    simp only [qabs, triL1, triEdges, sumOver_cons, sumOver_nil, triUnit01]
    grind
  have hunit := hc triUnit01
  rw [hcharge, hnorm] at hunit
  grind

/-- The filled-triangle signature over `ℚ`:
(1) `d1 ∘ d0 = 0`; (2) every repair leaves unit-weight ℓ¹ residual at least
`2`; (3) the repair `f = (0, 1, 0)` attains `2`, so `Φ = 2`; (4) the closure
charge is `Γ = |d1 δ| = 2`; (5) `y = (1, 1, -1)` annihilates every coboundary,
has `|y e| ≤ 1`, and pairs with `δ` to `2`; (6) the closure ratio is
`Γ / Φ = 1`; (7) the single row of `d1` has maximum absolute column entry `1`,
and `1` is the least constant `c` with `|d1 x| ≤ c ‖x‖₁`, so
`‖d1‖₁→₁ = 1` and the triangle saturates `Γ / Φ ≤ ‖d1‖₁→₁`. -/
theorem filled_triangle_signature :
    (∀ f0 f1 f2 : ℚ, triD1 (triD0 (f0, f1, f2)) = 0)
      ∧ (∀ f0 f1 f2 : ℚ, 2 ≤ triResidualMass (f0, f1, f2))
      ∧ triResidualMass (0, 1, 0) = 2
      ∧ qabs (triD1 triDefect) = 2
      ∧ ((∀ f0 f1 f2 : ℚ,
            sumOver triEdges (fun e => triDual e * triD0 (f0, f1, f2) e) = 0)
          ∧ (∀ e, qabs (triDual e) ≤ 1)
          ∧ sumOver triEdges (fun e => triDual e * triDefect e) = 2)
      ∧ qabs (triD1 triDefect) / triResidualMass (0, 1, 0) = 1
      ∧ ((∀ x, triD1 x = sumOver triEdges (fun e => triD1Row e * x e))
          ∧ (∀ e, qabs (triD1Row e) ≤ 1)
          ∧ qabs (triD1Row .e01) = 1
          ∧ (∀ x, qabs (triD1 x) ≤ 1 * triL1 x)
          ∧ (∀ c : ℚ, (∀ x, qabs (triD1 x) ≤ c * triL1 x) → 1 ≤ c)) := by
  refine ⟨tri_d1_d0, tri_residual_lower_bound, tri_residual_at_witness,
    tri_closure_charge,
    ⟨fun f0 f1 f2 => tri_dual_annihilates (f0, f1, f2), tri_dual_linf,
      tri_dual_pairing⟩,
    tri_closure_ratio,
    ⟨tri_d1_row, tri_d1_row_bounded, ?_, tri_d1_opbound, tri_d1_opnorm_least⟩⟩
  simp only [qabs, triD1Row]
  grind

/-! ## Observer passivity -/

/-- Observer passivity from the fiberwise infimum characterization. The
hypothesis `lower` is the lower-bound half of
`Φ_O y = inf {Φ r | O r = y}`; instantiated at `y = O q` it is the passivity
inequality itself. -/
theorem observer_passivity_of_infimum {Q R : Type}
    (O : Q → R) (Φ : Q → ℚ) (ΦO : R → ℚ)
    (lower : ∀ y r, O r = y → ΦO y ≤ Φ r) (q : Q) :
    ΦO (O q) ≤ Φ q ∧ (0 < ΦO (O q) → 0 < Φ q) ∧ (Φ q ≤ 0 → ΦO (O q) ≤ 0) := by
  have hle := lower (O q) q rfl
  refine ⟨hle, ?_, ?_⟩
  · intro hpos
    grind
  · intro hnonpos
    grind

/-- The induced observer norm is the largest passive observer functional:
from the greatest-lower-bound half of the fiberwise infimum, any `Ψ` with
`Ψ (O r) ≤ Φ r` for all `r` lies below `Φ_O` everywhere. -/
theorem induced_observer_norm_largest_passive {Q R : Type}
    (O : Q → R) (Φ : Q → ℚ) (ΦO : R → ℚ)
    (glb : ∀ y b, (∀ r, O r = y → b ≤ Φ r) → b ≤ ΦO y)
    (Ψ : R → ℚ) (passive : ∀ r, Ψ (O r) ≤ Φ r) :
    ∀ y, Ψ y ≤ ΦO y := by
  intro y
  apply glb y
  intro r hr
  subst hr
  exact passive r

/-- Exact classes stay exact: with a nonnegative core functional and both
halves of the fiberwise infimum, `Φ q = 0` forces `Φ_O (O q) = 0`. -/
theorem observer_exact_class_stays_exact {Q R : Type}
    (O : Q → R) (Φ : Q → ℚ) (ΦO : R → ℚ)
    (lower : ∀ y r, O r = y → ΦO y ≤ Φ r)
    (glb : ∀ y b, (∀ r, O r = y → b ≤ Φ r) → b ≤ ΦO y)
    (Φ_nonneg : ∀ r, 0 ≤ Φ r) (q : Q) (hexact : Φ q = 0) :
    ΦO (O q) = 0 := by
  have hupper := lower (O q) q rfl
  have hlower : 0 ≤ ΦO (O q) := glb (O q) 0 (fun r _ => Φ_nonneg r)
  grind

end WitnessedDifference.Obstruction
