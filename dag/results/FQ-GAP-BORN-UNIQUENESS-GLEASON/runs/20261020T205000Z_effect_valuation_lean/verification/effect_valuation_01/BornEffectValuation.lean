import Mathlib.Algebra.Module.Defs
import Mathlib.Algebra.Order.Field.Rat
import Mathlib.Algebra.Order.Ring.Rat
import Mathlib.Data.Rat.Defs
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Abel
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.LinearCombination
import Mathlib.Tactic.NormNum

/-
Effect-additive valuations over an ordered rational module.  AuthorityEffect: None.

Import note.  The frozen `contract.lean` begins with `import Mathlib`; this file imports only the
modules it uses (ordered rational field, modules, and the tactics named below).  The structures
and theorem statements are unchanged by this choice.

The structures `OrderedQUnit` and `EffectValuation` are copied verbatim from the frozen
interface `runs/20261020T004525Z_fable51_born/contract.lean` (Busch-type effect-additive inputs;
not a Gleason proof).  The eight theorems `val_zero` … `val_sandwich` are the frozen targets of
`target_types.txt` from that run, with the same names and binder order.

Scope fence.  Nothing here assumes continuity, monotonicity, real scalars, an order unit, or a
matrix representation.  Only the four order axioms, additivity on effects whose sum is again an
effect, positivity on effects, and normalisation of the unit are used.  The results are exact
over ℚ.  They do not by themselves give a trace representation or any Born/Gleason uniqueness.
-/

namespace BornFable

structure OrderedQUnit (V : Type*) [AddCommGroup V] [Module ℚ V] where
  le : V → V → Prop
  le_refl : ∀ x, le x x
  le_trans : ∀ x y z, le x y → le y z → le x z
  add_le_add_right : ∀ x y z, le x y → le (x + z) (y + z)
  smul_nonneg : ∀ (q : ℚ) (x : V), 0 ≤ q → le 0 x → le 0 (q • x)
  u : V
  u_nonneg : le 0 u

variable {V : Type*} [AddCommGroup V] [Module ℚ V]

def OrderedQUnit.Effect (S : OrderedQUnit V) (a : V) : Prop := S.le 0 a ∧ S.le a S.u

structure EffectValuation (S : OrderedQUnit V) where
  v : V → ℚ
  unit : v S.u = 1
  nonneg : ∀ a, S.Effect a → 0 ≤ v a
  additive : ∀ a b, S.Effect a → S.Effect b → S.Effect (a + b) → v (a + b) = v a + v b

/-! ### Order helpers derived from the four axioms -/

namespace OrderedQUnit

variable (S : OrderedQUnit V)

theorem le_iff_sub_nonneg {a b : V} : S.le a b ↔ S.le 0 (b - a) := by
  constructor
  · intro h
    have := S.add_le_add_right a b (-a) h
    simpa [sub_eq_add_neg] using this
  · intro h
    have := S.add_le_add_right 0 (b - a) a h
    simpa using this

theorem sub_nonneg_of_le {a b : V} (h : S.le a b) : S.le 0 (b - a) :=
  (S.le_iff_sub_nonneg).mp h

theorem le_of_sub_nonneg {a b : V} (h : S.le 0 (b - a)) : S.le a b :=
  (S.le_iff_sub_nonneg).mpr h

theorem add_nonneg {a b : V} (ha : S.le 0 a) (hb : S.le 0 b) : S.le 0 (a + b) := by
  have h1 : S.le b (a + b) := by
    have := S.add_le_add_right 0 a b ha
    simpa using this
  exact S.le_trans _ _ _ hb h1

theorem smul_le_smul {a b : V} {q : ℚ} (hq : 0 ≤ q) (h : S.le a b) :
    S.le (q • a) (q • b) := by
  apply S.le_of_sub_nonneg
  rw [← smul_sub]
  exact S.smul_nonneg q (b - a) hq (S.sub_nonneg_of_le h)

theorem neg_le_neg {a b : V} (h : S.le a b) : S.le (-b) (-a) := by
  apply S.le_of_sub_nonneg
  have e : -a - -b = b - a := by abel
  rw [e]
  exact S.sub_nonneg_of_le h

theorem effect_zero : S.Effect 0 := ⟨S.le_refl 0, S.u_nonneg⟩

theorem effect_u : S.Effect S.u := ⟨S.u_nonneg, S.le_refl S.u⟩

end OrderedQUnit

/-! ### The eight frozen targets -/

theorem val_zero (S : OrderedQUnit V) (W : EffectValuation S) : W.v 0 = 0 := by
  have h := W.additive 0 0 S.effect_zero S.effect_zero (by simpa using S.effect_zero)
  simp at h
  linarith

theorem effect_sub (S : OrderedQUnit V) {a b : V} (ha : S.Effect a) (hb : S.Effect b)
    (hab : S.le a b) : S.Effect (b - a) := by
  refine ⟨S.sub_nonneg_of_le hab, ?_⟩
  have h1 : S.le (b - a) b := by
    have := S.add_le_add_right 0 a (b - a) ha.1
    have e : a + (b - a) = b := by abel
    rw [zero_add, e] at this
    exact this
  exact S.le_trans _ _ _ h1 hb.2

theorem val_mono (S : OrderedQUnit V) (W : EffectValuation S) {a b : V} (ha : S.Effect a)
    (hb : S.Effect b) (hab : S.le a b) : W.v a ≤ W.v b := by
  have hd := effect_sub S ha hb hab
  have e : a + (b - a) = b := by abel
  have h := W.additive a (b - a) ha hd (by rw [e]; exact hb)
  rw [e] at h
  have := W.nonneg _ hd
  linarith

theorem val_le_one (S : OrderedQUnit V) (W : EffectValuation S) {a : V} (ha : S.Effect a) :
    W.v a ≤ 1 := by
  have := val_mono S W ha S.effect_u ha.2
  rwa [W.unit] at this

theorem effect_smul (S : OrderedQUnit V) {a : V} (q : ℚ) (hq0 : 0 ≤ q) (hq1 : q ≤ 1)
    (ha : S.Effect a) : S.Effect (q • a) := by
  refine ⟨S.smul_nonneg q a hq0 ha.1, ?_⟩
  apply S.le_of_sub_nonneg
  have e : S.u - q • a = (S.u - a) + (1 - q) • a := by
    rw [sub_smul, one_smul]
    abel
  rw [e]
  exact S.add_nonneg (S.sub_nonneg_of_le ha.2)
    (S.smul_nonneg (1 - q) a (by linarith) ha.1)

theorem val_nsmul (S : OrderedQUnit V) (W : EffectValuation S) {a : V} (k : ℕ)
    (ha : S.Effect a) (hka : S.Effect ((k : ℚ) • a)) :
    W.v ((k : ℚ) • a) = (k : ℚ) * W.v a := by
  have key : ∀ j : ℕ, j ≤ k → W.v ((j : ℚ) • a) = (j : ℚ) * W.v a := by
    intro j
    induction j with
    | zero =>
      intro _
      simp [val_zero S W]
    | succ j ih =>
      intro hjk
      have hkpos : (0 : ℚ) < k := by
        exact_mod_cast (Nat.lt_of_lt_of_le (Nat.succ_pos j) hjk)
      have hk0 : (k : ℚ) ≠ 0 := hkpos.ne'
      have scaled : ∀ m : ℕ, m ≤ k → S.Effect ((m : ℚ) • a) := by
        intro m hm
        have h0 : (0 : ℚ) ≤ (m : ℚ) / k := div_nonneg (by positivity) hkpos.le
        have h1 : (m : ℚ) / k ≤ 1 := by
          rw [div_le_one hkpos]
          exact_mod_cast hm
        have hmk : ((m : ℚ) / k) * k = m := by field_simp
        have := effect_smul S ((m : ℚ) / k) h0 h1 hka
        rwa [smul_smul, hmk] at this
      have hj : S.Effect ((j : ℚ) • a) := scaled j (Nat.le_of_succ_le hjk)
      have hj1 : S.Effect (((j + 1 : ℕ) : ℚ) • a) := scaled (j + 1) hjk
      have hsum : (j : ℚ) • a + a = ((j + 1 : ℕ) : ℚ) • a := by
        push_cast
        rw [add_smul, one_smul]
      have hadd := W.additive ((j : ℚ) • a) a hj ha (by rw [hsum]; exact hj1)
      rw [hsum] at hadd
      rw [hadd, ih (Nat.le_of_succ_le hjk)]
      push_cast
      ring
  exact key k le_rfl

theorem val_rat_smul (S : OrderedQUnit V) (W : EffectValuation S) {a : V} (q : ℚ)
    (hq0 : 0 ≤ q) (hq1 : q ≤ 1) (ha : S.Effect a) : W.v (q • a) = q * W.v a := by
  have hnpos : (0 : ℚ) < q.den := by exact_mod_cast q.den_pos
  have hn0 : (q.den : ℚ) ≠ 0 := hnpos.ne'
  have hnum : (q.num : ℚ) = q * q.den := (div_eq_iff hn0).mp (Rat.num_div_den q)
  have hnum0 : 0 ≤ q.num := Rat.num_nonneg.mpr hq0
  obtain ⟨m, hm⟩ : ∃ m : ℕ, (m : ℚ) = q * q.den :=
    ⟨q.num.toNat, by rw [← Int.cast_natCast q.num.toNat, Int.toNat_of_nonneg hnum0, hnum]⟩
  have hmn : (m : ℚ) ≤ q.den := by
    rw [hm]
    calc q * q.den ≤ 1 * q.den := mul_le_mul_of_nonneg_right hq1 hnpos.le
      _ = q.den := one_mul _
  obtain ⟨b, hb⟩ : ∃ b : V, b = (1 / (q.den : ℚ)) • a := ⟨_, rfl⟩
  have h1n : (1 : ℚ) ≤ q.den := Nat.one_le_cast.mpr q.den_pos
  have hb_eff : S.Effect b := by
    rw [hb]
    exact effect_smul S _ (by positivity) ((div_le_one hnpos).mpr h1n) ha
  have hnb : (q.den : ℚ) • b = a := by
    rw [hb, smul_smul, mul_one_div_cancel hn0, one_smul]
  have hmb : (m : ℚ) • b = q • a := by
    rw [hb, smul_smul]
    congr 1
    rw [hm]
    field_simp
  have hva := val_nsmul S W q.den hb_eff (by rw [hnb]; exact ha)
  rw [hnb] at hva
  have hvm := val_nsmul S W m hb_eff (by rw [hmb]; exact effect_smul S q hq0 hq1 ha)
  rw [hmb] at hvm
  rw [hvm, hva, hm]
  ring

/-- One-sided quantitative comparison: an upper bound on `a - b` by `ε • u` bounds `v a - v b`.
Only positivity of `ε` is used; `ε ≤ 1` is not needed. -/
theorem val_sub_le_of_le (S : OrderedQUnit V) (W : EffectValuation S) {a b : V}
    (ha : S.Effect a) (hb : S.Effect b) {ε : ℚ} (hε0 : 0 ≤ ε)
    (hhi : S.le (a - b) (ε • S.u)) : W.v a - W.v b ≤ ε := by
  have hpos : (0 : ℚ) < 1 + ε := by linarith
  have hne : (1 : ℚ) + ε ≠ 0 := hpos.ne'
  set c : ℚ := 1 / (1 + ε) with hc
  have hc0 : 0 ≤ c := by rw [hc]; positivity
  have hcpos : 0 < c := by rw [hc]; positivity
  have hc1 : c ≤ 1 := by
    rw [hc, div_le_one hpos]
    linarith
  have hεc0 : 0 ≤ ε * c := mul_nonneg hε0 hc0
  have hεc1 : ε * c ≤ 1 := by
    rw [hc, mul_one_div, div_le_one hpos]
    linarith
  have hc' : c * (1 + ε) = 1 := by
    rw [hc]
    exact one_div_mul_cancel hne
  have hcε : (1 : ℚ) - ε * c = c := by linear_combination -hc'
  have hcb : S.Effect (c • b) := effect_smul S c hc0 hc1 hb
  have hcu : S.Effect ((ε * c) • S.u) := effect_smul S (ε * c) hεc0 hεc1 S.effect_u
  have hca : S.Effect (c • a) := effect_smul S c hc0 hc1 ha
  have hle : S.le (c • a) (c • b + (ε * c) • S.u) := by
    have h1 : S.le a (b + ε • S.u) := by
      apply S.le_of_sub_nonneg
      have := S.sub_nonneg_of_le hhi
      have e : b + ε • S.u - a = ε • S.u - (a - b) := by abel
      rw [e]
      exact this
    have h2 := S.smul_le_smul hc0 h1
    have e : c • (b + ε • S.u) = c • b + (ε * c) • S.u := by
      rw [smul_add, smul_smul, mul_comm]
    rw [e] at h2
    exact h2
  have he : S.Effect (c • b + (ε * c) • S.u) := by
    refine ⟨S.add_nonneg hcb.1 hcu.1, ?_⟩
    apply S.le_of_sub_nonneg
    have e : S.u - (c • b + (ε * c) • S.u) = c • (S.u - b) := by
      rw [smul_sub]
      calc S.u - (c • b + (ε * c) • S.u) = (1 - ε * c) • S.u - c • b := by
            rw [sub_smul, one_smul]
            abel
        _ = c • S.u - c • b := by rw [hcε]
    rw [e]
    exact S.smul_nonneg c _ hc0 (S.sub_nonneg_of_le hb.2)
  have hmono := val_mono S W hca he hle
  have hadd := W.additive _ _ hcb hcu he
  rw [hadd, val_rat_smul S W c hc0 hc1 ha, val_rat_smul S W c hc0 hc1 hb,
    val_rat_smul S W (ε * c) hεc0 hεc1 S.effect_u, W.unit] at hmono
  have h' : c * W.v a ≤ c * (W.v b + ε) := by
    calc c * W.v a ≤ c * W.v b + ε * c * 1 := hmono
      _ = c * (W.v b + ε) := by ring
  have := le_of_mul_le_mul_left h' hcpos
  linarith

set_option linter.unusedVariables false in
theorem val_sandwich (S : OrderedQUnit V) (W : EffectValuation S) {a b : V} (ha : S.Effect a)
    (hb : S.Effect b) (ε : ℚ) (hε0 : 0 ≤ ε) (hε1 : ε ≤ 1) (hlo : S.le (-(ε • S.u)) (a - b))
    (hhi : S.le (a - b) (ε • S.u)) : -ε ≤ W.v a - W.v b ∧ W.v a - W.v b ≤ ε := by
  refine ⟨?_, val_sub_le_of_le S W ha hb hε0 hhi⟩
  have hlo' : S.le (b - a) (ε • S.u) := by
    have := S.neg_le_neg hlo
    have e1 : -(a - b) = b - a := by abel
    rw [e1, neg_neg] at this
    exact this
  have := val_sub_le_of_le S W hb ha hε0 hlo'
  linarith

end BornFable

#print axioms BornFable.OrderedQUnit.le_iff_sub_nonneg
#print axioms BornFable.OrderedQUnit.add_nonneg
#print axioms BornFable.OrderedQUnit.smul_le_smul
#print axioms BornFable.OrderedQUnit.neg_le_neg
#print axioms BornFable.val_zero
#print axioms BornFable.effect_sub
#print axioms BornFable.val_mono
#print axioms BornFable.val_le_one
#print axioms BornFable.effect_smul
#print axioms BornFable.val_nsmul
#print axioms BornFable.val_rat_smul
#print axioms BornFable.val_sub_le_of_le
#print axioms BornFable.val_sandwich
