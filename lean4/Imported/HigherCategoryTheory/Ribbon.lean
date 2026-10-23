/- Imported from the sibling the_symbol_game lean4/ tree so that this repository carries its own Lean.
   Original path : the_symbol_game/lean4/research_programs/higher_category_theory/Ribbon.lean
   Original sha256: 5b4d07db8910d6c5e0593c847445976ab8daf3ff4d9edaf753de917d5bc8fbe4 (bytes as found)
   Imported on    : 2026-10-23
   Module         : Imported.HigherCategoryTheory.Ribbon
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

import Imported.HigherCategoryTheory.Braided

namespace HigherCategoryTheory

universe u v

set_option linter.checkUnivs false
set_option linter.unusedVariables false

/-- Rigid monoidal category structure: every object X has a dual object X^*
    equipped with evaluation and coevaluation morphisms satisfying the snake (zig-zag) equations. -/
structure RigidStructure (Obj : Type u) (mon : MonoidalCategory.{u, v} Obj) where
  dual : Obj → Obj
  ev : (X : Obj) → mon.cat.Hom (mon.tensorObj (dual X) X) mon.unit
  coev : (X : Obj) → mon.cat.Hom mon.unit (mon.tensorObj X (dual X))
  -- Left snake / zig-zag equation:
  -- X ≅ I ⊗ X ⟶ (X ⊗ X*) ⊗ X ≅ X ⊗ (X* ⊗ X) ⟶ X ⊗ I ≅ X equals id_X
  left_snake : ∀ (X : Obj),
    let c1 := (mon.leftUnitor X).inv
    let c2 := mon.tensorHom (coev X) (mon.cat.id X)
    let c3 := (mon.associator X (dual X) X).hom
    let c4 := mon.tensorHom (mon.cat.id X) (ev X)
    let c5 := (mon.rightUnitor X).hom
    mon.cat.comp c1 (mon.cat.comp c2 (mon.cat.comp c3 (mon.cat.comp c4 c5))) =
      mon.cat.id X
  -- Right snake / zig-zag equation:
  -- X* ≅ X* ⊗ I ⟶ X* ⊗ (X ⊗ X*) ≅ (X* ⊗ X) ⊗ X* ⟶ I ⊗ X* ≅ X* equals id_{X*}
  right_snake : ∀ (X : Obj),
    let c1 := (mon.rightUnitor (dual X)).inv
    let c2 := mon.tensorHom (mon.cat.id (dual X)) (coev X)
    let c3 := (mon.associator (dual X) X (dual X)).inv
    let c4 := mon.tensorHom (ev X) (mon.cat.id (dual X))
    let c5 := (mon.leftUnitor (dual X)).hom
    mon.cat.comp c1 (mon.cat.comp c2 (mon.cat.comp c3 (mon.cat.comp c4 c5))) =
      mon.cat.id (dual X)

/-- Dual of a morphism f : X → Y in a rigid monoidal category. -/
def dualMorphism {Obj : Type u} {mon : MonoidalCategory.{u, v} Obj}
    (rig : RigidStructure Obj mon) {X Y : Obj} (f : mon.cat.Hom X Y) :
    mon.cat.Hom (rig.dual Y) (rig.dual X) :=
  let c1 := (mon.rightUnitor (rig.dual Y)).inv
  let c2 := mon.tensorHom (mon.cat.id (rig.dual Y)) (rig.coev X)
  let c3 := (mon.associator (rig.dual Y) X (rig.dual X)).inv
  let c4 := mon.tensorHom (mon.tensorHom (mon.cat.id (rig.dual Y)) f) (mon.cat.id (rig.dual X))
  let c5 := mon.tensorHom (rig.ev Y) (mon.cat.id (rig.dual X))
  let c6 := (mon.leftUnitor (rig.dual X)).hom
  mon.cat.comp c1 (mon.cat.comp c2 (mon.cat.comp c3 (mon.cat.comp c4 (mon.cat.comp c5 c6))))

/-- A Ribbon Category (also known as a tortile category) is a braided monoidal
    category equipped with a compatible rigid structure and a ribbon twist
    automorphism θ_X : X ≅ X satisfying the ribbon axiom and duality compatibility. -/
structure RibbonCategory (Obj : Type u) where
  br : BraidedCategory.{u, v} Obj
  rigid : RigidStructure Obj br.mon
  -- Twist / ribbon natural automorphism: θ_X : X ≅ X
  twist : (X : Obj) → Iso br.mon.cat X X
  -- Naturality of twist: f ≫ θ_Y = θ_X ≫ f
  twist_naturality : ∀ {X Y : Obj} (f : br.mon.cat.Hom X Y),
    br.mon.cat.comp f (twist Y).hom = br.mon.cat.comp (twist X).hom f
  -- Ribbon Axiom: θ_{X ⊗ Y} = (θ_X ⊗ θ_Y) ≫ β_{X,Y} ≫ β_{Y,X}
  ribbon_axiom : ∀ (X Y : Obj),
    let θ_XY := (twist (br.mon.tensorObj X Y)).hom
    let θ_prod := br.mon.tensorHom (twist X).hom (twist Y).hom
    let double_b := br.mon.cat.comp (br.braiding X Y).hom (br.braiding Y X).hom
    θ_XY = br.mon.cat.comp θ_prod double_b
  -- Compatibility with duality: θ_{X*} = (θ_X)*
  twist_dual : ∀ (X : Obj),
    (twist (rigid.dual X)).hom = dualMorphism rigid (twist X).hom

namespace RibbonCategory

variable {Obj : Type u} (R : RibbonCategory.{u, v} Obj)

/-- Quantum Trace of an endomorphism f : X → X in a ribbon category:
    Tr_q(f) = ev_X ∘ β_{X, X*} ∘ ((f ∘ θ_X) ⊗ id_{X*}) ∘ coev_X : I → I. -/
def quantumTrace {X : Obj} (f : R.br.mon.cat.Hom X X) :
    R.br.mon.cat.Hom R.br.mon.unit R.br.mon.unit :=
  let step1 := R.rigid.coev X
  let f_twist := R.br.mon.cat.comp f (R.twist X).hom
  let step2 := R.br.mon.tensorHom f_twist (R.br.mon.cat.id (R.rigid.dual X))
  let step3 := (R.br.braiding X (R.rigid.dual X)).hom
  let step4 := R.rigid.ev X
  R.br.mon.cat.comp step1 (R.br.mon.cat.comp step2 (R.br.mon.cat.comp step3 step4))

/-- Quantum Dimension of an object X in a ribbon category:
    dim_q(X) = Tr_q(id_X) : I → I. -/
def quantumDim (X : Obj) : R.br.mon.cat.Hom R.br.mon.unit R.br.mon.unit :=
  R.quantumTrace (R.br.mon.cat.id X)

/-- Quantum trace of identity is quantum dimension by definition. -/
theorem quantumTrace_id_eq_quantumDim (X : Obj) :
    R.quantumTrace (R.br.mon.cat.id X) = R.quantumDim X := rfl

end RibbonCategory

end HigherCategoryTheory
