/-
  E008 -- projection escape residual.
  AuthorityEffect: None. Candidate only. Not estate E008. Not PROVEN.

  Target proposition
    At m, the residual compares T(i m) with P(T(i m)). Observational
    Zero need not be equality. Obstruction means Zero does not erase
    that pair. The two endpoints and the presentation are retained.

  Imported carriers / ops / laws / finiteness / decidability
    L0: Type, Prop, Eq, Ne, Prod, Not, Iff, implication.
    L2: Bool.
    Campaign deps: E004 split, E006 P=i∘p, E007 named T,
    B008 only as named-Zero reminder (not a quotient here).
    No Quotient construction, no descent claim, no observer family,
    no metric, no Classical.choice.

  Positive finite witness
    Bool split, toggle hidden bit. T(i false)=(false,true),
    P of that is (false,false). Equality-Zero does not erase.

  Falsifier / negative control
    Same motion, total Zero: residual is observationally zero.
    Same pair is always p-related, so fiber-Zero also erases
    literal off-section motion.

  Explicit nonclaims
    Nonzero escape is not yet failure of dynamics to descend through p.
    Estate E008 remains OPEN. Not PROVEN.
-/

import Core

namespace GrokPdNight20260814.E008

open GrokPdNight20260814.Core

def P {X M : Type} (S : SplitPresentation X M) : X → X :=
  inducedP S

def escapeSrc {X M Prov : Type}
    (S : SplitPresentation X M) (D : AmbientDynamics X Prov) (m : M) : X :=
  D.T (S.i m)

def escapeDst {X M Prov : Type}
    (S : SplitPresentation X M) (D : AmbientDynamics X Prov) (m : M) : X :=
  P S (D.T (S.i m))

def pairResidual (X : Type) : Realization X (X × X) where
  δ x y := (x, y)
  Zero := fun q => q.1 = q.2

def totalResidual (X : Type) : Realization X (X × X) where
  δ x y := (x, y)
  Zero := fun _ => True

def fiberResidual {X M : Type} (p : X → M) : Realization X (X × X) where
  δ x y := (x, y)
  Zero := fun q => p q.1 = p q.2

def observationallyZero {X Cod : Type} (ρ : Realization X Cod)
    (x y : X) : Prop :=
  ρ.Zero (ρ.δ x y)

def escapeErased {X M Prov Cod : Type}
    (S : SplitPresentation X M) (D : AmbientDynamics X Prov)
    (ρ : Realization X Cod) (m : M) : Prop :=
  observationallyZero ρ (escapeSrc S D m) (escapeDst S D m)

def literalEscape {X M Prov : Type}
    (S : SplitPresentation X M) (D : AmbientDynamics X Prov) (m : M) : Prop :=
  escapeSrc S D m ≠ escapeDst S D m

theorem dest_is_P_src {X M Prov : Type}
    (S : SplitPresentation X M) (D : AmbientDynamics X Prov) (m : M) :
    escapeDst S D m = P S (escapeSrc S D m) :=
  rfl

#print axioms dest_is_P_src

/-- The escape pair always lies in one p-fiber. -/
theorem escape_same_fiber {X M Prov : Type}
    (S : SplitPresentation X M) (D : AmbientDynamics X Prov) (m : M) :
    S.p (escapeSrc S D m) = S.p (escapeDst S D m) := by
  change S.p (D.T (S.i m)) = S.p (S.i (S.p (D.T (S.i m))))
  rw [S.split (S.p (D.T (S.i m)))]

#print axioms escape_same_fiber

/-- Equality-Zero erases the residual exactly when there is no literal escape. -/
theorem eq_zero_iff_endpoints_eq {X M Prov : Type}
    (S : SplitPresentation X M) (D : AmbientDynamics X Prov) (m : M) :
    escapeErased S D (pairResidual X) m ↔
      escapeSrc S D m = escapeDst S D m :=
  Iff.rfl

#print axioms eq_zero_iff_endpoints_eq

/-! ## Witness: Bool split, toggle hidden -/

inductive DynProv
  | toggleHidden

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

theorem src_false : escapeSrc boolSplit toggleDyn false = (false, true) :=
  rfl

#print axioms src_false

theorem dst_false : escapeDst boolSplit toggleDyn false = (false, false) :=
  rfl

#print axioms dst_false

theorem literal_escape_false :
    literalEscape boolSplit toggleDyn false := by
  intro h
  cases h

#print axioms literal_escape_false

theorem eq_zero_does_not_erase :
    ¬ escapeErased boolSplit toggleDyn (pairResidual (Bool × Bool)) false :=
  literal_escape_false

#print axioms eq_zero_does_not_erase

theorem endpoints_retained :
    escapeSrc boolSplit toggleDyn false = (false, true) ∧
      escapeDst boolSplit toggleDyn false = (false, false) ∧
      boolSplit.p (false, true) = false ∧
      boolSplit.p (false, false) = false :=
  ⟨rfl, rfl, rfl, rfl⟩

#print axioms endpoints_retained

/-! ## Falsifier: total Zero erases the same literal motion -/

theorem total_erases_despite_literal :
    literalEscape boolSplit toggleDyn false ∧
      escapeErased boolSplit toggleDyn (totalResidual (Bool × Bool)) false :=
  ⟨literal_escape_false, True.intro⟩

#print axioms total_erases_despite_literal

/-- Fiber-Zero also erases: the pair is always same-fiber. -/
theorem fiber_zero_erases :
    literalEscape boolSplit toggleDyn false ∧
      escapeErased boolSplit toggleDyn (fiberResidual fstBool) false :=
  ⟨literal_escape_false, escape_same_fiber boolSplit toggleDyn false⟩

#print axioms fiber_zero_erases

/-- Class-equality characterization on the Bool fixture. -/
theorem class_eq_char :
    ¬ escapeErased boolSplit toggleDyn (pairResidual (Bool × Bool)) false ∧
      escapeErased boolSplit toggleDyn (fiberResidual fstBool) false ∧
      escapeErased boolSplit toggleDyn (totalResidual (Bool × Bool)) false :=
  ⟨eq_zero_does_not_erase, fiber_zero_erases.2, total_erases_despite_literal.2⟩

#print axioms class_eq_char

/-- Escape is not a descent statement. Same T may or may not preserve
    fibers off-section; this module does not mention fiber congruence. -/
theorem escape_is_not_descent :
    literalEscape boolSplit toggleDyn false ∧
      fstBool (toggleHidden (false, true)) = fstBool (false, true) :=
  ⟨literal_escape_false, rfl⟩

#print axioms escape_is_not_descent

end GrokPdNight20260814.E008
