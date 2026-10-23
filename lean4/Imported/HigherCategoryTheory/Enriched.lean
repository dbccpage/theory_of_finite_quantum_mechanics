/- Imported from the sibling the_symbol_game lean4/ tree so that this repository carries its own Lean.
   Original path : the_symbol_game/lean4/research_programs/higher_category_theory/Enriched.lean
   Original sha256: 2a4724877e4ffad2b69aa2542e04fc6a0376e9ff6cc582a7c776d244493c6491 (bytes as found)
   Imported on    : 2026-10-23
   Module         : Imported.HigherCategoryTheory.Enriched
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

universe u v

set_option linter.checkUnivs false
set_option linter.unusedVariables false

/-- An Enriched Category $\mathcal{C}$ over a monoidal category $\mathcal{V}$ consists of:
    - Objects `Obj : Type u`
    - Hom-objects $\mathcal{C}(X, Y) \in \text{Ob}(\mathcal{V})$
    - Composition morphisms $c_{X,Y,Z} : \mathcal{C}(Y, Z) \otimes \mathcal{C}(X, Y) \to \mathcal{C}(X, Z)$ in $\mathcal{V}$
    - Identity morphisms $j_X : I \to \mathcal{C}(X, X)$ in $\mathcal{V}$
    - Enriched associativity diagram commuting for all quadruples of objects
    - Enriched left and right unitor diagrams commuting for all pairs of objects -/
structure EnrichedCategory (Obj : Type u) {VObj : Type v}
    (V : MonoidalCategory.{v, v} VObj) where
  homObj : Obj → Obj → VObj
  compHom : (X Y Z : Obj) →
    V.cat.Hom (V.tensorObj (homObj Y Z) (homObj X Y)) (homObj X Z)
  idHom : (X : Obj) →
    V.cat.Hom V.unit (homObj X X)
  -- Enriched Associativity Diagram:
  -- c_{W,Y,Z} ∘ (id ⊗ c_{W,X,Y}) ∘ α = c_{W,X,Z} ∘ (c_{X,Y,Z} ⊗ id)
  assoc_commutes : ∀ (W X Y Z : Obj),
    V.cat.comp (V.associator (homObj Y Z) (homObj X Y) (homObj W X)).hom
      (V.cat.comp (V.tensorHom (V.cat.id (homObj Y Z)) (compHom W X Y)) (compHom W Y Z)) =
    V.cat.comp (V.tensorHom (compHom X Y Z) (V.cat.id (homObj W X))) (compHom W X Z)
  -- Enriched Left Unitor Diagram:
  -- c_{X,Y,Y} ∘ (j_Y ⊗ id) = λ
  left_unit_commutes : ∀ (X Y : Obj),
    V.cat.comp (V.tensorHom (idHom Y) (V.cat.id (homObj X Y))) (compHom X Y Y) =
      (V.leftUnitor (homObj X Y)).hom
  -- Enriched Right Unitor Diagram:
  -- c_{X,X,Y} ∘ (id ⊗ j_X) = ρ
  right_unit_commutes : ∀ (X Y : Obj),
    V.cat.comp (V.tensorHom (V.cat.id (homObj X Y)) (idHom X)) (compHom X X Y) =
      (V.rightUnitor (homObj X Y)).hom

namespace EnrichedCategory

variable {Obj : Type u} {VObj : Type v} {V : MonoidalCategory.{v, v} VObj}
    (E : EnrichedCategory Obj V)

/-- Constructive theorem: The enriched associativity diagram commutes for all quadruples of objects. -/
theorem enriched_assoc_commutes (W X Y Z : Obj) :
    V.cat.comp (V.associator (E.homObj Y Z) (E.homObj X Y) (E.homObj W X)).hom
      (V.cat.comp (V.tensorHom (V.cat.id (E.homObj Y Z)) (E.compHom W X Y)) (E.compHom W Y Z)) =
    V.cat.comp (V.tensorHom (E.compHom X Y Z) (V.cat.id (E.homObj W X))) (E.compHom W X Z) :=
  E.assoc_commutes W X Y Z

/-- Constructive theorem: The enriched left unitor diagram commutes for all pairs of objects. -/
theorem enriched_left_unit_commutes (X Y : Obj) :
    V.cat.comp (V.tensorHom (E.idHom Y) (V.cat.id (E.homObj X Y))) (E.compHom X Y Y) =
      (V.leftUnitor (E.homObj X Y)).hom :=
  E.left_unit_commutes X Y

/-- Constructive theorem: The enriched right unitor diagram commutes for all pairs of objects. -/
theorem enriched_right_unit_commutes (X Y : Obj) :
    V.cat.comp (V.tensorHom (V.cat.id (E.homObj X Y)) (E.idHom X)) (E.compHom X X Y) =
      (V.rightUnitor (E.homObj X Y)).hom :=
  E.right_unit_commutes X Y

/-- The underlying ordinary hom-types of a $\mathcal{V}$-enriched category. -/
def UnderlyingHom (X Y : Obj) : Type v :=
  V.cat.Hom V.unit (E.homObj X Y)

/-- Identity morphism in the underlying ordinary category $\mathcal{C}_0$. -/
def underlyingId (X : Obj) : UnderlyingHom E X X :=
  E.idHom X

/-- The underlying ordinary 1-category $\mathcal{C}_0$ of a $\mathcal{V}$-enriched category.
    Morphisms from $X$ to $Y$ are morphisms $I \to \mathcal{C}(X, Y)$ in $\mathcal{V}$. -/
structure UnderlyingCategory (Obj : Type u) {VObj : Type v}
    (V : MonoidalCategory.{v, v} VObj) (E : EnrichedCategory Obj V) where
  cat : Category.{u, v} Obj
  hom_def : ∀ (X Y : Obj), cat.Hom X Y = UnderlyingHom E X Y
  id_def : ∀ (X : Obj), (hom_def X X) ▸ (cat.id X) = underlyingId E X

end EnrichedCategory

end HigherCategoryTheory
