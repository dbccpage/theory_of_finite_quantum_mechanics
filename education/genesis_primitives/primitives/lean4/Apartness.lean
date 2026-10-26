/-!
# Genesis Primitives Category 8: Constructive Positive Apartness (Lean 4)

Extracted with full fidelity from 19L57G1:
- lean4/Derivation/Apartness.lean

Classification: Genesis Foundation Substrate.
AuthorityEffect: None.
-/

namespace GenesisPrimitives.Apartness

/-- Positive apartness: irreflexive, symmetric, cotransitive. -/
structure IsApart {X : Type} (r : X → X → Prop) : Prop where
  irrefl : ∀ x, ¬ r x x
  symm : ∀ x y, r x y → r y x
  cotrans : ∀ x y, r x y → ∀ z, r x z ∨ r z y

/-- Indistinguishability: the negation of apartness. -/
def Indist {X : Type} (r : X → X → Prop) (x y : X) : Prop := ¬ r x y

/-- Reflexivity of indistinguishability from irreflexivity of apartness. -/
theorem indist_refl {X : Type} {r : X → X → Prop} (h : IsApart r) :
    ∀ x, Indist r x x := h.irrefl

/-- Symmetry of indistinguishability from symmetry of apartness. -/
theorem indist_symm {X : Type} {r : X → X → Prop} (h : IsApart r)
    {x y : X} (hxy : Indist r x y) : Indist r y x :=
  fun hyx => hxy (h.symm y x hyx)

/-- Transitivity of indistinguishability: spent from cotransitivity. -/
theorem indist_trans {X : Type} {r : X → X → Prop} (h : IsApart r)
    {x y z : X} (hxy : Indist r x y) (hyz : Indist r y z) :
    Indist r x z :=
  fun hxz =>
    match h.cotrans x z hxz y with
    | Or.inl hxy' => hxy hxy'
    | Or.inr hyz' => hyz hyz'

/-- Indistinguishability under positive apartness is an equivalence relation. -/
theorem indist_equivalence {X : Type} {r : X → X → Prop}
    (h : IsApart r) :
    (∀ x, Indist r x x) ∧
    (∀ x y, Indist r x y → Indist r y x) ∧
    (∀ x y z, Indist r x y → Indist r y z → Indist r x z) :=
  ⟨indist_refl h,
   fun _ _ => indist_symm h,
   fun _ _ _ => indist_trans h⟩

/-- Tight apartness: non-apartness implies propositional equality. -/
def IsTightApart {X : Type} (r : X → X → Prop) : Prop :=
  IsApart r ∧ ∀ x y, Indist r x y → x = y

end GenesisPrimitives.Apartness
