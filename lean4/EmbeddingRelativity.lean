
namespace HilbertWalk.EmbeddingRelativity


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

def mul (x y : QSqrt5) : QSqrt5 :=
  ⟨x.a * y.a + 5 * x.b * y.b, x.a * y.b + x.b * y.a⟩

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


def evalAtS (s : Int) (x : QSqrt5) : Int :=
  4 * x.a + x.b * s

theorem eval_galois_conjugate (s : Int) (x : QSqrt5) :
    evalAtS (-s) x = evalAtS s (QSqrt5.galoisAut x) := by
  cases x
  dsimp [evalAtS, QSqrt5.galoisAut]
  rw [Int.mul_neg, Int.neg_mul]


structure PureGram2 where
  c0 : Int
  c1 : Int
  deriving DecidableEq, Repr

def diag0 (psi : PureGram2) : Int := psi.c0 * psi.c0
def diag1 (psi : PureGram2) : Int := psi.c1 * psi.c1
def off (psi : PureGram2) : Int := psi.c0 * psi.c1
def det (psi : PureGram2) : Int := (diag0 psi) * (diag1 psi) - (off psi) * (off psi)

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

theorem pure_state_totally_positive_2d (psi : PureGram2) :
    0 ≤ diag0 psi ∧ 0 ≤ diag1 psi ∧ 0 ≤ det psi :=
  ⟨pure_diag0_nonneg psi, pure_diag1_nonneg psi, pure_det_nonneg psi⟩


def witnessW5_diag0 : QSqrt5 := ⟨-2, 1⟩
def witnessW5_diag1 : QSqrt5 := ⟨3, -1⟩

theorem witnessW5_trace_is_one :
    (QSqrt5.add witnessW5_diag0 witnessW5_diag1).a = 1 ∧
    (QSqrt5.add witnessW5_diag0 witnessW5_diag1).b = 0 := by
  decide

theorem witnessW5_primary_positive :
    0 < evalAtS 9 witnessW5_diag0 ∧ 0 < evalAtS 9 witnessW5_diag1 := by
  decide

theorem witnessW5_conjugate_negative :
    evalAtS (-9) witnessW5_diag0 < 0 := by
  decide

theorem witnessW5_embedding_relative :
    (0 < evalAtS 9 witnessW5_diag0 ∧ 0 < evalAtS 9 witnessW5_diag1) ∧
    (evalAtS (-9) witnessW5_diag0 < 0) := by
  exact ⟨witnessW5_primary_positive, witnessW5_conjugate_negative⟩


structure EquivariantSelection where
  eval : Int → Int
  swap_invariant : eval 9 = eval (-9)

theorem selection_refusal (F : EquivariantSelection) :
    F.eval 9 = F.eval (-9) :=
  F.swap_invariant

theorem authority_effect_none : "AuthorityEffect: None" = "AuthorityEffect: None" := rfl

end HilbertWalk.EmbeddingRelativity

#print axioms HilbertWalk.EmbeddingRelativity.pure_state_totally_positive_2d
#print axioms HilbertWalk.EmbeddingRelativity.witnessW5_embedding_relative
#print axioms HilbertWalk.EmbeddingRelativity.selection_refusal

private def l5aProvenance : String :=
  "Origin: lean4/EmbeddingRelativity.lean Claim: galois_involutive AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
