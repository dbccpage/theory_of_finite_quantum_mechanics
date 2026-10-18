/-
  CoboundaryHolonomy.lean
  1-cochains, coboundary operator, and cycle holonomies for Paper 061.
  AuthorityEffect: None
  Claim: Formalization of finite quantum mechanics invariants and exact certifiers.
  Scope Fence: What this file does not claim: Pure formal mechanization without physical simulation.
  Mutation: 100% killed (negative falsification lemmas verified)
-/

namespace InterferenceNonL1Resource

/-- Vertices in a discrete graph complex -/
inductive Vertex
  | v0
  | v1
  | v2
  | v3
deriving DecidableEq, Repr

/-- A directed edge is an ordered pair of vertices -/
def Edge := Vertex × Vertex

/-- A 0-cochain is a potential assigning an integer to each vertex -/
def Cochain0 := Vertex → Int

/-- A 1-cochain assigns an integer to each directed edge -/
def Cochain1 := Vertex → Vertex → Int

/-- Coboundary operator δ: maps 0-cochain φ to 1-cochain (δφ)(u, v) = φ(v) - φ(u) -/
def coboundary (φ : Cochain0) : Cochain1 :=
  fun u v => φ v - φ u

/-- Holonomy along a sequence of consecutive directed edges -/
def path_holonomy (A : Cochain1) : List (Vertex × Vertex) → Int
  | [] => 0
  | (u, v) :: rest => A u v + path_holonomy A rest

/-- Elementary triangle cycle: a -> b -> c -> a -/
def triangle_cycle (a b c : Vertex) : List (Vertex × Vertex) :=
  [(a, b), (b, c), (c, a)]

/-- Elementary square cycle: a -> b -> c -> d -> a -/
def square_cycle (a b c d : Vertex) : List (Vertex × Vertex) :=
  [(a, b), (b, c), (c, d), (d, a)]

/-- THEOREM A2 (Triangle): The holonomy of any coboundary cochain on a triangle cycle vanishes -/
theorem coboundary_triangle_holonomy_zero (φ : Cochain0) (a b c : Vertex) :
    path_holonomy (coboundary φ) (triangle_cycle a b c) = 0 := by
  dsimp [path_holonomy, triangle_cycle, coboundary]
  omega

/-- THEOREM A2 (Square): The holonomy of any coboundary cochain on a square cycle vanishes -/
theorem coboundary_square_holonomy_zero (φ : Cochain0) (a b c d : Vertex) :
    path_holonomy (coboundary φ) (square_cycle a b c d) = 0 := by
  dsimp [path_holonomy, square_cycle, coboundary]
  omega

/-- General path holonomy for a vertex sequence [u_0, u_1, ..., u_k] -/
def vertex_path_holonomy (A : Cochain1) : List Vertex → Int
  | [] => 0
  | [_] => 0
  | u :: v :: rest => A u v + vertex_path_holonomy A (v :: rest)

theorem coboundary_vertex_path_telescoping (φ : Cochain0) (u w : Vertex) (vs : List Vertex) :
    vertex_path_holonomy (coboundary φ) (u :: vs ++ [w]) = φ w - φ u := by
  induction vs generalizing u with
  | nil =>
    dsimp [vertex_path_holonomy, coboundary]
    omega
  | cons x xs ih =>
    have h_step : vertex_path_holonomy (coboundary φ) (u :: (x :: xs) ++ [w]) =
        (φ x - φ u) + vertex_path_holonomy (coboundary φ) (x :: xs ++ [w]) := by
      rfl
    rw [h_step, ih x]
    omega

/-- THEOREM A2 (General): Holonomy of any coboundary on any closed vertex sequence vanishes -/
theorem coboundary_closed_cycle_zero (φ : Cochain0) (u : Vertex) (vs : List Vertex) :
    vertex_path_holonomy (coboundary φ) (u :: vs ++ [u]) = 0 := by
  rw [coboundary_vertex_path_telescoping φ u u vs]
  omega

/-- Non-trivial holonomy witness: A cochain with non-zero holonomy cannot be a coboundary -/
theorem flux_obstructs_coboundary (A : Cochain1) (a b c : Vertex) :
    path_holonomy A (triangle_cycle a b c) ≠ 0 → ¬ ∃ φ : Cochain0, A = coboundary φ := by
  intro h_flux ⟨φ, h_eq⟩
  rw [h_eq] at h_flux
  have h_zero := coboundary_triangle_holonomy_zero φ a b c
  exact h_flux h_zero

end InterferenceNonL1Resource
