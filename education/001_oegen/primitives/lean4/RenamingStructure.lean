/-!
# Genesis Primitives Category 11: Renaming Structures & Permutation Gauge (Lean 4)

Extracted with full fidelity from 19L57G1:
- lean4/Derivation/RenamingStructure.lean
- lean4/Derivation/FormRenaming.lean
- lean4/Derivation/IsoCanon.lean

Classification: Genesis Foundation Substrate.
AuthorityEffect: None.
-/

namespace GenesisPrimitives.RenamingStructure

/-- Bijection on a finite carrier type. -/
structure Permutation (X : Type) where
  toFun : X → X
  invFun : X → X
  left_inv : ∀ x, invFun (toFun x) = x
  right_inv : ∀ x, toFun (invFun x) = x

/-- Action of a permutation on a binary relation. -/
def actRel {X : Type} (p : Permutation X) (r : X → X → Prop) : X → X → Prop :=
  fun x y => r (p.invFun x) (p.invFun y)

/-- Automorphism condition: permutation stabilizes the relation. -/
def IsAutomorphism {X : Type} (p : Permutation X) (r : X → X → Prop) : Prop :=
  ∀ x y, actRel p r x y ↔ r x y

/-- Isomorphism between two relational carriers. -/
structure RelIso {X Y : Type} (rX : X → X → Prop) (rY : Y → Y → Prop) where
  toFun : X → Y
  invFun : Y → X
  left_inv : ∀ x, invFun (toFun x) = x
  right_inv : ∀ y, toFun (invFun y) = y
  preserves : ∀ x1 x2, rX x1 x2 ↔ rY (toFun x1) (toFun x2)

end GenesisPrimitives.RenamingStructure
