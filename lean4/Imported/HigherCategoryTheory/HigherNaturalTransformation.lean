/- Imported from the sibling the_symbol_game lean4/ tree so that this repository carries its own Lean.
   Original path : the_symbol_game/lean4/research_programs/higher_category_theory/HigherNaturalTransformation.lean
   Original sha256: 1da9a426a8285ad612f032f69a4ea567608575da76f661d98875cb915069c18c (bytes as found)
   Imported on    : 2026-10-23
   Module         : Imported.HigherCategoryTheory.HigherNaturalTransformation
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

import Imported.HigherCategoryTheory.HigherFunctor
import Imported.HigherCategoryTheory.TwoCategory

namespace HigherCategoryTheory

universe u1 v1 w1 u2 v2 w2

set_option linter.checkUnivs false
set_option linter.unusedVariables false

/-- A Pseudonatural Transformation (2-natural transformation) σ : F ⇒ G between pseudofunctors
    consists of:
    - 1-cell components σ_A : F(A) → G(A) for each 0-cell A
    - Invertible 2-cells σ_f : F(f) ∘_h σ_B ≅ σ_A ∘_h G(f) for each 1-cell f : A → B
    - Naturality with respect to 2-cells
    - Coherence with 1-cell composition and identities. -/
structure PseudoNatTrans {Obj1 : Type u1} {Obj2 : Type u2}
    {B1 : Bicategory.{u1, v1, w1} Obj1} {B2 : Bicategory.{u2, v2, w2} Obj2}
    (F G : Pseudofunctor B1 B2) where
  comp1 : (A : Obj1) → B2.Hom (F.obj A) (G.obj A)
  comp2 : {A B : Obj1} → (f : B1.Hom A B) →
    Iso2 (B2.homCat (F.obj A) (G.obj B))
      (B2.hcomp1 (F.map1 f) (comp1 B))
      (B2.hcomp1 (comp1 A) (G.map1 f))
  -- 2-cell naturality: for any α : f ⇒ g,
  -- (F(α) ▷ σ_B) ≫ (σ_g).hom = (σ_f).hom ≫ (σ_A ◁ G(α))
  naturality2 : ∀ {A B : Obj1} {f g : B1.Hom A B} (α : B1.Hom2 f g),
    (B2.homCat (F.obj A) (G.obj B)).vcomp (B2.whiskerRight (F.map2 α) (comp1 B)) (comp2 g).hom =
      (B2.homCat (F.obj A) (G.obj B)).vcomp (comp2 f).hom (B2.whiskerLeft (comp1 A) (G.map2 α))
  -- Composition coherence: compatibility with compositor 2-isomorphisms
  comp_coherence : ∀ {A B C : Obj1} (f : B1.Hom A B) (g : B1.Hom B C),
    let l1 := B2.whiskerRight (F.compositor f g).hom (comp1 C)
    let l2 := (comp2 (B1.hcomp1 f g)).hom
    let r1 := (B2.associator (F.map1 f) (F.map1 g) (comp1 C)).hom
    let r2 := B2.whiskerLeft (F.map1 f) (comp2 g).hom
    let r3 := (B2.associator (F.map1 f) (comp1 B) (G.map1 g)).inv
    let r4 := B2.whiskerRight (comp2 f).hom (G.map1 g)
    let r5 := (B2.associator (comp1 A) (G.map1 f) (G.map1 g)).hom
    let r6 := B2.whiskerLeft (comp1 A) (G.compositor f g).hom
    (B2.homCat (F.obj A) (G.obj C)).vcomp l1 l2 =
      (B2.homCat (F.obj A) (G.obj C)).vcomp r1
        ((B2.homCat (F.obj A) (G.obj C)).vcomp r2
          ((B2.homCat (F.obj A) (G.obj C)).vcomp r3
            ((B2.homCat (F.obj A) (G.obj C)).vcomp r4
              ((B2.homCat (F.obj A) (G.obj C)).vcomp r5 r6))))
  -- Identity coherence, including both pseudofunctor unitors.
  id_coherence : ∀ (A : Obj1),
    (B2.homCat (F.obj A) (G.obj A)).vcomp
      (B2.whiskerRight (F.unitor A).hom (comp1 A)) (comp2 (B1.id1 A)).hom =
    (B2.homCat (F.obj A) (G.obj A)).vcomp (B2.leftUnitor (comp1 A)).hom
      ((B2.homCat (F.obj A) (G.obj A)).vcomp (B2.rightUnitor (comp1 A)).inv
        (B2.whiskerLeft (comp1 A) (G.unitor A).hom))

namespace PseudoNatTrans

variable {Obj1 : Type u1} {Obj2 : Type u2}
variable {B1 : Bicategory.{u1, v1, w1} Obj1} {B2 : Bicategory.{u2, v2, w2} Obj2}
variable {F G : Pseudofunctor B1 B2}

/-- A 2-natural transformation is strict if its comparison 2-cells are equalities. -/
def IsStrict (σ : PseudoNatTrans F G) : Prop :=
  ∀ {A B : Obj1} (f : B1.Hom A B),
    ∃ p : B2.hcomp1 (F.map1 f) (σ.comp1 B) = B2.hcomp1 (σ.comp1 A) (G.map1 f),
      σ.comp2 f = eqToIso2 (B2.homCat (F.obj A) (G.obj B)) p

end PseudoNatTrans

/-- Strict 2-natural endotransformation of the identity 2-functor on C. -/
structure Strict2NatTrans {Obj : Type u1} (C : Strict2Category Obj) where
  comp1 : (A : Obj) → C.Hom A A
  naturality : ∀ {A B : Obj} (f : C.Hom A B),
    C.hcomp1 f (comp1 B) = C.hcomp1 (comp1 A) f
  naturality2 : ∀ {A B : Obj} {f g : C.Hom A B} (α : C.Hom2 f g),
    HEq (C.hcomp2 α ((C.homCat B B).id2 (comp1 B)))
      (C.hcomp2 ((C.homCat A A).id2 (comp1 A)) α)

/-- Identity strict 2-natural transformation on any strict 2-category. -/
def Strict2NatTrans.id {Obj : Type u1} (C : Strict2Category Obj) : Strict2NatTrans C where
  comp1 := fun A => C.id1 A
  naturality := fun {A B} f => by
    rw [C.hcomp1_id1, C.id1_hcomp1]
  naturality2 := fun α => (C.hcomp2_id1 α).trans (C.id1_hcomp2 α).symm

/-- A Modification μ : σ ⇛ τ between pseudonatural transformations σ, τ : F ⇒ G consists of:
    - A family of 2-cells μ_A : σ_A ⇒ τ_A in B2
    - Modification axiom: for all 1-cells f : A → B in B1,
      (F(f) ◁ μ_B) ≫ τ_f.hom = σ_f.hom ≫ (μ_A ▷ G(f)). -/
structure Modification {Obj1 : Type u1} {Obj2 : Type u2}
    {B1 : Bicategory.{u1, v1, w1} Obj1} {B2 : Bicategory.{u2, v2, w2} Obj2}
    {F G : Pseudofunctor B1 B2} (σ τ : PseudoNatTrans F G) where
  mod2 : (A : Obj1) → B2.Hom2 (σ.comp1 A) (τ.comp1 A)
  -- Modification axiom:
  -- (F(f) ◁ μ_B) ≫ τ_f.hom = σ_f.hom ≫ (μ_A ▷ G(f))
  mod_axiom : ∀ {A B : Obj1} (f : B1.Hom A B),
    (B2.homCat (F.obj A) (G.obj B)).vcomp (B2.whiskerLeft (F.map1 f) (mod2 B)) (τ.comp2 f).hom =
      (B2.homCat (F.obj A) (G.obj B)).vcomp (σ.comp2 f).hom (B2.whiskerRight (mod2 A) (G.map1 f))

namespace Modification

variable {Obj1 : Type u1} {Obj2 : Type u2}
variable {B1 : Bicategory.{u1, v1, w1} Obj1} {B2 : Bicategory.{u2, v2, w2} Obj2}
variable {F G : Pseudofunctor B1 B2}

/-- Identity modification on a pseudonatural transformation σ. -/
def id (σ : PseudoNatTrans F G) : Modification σ σ where
  mod2 := fun A => (B2.homCat (F.obj A) (G.obj A)).id2 (σ.comp1 A)
  mod_axiom := fun {A B} f => by
    have h1 : B2.whiskerLeft (F.map1 f) ((B2.homCat (F.obj B) (G.obj B)).id2 (σ.comp1 B)) =
      (B2.homCat _ _).id2 (B2.hcomp1 (F.map1 f) (σ.comp1 B)) := by
      rw [B2.whiskerLeft_eq, B2.hcomp2_id2]
    have h2 : B2.whiskerRight ((B2.homCat (F.obj A) (G.obj A)).id2 (σ.comp1 A)) (G.map1 f) =
      (B2.homCat _ _).id2 (B2.hcomp1 (σ.comp1 A) (G.map1 f)) := by
      rw [B2.whiskerRight_eq, B2.hcomp2_id2]
    rw [h1, h2]
    rw [(B2.homCat _ _).id2_vcomp, (B2.homCat _ _).vcomp_id2]

/-- Vertical composition of modifications. -/
def vcomp {σ τ ρ : PseudoNatTrans F G}
    (μ : Modification σ τ) (ν : Modification τ ρ) : Modification σ ρ where
  mod2 := fun A => (B2.homCat (F.obj A) (G.obj A)).vcomp (μ.mod2 A) (ν.mod2 A)
  mod_axiom := fun {A B} f => by
    have hL : (B2.homCat (F.obj A) (G.obj B)).vcomp
        (B2.whiskerLeft (F.map1 f) ((B2.homCat (F.obj B) (G.obj B)).vcomp (μ.mod2 B) (ν.mod2 B)))
        (ρ.comp2 f).hom =
      (B2.homCat (F.obj A) (G.obj B)).vcomp
        (B2.whiskerLeft (F.map1 f) (μ.mod2 B))
        ((B2.homCat (F.obj A) (G.obj B)).vcomp (B2.whiskerLeft (F.map1 f) (ν.mod2 B)) (ρ.comp2 f).hom) := by
      rw [B2.whiskerLeft_eq, B2.whiskerLeft_eq, B2.whiskerLeft_eq]
      rw [← (B2.homCat _ _).vcomp_assoc]
      have hint := (B2.interchange ((B2.homCat (F.obj A) (F.obj B)).id2 (F.map1 f))
        ((B2.homCat (F.obj A) (F.obj B)).id2 (F.map1 f)) (μ.mod2 B) (ν.mod2 B)).symm
      rw [(B2.homCat _ _).vcomp_id2] at hint
      rw [hint]
    rw [hL, ν.mod_axiom, ← (B2.homCat _ _).vcomp_assoc, μ.mod_axiom, (B2.homCat _ _).vcomp_assoc]
    have hR : (B2.homCat (F.obj A) (G.obj B)).vcomp
        (B2.whiskerRight (μ.mod2 A) (G.map1 f))
        (B2.whiskerRight (ν.mod2 A) (G.map1 f)) =
      B2.whiskerRight ((B2.homCat (F.obj A) (G.obj A)).vcomp (μ.mod2 A) (ν.mod2 A)) (G.map1 f) := by
      rw [B2.whiskerRight_eq, B2.whiskerRight_eq, B2.whiskerRight_eq]
      have hint := (B2.interchange (μ.mod2 A) (ν.mod2 A)
        ((B2.homCat (G.obj A) (G.obj B)).id2 (G.map1 f)) ((B2.homCat (G.obj A) (G.obj B)).id2 (G.map1 f))).symm
      rw [(B2.homCat _ _).vcomp_id2] at hint
      rw [hint]
    rw [hR]

end Modification

end HigherCategoryTheory
