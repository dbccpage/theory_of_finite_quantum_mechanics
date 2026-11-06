/-!
# Genesis Primitives Category 15: Trace Algebra & Causal Concurrency (Lean 4)

Extracted with full fidelity from 19L57G1:
- lean4/Derivation/TraceAlgebra.lean

Classification: Genesis Foundation Substrate.
AuthorityEffect: None.
-/

namespace GenesisPrimitives.TraceAlgebra

/-- Independence relation: symmetric, irreflexive relation between commuting events. -/
structure IndependenceRelation (Event : Type) where
  indep : Event → Event → Prop
  irrefl : ∀ e, ¬ indep e e
  symm : ∀ e1 e2, indep e1 e2 → indep e2 e1

/-- Commutative transition record: executing independent steps in either order yields identical results. -/
structure CommutingPair (State Event : Type) (step : State → Event → State) where
  e1 : Event
  e2 : Event
  commutes : ∀ s, step (step s e1) e2 = step (step s e2) e1

/-- Mazurkiewicz trace monoid equivalence step. -/
inductive TraceEquiv (Event : Type) (I : IndependenceRelation Event) : List Event → List Event → Prop where
  | refl (l : List Event) : TraceEquiv Event I l l
  | swap (u v : List Event) (a b : Event) (h : I.indep a b) :
      TraceEquiv Event I (u ++ [a, b] ++ v) (u ++ [b, a] ++ v)
  | trans (l1 l2 l3 : List Event) :
      TraceEquiv Event I l1 l2 → TraceEquiv Event I l2 l3 → TraceEquiv Event I l1 l3

end GenesisPrimitives.TraceAlgebra
