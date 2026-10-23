import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Analysis.Complex.Circle
import Mathlib.Analysis.Complex.Trigonometric
import Mathlib.Data.Fintype.Pi
import Mathlib.Data.ZMod.Basic

/-!
# Campaign: FSP-U1-WILSON-ACTION

AuthorityEffect: None.
Origin: lean4/CampaignFspU1WilsonAction.lean

Claim: for any vertex type `V`, any finite family of closed oriented paths
(plaquettes) in `V`, any real coupling `β` and any `U(1)` link field
`U : V → V → Circle`, the Wilson action `S = β Σ_p (1 - Re U_p)` is unchanged by
every local gauge transformation `U a b ↦ g a * U a b * (g b)⁻¹` with
`g : V → Circle`, and `S ≥ 0` when `β ≥ 0`. With angles, `U a b = exp(i A a b)`,
the gauge action is `A a b ↦ A a b + θ a - θ b` and `Re U_p = cos (Σ_p A)`.

Supporting API:
* gauge action on link fields over any group, its unit and composition laws, and
  preservation of the orientation-reversal convention `U b a = (U a b)⁻¹`;
* gauge covariance of path holonomy over any group, conjugation of closed-path
  holonomy over any group and invariance over any commutative group;
* `S = 0` exactly when every plaquette holonomy is `1`, for `β > 0`;
* a one-plaquette model with `β = -1` and `S = -2`, so `β ≥ 0` cannot be dropped;
* the elementary plaquettes of the periodic hypercubic lattice `(ZMod L)^d`.

Not claimed: a fermion-sign consequence, a continuum limit, a transfer matrix or
reflection positivity, a gauge-fixing statement, or any non-abelian Wilson action.
-/

open scoped BigOperators

namespace CampaignFspU1WilsonAction

noncomputable section

/-! ## Gauge action and path holonomy over a group -/

section Group

variable {V G : Type*} [Group G]

/-- Local gauge action on a link field: `U a b ↦ g a * U a b * (g b)⁻¹`. -/
def gaugeAct (g : V → G) (U : V → V → G) : V → V → G :=
  fun a b => g a * U a b * (g b)⁻¹

@[simp] theorem gaugeAct_apply (g : V → G) (U : V → V → G) (a b : V) :
    gaugeAct g U a b = g a * U a b * (g b)⁻¹ := rfl

/-- The trivial gauge transformation acts as the identity. -/
theorem gaugeAct_one (U : V → V → G) : gaugeAct (fun _ => (1 : G)) U = U := by
  funext a b
  simp

/-- Successive gauge transformations compose pointwise. -/
theorem gaugeAct_gaugeAct (g h : V → G) (U : V → V → G) :
    gaugeAct g (gaugeAct h U) = gaugeAct (fun v => g v * h v) U := by
  funext a b
  simp [mul_assoc]

/-- The orientation-reversal convention `U b a = (U a b)⁻¹` is preserved by every
gauge transformation. -/
theorem gaugeAct_reversal {U : V → V → G} (hU : ∀ a b, U b a = (U a b)⁻¹)
    (g : V → G) (a b : V) : gaugeAct g U b a = (gaugeAct g U a b)⁻¹ := by
  simp only [gaugeAct_apply]
  rw [hU a b]
  simp [mul_assoc]

/-- Ordered product of link variables along the path `a → l₀ → l₁ → ⋯`.
Each ordered vertex pair uses its supplied value in `U`; an empty list gives `1`. -/
def holonomy (U : V → V → G) : V → List V → G
  | _, [] => 1
  | a, b :: rest => U a b * holonomy U b rest

/-- Last vertex of the path `a → l₀ → l₁ → ⋯`. -/
def endpoint : V → List V → V
  | a, [] => a
  | _, b :: rest => endpoint b rest

@[simp] theorem holonomy_nil (U : V → V → G) (a : V) : holonomy U a [] = 1 := rfl

@[simp] theorem holonomy_cons (U : V → V → G) (a b : V) (rest : List V) :
    holonomy U a (b :: rest) = U a b * holonomy U b rest := rfl

@[simp] theorem endpoint_nil (a : V) : endpoint a ([] : List V) = a := rfl

@[simp] theorem endpoint_cons (a b : V) (rest : List V) :
    endpoint a (b :: rest) = endpoint b rest := rfl

/-- Gauge covariance of path holonomy, over any group. -/
theorem holonomy_gaugeAct (g : V → G) (U : V → V → G) (a : V) (l : List V) :
    holonomy (gaugeAct g U) a l = g a * holonomy U a l * (g (endpoint a l))⁻¹ := by
  induction l generalizing a with
  | nil => simp
  | cons b rest ih =>
    rw [holonomy_cons, ih, endpoint_cons, holonomy_cons, gaugeAct_apply]
    simp [mul_assoc]

/-- A closed oriented path: a base vertex and a vertex list that ends at the base. -/
structure ClosedPath (V : Type*) where
  base : V
  path : List V
  closed : endpoint base path = base

/-- Holonomy around a closed oriented path. -/
def loopHolonomy (U : V → V → G) (p : ClosedPath V) : G :=
  holonomy U p.base p.path

/-- Over any group, a gauge transformation conjugates a closed-path holonomy by the
gauge value at the base vertex. -/
theorem loopHolonomy_gaugeAct_conj (g : V → G) (U : V → V → G) (p : ClosedPath V) :
    loopHolonomy (gaugeAct g U) p = g p.base * loopHolonomy U p * (g p.base)⁻¹ := by
  unfold loopHolonomy
  rw [holonomy_gaugeAct, p.closed]

end Group

section CommGroup

variable {V G : Type*} [CommGroup G]

/-- Over a commutative group, closed-path holonomy is gauge invariant. -/
theorem loopHolonomy_gaugeAct (g : V → G) (U : V → V → G) (p : ClosedPath V) :
    loopHolonomy (gaugeAct g U) p = loopHolonomy U p := by
  rw [loopHolonomy_gaugeAct_conj, mul_comm (g p.base), mul_assoc, mul_inv_cancel, mul_one]

end CommGroup

/-! ## The U(1) Wilson action -/

section Wilson

variable {V ι : Type*} [Fintype ι]

/-- Wilson action `S = β Σ_p (1 - Re U_p)` of a `U(1)` link field on a finite family
of closed oriented paths. -/
def wilsonAction (plaq : ι → ClosedPath V) (β : ℝ) (U : V → V → Circle) : ℝ :=
  β * ∑ p, (1 - ((loopHolonomy U (plaq p) : Circle) : ℂ).re)

/-- Local `U(1)` gauge invariance of the Wilson action. -/
theorem wilsonAction_gauge_invariant (plaq : ι → ClosedPath V) (β : ℝ)
    (g : V → Circle) (U : V → V → Circle) :
    wilsonAction plaq β (gaugeAct g U) = wilsonAction plaq β U := by
  simp only [wilsonAction, loopHolonomy_gaugeAct]

/-- Each plaquette term `1 - Re z` with `|z| = 1` is nonnegative. -/
theorem one_sub_re_nonneg (z : Circle) : 0 ≤ 1 - (z : ℂ).re := by
  have h := Complex.re_le_norm (z : ℂ)
  rw [Circle.norm_coe] at h
  linarith

/-- For `|z| = 1`, `Re z = 1` exactly when `z = 1`. -/
theorem re_eq_one_iff (z : Circle) : (z : ℂ).re = 1 ↔ z = 1 := by
  constructor
  · intro h
    have hn := Circle.normSq_coe z
    rw [Complex.normSq_apply, h] at hn
    have hsq : (z : ℂ).im * (z : ℂ).im = 0 := by linarith
    have him : (z : ℂ).im = 0 := mul_self_eq_zero.mp hsq
    apply Circle.coe_injective
    apply Complex.ext <;> simp [h, him]
  · rintro rfl
    simp

/-- Nonnegativity of the Wilson action for `β ≥ 0`. -/
theorem wilsonAction_nonneg (plaq : ι → ClosedPath V) {β : ℝ} (hβ : 0 ≤ β)
    (U : V → V → Circle) : 0 ≤ wilsonAction plaq β U :=
  mul_nonneg hβ (Finset.sum_nonneg fun _ _ => one_sub_re_nonneg _)

/-- For `β > 0`, the Wilson action vanishes exactly when every path in the selected
family `plaq` has holonomy `1`. -/
theorem wilsonAction_eq_zero_iff (plaq : ι → ClosedPath V) {β : ℝ} (hβ : 0 < β)
    (U : V → V → Circle) :
    wilsonAction plaq β U = 0 ↔ ∀ p, loopHolonomy U (plaq p) = 1 := by
  unfold wilsonAction
  rw [mul_eq_zero, or_iff_right hβ.ne',
    Finset.sum_eq_zero_iff_of_nonneg (fun p _ => one_sub_re_nonneg _)]
  constructor
  · intro h p
    exact (re_eq_one_iff _).1 (by linarith [h p (Finset.mem_univ _)])
  · intro h p _
    rw [h p]
    simp

/-- The one-vertex model with a single self-link plaquette. -/
def selfLoop : ClosedPath Unit := ⟨(), [()], rfl⟩

/-- With `β = -1` and the link phase `-1`, the action is `-2`; nonnegativity needs
`β ≥ 0`. -/
theorem wilsonAction_negative_beta_witness :
    wilsonAction (fun _ : Unit => selfLoop) (-1) (fun _ _ => (-1 : Circle)) = -2 := by
  simp [wilsonAction, loopHolonomy, selfLoop]
  norm_num

/-- The hypothesis `β ≥ 0` of `wilsonAction_nonneg` cannot be dropped. -/
theorem wilsonAction_nonneg_needs_beta :
    ¬ ∀ (β : ℝ) (U : Unit → Unit → Circle),
      0 ≤ wilsonAction (fun _ : Unit => selfLoop) β U := by
  intro h
  have := h (-1) (fun _ _ => (-1 : Circle))
  rw [wilsonAction_negative_beta_witness] at this
  norm_num at this

end Wilson

/-! ## Link angles: `U a b = exp(i A a b)` -/

section Angle

variable {V : Type*}

/-- Link phases from real link angles in radians, `U a b = exp(i A a b)`. -/
def linkOfAngle (A : V → V → ℝ) : V → V → Circle :=
  fun a b => Circle.exp (A a b)

/-- Local `U(1)` gauge transformation of the angles, `A a b ↦ A a b + θ a - θ b`. -/
def gaugeAngle (θ : V → ℝ) (A : V → V → ℝ) : V → V → ℝ :=
  fun a b => A a b + θ a - θ b

/-- The angle gauge transformation is the gauge action of `g = exp(i θ)`. -/
theorem linkOfAngle_gaugeAngle (θ : V → ℝ) (A : V → V → ℝ) :
    linkOfAngle (gaugeAngle θ A) = gaugeAct (fun v => Circle.exp (θ v)) (linkOfAngle A) := by
  funext a b
  simp only [linkOfAngle, gaugeAngle, gaugeAct_apply, Circle.exp_sub, Circle.exp_add,
    div_eq_mul_inv]
  rw [mul_comm (Circle.exp (A a b))]

/-- Sum of link angles in radians along the path `a → l₀ → l₁ → ⋯`.
An empty list gives `0`; the sum is not reduced modulo `2π`. -/
def pathAngle (A : V → V → ℝ) : V → List V → ℝ
  | _, [] => 0
  | a, b :: rest => A a b + pathAngle A b rest

/-- The holonomy of angle links is the exponential of the summed angle. -/
theorem holonomy_linkOfAngle (A : V → V → ℝ) (a : V) (l : List V) :
    holonomy (linkOfAngle A) a l = Circle.exp (pathAngle A a l) := by
  induction l generalizing a with
  | nil => simp [pathAngle]
  | cons b rest ih => simp [pathAngle, ih, linkOfAngle, Circle.exp_add]

/-- In angles, `S = β Σ_p (1 - cos (Σ_{links of p} A))`. -/
theorem wilsonAction_linkOfAngle {ι : Type*} [Fintype ι] (plaq : ι → ClosedPath V)
    (β : ℝ) (A : V → V → ℝ) :
    wilsonAction plaq β (linkOfAngle A)
      = β * ∑ p, (1 - Real.cos (pathAngle A (plaq p).base (plaq p).path)) := by
  simp only [wilsonAction, loopHolonomy, holonomy_linkOfAngle, Circle.coe_exp,
    Complex.exp_ofReal_mul_I_re]

/-- FSP-U1-WILSON-ACTION. With link phases `U a b = exp(i A a b)` and oriented
closed-path products `U_p` on any finite plaquette family, the Wilson action
`S = β Σ_p (1 - Re U_p)` is invariant under every local `U(1)` gauge transformation,
both as `U a b ↦ g a * U a b * (g b)⁻¹` with `g : V → Circle` and as
`A a b ↦ A a b + θ a - θ b`, and is nonnegative when `β ≥ 0`. -/
theorem fsp_u1_wilson_action {ι : Type*} [Fintype ι] (plaq : ι → ClosedPath V)
    (β : ℝ) (A : V → V → ℝ) :
    (∀ g : V → Circle,
        wilsonAction plaq β (gaugeAct g (linkOfAngle A)) = wilsonAction plaq β (linkOfAngle A)) ∧
    (∀ θ : V → ℝ,
        wilsonAction plaq β (linkOfAngle (gaugeAngle θ A)) = wilsonAction plaq β (linkOfAngle A)) ∧
    (0 ≤ β → 0 ≤ wilsonAction plaq β (linkOfAngle A)) :=
  ⟨fun g => wilsonAction_gauge_invariant plaq β g _,
   fun θ => by rw [linkOfAngle_gaugeAngle, wilsonAction_gauge_invariant],
   fun hβ => wilsonAction_nonneg plaq hβ _⟩

end Angle

/-! ## The periodic hypercubic lattice `(ZMod L)^d` -/

section Hypercubic

variable (d L : ℕ) [NeZero L]

/-- Sites of the periodic hypercubic lattice. -/
abbrev Site := Fin d → ZMod L

/-- The unit vector in direction `μ`. -/
def unitVec (μ : Fin d) : Site d L := Pi.single μ 1

/-- Plaquette labels: a site and an ordered pair of directions `μ < ν`. -/
abbrev PlaqIndex := Site d L × {q : Fin d × Fin d // q.1 < q.2}

/-- The elementary plaquette at `x` in the `μν`-plane, traversed
`x → x+μ → x+μ+ν → x+ν → x`. -/
def plaquette (i : PlaqIndex d L) : ClosedPath (Site d L) where
  base := i.1
  path := [i.1 + unitVec d L i.2.1.1, i.1 + unitVec d L i.2.1.1 + unitVec d L i.2.1.2,
    i.1 + unitVec d L i.2.1.2, i.1]
  closed := rfl

/-- The hypercubic Wilson action `β Σ_{x, μ<ν} (1 - Re U_{μν}(x))`.
Links are indexed by ordered vertex pairs, so distinct parallel links are identified
when `L ≤ 2`. -/
def hypercubicWilson (β : ℝ) (U : Site d L → Site d L → Circle) : ℝ :=
  wilsonAction (plaquette d L) β U

/-- Gauge invariance of the hypercubic Wilson action. -/
theorem hypercubicWilson_gauge_invariant (β : ℝ) (g : Site d L → Circle)
    (U : Site d L → Site d L → Circle) :
    hypercubicWilson d L β (gaugeAct g U) = hypercubicWilson d L β U :=
  wilsonAction_gauge_invariant _ β g U

/-- Nonnegativity of the hypercubic Wilson action for `β ≥ 0`. -/
theorem hypercubicWilson_nonneg {β : ℝ} (hβ : 0 ≤ β) (U : Site d L → Site d L → Circle) :
    0 ≤ hypercubicWilson d L β U :=
  wilsonAction_nonneg _ hβ U

end Hypercubic

end

end CampaignFspU1WilsonAction

#print axioms CampaignFspU1WilsonAction.holonomy_gaugeAct
#print axioms CampaignFspU1WilsonAction.loopHolonomy_gaugeAct
#print axioms CampaignFspU1WilsonAction.gaugeAct_gaugeAct
#print axioms CampaignFspU1WilsonAction.gaugeAct_reversal
#print axioms CampaignFspU1WilsonAction.wilsonAction_gauge_invariant
#print axioms CampaignFspU1WilsonAction.wilsonAction_nonneg
#print axioms CampaignFspU1WilsonAction.wilsonAction_eq_zero_iff
#print axioms CampaignFspU1WilsonAction.wilsonAction_nonneg_needs_beta
#print axioms CampaignFspU1WilsonAction.wilsonAction_linkOfAngle
#print axioms CampaignFspU1WilsonAction.fsp_u1_wilson_action
#print axioms CampaignFspU1WilsonAction.hypercubicWilson_gauge_invariant
#print axioms CampaignFspU1WilsonAction.hypercubicWilson_nonneg
