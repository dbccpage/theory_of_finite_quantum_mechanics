/-
  E005 -- identify the fiber quotient with the presented carrier.
  AuthorityEffect: None. Candidate only. Not estate E005. Not PROVEN.

  Target proposition
    Given a SplitPresentation p, i with p ∘ i = id, the quotient of X
    by p-fiber equality is equivalent to M via [x] ↦ p x and
    m ↦ [i m]. The inverse uses the supplied i; no other section
    is chosen.

  Imported carriers / ops / laws / finiteness / decidability
    L0: Type, Prop, Eq, Ne, Iff, Prod, implication.
    L1: Quotient, Setoid, Quotient.mk / sound / exact / lift / inductionOn.
    L2: Bool, Unit.
    Dependencies: E003 fiber relation p x = p y, E004 SplitPresentation.
    No observer, metric, dynamics, Classical.choice.

  Positive finite witness
    Bool×Bool first-coordinate split. [ (false,true) ] and
    [ (false,false) ] both map to false.

  Falsifier / negative control
    constFalse : Unit → Bool has a fiber quotient of one point and
    no section. It cannot be equivalent to Bool.

  Explicit nonclaims
    This equivalence is relative to the supplied presentation, not a
    canonical presentation of X. Estate E005 remains OPEN. Not PROVEN.
    Quot.sound / propext, if reported, are Lean L1.
-/

import Core
import ProjectionFiberPrimitiveDifference

namespace ProjectionFiber.E005

open ProjectionFiber.Core

def fiberSetoid {X M : Type} (p : X → M) : Setoid X where
  r := fun x y => p x = p y
  iseqv := {
    refl := fun _ => rfl
    symm := fun h => h.symm
    trans := fun h1 h2 => h1.trans h2
  }

theorem quotient_eq_iff_report_eq {X Q : Type} (pres : X → Q) (x y : X) :
    Quotient.mk (fiberSetoid pres) x = Quotient.mk (fiberSetoid pres) y ↔ pres x = pres y := by
  constructor
  · intro h; exact Quotient.exact h
  · intro h; apply Quotient.sound; exact h

#print axioms quotient_eq_iff_report_eq

/-- Forward: classes to the presented carrier. Well-defined by fiber equality. -/
def toM {X M : Type} (p : X → M) : ResidualQuotient (fiberSetoid p) → M :=
  Quotient.lift p (fun _ _ h => h)

theorem toM_classOf {X M : Type} (p : X → M) (x : X) :
    toM p (classOf (fiberSetoid p) x) = p x :=
  rfl

#print axioms toM_classOf

/-- Inverse: uses the *supplied* section only. -/
def toQ {X M : Type} (S : SplitPresentation X M) (m : M) :
    ResidualQuotient (fiberSetoid S.p) :=
  classOf (fiberSetoid S.p) (S.i m)

theorem toM_toQ {X M : Type} (S : SplitPresentation X M) (m : M) :
    toM S.p (toQ S m) = m := by
  change S.p (S.i m) = m
  exact S.split m

#print axioms toM_toQ

theorem toQ_toM {X M : Type} (S : SplitPresentation X M)
    (q : ResidualQuotient (fiberSetoid S.p)) :
    toQ S (toM S.p q) = q := by
  refine Quotient.inductionOn q ?_
  intro x
  change classOf (fiberSetoid S.p) (S.i (S.p x)) = classOf (fiberSetoid S.p) x
  apply Quotient.sound
  change S.p (S.i (S.p x)) = S.p x
  rw [S.split (S.p x)]

#print axioms toQ_toM

/-! ## Witness: Bool × Bool first-coordinate split -/

def fstBool (q : Bool × Bool) : Bool :=
  q.1

def sectionFalse (a : Bool) : Bool × Bool :=
  (a, false)

def boolSplit : SplitPresentation (Bool × Bool) Bool where
  p := fstBool
  i := sectionFalse
  split := fun _ => rfl

theorem witness_classes_agree :
    classOf (fiberSetoid fstBool) (false, true) = classOf (fiberSetoid fstBool) (false, false) :=
  (classOf_eq_iff (fiberSetoid fstBool) (false, true) (false, false)).mpr rfl

#print axioms witness_classes_agree

theorem witness_toM :
    toM fstBool (classOf (fiberSetoid fstBool) (false, true)) = false :=
  rfl

#print axioms witness_toM

theorem witness_toQ :
    toQ boolSplit false = classOf (fiberSetoid fstBool) (false, false) :=
  rfl

#print axioms witness_toQ

theorem witness_both_laws (a : Bool) (q : Bool × Bool) :
    toM fstBool (toQ boolSplit a) = a ∧
      toQ boolSplit (toM fstBool (classOf (fiberSetoid fstBool) q)) =
        classOf (fiberSetoid fstBool) q :=
  ⟨toM_toQ boolSplit a, toQ_toM boolSplit (classOf (fiberSetoid fstBool) q)⟩

#print axioms witness_both_laws

/-! ## Falsifier: nonsurjective p, no section, not equivalent to M -/

def constFalse : Unit → Bool :=
  fun _ => false

theorem constFalse_not_surjective :
    ¬ ∀ b : Bool, ∃ u : Unit, constFalse u = b := by
  intro h
  rcases h true with ⟨_, ht⟩
  cases ht

#print axioms constFalse_not_surjective

/-- A map ResidualQuotient (fiberSetoid constFalse) → Bool cannot be surjective:
    the domain is a singleton. -/
theorem unit_fiber_quotient_subsingleton
    (q1 q2 : ResidualQuotient (fiberSetoid constFalse)) : q1 = q2 := by
  refine Quotient.inductionOn₂ q1 q2 ?_
  intro x y
  apply Quotient.sound
  rfl

#print axioms unit_fiber_quotient_subsingleton

theorem no_equiv_to_bool :
    ¬ ∃ f : ResidualQuotient (fiberSetoid constFalse) → Bool,
      ∃ g : Bool → ResidualQuotient (fiberSetoid constFalse),
        (∀ b : Bool, f (g b) = b) := by
  intro h
  rcases h with ⟨f, g, hf⟩
  have hft : f (g false) = false := hf false
  have htt : f (g true) = true := hf true
  have same : g false = g true :=
    unit_fiber_quotient_subsingleton (g false) (g true)
  have : false = true := by
    calc
      false = f (g false) := hft.symm
      _ = f (g true) := congrArg f same
      _ = true := htt
  cases this

#print axioms no_equiv_to_bool

/-- Relative, not canonical: two sections of the same p land in one class. -/
def sectionTrue (a : Bool) : Bool × Bool :=
  (a, true)

def boolSplitTrue : SplitPresentation (Bool × Bool) Bool where
  p := fstBool
  i := sectionTrue
  split := fun _ => rfl

theorem sections_themselves_differ :
    boolSplit.i false ≠ boolSplitTrue.i false := by
  intro h
  cases h

#print axioms sections_themselves_differ

theorem two_sections_same_class :
    toQ boolSplit false = toQ boolSplitTrue false :=
  (classOf_eq_iff (fiberSetoid fstBool) (false, false) (false, true)).mpr rfl

#print axioms two_sections_same_class

/-- The equivalence uses i only through its class. i is not recovered. -/
theorem i_not_recovered_from_toQ :
    toQ boolSplit false = toQ boolSplitTrue false ∧
      boolSplit.i false ≠ boolSplitTrue.i false :=
  ⟨two_sections_same_class, sections_themselves_differ⟩

#print axioms i_not_recovered_from_toQ

end ProjectionFiber.E005
