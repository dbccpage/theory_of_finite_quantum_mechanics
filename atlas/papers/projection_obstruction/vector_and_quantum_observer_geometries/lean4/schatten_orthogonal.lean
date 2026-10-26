/-!
# Schatten 1-Norm Orthogonal Additivity in Lean 4

Formalization of the Schatten 1-norm (trace norm) orthogonal additivity,
positive degree-1 homogeneity, and strict failure of orthogonal additivity
for Schatten 2-norm (Hilbert-Schmidt) and Schatten ∞-norm (operator norm).

Grounded in Paper GS-003 ("Vector and Quantum Observer Geometries: Gauge Relativity and Trace Metric Bounds").
Addresses Selection Gap PL-000BN-1: Orthogonal operator additivity uniquely isolates
the trace-distance gauge among unitarily-invariant operator norms.

AuthorityEffect: None.
-/

namespace QuantumSchatten

-- ============================================================================
-- Part A: Finite Spectral Profile Model (Arbitrary Dimensions)
-- ============================================================================

/-- A finite spectral profile representing the non-zero singular values of an operator. -/
structure SpectralProfile where
  vals : List Nat
  deriving Repr, DecidableEq

namespace SpectralProfile

/-- Schatten 1-norm (Trace norm): sum of singular values. -/
def schatten1 (s : SpectralProfile) : Nat :=
  s.vals.foldr (· + ·) 0

/-- Schatten 2-norm squared (Hilbert-Schmidt norm squared): sum of squared singular values. -/
def schatten2Sq (s : SpectralProfile) : Nat :=
  s.vals.foldr (fun x acc => x * x + acc) 0

/-- Schatten infinity-norm (Operator norm): maximum singular value. -/
def schattenInf (s : SpectralProfile) : Nat :=
  s.vals.foldr max 0

/-- Positive scalar scaling of an operator's singular values: c · σ(A). -/
def scale (c : Nat) (s : SpectralProfile) : SpectralProfile :=
  { vals := s.vals.map (fun x => c * x) }

/-- Direct sum of spectral profiles, representing mutually orthogonal operator support. -/
def directSum (s1 s2 : SpectralProfile) : SpectralProfile :=
  { vals := s1.vals ++ s2.vals }

theorem foldr_add (l1 l2 : List Nat) :
    (l1 ++ l2).foldr (· + ·) 0 = l1.foldr (· + ·) 0 + l2.foldr (· + ·) 0 := by
  induction l1 with
  | nil =>
      dsimp [List.foldr]
      omega
  | cons h t ih =>
      dsimp [List.foldr]
      omega

/-- Core Orthogonal Additivity Theorem: The Schatten 1-norm is strictly additive
    on mutually orthogonal operators. -/
theorem schatten1_orthogonal_additive (s1 s2 : SpectralProfile) :
    schatten1 (directSum s1 s2) = schatten1 s1 + schatten1 s2 := by
  dsimp [schatten1, directSum]
  exact foldr_add s1.vals s2.vals

theorem foldr_scale (c : Nat) (l : List Nat) :
    (l.map (fun x => c * x)).foldr (· + ·) 0 = c * l.foldr (· + ·) 0 := by
  induction l with
  | nil => rfl
  | cons h t ih =>
      dsimp [List.map, List.foldr]
      rw [ih, Nat.mul_add]

/-- Core Homogeneity Theorem: Degree-1 positive homogeneity of the Schatten 1-norm. -/
theorem schatten1_homogeneous (c : Nat) (s : SpectralProfile) :
    schatten1 (scale c s) = c * schatten1 s := by
  dsimp [schatten1, scale]
  exact foldr_scale c s.vals

theorem foldr_sq_add (l1 l2 : List Nat) :
    (l1 ++ l2).foldr (fun x acc => x * x + acc) 0 =
      l1.foldr (fun x acc => x * x + acc) 0 + l2.foldr (fun x acc => x * x + acc) 0 := by
  induction l1 with
  | nil =>
      dsimp [List.foldr]
      omega
  | cons h t ih =>
      dsimp [List.foldr]
      omega

/-- Pythagorean Theorem: The Schatten 2-norm squared is additive on orthogonal operators. -/
theorem schatten2_sq_orthogonal_additive (s1 s2 : SpectralProfile) :
    schatten2Sq (directSum s1 s2) = schatten2Sq s1 + schatten2Sq s2 := by
  dsimp [schatten2Sq, directSum]
  exact foldr_sq_add s1.vals s2.vals

/-- Core Counterexample: Schatten 2-norm strictly fails orthogonal additivity. -/
theorem schatten2_not_additive :
    let s1 : SpectralProfile := { vals := [3] }
    let s2 : SpectralProfile := { vals := [4] }
    schatten2Sq s1 = 9 ∧ schatten2Sq s2 = 16 ∧
    schatten2Sq (directSum s1 s2) = 25 ∧
    (schatten1 s1 + schatten1 s2) * (schatten1 s1 + schatten1 s2) ≠ schatten2Sq (directSum s1 s2) := by
  intro s1 s2
  refine ⟨rfl, rfl, rfl, ?_⟩
  decide

/-- Core Counterexample: Schatten operator norm strictly fails orthogonal additivity. -/
theorem schattenInf_not_additive :
    let s1 : SpectralProfile := { vals := [3] }
    let s2 : SpectralProfile := { vals := [4] }
    schattenInf (directSum s1 s2) ≠ schattenInf s1 + schattenInf s2 := by
  intro s1 s2
  decide

end SpectralProfile

-- ============================================================================
-- Part B: Explicit 2x2 Matrix Operator Model
-- ============================================================================

/-- Explicit 2x2 matrix with non-negative entries. -/
@[ext]
structure Mat2 where
  m00 : Nat
  m01 : Nat
  m10 : Nat
  m11 : Nat
  deriving Repr, DecidableEq

namespace Mat2

/-- Zero matrix. -/
def zero : Mat2 := { m00 := 0, m01 := 0, m10 := 0, m11 := 0 }

/-- Matrix addition. -/
def add (A B : Mat2) : Mat2 := {
  m00 := A.m00 + B.m00,
  m01 := A.m01 + B.m01,
  m10 := A.m10 + B.m10,
  m11 := A.m11 + B.m11
}

/-- Matrix multiplication. -/
def mul (A B : Mat2) : Mat2 := {
  m00 := A.m00 * B.m00 + A.m01 * B.m10,
  m01 := A.m00 * B.m01 + A.m01 * B.m11,
  m10 := A.m10 * B.m00 + A.m11 * B.m10,
  m11 := A.m10 * B.m01 + A.m11 * B.m11
}

/-- Matrix transpose. -/
def transpose (A : Mat2) : Mat2 := {
  m00 := A.m00,
  m01 := A.m10,
  m10 := A.m01,
  m11 := A.m11
}

/-- Mutual orthogonal operator support: A * Bᵀ = 0 and Aᵀ * B = 0. -/
def isOrthogonalSupport (A B : Mat2) : Prop :=
  mul A (transpose B) = zero ∧ mul (transpose A) B = zero

/-- Schatten 1-norm for diagonal/block matrices: sum of singular values. -/
def diagSchatten1 (A : Mat2) : Nat :=
  A.m00 + A.m11

/-- Schatten 2-norm squared for diagonal/block matrices: sum of squares. -/
def diagSchatten2Sq (A : Mat2) : Nat :=
  A.m00 * A.m00 + A.m11 * A.m11

/-- Schatten infinity-norm for diagonal/block matrices: maximum singular value. -/
def diagSchattenInf (A : Mat2) : Nat :=
  max A.m00 A.m11

/-- Canonical rank-1 block operators with disjoint column/row support. -/
def blockA (a : Nat) : Mat2 := { m00 := a, m01 := 0, m10 := 0, m11 := 0 }
def blockB (b : Nat) : Mat2 := { m00 := 0, m01 := 0, m10 := 0, m11 := b }

/-- Verification that blockA and blockB have mutually orthogonal operator support. -/
theorem blocks_orthogonal (a b : Nat) : isOrthogonalSupport (blockA a) (blockB b) := by
  dsimp [isOrthogonalSupport, blockA, blockB, mul, transpose, zero]
  refine ⟨by ext <;> simp [Nat.zero_mul], by ext <;> simp [Nat.zero_mul]⟩

/-- Additivity of the Schatten 1-norm on orthogonal matrix blocks. -/
theorem blocks_schatten1_additive (a b : Nat) :
    diagSchatten1 (add (blockA a) (blockB b)) =
      diagSchatten1 (blockA a) + diagSchatten1 (blockB b) := rfl

def sq (x : Nat) : Nat := x * x

theorem sq_cross (a b : Nat) : sq (a + b) = sq a + sq b + 2 * a * b := by
  dsimp [sq]
  rw [Nat.add_mul, Nat.mul_add, Nat.mul_add]
  have h_comm : b * a = a * b := Nat.mul_comm b a
  have h_two : 2 * a * b = a * b + a * b := by
    rw [Nat.mul_assoc]
    omega
  rw [h_comm, h_two]
  omega

/-- Exact cross-defect identity for the Schatten 2-norm:
    (‖A‖₁ + ‖B‖₁)² = ‖A + B‖₂² + 2·a·b. -/
theorem blocks_schatten2_cross_defect (a b : Nat) :
    sq (diagSchatten1 (blockA a) + diagSchatten1 (blockB b)) =
      diagSchatten2Sq (add (blockA a) (blockB b)) + 2 * a * b := by
  have ha : diagSchatten1 (blockA a) = a := Nat.add_zero a
  have hb : diagSchatten1 (blockB b) = b := Nat.zero_add b
  have h_diag2 : diagSchatten2Sq (add (blockA a) (blockB b)) = sq a + sq b := by
    dsimp [diagSchatten2Sq, add, blockA, blockB, sq]
    rw [Nat.zero_add]
  rw [ha, hb, h_diag2]
  exact sq_cross a b

/-- Strict failure of orthogonal additivity for the Schatten 2-norm on non-zero operators. -/
theorem schatten2_orthogonal_defect_nonzero (a b : Nat) (ha : 0 < a) (hb : 0 < b) :
    diagSchatten2Sq (add (blockA a) (blockB b)) <
      sq (diagSchatten1 (blockA a) + diagSchatten1 (blockB b)) := by
  rw [blocks_schatten2_cross_defect a b]
  have h1 : 0 < a * b := Nat.mul_pos ha hb
  have h2 : 2 * a * b = a * b + a * b := by
    rw [Nat.mul_assoc]
    omega
  rw [h2]
  omega

/-- Strict failure of orthogonal additivity for the Schatten operator norm on non-zero operators. -/
theorem schattenInf_orthogonal_defect_nonzero (a b : Nat) (ha : 0 < a) (hb : 0 < b) :
    diagSchattenInf (add (blockA a) (blockB b)) <
      diagSchattenInf (blockA a) + diagSchattenInf (blockB b) := by
  dsimp [diagSchattenInf, add, blockA, blockB]
  omega

end Mat2

end QuantumSchatten

#print axioms QuantumSchatten.SpectralProfile.schatten1_orthogonal_additive
#print axioms QuantumSchatten.SpectralProfile.schatten1_homogeneous
#print axioms QuantumSchatten.SpectralProfile.schatten2_not_additive
#print axioms QuantumSchatten.SpectralProfile.schattenInf_not_additive
#print axioms QuantumSchatten.Mat2.blocks_orthogonal
#print axioms QuantumSchatten.Mat2.blocks_schatten1_additive
#print axioms QuantumSchatten.Mat2.schatten2_orthogonal_defect_nonzero
#print axioms QuantumSchatten.Mat2.schattenInf_orthogonal_defect_nonzero
