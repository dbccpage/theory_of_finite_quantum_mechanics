/-!
# Simplicial Complexes & Boundary Cancellation (Lean 4)

Extracted with full fidelity from 19L57G1:
- lean4/Derivation/HigherStructure.lean
- lean4/Derivation/BoundaryCancellation.lean

Classification: Simplicial calculus and homological boundary algebra.
AuthorityEffect: None.
-/

namespace GenesisPrimitives.SimplicialComplex

abbrev Vertex := Nat
abbrev Edge := Nat × Nat
abbrev Tri := Nat × Nat × Nat
abbrev Tet := Nat × Nat × Nat × Nat
abbrev Cell := List Nat

/-- 4-graded Simplicial Complex: vertices, edges, triangles, tetrahedra. -/
structure Complex where
  c0 : List Vertex
  c1 : List Edge
  c2 : List Tri
  c3 : List Tet
deriving Repr, DecidableEq

/-- Simplicial cell attachment events. -/
inductive CEvent where
  | addV (v : Vertex)
  | addE (i j : Vertex)
  | addT (i j k : Vertex)
  | addQ (i j k l : Vertex)
deriving Repr, DecidableEq

/-- Simplicial Chain: list of signed cells (sign, cell). -/
abbrev Chain := List (Int × Cell)

/-- Alternating sign (-1)^i. -/
def sgn (i : Nat) : Int :=
  if i % 2 == 0 then 1 else -1

/-- Erase index from cell list. -/
def eraseIdx (sigma : Cell) (i : Nat) : Cell :=
  sigma.eraseIdx i

/-- Strict ascent predicate: cell vertices strictly ascending. -/
def asc : Cell → Bool
  | [] => true
  | [_] => true
  | x :: y :: rest => (x < y) && asc (y :: rest)

end GenesisPrimitives.SimplicialComplex
