/-
  E009 -- literal invariance of the chosen section.
  AuthorityEffect: None. Candidate only. Not estate E009. Not PROVEN.

  Target proposition
    T(i m) lies in the image of i exactly when T(i m) = P(T(i m)).
    This is equality-level. A coarse ZeroRel cannot replace equality.

  Imported carriers / ops / laws / finiteness / decidability
    L0: Type, Prop, Eq, Ne, Not, Prod, implication, Iff.
    L2: Bool.
    Dependencies: Core SplitPresentation / inducedP / AmbientDynamics
    (E004, E006, E007). Realization Zero is observational data.
    No Quotient, no descent claim, no observer-family, no metric,
    no Classical.choice.

  Positive finite witness
    Identity dynamics: T(i m) = i m, so T(i m) is literally i(m).

  Falsifier / negative control
    Toggle hidden bit: T(i false)=(false,true) is off-image, so
    literal invariance fails. Total Zero and fiber Zero still erase
    the pair, so observational invariance is not the same statement.

  Explicit nonclaims
    Literal invariance is stronger than observational zero residual.
    This is not E008 descent and not E011 fiber congruence.
    Estate E009 remains OPEN. Not PROVEN.
-/

import Core

namespace ProjectionFiber.E009

open ProjectionFiber.Core

def P {X M : Type} (S : SplitPresentation X M) : X → X :=
  inducedP S

def InImageI {X M : Type} (S : SplitPresentation X M) (x : X) : Prop :=
  ∃ m : M, S.i m = x

/-- Equality-level literal invariance at m. -/
def LiterallyInvariant {X M Prov : Type}
    (S : SplitPresentation X M) (D : AmbientDynamics X Prov) (m : M) : Prop :=
  D.T (S.i m) = P S (D.T (S.i m))

theorem literal_iff_in_image {X M Prov : Type}
    (S : SplitPresentation X M) (D : AmbientDynamics X Prov) (m : M) :
    LiterallyInvariant S D m ↔ InImageI S (D.T (S.i m)) := by
  constructor
  · intro h
    exact ⟨S.p (D.T (S.i m)), h.symm⟩
  · intro h
    rcases h with ⟨m', hm⟩
    change D.T (S.i m) = S.i (S.p (D.T (S.i m)))
    rw [← hm, S.split m']

#print axioms literal_iff_in_image

/-- Witness form: T(i m) = i m' for an explicit m'. -/
theorem literal_gives_explicit_section_point {X M Prov : Type}
    (S : SplitPresentation X M) (D : AmbientDynamics X Prov) (m : M)
    (h : LiterallyInvariant S D m) :
    ∃ m' : M, D.T (S.i m) = S.i m' :=
  ⟨S.p (D.T (S.i m)), h⟩

#print axioms literal_gives_explicit_section_point

/-! ## Witness: identity dynamics -/

def fstBool (q : Bool × Bool) : Bool :=
  q.1

def sectionFalse (a : Bool) : Bool × Bool :=
  (a, false)

def boolSplit : SplitPresentation (Bool × Bool) Bool where
  p := fstBool
  i := sectionFalse
  split := fun _ => rfl

inductive DynProv
  | identity
  | toggleHidden

def idDyn : AmbientDynamics (Bool × Bool) DynProv where
  T := id
  provenance := .identity

theorem id_literal (a : Bool) : LiterallyInvariant boolSplit idDyn a :=
  rfl

#print axioms id_literal

theorem id_hits_section (a : Bool) :
    idDyn.T (boolSplit.i a) = boolSplit.i a :=
  rfl

#print axioms id_hits_section

theorem id_in_image (a : Bool) :
    InImageI boolSplit (idDyn.T (boolSplit.i a)) :=
  (literal_iff_in_image boolSplit idDyn a).mp (id_literal a)

#print axioms id_in_image

/-! ## Falsifier: toggle leaves the section; coarse Zero erases -/

def toggleHidden (q : Bool × Bool) : Bool × Bool :=
  (q.1, !q.2)

def toggleDyn : AmbientDynamics (Bool × Bool) DynProv where
  T := toggleHidden
  provenance := .toggleHidden

theorem toggle_off_section :
    toggleDyn.T (boolSplit.i false) = (false, true) :=
  rfl

#print axioms toggle_off_section

theorem toggle_not_literal :
    ¬ LiterallyInvariant boolSplit toggleDyn false := by
  intro h
  cases h

#print axioms toggle_not_literal

theorem toggle_not_in_image :
    ¬ InImageI boolSplit (toggleDyn.T (boolSplit.i false)) := by
  intro h
  exact toggle_not_literal ((literal_iff_in_image boolSplit toggleDyn false).mpr h)

#print axioms toggle_not_in_image

def observationallyZero {X D : Type} (ρ : Realization X D) (x y : X) : Prop :=
  ρ.Zero (ρ.δ x y)

def totalResidual (X : Type) : Realization X (X × X) where
  δ x y := (x, y)
  Zero := fun _ => True

def fiberResidual {X M : Type} (p : X → M) : Realization X (X × X) where
  δ x y := (x, y)
  Zero := fun q => p q.1 = p q.2

def pairResidual (X : Type) : Realization X (X × X) where
  δ x y := (x, y)
  Zero := fun q => q.1 = q.2

theorem eq_zero_tracks_literal (a : Bool) :
    observationallyZero (pairResidual (Bool × Bool))
        (toggleDyn.T (boolSplit.i a))
        (P boolSplit (toggleDyn.T (boolSplit.i a))) ↔
      LiterallyInvariant boolSplit toggleDyn a :=
  Iff.rfl

#print axioms eq_zero_tracks_literal

theorem total_zero_erases_off_section :
    ¬ LiterallyInvariant boolSplit toggleDyn false ∧
      observationallyZero (totalResidual (Bool × Bool))
        (toggleDyn.T (boolSplit.i false))
        (P boolSplit (toggleDyn.T (boolSplit.i false))) :=
  ⟨toggle_not_literal, True.intro⟩

#print axioms total_zero_erases_off_section

theorem fiber_zero_erases_off_section :
    ¬ LiterallyInvariant boolSplit toggleDyn false ∧
      observationallyZero (fiberResidual fstBool)
        (toggleDyn.T (boolSplit.i false))
        (P boolSplit (toggleDyn.T (boolSplit.i false))) :=
  ⟨toggle_not_literal, rfl⟩

#print axioms fiber_zero_erases_off_section

/-- Coarse Zero cannot replace equality in the invariance statement. -/
theorem coarse_zero_is_not_literal :
    (¬ LiterallyInvariant boolSplit toggleDyn false) ∧
      observationallyZero (totalResidual (Bool × Bool))
        (toggleDyn.T (boolSplit.i false))
        (P boolSplit (toggleDyn.T (boolSplit.i false))) ∧
      observationallyZero (fiberResidual fstBool)
        (toggleDyn.T (boolSplit.i false))
        (P boolSplit (toggleDyn.T (boolSplit.i false))) :=
  ⟨toggle_not_literal, True.intro, rfl⟩

#print axioms coarse_zero_is_not_literal

end ProjectionFiber.E009
