/- Imported so that this repository carries its own Lean evidence.
   Original sha256: 670e4493baa6345a265ec54a489e096b6839d070a773c7c16e8d120811fbc271 (bytes as found)
   Imported on    : 2026-10-23
   Module         : Imported.HigherCategoryTheory.TwoCategory
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

universe u v w

set_option linter.checkUnivs false

/-- Canonical 2-isomorphism induced by an equality of 1-cells. -/
def eqToIso2 {Hom : Type v} {Hom2 : Hom → Hom → Type w}
    (cat : HomCategory Hom Hom2) {f g : Hom} (h : f = g) : Iso2 cat f g := by
  subst h
  exact Iso2.refl cat f

@[simp]
theorem eqToIso2_refl {Hom : Type v} {Hom2 : Hom → Hom → Type w}
    (cat : HomCategory Hom Hom2) (f : Hom) :
    eqToIso2 cat (rfl : f = f) = Iso2.refl cat f := rfl

/-- Predicate characterizing when a bicategory is strict: its associators
    and unitors are trivial identity 2-isomorphisms (equalities). -/
def Bicategory.IsStrict {Obj : Type u} (B : Bicategory Obj) : Prop :=
  (∀ {A B' C' D : Obj} (f : B.Hom A B') (g : B.Hom B' C') (h : B.Hom C' D),
    ∃ p : B.hcomp1 (B.hcomp1 f g) h = B.hcomp1 f (B.hcomp1 g h),
      B.associator f g h = eqToIso2 (B.homCat A D) p) ∧
  (∀ {A B' : Obj} (f : B.Hom A B'), ∃ p : B.hcomp1 (B.id1 A) f = f,
    B.leftUnitor f = eqToIso2 (B.homCat A B') p) ∧
  (∀ {A B' : Obj} (f : B.Hom A B'), ∃ p : B.hcomp1 f (B.id1 B') = f,
    B.rightUnitor f = eqToIso2 (B.homCat A B') p)

/-- A Strict 2-Category is a higher category where 1-cell composition is strictly
    associative and strictly unital, and horizontal composition of 2-cells satisfies
    the interchange law. -/
structure Strict2Category (Obj : Type u) where
  Hom : Obj → Obj → Type v
  Hom2 : {A B : Obj} → Hom A B → Hom A B → Type w
  homCat : (A B : Obj) → HomCategory (Hom A B) (Hom2 (A := A) (B := B))
  id1 : (A : Obj) → Hom A A
  hcomp1 : {A B C : Obj} → Hom A B → Hom B C → Hom A C
  -- Strict associativity and unitality of 1-cells
  hcomp1_assoc : ∀ {A B C D : Obj} (f : Hom A B) (g : Hom B C) (h : Hom C D),
    hcomp1 (hcomp1 f g) h = hcomp1 f (hcomp1 g h)
  id1_hcomp1 : ∀ {A B : Obj} (f : Hom A B), hcomp1 (id1 A) f = f
  hcomp1_id1 : ∀ {A B : Obj} (f : Hom A B), hcomp1 f (id1 B) = f
  -- Horizontal composition of 2-cells
  hcomp2 : {A B C : Obj} → {f1 f2 : Hom A B} → {g1 g2 : Hom B C} →
    Hom2 f1 f2 → Hom2 g1 g2 → Hom2 (hcomp1 f1 g1) (hcomp1 f2 g2)
  hcomp2_id2 : ∀ {A B C : Obj} (f : Hom A B) (g : Hom B C),
    hcomp2 ((homCat A B).id2 f) ((homCat B C).id2 g) = (homCat A C).id2 (hcomp1 f g)
  -- Strictness also applies to 2-cells, with transport along the 1-cell equalities.
  hcomp2_assoc : ∀ {A B C D : Obj}
    {f1 f2 : Hom A B} {g1 g2 : Hom B C} {h1 h2 : Hom C D}
    (α : Hom2 f1 f2) (β : Hom2 g1 g2) (γ : Hom2 h1 h2),
    HEq (hcomp2 (hcomp2 α β) γ) (hcomp2 α (hcomp2 β γ))
  id1_hcomp2 : ∀ {A B : Obj} {f g : Hom A B} (α : Hom2 f g),
    HEq (hcomp2 ((homCat A A).id2 (id1 A)) α) α
  hcomp2_id1 : ∀ {A B : Obj} {f g : Hom A B} (α : Hom2 f g),
    HEq (hcomp2 α ((homCat B B).id2 (id1 B))) α
  -- Middle-four interchange law
  interchange : ∀ {A B C : Obj} {f1 f2 f3 : Hom A B} {g1 g2 g3 : Hom B C}
    (α : Hom2 f1 f2) (β : Hom2 f2 f3) (γ : Hom2 g1 g2) (δ : Hom2 g2 g3),
    hcomp2 ((homCat A B).vcomp α β) ((homCat B C).vcomp γ δ) =
      (homCat A C).vcomp (hcomp2 α γ) (hcomp2 β δ)

namespace Strict2Category

variable {Obj : Type u} (C : Strict2Category Obj)

/-- Left whiskering in a strict 2-category. -/
def whiskerLeft {A B' C' : Obj} (f : C.Hom A B') {g1 g2 : C.Hom B' C'}
    (β : C.Hom2 g1 g2) : C.Hom2 (C.hcomp1 f g1) (C.hcomp1 f g2) :=
  C.hcomp2 ((C.homCat A B').id2 f) β

/-- Right whiskering in a strict 2-category. -/
def whiskerRight {A B' C' : Obj} {f1 f2 : C.Hom A B'} (α : C.Hom2 f1 f2)
    (g : C.Hom B' C') : C.Hom2 (C.hcomp1 f1 g) (C.hcomp1 f2 g) :=
  C.hcomp2 α ((C.homCat B' C').id2 g)

/-- Canonical associator isomorphism in a strict 2-category. -/
def associator {A B' C' D : Obj} (f : C.Hom A B') (g : C.Hom B' C') (h : C.Hom C' D) :
    Iso2 (C.homCat A D) (C.hcomp1 (C.hcomp1 f g) h) (C.hcomp1 f (C.hcomp1 g h)) :=
  eqToIso2 (C.homCat A D) (C.hcomp1_assoc f g h)

/-- Canonical left unitor isomorphism in a strict 2-category. -/
def leftUnitor {A B : Obj} (f : C.Hom A B) :
    Iso2 (C.homCat A B) (C.hcomp1 (C.id1 A) f) f :=
  eqToIso2 (C.homCat A B) (C.id1_hcomp1 f)

/-- Canonical right unitor isomorphism in a strict 2-category. -/
def rightUnitor {A B : Obj} (f : C.Hom A B) :
    Iso2 (C.homCat A B) (C.hcomp1 f (C.id1 B)) f :=
  eqToIso2 (C.homCat A B) (C.hcomp1_id1 f)

/-- Whiskering exchange theorem for strict 2-categories. -/
theorem whisker_exchange {A B' C' : Obj} {f1 f2 : C.Hom A B'} {g1 g2 : C.Hom B' C'}
    (α : C.Hom2 f1 f2) (β : C.Hom2 g1 g2) :
    (C.homCat A C').vcomp (C.whiskerRight α g1) (C.whiskerLeft f2 β) =
      (C.homCat A C').vcomp (C.whiskerLeft f1 β) (C.whiskerRight α g2) := by
  have h1 : (C.homCat A C').vcomp (C.whiskerRight α g1) (C.whiskerLeft f2 β) = C.hcomp2 α β := by
    dsimp [whiskerRight, whiskerLeft]
    have eq := (C.interchange α ((C.homCat A B').id2 f2) ((C.homCat B' C').id2 g1) β).symm
    rw [eq]
    rw [(C.homCat A B').vcomp_id2, (C.homCat B' C').id2_vcomp]
  have h2 : (C.homCat A C').vcomp (C.whiskerLeft f1 β) (C.whiskerRight α g2) = C.hcomp2 α β := by
    dsimp [whiskerRight, whiskerLeft]
    have eq := (C.interchange ((C.homCat A B').id2 f1) α β ((C.homCat B' C').id2 g2)).symm
    rw [eq]
    rw [(C.homCat A B').id2_vcomp, (C.homCat B' C').vcomp_id2]
  rw [h1, h2]

end Strict2Category

end HigherCategoryTheory
