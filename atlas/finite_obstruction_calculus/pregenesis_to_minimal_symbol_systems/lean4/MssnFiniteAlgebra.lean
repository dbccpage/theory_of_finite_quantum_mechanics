/-! Finite integer signed-pair and matrix identities.
AuthorityEffect: None. No physical model or coherence theorem is certified. -/
namespace MssnFiniteAlgebra

-- =========================================================================
-- 2. Finite signed-pair cancellation
-- =========================================================================

/-- Discrete signed path configuration with exact integer action and fermion sign. -/
structure SignedConfig where
  id : Nat
  action : Nat
  sign : Int
  deriving Repr, DecidableEq

/-- Theorem: When two configurations form an exact sign-reversing pair (sign' = -sign),
    their contributions to the path sum cancel identically to zero. -/
theorem involution_pair_sum_cancels (c1 c2 : SignedConfig) (_h_action : c1.action = c2.action) (h_sign : c2.sign = -c1.sign) :
    c1.sign + c2.sign = 0 := by
  omega

/-- An involution pairing between two signed configurations. -/
structure InvolutionPair where
  c1 : SignedConfig
  c2 : SignedConfig
  action_eq : c1.action = c2.action
  sign_rev : c2.sign = -c1.sign

/-- Net sign contribution of any valid involution pair is identically zero. -/
theorem involution_pair_net_sign (pair : InvolutionPair) :
    pair.c1.sign + pair.c2.sign = 0 := by
  rw [pair.sign_rev]
  omega

-- =========================================================================
-- 3. Finite matrix commutators
-- =========================================================================

/-- Exact 2x2 matrix over Int. -/
structure Mat2x2 where
  a11 : Int
  a12 : Int
  a21 : Int
  a22 : Int
  deriving Repr, DecidableEq

def Mat2x2.zero : Mat2x2 := ⟨0, 0, 0, 0⟩
def Mat2x2.one : Mat2x2 := ⟨1, 0, 0, 1⟩

def Mat2x2.add (A B : Mat2x2) : Mat2x2 :=
  ⟨A.a11 + B.a11, A.a12 + B.a12, A.a21 + B.a21, A.a22 + B.a22⟩

def Mat2x2.sub (A B : Mat2x2) : Mat2x2 :=
  ⟨A.a11 - B.a11, A.a12 - B.a12, A.a21 - B.a21, A.a22 - B.a22⟩

def Mat2x2.mul (A B : Mat2x2) : Mat2x2 :=
  ⟨A.a11 * B.a11 + A.a12 * B.a21,
   A.a11 * B.a12 + A.a12 * B.a22,
   A.a21 * B.a11 + A.a22 * B.a21,
   A.a21 * B.a12 + A.a22 * B.a22⟩

instance : Add Mat2x2 := ⟨Mat2x2.add⟩
instance : Sub Mat2x2 := ⟨Mat2x2.sub⟩
instance : Mul Mat2x2 := ⟨Mat2x2.mul⟩

/-- Matrix commutator bracket: [A, B] = A * B - B * A. -/
def bracket (A B : Mat2x2) : Mat2x2 :=
  A * B - B * A

/-- Evaluates the Lie algebra Jacobi sum: [A, [B, C]] + [B, [C, A]] + [C, [A, B]]. -/
def jacobiSum (A B C : Mat2x2) : Mat2x2 :=
  bracket A (bracket B C) + bracket B (bracket C A) + bracket C (bracket A B)

/-- Exact matrix trace: Tr(A) = A.a11 + A.a22. -/
def Mat2x2.trace (A : Mat2x2) : Int :=
  A.a11 + A.a22

/-- Theorem: Matrix commutator trace is identically zero: Tr([A, B]) = 0.
    Follows from trace cyclicity: Tr(AB) = Tr(BA). -/
theorem mat2x2_trace_commutator_zero (A B : Mat2x2) :
    (bracket A B).trace = 0 := by
  change (A.a11 * B.a11 + A.a12 * B.a21 - (B.a11 * A.a11 + B.a12 * A.a21)) +
         (A.a21 * B.a12 + A.a22 * B.a22 - (B.a21 * A.a12 + B.a22 * A.a22)) = 0
  rw [Int.mul_comm B.a11 A.a11, Int.mul_comm B.a12 A.a21, Int.mul_comm B.a21 A.a12, Int.mul_comm B.a22 A.a22]
  omega

/-- Theorem: Heisenberg commutation relation [A, B] = c * I is algebraically obstructed for c ≠ 0
    on finite matrices, certified by trace cyclicity: if [A, B] = c * I, then 2 * c = 0. -/
theorem heisenberg_trace_obstruction (A B : Mat2x2) (c : Int)
    (h : bracket A B = ⟨c, 0, 0, c⟩) : 2 * c = 0 := by
  have h_tr : (bracket A B).trace = 0 := mat2x2_trace_commutator_zero A B
  have h_c : (bracket A B).trace = 2 * c := by
    rw [h]
    dsimp [Mat2x2.trace]
    omega
  omega

def matX : Mat2x2 := ⟨0, 1, 1, 0⟩
def matY : Mat2x2 := ⟨0, -1, 1, 0⟩
def matZ : Mat2x2 := ⟨1, 0, 0, -1⟩

theorem discrete_matrices_do_not_commute :
    bracket matX matY ≠ Mat2x2.zero := by
  dsimp [bracket, matX, matY, Mat2x2.mul, Mat2x2.sub, Mat2x2.zero]
  decide

/-- Mechanical confirmation: Pauli generator basis satisfies the Lie algebra Jacobi identity. -/
theorem pauli_basis_jacobi_identity :
    jacobiSum matX matY matZ = Mat2x2.zero := by
  dsimp [jacobiSum, bracket, matX, matY, matZ, Mat2x2.mul, Mat2x2.sub, Mat2x2.add, Mat2x2.zero]
  decide

/-- A swap matrix; this involution is not a Mac Lane pentagon.
    In the integer matrix representation, F = [[0, 1], [1, 0]] satisfies F^2 = I. -/
def anyonInvolutionF : Mat2x2 := ⟨0, 1, 1, 0⟩

theorem anyon_involution_f_squared_is_identity :
    anyonInvolutionF * anyonInvolutionF = Mat2x2.one := by
  dsimp [anyonInvolutionF, Mat2x2.mul, Mat2x2.one]
  decide


end MssnFiniteAlgebra
