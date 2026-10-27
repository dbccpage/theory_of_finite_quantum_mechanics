/-
  E012 -- unique descended dynamics iff fiber congruence.
  AuthorityEffect: None. Candidate only. Not estate E012. Not PROVEN.

  Target proposition
    There exists a unique Tbar : M → M with Tbar ∘ p = p ∘ T exactly
    when T preserves p-fibers, provided p is surjective (a section
    supplies that). Without a section, uniqueness holds only on im p.

  Imported carriers / ops / laws / finiteness / decidability
    L0: Type, Prop, Eq, Ne, Iff, Prod, implication.
    L2: Bool, Unit.
    Dependencies: Core SplitPresentation / AmbientDynamics;
    E011 FiberDynamicsCongruent; E013 selectedS as the witness Tbar;
    E005 only for the surjectivity/image distinction (no new quotient).
    No observer, metric, Classical.choice.

  Positive finite witness
    Bool split + toggle. Tbar = selectedS = id. Unique.

  Falsifier / negative control
    Bool split + leak: congruence fails, no Tbar.
    constFalse : Unit → Bool, T = id: congruence holds; const-false
    and id both extend the image factor; global uniqueness fails.

  Explicit nonclaims
    An existential factor through im p is not a unique total factor
    on an arbitrary codomain. Estate E012 remains OPEN. Not PROVEN.
-/

import Core
import FiberDynamicsCongruence
import SelectedProjectedMap

namespace ProjectionFiber.E012

open ProjectionFiber.Core
open ProjectionFiber.E011 (FiberDynamicsCongruent fiber_dynamics_congruent_iff)
open ProjectionFiber.E013 (selectedS)

def AgreesOnImage {X M Prov : Type}
    (p : X → M) (D : AmbientDynamics X Prov) (Tbar : M → M) : Prop :=
  ∀ x : X, Tbar (p x) = p (D.T x)

/-- Image-local uniqueness: no section required. -/
theorem unique_on_image {X M Prov : Type}
    (p : X → M) (D : AmbientDynamics X Prov)
    (T1 T2 : M → M)
    (h1 : AgreesOnImage p D T1) (h2 : AgreesOnImage p D T2)
    (m : M) (hm : ∃ x : X, p x = m) :
    T1 m = T2 m := by
  rcases hm with ⟨x, hx⟩
  rw [← hx, h1 x, h2 x]

#print axioms unique_on_image

/-- Existence of some Tbar agreeing on im p implies fiber congruence. -/
theorem agrees_implies_congruent {X M Prov : Type}
    (p : X → M) (D : AmbientDynamics X Prov) (Tbar : M → M)
    (h : AgreesOnImage p D Tbar) :
    FiberDynamicsCongruent p D := by
  intro x y hxy
  calc
    p (D.T x) = Tbar (p x) := (h x).symm
    _ = Tbar (p y) := by
      have : p x = p y := (ProjectionFiber.E003.fiberPD_zeroRel_iff p x y).mp hxy
      rw [this]
    _ = p (D.T y) := h y

#print axioms agrees_implies_congruent

/-- With a split, selectedS agrees on the whole of M's preimage. -/
theorem selectedS_agrees_of_congruent {X M Prov : Type}
    (S : SplitPresentation X M) (D : AmbientDynamics X Prov)
    (h : FiberDynamicsCongruent S.p D) :
    AgreesOnImage S.p D (selectedS S D) := by
  intro x
  have hfib : S.p x = S.p (S.i (S.p x)) := (S.split (S.p x)).symm
  have : S.p (D.T x) = S.p (D.T (S.i (S.p x))) :=
    (fiber_dynamics_congruent_iff S.p D).mp h x (S.i (S.p x)) hfib
  exact this.symm

#print axioms selectedS_agrees_of_congruent

theorem selectedS_unique_on_M {X M Prov : Type}
    (S : SplitPresentation X M) (D : AmbientDynamics X Prov)
    (Tbar : M → M) (h : AgreesOnImage S.p D Tbar) (m : M) :
    Tbar m = selectedS S D m := by
  have : Tbar (S.p (S.i m)) = S.p (D.T (S.i m)) := h (S.i m)
  rw [S.split m] at this
  exact this

#print axioms selectedS_unique_on_M

/-- Ceiling, with a split: unique total Tbar iff fiber congruence. -/
theorem unique_Tbar_iff_congruent {X M Prov : Type}
    (S : SplitPresentation X M) (D : AmbientDynamics X Prov) :
    (∃ Tbar : M → M, AgreesOnImage S.p D Tbar ∧
        ∀ T' : M → M, AgreesOnImage S.p D T' → T' = Tbar) ↔
      FiberDynamicsCongruent S.p D := by
  constructor
  · intro h
    rcases h with ⟨Tbar, hA, _⟩
    exact agrees_implies_congruent S.p D Tbar hA
  · intro h
    refine ⟨selectedS S D, selectedS_agrees_of_congruent S D h, ?_⟩
    intro T' hT'
    funext m
    exact selectedS_unique_on_M S D T' hT' m

#print axioms unique_Tbar_iff_congruent

/-! ## Witness: Bool split + toggle. Tbar = id. -/

def fstBool (q : Bool × Bool) : Bool :=
  q.1

def sectionFalse (a : Bool) : Bool × Bool :=
  (a, false)

def boolSplit : SplitPresentation (Bool × Bool) Bool where
  p := fstBool
  i := sectionFalse
  split := fun _ => rfl

inductive DynProv
  | toggleHidden
  | leakHidden
  | identity

def toggleHidden (q : Bool × Bool) : Bool × Bool :=
  (q.1, !q.2)

def toggleDyn : AmbientDynamics (Bool × Bool) DynProv where
  T := toggleHidden
  provenance := .toggleHidden

theorem toggle_congruent :
    FiberDynamicsCongruent fstBool toggleDyn := by
  intro x y hxy
  exact (ProjectionFiber.E003.fiberPD_zeroRel_iff fstBool x y).mp hxy

#print axioms toggle_congruent

theorem toggle_Tbar_is_id (a : Bool) :
    selectedS boolSplit toggleDyn a = a :=
  rfl

#print axioms toggle_Tbar_is_id

theorem toggle_unique_Tbar :
    ∃ Tbar : Bool → Bool, AgreesOnImage fstBool toggleDyn Tbar ∧
      ∀ T' : Bool → Bool, AgreesOnImage fstBool toggleDyn T' → T' = Tbar :=
  (unique_Tbar_iff_congruent boolSplit toggleDyn).mpr toggle_congruent

#print axioms toggle_unique_Tbar

/-! ## Falsifier 1: leak, congruence fails, no Tbar -/

def leakHidden (q : Bool × Bool) : Bool × Bool :=
  (q.2, q.2)

def leakDyn : AmbientDynamics (Bool × Bool) DynProv where
  T := leakHidden
  provenance := .leakHidden

theorem leak_not_congruent :
    ¬ FiberDynamicsCongruent fstBool leakDyn := by
  intro h
  have : fstBool (leakDyn.T (false, false)) = fstBool (leakDyn.T (false, true)) :=
    (fiber_dynamics_congruent_iff fstBool leakDyn).mp h (false, false) (false, true) rfl
  cases this

#print axioms leak_not_congruent

theorem leak_no_Tbar :
    ¬ ∃ Tbar : Bool → Bool, AgreesOnImage fstBool leakDyn Tbar := by
  intro h
  rcases h with ⟨Tbar, hA⟩
  exact leak_not_congruent (agrees_implies_congruent fstBool leakDyn Tbar hA)

#print axioms leak_no_Tbar

/-! ## Falsifier 2: nonsurjective p, two total extensions -/

def constFalse : Unit → Bool :=
  fun _ => false

def idUnit : AmbientDynamics Unit Unit where
  T := id
  provenance := ()

theorem constFalse_congruent :
    FiberDynamicsCongruent constFalse idUnit := by
  intro x y _
  rfl

#print axioms constFalse_congruent

def extConst : Bool → Bool :=
  fun _ => false

def extId : Bool → Bool :=
  id

theorem both_extend_image :
    AgreesOnImage constFalse idUnit extConst ∧
      AgreesOnImage constFalse idUnit extId :=
  ⟨fun _ => rfl, fun _ => rfl⟩

#print axioms both_extend_image

theorem extensions_disagree :
    extConst ≠ extId := by
  intro h
  have : false = true := congrArg (fun f => f true) h
  cases this

#print axioms extensions_disagree

theorem no_unique_total_without_section :
    FiberDynamicsCongruent constFalse idUnit ∧
      AgreesOnImage constFalse idUnit extConst ∧
      AgreesOnImage constFalse idUnit extId ∧
      extConst ≠ extId :=
  ⟨constFalse_congruent, both_extend_image.1, both_extend_image.2,
    extensions_disagree⟩

#print axioms no_unique_total_without_section

/-- They still agree on im p. -/
theorem unique_on_image_constFalse (T1 T2 : Bool → Bool)
    (h1 : AgreesOnImage constFalse idUnit T1)
    (h2 : AgreesOnImage constFalse idUnit T2) :
    T1 false = T2 false :=
  unique_on_image constFalse idUnit T1 T2 h1 h2 false ⟨(), rfl⟩

#print axioms unique_on_image_constFalse

end ProjectionFiber.E012
