/-!
# Genesis Primitives Category 19: Endogenous Fidelity & No-Outside Invariants (Lean 4)

Extracted with full fidelity from 19L57G1:
- lean4/Derivation/NoOutside.lean
- lean4/Derivation/FidelityClosure.lean
- lean4/Derivation/Breaking.lean

Classification: Genesis Foundation Substrate.
AuthorityEffect: None.
-/

namespace GenesisPrimitives.EndogenousFidelity

/-- The operational support of a relational configuration. -/
structure OperationalSupport (Data View Req Refusal : Type) where
  data : List Data
  views : List (List Data)
  reqs : List (Data × Data)
  refusals : List (Data × Data)

/-- The Effectual-Outside Dichotomy: any distinction that alters an operational
    evaluation must already reside within the represented support. -/
def EffectualOutsideDichotomy (World : Type) (supp : World → OperationalSupport Nat Nat Nat Nat)
    (eval : World → Bool) : Prop :=
  ∀ w1 w2 : World, supp w1 = supp w2 → eval w1 = eval w2

/-- Explicit witness certifying the breaking of a relational symmetry. -/
structure SymmetryBreakingWitness (X : Type) (r : X → X → Prop) where
  x : X
  y : X
  symmetry_broken : r x y ∧ ¬ r y x

end GenesisPrimitives.EndogenousFidelity
