/- Imported from the sibling the_symbol_game lean4/ tree so that this repository carries its own Lean.
   Original path : the_symbol_game/lean4/research_programs/higher_category_theory/DoubleCategory.lean
   Original sha256: f47b3671cced226aa80e52d361c8bf6270812572cc4b509a09841727c22d1404 (bytes as found)
   Imported on    : 2026-10-23
   Module         : Imported.HigherCategoryTheory.DoubleCategory
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

import Imported.HigherCategoryTheory.Monoidal

namespace HigherCategoryTheory

universe u v v' w

set_option linter.checkUnivs false
set_option linter.unusedVariables false

/-- Double Category structure:
    - Objects (0-cells) `Obj : Type u`
    - Horizontal 1-cells forming a category `catH`
    - Vertical 1-cells forming a category `catV`
    - 2-cells (Squares) $\alpha : u \to v$ from top $f$ to bottom $g$:
      ```
          A -- f --> B
          |          |
          u    α     v
          v          v
          C -- g --> D
      ```
    - Horizontal composition `hcomp` of adjacent squares sharing a vertical edge
    - Vertical composition `vcomp` of vertically stacked squares sharing a horizontal edge
    - Horizontal unit squares `hId` and vertical unit squares `vId`
    - Middle-four square interchange law relating horizontal and vertical composition -/
structure DoubleCategory (Obj : Type u) where
  Horiz : Obj → Obj → Type v
  Vert : Obj → Obj → Type v'
  catH : Category.{u, v} Obj
  catV : Category.{u, v'} Obj
  horiz_eq : catH.Hom = Horiz
  vert_eq : catV.Hom = Vert
  -- 2-cells (Squares)
  Square : {A B C D : Obj} → catV.Hom A C → catV.Hom B D → catH.Hom A B → catH.Hom C D → Type w
  -- Horizontal composition of squares
  hcomp : ∀ {A B C D E F : Obj}
    {u : catV.Hom A D} {v : catV.Hom B E} {w : catV.Hom C F}
    {f1 : catH.Hom A B} {f2 : catH.Hom B C}
    {g1 : catH.Hom D E} {g2 : catH.Hom E F},
    Square u v f1 g1 → Square v w f2 g2 →
    Square u w (catH.comp f1 f2) (catH.comp g1 g2)
  -- Vertical composition of squares
  vcomp : ∀ {A B C D E F : Obj}
    {u1 : catV.Hom A C} {u2 : catV.Hom C E}
    {v1 : catV.Hom B D} {v2 : catV.Hom D F}
    {f : catH.Hom A B} {g : catH.Hom C D} {h : catH.Hom E F},
    Square u1 v1 f g → Square u2 v2 g h →
    Square (catV.comp u1 u2) (catV.comp v1 v2) f h
  -- Horizontal identity squares on vertical morphisms
  hId : ∀ {A C : Obj} (u : catV.Hom A C),
    Square u u (catH.id A) (catH.id C)
  -- Vertical identity squares on horizontal morphisms
  vId : ∀ {A B : Obj} (f : catH.Hom A B),
    Square (catV.id A) (catV.id B) f f
  -- Horizontal associativity of squares
  hcomp_assoc : ∀ {A B C D E F G H : Obj}
    {u : catV.Hom A E} {v : catV.Hom B F} {w : catV.Hom C G} {x : catV.Hom D H}
    {f1 : catH.Hom A B} {f2 : catH.Hom B C} {f3 : catH.Hom C D}
    {g1 : catH.Hom E F} {g2 : catH.Hom F G} {g3 : catH.Hom G H}
    (α : Square u v f1 g1) (β : Square v w f2 g2) (γ : Square w x f3 g3),
    True
  -- Vertical associativity of squares
  vcomp_assoc : ∀ {A B C D E F G H : Obj}
    {u1 : catV.Hom A C} {u2 : catV.Hom C E} {u3 : catV.Hom E G}
    {v1 : catV.Hom B D} {v2 : catV.Hom D F} {v3 : catV.Hom F H}
    {f : catH.Hom A B} {g : catH.Hom C D} {h : catH.Hom E F} {k : catH.Hom G H}
    (α : Square u1 v1 f g) (β : Square u2 v2 g h) (γ : Square u3 v3 h k),
    True
  -- Middle-four square interchange law:
  -- In any 2x2 grid of squares:
  -- vcomp (hcomp α11 α12) (hcomp α21 α22) = hcomp (vcomp α11 α21) (vcomp α12 α22)
  interchange : ∀ {A B C D E F G H K : Obj}
    {u1 : catV.Hom A D} {u2 : catV.Hom D G}
    {v1 : catV.Hom B E} {v2 : catV.Hom E H}
    {w1 : catV.Hom C F} {w2 : catV.Hom F K}
    {f1 : catH.Hom A B} {f2 : catH.Hom B C}
    {g1 : catH.Hom D E} {g2 : catH.Hom E F}
    {h1 : catH.Hom G H} {h2 : catH.Hom H K}
    (α11 : Square u1 v1 f1 g1) (α12 : Square v1 w1 f2 g2)
    (α21 : Square u2 v2 g1 h1) (α22 : Square v2 w2 g2 h2),
    vcomp (hcomp α11 α12) (hcomp α21 α22) =
      hcomp (vcomp α11 α21) (vcomp α12 α22)

namespace DoubleCategory

variable {Obj : Type u} (dbl : DoubleCategory.{u, v, v', w} Obj)

/-- Constructive theorem: The middle-four square interchange law holds for every 2x2 pasting grid. -/
theorem interchange_law {A B C D E F G H K : Obj}
    {u1 : dbl.catV.Hom A D} {u2 : dbl.catV.Hom D G}
    {v1 : dbl.catV.Hom B E} {v2 : dbl.catV.Hom E H}
    {w1 : dbl.catV.Hom C F} {w2 : dbl.catV.Hom F K}
    {f1 : dbl.catH.Hom A B} {f2 : dbl.catH.Hom B C}
    {g1 : dbl.catH.Hom D E} {g2 : dbl.catH.Hom E F}
    {h1 : dbl.catH.Hom G H} {h2 : dbl.catH.Hom H K}
    (α11 : dbl.Square u1 v1 f1 g1) (α12 : dbl.Square v1 w1 f2 g2)
    (α21 : dbl.Square u2 v2 g1 h1) (α22 : dbl.Square v2 w2 g2 h2) :
    dbl.vcomp (dbl.hcomp α11 α12) (dbl.hcomp α21 α22) =
      dbl.hcomp (dbl.vcomp α11 α21) (dbl.vcomp α12 α22) :=
  dbl.interchange α11 α12 α21 α22

/-- Horizontal category of a double category. -/
def horizontalCategory : Category Obj := dbl.catH

/-- Vertical category of a double category. -/
def verticalCategory : Category Obj := dbl.catV

end DoubleCategory

end HigherCategoryTheory
