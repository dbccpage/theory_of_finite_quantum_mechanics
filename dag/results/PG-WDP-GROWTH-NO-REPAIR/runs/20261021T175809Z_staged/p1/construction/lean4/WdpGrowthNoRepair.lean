import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Data.Fin.VecNotation
import Mathlib.Tactic.Linarith
import Mathlib.Algebra.Order.Ring.Abs
import Mathlib.Tactic.Ring

/-!
# Growth does not repair a quotient residual

AuthorityEffect: None.  Scope: the weighted-L1 quotient defect `Phi1(h) = min_x Σ_e w_e |h_e - (D x)_e|`
of a degree-1 window with 2-cells given by rows `D1`.  The source Lean theorems
(`wdp_growth_subcomplex_monotone`, `wdp_two_simplex_attachment_preserves_phi1` in
`DerivationDagQMClosure.lean`) are about a `List Nat` of edge residuals: the first says a sum of naturals only
grows when more naturals are appended (it is not about the minimum over potentials), the second is `rfl`
because the record update does not touch the residual list.  Neither mentions `Phi1` as a quotient defect.

Proved here (general over finite index types, unless marked INSTANCE):
* `phi_restrict_le`: if the sub-window's `d0` is the restriction of the big one (`hcompat`), its cochain and
  weights are the restrictions (weights `≤`), then `Phi1(sub) ≤ Phi1(big)`.  Growth with an extending cochain
  therefore never lowers `Phi1` (`phi_growth_not_lower`).
* `phi_le_unrepaired`: the source's list sum is only the unrepaired upper bound `cost 0 ≥ Phi1`.
* `phi_attach_iff` (definitional), `gamma2_attach` (the representative norm `‖d1 h‖₁` gains `|row · h|`),
  `gamma2_attach_ge`, `closed_attach`, `triangle_row_closed`, `gamma2_repair` (under `d1 d0 = 0` the norm is the
  same at every repair, hence at a minimal residual, which is where the source takes `Gamma2`): attaching 2-cells
  leaves `Phi1` alone and can only raise `Gamma2`.  Every inequality assumes the minima exist (`IsPhi`).
* Boundaries (INSTANCES): `incompatible_d0_instance` (`hcompat` dropped), `rescaled_weights_instance`
  (weights `≤` dropped), `nonmonotone_norm_instance` (norm arithmetic only: `J(1,-1) < J(1,0)`; for `d0 = 0` the defect of `h` is `J h`, so deleting a coordinate
raises it, a consequence that is NOT stated as a theorem about `IsPhi`).
It does NOT prove: monotonicity for arbitrary norms (false, see the last instance), existence of minimisers
(part of `IsPhi`), or anything about equal-weight subdivision, filtration limit pages or complex coefficients.
-/

set_option linter.unusedSectionVars false

namespace WdpGrowthNoRepair

open Finset

section General

variable {E V E' V' : Type*} [Fintype E] [Fintype V] [Fintype E'] [Fintype V']

/-- Weighted L1 repair cost of the potential `x`. -/
def cost (D : E → V → ℚ) (w h : E → ℚ) (x : V → ℚ) : ℚ := ∑ e, w e * |h e - ∑ v, D e v * x v|

/-- `p` is the attained minimum of the repair cost: the quotient defect. -/
def IsPhi (D : E → V → ℚ) (w h : E → ℚ) (p : ℚ) : Prop :=
  (∀ x, p ≤ cost D w h x) ∧ ∃ x, cost D w h x = p

/-- Restriction to a sub-window never raises the defect. -/
theorem phi_restrict_le (D : E → V → ℚ) (w h : E → ℚ) (D' : E' → V' → ℚ) (w' h' : E' → ℚ)
    (ε : E' → E) (hε : Function.Injective ε) (ι : V' → V)
    (hcompat : ∀ e' (x : V → ℚ), ∑ v', D' e' v' * x (ι v') = ∑ v, D (ε e') v * x v)
    (hh : ∀ e', h' e' = h (ε e')) (hw : ∀ e', w' e' ≤ w (ε e')) (hw0 : ∀ e, 0 ≤ w e)
    {p q : ℚ} (hp : IsPhi D w h p) (hq : IsPhi D' w' h' q) : q ≤ p := by
  classical
  obtain ⟨_, x, hx⟩ := hp
  obtain ⟨hql, _⟩ := hq
  have step1 : cost D' w' h' (fun v' => x (ι v')) ≤
      ∑ e', w (ε e') * |h (ε e') - ∑ v, D (ε e') v * x v| := by
    unfold cost
    refine Finset.sum_le_sum fun e' _ => ?_
    rw [hcompat e' x, hh e']
    exact mul_le_mul_of_nonneg_right (hw e') (abs_nonneg _)
  have step2 : ∑ e', w (ε e') * |h (ε e') - ∑ v, D (ε e') v * x v| ≤ cost D w h x := by
    unfold cost
    have himg : ∑ e ∈ (Finset.univ : Finset E').image ε, w e * |h e - ∑ v, D e v * x v| =
        ∑ e', w (ε e') * |h (ε e') - ∑ v, D (ε e') v * x v| :=
      Finset.sum_image fun a _ b _ hab => hε hab
    rw [← himg]
    exact Finset.sum_le_sum_of_subset_of_nonneg (Finset.subset_univ _)
      fun e _ _ => mul_nonneg (hw0 e) (abs_nonneg _)
  have := hql (fun v' => x (ι v'))
  linarith

/-- Growth with an extending cochain (same `d0` restriction, same values, weights not decreased)
cannot lower the defect: the sub-window's defect is a lower bound. -/
theorem phi_growth_not_lower (D : E → V → ℚ) (w h : E → ℚ) (D' : E' → V' → ℚ) (w' h' : E' → ℚ)
    (ε : E' → E) (hε : Function.Injective ε) (ι : V' → V)
    (hcompat : ∀ e' (x : V → ℚ), ∑ v', D' e' v' * x (ι v') = ∑ v, D (ε e') v * x v)
    (hh : ∀ e', h' e' = h (ε e')) (hw : ∀ e', w' e' ≤ w (ε e')) (hw0 : ∀ e, 0 ≤ w e)
    {p q : ℚ} (hp : IsPhi D w h p) (hq : IsPhi D' w' h' q) : ¬ p < q := by
  intro hlt
  have := phi_restrict_le D w h D' w' h' ε hε ι hcompat hh hw hw0 hp hq
  linarith

/-- The unrepaired residual sum (the source's list sum) is only an upper bound of the defect. -/
theorem phi_le_unrepaired (D : E → V → ℚ) (w h : E → ℚ) {p : ℚ} (hp : IsPhi D w h p) :
    p ≤ ∑ e, w e * |h e| := by
  obtain ⟨hl, _⟩ := hp
  have := hl (fun _ => 0)
  simpa [cost] using this

end General

section Attach

variable {E V R : Type*} [Fintype E] [Fintype V] [Fintype R]

/-- A degree-1 window with a weighted-L1 norm and 2-cell rows. -/
structure Win (E V R : Type*) where
  D0 : E → V → ℚ
  w : E → ℚ
  h : E → ℚ
  D1 : R → E → ℚ

/-- Closure charge `Gamma2 = ‖d1 h‖₁`. -/
def Win.gamma2 (W : Win E V R) : ℚ := ∑ r, |∑ e, W.D1 r e * W.h e|

/-- The complex condition `d1 d0 = 0`. -/
def Win.closed (W : Win E V R) : Prop := ∀ r v, ∑ e, W.D1 r e * W.D0 e v = 0

/-- Attach one 2-cell with boundary row `row`. -/
def Win.attach (W : Win E V R) (row : E → ℚ) : Win E V (R ⊕ Unit) :=
  ⟨W.D0, W.w, W.h, Sum.elim W.D1 (fun _ => row)⟩

/-- DEFINITIONAL: the defect only reads `(D0, w, h)`, so attaching 2-cells leaves it unchanged. -/
theorem phi_attach_iff (W : Win E V R) (row : E → ℚ) (p : ℚ) :
    IsPhi (W.attach row).D0 (W.attach row).w (W.attach row).h p ↔ IsPhi W.D0 W.w W.h p := Iff.rfl

theorem gamma2_attach (W : Win E V R) (row : E → ℚ) :
    (W.attach row).gamma2 = W.gamma2 + |∑ e, row e * W.h e| := by
  unfold Win.gamma2 Win.attach
  rw [Fintype.sum_sum_type]
  simp

/-- Attaching a 2-cell can only raise `Gamma2`. -/
theorem gamma2_attach_ge (W : Win E V R) (row : E → ℚ) : W.gamma2 ≤ (W.attach row).gamma2 := by
  rw [gamma2_attach]; exact le_add_of_nonneg_right (abs_nonneg _)

theorem closed_attach (W : Win E V R) (row : E → ℚ) (hW : W.closed)
    (hrow : ∀ v, ∑ e, row e * W.D0 e v = 0) : (W.attach row).closed := by
  intro r v
  cases r with
  | inl r => exact hW r v
  | inr u => exact hrow v

/-- With `d1 d0 = 0`, `Gamma2 = ‖d1 h‖₁` is the same at every repair `h - D0 x`, in particular at a
minimal residual (the source Gamma2 is taken there).  Without closure the two readings differ. -/
theorem gamma2_repair (W : Win E V R) (hW : W.closed) (x : V → ℚ) :
    ∑ r, |∑ e, W.D1 r e * (W.h e - ∑ v, W.D0 e v * x v)| = W.gamma2 := by
  unfold Win.gamma2
  refine Finset.sum_congr rfl fun r _ => ?_
  congr 1
  have key : ∑ e, W.D1 r e * (∑ v, W.D0 e v * x v) = 0 := by
    calc ∑ e, W.D1 r e * (∑ v, W.D0 e v * x v) = ∑ e, ∑ v, W.D1 r e * W.D0 e v * x v := by
          simp only [Finset.mul_sum, mul_assoc]
      _ = ∑ v, ∑ e, W.D1 r e * W.D0 e v * x v := Finset.sum_comm
      _ = ∑ v, (∑ e, W.D1 r e * W.D0 e v) * x v := by simp only [Finset.sum_mul]
      _ = 0 := by simp [hW r]
  have : ∑ e, W.D1 r e * (W.h e - ∑ v, W.D0 e v * x v) =
      ∑ e, W.D1 r e * W.h e - ∑ e, W.D1 r e * (∑ v, W.D0 e v * x v) := by
    rw [← Finset.sum_sub_distrib]
    exact Finset.sum_congr rfl fun e _ => by ring
  rw [this, key, sub_zero]

/-- Graph window: edge `e` runs from `s e` to `t e`; `d0 f = f (t e) - f (s e)`. -/
def graphD0 {E V : Type*} [DecidableEq V] (s t : E → V) (e : E) (v : V) : ℚ :=
  (if v = t e then 1 else 0) - (if v = s e then 1 else 0)

/-- The boundary row `ab + bc - ac` of a triangle is a cocycle for any graph window: a triangle can always
be attached without breaking `d1 d0 = 0`. -/
theorem triangle_row_closed {E V : Type*} [Fintype E] [DecidableEq E] [DecidableEq V] (s t : E → V)
    (ab bc ac : E) (a b c : V) (h1 : s ab = a ∧ t ab = b) (h2 : s bc = b ∧ t bc = c)
    (h3 : s ac = a ∧ t ac = c) (v : V) :
    ∑ e, ((if e = ab then (1 : ℚ) else 0) + (if e = bc then 1 else 0) - (if e = ac then 1 else 0)) *
      graphD0 s t e v = 0 := by
  simp only [add_mul, sub_mul, ite_mul, one_mul, zero_mul, Finset.sum_add_distrib, Finset.sum_sub_distrib,
    Finset.sum_ite_eq', Finset.mem_univ, ite_true]
  unfold graphD0
  rw [h1.1, h1.2, h2.1, h2.2, h3.1, h3.2]
  ring

end Attach

section Boundaries

/-- INSTANCE (hypothesis `hcompat` dropped): one edge, `d0 = (1)` in the big window but `(0)` in the "sub"
window with the same cochain and weight: the defect goes up from `0` to `1`. -/
theorem incompatible_d0_instance :
    ∃ p q : ℚ, IsPhi (fun _ _ : Fin 1 => (1 : ℚ)) (fun _ => 1) (fun _ => 1) p ∧
      IsPhi (fun _ _ : Fin 1 => (0 : ℚ)) (fun _ => 1) (fun _ => 1) q ∧ p < q := by
  refine ⟨0, 1, ⟨?_, 1, ?_⟩, ⟨?_, 0, ?_⟩, by norm_num⟩
  · intro x; simp [cost]
  · simp [cost]
  · intro x; norm_num [cost]
  · simp [cost]

/-- Parallel-edge model: two vertices, three edges `0 → 1`, cochain `(1, -1, 0)`. -/
def parD : Fin 3 → Fin 2 → ℚ := fun _ v => if v = 1 then 1 else -1
def parH : Fin 3 → ℚ := ![1, -1, 0]

/-- INSTANCE (weights `≤` dropped): full window weights `2` has `Phi1 = 4`; the sub-window on the first two
edges with weights rescaled to `3` has `Phi1 = 6 > 4`. -/
theorem rescaled_weights_instance :
    IsPhi parD (fun _ => 2) parH 4 ∧ IsPhi (fun (e : Fin 2) v => parD e.castSucc v) (fun _ => 3)
      (fun e => parH e.castSucc) 6 := by
  have hs : ∀ (e : Fin 3) (x : Fin 2 → ℚ), ∑ v, parD e v * x v = x 1 - x 0 := by
    intro e x
    simp [parD, Fin.sum_univ_two]
    ring
  have hfull : ∀ x : Fin 2 → ℚ, cost parD (fun _ => 2) parH x =
      2 * |1 - (x 1 - x 0)| + 2 * |-1 - (x 1 - x 0)| + 2 * |0 - (x 1 - x 0)| := by
    intro x
    simp [cost, hs, Fin.sum_univ_three, parH]
  have hsub : ∀ x : Fin 2 → ℚ, cost (fun (e : Fin 2) v => parD e.castSucc v) (fun _ => 3)
      (fun e => parH e.castSucc) x = 3 * |1 - (x 1 - x 0)| + 3 * |-1 - (x 1 - x 0)| := by
    intro x
    simp [cost, hs, Fin.sum_univ_two, parH]
  refine ⟨⟨?_, fun _ => 0, ?_⟩, ⟨?_, fun _ => 0, ?_⟩⟩
  · intro x
    rw [hfull]
    have a1 := le_abs_self (1 - (x 1 - x 0))
    have a2 := neg_le_abs (-1 - (x 1 - x 0))
    have a3 := abs_nonneg (0 - (x 1 - x 0))
    linarith
  · rw [hfull]; norm_num
  · intro x
    rw [hsub]
    have a1 := le_abs_self (1 - (x 1 - x 0))
    have a2 := neg_le_abs (-1 - (x 1 - x 0))
    linarith
  · rw [hsub]; norm_num

/-- A norm on `ℚ × ℚ`: `J(a,b) = |a+b| + |a-b|/4`. -/
def Jn (u : ℚ × ℚ) : ℚ := |u.1 + u.2| + |u.1 - u.2| / 4

/-- INSTANCE (norm not monotone under coordinate deletion): with `d0 = 0` the defect of `h = (1,-1)` is
`J h = 1/2`, but its restriction to the first coordinate has `J(1,0) = 5/4 > 1/2`. -/
theorem nonmonotone_norm_instance :
    Jn (1, -1) = 1 / 2 ∧ Jn (1, 0) = 5 / 4 ∧ (∀ u v : ℚ × ℚ, Jn (u + v) ≤ Jn u + Jn v) ∧
      (∀ (c : ℚ) (u : ℚ × ℚ), Jn (c • u) = |c| * Jn u) ∧ (∀ u, Jn u = 0 → u = (0, 0)) := by
  refine ⟨by norm_num [Jn], by norm_num [Jn], ?_, ?_, ?_⟩
  · intro u v
    simp only [Jn, Prod.fst_add, Prod.snd_add]
    have h1 := abs_add_le (u.1 + u.2) (v.1 + v.2)
    have h2 := abs_add_le (u.1 - u.2) (v.1 - v.2)
    have e1 : u.1 + v.1 + (u.2 + v.2) = u.1 + u.2 + (v.1 + v.2) := by ring
    have e2 : u.1 + v.1 - (u.2 + v.2) = u.1 - u.2 + (v.1 - v.2) := by ring
    rw [e1, e2]
    linarith
  · intro c u
    simp only [Jn, Prod.smul_fst, Prod.smul_snd, smul_eq_mul]
    have e1 : c * u.1 + c * u.2 = c * (u.1 + u.2) := by ring
    have e2 : c * u.1 - c * u.2 = c * (u.1 - u.2) := by ring
    rw [e1, e2, abs_mul, abs_mul]
    ring
  · intro u hu
    simp only [Jn] at hu
    have h1 := abs_nonneg (u.1 + u.2)
    have h2 := abs_nonneg (u.1 - u.2)
    have h1' : |u.1 + u.2| = 0 := by linarith
    have h2' : |u.1 - u.2| = 0 := by linarith
    rw [abs_eq_zero] at h1' h2'
    ext <;> simp <;> linarith

end Boundaries

end WdpGrowthNoRepair

#print axioms WdpGrowthNoRepair.phi_restrict_le
#print axioms WdpGrowthNoRepair.phi_growth_not_lower
#print axioms WdpGrowthNoRepair.phi_le_unrepaired
#print axioms WdpGrowthNoRepair.phi_attach_iff
#print axioms WdpGrowthNoRepair.gamma2_attach
#print axioms WdpGrowthNoRepair.gamma2_attach_ge
#print axioms WdpGrowthNoRepair.closed_attach
#print axioms WdpGrowthNoRepair.gamma2_repair
#print axioms WdpGrowthNoRepair.triangle_row_closed
#print axioms WdpGrowthNoRepair.incompatible_d0_instance
#print axioms WdpGrowthNoRepair.rescaled_weights_instance
#print axioms WdpGrowthNoRepair.nonmonotone_norm_instance
