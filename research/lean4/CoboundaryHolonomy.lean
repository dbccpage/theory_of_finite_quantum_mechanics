
namespace InterferenceNonL1Resource

inductive Vertex
  | v0
  | v1
  | v2
  | v3
deriving DecidableEq, Repr

def Edge := Vertex × Vertex

def Cochain0 := Vertex → Int

def Cochain1 := Vertex → Vertex → Int

def coboundary (φ : Cochain0) : Cochain1 :=
  fun u v => φ v - φ u

def path_holonomy (A : Cochain1) : List (Vertex × Vertex) → Int
  | [] => 0
  | (u, v) :: rest => A u v + path_holonomy A rest

def triangle_cycle (a b c : Vertex) : List (Vertex × Vertex) :=
  [(a, b), (b, c), (c, a)]

def square_cycle (a b c d : Vertex) : List (Vertex × Vertex) :=
  [(a, b), (b, c), (c, d), (d, a)]

theorem coboundary_triangle_holonomy_zero (φ : Cochain0) (a b c : Vertex) :
    path_holonomy (coboundary φ) (triangle_cycle a b c) = 0 := by
  dsimp [path_holonomy, triangle_cycle, coboundary]
  omega

theorem coboundary_square_holonomy_zero (φ : Cochain0) (a b c d : Vertex) :
    path_holonomy (coboundary φ) (square_cycle a b c d) = 0 := by
  dsimp [path_holonomy, square_cycle, coboundary]
  omega

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

theorem coboundary_closed_cycle_zero (φ : Cochain0) (u : Vertex) (vs : List Vertex) :
    vertex_path_holonomy (coboundary φ) (u :: vs ++ [u]) = 0 := by
  rw [coboundary_vertex_path_telescoping φ u u vs]
  omega

theorem flux_obstructs_coboundary (A : Cochain1) (a b c : Vertex) :
    path_holonomy A (triangle_cycle a b c) ≠ 0 → ¬ ∃ φ : Cochain0, A = coboundary φ := by
  intro h_flux ⟨φ, h_eq⟩
  rw [h_eq] at h_flux
  have h_zero := coboundary_triangle_holonomy_zero φ a b c
  exact h_flux h_zero

end InterferenceNonL1Resource

private def l5aProvenance : String :=
  "Origin: lean4/CoboundaryHolonomy.lean Claim: coboundary_triangle_holonomy_zero AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
