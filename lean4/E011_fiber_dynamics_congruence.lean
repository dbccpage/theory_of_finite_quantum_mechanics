/-
  E011 -- exact dynamics-congruence criterion.
  AuthorityEffect: None. Candidate only. Not estate E011. Not PROVEN.

  Target proposition
    InvariantCongruent (fiberPD p) (p circ T) is exactly
    forall x y, p x = p y -> p (T x) = p (T y). That is the
    criterion for p circ T to descend to residual classes.

  Imported carriers / ops / laws / finiteness / decidability
    L0: Type, Prop, Eq, Ne, Iff, Prod, implication.
    L1: Quotient, Setoid, Quotient.mk / sound / exact / lift.
    L2: Bool.
    Campaign deps: Core Realization / PrimitiveDifference / classOf /
    AmbientDynamics / SplitPresentation; E003 fiberPD.
    No observer, metric, unique Tbar on M (E012), Classical.choice.

  Positive finite witness
    Toggle hidden bit on Bool x Bool, p = fst. Same first coordinate
    is preserved, so p circ T is fiber-invariant.

  Falsifier / negative control
    Copy hidden bit onto the presented coordinate: (false,false) and
    (false,true) are one fiber and land on different presented values.
    Restriction of the same test to the chosen section is vacuous.

  Explicit nonclaims
    Checking T only on the chosen section is insufficient.
    Fiber congruence is independent of whether T leaves image i.
    This is not unique descended dynamics (E012).
    Estate E011 remains OPEN. Not PROVEN.
    Quot.sound / propext, if reported, are Lean kernel L1.
-/

import Core
import E003_projection_fiber_primitive_difference

namespace GrokPdNight20260814.E011

open GrokPdNight20260814.Core
open GrokPdNight20260814.E003 (fiberPD fiberPD_zeroRel_iff fiber_refl fiber_symm fiber_trans)

/-- Kernel-shaped class-constancy for a map out of a PrimitiveDifference. -/
def InvariantCongruent {α β γ : Type} (P : PrimitiveDifference α β) (φ : α → γ) : Prop :=
  ∀ x y : α, ZeroRel P x y → φ x = φ y

/-- The exact criterion: p ∘ T is invariant under fiberPD p. -/
def FiberDynamicsCongruent {X M Prov : Type}
    (p : X → M) (D : AmbientDynamics X Prov) : Prop :=
  InvariantCongruent (fiberPD p) (fun x => p (D.T x))

theorem fiber_dynamics_congruent_iff {X M Prov : Type}
    (p : X → M) (D : AmbientDynamics X Prov) :
    FiberDynamicsCongruent p D ↔
      ∀ x y : X, p x = p y → p (D.T x) = p (D.T y) := by
  constructor
  · intro h x y hp
    exact h x y ((fiberPD_zeroRel_iff p x y).mpr hp)
  · intro h x y hz
    exact h x y ((fiberPD_zeroRel_iff p x y).mp hz)

#print axioms fiber_dynamics_congruent_iff

def fiberSetoid {X M : Type} (p : X → M) : Setoid X where
  r := ZeroRel (fiberPD p)
  iseqv := {
    refl := fun x => fiber_refl p x
    symm := fun {x y} h => fiber_symm p x y h
    trans := fun {x y z} h1 h2 => fiber_trans p x y z h1 h2
  }

/-- Descent of p ∘ T through the fiber quotient, when the criterion holds. -/
def projectedFactor {X M Prov : Type} (p : X → M) (D : AmbientDynamics X Prov)
    (h : FiberDynamicsCongruent p D) :
    ResidualQuotient (fiberSetoid p) → M :=
  Quotient.lift (fun x => p (D.T x)) (fun x y hxy => h x y hxy)

theorem projectedFactor_classOf {X M Prov : Type}
    (p : X → M) (D : AmbientDynamics X Prov)
    (h : FiberDynamicsCongruent p D) (x : X) :
    projectedFactor p D h (classOf (fiberSetoid p) x) = p (D.T x) :=
  rfl

#print axioms projectedFactor_classOf

theorem projectedFactor_requires_congruence {X M Prov : Type}
    (p : X → M) (D : AmbientDynamics X Prov)
    (F : ResidualQuotient (fiberSetoid p) → M)
    (hF : ∀ x : X, F (classOf (fiberSetoid p) x) = p (D.T x)) :
    FiberDynamicsCongruent p D := by
  intro x y hxy
  calc
    p (D.T x) = F (classOf (fiberSetoid p) x) := (hF x).symm
    _ = F (classOf (fiberSetoid p) y) := by
      rw [(classOf_eq_iff (fiberSetoid p) x y).mpr hxy]
    _ = p (D.T y) := hF y

#print axioms projectedFactor_requires_congruence

theorem projectedFactor_exists_iff {X M Prov : Type}
    (p : X → M) (D : AmbientDynamics X Prov) :
    (∃ F : ResidualQuotient (fiberSetoid p) → M,
        ∀ x : X, F (classOf (fiberSetoid p) x) = p (D.T x)) ↔
      FiberDynamicsCongruent p D := by
  constructor
  · intro h
    rcases h with ⟨F, hF⟩
    exact projectedFactor_requires_congruence p D F hF
  · intro h
    exact ⟨projectedFactor p D h, projectedFactor_classOf p D h⟩

#print axioms projectedFactor_exists_iff

/-- Section points of a split lie in distinct p-fibers. -/
theorem section_points_separate {X M : Type} (S : SplitPresentation X M)
    (m m' : M) (h : S.p (S.i m) = S.p (S.i m')) : m = m' := by
  calc
    m = S.p (S.i m) := (S.split m).symm
    _ = S.p (S.i m') := h
    _ = m' := S.split m'

#print axioms section_points_separate

/-- Restricted to the chosen section, fiber preservation is automatic. -/
theorem section_restriction_always {X M Prov : Type}
    (S : SplitPresentation X M) (D : AmbientDynamics X Prov)
    (m m' : M) (h : S.p (S.i m) = S.p (S.i m')) :
    S.p (D.T (S.i m)) = S.p (D.T (S.i m')) := by
  rw [section_points_separate S m m' h]

#print axioms section_restriction_always

/-! ## Witness: toggle hidden bit preserves presented coordinate -/

inductive DynProv
  | toggleHidden
  | identity
  | leakHidden

def fstBool (q : Bool × Bool) : Bool :=
  q.1

def sectionFalse (a : Bool) : Bool × Bool :=
  (a, false)

def boolSplit : SplitPresentation (Bool × Bool) Bool where
  p := fstBool
  i := sectionFalse
  split := fun _ => rfl

def toggleHidden (q : Bool × Bool) : Bool × Bool :=
  (q.1, !q.2)

def toggleDyn : AmbientDynamics (Bool × Bool) DynProv where
  T := toggleHidden
  provenance := .toggleHidden

theorem toggle_preserves_p (q : Bool × Bool) :
    fstBool (toggleDyn.T q) = fstBool q :=
  rfl

#print axioms toggle_preserves_p

theorem toggle_hidden_congruent :
    FiberDynamicsCongruent fstBool toggleDyn := by
  intro x y h
  change fstBool (toggleHidden x) = fstBool (toggleHidden y)
  exact (fiberPD_zeroRel_iff fstBool x y).mp h

#print axioms toggle_hidden_congruent

theorem toggle_hidden_descends :
    ∃ F : ResidualQuotient (fiberSetoid fstBool) → Bool,
      ∀ q : Bool × Bool, F (classOf (fiberSetoid fstBool) q) = fstBool (toggleDyn.T q) :=
  (projectedFactor_exists_iff fstBool toggleDyn).mpr toggle_hidden_congruent

#print axioms toggle_hidden_descends

def idDyn : AmbientDynamics (Bool × Bool) DynProv where
  T := id
  provenance := .identity

theorem id_congruent :
    FiberDynamicsCongruent fstBool idDyn := by
  intro x y h
  exact (fiberPD_zeroRel_iff fstBool x y).mp h

#print axioms id_congruent

/-! ## Independence from leaving the selected section -/

theorem toggle_leaves_false_section :
    toggleDyn.T (boolSplit.i false) ≠ boolSplit.i false := by
  intro h
  cases h

#print axioms toggle_leaves_false_section

theorem id_stays_false_section :
    idDyn.T (boolSplit.i false) = boolSplit.i false :=
  rfl

#print axioms id_stays_false_section

theorem cong_independent_of_section_image :
    FiberDynamicsCongruent fstBool toggleDyn ∧
      FiberDynamicsCongruent fstBool idDyn ∧
      toggleDyn.T (boolSplit.i false) ≠ boolSplit.i false ∧
      idDyn.T (boolSplit.i false) = boolSplit.i false :=
  ⟨toggle_hidden_congruent, id_congruent,
    toggle_leaves_false_section, id_stays_false_section⟩

#print axioms cong_independent_of_section_image

/-! ## Falsifier: same fiber, different presented values after T -/

def leakHidden (q : Bool × Bool) : Bool × Bool :=
  (q.2, q.2)

def leakDyn : AmbientDynamics (Bool × Bool) DynProv where
  T := leakHidden
  provenance := .leakHidden

theorem same_fiber_ff_ft :
    ZeroRel (fiberPD fstBool) (false, false) (false, true) :=
  rfl

#print axioms same_fiber_ff_ft

theorem leak_splits_fiber :
    fstBool (leakDyn.T (false, false)) ≠ fstBool (leakDyn.T (false, true)) := by
  intro h
  cases h

#print axioms leak_splits_fiber

theorem leak_not_congruent :
    ¬ FiberDynamicsCongruent fstBool leakDyn := by
  intro h
  exact leak_splits_fiber (h (false, false) (false, true) same_fiber_ff_ft)

#print axioms leak_not_congruent

theorem leak_no_factor :
    ¬ ∃ F : ResidualQuotient (fiberSetoid fstBool) → Bool,
      ∀ q : Bool × Bool, F (classOf (fiberSetoid fstBool) q) = fstBool (leakDyn.T q) := by
  intro h
  exact leak_not_congruent ((projectedFactor_exists_iff fstBool leakDyn).mp h)

#print axioms leak_no_factor

/-- Section-only check holds for leakDyn, but fiber congruence fails. -/
theorem section_check_insufficient :
    (∀ m m' : Bool,
      boolSplit.p (boolSplit.i m) = boolSplit.p (boolSplit.i m') →
        boolSplit.p (leakDyn.T (boolSplit.i m)) =
          boolSplit.p (leakDyn.T (boolSplit.i m'))) ∧
      ¬ FiberDynamicsCongruent fstBool leakDyn :=
  ⟨section_restriction_always boolSplit leakDyn, leak_not_congruent⟩

#print axioms section_check_insufficient

end GrokPdNight20260814.E011
