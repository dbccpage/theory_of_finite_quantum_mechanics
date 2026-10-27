/- Imported so that this repository carries its own Lean evidence.
   Original sha256: 63847acd16dfff482a97d97ff4734e14537d8546fa852828ef7e9d7d5f611554 (bytes as found)
   Imported on    : 2026-10-23
   Module         : Imported.HigherCategoryTheory.Monoidal
   Reason         : HCT
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
/-
Released under Apache 2.0 license as described in the file LICENSE.
-/

import Imported.HigherCategoryTheory.Bicategory

namespace HigherCategoryTheory

universe u v

set_option linter.checkUnivs false
set_option linter.unusedVariables false

/-- Standard 1-category structure. -/
structure Category (Obj : Type u) where
  Hom : Obj → Obj → Type v
  id : (X : Obj) → Hom X X
  comp : {X Y Z : Obj} → Hom X Y → Hom Y Z → Hom X Z
  comp_assoc : ∀ {W X Y Z : Obj} (f : Hom W X) (g : Hom X Y) (h : Hom Y Z),
    comp (comp f g) h = comp f (comp g h)
  id_comp : ∀ {X Y : Obj} (f : Hom X Y), comp (id X) f = f
  comp_id : ∀ {X Y : Obj} (f : Hom X Y), comp f (id Y) = f

/-- An isomorphism between objects in a category. -/
structure Iso {Obj : Type u} (C : Category Obj) (X Y : Obj) where
  hom : C.Hom X Y
  inv : C.Hom Y X
  hom_inv_id : C.comp hom inv = C.id X
  inv_hom_id : C.comp inv hom = C.id Y

/-- Identity isomorphism. -/
def Iso.refl {Obj : Type u} (C : Category Obj) (X : Obj) : Iso C X X where
  hom := C.id X
  inv := C.id X
  hom_inv_id := C.comp_id (C.id X)
  inv_hom_id := C.comp_id (C.id X)

/-- Inverse isomorphism. -/
def Iso.symm {Obj : Type u} {C : Category Obj} {X Y : Obj} (i : Iso C X Y) : Iso C Y X where
  hom := i.inv
  inv := i.hom
  hom_inv_id := i.inv_hom_id
  inv_hom_id := i.hom_inv_id

/-- Composition of isomorphisms. -/
def Iso.trans {Obj : Type u} {C : Category Obj} {X Y Z : Obj}
    (i : Iso C X Y) (j : Iso C Y Z) : Iso C X Z where
  hom := C.comp i.hom j.hom
  inv := C.comp j.inv i.inv
  hom_inv_id := by
    rw [C.comp_assoc]
    have hmid : C.comp j.hom (C.comp j.inv i.inv) = C.comp (C.comp j.hom j.inv) i.inv := by
      rw [C.comp_assoc]
    rw [hmid, j.hom_inv_id, C.id_comp, i.hom_inv_id]
  inv_hom_id := by
    rw [C.comp_assoc]
    have hmid : C.comp i.inv (C.comp i.hom j.hom) = C.comp (C.comp i.inv i.hom) j.hom := by
      rw [C.comp_assoc]
    rw [hmid, i.inv_hom_id, C.id_comp, j.inv_hom_id]

/-- A Monoidal Category consists of:
    - An underlying category `cat`
    - A tensor bifunctor `tensorObj` on objects and `tensorHom` on morphisms
    - A monoidal unit object `unit`
    - Natural associator isomorphisms
    - Natural left and right unitor isomorphisms
    - Mac Lane's pentagon and triangle coherence axioms -/
structure MonoidalCategory (Obj : Type u) where
  cat : Category.{u, v} Obj
  -- Monoidal product
  tensorObj : Obj → Obj → Obj
  unit : Obj
  tensorHom : {X1 X2 Y1 Y2 : Obj} → cat.Hom X1 X2 → cat.Hom Y1 Y2 →
    cat.Hom (tensorObj X1 Y1) (tensorObj X2 Y2)
  -- Bifunctoriality
  tensorHom_id : ∀ (X Y : Obj),
    tensorHom (cat.id X) (cat.id Y) = cat.id (tensorObj X Y)
  tensorHom_comp : ∀ {X1 X2 X3 Y1 Y2 Y3 : Obj}
    (f1 : cat.Hom X1 X2) (f2 : cat.Hom X2 X3)
    (g1 : cat.Hom Y1 Y2) (g2 : cat.Hom Y2 Y3),
    tensorHom (cat.comp f1 f2) (cat.comp g1 g2) =
      cat.comp (tensorHom f1 g1) (tensorHom f2 g2)
  -- Associator isomorphism: (X ⊗ Y) ⊗ Z ≅ X ⊗ (Y ⊗ Z)
  associator : (X Y Z : Obj) →
    Iso cat (tensorObj (tensorObj X Y) Z) (tensorObj X (tensorObj Y Z))
  -- Left unitor: I ⊗ X ≅ X
  leftUnitor : (X : Obj) →
    Iso cat (tensorObj unit X) X
  -- Right unitor: X ⊗ I ≅ X
  rightUnitor : (X : Obj) →
    Iso cat (tensorObj X unit) X
  -- Naturality of associator
  associator_naturality : ∀ {X1 X2 Y1 Y2 Z1 Z2 : Obj}
    (f : cat.Hom X1 X2) (g : cat.Hom Y1 Y2) (h : cat.Hom Z1 Z2),
    cat.comp (tensorHom (tensorHom f g) h) (associator X2 Y2 Z2).hom =
      cat.comp (associator X1 Y1 Z1).hom (tensorHom f (tensorHom g h))
  -- Naturality of left unitor
  leftUnitor_naturality : ∀ {X1 X2 : Obj} (f : cat.Hom X1 X2),
    cat.comp (tensorHom (cat.id unit) f) (leftUnitor X2).hom =
      cat.comp (leftUnitor X1).hom f
  -- Naturality of right unitor
  rightUnitor_naturality : ∀ {X1 X2 : Obj} (f : cat.Hom X1 X2),
    cat.comp (tensorHom f (cat.id unit)) (rightUnitor X2).hom =
      cat.comp (rightUnitor X1).hom f
  -- Mac Lane's Pentagon coherence axiom:
  pentagon : ∀ (W X Y Z : Obj),
    let step1 := tensorHom (associator W X Y).hom (cat.id Z)
    let step2 := (associator W (tensorObj X Y) Z).hom
    let step3 := tensorHom (cat.id W) (associator X Y Z).hom
    let step4 := (associator (tensorObj W X) Y Z).hom
    let step5 := (associator W X (tensorObj Y Z)).hom
    cat.comp step1 (cat.comp step2 step3) = cat.comp step4 step5
  -- Mac Lane's Triangle coherence axiom:
  triangle : ∀ (X Y : Obj),
    cat.comp (associator X unit Y).hom (tensorHom (cat.id X) (leftUnitor Y).hom) =
      tensorHom (rightUnitor X).hom (cat.id Y)

namespace MonoidalCategory

variable {Obj : Type u} (M : MonoidalCategory.{u, v} Obj)

/-- Delooping: Canonical representation of a Monoidal Category as a 1-object Bicategory. -/
def toBicategory : Bicategory.{0, u, v} Unit where
  Hom := fun _ _ => Obj
  Hom2 := fun {A B} X Y => M.cat.Hom X Y
  homCat := fun _ _ => {
    id2 := fun X => M.cat.id X
    vcomp := fun α β => M.cat.comp α β
    vcomp_assoc := fun α β γ => M.cat.comp_assoc α β γ
    id2_vcomp := fun α => M.cat.id_comp α
    vcomp_id2 := fun α => M.cat.comp_id α
  }
  id1 := fun _ => M.unit
  hcomp1 := fun {A B C} X Y => M.tensorObj X Y
  whiskerLeft := fun {A B C} X {Y1 Y2} β => M.tensorHom (M.cat.id X) β
  whiskerRight := fun {A B C} {X1 X2} α Y => M.tensorHom α (M.cat.id Y)
  hcomp2 := fun {A B C} {X1 X2 Y1 Y2} α β => M.tensorHom α β
  whiskerLeft_eq := fun {A B C} f {g1 g2} β => rfl
  whiskerRight_eq := fun {A B C} {f1 f2} α g => rfl
  hcomp2_id2 := fun X Y => M.tensorHom_id X Y
  interchange := fun {A B C} {X1 X2 X3 Y1 Y2 Y3} α β γ δ => M.tensorHom_comp α β γ δ
  associator := fun {A B C D} X Y Z => {
    hom := (M.associator X Y Z).hom
    inv := (M.associator X Y Z).inv
    hom_inv_id := (M.associator X Y Z).hom_inv_id
    inv_hom_id := (M.associator X Y Z).inv_hom_id
  }
  leftUnitor := fun {A B} X => {
    hom := (M.leftUnitor X).hom
    inv := (M.leftUnitor X).inv
    hom_inv_id := (M.leftUnitor X).hom_inv_id
    inv_hom_id := (M.leftUnitor X).inv_hom_id
  }
  rightUnitor := fun {A B} X => {
    hom := (M.rightUnitor X).hom
    inv := (M.rightUnitor X).inv
    hom_inv_id := (M.rightUnitor X).hom_inv_id
    inv_hom_id := (M.rightUnitor X).inv_hom_id
  }
  associator_naturality := fun {A B C D X1 X2 Y1 Y2 Z1 Z2} α β γ =>
    M.associator_naturality α β γ
  leftUnitor_naturality := fun {A B X1 X2} α =>
    M.leftUnitor_naturality α
  rightUnitor_naturality := fun {A B X1 X2} α =>
    M.rightUnitor_naturality α
  pentagon := fun {A B C D E} W X Y Z =>
    M.pentagon W X Y Z
  triangle := fun {A B C} X Y =>
    M.triangle X Y

end MonoidalCategory

end HigherCategoryTheory
