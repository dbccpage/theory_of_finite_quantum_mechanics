/- Imported from the sibling the_symbol_game lean4/ tree so that this repository carries its own Lean.
   Original path : the_symbol_game/lean4/research_programs/higher_category_theory/HigherFunctor.lean
   Original sha256: ce048f51b0fde6fb1e5e578f8bf76a4219feb29d114a48ce8eed6605037f19ea (bytes as found)
   Imported on    : 2026-10-23
   Module         : Imported.HigherCategoryTheory.HigherFunctor
   Reason         : HCT
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
/-
Copyright (c) 2026 Anomalon Research. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Worker M1 (Lean 4 HCT Formalization)
-/

import Imported.HigherCategoryTheory.Bicategory
import Imported.HigherCategoryTheory.TwoCategory

namespace HigherCategoryTheory

universe u1 v1 w1 u2 v2 w2

set_option linter.checkUnivs false
set_option linter.unusedVariables false

/-- A Pseudofunctor (weak 2-functor) F : B1 → B2 between bicategories consists of:
    - Object map `obj : Obj1 → Obj2`
    - 1-cell map `map1 : Hom(A, B) → Hom(FA, FB)`
    - 2-cell map `map2 : Hom2(f, g) → Hom2(Ff, Fg)` preserving vertical identity and composition
    - Invertible compositor 2-cells: F(f) ∘_h F(g) ≅ F(f ∘_h g)
    - Invertible unitor 2-cells: id_{FA} ≅ F(id_A)
    - Naturality and coherence axioms relating compositors/unitors to associator and unitors. -/
structure Pseudofunctor {Obj1 : Type u1} {Obj2 : Type u2}
    (B1 : Bicategory.{u1, v1, w1} Obj1) (B2 : Bicategory.{u2, v2, w2} Obj2) where
  obj : Obj1 → Obj2
  map1 : {A B : Obj1} → B1.Hom A B → B2.Hom (obj A) (obj B)
  map2 : {A B : Obj1} → {f g : B1.Hom A B} →
    B1.Hom2 f g → B2.Hom2 (map1 f) (map1 g)
  -- Functoriality on 2-cells
  map2_id2 : ∀ {A B : Obj1} (f : B1.Hom A B),
    map2 ((B1.homCat A B).id2 f) = (B2.homCat (obj A) (obj B)).id2 (map1 f)
  map2_vcomp : ∀ {A B : Obj1} {f g h : B1.Hom A B}
    (α : B1.Hom2 f g) (β : B1.Hom2 g h),
    map2 ((B1.homCat A B).vcomp α β) =
      (B2.homCat (obj A) (obj B)).vcomp (map2 α) (map2 β)
  -- Compositor 2-isomorphism: F(f) ∘_h F(g) ≅ F(f ∘_h g)
  compositor : {A B C : Obj1} → (f : B1.Hom A B) → (g : B1.Hom B C) →
    Iso2 (B2.homCat (obj A) (obj C)) (B2.hcomp1 (map1 f) (map1 g)) (map1 (B1.hcomp1 f g))
  -- Unitor 2-isomorphism: id_{FA} ≅ F(id_A)
  unitor : (A : Obj1) →
    Iso2 (B2.homCat (obj A) (obj A)) (B2.id1 (obj A)) (map1 (B1.id1 A))
  -- Compositor naturality
  compositor_naturality : ∀ {A B C : Obj1}
    {f1 f2 : B1.Hom A B} {g1 g2 : B1.Hom B C}
    (α : B1.Hom2 f1 f2) (β : B1.Hom2 g1 g2),
    (B2.homCat (obj A) (obj C)).vcomp (B2.hcomp2 (map2 α) (map2 β)) (compositor f2 g2).hom =
      (B2.homCat (obj A) (obj C)).vcomp (compositor f1 g1).hom (map2 (B1.hcomp2 α β))
  -- Associator coherence for pseudofunctor:
  -- (compositor f g ▷ Fh) ≫ compositor (f ∘ g) h ≫ F(α_{f,g,h}) =
  -- α_{Ff,Fg,Fh} ≫ (Ff ◁ compositor g h) ≫ compositor f (g ∘ h)
  associator_coherence : ∀ {A B C D : Obj1}
    (f : B1.Hom A B) (g : B1.Hom B C) (h : B1.Hom C D),
    let l1 := B2.whiskerRight (compositor f g).hom (map1 h)
    let l2 := (compositor (B1.hcomp1 f g) h).hom
    let l3 := map2 (B1.associator f g h).hom
    let r1 := (B2.associator (map1 f) (map1 g) (map1 h)).hom
    let r2 := B2.whiskerLeft (map1 f) (compositor g h).hom
    let r3 := (compositor f (B1.hcomp1 g h)).hom
    (B2.homCat (obj A) (obj D)).vcomp l1 ((B2.homCat (obj A) (obj D)).vcomp l2 l3) =
      (B2.homCat (obj A) (obj D)).vcomp r1 ((B2.homCat (obj A) (obj D)).vcomp r2 r3)
  -- Left unitor coherence:
  leftUnitor_coherence : ∀ {A B : Obj1} (f : B1.Hom A B),
    let l1 := B2.whiskerRight (unitor A).hom (map1 f)
    let l2 := (compositor (B1.id1 A) f).hom
    let l3 := map2 (B1.leftUnitor f).hom
    let r1 := (B2.leftUnitor (map1 f)).hom
    (B2.homCat (obj A) (obj B)).vcomp l1 ((B2.homCat (obj A) (obj B)).vcomp l2 l3) = r1
  -- Right unitor coherence:
  rightUnitor_coherence : ∀ {A B : Obj1} (f : B1.Hom A B),
    let l1 := B2.whiskerLeft (map1 f) (unitor B).hom
    let l2 := (compositor f (B1.id1 B)).hom
    let l3 := map2 (B1.rightUnitor f).hom
    let r1 := (B2.rightUnitor (map1 f)).hom
    (B2.homCat (obj A) (obj B)).vcomp l1 ((B2.homCat (obj A) (obj B)).vcomp l2 l3) = r1

namespace Pseudofunctor

variable {Obj1 : Type u1} {Obj2 : Type u2}
variable {B1 : Bicategory.{u1, v1, w1} Obj1} {B2 : Bicategory.{u2, v2, w2} Obj2}
variable (F : Pseudofunctor B1 B2)

/-- A pseudofunctor is strict if its compositors and unitors are identity 2-isomorphisms. -/
def IsStrict : Prop :=
  (∀ {A B C : Obj1} (f : B1.Hom A B) (g : B1.Hom B C),
    ∃ p : B2.hcomp1 (F.map1 f) (F.map1 g) = F.map1 (B1.hcomp1 f g),
      F.compositor f g = eqToIso2 (B2.homCat (F.obj A) (F.obj C)) p) ∧
  (∀ (A : Obj1), ∃ p : B2.id1 (F.obj A) = F.map1 (B1.id1 A),
    F.unitor A = eqToIso2 (B2.homCat (F.obj A) (F.obj A)) p)

/-- Identity pseudofunctor on any bicategory. -/
def id {Obj : Type u1} (Bcat : Bicategory.{u1, v1, w1} Obj) : Pseudofunctor Bcat Bcat where
  obj := _root_.id
  map1 := _root_.id
  map2 := _root_.id
  map2_id2 := fun f => rfl
  map2_vcomp := fun α β => rfl
  compositor := fun f g => Iso2.refl (Bcat.homCat _ _) (Bcat.hcomp1 f g)
  unitor := fun A => Iso2.refl (Bcat.homCat _ _) (Bcat.id1 A)
  compositor_naturality := fun {A B C f1 f2 g1 g2} α β => by
    dsimp [Iso2.refl]
    rw [(Bcat.homCat A C).vcomp_id2, (Bcat.homCat A C).id2_vcomp]
  associator_coherence := fun {A B C D} f g h => by
    dsimp [Iso2.refl]
    rw [Bcat.whiskerRight_eq, Bcat.whiskerLeft_eq]
    rw [Bcat.hcomp2_id2, Bcat.hcomp2_id2]
    rw [(Bcat.homCat A D).id2_vcomp, (Bcat.homCat A D).id2_vcomp]
    rw [(Bcat.homCat A D).id2_vcomp, (Bcat.homCat A D).vcomp_id2]
  leftUnitor_coherence := fun {A B} f => by
    dsimp [Iso2.refl]
    rw [Bcat.whiskerRight_eq]
    rw [Bcat.hcomp2_id2]
    rw [(Bcat.homCat A B).id2_vcomp, (Bcat.homCat A B).id2_vcomp]
  rightUnitor_coherence := fun {A B} f => by
    dsimp [Iso2.refl]
    rw [Bcat.whiskerLeft_eq]
    rw [Bcat.hcomp2_id2]
    rw [(Bcat.homCat A B).id2_vcomp, (Bcat.homCat A B).id2_vcomp]

end Pseudofunctor

end HigherCategoryTheory
