/- Imported from the sibling the_symbol_game lean4/ tree so that this repository carries its own Lean.
   Original path : the_symbol_game/lean4/research_programs/higher_category_theory/Bicategory.lean
   Original sha256: d4fbee0e7ce6288cfbde7042569ebd06401e4cb9200885ebe20017ae607b8a62 (bytes as found)
   Imported on    : 2026-10-23
   Module         : Imported.HigherCategoryTheory.Bicategory
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

namespace HigherCategoryTheory

universe u v w

set_option linter.checkUnivs false

/-- The category structure on 1-cells between two 0-cells in a bicategory,
    governing vertical composition of 2-cells. -/
structure HomCategory (Hom : Type v) (Hom2 : Hom → Hom → Type w) where
  id2 : (f : Hom) → Hom2 f f
  vcomp : {f g h : Hom} → Hom2 f g → Hom2 g h → Hom2 f h
  vcomp_assoc : ∀ {f g h k : Hom} (α : Hom2 f g) (β : Hom2 g h) (γ : Hom2 h k),
    vcomp (vcomp α β) γ = vcomp α (vcomp β γ)
  id2_vcomp : ∀ {f g : Hom} (α : Hom2 f g), vcomp (id2 f) α = α
  vcomp_id2 : ∀ {f g : Hom} (α : Hom2 f g), vcomp α (id2 g) = α

/-- An invertible 2-cell (2-isomorphism) between two 1-cells. -/
structure Iso2 {Hom : Type v} {Hom2 : Hom → Hom → Type w}
    (cat : HomCategory Hom Hom2) (f g : Hom) where
  hom : Hom2 f g
  inv : Hom2 g f
  hom_inv_id : cat.vcomp hom inv = cat.id2 f
  inv_hom_id : cat.vcomp inv hom = cat.id2 g

/-- Identity 2-isomorphism. -/
def Iso2.refl {Hom : Type v} {Hom2 : Hom → Hom → Type w}
    (cat : HomCategory Hom Hom2) (f : Hom) : Iso2 cat f f where
  hom := cat.id2 f
  inv := cat.id2 f
  hom_inv_id := cat.vcomp_id2 (cat.id2 f)
  inv_hom_id := cat.vcomp_id2 (cat.id2 f)

/-- Inverse of a 2-isomorphism. -/
def Iso2.symm {Hom : Type v} {Hom2 : Hom → Hom → Type w}
    {cat : HomCategory Hom Hom2} {f g : Hom} (i : Iso2 cat f g) : Iso2 cat g f where
  hom := i.inv
  inv := i.hom
  hom_inv_id := i.inv_hom_id
  inv_hom_id := i.hom_inv_id

/-- Composition of 2-isomorphisms. -/
def Iso2.trans {Hom : Type v} {Hom2 : Hom → Hom → Type w}
    {cat : HomCategory Hom Hom2} {f g h : Hom}
    (i : Iso2 cat f g) (j : Iso2 cat g h) : Iso2 cat f h where
  hom := cat.vcomp i.hom j.hom
  inv := cat.vcomp j.inv i.inv
  hom_inv_id := by
    rw [cat.vcomp_assoc]
    rw [← cat.vcomp_assoc j.hom j.inv i.inv]
    rw [j.hom_inv_id]
    rw [cat.id2_vcomp]
    rw [i.hom_inv_id]
  inv_hom_id := by
    rw [cat.vcomp_assoc]
    rw [← cat.vcomp_assoc i.inv i.hom j.hom]
    rw [i.inv_hom_id]
    rw [cat.id2_vcomp]
    rw [j.inv_hom_id]

/-- A Bicategory consists of:
    - 0-cells `Obj`
    - 1-cells `Hom A B`
    - 2-cells `Hom2 f g`
    - Vertical composition and identity forming a category on each Hom(A, B)
    - Horizontal composition of 1-cells and 2-cells
    - Left and right whiskering operations
    - Associator 2-isomorphism
    - Left and right unitors
    - Middle-four interchange law
    - Coherence pentagon and triangle identities -/
structure Bicategory (Obj : Type u) where
  Hom : Obj → Obj → Type v
  Hom2 : {A B : Obj} → Hom A B → Hom A B → Type w
  homCat : (A B : Obj) → HomCategory (Hom A B) (Hom2 (A := A) (B := B))
  -- 1-cell identity and composition
  id1 : (A : Obj) → Hom A A
  hcomp1 : {A B C : Obj} → Hom A B → Hom B C → Hom A C
  -- Whiskering operations
  whiskerLeft : {A B C : Obj} → (f : Hom A B) → {g1 g2 : Hom B C} →
    Hom2 g1 g2 → Hom2 (hcomp1 f g1) (hcomp1 f g2)
  whiskerRight : {A B C : Obj} → {f1 f2 : Hom A B} →
    Hom2 f1 f2 → (g : Hom B C) → Hom2 (hcomp1 f1 g) (hcomp1 f2 g)
  -- 2-cell horizontal composition
  hcomp2 : {A B C : Obj} → {f1 f2 : Hom A B} → {g1 g2 : Hom B C} →
    Hom2 f1 f2 → Hom2 g1 g2 → Hom2 (hcomp1 f1 g1) (hcomp1 f2 g2)
  -- Whiskering relates to horizontal composition
  whiskerLeft_eq : ∀ {A B C : Obj} (f : Hom A B) {g1 g2 : Hom B C} (β : Hom2 g1 g2),
    whiskerLeft f β = hcomp2 ((homCat A B).id2 f) β
  whiskerRight_eq : ∀ {A B C : Obj} {f1 f2 : Hom A B} (α : Hom2 f1 f2) (g : Hom B C),
    whiskerRight α g = hcomp2 α ((homCat B C).id2 g)
  -- Horizontal composition preserves identity 2-cells
  hcomp2_id2 : ∀ {A B C : Obj} (f : Hom A B) (g : Hom B C),
    hcomp2 ((homCat A B).id2 f) ((homCat B C).id2 g) = (homCat A C).id2 (hcomp1 f g)
  -- Middle-four interchange law:
  -- (δ ∘_v γ) ∘_h (β ∘_v α) = (δ ∘_h β) ∘_v (γ ∘_h α)
  interchange : ∀ {A B C : Obj} {f1 f2 f3 : Hom A B} {g1 g2 g3 : Hom B C}
    (α : Hom2 f1 f2) (β : Hom2 f2 f3) (γ : Hom2 g1 g2) (δ : Hom2 g2 g3),
    hcomp2 ((homCat A B).vcomp α β) ((homCat B C).vcomp γ δ) =
      (homCat A C).vcomp (hcomp2 α γ) (hcomp2 β δ)
  -- Associator natural 2-isomorphism: (f ∘_h g) ∘_h h ≅ f ∘_h (g ∘_h h)
  associator : {A B C D : Obj} → (f : Hom A B) → (g : Hom B C) → (h : Hom C D) →
    Iso2 (homCat A D) (hcomp1 (hcomp1 f g) h) (hcomp1 f (hcomp1 g h))
  -- Left unitor: id ∘_h f ≅ f
  leftUnitor : {A B : Obj} → (f : Hom A B) →
    Iso2 (homCat A B) (hcomp1 (id1 A) f) f
  -- Right unitor: f ∘_h id ≅ f
  rightUnitor : {A B : Obj} → (f : Hom A B) →
    Iso2 (homCat A B) (hcomp1 f (id1 B)) f
  -- Naturality of associator
  associator_naturality : ∀ {A B C D : Obj}
    {f1 f2 : Hom A B} {g1 g2 : Hom B C} {h1 h2 : Hom C D}
    (α : Hom2 f1 f2) (β : Hom2 g1 g2) (γ : Hom2 h1 h2),
    (homCat A D).vcomp (hcomp2 (hcomp2 α β) γ) (associator f2 g2 h2).hom =
      (homCat A D).vcomp (associator f1 g1 h1).hom (hcomp2 α (hcomp2 β γ))
  -- Naturality of left unitor
  leftUnitor_naturality : ∀ {A B : Obj} {f1 f2 : Hom A B} (α : Hom2 f1 f2),
    (homCat A B).vcomp (whiskerLeft (id1 A) α) (leftUnitor f2).hom =
      (homCat A B).vcomp (leftUnitor f1).hom α
  -- Naturality of right unitor
  rightUnitor_naturality : ∀ {A B : Obj} {f1 f2 : Hom A B} (α : Hom2 f1 f2),
    (homCat A B).vcomp (whiskerRight α (id1 B)) (rightUnitor f2).hom =
      (homCat A B).vcomp (rightUnitor f1).hom α
  -- Mac Lane's Pentagon coherence axiom:
  pentagon : ∀ {A B C D E : Obj}
    (f : Hom A B) (g : Hom B C) (h : Hom C D) (k : Hom D E),
    let step1 := whiskerRight (associator f g h).hom k
    let step2 := (associator f (hcomp1 g h) k).hom
    let step3 := whiskerLeft f (associator g h k).hom
    let step4 := (associator (hcomp1 f g) h k).hom
    let step5 := (associator f g (hcomp1 h k)).hom
    (homCat A E).vcomp step1 ((homCat A E).vcomp step2 step3) =
      (homCat A E).vcomp step4 step5
  -- Mac Lane's Triangle coherence axiom:
  triangle : ∀ {A B C : Obj} (f : Hom A B) (g : Hom B C),
    (homCat A C).vcomp (associator f (id1 B) g).hom (whiskerLeft f (leftUnitor g).hom) =
      whiskerRight (rightUnitor f).hom g

/-- Whiskering exchange law derived from the middle-four interchange law. -/
theorem Bicategory.whisker_exchange {Obj : Type u} (B : Bicategory Obj) {A B' C : Obj}
    {f1 f2 : B.Hom A B'} {g1 g2 : B.Hom B' C}
    (α : B.Hom2 f1 f2) (β : B.Hom2 g1 g2) :
    (B.homCat A C).vcomp (B.whiskerRight α g1) (B.whiskerLeft f2 β) =
      (B.homCat A C).vcomp (B.whiskerLeft f1 β) (B.whiskerRight α g2) := by
  have h1 : (B.homCat A C).vcomp (B.whiskerRight α g1) (B.whiskerLeft f2 β) = B.hcomp2 α β := by
    rw [B.whiskerRight_eq, B.whiskerLeft_eq]
    have eq := (B.interchange α ((B.homCat A B').id2 f2) ((B.homCat B' C).id2 g1) β).symm
    rw [eq]
    rw [(B.homCat A B').vcomp_id2, (B.homCat B' C).id2_vcomp]
  have h2 : (B.homCat A C).vcomp (B.whiskerLeft f1 β) (B.whiskerRight α g2) = B.hcomp2 α β := by
    rw [B.whiskerRight_eq, B.whiskerLeft_eq]
    have eq := (B.interchange ((B.homCat A B').id2 f1) α β ((B.homCat B' C).id2 g2)).symm
    rw [eq]
    rw [(B.homCat A B').id2_vcomp, (B.homCat B' C).vcomp_id2]
  rw [h1, h2]

end HigherCategoryTheory
