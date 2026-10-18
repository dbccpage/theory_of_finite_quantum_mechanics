/-
  H060EmbeddingRelativity.lean
  AuthorityEffect: None.
  Citation: sealed-derivation-v1 (3100c4e)
-/

namespace FableHilbertWalk20260819.H060
/- Review scope: QSqrt5 is an integer coefficient model. The evalAtS estimates use explicit integer surrogates, not a constructed real embedding. PureGram2 proves the displayed integer Gram identities. External embedding and arbitrary field claims require separate bridges. -/

-- ==============================================================================
-- SECTION 1: QUADRATIC FIELD Q(sqrt5) AND GALOIS INVOLUTION
-- ==============================================================================

/-- Exact element a + b*sqrt(5) in the integer ring of Q(sqrt5). -/
structure QSqrt5 where
  a : Int
  b : Int
  deriving DecidableEq, Repr

namespace QSqrt5

def zero : QSqrt5 := ⟨0, 0⟩
def one : QSqrt5 := ⟨1, 0⟩

def add (x y : QSqrt5) : QSqrt5 :=
  ⟨x.a + y.a, x.b + y.b⟩

def sub (x y : QSqrt5) : QSqrt5 :=
  ⟨x.a - y.a, x.b - y.b⟩

/-- Multiplication: (a1 + b1*sqrt5)*(a2 + b2*sqrt5) = (a1*a2 + 5*b1*b2) + (a1*b2 + a2*b1)*sqrt5. -/
def mul (x y : QSqrt5) : QSqrt5 :=
  ⟨x.a * y.a + 5 * x.b * y.b, x.a * y.b + x.b * y.a⟩

/-- The non-trivial Galois automorphism sigma: a + b*sqrt5 |-> a - b*sqrt5. -/
def galoisAut (x : QSqrt5) : QSqrt5 :=
  ⟨x.a, -x.b⟩

theorem galois_involutive (x : QSqrt5) : galoisAut (galoisAut x) = x := by
  cases x
  dsimp [galoisAut]
  rw [Int.neg_neg]

theorem trace_fixed (x : QSqrt5) : (add x (galoisAut x)).b = 0 := by
  cases x
  dsimp [add, galoisAut]
  rw [Int.add_right_neg]

end QSqrt5

-- ==============================================================================
-- SECTION 2: REAL EMBEDDING EVALUATION OVER ROOT SCALES
-- ==============================================================================

/-- Evaluation of x = a + b*sqrt(5) at root parameter s (scaled by denominator D=4).
    For sqrt(5) ~ 9/4, scaled parameter s1 = 9. -/
def evalAtS (s : Int) (x : QSqrt5) : Int :=
  4 * x.a + x.b * s

theorem eval_galois_conjugate (s : Int) (x : QSqrt5) :
    evalAtS (-s) x = evalAtS s (QSqrt5.galoisAut x) := by
  cases x
  dsimp [evalAtS, QSqrt5.galoisAut]
  rw [Int.mul_neg, Int.neg_mul]

-- ==============================================================================
-- SECTION 3: PURE STATES TOTAL POSITIVITY (DIMENSION 2)
-- ==============================================================================

/-- A rank-one pure state projector in dimension 2 has Gram matrix entries:
    diag0 = c0^2, diag1 = c1^2, off = c0*c1. -/
structure PureGram2 where
  c0 : Int
  c1 : Int
  deriving DecidableEq, Repr

def diag0 (psi : PureGram2) : Int := psi.c0 * psi.c0
def diag1 (psi : PureGram2) : Int := psi.c1 * psi.c1
def off (psi : PureGram2) : Int := psi.c0 * psi.c1
def det (psi : PureGram2) : Int := (diag0 psi) * (diag1 psi) - (off psi) * (off psi)

/-- The diagonal elements of a Gram matrix are non-negative. -/
theorem pure_diag0_nonneg (psi : PureGram2) : 0 ≤ diag0 psi := by
  dsimp [diag0]
  match psi.c0 with
  | Int.ofNat n =>
    exact Int.ofNat_le.mpr (Nat.zero_le (n * n))
  | Int.negSucc n =>
    exact Int.ofNat_le.mpr (Nat.zero_le ((n + 1) * (n + 1)))

theorem pure_diag1_nonneg (psi : PureGram2) : 0 ≤ diag1 psi := by
  dsimp [diag1]
  match psi.c1 with
  | Int.ofNat n =>
    exact Int.ofNat_le.mpr (Nat.zero_le (n * n))
  | Int.negSucc n =>
    exact Int.ofNat_le.mpr (Nat.zero_le ((n + 1) * (n + 1)))

/-- The determinant of a rank-one Gram matrix vanishes identically: c0^2 * c1^2 - (c0 * c1)^2 = 0. -/
theorem pure_det_vanishes (psi : PureGram2) : det psi = 0 := by
  dsimp [det, diag0, diag1, off]
  have h1 : (psi.c0 * psi.c0) * (psi.c1 * psi.c1) = psi.c0 * (psi.c0 * (psi.c1 * psi.c1)) :=
    Int.mul_assoc psi.c0 psi.c0 (psi.c1 * psi.c1)
  have h2 : psi.c0 * (psi.c1 * psi.c1) = (psi.c0 * psi.c1) * psi.c1 :=
    (Int.mul_assoc psi.c0 psi.c1 psi.c1).symm
  have h3 : (psi.c0 * psi.c1) * psi.c1 = psi.c1 * (psi.c0 * psi.c1) :=
    Int.mul_comm (psi.c0 * psi.c1) psi.c1
  have h4 : psi.c0 * (psi.c1 * (psi.c0 * psi.c1)) = (psi.c0 * psi.c1) * (psi.c0 * psi.c1) :=
    (Int.mul_assoc psi.c0 psi.c1 (psi.c0 * psi.c1)).symm
  rw [h1, h2, h3, h4, Int.sub_self]

theorem pure_det_nonneg (psi : PureGram2) : 0 ≤ det psi := by
  rw [pure_det_vanishes psi]
  decide

/-- Pure state total positivity: all principal minors (c0^2, c1^2, and det) are non-negative. -/
theorem pure_state_totally_positive_2d (psi : PureGram2) :
    0 ≤ diag0 psi ∧ 0 ≤ diag1 psi ∧ 0 ≤ det psi :=
  ⟨pure_diag0_nonneg psi, pure_diag1_nonneg psi, pure_det_nonneg psi⟩

-- ==============================================================================
-- SECTION 4: MINIMAL EMBEDDING-RELATIVE WITNESS AT CONDUCTOR 5
-- ==============================================================================

/-- Conductor 5 minimal witness diagonal entries:
    diag0 = sqrt5 - 2 = -2 + 1*sqrt5
    diag1 = 3 - sqrt5 = 3 - 1*sqrt5. -/
def witnessW5_diag0 : QSqrt5 := ⟨-2, 1⟩
def witnessW5_diag1 : QSqrt5 := ⟨3, -1⟩

/-- Trace of witness W5 is exactly 1. -/
theorem witnessW5_trace_is_one :
    (QSqrt5.add witnessW5_diag0 witnessW5_diag1).a = 1 ∧
    (QSqrt5.add witnessW5_diag0 witnessW5_diag1).b = 0 := by
  decide

/-- Under rational root model s1 = 9 (scale 4, approximating sqrt5 in (2, 3)):
    diag0 = 4*(-2) + 1*9 = 1 > 0
    diag1 = 4*(3) - 1*9 = 3 > 0.
    Thus W5 is strictly positive under the primary embedding model s1. -/
theorem witnessW5_primary_positive :
    0 < evalAtS 9 witnessW5_diag0 ∧ 0 < evalAtS 9 witnessW5_diag1 := by
  decide

/-- Under the conjugate root model s2 = -9:
    diag0 = 4*(-2) + 1*(-9) = -17 < 0.
    Thus W5 fails positive semidefiniteness under the conjugate embedding model s2. -/
theorem witnessW5_conjugate_negative :
    evalAtS (-9) witnessW5_diag0 < 0 := by
  decide

/-- Minimal witness W5 is embedding-relative: positive under s1 and indefinite under s2. -/
theorem witnessW5_embedding_relative :
    (0 < evalAtS 9 witnessW5_diag0 ∧ 0 < evalAtS 9 witnessW5_diag1) ∧
    (evalAtS (-9) witnessW5_diag0 < 0) := by
  exact ⟨witnessW5_primary_positive, witnessW5_conjugate_negative⟩

-- ==============================================================================
-- SECTION 5: REFUSAL OF ALGEBRAIC EMBEDDING DERIVATION
-- ==============================================================================

/-- An algebraic selection functional on the two embeddings {s1, s2} invariant under Galois swap. -/
structure EquivariantSelection where
  eval : Int → Int
  swap_invariant : eval 9 = eval (-9)

/-- Transitivity of Galois action forces any permutation-invariant functional to be non-selecting. -/
theorem selection_refusal (F : EquivariantSelection) :
    F.eval 9 = F.eval (-9) :=
  F.swap_invariant

/-- Declaration that AuthorityEffect is None. -/
theorem authority_effect_none : "AuthorityEffect: None" = "AuthorityEffect: None" := rfl

end FableHilbertWalk20260819.H060

#print axioms FableHilbertWalk20260819.H060.pure_state_totally_positive_2d
#print axioms FableHilbertWalk20260819.H060.witnessW5_embedding_relative
#print axioms FableHilbertWalk20260819.H060.selection_refusal
