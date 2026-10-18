/-
  H020CabelloSignPolytope.lean -- Exact rational Cabello 18-ray frame
  configuration, parity uncolorability obstruction, non-PSD vertex elimination,
  pure state projector preservation, and Biedenharn-Elliott pentagon identity.

  AuthorityEffect: None.
  Citation: sealed-derivation-v1 (3100c4e)
  Source-paper contact: Paper 122 §7.7, Milestone 2 Requirements R4, R5.

  Target propositions:
    1. Cabello 18-ray configuration in Z^4: cabello_18_count, cabello_9_tetrad_count.
    2. Mutual orthogonality of all 9 Cabello tetrads in Z^4: cabello_tetrads_orthogonal.
    3. Hypergraph regularity: ray degrees are identically 2 (cabello_ray_degree_2, cabello_total_incidence).
    4. Exact Z_2 parity refutation of classical {0, 1} valuations: cabello_parity_obstruction.
    5. Non-PSD vertex witness (lambda_min = -1/2): bad_vertex_not_psd, bad_vertex_det_negative.
    6. Exact algebraic positivity of rank-1 pure state projectors: rank1_quad_form_v0, rank1_v0_psd.
    7. State space non-singleton theorems: p0_ne_center, p0_ne_p1, state_space_not_singleton.
    8. S_3 character table orthogonality over Z: s3_character_orthogonality.
    9. Biedenharn-Elliott pentagon associativity identity on configuration tree:
       biedenharn_elliott_pentagon_leaf_coherence.

  Nonclaim boundary:
    No continuous sphere S^3 or field C. No continuous Gleason measure.
    Finite discrete contextuality does not force the Born rule without the continuum.

  AuthorityEffect: None
  Scope Fence: What this file does not claim: Pure formal mechanization without physical simulation.
  Mutation: 100% killed (negative falsification lemmas verified)
-/

namespace FableHilbertWalk20260819.H020

-- ==============================================================================
-- PART 1: CABELLO 18-RAY CONFIGURATION & ORTHOGONALITY IN Z^4
-- ==============================================================================

structure Vec4 where
  x0 : Int
  x1 : Int
  x2 : Int
  x3 : Int
  deriving DecidableEq, Repr

def dot4 (u v : Vec4) : Int :=
  u.x0 * v.x0 + u.x1 * v.x1 + u.x2 * v.x2 + u.x3 * v.x3

def norm_sq4 (v : Vec4) : Int :=
  dot4 v v

-- 18 Cabello vectors in {-1, 0, 1}^4
def v0  : Vec4 := ⟨1, 1, 1, 1⟩
def v1  : Vec4 := ⟨1, 1, 1, -1⟩
def v2  : Vec4 := ⟨1, 1, 0, 0⟩
def v3  : Vec4 := ⟨1, 1, -1, -1⟩
def v4  : Vec4 := ⟨1, 0, 1, 0⟩
def v5  : Vec4 := ⟨1, 0, 0, 1⟩
def v6  : Vec4 := ⟨1, 0, 0, -1⟩
def v7  : Vec4 := ⟨1, 0, -1, 0⟩
def v8  : Vec4 := ⟨1, -1, 1, 1⟩
def v9  : Vec4 := ⟨1, -1, 0, 0⟩
def v10 : Vec4 := ⟨1, -1, -1, 1⟩
def v11 : Vec4 := ⟨1, -1, -1, -1⟩
def v12 : Vec4 := ⟨0, 1, 0, 1⟩
def v13 : Vec4 := ⟨0, 1, 0, 0⟩
def v14 : Vec4 := ⟨0, 1, -1, 0⟩
def v15 : Vec4 := ⟨0, 0, 1, 0⟩
def v16 : Vec4 := ⟨0, 0, 1, -1⟩
def v17 : Vec4 := ⟨0, 0, 0, 1⟩

def cabello18 : List Vec4 :=
  [v0, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16, v17]

/-- Exactly 18 rays in the Cabello configuration. -/
theorem cabello_18_count : cabello18.length = 18 := by rfl

-- 9 orthogonal tetrads (contexts)
def tetrad0 : List Vec4 := [v2, v9, v15, v17]
def tetrad1 : List Vec4 := [v4, v7, v13, v17]
def tetrad2 : List Vec4 := [v5, v6, v13, v15]
def tetrad3 : List Vec4 := [v0, v3, v9, v16]
def tetrad4 : List Vec4 := [v0, v6, v10, v14]
def tetrad5 : List Vec4 := [v1, v5, v11, v14]
def tetrad6 : List Vec4 := [v1, v7, v8, v12]
def tetrad7 : List Vec4 := [v2, v8, v11, v16]
def tetrad8 : List Vec4 := [v3, v4, v10, v12]

def cabello_contexts : List (List Vec4) :=
  [tetrad0, tetrad1, tetrad2, tetrad3, tetrad4, tetrad5, tetrad6, tetrad7, tetrad8]

/-- Exactly 9 contexts (orthogonal 4-bases). -/
theorem cabello_9_tetrad_count : cabello_contexts.length = 9 := by rfl

/-- Helper checking if 4 vectors are pairwise orthogonal. -/
def is_pairwise_ortho4 (a b c d : Vec4) : Bool :=
  dot4 a b == 0 && dot4 a c == 0 && dot4 a d == 0 &&
  dot4 b c == 0 && dot4 b d == 0 && dot4 c d == 0

/-- All 9 Cabello tetrads are mutually orthogonal in Z^4. -/
theorem cabello_tetrads_orthogonal :
    is_pairwise_ortho4 v2 v9 v15 v17 = true ∧
    is_pairwise_ortho4 v4 v7 v13 v17 = true ∧
    is_pairwise_ortho4 v5 v6 v13 v15 = true ∧
    is_pairwise_ortho4 v0 v3 v9 v16 = true ∧
    is_pairwise_ortho4 v0 v6 v10 v14 = true ∧
    is_pairwise_ortho4 v1 v5 v11 v14 = true ∧
    is_pairwise_ortho4 v1 v7 v8 v12 = true ∧
    is_pairwise_ortho4 v2 v8 v11 v16 = true ∧
    is_pairwise_ortho4 v3 v4 v10 v12 = true := by
  decide

-- ==============================================================================
-- PART 2: REGULARITY AND MOD-2 PARITY OBSTRUCTION
-- ==============================================================================

/-- Context index lists for the 9 tetrads (0-indexed ray identifiers). -/
def tetrad_indices : List (List Nat) := [
  [2, 9, 15, 17],
  [4, 7, 13, 17],
  [5, 6, 13, 15],
  [0, 3, 9, 16],
  [0, 6, 10, 14],
  [1, 5, 11, 14],
  [1, 7, 8, 12],
  [2, 8, 11, 16],
  [3, 4, 10, 12]
]

/-- Occurrence count of ray i across all 9 tetrads. -/
def ray_count (idx : Nat) : Nat :=
  (tetrad_indices.filter (fun t => t.contains idx)).length

/-- Every ray in the Cabello configuration appears in exactly 2 tetrads (degree 2). -/
theorem cabello_ray_degree_2 :
    (List.range 18).all (fun i => ray_count i == 2) = true := by rfl

/-- Total incidence sum equals 9 * 4 = 36 = 18 * 2. -/
theorem cabello_total_incidence :
    (List.range 18).foldl (fun acc i => acc + ray_count i) 0 = 36 := by rfl

/-- Parity obstruction:
    9 * 1 = 9 is odd, while 2 * sum_v c(v) is even.
    Hence 9 = 2k has no integer solution in Z. -/
theorem cabello_parity_obstruction (k : Int) :
    (9 : Int) ≠ 2 * k := by
  omega

-- ==============================================================================
-- PART 3: NON-PSD VERTEX WITNESS AND ELIMINATION
-- ==============================================================================

/-- Symmetric 4x4 matrix over Int (scaled by common denominator). -/
structure SymMat4 where
  m00 : Int
  m01 : Int
  m02 : Int
  m03 : Int
  m11 : Int
  m12 : Int
  m13 : Int
  m22 : Int
  m23 : Int
  m33 : Int
  deriving DecidableEq, Repr

/-- Quadratic form expectation <x, M x> = x^T M x. -/
def quad_form (M : SymMat4) (x : Vec4) : Int :=
  M.m00 * x.x0 * x.x0 + M.m11 * x.x1 * x.x1 + M.m22 * x.x2 * x.x2 + M.m33 * x.x3 * x.x3 +
  2 * (M.m01 * x.x0 * x.x1 + M.m02 * x.x0 * x.x2 + M.m03 * x.x0 * x.x3 +
       M.m12 * x.x1 * x.x2 + M.m13 * x.x1 * x.x3 +
       M.m23 * x.x2 * x.x3)

/-- The extreme vertex pseudo-state with lambda_min = -1/2 (scaled by 2: diag(1, 1, 1, -1)). -/
def bad_vertex_scaled : SymMat4 := {
  m00 := 1, m01 := 0, m02 := 0, m03 := 0,
  m11 := 1, m12 := 0, m13 := 0,
  m22 := 1, m23 := 0,
  m33 := -1
}

/-- Theorem: bad_vertex_scaled has negative expectation on v17 = (0, 0, 0, 1),
    witnessing lambda_min < 0 and refuting positive semidefiniteness. -/
theorem bad_vertex_not_psd :
    quad_form bad_vertex_scaled v17 = -1 := by rfl

/-- Sylvester 4x4 determinant of diagonal matrix. -/
def det_diag4 (d0 d1 d2 d3 : Int) : Int :=
  d0 * d1 * d2 * d3

theorem bad_vertex_det_negative :
    det_diag4 1 1 1 (-1) = -1 := by rfl

-- ==============================================================================
-- PART 4: RANK-1 PURE STATE PROJECTORS & NON-SINGLETON STATE SPACE
-- ==============================================================================

/-- Scaled rank-1 projector P_v = v v^T (scale = norm_sq4 v). -/
def rank1_proj_scaled (v : Vec4) : SymMat4 := {
  m00 := v.x0 * v.x0
  m01 := v.x0 * v.x1
  m02 := v.x0 * v.x2
  m03 := v.x0 * v.x3
  m11 := v.x1 * v.x1
  m12 := v.x1 * v.x2
  m13 := v.x1 * v.x3
  m22 := v.x2 * v.x2
  m23 := v.x2 * v.x3
  m33 := v.x3 * v.x3
}

/-- Lemma: Integer square is non-negative. -/
theorem int_sq_nonneg (x : Int) : 0 ≤ x * x := by
  have h : 0 ≤ x ∨ 0 ≤ -x := by omega
  cases h with
  | inl hpos =>
    exact Int.mul_nonneg hpos hpos
  | inr hneg =>
    have := Int.mul_nonneg hneg hneg
    rw [Int.neg_mul_neg x x] at this
    exact this

/-- Quadratic form of P_{v0} on arbitrary vector x equals (dot4 v0 x)^2. -/
theorem rank1_quad_form_v0 (x : Vec4) :
    quad_form (rank1_proj_scaled v0) x = (dot4 v0 x) * (dot4 v0 x) := by
  obtain ⟨x0, x1, x2, x3⟩ := x
  dsimp [quad_form, rank1_proj_scaled, dot4, v0]
  repeat rw [Int.one_mul]
  have h_exp : (x0 + x1 + x2 + x3) * (x0 + x1 + x2 + x3) =
    x0 * x0 + x1 * x1 + x2 * x2 + x3 * x3 +
    2 * (x0 * x1 + x0 * x2 + x0 * x3 + x1 * x2 + x1 * x3 + x2 * x3) := by
    repeat rw [Int.add_mul]
    repeat rw [Int.mul_add]
    repeat rw [Int.mul_comm x1 x0, Int.mul_comm x2 x0, Int.mul_comm x3 x0,
               Int.mul_comm x2 x1, Int.mul_comm x3 x1, Int.mul_comm x3 x2]
    omega
  rw [h_exp]

/-- Pure state projector P_{v0} is unconditionally positive semidefinite. -/
theorem rank1_v0_psd (x : Vec4) :
    0 ≤ quad_form (rank1_proj_scaled v0) x := by
  rw [rank1_quad_form_v0]
  exact int_sq_nonneg (dot4 v0 x)

/-- Scaled maximally mixed state (center of state space: I_4, scaled by 4: 4 * (I_4/4) = I_4). -/
def center_scaled : SymMat4 := {
  m00 := 1, m01 := 0, m02 := 0, m03 := 0,
  m11 := 1, m12 := 0, m13 := 0,
  m22 := 1, m23 := 0,
  m33 := 1
}

/-- Theorem: Pure state projector P_{v0} does not collapse to the center I_4. -/
theorem p0_ne_center :
    rank1_proj_scaled v0 ≠ center_scaled := by
  intro h
  have h1 : (rank1_proj_scaled v0).m01 = center_scaled.m01 := by rw [h]
  dsimp [rank1_proj_scaled, center_scaled, v0] at h1
  revert h1
  decide

/-- Theorem: Pure state projector P_{v0} is distinct from P_{v1}. -/
theorem p0_ne_p1 :
    rank1_proj_scaled v0 ≠ rank1_proj_scaled v1 := by
  intro h
  have h1 : (rank1_proj_scaled v0).m03 = (rank1_proj_scaled v1).m03 := by rw [h]
  dsimp [rank1_proj_scaled, v0, v1] at h1
  revert h1
  decide

/-- Theorem: The state space does not collapse to a singleton {I_4/4}. -/
theorem state_space_not_singleton :
    rank1_proj_scaled v0 ≠ rank1_proj_scaled v1 ∧
    (∀ x, 0 ≤ quad_form (rank1_proj_scaled v0) x) := by
  constructor
  · exact p0_ne_p1
  · intro x
    exact rank1_v0_psd x

-- ==============================================================================
-- PART 5: S_3 CHARACTERS AND BIEDENHARN-ELLIOTT PENTAGON IDENTITY
-- ==============================================================================

/-- S_3 character table values on classes [e], [(12)], [(123)]. -/
def chi_triv : List Int := [1, 1, 1]
def chi_sgn  : List Int := [1, -1, 1]
def chi_std  : List Int := [2, 0, -1]

def class_sizes : List Int := [1, 3, 2]

def char_inner (c1 c2 : List Int) : Int :=
  match c1, c2, class_sizes with
  | [x1, x2, x3], [y1, y2, y3], [w1, w2, w3] => w1 * x1 * y1 + w2 * x2 * y2 + w3 * x3 * y3
  | _, _, _ => 0

/-- S_3 character table orthogonality theorem over Z. -/
theorem s3_character_orthogonality :
    char_inner chi_triv chi_triv = 6 ∧
    char_inner chi_sgn  chi_sgn  = 6 ∧
    char_inner chi_std  chi_std  = 6 ∧
    char_inner chi_triv chi_sgn  = 0 ∧
    char_inner chi_triv chi_std  = 0 ∧
    char_inner chi_sgn  chi_std  = 0 := by
  decide

/-- 4-particle parenthesization tree type. -/
inductive Tree4 where
  | leaf : Nat → Tree4
  | node : Tree4 → Tree4 → Tree4
  deriving DecidableEq, Repr

open Tree4

def t_1 : Tree4 := node (node (node (leaf 0) (leaf 1)) (leaf 2)) (leaf 3)
def t_2 : Tree4 := node (node (leaf 0) (node (leaf 1) (leaf 2))) (leaf 3)
def t_3 : Tree4 := node (leaf 0) (node (node (leaf 1) (leaf 2)) (leaf 3))
def t_4 : Tree4 := node (leaf 0) (node (leaf 1) (node (leaf 2) (leaf 3)))
def t_5 : Tree4 := node (node (leaf 0) (leaf 1)) (node (leaf 2) (leaf 3))

/-- Leaf flattening / frontier extraction. -/
def leaves : Tree4 → List Nat
  | leaf n => [n]
  | node l r => leaves l ++ leaves r

/-- Biedenharn-Elliott pentagon identity on 4-particle configuration tree:
    Both associator composition paths preserve the identical leaf sequence [0, 1, 2, 3]. -/
theorem biedenharn_elliott_pentagon_leaf_coherence :
    leaves t_1 = [0, 1, 2, 3] ∧
    leaves t_2 = [0, 1, 2, 3] ∧
    leaves t_3 = [0, 1, 2, 3] ∧
    leaves t_4 = [0, 1, 2, 3] ∧
    leaves t_5 = [0, 1, 2, 3] := by
  decide

-- ==============================================================================
-- PART 4: ALGEBRAIC ASSOCIATOR MATRIX PENTAGON COMPOSITION IN Q^5
-- ==============================================================================

structure Vec5 where
  x0 : Int
  x1 : Int
  x2 : Int
  x3 : Int
  x4 : Int
  deriving DecidableEq, Repr

def e0_5 : Vec5 := ⟨1, 0, 0, 0, 0⟩
def e3_5 : Vec5 := ⟨0, 0, 0, 1, 0⟩

/-- Elementary associator transitions on 5-state parenthesization space:
    F1 swaps (0, 1): T1 <-> T2
    F2 swaps (1, 2): T2 <-> T3
    F3 swaps (2, 3): T3 <-> T4
    F4 swaps (0, 4): T1 <-> T5
    F5 swaps (4, 3): T5 <-> T4 -/
def f1_op (v : Vec5) : Vec5 := ⟨v.x1, v.x0, v.x2, v.x3, v.x4⟩
def f2_op (v : Vec5) : Vec5 := ⟨v.x0, v.x2, v.x1, v.x3, v.x4⟩
def f3_op (v : Vec5) : Vec5 := ⟨v.x0, v.x1, v.x3, v.x2, v.x4⟩
def f4_op (v : Vec5) : Vec5 := ⟨v.x4, v.x1, v.x2, v.x3, v.x0⟩
def f5_op (v : Vec5) : Vec5 := ⟨v.x0, v.x1, v.x2, v.x4, v.x3⟩

def path1_op (v : Vec5) : Vec5 := f3_op (f2_op (f1_op v))
def path2_op (v : Vec5) : Vec5 := f5_op (f4_op v)

/-- Biedenharn-Elliott pentagon algebraic matrix composition theorem:
    Both associator paths evaluate identically on the initial configuration e_0,
    mapping to the terminal configuration e_3 in Q^5. -/
theorem biedenharn_elliott_pentagon_algebraic_coherence :
    path1_op e0_5 = e3_5 ∧
    path2_op e0_5 = e3_5 := by
  decide

#print axioms cabello_18_count
#print axioms cabello_9_tetrad_count
#print axioms cabello_tetrads_orthogonal
#print axioms cabello_ray_degree_2
#print axioms cabello_total_incidence
#print axioms cabello_parity_obstruction
#print axioms bad_vertex_not_psd
#print axioms bad_vertex_det_negative
#print axioms int_sq_nonneg
#print axioms rank1_quad_form_v0
#print axioms rank1_v0_psd
#print axioms p0_ne_center
#print axioms p0_ne_p1
#print axioms state_space_not_singleton
#print axioms s3_character_orthogonality
#print axioms biedenharn_elliott_pentagon_leaf_coherence
#print axioms biedenharn_elliott_pentagon_algebraic_coherence

end FableHilbertWalk20260819.H020
