import Mathlib
import WitnessedDifference.ClassicalPackage
import WitnessedDifference.EmpiricalModel

/-!
# A composition principle for two finite systems

`WDP-CH19-O02` asks for a composition principle for two systems, its
consistency with the observer architecture, and the countermodels it excludes.
Primitive difference does not choose among Cartesian, tensor and constrained
composites. This module states a composition principle that needs no import
and proves what its clauses do and do not decide.

The composition principle CP has three clauses:

* (T) injective tagging: the composite report determines both local reports;
* (NS) no-signalling: a complete local instrument, summed over its outcomes,
  preserves the other side's marginal, and on the CHSH product cover this is compatibility on
  overlaps;
* (B) bilinear positivity: a composite state is a bilinear form on product
  effects that is nonnegative and normalized. It is formulated here for
  classical carriers only.

* `WDP-CH19-P08`. A composite tagging has local decoders for both factors
  exactly when it is injective. The degenerate map `dumpRight`, which forgets
  the left report, has none.
* `WDP-CH19-P09`. For the Cartesian composite, summing a complete local
  instrument `1 ⊗ K_o` over all outcomes preserves the other factor's marginal.
  A selected outcome need not preserve it. A presentation map on one
  factor lifts to the composite and commutes with marginalization.
* `WDP-CH19-P10`. For classical carriers, clause (B) forces the composite
  state to be a joint distribution on the Cartesian product, uniquely. On the
  CHSH product cover the PR box satisfies (NS), is compatible, and is not
  noncontextual: clauses (T) and (NS) alone do not exclude it. Clause (B) is not
  formulated for its nonclassical factors, so its status under CP is undecided.

Nothing here excludes the PR box or derives the Hilbert tensor product
(import 5). This file declares no synthetic axioms.
-/

set_option linter.unusedSectionVars false
set_option linter.unusedSimpArgs false

namespace WitnessedDifference.Composition

open Matrix Finset

/-! ## `WDP-CH19-P08`: injective tagging -/

section Tagging

variable {A B C : Type*}

/-- The tagging that forgets the left report. -/
def dumpRight : A × B → B := Prod.snd

/-- A composite tagging has local decoders for both factors. -/
def LocallyRecoverable (c : A × B → C) : Prop :=
  ∃ (dA : C → A) (dB : C → B), ∀ a b, dA (c (a, b)) = a ∧ dB (c (a, b)) = b

theorem injective_of_locallyRecoverable {c : A × B → C} (h : LocallyRecoverable c) :
    Function.Injective c := by
  obtain ⟨dA, dB, hd⟩ := h
  rintro ⟨a, b⟩ ⟨a', b'⟩ hc
  have h1 := (hd a b).1
  have h2 := (hd a b).2
  have h3 := (hd a' b').1
  have h4 := (hd a' b').2
  rw [hc] at h1 h2
  exact Prod.ext (h1.symm.trans h3) (h2.symm.trans h4)

theorem locallyRecoverable_of_injective [Nonempty A] [Nonempty B] {c : A × B → C}
    (h : Function.Injective c) : LocallyRecoverable c := by
  classical
  refine ⟨fun x => (Function.invFun c x).1, fun x => (Function.invFun c x).2,
    fun a b => ?_⟩
  have := Function.leftInverse_invFun h (a, b)
  simp [this]

/-- `WDP-CH19-P08`. A composite tagging has local decoders for both factors
exactly when it is injective. -/
theorem locallyRecoverable_iff_injective [Nonempty A] [Nonempty B] (c : A × B → C) :
    LocallyRecoverable c ↔ Function.Injective c :=
  ⟨injective_of_locallyRecoverable, locallyRecoverable_of_injective⟩

/-- `WDP-CH19-P08`. The tagging `dumpRight` forgets the left report: with two
distinct left reports it is not injective, so it has no local decoders. -/
theorem dumpRight_not_recoverable [Nontrivial A] [Nonempty B] :
    ¬ LocallyRecoverable (dumpRight : A × B → B) := by
  intro h
  have hi := injective_of_locallyRecoverable h
  obtain ⟨a, a', hne⟩ := exists_pair_ne A
  obtain ⟨b⟩ := ‹Nonempty B›
  exact hne (congrArg Prod.fst (hi (a₁ := (a, b)) (a₂ := (a', b)) rfl))

end Tagging

/-! ## `WDP-CH19-P09`: no-signalling and observer compatibility -/

section NoSignalling

variable {A B O : Type*} [Fintype A] [Fintype B] [DecidableEq A] [DecidableEq B]
  [Fintype O]

/-- The local update `1 ⊗ K` on the second factor of `A × B`. -/
def localRight (K : Matrix B B ℚ) : Matrix (A × B) (A × B) ℚ :=
  Matrix.kroneckerMap (· * ·) (1 : Matrix A A ℚ) K

/-- The local update `K ⊗ 1` on the first factor of `A × B`. -/
def localLeft (K : Matrix A A ℚ) : Matrix (A × B) (A × B) ℚ :=
  Matrix.kroneckerMap (· * ·) K (1 : Matrix B B ℚ)

theorem localRight_mulVec (K : Matrix B B ℚ) (p : A × B → ℚ) (a : A) (b' : B) :
    (localRight K *ᵥ p) (a, b') = (K *ᵥ fun b => p (a, b)) b' := by
  simp [localRight, mulVec, dotProduct, Fintype.sum_prod_type, Matrix.kroneckerMap_apply,
    Matrix.one_apply]

theorem localLeft_mulVec (K : Matrix A A ℚ) (p : A × B → ℚ) (a' : A) (b : B) :
    (localLeft K *ᵥ p) (a', b) = (K *ᵥ fun a => p (a, b)) a' := by
  simp [localLeft, mulVec, dotProduct, Fintype.sum_prod_type, Matrix.kroneckerMap_apply,
    Matrix.one_apply]

/-- `WDP-CH19-P09`. A local classical instrument on the second factor does not
change the marginal of the first: summed over outcomes and post-states, the
weight over `a` is the weight over `a` before. -/
theorem noSignalling_right (I : ClassicalPackage.Instrument B O) (p : A × B → ℚ)
    (a : A) :
    ∑ o, ∑ b', (localRight (A := A) (I.T o) *ᵥ p) (a, b') = ∑ b, p (a, b) := by
  simp_rw [localRight_mulVec]
  exact I.sum_step fun b => p (a, b)

/-- `WDP-CH19-P09`, the symmetric statement for the first factor. -/
theorem noSignalling_left (I : ClassicalPackage.Instrument A O) (p : A × B → ℚ)
    (b : B) :
    ∑ o, ∑ a', (localLeft (B := B) (I.T o) *ᵥ p) (a', b) = ∑ a, p (a, b) := by
  simp_rw [localLeft_mulVec]
  exact I.sum_step fun a => p (a, b)

/-- Two different local instruments on the second factor leave the marginal of
the first factor equal: what the second party does cannot be seen locally. -/
theorem marginal_independent_of_choice (I J : ClassicalPackage.Instrument B O)
    (p : A × B → ℚ) (a : A) :
    ∑ o, ∑ b', (localRight (A := A) (I.T o) *ᵥ p) (a, b') =
      ∑ o, ∑ b', (localRight (A := A) (J.T o) *ᵥ p) (a, b') := by
  rw [noSignalling_right, noSignalling_right]

/-- A presentation map on the first factor lifts to the composite as
`pres ∘ fst`, and pushing forward the first marginal is the first marginal of
the pushforward: the observer of one side commutes with marginalization. -/
theorem presentation_commutes_with_marginal {Q : Type*} [DecidableEq Q]
    (pres : A → Q) (p : A × B → ℚ) (r : Q) :
    ∑ a ∈ univ.filter (fun a => pres a = r), ∑ b, p (a, b) =
      ∑ x ∈ univ.filter (fun x : A × B => pres x.1 = r), p x := by
  rw [Finset.sum_filter, Finset.sum_filter, Fintype.sum_prod_type]
  refine Finset.sum_congr rfl fun a _ => ?_
  by_cases h : pres a = r <;> simp [h]

end NoSignalling

/-! ## `WDP-CH19-P10`: classical composites are Cartesian -/

section Classical

variable {A B : Type*} [Fintype A] [Fintype B] [DecidableEq A] [DecidableEq B]

/-- A bilinear form on effect vectors of `A` and `B`. -/
abbrev Bil (A B : Type*) := (A → ℚ) →ₗ[ℚ] (B → ℚ) →ₗ[ℚ] ℚ

/-- The bilinear form of a joint weight. -/
def ofJoint (p : A → B → ℚ) : Bil A B :=
  LinearMap.mk₂ ℚ (fun e f => ∑ a, ∑ b, e a * f b * p a b)
    (fun e e' f => by
      simp only [Pi.add_apply, add_mul, Finset.sum_add_distrib])
    (fun c e f => by
      simp only [Pi.smul_apply, smul_eq_mul, Finset.mul_sum, mul_assoc])
    (fun e f f' => by
      simp only [Pi.add_apply, mul_add, add_mul, Finset.sum_add_distrib])
    (fun c e f => by
      simp only [Pi.smul_apply, smul_eq_mul, Finset.mul_sum]
      refine Finset.sum_congr rfl fun a _ => Finset.sum_congr rfl fun b _ => ?_
      ring)

/-- The weight a bilinear form gives to a pair of indicator effects. -/
def jointOf (ω : Bil A B) (a : A) (b : B) : ℚ :=
  ω (Pi.single a 1) (Pi.single b 1)

theorem ofJoint_apply (p : A → B → ℚ) (e : A → ℚ) (f : B → ℚ) :
    ofJoint p e f = ∑ a, ∑ b, e a * f b * p a b := rfl

theorem jointOf_ofJoint (p : A → B → ℚ) (a : A) (b : B) :
    jointOf (ofJoint p) a b = p a b := by
  simp [jointOf, ofJoint_apply, Pi.single_apply]

/-- A bilinear form is its joint weight on indicator effects. -/
theorem bil_eq_ofJoint (ω : Bil A B) : ω = ofJoint (jointOf ω) := by
  apply LinearMap.ext₂
  intro e f
  have he : e = ∑ a, e a • (Pi.single a (1 : ℚ) : A → ℚ) := by
    ext x; simp [Finset.sum_apply, Pi.single_apply]
  have hf : f = ∑ b, f b • (Pi.single b (1 : ℚ) : B → ℚ) := by
    ext x; simp [Finset.sum_apply, Pi.single_apply]
  rw [ofJoint_apply]
  have h2 : ω e f = ω (∑ a, e a • (Pi.single a (1 : ℚ) : A → ℚ))
      (∑ b, f b • (Pi.single b (1 : ℚ) : B → ℚ)) := by
    rw [← he, ← hf]
  rw [h2]
  simp only [map_sum, LinearMap.sum_apply, map_smul, LinearMap.smul_apply, smul_eq_mul,
    jointOf]
  simp_rw [Finset.mul_sum]
  rw [Finset.sum_comm]
  refine Finset.sum_congr rfl fun a _ => Finset.sum_congr rfl fun b _ => ?_
  ring

/-- An effect: every value lies in `[0, 1]`. -/
def IsEffect {Q : Type*} (e : Q → ℚ) : Prop := ∀ q, 0 ≤ e q ∧ e q ≤ 1

/-- Clause (B): a composite state is nonnegative on product effects and
normalized on the unit effects. -/
def IsCompositeState (ω : Bil A B) : Prop :=
  (∀ e f, IsEffect e → IsEffect f → 0 ≤ ω e f) ∧ ω (fun _ => 1) (fun _ => 1) = 1

theorem isEffect_single {Q : Type*} [DecidableEq Q] (q : Q) :
    IsEffect (Pi.single q (1 : ℚ) : Q → ℚ) := by
  intro x
  by_cases h : x = q <;> simp [Pi.single_apply, h]

/-- `WDP-CH19-P10`. For classical carriers a composite state is exactly a joint
distribution on `A × B`, and the joint distribution is unique: a bilinear form
that is nonnegative on product effects and normalized is `ofJoint p` for a
unique nonnegative normalized `p`, and conversely. -/
theorem composite_state_iff_joint_distribution (ω : Bil A B) :
    IsCompositeState ω ↔
      ∃ p : A → B → ℚ, (∀ a b, 0 ≤ p a b) ∧ ∑ a, ∑ b, p a b = 1 ∧ ω = ofJoint p := by
  constructor
  · rintro ⟨hpos, hnorm⟩
    refine ⟨jointOf ω, fun a b => hpos _ _ (isEffect_single a) (isEffect_single b),
      ?_, bil_eq_ofJoint ω⟩
    have h := hnorm
    rw [bil_eq_ofJoint ω, ofJoint_apply] at h
    simpa using h
  · rintro ⟨p, hp, hsum, rfl⟩
    refine ⟨fun e f he hf => ?_, by simpa [ofJoint_apply] using hsum⟩
    rw [ofJoint_apply]
    exact Finset.sum_nonneg fun a _ => Finset.sum_nonneg fun b _ =>
      mul_nonneg (mul_nonneg (he a).1 (hf b).1) (hp a b)

theorem joint_unique {p q : A → B → ℚ} (h : ofJoint p = ofJoint q) : p = q := by
  funext a b
  rw [← jointOf_ofJoint p a b, ← jointOf_ofJoint q a b, h]

end Classical

/-! ## The PR box on the CHSH product cover -/

open WitnessedDifference.Empirical in
/-- `WDP-CH19-P10`. On the CHSH cover, the contexts `{(0,x), (1,y)}` are the
product cover of two two-setting scenarios. The PR box is compatible, so it
satisfies (NS) on every overlap; it is not noncontextual and has
`CHSH = 4`. So (T) and (NS) alone do not choose the Cartesian composite for
nonclassical factors. -/
theorem no_signalling_does_not_force_the_local_composite :
    Compatible chshContext prWeight ∧ ¬ IsNoncontextual chshContext prWeight ∧
      chsh prWeight = 4 :=
  ⟨prBox.compatible, prBox_signed_not_nonneg.2.2, chsh_prBox⟩

end WitnessedDifference.Composition
