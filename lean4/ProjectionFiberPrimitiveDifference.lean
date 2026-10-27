/-
  E003 -- projection-fiber primitive difference.
  AuthorityEffect: None. Candidate only. Not estate E003. Not PROVEN.

  Target proposition
    For a supplied p : X → M, δ(x,y)=(x,y) and Zero(x,y) iff p x = p y
    give ZeroRel exactly the p-fiber relation. No section is used.

  Imported carriers / ops / laws / finiteness / decidability
    L0: Type, Prop, Eq, Ne, Iff, Prod, implication.
    L2: Bool.
    Dependencies: B008 (named Setoid / class map exist; not invoked
    as a presentation here), B004 Realization, B005 law hypotheses,
    E001 pair residual restated. Shared-kernel PrimitiveDifference
    is READ-ONLY evidence; not imported.
    No Quotient, section, retraction, observer, metric, addition,
    graph, or Classical.choice.

  Positive finite witness
    p(a,b)=a on Bool×Bool. Same first coordinate iff ZeroRel.
    (false,false)~(false,true); (false,false) not related to
    (true,false). The three laws hold.

  Falsifier / negative control
    snd on the same carrier: (false,false) and (false,true) are
    fst-related and not snd-related. Changing p changes classes.

  Explicit nonclaims
    A presentation map is supplied, not derived from raw difference.
    This is not a split, not a section, not classOf (E024), and not
    unique descended dynamics. Estate E003 remains OPEN. Not PROVEN.
-/

import Core

namespace ProjectionFiber.E003

open ProjectionFiber.Core

/-- Pair residual whose Zero is equality after a supplied presentation. -/
def fiberResidual {X M : Type} (p : X → M) : Realization X (X × X) where
  δ x y := (x, y)
  Zero := fun q => p q.1 = p q.2

def fiberRel {X M : Type} (p : X → M) (x y : X) : Prop :=
  p x = p y

theorem fiber_zeroRel_iff {X M : Type} (p : X → M) (x y : X) :
    zeroRel (fiberResidual p) x y ↔ p x = p y :=
  Iff.rfl

#print axioms fiber_zeroRel_iff

theorem fiber_realizes {X M : Type} (p : X → M) :
    Realizes (fiberRel p) (fiberResidual p) :=
  fun _ _ => Iff.rfl

#print axioms fiber_realizes

theorem fiber_refl {X M : Type} (p : X → M) : HasRefl (fiberResidual p) :=
  fun _ => rfl

#print axioms fiber_refl

theorem fiber_symm {X M : Type} (p : X → M) : HasSymm (fiberResidual p) :=
  fun _ _ h => h.symm

#print axioms fiber_symm

theorem fiber_trans {X M : Type} (p : X → M) : HasTrans (fiberResidual p) :=
  fun _ _ _ h1 h2 => h1.trans h2

#print axioms fiber_trans

def fiberPD {X M : Type} (p : X → M) : PrimitiveDifference X (X × X) :=
  ofRealization (fiberResidual p) (fiber_refl p) (fiber_symm p) (fiber_trans p)

theorem fiberPD_zeroRel_iff {X M : Type} (p : X → M) (x y : X) :
    ZeroRel (fiberPD p) x y ↔ p x = p y :=
  Iff.rfl

#print axioms fiberPD_zeroRel_iff

/-! ## Witness: first projection on Bool × Bool -/

def fstBool : Bool × Bool → Bool :=
  fun q => q.1

def sndBool : Bool × Bool → Bool :=
  fun q => q.2

def ff : Bool × Bool := (false, false)
def ft : Bool × Bool := (false, true)
def tf : Bool × Bool := (true, false)

theorem fst_relates_same_first :
    zeroRel (fiberResidual fstBool) ff ft :=
  rfl

#print axioms fst_relates_same_first

theorem fst_separates_different_first :
    ¬ zeroRel (fiberResidual fstBool) ff tf := by
  intro h
  cases h

#print axioms fst_separates_different_first

theorem fst_witness :
    Realizes (fiberRel fstBool) (fiberResidual fstBool) ∧
      HasRefl (fiberResidual fstBool) ∧
      HasSymm (fiberResidual fstBool) ∧
      HasTrans (fiberResidual fstBool) ∧
      zeroRel (fiberResidual fstBool) ff ft ∧
      ¬ zeroRel (fiberResidual fstBool) ff tf :=
  ⟨fiber_realizes fstBool, fiber_refl fstBool, fiber_symm fstBool,
    fiber_trans fstBool, fst_relates_same_first, fst_separates_different_first⟩

#print axioms fst_witness

/-! ## Falsifier: snd on the same carrier changes the classes -/

theorem snd_not_ff_ft :
    ¬ zeroRel (fiberResidual sndBool) ff ft := by
  intro h
  cases h

#print axioms snd_not_ff_ft

theorem snd_relates_ff_tf :
    zeroRel (fiberResidual sndBool) ff tf :=
  rfl

#print axioms snd_relates_ff_tf

/-- Same carrier, two presentations, two different fiber relations. -/
theorem different_p_different_classes :
    zeroRel (fiberResidual fstBool) ff ft ∧
      ¬ zeroRel (fiberResidual sndBool) ff ft ∧
      ¬ zeroRel (fiberResidual fstBool) ff tf ∧
      zeroRel (fiberResidual sndBool) ff tf :=
  ⟨fst_relates_same_first, snd_not_ff_ft,
    fst_separates_different_first, snd_relates_ff_tf⟩

#print axioms different_p_different_classes

/-- Equality residual is the special case p = id. Not a derivation of p. -/
def idBool : Bool → Bool := id

theorem id_recovers_equality (x y : Bool) :
    zeroRel (fiberResidual idBool) x y ↔ x = y :=
  Iff.rfl

#print axioms id_recovers_equality

theorem fst_is_not_id :
    zeroRel (fiberResidual fstBool) ff ft ∧
      ¬ zeroRel (fiberResidual (fun q : Bool × Bool => (q.1, q.2))) ff ft := by
  constructor
  · exact fst_relates_same_first
  · intro h
    cases h

#print axioms fst_is_not_id

/-- Presentation is extra data: fiberPD needs a supplied p. -/
theorem presentation_is_supplied :
    fiberRel fstBool ff ft ∧ ¬ fiberRel sndBool ff ft :=
  ⟨rfl, by intro h; cases h⟩

#print axioms presentation_is_supplied

end ProjectionFiber.E003
