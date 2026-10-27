/- Imported so that this repository carries its own Lean evidence.
   Original sha256: 4b557794538acd7795da66c633f1cff41145e66982b3dc80400778facf67e0ac (bytes as found)
   Imported on    : 2026-10-23
   Module         : Imported.HigherCategoryTheory.Braided
   Reason         : HCT
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
/-
Released under Apache 2.0 license as described in the file LICENSE.
-/

import Imported.HigherCategoryTheory.Monoidal

namespace HigherCategoryTheory

universe u v

set_option linter.checkUnivs false
set_option linter.unusedVariables false

/-- A Braided Monoidal Category is a monoidal category equipped with a natural
    isomorphism (braiding) β_{X,Y} : X ⊗ Y ≅ Y ⊗ X satisfying the two hexagon coherence axioms. -/
structure BraidedCategory (Obj : Type u) where
  mon : MonoidalCategory.{u, v} Obj
  -- Braiding isomorphism: X ⊗ Y ≅ Y ⊗ X
  braiding : (X Y : Obj) →
    Iso mon.cat (mon.tensorObj X Y) (mon.tensorObj Y X)
  -- Naturality of braiding
  braiding_naturality : ∀ {X1 X2 Y1 Y2 : Obj}
    (f : mon.cat.Hom X1 X2) (g : mon.cat.Hom Y1 Y2),
    mon.cat.comp (mon.tensorHom f g) (braiding X2 Y2).hom =
      mon.cat.comp (braiding X1 Y1).hom (mon.tensorHom g f)
  -- Hexagon Axiom 1 (Forward):
  -- α_{X,Y,Z} ≫ β_{X, Y ⊗ Z} ≫ α_{Y,Z,X} = (β_{X,Y} ⊗ id_Z) ≫ α_{Y,X,Z} ≫ (id_Y ⊗ β_{X,Z})
  hexagon1 : ∀ (X Y Z : Obj),
    let l1 := (mon.associator X Y Z).hom
    let l2 := (braiding X (mon.tensorObj Y Z)).hom
    let l3 := (mon.associator Y Z X).hom
    let r1 := mon.tensorHom (braiding X Y).hom (mon.cat.id Z)
    let r2 := (mon.associator Y X Z).hom
    let r3 := mon.tensorHom (mon.cat.id Y) (braiding X Z).hom
    mon.cat.comp l1 (mon.cat.comp l2 l3) =
      mon.cat.comp r1 (mon.cat.comp r2 r3)
  -- Hexagon Axiom 2 (Reverse):
  -- α^{-1}_{X,Y,Z} ≫ β_{X ⊗ Y, Z} ≫ α^{-1}_{Z,X,Y} = (id_X ⊗ β_{Y,Z}) ≫ α^{-1}_{X,Z,Y} ≫ (β_{X,Z} ⊗ id_Y)
  hexagon2 : ∀ (X Y Z : Obj),
    let l1 := (mon.associator X Y Z).inv
    let l2 := (braiding (mon.tensorObj X Y) Z).hom
    let l3 := (mon.associator Z X Y).inv
    let r1 := mon.tensorHom (mon.cat.id X) (braiding Y Z).hom
    let r2 := (mon.associator X Z Y).inv
    let r3 := mon.tensorHom (braiding X Z).hom (mon.cat.id Y)
    mon.cat.comp l1 (mon.cat.comp l2 l3) =
      mon.cat.comp r1 (mon.cat.comp r2 r3)

namespace BraidedCategory

variable {Obj : Type u} (B : BraidedCategory.{u, v} Obj)

/-- Full twist / double braiding on two strands: β_{Y,X} ∘ β_{X,Y} : X ⊗ Y → X ⊗ Y. -/
def doubleBraiding (X Y : Obj) : B.mon.cat.Hom (B.mon.tensorObj X Y) (B.mon.tensorObj X Y) :=
  B.mon.cat.comp (B.braiding X Y).hom (B.braiding Y X).hom

/-- A braided category is symmetric if every double braiding is the identity morphism. -/
def IsSymmetric : Prop :=
  ∀ (X Y : Obj), B.doubleBraiding X Y = B.mon.cat.id (B.mon.tensorObj X Y)

end BraidedCategory

end HigherCategoryTheory
