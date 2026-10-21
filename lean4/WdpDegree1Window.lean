import Mathlib.LinearAlgebra.Quotient.Basic
import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Data.Fin.VecNotation
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Abel

/-!
# The degree-1 window: kappa1 on Q1, H1, the quotient defect and the three diagnostic classes

AuthorityEffect: None.  Scope: finite data `(C0, C1, C2, d0, d1)`; modules over a field for the
algebra, `ℚ`-valued costs for the quotient defect.  The window is a DECLARED datum: nothing here
derives it from Genesis admission, and nothing here is a physical statement.

What is proved (all general, over arbitrary modules or finite index types, unless marked INSTANCE):
* `kappa_descends_iff`: `d1` descends to `Q1 = C1 / im d0` exactly when `d1 ∘ d0 = 0`; the hypothesis
  cannot be dropped (`kappa_not_defined_instance`, an INSTANCE with `d1 ∘ d0 ≠ 0`).
* `ker_kappa_eq_map`, `kappa_eq_zero_iff`: `H1 = ker kappa1` is the image of `ker d1` in `Q1`; a class is
  closed iff every (iff some) representative is closed.
* `isPhi_shift`, `isPhi_unique`, `isPhi_zero_iff`: the quotient defect `Phi_J` (attained minimum of `J` over
  the class) depends on the class only; it is `0` exactly for the zero class when `J` is definite.
* `diag_unique`, `ratio_class`: the case analysis ExactClass / ClosedResidual / ActiveClosureFailure (the
  Rust `ObstructionDiagnosticClass`, whose first variant is named `ExactRepair` there) and `R_cl = Gamma2/Phi1`.
* `weak_duality`: a bounded dual vector annihilating the coboundaries lower-bounds every weighted-L1 repair.
* `tri_phi`, `tri_gamma2`: the filled triangle (INSTANCE): `Phi1 = 2`, `Gamma2 = 2`.
It does NOT prove: any statement about a particular norm other than weighted L1, existence of minimisers in
general (attainment is part of the definition `IsPhi`; it is a theorem only for the finite polyhedral case,
which is checked natively), or anything about complex coefficients.
-/

namespace WdpDegree1Window

section Quotient

variable {K : Type*} [Field K] {C0 C1 C2 : Type*}
  [AddCommGroup C0] [Module K C0] [AddCommGroup C1] [Module K C1] [AddCommGroup C2] [Module K C2]

/-- The repair quotient `Q1 = C1 / im d0`. -/
abbrev Q1 (d0 : C0 →ₗ[K] C1) : Type _ := C1 ⧸ LinearMap.range d0

/-- `d1` descends to `Q1` exactly when `d1 ∘ d0 = 0`. -/
theorem kappa_descends_iff (d0 : C0 →ₗ[K] C1) (d1 : C1 →ₗ[K] C2) :
    (∃ κ : Q1 d0 →ₗ[K] C2, ∀ h, κ (Submodule.Quotient.mk h) = d1 h) ↔ d1 ∘ₗ d0 = 0 := by
  constructor
  · rintro ⟨κ, hκ⟩
    ext a
    have h0 : (Submodule.Quotient.mk (d0 a) : Q1 d0) = 0 :=
      (Submodule.Quotient.mk_eq_zero _).mpr ⟨a, rfl⟩
    simp only [LinearMap.comp_apply, LinearMap.zero_apply]
    rw [← hκ, h0, map_zero]
  · intro h
    exact ⟨(LinearMap.range d0).liftQ d1 (LinearMap.range_le_ker_iff.mpr h), fun x => rfl⟩

/-- The descended closure map `kappa1 : Q1 → C2`. -/
def kappa (d0 : C0 →ₗ[K] C1) (d1 : C1 →ₗ[K] C2) (h : d1 ∘ₗ d0 = 0) : Q1 d0 →ₗ[K] C2 :=
  (LinearMap.range d0).liftQ d1 (LinearMap.range_le_ker_iff.mpr h)

@[simp] theorem kappa_mk (d0 : C0 →ₗ[K] C1) (d1 : C1 →ₗ[K] C2) (h : d1 ∘ₗ d0 = 0) (x : C1) :
    kappa d0 d1 h (Submodule.Quotient.mk x) = d1 x := rfl

/-- A class is closed iff every representative is closed. -/
theorem kappa_eq_zero_iff (d0 : C0 →ₗ[K] C1) (d1 : C1 →ₗ[K] C2) (h : d1 ∘ₗ d0 = 0) (q : Q1 d0) :
    kappa d0 d1 h q = 0 ↔ ∀ x, (Submodule.Quotient.mk x : Q1 d0) = q → d1 x = 0 := by
  obtain ⟨x0, rfl⟩ := Submodule.Quotient.mk_surjective _ q
  constructor
  · intro hq x hx
    have : kappa d0 d1 h (Submodule.Quotient.mk x) = 0 := by rw [hx]; exact hq
    simpa using this
  · intro hall
    simpa using hall x0 rfl

/-- `H1 = ker kappa1` is the image of `ker d1` in `Q1`. -/
theorem ker_kappa_eq_map (d0 : C0 →ₗ[K] C1) (d1 : C1 →ₗ[K] C2) (h : d1 ∘ₗ d0 = 0) :
    LinearMap.ker (kappa d0 d1 h) = (LinearMap.ker d1).map (Submodule.mkQ (LinearMap.range d0)) := by
  ext q
  obtain ⟨x, rfl⟩ := Submodule.Quotient.mk_surjective _ q
  simp only [LinearMap.mem_ker, Submodule.mem_map, Submodule.mkQ_apply, kappa_mk]
  constructor
  · intro hx
    exact ⟨x, hx, rfl⟩
  · rintro ⟨y, hy, hmk⟩
    have hxy : (Submodule.Quotient.mk y : Q1 d0) = Submodule.Quotient.mk x := hmk
    have := congrArg (kappa d0 d1 h) hxy
    simpa [hy] using this.symm

/-- Boundary (INSTANCE): with `d0 = d1 = id` on `ℚ` (so `d1 ∘ d0 ≠ 0`) no `kappa1` exists on `Q1`. -/
theorem kappa_not_defined_instance :
    ¬ ∃ κ : Q1 (LinearMap.id : ℚ →ₗ[ℚ] ℚ) →ₗ[ℚ] ℚ, ∀ h, κ (Submodule.Quotient.mk h) =
      (LinearMap.id : ℚ →ₗ[ℚ] ℚ) h := by
  intro hex
  have := (kappa_descends_iff (LinearMap.id : ℚ →ₗ[ℚ] ℚ) (LinearMap.id : ℚ →ₗ[ℚ] ℚ)).mp hex
  have h1 := congrArg (fun f : ℚ →ₗ[ℚ] ℚ => f 1) this
  simp at h1

/-- The two representatives `0` and `d0 1 = 1` of the zero class have different `d1` values there. -/
theorem representatives_disagree_instance :
    (Submodule.Quotient.mk (0 : ℚ) : Q1 (LinearMap.id : ℚ →ₗ[ℚ] ℚ)) = Submodule.Quotient.mk 1 ∧
      (LinearMap.id : ℚ →ₗ[ℚ] ℚ) 0 ≠ (LinearMap.id : ℚ →ₗ[ℚ] ℚ) 1 := by
  refine ⟨?_, by simp⟩
  rw [Submodule.Quotient.eq]
  exact ⟨-1, by simp⟩

end Quotient

section Phi

variable {K : Type*} [Field K] {C0 C1 : Type*}
  [AddCommGroup C0] [Module K C0] [AddCommGroup C1] [Module K C1]

/-- `p` is the quotient defect of the class of `h`: the attained minimum of `J` over `h + im d0`. -/
def IsPhi (J : C1 → ℚ) (d0 : C0 →ₗ[K] C1) (h : C1) (p : ℚ) : Prop :=
  (∀ x, p ≤ J (h + d0 x)) ∧ ∃ x, J (h + d0 x) = p

/-- The defect depends on the class only (repair invariance). -/
theorem isPhi_shift (J : C1 → ℚ) (d0 : C0 →ₗ[K] C1) (h : C1) (y : C0) (p : ℚ) :
    IsPhi J d0 (h + d0 y) p ↔ IsPhi J d0 h p := by
  unfold IsPhi
  constructor
  · rintro ⟨hl, x, hx⟩
    refine ⟨fun z => ?_, x + y, ?_⟩
    · have := hl (z - y)
      have e : h + d0 y + d0 (z - y) = h + d0 z := by rw [map_sub]; abel
      rwa [e] at this
    · have e : h + d0 (x + y) = h + d0 y + d0 x := by rw [map_add]; abel
      rw [e]; exact hx
  · rintro ⟨hl, x, hx⟩
    refine ⟨fun z => ?_, x - y, ?_⟩
    · have := hl (z + y)
      have e : h + d0 (z + y) = h + d0 y + d0 z := by rw [map_add]; abel
      rwa [e] at this
    · have e : h + d0 y + d0 (x - y) = h + d0 x := by rw [map_sub]; abel
      rw [e]; exact hx

theorem isPhi_unique {J : C1 → ℚ} {d0 : C0 →ₗ[K] C1} {h : C1} {p q : ℚ}
    (hp : IsPhi J d0 h p) (hq : IsPhi J d0 h q) : p = q := by
  obtain ⟨hp1, x, hx⟩ := hp
  obtain ⟨hq1, z, hz⟩ := hq
  have := hp1 z
  have := hq1 x
  linarith

/-- With a definite nonnegative `J`, `Phi_J = 0` exactly for the zero class of `Q1`. -/
theorem isPhi_zero_iff (J : C1 → ℚ) (d0 : C0 →ₗ[K] C1) (h : C1)
    (hnn : ∀ v, 0 ≤ J v) (hdef : ∀ v, J v = 0 ↔ v = 0) :
    IsPhi J d0 h 0 ↔ (Submodule.Quotient.mk h : Q1 d0) = 0 := by
  rw [Submodule.Quotient.mk_eq_zero]
  constructor
  · rintro ⟨_, x, hx⟩
    have hz : h + d0 x = 0 := (hdef _).mp hx
    exact ⟨-x, by simp [eq_neg_of_add_eq_zero_right hz]⟩
  · rintro ⟨x, hx⟩
    refine ⟨fun z => hnn _, -x, ?_⟩
    rw [map_neg, hx]
    simp [(hdef 0).mpr rfl]

end Phi

section Diagnostic

/-- The three diagnostic classes (the Rust enum calls the first one `ExactRepair`). -/
inductive Diag | exact | closedResidual | active
  deriving DecidableEq

/-- Classification from `Phi1` and `Gamma2`: exact iff `Phi1 = 0`; else closed iff `Gamma2 = 0`. -/
def diag (phi gam : ℚ) : Diag :=
  if phi = 0 then .exact else if gam = 0 then .closedResidual else .active

/-- Every `(Phi1, Gamma2)` falls in exactly one class. -/
theorem diag_unique (phi gam : ℚ) :
    ∃! c : Diag, (c = .exact ∧ phi = 0) ∨ (c = .closedResidual ∧ phi ≠ 0 ∧ gam = 0) ∨
      (c = .active ∧ phi ≠ 0 ∧ gam ≠ 0) := by
  by_cases h1 : phi = 0
  · refine ⟨.exact, Or.inl ⟨rfl, h1⟩, ?_⟩
    rintro c (⟨rfl, _⟩ | ⟨_, h, _⟩ | ⟨_, h, _⟩) <;> first | rfl | exact absurd h1 h
  · by_cases h2 : gam = 0
    · refine ⟨.closedResidual, Or.inr (Or.inl ⟨rfl, h1, h2⟩), ?_⟩
      rintro c (⟨_, h⟩ | ⟨rfl, _, _⟩ | ⟨_, _, h⟩) <;> first | rfl | exact absurd h h1 | exact absurd h2 h
    · refine ⟨.active, Or.inr (Or.inr ⟨rfl, h1, h2⟩), ?_⟩
      rintro c (⟨_, h⟩ | ⟨_, _, h⟩ | ⟨rfl, _, _⟩) <;> first | rfl | exact absurd h h1 | exact absurd h h2

theorem diag_eq_exact_iff (phi gam : ℚ) : diag phi gam = .exact ↔ phi = 0 := by
  unfold diag; split_ifs <;> simp_all

theorem diag_eq_closed_iff (phi gam : ℚ) : diag phi gam = .closedResidual ↔ phi ≠ 0 ∧ gam = 0 := by
  unfold diag; split_ifs <;> simp_all

theorem diag_eq_active_iff (phi gam : ℚ) : diag phi gam = .active ↔ phi ≠ 0 ∧ gam ≠ 0 := by
  unfold diag; split_ifs <;> simp_all

/-- `R_cl = Gamma2 / Phi1`, defined only when `Phi1 > 0`. -/
def ratio (phi gam : ℚ) : Option ℚ := if 0 < phi then some (gam / phi) else none

/-- For `Phi1 ≥ 0` and `Gamma2 ≥ 0`: exact iff no ratio; closed iff ratio `0`; active iff ratio `> 0`. -/
theorem ratio_class (phi gam : ℚ) (hp : 0 ≤ phi) (hg : 0 ≤ gam) :
    (diag phi gam = .exact ↔ ratio phi gam = none) ∧
    (diag phi gam = .closedResidual ↔ ratio phi gam = some 0) ∧
    (diag phi gam = .active ↔ ∃ r, 0 < r ∧ ratio phi gam = some r) := by
  rw [diag_eq_exact_iff, diag_eq_closed_iff, diag_eq_active_iff]
  rcases hp.lt_or_eq with h | h
  · have hr : ratio phi gam = some (gam / phi) := by simp [ratio, h]
    rw [hr]
    refine ⟨⟨fun e => absurd e h.ne', by simp⟩, ?_, ?_⟩
    · constructor
      · rintro ⟨_, e⟩; simp [e]
      · intro e; simp only [Option.some.injEq, div_eq_zero_iff] at e
        exact ⟨h.ne', e.resolve_right h.ne'⟩
    · constructor
      · rintro ⟨_, e⟩
        exact ⟨gam / phi, div_pos (lt_of_le_of_ne hg (Ne.symm e)) h, rfl⟩
      · rintro ⟨r, hr0, e⟩
        simp only [Option.some.injEq] at e
        refine ⟨h.ne', fun g0 => ?_⟩
        rw [g0, zero_div] at e
        linarith
  · subst h
    simp [ratio]

end Diagnostic

section Dual

open Finset

variable {E V : Type*} [Fintype E] [Fintype V]

/-- Weighted L1 repair cost of the potential `x` for the defect `h`: `Σ_e w_e |h_e - (D x)_e|`. -/
def cost (D : E → V → ℚ) (w h : E → ℚ) (x : V → ℚ) : ℚ := ∑ e, w e * |h e - ∑ v, D e v * x v|

/-- Weak duality: a dual vector with `D^T y = 0` and `|y_e| ≤ w_e` lower-bounds every repair cost. -/
theorem weak_duality (D : E → V → ℚ) (w h y : E → ℚ) (hann : ∀ v, ∑ e, y e * D e v = 0)
    (hb : ∀ e, |y e| ≤ w e) (x : V → ℚ) : ∑ e, y e * h e ≤ cost D w h x := by
  have key : ∑ e, y e * (∑ v, D e v * x v) = 0 := by
    calc ∑ e, y e * (∑ v, D e v * x v) = ∑ e, ∑ v, y e * D e v * x v := by
          simp only [Finset.mul_sum, mul_assoc]
      _ = ∑ v, ∑ e, y e * D e v * x v := Finset.sum_comm
      _ = ∑ v, (∑ e, y e * D e v) * x v := by simp only [Finset.sum_mul]
      _ = 0 := by simp [hann]
  have split : ∑ e, y e * h e =
      ∑ e, y e * (h e - ∑ v, D e v * x v) + ∑ e, y e * (∑ v, D e v * x v) := by
    rw [← Finset.sum_add_distrib]
    exact Finset.sum_congr rfl fun e _ => by ring
  rw [split, key, add_zero]
  unfold cost
  refine Finset.sum_le_sum fun e _ => ?_
  calc y e * (h e - ∑ v, D e v * x v) ≤ |y e * (h e - ∑ v, D e v * x v)| := le_abs_self _
    _ = |y e| * |h e - ∑ v, D e v * x v| := abs_mul _ _
    _ ≤ w e * |h e - ∑ v, D e v * x v| := mul_le_mul_of_nonneg_right (hb e) (abs_nonneg _)

/-- A repair `x` and a dual vector with equal values certify the quotient defect. -/
theorem isPhi_of_certificate (D : E → V → ℚ) (w h y : E → ℚ) (hann : ∀ v, ∑ e, y e * D e v = 0)
    (hb : ∀ e, |y e| ≤ w e) (x : V → ℚ) (hx : cost D w h x = ∑ e, y e * h e) :
    (∀ z, ∑ e, y e * h e ≤ cost D w h z) ∧ ∃ z, cost D w h z = ∑ e, y e * h e :=
  ⟨weak_duality D w h y hann hb, x, hx⟩

end Dual

section Triangle

/-- Filled triangle, edges `(01, 12, 02)`: `d0 f = (f1 - f0, f2 - f1, f2 - f0)`. -/
def triD0 : Fin 3 → Fin 3 → ℚ := ![![-1, 1, 0], ![0, -1, 1], ![-1, 0, 1]]
/-- Its only 2-cell: `d1 x = x01 + x12 - x02`. -/
def triD1 : Fin 1 → Fin 3 → ℚ := ![![1, 1, -1]]
def triH : Fin 3 → ℚ := ![1, 1, 0]
def triY : Fin 3 → ℚ := ![1, 1, -1]
def triW : Fin 3 → ℚ := fun _ => 1
def triX : Fin 3 → ℚ := ![0, 1, 0]

/-- INSTANCE: `d1 ∘ d0 = 0` for the triangle. -/
theorem tri_d1_d0 : ∀ v : Fin 3, ∑ e, triD1 0 e * triD0 e v = 0 := by
  intro v; fin_cases v <;> simp [triD1, triD0, Fin.sum_univ_three]

/-- INSTANCE: the filled triangle with defect `(1,1,0)` has `Phi1 = 2`, attained at `x = (0,1,0)`. -/
theorem tri_phi :
    (∀ z, (2 : ℚ) ≤ cost triD0 triW triH z) ∧ ∃ z, cost triD0 triW triH z = 2 := by
  have hann : ∀ v, ∑ e, triY e * triD0 e v = 0 := by
    intro v; fin_cases v <;> simp [triY, triD0, Fin.sum_univ_three]
  have hb : ∀ e, |triY e| ≤ triW e := by
    intro e; fin_cases e <;> simp [triY, triW]
  have hpair : ∑ e, triY e * triH e = 2 := by simp [triY, triH, Fin.sum_univ_three]; norm_num
  have hx : cost triD0 triW triH triX = 2 := by
    simp [cost, triW, triH, triD0, triX, Fin.sum_univ_three]
    norm_num
  have := isPhi_of_certificate triD0 triW triH triY hann hb triX (by rw [hx, hpair])
  rw [hpair] at this
  exact this

/-- INSTANCE: `Gamma2 = ‖d1 h‖₁ = 2` and the class is ActiveClosureFailure. -/
theorem tri_gamma2 : (∑ r, |∑ e, triD1 r e * triH e| : ℚ) = 2 ∧ diag 2 2 = .active := by
  refine ⟨?_, ?_⟩
  · simp [triD1, triH, Fin.sum_univ_three]; norm_num
  · simp [diag]

end Triangle

end WdpDegree1Window

#print axioms WdpDegree1Window.kappa_descends_iff
#print axioms WdpDegree1Window.ker_kappa_eq_map
#print axioms WdpDegree1Window.kappa_eq_zero_iff
#print axioms WdpDegree1Window.kappa_not_defined_instance
#print axioms WdpDegree1Window.isPhi_shift
#print axioms WdpDegree1Window.isPhi_zero_iff
#print axioms WdpDegree1Window.diag_unique
#print axioms WdpDegree1Window.ratio_class
#print axioms WdpDegree1Window.weak_duality
#print axioms WdpDegree1Window.tri_phi
#print axioms WdpDegree1Window.tri_gamma2
