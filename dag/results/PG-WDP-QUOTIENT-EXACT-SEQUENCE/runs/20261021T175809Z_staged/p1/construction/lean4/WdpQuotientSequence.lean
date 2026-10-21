import Mathlib.LinearAlgebra.Quotient.Basic
import Mathlib.LinearAlgebra.Dual.Lemmas
import Mathlib.LinearAlgebra.FiniteDimensional.Lemmas
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Data.Fin.VecNotation
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Abel

/-!
# The exact sequence 0 -> H1 -> Q1 -> im d1 -> 0, its non-canonical splitting and the bound Gamma2 <= ‖d1‖ Phi1

AuthorityEffect: None.  Scope: a declared window `(C0, C1, C2, d0, d1)` of modules over a field with
`d1 ∘ d0 = 0`; weighted-L1 norms for the inequality.  The window is a declared datum, not derived.

Proved (general over modules over a field unless marked INSTANCE):
* `exact_sequence`: `incl : H1 → Q1` is injective, `ker pi = range incl`, `pi : Q1 → im d1` is onto
  (`kappa` and `H1` as in the source `Obstruction.lean`, here on mathlib quotient modules).
* `finrank_sequence`: `dim Q1 = dim H1 + dim im d1`, `dim Q1 + dim im d0 = dim C1` (finite dimension).
* `no_natural_section`: if `H1` and `im d1` are both nontrivial then NO section of `pi` is fixed by all
  automorphisms `1 + incl ∘ f ∘ pi` (they fix `H1` pointwise and induce the identity on `im d1`):
  the sequence has no canonical splitting.  Boundary: `section_unique_of_subsingleton` and `exists_unique_invariant_section_of_trivial` (when `H1 = 0` or
  `im d1 = 0`, i.e. `d1 = 0`, there is exactly one section and it is invariant, so "no canonical splitting" is FALSE there).
  The automorphisms `1 + incl f pi` are automorphisms of the EXTENSION, not of the window or isometries of `J`.
* `window_instance_no_natural_section` (INSTANCE): the model `C1 = ℚ²`, `d0 = 0`, `d1 (a,b) = b`.
* `diag_unique`, `isPhi_zero_iff`: exactly one diagnostic class; `Phi1 = 0` iff the class is zero when `J`
  is definite; `seminorm_instance`: for a seminorm `Phi1 = 0` does NOT force the zero class.
* `gamma_le_opnorm_phi`, `opbound_of_columns`, `columns_of_opbound`: `Gamma2 <= c * Phi1` for any `c` with
  `‖d1 v‖₁ <= c * ‖v‖_J` (weighted L1), and the least such `c` is `max_e (Σ_r |d1_re|) / w_e`;
  `gamma_bound_fails_instance` (INSTANCE): with a smaller constant (the largest entry instead of the
  column sum) the inequality is false.
Not proved: the inequality for a norm other than weighted L1, existence of minimisers (part of `IsPhi`),
any claim over ℂ, or any derivation of the window.
-/

set_option linter.unusedSectionVars false

namespace WdpQuotientSequence

section Sequence

variable {K : Type*} [Field K] {C0 C1 C2 : Type*}
  [AddCommGroup C0] [Module K C0] [AddCommGroup C1] [Module K C1] [AddCommGroup C2] [Module K C2]

abbrev Q1 (d0 : C0 →ₗ[K] C1) : Type _ := C1 ⧸ LinearMap.range d0

/-- `kappa1 : Q1 → C2`, defined when `d1 ∘ d0 = 0`. -/
def kappa (d0 : C0 →ₗ[K] C1) (d1 : C1 →ₗ[K] C2) (h : d1 ∘ₗ d0 = 0) : Q1 d0 →ₗ[K] C2 :=
  (LinearMap.range d0).liftQ d1 (LinearMap.range_le_ker_iff.mpr h)

@[simp] theorem kappa_mk (d0 : C0 →ₗ[K] C1) (d1 : C1 →ₗ[K] C2) (h : d1 ∘ₗ d0 = 0) (x : C1) :
    kappa d0 d1 h (Submodule.Quotient.mk x) = d1 x := rfl

/-- `kappa1` has the same range as `d1`. -/
theorem range_kappa (d0 : C0 →ₗ[K] C1) (d1 : C1 →ₗ[K] C2) (h : d1 ∘ₗ d0 = 0) :
    LinearMap.range (kappa d0 d1 h) = LinearMap.range d1 := by
  ext z
  constructor
  · rintro ⟨q, rfl⟩
    obtain ⟨x, rfl⟩ := Submodule.Quotient.mk_surjective _ q
    exact ⟨x, rfl⟩
  · rintro ⟨x, rfl⟩
    exact ⟨Submodule.Quotient.mk x, rfl⟩

/-- The quotient map `Q1 → im d1`. -/
def pi (d0 : C0 →ₗ[K] C1) (d1 : C1 →ₗ[K] C2) (h : d1 ∘ₗ d0 = 0) :
    Q1 d0 →ₗ[K] LinearMap.range d1 :=
  (kappa d0 d1 h).codRestrict (LinearMap.range d1) fun q => by
    rw [← range_kappa d0 d1 h]; exact ⟨q, rfl⟩

/-- The inclusion `H1 = ker kappa1 → Q1`. -/
def incl (d0 : C0 →ₗ[K] C1) (d1 : C1 →ₗ[K] C2) (h : d1 ∘ₗ d0 = 0) :
    LinearMap.ker (kappa d0 d1 h) →ₗ[K] Q1 d0 := Submodule.subtype _

/-- Exactness of `0 → H1 → Q1 → im d1 → 0`. -/
theorem exact_sequence (d0 : C0 →ₗ[K] C1) (d1 : C1 →ₗ[K] C2) (h : d1 ∘ₗ d0 = 0) :
    Function.Injective (incl d0 d1 h) ∧
    LinearMap.ker (pi d0 d1 h) = LinearMap.range (incl d0 d1 h) ∧
    Function.Surjective (pi d0 d1 h) := by
  refine ⟨Submodule.injective_subtype _, ?_, ?_⟩
  · ext q
    simp only [LinearMap.mem_ker, LinearMap.mem_range]
    constructor
    · intro hq
      refine ⟨⟨q, ?_⟩, rfl⟩
      have := congrArg Subtype.val hq
      simpa [pi] using this
    · rintro ⟨⟨q', hq'⟩, rfl⟩
      exact Subtype.ext (LinearMap.mem_ker.mp hq')
  · rintro ⟨z, x, rfl⟩
    exact ⟨Submodule.Quotient.mk x, Subtype.ext rfl⟩

/-- Dimension count for finite-dimensional modules. -/
theorem finrank_sequence [Module.Finite K C1] (d0 : C0 →ₗ[K] C1) (d1 : C1 →ₗ[K] C2)
    (h : d1 ∘ₗ d0 = 0) :
    Module.finrank K (Q1 d0) =
      Module.finrank K (LinearMap.ker (kappa d0 d1 h)) + Module.finrank K (LinearMap.range d1) ∧
    Module.finrank K (Q1 d0) + Module.finrank K (LinearMap.range d0) = Module.finrank K C1 := by
  refine ⟨?_, Submodule.finrank_quotient_add_finrank _⟩
  have := LinearMap.finrank_range_add_finrank_ker (kappa d0 d1 h)
  rw [range_kappa] at this
  omega

end Sequence

section Splitting

variable {K : Type*} [Field K] {H Q I : Type*}
  [AddCommGroup H] [Module K H] [AddCommGroup Q] [Module K Q] [AddCommGroup I] [Module K I]

/-- The unipotent automorphism `1 + i ∘ f ∘ p` of the middle term of `0 → H → Q → I → 0`. -/
def phi (i : H →ₗ[K] Q) (p : Q →ₗ[K] I) (f : I →ₗ[K] H) : Q →ₗ[K] Q :=
  LinearMap.id + i ∘ₗ f ∘ₗ p

variable (i : H →ₗ[K] Q) (p : Q →ₗ[K] I) (hi : Function.Injective i)
  (hex : ∀ q, p q = 0 ↔ q ∈ LinearMap.range i)

include hex in
theorem phi_fixes_H (f : I →ₗ[K] H) (x : H) : phi i p f (i x) = i x := by
  have : p (i x) = 0 := (hex _).mpr ⟨x, rfl⟩
  simp [phi, this]

include hex in
theorem phi_induces_id (f : I →ₗ[K] H) (q : Q) : p (phi i p f q) = p q := by
  have : p (i (f (p q))) = 0 := (hex _).mpr ⟨_, rfl⟩
  simp [phi, this]

include hex in
theorem phi_inverse (f : I →ₗ[K] H) (q : Q) : phi i p (-f) (phi i p f q) = q := by
  have h1 : p (i (f (p q))) = 0 := (hex _).mpr ⟨_, rfl⟩
  simp [phi, h1]

include hi in
/-- The automorphism `phi f` fixes the section `s` iff `f = 0`. -/
theorem phi_section_iff (s : I →ₗ[K] Q) (hs : ∀ y, p (s y) = y) (f : I →ₗ[K] H) :
    (∀ y, phi i p f (s y) = s y) ↔ f = 0 := by
  constructor
  · intro h
    ext y
    have := h y
    simp only [phi, LinearMap.add_apply, LinearMap.id_apply, LinearMap.comp_apply, hs] at this
    exact hi (by simpa using this)
  · rintro rfl y
    simp [phi]

include hi hex in
/-- No canonical splitting: when `H` and `I` are nontrivial, no section of `p` is fixed by every
automorphism `1 + i f p`. -/
theorem no_natural_section [Nontrivial H] [Nontrivial I] :
    ¬ ∃ s : I →ₗ[K] Q, (∀ y, p (s y) = y) ∧ ∀ f : I →ₗ[K] H, ∀ y, phi i p f (s y) = s y := by
  rintro ⟨s, hs, hfix⟩
  obtain ⟨v, hv⟩ := exists_ne (0 : I)
  obtain ⟨h0, hh0⟩ := exists_ne (0 : H)
  have hd : ¬ ∀ φ : Module.Dual K I, φ v = 0 := fun h => hv ((Module.forall_dual_apply_eq_zero_iff K v).mp h)
  push Not at hd
  obtain ⟨φ, hφ⟩ := hd
  let f : I →ₗ[K] H := φ.smulRight h0
  have hf : f ≠ 0 := by
    intro h
    have := congrArg (fun g : I →ₗ[K] H => g v) h
    simp only [f, LinearMap.smulRight_apply, LinearMap.zero_apply] at this
    exact (smul_ne_zero hφ hh0) this
  exact hf ((phi_section_iff i p hi s hs f).mp (hfix f))

include hex in
/-- Boundary: with `H` trivial the section is unique, so a canonical splitting exists. -/
theorem section_unique_of_subsingleton [Subsingleton H] (s t : I →ₗ[K] Q)
    (hs : ∀ y, p (s y) = y) (ht : ∀ y, p (t y) = y) : s = t := by
  ext y
  have : p (s y - t y) = 0 := by simp [hs, ht]
  obtain ⟨x, hx⟩ := (hex _).mp this
  have hx0 : x = 0 := Subsingleton.elim _ _
  have : s y - t y = 0 := by rw [← hx, hx0, map_zero]
  exact sub_eq_zero.mp this

include hex in
/-- Boundary, both halves: when `H` or `I` is trivial (and `p` is onto) there is exactly one section, and it is
invariant under every `1 + i f p` (they act as the identity). -/
theorem exists_unique_invariant_section_of_trivial (hsurj : Function.Surjective p)
    (htriv : Subsingleton H ∨ Subsingleton I) :
    ∃! s : I →ₗ[K] Q, (∀ y, p (s y) = y) ∧ ∀ f : I →ₗ[K] H, ∀ y, phi i p f (s y) = s y := by
  rcases htriv with hH | hI
  · have hinj : Function.Injective p := by
      intro a b hab
      have h0 : p (a - b) = 0 := by rw [map_sub, hab, sub_self]
      obtain ⟨x, hx⟩ := (hex _).mp h0
      have hx0 : x = 0 := Subsingleton.elim _ _
      rw [hx0, map_zero] at hx
      exact sub_eq_zero.mp hx.symm
    let e := LinearEquiv.ofBijective p ⟨hinj, hsurj⟩
    refine ⟨e.symm.toLinearMap, ⟨fun y => e.apply_symm_apply y, fun f y => ?_⟩, ?_⟩
    · have : f (p (e.symm y)) = 0 := Subsingleton.elim _ _
      simp [phi, this]
    · rintro s' ⟨hs', _⟩
      exact section_unique_of_subsingleton i p hex s' e.symm.toLinearMap hs' (fun y => e.apply_symm_apply y)
  · refine ⟨0, ⟨fun y => ?_, fun f y => ?_⟩, ?_⟩
    · have : y = 0 := Subsingleton.elim _ _
      simp [this]
    · simp [phi]
    · rintro s' _
      ext y
      have : y = 0 := Subsingleton.elim _ _
      simp [this]

end Splitting

section Model

/-- INSTANCE window: `C0 = ℚ` with `d0 = 0`, `C1 = ℚ × ℚ`, `C2 = ℚ`, `d1 (a,b) = b`. -/
def m_d0 : ℚ →ₗ[ℚ] ℚ × ℚ := 0
def m_d1 : ℚ × ℚ →ₗ[ℚ] ℚ := LinearMap.snd ℚ ℚ ℚ
theorem m_cl : m_d1 ∘ₗ m_d0 = 0 := by ext; simp [m_d0]

instance : Nontrivial (LinearMap.ker (kappa m_d0 m_d1 m_cl)) := by
  refine ⟨⟨⟨Submodule.Quotient.mk (1, 0), by simp [m_d1]⟩, 0, ?_⟩⟩
  intro h
  have := congrArg Subtype.val h
  simp only [ZeroMemClass.coe_zero] at this
  rw [Submodule.Quotient.mk_eq_zero] at this
  simp [m_d0] at this

instance : Nontrivial (LinearMap.range m_d1) := by
  refine ⟨⟨⟨1, ⟨(0, 1), by simp [m_d1]⟩⟩, 0, ?_⟩⟩
  intro h
  have := congrArg Subtype.val h
  simp at this

/-- INSTANCE: in this exact model no section of `Q1 → im d1` is invariant under all the automorphisms. -/
theorem window_instance_no_natural_section :
    ¬ ∃ s : LinearMap.range m_d1 →ₗ[ℚ] Q1 m_d0, (∀ y, pi m_d0 m_d1 m_cl (s y) = y) ∧
      ∀ f : LinearMap.range m_d1 →ₗ[ℚ] LinearMap.ker (kappa m_d0 m_d1 m_cl), ∀ y,
        phi (incl m_d0 m_d1 m_cl) (pi m_d0 m_d1 m_cl) f (s y) = s y := by
  obtain ⟨hinj, hker, _⟩ := exact_sequence m_d0 m_d1 m_cl
  exact no_natural_section (incl m_d0 m_d1 m_cl) (pi m_d0 m_d1 m_cl) hinj
    (fun q => by rw [← LinearMap.mem_ker, hker])

end Model

section Diagnostic

inductive Diag | exact | closedResidual | active
  deriving DecidableEq

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

variable {K : Type*} [Field K] {C0 C1 : Type*}
  [AddCommGroup C0] [Module K C0] [AddCommGroup C1] [Module K C1]

/-- The quotient defect: attained minimum of `J` over the class of `h`. -/
def IsPhi (J : C1 → ℚ) (d0 : C0 →ₗ[K] C1) (h : C1) (p : ℚ) : Prop :=
  (∀ x, p ≤ J (h + d0 x)) ∧ ∃ x, J (h + d0 x) = p

/-- With a definite nonnegative `J`: `Phi1 = 0` exactly for the zero class. -/
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

/-- Boundary (INSTANCE, `J = 0` is a seminorm): `Phi1 = 0` but the class of `1` is nonzero. -/
theorem seminorm_instance :
    IsPhi (fun _ : ℚ => (0 : ℚ)) (0 : ℚ →ₗ[ℚ] ℚ) 1 0 ∧
      (Submodule.Quotient.mk (1 : ℚ) : Q1 (0 : ℚ →ₗ[ℚ] ℚ)) ≠ 0 := by
  refine ⟨⟨fun _ => le_refl _, 0, rfl⟩, ?_⟩
  rw [Ne, Submodule.Quotient.mk_eq_zero]
  simp

end Diagnostic

section Inequality

open Finset

variable {m n k : ℕ}

/-- Weighted L1 norm. -/
def wl1 (w v : Fin m → ℚ) : ℚ := ∑ e, w e * |v e|
/-- `Gamma2 = ‖d1 v‖₁` for the matrix `D1` (unweighted L1). -/
def gamma2 (D1 : Fin k → Fin m → ℚ) (v : Fin m → ℚ) : ℚ := ∑ r, |∑ e, D1 r e * v e|
/-- Repair cost in the quotient convention `h + D0 x`. -/
def rcost (D0 : Fin m → Fin n → ℚ) (w h : Fin m → ℚ) (x : Fin n → ℚ) : ℚ :=
  wl1 w (fun e => h e + ∑ v, D0 e v * x v)
def IsPhiM (D0 : Fin m → Fin n → ℚ) (w h : Fin m → ℚ) (p : ℚ) : Prop :=
  (∀ x, p ≤ rcost D0 w h x) ∧ ∃ x, rcost D0 w h x = p

/-- The norm hypothesis in column form implies `‖d1 v‖₁ ≤ c ‖v‖_J`. -/
theorem opbound_of_columns (D1 : Fin k → Fin m → ℚ) (w : Fin m → ℚ) (c : ℚ)
    (hcol : ∀ e, ∑ r, |D1 r e| ≤ c * w e) (v : Fin m → ℚ) : gamma2 D1 v ≤ c * wl1 w v := by
  unfold gamma2 wl1
  calc ∑ r, |∑ e, D1 r e * v e| ≤ ∑ r, ∑ e, |D1 r e| * |v e| := by
        refine Finset.sum_le_sum fun r _ => ?_
        calc |∑ e, D1 r e * v e| ≤ ∑ e, |D1 r e * v e| := Finset.abs_sum_le_sum_abs _ _
          _ = ∑ e, |D1 r e| * |v e| := by simp only [abs_mul]
    _ = ∑ e, (∑ r, |D1 r e|) * |v e| := by
        rw [Finset.sum_comm]; simp only [Finset.sum_mul]
    _ ≤ ∑ e, (c * w e) * |v e| :=
        Finset.sum_le_sum fun e _ => mul_le_mul_of_nonneg_right (hcol e) (abs_nonneg _)
    _ = c * ∑ e, w e * |v e| := by rw [Finset.mul_sum]; exact Finset.sum_congr rfl fun e _ => by ring

/-- Conversely the column bound is necessary (unit vectors): the least constant is the column maximum. -/
theorem columns_of_opbound (D1 : Fin k → Fin m → ℚ) (w : Fin m → ℚ) (c : ℚ)
    (hb : ∀ v, gamma2 D1 v ≤ c * wl1 w v) (e : Fin m) : ∑ r, |D1 r e| ≤ c * w e := by
  have := hb (Pi.single e 1)
  have e1 : gamma2 D1 (Pi.single e 1) = ∑ r, |D1 r e| := by
    unfold gamma2
    refine Finset.sum_congr rfl fun r _ => ?_
    congr 1
    rw [Finset.sum_eq_single e]
    · simp
    · intro b _ hb; simp [hb]
    · simp
  have e2 : wl1 w (Pi.single e 1) = w e := by
    unfold wl1
    rw [Finset.sum_eq_single e]
    · simp
    · intro b _ hb; simp [hb]
    · simp
  rwa [e1, e2] at this

/-- Gamma2 is constant on a class when `D1 * D0 = 0`. -/
theorem gamma2_repair (D0 : Fin m → Fin n → ℚ) (D1 : Fin k → Fin m → ℚ)
    (hcl : ∀ r v, ∑ e, D1 r e * D0 e v = 0) (h : Fin m → ℚ) (x : Fin n → ℚ) :
    gamma2 D1 (fun e => h e + ∑ v, D0 e v * x v) = gamma2 D1 h := by
  unfold gamma2
  refine Finset.sum_congr rfl fun r _ => ?_
  congr 1
  have : ∑ e, D1 r e * (h e + ∑ v, D0 e v * x v) = ∑ e, D1 r e * h e + ∑ v, (∑ e, D1 r e * D0 e v) * x v := by
    simp only [mul_add, Finset.sum_add_distrib, Finset.mul_sum, Finset.sum_mul]
    congr 1
    rw [Finset.sum_comm]
    exact Finset.sum_congr rfl fun v _ => Finset.sum_congr rfl fun e _ => by ring
  rw [this]
  simp [hcl]

/-- `Gamma2 ≤ ‖d1‖ · Phi1` for the weighted-L1 window, with the operator-norm hypothesis in column form. -/
theorem gamma_le_opnorm_phi (D0 : Fin m → Fin n → ℚ) (D1 : Fin k → Fin m → ℚ)
    (hcl : ∀ r v, ∑ e, D1 r e * D0 e v = 0) (w h : Fin m → ℚ) (c p : ℚ)
    (hcol : ∀ e, ∑ r, |D1 r e| ≤ c * w e) (hp : IsPhiM D0 w h p) : gamma2 D1 h ≤ c * p := by
  obtain ⟨_, x, hx⟩ := hp
  have := opbound_of_columns D1 w c hcol (fun e => h e + ∑ v, D0 e v * x v)
  rw [gamma2_repair D0 D1 hcl] at this
  unfold rcost at hx
  rw [hx] at this
  exact this

/-- The source reading: `Gamma2` taken at the minimal residual obeys the bound with NO closure hypothesis. -/
theorem gamma_at_minimiser_le (D0 : Fin m → Fin n → ℚ) (D1 : Fin k → Fin m → ℚ) (w h : Fin m → ℚ)
    (c p : ℚ) (hcol : ∀ e, ∑ r, |D1 r e| ≤ c * w e) (hp : IsPhiM D0 w h p) :
    ∃ x : Fin n → ℚ, gamma2 D1 (fun e => h e + ∑ v, D0 e v * x v) ≤ c * p := by
  obtain ⟨_, x, hx⟩ := hp
  refine ⟨x, ?_⟩
  have := opbound_of_columns D1 w c hcol (fun e => h e + ∑ v, D0 e v * x v)
  unfold rcost at hx
  rw [hx] at this
  exact this

/-- Nonnegativity of `Gamma2`. -/
theorem gamma2_nonneg (D1 : Fin k → Fin m → ℚ) (v : Fin m → ℚ) : 0 ≤ gamma2 D1 v :=
  Finset.sum_nonneg fun _ _ => abs_nonneg _

/-- INSTANCE (hypothesis dropped): one edge, weight 1, `d1` the column `(1,1,1)`, `d0 = 0`, `h = 1`:
`Phi1 = 1`, `Gamma2 = 3`, and the inequality fails for `c = 1` (largest entry used as "‖d1‖"). -/
theorem gamma_bound_fails_instance :
    IsPhiM (fun _ _ : Fin 1 => (0 : ℚ)) (fun _ => 1) (fun _ => 1) 1 ∧
      gamma2 (fun (_ : Fin 3) (_ : Fin 1) => (1 : ℚ)) (fun _ => 1) = 3 ∧
      ¬ gamma2 (fun (_ : Fin 3) (_ : Fin 1) => (1 : ℚ)) (fun _ => 1) ≤ 1 * 1 ∧
      ¬ ∀ e : Fin 1, ∑ r : Fin 3, |(fun (_ : Fin 3) (_ : Fin 1) => (1 : ℚ)) r e| ≤ 1 * (fun (_ : Fin 1) => (1 : ℚ)) e := by
  refine ⟨⟨fun x => ?_, fun _ => 0, ?_⟩, ?_, ?_, ?_⟩
  · simp [rcost, wl1]
  · simp [rcost, wl1]
  · simp [gamma2]
  · simp [gamma2]
  · intro h
    have := h 0
    simp at this

end Inequality

end WdpQuotientSequence

#print axioms WdpQuotientSequence.exact_sequence
#print axioms WdpQuotientSequence.finrank_sequence
#print axioms WdpQuotientSequence.no_natural_section
#print axioms WdpQuotientSequence.section_unique_of_subsingleton
#print axioms WdpQuotientSequence.exists_unique_invariant_section_of_trivial
#print axioms WdpQuotientSequence.gamma2_repair
#print axioms WdpQuotientSequence.gamma_at_minimiser_le
#print axioms WdpQuotientSequence.gamma2_nonneg
#print axioms WdpQuotientSequence.window_instance_no_natural_section
#print axioms WdpQuotientSequence.diag_unique
#print axioms WdpQuotientSequence.isPhi_zero_iff
#print axioms WdpQuotientSequence.seminorm_instance
#print axioms WdpQuotientSequence.opbound_of_columns
#print axioms WdpQuotientSequence.columns_of_opbound
#print axioms WdpQuotientSequence.gamma_le_opnorm_phi
#print axioms WdpQuotientSequence.gamma_bound_fails_instance
