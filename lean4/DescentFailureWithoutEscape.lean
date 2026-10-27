/-
  E018 -- countermodel: descent failure without section escape.
  AuthorityEffect: None. Candidate only. Not estate E018. Not PROVEN.

  Target proposition
    T can fix every selected point i(m) while failing to preserve
    p-fibers off the section. Escape and selected S are zero;
    no descended Tbar exists.

  Imported carriers / ops / laws / finiteness / decidability
    L0: Type, Prop, Eq, Ne, Prod, implication.
    L2: Bool.
    Dependencies: Core SplitPresentation / AmbientDynamics;
    E008 literalEscape; E009 LiterallyInvariant; E011
    FiberDynamicsCongruent; E013 selectedS. No observer, metric,
    Classical.choice.

  Positive finite witness
    T(a,false)=(a,false), T(a,true)=(!a,true). Every i(m) is fixed.

  Falsifier / negative control
    (false,false) and (false,true) are one fiber and land on
    different presented values, so no Tbar.

  Explicit nonclaims
    Testing only selected representatives cannot certify descent.
    Estate E018 remains OPEN. Not PROVEN.
-/

import Core
import ProjectionEscapeResidual
import LiteralInvariance
import FiberDynamicsCongruence
import UniqueDescendedDynamics
import SelectedProjectedMap

namespace ProjectionFiber.E018

open ProjectionFiber.Core
open ProjectionFiber.E008 (literalEscape escapeSrc escapeDst)
open ProjectionFiber.E009 (LiterallyInvariant)
open ProjectionFiber.E011 (FiberDynamicsCongruent fiber_dynamics_congruent_iff)
open ProjectionFiber.E012 (AgreesOnImage)
open ProjectionFiber.E013 (selectedS)

def fstBool (q : Bool × Bool) : Bool :=
  q.1

def sectionFalse (a : Bool) : Bool × Bool :=
  (a, false)

def boolSplit : SplitPresentation (Bool × Bool) Bool where
  p := fstBool
  i := sectionFalse
  split := fun _ => rfl

/-- Spec T: fix the section; flip the presented bit off-section. -/
def fixSectionFlipHidden (q : Bool × Bool) : Bool × Bool :=
  (if q.2 then !q.1 else q.1, q.2)

inductive DynProv
  | fixSection

def fixDyn : AmbientDynamics (Bool × Bool) DynProv where
  T := fixSectionFlipHidden
  provenance := .fixSection

theorem T_on_section (a : Bool) :
    fixDyn.T (boolSplit.i a) = boolSplit.i a :=
  rfl

#print axioms T_on_section

theorem T_off_section (a : Bool) :
    fixDyn.T (a, true) = (!a, true) :=
  rfl

#print axioms T_off_section

/-! ## Witness: no escape, S = id -/

theorem no_literal_escape (a : Bool) :
    ¬ literalEscape boolSplit fixDyn a := by
  intro h
  exact h rfl

#print axioms no_literal_escape

theorem literally_invariant (a : Bool) :
    LiterallyInvariant boolSplit fixDyn a :=
  rfl

#print axioms literally_invariant

theorem S_is_id (a : Bool) :
    selectedS boolSplit fixDyn a = a :=
  rfl

#print axioms S_is_id

theorem section_check_vacuous (a b : Bool)
    (h : boolSplit.p (boolSplit.i a) = boolSplit.p (boolSplit.i b)) :
    boolSplit.p (fixDyn.T (boolSplit.i a)) =
      boolSplit.p (fixDyn.T (boolSplit.i b)) := by
  rw [T_on_section a, T_on_section b]
  exact h

#print axioms section_check_vacuous

/-! ## Falsifier: same fiber, different p ∘ T; no Tbar -/

theorem same_fiber_ff_ft :
    fstBool (false, false) = fstBool (false, true) :=
  rfl

#print axioms same_fiber_ff_ft

theorem splits_fiber :
    fstBool (fixDyn.T (false, false)) ≠ fstBool (fixDyn.T (false, true)) := by
  intro h
  cases h

#print axioms splits_fiber

theorem not_congruent :
    ¬ FiberDynamicsCongruent fstBool fixDyn := by
  intro h
  exact splits_fiber
    ((fiber_dynamics_congruent_iff fstBool fixDyn).mp h
      (false, false) (false, true) rfl)

#print axioms not_congruent

theorem no_tbar :
    ¬ ∃ Tbar : Bool → Bool, AgreesOnImage fstBool fixDyn Tbar := by
  intro h
  rcases h with ⟨Tbar, hA⟩
  have h1 : Tbar false = fstBool (fixDyn.T (false, false)) := hA (false, false)
  have h2 : Tbar false = fstBool (fixDyn.T (false, true)) := hA (false, true)
  have : fstBool (fixDyn.T (false, false)) = fstBool (fixDyn.T (false, true)) :=
    h1.symm.trans h2
  exact splits_fiber this

#print axioms no_tbar

/-- Section fixation + zero S is not descent. -/
theorem section_fixation_not_descent :
    (∀ a : Bool, fixDyn.T (boolSplit.i a) = boolSplit.i a) ∧
      (∀ a : Bool, selectedS boolSplit fixDyn a = a) ∧
      ¬ FiberDynamicsCongruent fstBool fixDyn ∧
      ¬ ∃ Tbar : Bool → Bool, AgreesOnImage fstBool fixDyn Tbar :=
  ⟨T_on_section, S_is_id, not_congruent, no_tbar⟩

#print axioms section_fixation_not_descent

end ProjectionFiber.E018
