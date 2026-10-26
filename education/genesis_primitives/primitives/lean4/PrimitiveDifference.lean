/-!
# Primitive Difference Candidates, Pointed Relations & Category (Lean 4)

Extracted with full fidelity from 19L57G1:
- lean4/Derivation/PrimDiff.lean
- lean4/Derivation/PrimitiveCore.lean
- lean4/Derivation/PrimitiveCats.lean

Classification: Metatheory apparatus & formal mathematical spine.
AuthorityEffect: None.
-/

namespace GenesisPrimitives.PrimitiveDifference

/-- Irreflexivity: weakest object-level fidelity commitment studied here. -/
def Irrefl {α : Type} (r : α → α → Prop) : Prop := ∀ x, ¬ r x x

/-- Symmetrization of a relation. -/
def Sym {α : Type} (r : α → α → Prop) : α → α → Prop :=
  fun x y => r x y ∨ r y x

/-- Transpose of a relation. -/
def Transpose {α : Type} (r : α → α → Prop) : α → α → Prop :=
  fun x y => r y x

/-- The oriented two-element difference: carrier Bool, one directed edge. -/
def D2 : Bool → Bool → Prop := fun x y => x = false ∧ y = true

/-- The reversed orientation. -/
def D2rev : Bool → Bool → Prop := fun x y => x = true ∧ y = false

/-- The symmetric two-element difference: symmetrization of D2. -/
def S2 : Bool → Bool → Prop := Sym D2

/-- The common signature for the nine candidate readings.
    Fields: carrier `X`, asserted relation `r`, endpoints `a` and `b`,
    retention store `ret`, protection store `prot`, and operation family `Ops`. -/
structure Setting where
  X : Type
  r : X → X → Prop
  a : X
  b : X
  ret : X → X → Prop
  prot : X → X → Prop
  Ops : (X → X) → Prop

/-- Cotransitivity: an asserted difference splits against every third point. -/
def Cotrans {X : Type} (r : X → X → Prop) : Prop :=
  ∀ x y, r x y → ∀ z, r x z ∨ r z y

/-- Locatedness: the relation is realized by a boolean-valued function. -/
def Located {X : Type} (r : X → X → Prop) : Prop :=
  ∃ f : X → X → Bool, ∀ x y, r x y ↔ f x y = true

/-- W: bare witnessed pair. -/
def W (S : Setting) : Prop := S.r S.a S.b

/-- A: pointed witnessed irreflexive relation (PD-A). -/
def A (S : Setting) : Prop := S.r S.a S.b ∧ Irrefl S.r

/-- Bs: symmetric PD-B axis: A plus symmetry. -/
def Bs (S : Setting) : Prop := A S ∧ (∀ x y, S.r x y → S.r y x)

/-- Bc: cotransitive PD-B axis: A plus cotransitivity. -/
def Bc (S : Setting) : Prop := A S ∧ Cotrans S.r

/-- Bl: located PD-B axis: A plus locatedness. -/
def Bl (S : Setting) : Prop := A S ∧ Located S.r

/-- C: witnessed non-identification (PD-C): asserted pair plus protected demand. -/
def C (S : Setting) : Prop := S.r S.a S.b ∧ S.prot S.a S.b

/-- D: non-factorization through the point (PD-D): metatheoretic endpoint inequality. -/
def D (S : Setting) : Prop := ¬ ∃ p : Unit → S.X, p () = S.a ∧ p () = S.b

/-- F: protected retained primitive difference (PD-F): A plus retention plus protection. -/
def F (S : Setting) : Prop := A S ∧ S.ret S.a S.b ∧ S.prot S.a S.b

/-- Pointed witnessed relation category object: carrier X, relation r,
    designated endpoints a and b, and the witness proof `w : r a b`. -/
structure PtdRel where
  X : Type
  r : X → X → Prop
  a : X
  b : X
  w : r a b

/-- Morphism in PtdRel preserving designated endpoints and arrows. -/
structure Hom (A B : PtdRel) where
  f : A.X → B.X
  ha : f A.a = B.a
  hb : f A.b = B.b
  hr : ∀ x y, A.r x y → B.r (f x) (f y)

end GenesisPrimitives.PrimitiveDifference
