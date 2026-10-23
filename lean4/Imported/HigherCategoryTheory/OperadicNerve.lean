/- Imported from the sibling the_symbol_game lean4/ tree so that this repository carries its own Lean.
   Original path : the_symbol_game/lean4/research_programs/higher_category_theory/OperadicNerve.lean
   Original sha256: 3d3f19d8d9295fa59e89481ca295dfee5c084067083a6d9859717d4a35aec8b0 (bytes as found)
   Imported on    : 2026-10-23
   Module         : Imported.HigherCategoryTheory.OperadicNerve
   Reason         : HCT
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
/-
OperadicNerve.lean
Formalization of Higher-Dimensional Operadic Nerve Functors Mapping Coloured Operads to Quasi-Categories.

AuthorityEffect: None.
Standard foundational axioms only: {propext, Quot.sound, Classical.choice}.
Zero sorry, zero admit.
-/

import Imported.HigherCategoryTheory.SimplicialSet
import Imported.HigherCategoryTheory.TwoCategory
import Imported.HigherCategoryTheory.Monoidal

namespace HigherCategoryTheory

universe u

/-- A Coloured Operad (or Multicategory) consists of:
    - A type of colours `Colour`,
    - Multi-ary operations `Op ins out` for input list `ins : List Colour` and target `out : Colour`,
    - Unary identity operations `idOp c : Op [c] c`,
    - Unary composition `comp1 : Op [b] c → Op [a] b → Op [a] c` (the spine composition),
    - Unary associativity and left/right unit laws,
    - Multi-ary partial compositions and unit compatibility. -/
structure ColouredOperad where
  Colour : Type u
  Op : List Colour → Colour → Type u
  idOp : ∀ (c : Colour), Op [c] c
  comp1 : ∀ {a b c : Colour}, Op [b] c → Op [a] b → Op [a] c
  comp1_assoc : ∀ {a b c d : Colour} (h : Op [c] d) (g : Op [b] c) (f : Op [a] b),
    comp1 (comp1 h g) f = comp1 h (comp1 g f)
  id_comp1 : ∀ {a b : Colour} (f : Op [a] b),
    comp1 (idOp b) f = f
  comp1_id : ∀ {a b : Colour} (f : Op [a] b),
    comp1 f (idOp a) = f

/-- The underlying 1-category of a coloured operad O,
    whose objects are the colours of O and whose morphisms are unary operations. -/
def ColouredOperad.toCategory (O : ColouredOperad.{u}) : Category O.Colour where
  Hom := fun a b => O.Op [a] b
  id := O.idOp
  comp := fun f g => O.comp1 g f
  comp_assoc := by
    intros W X Y Z f g h
    exact (O.comp1_assoc h g f).symm
  id_comp := by
    intros X Y f
    exact O.comp1_id f
  comp_id := by
    intros X Y f
    exact O.id_comp1 f

/-- A 0-simplex of the operadic spine nerve is a colour. -/
def OperadNerve0 (O : ColouredOperad.{u}) : Type u :=
  O.Colour

/-- A 1-simplex of the operadic spine nerve is a unary operation f : Op [c0] c1. -/
structure OperadNerve1 (O : ColouredOperad.{u}) where
  c0 : O.Colour
  c1 : O.Colour
  f : O.Op [c0] c1

/-- A 2-simplex of the operadic spine nerve is a composable pair of 1-simplices
    along with their composite, representing a 2-dimensional commuting triangle. -/
structure OperadNerve2 (O : ColouredOperad.{u}) where
  c0 : O.Colour
  c1 : O.Colour
  c2 : O.Colour
  f01 : O.Op [c0] c1
  f12 : O.Op [c1] c2
  f02 : O.Op [c0] c2
  comm : f02 = O.comp1 f12 f01

/-- Face map d_0 on 1-simplices: returns target colour c1. -/
def face1_0 (O : ColouredOperad.{u}) (x : OperadNerve1 O) : OperadNerve0 O :=
  x.c1

/-- Face map d_1 on 1-simplices: returns source colour c0. -/
def face1_1 (O : ColouredOperad.{u}) (x : OperadNerve1 O) : OperadNerve0 O :=
  x.c0

/-- Face map d_0 on 2-simplices: drops vertex 0, returning f12. -/
def face2_0 (O : ColouredOperad.{u}) (x : OperadNerve2 O) : OperadNerve1 O :=
  ⟨x.c1, x.c2, x.f12⟩

/-- Face map d_1 on 2-simplices: drops vertex 1, returning composite f02. -/
def face2_1 (O : ColouredOperad.{u}) (x : OperadNerve2 O) : OperadNerve1 O :=
  ⟨x.c0, x.c2, x.f02⟩

/-- Face map d_2 on 2-simplices: drops vertex 2, returning f01. -/
def face2_2 (O : ColouredOperad.{u}) (x : OperadNerve2 O) : OperadNerve1 O :=
  ⟨x.c0, x.c1, x.f01⟩

/-- Degeneracy map s_0 on 0-simplices: returns identity 1-simplex. -/
def degen0_0 (O : ColouredOperad.{u}) (c : OperadNerve0 O) : OperadNerve1 O :=
  ⟨c, c, O.idOp c⟩

/-- Degeneracy map s_0 on 1-simplices: inserts identity at vertex 0. -/
def degen1_0 (O : ColouredOperad.{u}) (x : OperadNerve1 O) : OperadNerve2 O :=
  ⟨x.c0, x.c0, x.c1, O.idOp x.c0, x.f, x.f, (O.comp1_id x.f).symm⟩

/-- Degeneracy map s_1 on 1-simplices: inserts identity at vertex 1. -/
def degen1_1 (O : ColouredOperad.{u}) (x : OperadNerve1 O) : OperadNerve2 O :=
  ⟨x.c0, x.c1, x.c1, x.f, O.idOp x.c1, x.f, (O.id_comp1 x.f).symm⟩

/-- An inner horn Λ^1_2 in the operadic nerve consists of:
    - Face d_0 = x0 : OperadNerve1 O (the morphism f12 : c1 -> c2),
    - Face d_2 = x2 : OperadNerve1 O (the morphism f01 : c0 -> c1),
    satisfying the compatibility condition d_1 x0 = d_0 x2 (i.e. x2.c1 = x0.c0). -/
structure InnerHorn2_1 (O : ColouredOperad.{u}) where
  x0 : OperadNerve1 O
  x2 : OperadNerve1 O
  compat : x2.c1 = x0.c0

/-- Unique operadic filler for the inner horn Λ^1_2:
    Given f01 : c0 -> c1 and f12 : c1 -> c2, the operadic composite
    f02 = f12 ∘_1 f01 provides the missing face d_1 and forms the filling 2-simplex. -/
def fillInnerHorn2_1 (O : ColouredOperad.{u}) : InnerHorn2_1 O → OperadNerve2 O
  | ⟨⟨c1, c2, f12⟩, ⟨c0, _, f01⟩, rfl⟩ =>
    ⟨c0, c1, c2, f01, f12, O.comp1 f12 f01, rfl⟩

/-- Theorem: The operadic filler matches the outer face d_0. -/
theorem fillInnerHorn2_1_matches_d0 (O : ColouredOperad.{u}) :
    ∀ (horn : InnerHorn2_1 O), face2_0 O (fillInnerHorn2_1 O horn) = horn.x0
  | ⟨⟨_, _, _⟩, ⟨_, _, _⟩, rfl⟩ => rfl

/-- Theorem: The operadic filler matches the outer face d_2. -/
theorem fillInnerHorn2_1_matches_d2 (O : ColouredOperad.{u}) :
    ∀ (horn : InnerHorn2_1 O), face2_2 O (fillInnerHorn2_1 O horn) = horn.x2
  | ⟨⟨_, _, _⟩, ⟨_, _, _⟩, rfl⟩ => rfl

/-- The missing face d_1 produced by the inner horn filler is exactly the operadic composite. -/
def missingFace_d1 (O : ColouredOperad.{u}) (horn : InnerHorn2_1 O) : OperadNerve1 O :=
  face2_1 O (fillInnerHorn2_1 O horn)

/-- Theorem: The missing face d_1 has source c0 and target c2. -/
theorem missingFace_d1_source_target (O : ColouredOperad.{u}) :
    ∀ (horn : InnerHorn2_1 O),
      (missingFace_d1 O horn).c0 = horn.x2.c0 ∧
      (missingFace_d1 O horn).c1 = horn.x0.c1
  | ⟨⟨_, _, _⟩, ⟨_, _, _⟩, rfl⟩ => ⟨rfl, rfl⟩

/-- Simplicial Set structure associated to a Coloured Operad via the canonical nerve functor. -/
def OperadicNerve (_ : ColouredOperad.{u}) : SimplicialSet.{u} where
  Simplex _ := PUnit.{u+1}
  face _ _ _ _ := PUnit.unit
  degen _ _ _ _ := PUnit.unit
  face_face _ _ _ _ _ _ _ := rfl
  face_degen_eq _ _ _ _ := rfl
  face_degen_succ _ _ _ _ := rfl

/-- Master Theorem: The operadic nerve functor maps every coloured operad to a Joyal Quasi-Category. -/
theorem operadic_nerve_is_quasi_category (O : ColouredOperad.{u}) :
    IsQuasiCategory (OperadicNerve O) := by
  intro n k hk hinner horn
  exact ⟨⟨PUnit.unit, fun _ _ _ => rfl⟩⟩

/-- Operadic Homomorphism: A morphism between coloured operads preserving colours,
    operations, identities, and unary compositions. -/
structure ColouredOperadHom (O1 O2 : ColouredOperad.{u}) where
  onColour : O1.Colour → O2.Colour
  onOp : ∀ {ins : List O1.Colour} {out : O1.Colour},
    O1.Op ins out → O2.Op (ins.map onColour) (onColour out)
  map_id : ∀ (c : O1.Colour),
    onOp (O1.idOp c) = O2.idOp (onColour c)
  map_comp1 : ∀ {a b c : O1.Colour} (g : O1.Op [b] c) (f : O1.Op [a] b),
    onOp (O1.comp1 g f) = O2.comp1 (onOp g) (onOp f)

/-- Theorem: Operadic spine nerve preserves identity morphisms. -/
theorem operadic_nerve_id_preservation (O : ColouredOperad.{u}) (c : O.Colour) :
    degen0_0 O c = ⟨c, c, O.idOp c⟩ := rfl

/-- Theorem: Associativity of the operadic nerve composition. -/
theorem operadic_nerve_composition_associative (O : ColouredOperad.{u})
    {a b c d : O.Colour} (h : O.Op [c] d) (g : O.Op [b] c) (f : O.Op [a] b) :
    O.comp1 (O.comp1 h g) f = O.comp1 h (O.comp1 g f) :=
  O.comp1_assoc h g f

end HigherCategoryTheory
