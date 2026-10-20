import BornEffectValuation
import Mathlib.Algebra.Module.LinearMap.Rat
import Mathlib.Tactic.Module

/- The scalar identities below are closed by the uniform block `match_scalars <;> field_simp <;> ring`;
how many goals survive `field_simp` varies by site, so the three style linters that comment on
`<;>` and on unexecuted `ring` calls are disabled for this file.  They affect no proof content. -/
set_option linter.unnecessarySeqFocus false
set_option linter.unusedTactic false
set_option linter.unreachableTactic false

/-
Linear extension of an effect valuation.  AuthorityEffect: None.

Given an `OrderedQUnit` whose unit is an order unit (every element lies between `-(k • u)` and
`k • u` for some natural `k`) and an `EffectValuation`, this file builds the ℚ-linear functional
on `V` that agrees with the valuation on effects, and shows that it is unital, positive on the
positive cone, and the unique ℚ-linear functional agreeing with the valuation on effects.

Method (the user's reviewed written Steps 04–07, made exact): for `a` bounded by `t > 0` the
element `m_t(a) := (1/(2t)) • (a + t • u)` is an effect, and the value
`2t · v(m_t(a)) - t` does not depend on the admissible bound `t`.  Additivity of the resulting
function is checked on a common bound, and additivity on a ℚ-module already gives ℚ-linearity
(`AddMonoidHom.toRatLinearMap`).  No continuity, real scalars, or matrix structure is used.
-/

namespace BornFable

variable {V : Type*} [AddCommGroup V] [Module ℚ V]

namespace OrderedQUnit

variable (S : OrderedQUnit V)

/-- `a` lies in the symmetric interval `[-(t • u), t • u]`. -/
def Bounded (a : V) (t : ℚ) : Prop := S.le (-(t • S.u)) a ∧ S.le a (t • S.u)

/-- The unit is an order unit: every element is bounded by some natural multiple of `u`. -/
def IsOrderUnit : Prop := ∀ a : V, ∃ k : ℕ, S.Bounded a k

theorem bounded_mono {a : V} {s t : ℚ} (hst : s ≤ t) (h : S.Bounded a s) : S.Bounded a t := by
  have hdiff : S.le 0 ((t - s) • S.u) := S.smul_nonneg (t - s) S.u (by linarith) S.u_nonneg
  constructor
  · have h1 : S.le (-(t • S.u)) (-(s • S.u)) := by
      apply S.le_of_sub_nonneg
      have e : -(s • S.u) - -(t • S.u) = (t - s) • S.u := by
        rw [sub_smul]
        abel
      rw [e]
      exact hdiff
    exact S.le_trans _ _ _ h1 h.1
  · have h2 : S.le (s • S.u) (t • S.u) := by
      apply S.le_of_sub_nonneg
      have e : t • S.u - s • S.u = (t - s) • S.u := by rw [sub_smul]
      rw [e]
      exact hdiff
    exact S.le_trans _ _ _ h.2 h2

theorem bounded_add {a b : V} {s t : ℚ} (ha : S.Bounded a s) (hb : S.Bounded b t) :
    S.Bounded (a + b) (s + t) := by
  constructor
  · have h1 := S.add_le_add_right _ _ b ha.1
    have h2 := S.add_le_add_right _ _ (-(s • S.u)) hb.1
    have e1 : -(t • S.u) + -(s • S.u) = -((s + t) • S.u) := by
      rw [add_smul]
      abel
    have e2 : b + -(s • S.u) = -(s • S.u) + b := by abel
    rw [e1, e2] at h2
    exact S.le_trans _ _ _ h2 h1
  · have h1 := S.add_le_add_right _ _ b ha.2
    have h2 := S.add_le_add_right _ _ (s • S.u) hb.2
    have e1 : b + s • S.u = s • S.u + b := by abel
    have e2 : t • S.u + s • S.u = (s + t) • S.u := by
      rw [add_smul]
      abel
    rw [e1, e2] at h2
    exact S.le_trans _ _ _ h1 h2

theorem bounded_of_effect {a : V} (ha : S.Effect a) : S.Bounded a 1 := by
  constructor
  · have h0 : S.le (-((1 : ℚ) • S.u)) 0 := by
      apply S.le_of_sub_nonneg
      rw [one_smul, zero_sub, neg_neg]
      exact S.u_nonneg
    exact S.le_trans _ _ _ h0 ha.1
  · rw [one_smul]
    exact ha.2

/-- The effect attached to an element bounded by `t`: `(1/(2t)) • (a + t • u)`. -/
def midpoint (a : V) (t : ℚ) : V := (1 / (2 * t)) • (a + t • S.u)

theorem midpoint_effect {a : V} {t : ℚ} (ht : 0 < t) (h : S.Bounded a t) :
    S.Effect (S.midpoint a t) := by
  have ht0 : t ≠ 0 := ht.ne'
  have hc0 : (0 : ℚ) ≤ 1 / (2 * t) := by positivity
  constructor
  · apply S.smul_nonneg _ _ hc0
    have := S.add_le_add_right _ _ (t • S.u) h.1
    rw [neg_add_cancel] at this
    exact this
  · apply S.le_of_sub_nonneg
    have e : S.u - S.midpoint a t = (1 / (2 * t)) • (t • S.u - a) := by
      unfold midpoint
      match_scalars <;> field_simp <;> ring
    rw [e]
    exact S.smul_nonneg _ _ hc0 (S.sub_nonneg_of_le h.2)

/-- The extension value computed at an admissible bound `t`. -/
def extAt (W : EffectValuation S) (a : V) (t : ℚ) : ℚ := 2 * t * W.v (S.midpoint a t) - t

theorem extAt_add (W : EffectValuation S) {a b : V} {s t : ℚ} (hs : 0 < s) (ht : 0 < t)
    (ha : S.Bounded a s) (hb : S.Bounded b t) :
    S.extAt W (a + b) (s + t) = S.extAt W a s + S.extAt W b t := by
  have hst : 0 < s + t := by linarith
  have hs0 : s ≠ 0 := hs.ne'
  have ht0 : t ≠ 0 := ht.ne'
  have hst0 : s + t ≠ 0 := hst.ne'
  have hq1 : 0 ≤ s / (s + t) := by positivity
  have hq1' : s / (s + t) ≤ 1 := by
    rw [div_le_one hst]
    linarith
  have hq2 : 0 ≤ t / (s + t) := by positivity
  have hq2' : t / (s + t) ≤ 1 := by
    rw [div_le_one hst]
    linarith
  have hea := S.midpoint_effect hs ha
  have heb := S.midpoint_effect ht hb
  have heab := S.midpoint_effect hst (S.bounded_add ha hb)
  have e : S.midpoint (a + b) (s + t) =
      (s / (s + t)) • S.midpoint a s + (t / (s + t)) • S.midpoint b t := by
    unfold midpoint
    match_scalars <;> field_simp <;> ring
  have h1 := effect_smul S _ hq1 hq1' hea
  have h2 := effect_smul S _ hq2 hq2' heb
  have hadd := W.additive _ _ h1 h2 (by rw [← e]; exact heab)
  unfold extAt
  rw [e, hadd, val_rat_smul S W _ hq1 hq1' hea, val_rat_smul S W _ hq2 hq2' heb]
  field_simp
  ring

theorem extAt_mono (W : EffectValuation S) {a : V} {s t : ℚ} (hs : 0 < s) (hst : s ≤ t)
    (ha : S.Bounded a s) : S.extAt W a s = S.extAt W a t := by
  have ht : 0 < t := lt_of_lt_of_le hs hst
  have hs0 : s ≠ 0 := hs.ne'
  have ht0 : t ≠ 0 := ht.ne'
  have hq1 : 0 ≤ s / t := by positivity
  have hq1' : s / t ≤ 1 := by
    rw [div_le_one ht]
    exact hst
  have hq2 : 0 ≤ (t - s) / (2 * t) := by
    apply div_nonneg <;> linarith
  have hq2' : (t - s) / (2 * t) ≤ 1 := by
    rw [div_le_one (by linarith)]
    linarith
  have hes := S.midpoint_effect hs ha
  have het := S.midpoint_effect ht (S.bounded_mono hst ha)
  have e : S.midpoint a t = (s / t) • S.midpoint a s + ((t - s) / (2 * t)) • S.u := by
    unfold midpoint
    match_scalars <;> field_simp <;> ring
  have h1 := effect_smul S _ hq1 hq1' hes
  have h2 := effect_smul S _ hq2 hq2' S.effect_u
  have hadd := W.additive _ _ h1 h2 (by rw [← e]; exact het)
  unfold extAt
  rw [e, hadd, val_rat_smul S W _ hq1 hq1' hes, val_rat_smul S W _ hq2 hq2' S.effect_u, W.unit]
  field_simp
  ring

theorem extAt_eq (W : EffectValuation S) {a : V} {s t : ℚ} (hs : 0 < s) (ht : 0 < t)
    (ha : S.Bounded a s) (ha' : S.Bounded a t) : S.extAt W a s = S.extAt W a t := by
  rw [S.extAt_mono W hs (by linarith : s ≤ s + t) ha,
    S.extAt_mono W ht (by linarith : t ≤ s + t) ha']

/-- A positive rational bound for `a`, chosen from the order-unit property. -/
noncomputable def bound (hU : S.IsOrderUnit) (a : V) : ℚ :=
  ((Classical.choose (hU a) : ℕ) : ℚ) + 1

theorem bound_pos (hU : S.IsOrderUnit) (a : V) : 0 < S.bound hU a := by
  unfold bound
  positivity

theorem bounded_bound (hU : S.IsOrderUnit) (a : V) : S.Bounded a (S.bound hU a) :=
  S.bounded_mono (by unfold bound; linarith) (Classical.choose_spec (hU a))

/-- The extension of `W` to all of `V`, as a function. -/
noncomputable def extend (hU : S.IsOrderUnit) (W : EffectValuation S) (a : V) : ℚ :=
  S.extAt W a (S.bound hU a)

theorem extend_eq_extAt (hU : S.IsOrderUnit) (W : EffectValuation S) {a : V} {t : ℚ}
    (ht : 0 < t) (ha : S.Bounded a t) : S.extend hU W a = S.extAt W a t :=
  S.extAt_eq W (S.bound_pos hU a) ht (S.bounded_bound hU a) ha

theorem extend_add (hU : S.IsOrderUnit) (W : EffectValuation S) (a b : V) :
    S.extend hU W (a + b) = S.extend hU W a + S.extend hU W b := by
  have ha := S.bounded_bound hU a
  have hb := S.bounded_bound hU b
  have hpa := S.bound_pos hU a
  have hpb := S.bound_pos hU b
  rw [S.extend_eq_extAt hU W (by linarith) (S.bounded_add ha hb)]
  exact S.extAt_add W hpa hpb ha hb

theorem extend_effect (hU : S.IsOrderUnit) (W : EffectValuation S) {a : V} (ha : S.Effect a) :
    S.extend hU W a = W.v a := by
  rw [S.extend_eq_extAt hU W one_pos (S.bounded_of_effect ha)]
  have e : S.midpoint a 1 = (1 / 2 : ℚ) • a + (1 / 2 : ℚ) • S.u := by
    unfold midpoint
    match_scalars <;> norm_num
  have h1 := effect_smul S (1 / 2 : ℚ) (by norm_num) (by norm_num) ha
  have h2 := effect_smul S (1 / 2 : ℚ) (by norm_num) (by norm_num) S.effect_u
  have hsum : S.Effect ((1 / 2 : ℚ) • a + (1 / 2 : ℚ) • S.u) := by
    rw [← e]
    exact S.midpoint_effect one_pos (S.bounded_of_effect ha)
  unfold extAt
  rw [e, W.additive _ _ h1 h2 hsum, val_rat_smul S W _ (by norm_num) (by norm_num) ha,
    val_rat_smul S W _ (by norm_num) (by norm_num) S.effect_u, W.unit]
  ring

theorem extend_nonneg (hU : S.IsOrderUnit) (W : EffectValuation S) {a : V} (ha : S.le 0 a) :
    0 ≤ S.extend hU W a := by
  have ht : 0 < S.bound hU a := S.bound_pos hU a
  have ht0 : S.bound hU a ≠ 0 := ht.ne'
  have hb : S.Bounded a (S.bound hU a) := S.bounded_bound hU a
  have hc0 : (0 : ℚ) ≤ 1 / (2 * S.bound hU a) := by positivity
  have h1 : S.Effect ((1 / (2 * S.bound hU a)) • a) := by
    constructor
    · exact S.smul_nonneg _ _ hc0 ha
    · apply S.le_of_sub_nonneg
      have e : S.u - (1 / (2 * S.bound hU a)) • a =
          (1 / (2 * S.bound hU a)) • ((S.bound hU a • S.u - a) + S.bound hU a • S.u) := by
        match_scalars <;> field_simp <;> ring
      rw [e]
      exact S.smul_nonneg _ _ hc0 (S.add_nonneg (S.sub_nonneg_of_le hb.2)
        (S.smul_nonneg _ _ ht.le S.u_nonneg))
  have h2 := effect_smul S (1 / 2 : ℚ) (by norm_num) (by norm_num) S.effect_u
  have e : S.midpoint a (S.bound hU a) =
      (1 / (2 * S.bound hU a)) • a + (1 / 2 : ℚ) • S.u := by
    unfold midpoint
    match_scalars <;> field_simp <;> ring
  have hm := S.midpoint_effect ht hb
  rw [e] at hm
  have hadd := W.additive _ _ h1 h2 hm
  have hv1 := W.nonneg _ h1
  unfold extend extAt
  rw [e, hadd, val_rat_smul S W _ (by norm_num) (by norm_num) S.effect_u, W.unit]
  nlinarith [mul_nonneg ht.le hv1]

theorem extend_u (hU : S.IsOrderUnit) (W : EffectValuation S) : S.extend hU W S.u = 1 := by
  rw [S.extend_effect hU W S.effect_u, W.unit]

/-- The extension as an additive homomorphism. -/
noncomputable def extendHom (hU : S.IsOrderUnit) (W : EffectValuation S) : V →+ ℚ where
  toFun := S.extend hU W
  map_zero' := by
    have h := S.extend_add hU W 0 0
    rw [add_zero] at h
    linarith
  map_add' := S.extend_add hU W

/-- The extension as a ℚ-linear functional: additivity on a ℚ-module gives ℚ-linearity. -/
noncomputable def extendₗ (hU : S.IsOrderUnit) (W : EffectValuation S) : V →ₗ[ℚ] ℚ :=
  (S.extendHom hU W).toRatLinearMap

theorem extendₗ_apply (hU : S.IsOrderUnit) (W : EffectValuation S) (a : V) :
    S.extendₗ hU W a = S.extend hU W a := by
  unfold extendₗ
  rw [AddMonoidHom.coe_toRatLinearMap]
  rfl

theorem extendₗ_effect (hU : S.IsOrderUnit) (W : EffectValuation S) {a : V}
    (ha : S.Effect a) : S.extendₗ hU W a = W.v a := by
  rw [S.extendₗ_apply, S.extend_effect hU W ha]

theorem extendₗ_nonneg (hU : S.IsOrderUnit) (W : EffectValuation S) {a : V}
    (ha : S.le 0 a) : 0 ≤ S.extendₗ hU W a := by
  rw [S.extendₗ_apply]
  exact S.extend_nonneg hU W ha

theorem extendₗ_u (hU : S.IsOrderUnit) (W : EffectValuation S) : S.extendₗ hU W S.u = 1 := by
  rw [S.extendₗ_apply, S.extend_u]

/-- Any ℚ-linear functional agreeing with `W` on effects is the extension. -/
theorem extend_unique (hU : S.IsOrderUnit) (W : EffectValuation S) (L : V →ₗ[ℚ] ℚ)
    (hL : ∀ a, S.Effect a → L a = W.v a) (a : V) : L a = S.extend hU W a := by
  have ht := S.bound_pos hU a
  have ht0 : S.bound hU a ≠ 0 := ht.ne'
  have hb := S.bounded_bound hU a
  have e : a = (2 * S.bound hU a) • S.midpoint a (S.bound hU a) - S.bound hU a • S.u := by
    unfold midpoint
    match_scalars <;> field_simp <;> ring
  have hm := S.midpoint_effect ht hb
  calc L a = L ((2 * S.bound hU a) • S.midpoint a (S.bound hU a) - S.bound hU a • S.u) := by
        rw [← e]
    _ = (2 * S.bound hU a) * L (S.midpoint a (S.bound hU a)) - S.bound hU a * L S.u := by
        rw [map_sub, map_smul, map_smul, smul_eq_mul, smul_eq_mul]
    _ = (2 * S.bound hU a) * W.v (S.midpoint a (S.bound hU a)) - S.bound hU a * 1 := by
        rw [hL _ hm, hL _ S.effect_u, W.unit]
    _ = S.extend hU W a := by
        unfold extend extAt
        ring

/-- Existence and uniqueness of the ℚ-linear functional agreeing with `W` on effects. -/
theorem linear_extension (hU : S.IsOrderUnit) (W : EffectValuation S) :
    ∃! L : V →ₗ[ℚ] ℚ, ∀ a, S.Effect a → L a = W.v a := by
  refine ⟨S.extendₗ hU W, fun a ha => S.extendₗ_effect hU W ha, fun L hL => ?_⟩
  ext a
  rw [S.extend_unique hU W L hL a, S.extendₗ_apply]

end OrderedQUnit

end BornFable

#print axioms BornFable.OrderedQUnit.bounded_mono
#print axioms BornFable.OrderedQUnit.bounded_add
#print axioms BornFable.OrderedQUnit.bounded_of_effect
#print axioms BornFable.OrderedQUnit.midpoint_effect
#print axioms BornFable.OrderedQUnit.extAt_add
#print axioms BornFable.OrderedQUnit.extAt_mono
#print axioms BornFable.OrderedQUnit.extAt_eq
#print axioms BornFable.OrderedQUnit.bound_pos
#print axioms BornFable.OrderedQUnit.bounded_bound
#print axioms BornFable.OrderedQUnit.extend_eq_extAt
#print axioms BornFable.OrderedQUnit.extend_add
#print axioms BornFable.OrderedQUnit.extend_effect
#print axioms BornFable.OrderedQUnit.extend_nonneg
#print axioms BornFable.OrderedQUnit.extend_u
#print axioms BornFable.OrderedQUnit.extendₗ_apply
#print axioms BornFable.OrderedQUnit.extendₗ_effect
#print axioms BornFable.OrderedQUnit.extendₗ_nonneg
#print axioms BornFable.OrderedQUnit.extendₗ_u
#print axioms BornFable.OrderedQUnit.extend_unique
#print axioms BornFable.OrderedQUnit.linear_extension
