/-!
# Genesis Primitives Category 17: Weight Profiles & Ray Equivalence (Lean 4)

Extracted with full fidelity from 19L57G1:
- lean4/Derivation/WeightProfile.lean
- lean4/Derivation/CountTransport.lean

Classification: Genesis Foundation Substrate.
AuthorityEffect: None.
-/

namespace GenesisPrimitives.WeightProfile

/-- Discrete weight profile: mapping from finite points to non-negative integers. -/
def WeightFn (X : Type) := X → Nat

/-- Total mass of a weight function over a finite list carrier. -/
def totalMass {X : Type} (carrier : List X) (w : WeightFn X) : Nat :=
  (carrier.map w).foldl (· + ·) 0

/-- Ray equivalence in discrete projective space: two weight functions lie on the same ray
    if their cross-multiplied products agree on all elements (no division). -/
def SameRay {X : Type} (carrier : List X) (w v : WeightFn X) : Prop :=
  let tw := totalMass carrier w
  let tv := totalMass carrier v
  tw > 0 ∧ tv > 0 ∧ ∀ x, x ∈ carrier → w x * tv = v x * tw

/-- Reflexivity of discrete ray equivalence on positive mass profiles. -/
theorem sameRay_refl {X : Type} (carrier : List X) (w : WeightFn X)
    (h : totalMass carrier w > 0) : SameRay carrier w w :=
  ⟨h, h, fun _ _ => rfl⟩

/-- Symmetry of discrete ray equivalence via integer equality symmetry. -/
theorem sameRay_symm {X : Type} (carrier : List X) (w v : WeightFn X)
    (h : SameRay carrier w v) : SameRay carrier v w :=
  ⟨h.2.1, h.1, fun x hx => (h.2.2 x hx).symm⟩

end GenesisPrimitives.WeightProfile
