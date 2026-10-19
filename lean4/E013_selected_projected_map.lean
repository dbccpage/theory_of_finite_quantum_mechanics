/-
  E013 -- selected projected map.
  AuthorityEffect: None. Candidate only. Not estate E013. Not PROVEN.

  Target proposition
    S = p ∘ T ∘ i is a well-typed endomap of M for every supplied
    split and T. Typing and section agreement only.

  Imported carriers / ops / laws / finiteness / decidability
    L0: Type, Prop, Eq, Ne, Prod, implication.
    L2: Bool.
    Campaign deps: Core SplitPresentation / AmbientDynamics (E004, E007).
    No Quotient, no fiber congruence hypothesis, no unique Tbar,
    no observer, metric, Classical.choice.

  Positive finite witness
    Bool split, toggle hidden. S a = a. Section agreement:
    S (p (i a)) = p (T (i a)).

  Falsifier / negative control
    Same split, leak-hidden T. Off-section x=(false,true) has
    S (p x) ≠ p (T x). S still exists as an endomap of Bool.

  Explicit nonclaims
    Existence of S is not descent. S need not equal the descended
    factor of p ∘ T (E012). Estate E013 remains OPEN. Not PROVEN.
-/

import Core

namespace GrokPdNight20260814.E013

open GrokPdNight20260814.Core

/-- Selected projected map. Defined for every split and T. -/
def selectedS {X M Prov : Type}
    (S : SplitPresentation X M) (D : AmbientDynamics X Prov) : M → M :=
  fun m => S.p (D.T (S.i m))

theorem selectedS_section_agreement {X M Prov : Type}
    (Splt : SplitPresentation X M) (D : AmbientDynamics X Prov) (m : M) :
    selectedS Splt D (Splt.p (Splt.i m)) = Splt.p (D.T (Splt.i m)) := by
  rw [Splt.split m]
  rfl

#print axioms selectedS_section_agreement

/-! ## Witness: Bool split, toggle hidden. S is id. -/

inductive DynProv
  | toggleHidden
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

theorem toggle_S_formula (a : Bool) :
    selectedS boolSplit toggleDyn a = a :=
  rfl

#print axioms toggle_S_formula

theorem toggle_S_section_agrees (a : Bool) :
    selectedS boolSplit toggleDyn (boolSplit.p (boolSplit.i a)) =
      boolSplit.p (toggleDyn.T (boolSplit.i a)) :=
  selectedS_section_agreement boolSplit toggleDyn a

#print axioms toggle_S_section_agrees

theorem toggle_witness :
    (∀ a : Bool, selectedS boolSplit toggleDyn a = a) ∧
      selectedS boolSplit toggleDyn false = false ∧
      selectedS boolSplit toggleDyn true = true :=
  ⟨toggle_S_formula, rfl, rfl⟩

#print axioms toggle_witness

/-! ## Falsifier: S exists, but S(p x) ≠ p(T x) off the section -/

def leakHidden (q : Bool × Bool) : Bool × Bool :=
  (q.2, q.2)

def leakDyn : AmbientDynamics (Bool × Bool) DynProv where
  T := leakHidden
  provenance := .leakHidden

def offSection : Bool × Bool :=
  (false, true)

theorem leak_S_const_false (a : Bool) :
    selectedS boolSplit leakDyn a = false :=
  rfl

#print axioms leak_S_const_false

theorem leak_off_section_disagrees :
    selectedS boolSplit leakDyn (fstBool offSection) ≠
      fstBool (leakDyn.T offSection) := by
  intro h
  cases h

#print axioms leak_off_section_disagrees

theorem same_fiber_off_section :
    fstBool offSection = fstBool (false, false) :=
  rfl

#print axioms same_fiber_off_section

/-- S is still a well-typed endomap of M when congruence fails. -/
theorem leak_S_exists_without_descent :
    (∀ a : Bool, selectedS boolSplit leakDyn a = false) ∧
      selectedS boolSplit leakDyn (fstBool offSection) ≠
        fstBool (leakDyn.T offSection) :=
  ⟨leak_S_const_false, leak_off_section_disagrees⟩

#print axioms leak_S_exists_without_descent

/-- Existence of S is not a descent statement. -/
theorem S_is_not_descent :
    selectedS boolSplit leakDyn false = false ∧
      fstBool (leakDyn.T offSection) = true :=
  ⟨rfl, rfl⟩

#print axioms S_is_not_descent

end GrokPdNight20260814.E013
