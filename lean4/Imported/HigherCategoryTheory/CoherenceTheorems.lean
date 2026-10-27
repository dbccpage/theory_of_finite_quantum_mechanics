/- Imported so that this repository carries its own Lean evidence.
   Original sha256: 093a78e4295db87030789e22bc4c890065cbbac6f16e8c9742b2f68f57262e3f (bytes as found)
   Imported on    : 2026-10-23
   Module         : Imported.HigherCategoryTheory.CoherenceTheorems
   Reason         : HCT
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
/-
Released under Apache 2.0 license as described in the file LICENSE.
-/

import Imported.HigherCategoryTheory.Bicategory
import Imported.HigherCategoryTheory.TwoCategory
import Imported.HigherCategoryTheory.Monoidal
import Imported.HigherCategoryTheory.Braided
import Imported.HigherCategoryTheory.Ribbon

namespace HigherCategoryTheory

universe u v w

set_option linter.checkUnivs false
set_option linter.unusedVariables false

/-!
# Coherence Theorems in Higher Category Theory

This module constructively establishes Mac Lane's pentagon and triangle coherence diagrams
as theorems on canonical models, rather than unverified axioms.
-/

section CartesianCoherence

/-- The canonical category of types and functions. -/
def typeCat : Category.{u + 1, u} (Type u) where
  Hom := fun X Y => X → Y
  id := fun X => id
  comp := fun f g => g ∘ f
  comp_assoc := fun f g h => rfl
  id_comp := fun f => rfl
  comp_id := fun f => rfl

/-- The canonical product associator isomorphism between types. -/
def prodAssociator (W X Y : Type u) : Iso typeCat ((W × X) × Y) (W × (X × Y)) where
  hom := fun ((w, x), y) => (w, (x, y))
  inv := fun (w, (x, y)) => ((w, x), y)
  hom_inv_id := rfl
  inv_hom_id := rfl

/-- The canonical product left unitor isomorphism. -/
def prodLeftUnitor (X : Type u) : Iso typeCat (PUnit × X) X where
  hom := fun (_, x) => x
  inv := fun x => (PUnit.unit, x)
  hom_inv_id := by
    funext p
    cases p
    rename_i u x
    cases u
    rfl
  inv_hom_id := rfl

/-- The canonical product right unitor isomorphism. -/
def prodRightUnitor (X : Type u) : Iso typeCat (X × PUnit) X where
  hom := fun (x, _) => x
  inv := fun x => (x, PUnit.unit)
  hom_inv_id := by
    funext p
    cases p
    rename_i x u
    cases u
    rfl
  inv_hom_id := rfl

/-- Concrete proof of Mac Lane's Pentagon Theorem for the cartesian product monoidal structure. -/
theorem cartesian_pentagon_theorem (W X Y Z : Type u) :
    let step1 : ((W × X) × Y) × Z → (W × (X × Y)) × Z := fun (((w, x), y), z) => ((w, (x, y)), z)
    let step2 : (W × (X × Y)) × Z → W × ((X × Y) × Z) := fun ((w, xy), z) => (w, (xy, z))
    let step3 : W × ((X × Y) × Z) → W × (X × (Y × Z)) := fun (w, ((x, y), z)) => (w, (x, (y, z)))
    let step4 : ((W × X) × Y) × Z → (W × X) × (Y × Z) := fun (((w, x), y), z) => ((w, x), (y, z))
    let step5 : (W × X) × (Y × Z) → W × (X × (Y × Z)) := fun ((w, x), yz) => (w, (x, yz))
    (step3 ∘ step2 ∘ step1) = (step5 ∘ step4) := by
  funext (((w, x), y), z)
  rfl

/-- Concrete proof of Mac Lane's Triangle Theorem for the cartesian product monoidal structure. -/
theorem cartesian_triangle_theorem (X Y : Type u) :
    let assoc : (X × PUnit) × Y → X × (PUnit × Y) := fun ((x, u), y) => (x, (u, y))
    let left_unitor_act : X × (PUnit × Y) → X × Y := fun (x, (_, y)) => (x, y)
    let right_unitor_act : (X × PUnit) × Y → X × Y := fun ((x, _), y) => (x, y)
    (left_unitor_act ∘ assoc) = right_unitor_act := by
  funext ((x, u), y)
  rfl

end CartesianCoherence

section StrictCoherence

/-- Equality proofs between the same 1-cell endpoints agree by proof irrelevance.
    This is not a proof of equality of arbitrary associator 2-cells. -/
theorem strict_pentagon_equality_paths {Obj : Type u} (C : Strict2Category Obj)
    {A B C' D E : Obj} (f : C.Hom A B) (g : C.Hom B C') (h : C.Hom C' D) (k : C.Hom D E) :
    let p1 : C.hcomp1 (C.hcomp1 (C.hcomp1 f g) h) k = C.hcomp1 (C.hcomp1 f (C.hcomp1 g h)) k := by
      rw [C.hcomp1_assoc f g h]
    let p2 : C.hcomp1 (C.hcomp1 f (C.hcomp1 g h)) k = C.hcomp1 f (C.hcomp1 (C.hcomp1 g h) k) :=
      C.hcomp1_assoc f (C.hcomp1 g h) k
    let p3 : C.hcomp1 f (C.hcomp1 (C.hcomp1 g h) k) = C.hcomp1 f (C.hcomp1 g (C.hcomp1 h k)) := by
      rw [C.hcomp1_assoc g h k]
    let q1 : C.hcomp1 (C.hcomp1 (C.hcomp1 f g) h) k = C.hcomp1 (C.hcomp1 f g) (C.hcomp1 h k) :=
      C.hcomp1_assoc (C.hcomp1 f g) h k
    let q2 : C.hcomp1 (C.hcomp1 f g) (C.hcomp1 h k) = C.hcomp1 f (C.hcomp1 g (C.hcomp1 h k)) :=
      C.hcomp1_assoc f g (C.hcomp1 h k)
    (p1.trans (p2.trans p3)) = (q1.trans q2) := by
  rfl

/-- The two proofs of the 1-cell unit equality agree by proof irrelevance. -/
theorem strict_triangle_equality_paths {Obj : Type u} (C : Strict2Category Obj)
    {A B C' : Obj} (f : C.Hom A B) (g : C.Hom B C') :
    let p1 : C.hcomp1 (C.hcomp1 f (C.id1 B)) g = C.hcomp1 f (C.hcomp1 (C.id1 B) g) :=
      C.hcomp1_assoc f (C.id1 B) g
    let p2 : C.hcomp1 f (C.hcomp1 (C.id1 B) g) = C.hcomp1 f g := by
      rw [C.id1_hcomp1 g]
    let q : C.hcomp1 (C.hcomp1 f (C.id1 B)) g = C.hcomp1 f g := by
      rw [C.hcomp1_id1 f]
    (p1.trans p2) = q := by
  rfl

end StrictCoherence

section InterchangeTheorems

/-- The middle-four interchange law is assumed by the structure for any pair of vertically
    and horizontally composable 2-cells in a bicategory. -/
theorem interchange_law_theorem {Obj : Type u} (B : Bicategory Obj)
    {A B' C : Obj} {f1 f2 f3 : B.Hom A B'} {g1 g2 g3 : B.Hom B' C}
    (α : B.Hom2 f1 f2) (β : B.Hom2 f2 f3) (γ : B.Hom2 g1 g2) (δ : B.Hom2 g2 g3) :
    B.hcomp2 ((B.homCat A B').vcomp α β) ((B.homCat B' C).vcomp γ δ) =
      (B.homCat A C).vcomp (B.hcomp2 α γ) (B.hcomp2 β δ) :=
  B.interchange α β γ δ

/-- The monoidal interchange law holds for tensor products of composite morphisms. -/
theorem monoidal_interchange_theorem {Obj : Type u} (M : MonoidalCategory Obj)
    {X1 X2 X3 Y1 Y2 Y3 : Obj}
    (f1 : M.cat.Hom X1 X2) (f2 : M.cat.Hom X2 X3)
    (g1 : M.cat.Hom Y1 Y2) (g2 : M.cat.Hom Y2 Y3) :
    M.tensorHom (M.cat.comp f1 f2) (M.cat.comp g1 g2) =
      M.cat.comp (M.tensorHom f1 g1) (M.tensorHom f2 g2) :=
  M.tensorHom_comp f1 f2 g1 g2

end InterchangeTheorems

section RibbonTheorems

/-- In any ribbon category, the assumed ribbon law expresses a tensor product twist as
    the tensor product of individual twists followed by double braiding. -/
theorem ribbon_twist_product_theorem {Obj : Type u} (R : RibbonCategory Obj) (X Y : Obj) :
    let θ_XY := (R.twist (R.br.mon.tensorObj X Y)).hom
    let θ_prod := R.br.mon.tensorHom (R.twist X).hom (R.twist Y).hom
    let double_b := R.br.mon.cat.comp (R.br.braiding X Y).hom (R.br.braiding Y X).hom
    θ_XY = R.br.mon.cat.comp θ_prod double_b :=
  R.ribbon_axiom X Y

/-- Quantum dimension is the quantum trace of the identity morphism. -/
theorem quantum_dim_def_theorem {Obj : Type u} (R : RibbonCategory Obj) (X : Obj) :
    R.quantumDim X = R.quantumTrace (R.br.mon.cat.id X) :=
  rfl

end RibbonTheorems

end HigherCategoryTheory
