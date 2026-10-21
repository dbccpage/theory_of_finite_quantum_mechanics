import Mathlib.Data.Matrix.Block
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.FinCases

/-!
# Realification `R(A) = [[P, -Q], [Q, P]]` of complex matrices and the declared complex structure `J`

AuthorityEffect: None.  Scope: a complex `m x n` matrix over a commutative ring `alpha` is a pair
`A = (P, Q)` of real parts and imaginary parts (`A = P + i Q`), with the complex product
`(P,Q)(S,T) = (PS - QT, PT + QS)`.  `R A = fromBlocks P (-Q) Q P`, rows and columns indexed by `m ⊕ m` and
`n ⊕ n` (all real coordinates before all imaginary ones; the ordering is part of the definition), and
`J_n = fromBlocks 0 (-1) 1 0`.

Theorem 1 (general `m n k`, general commutative ring): `R` is additive and `alpha`-linear, multiplicative on
composable matrices, preserves the identity, is injective, satisfies `J^2 = -1`, `R(A*) = R(A)^T` (so `A` is Hermitian iff `R A` is symmetric),
`J_m R(A) = R(A) J_n`, `R(i A) = J_m R(A)` and `Tr R(A) = 2 Tr P` (twice the REAL part of the complex trace;
`trace_not_twice_complex_trace` is the instance `A = 1 + i`).
Theorem 2 (exact image): a matrix `M` indexed by `(m ⊕ m) x (n ⊕ n)` is `R A` for exactly one `A` iff
`J_m M = M J_n`.

The complex structure `J` is DECLARED, not selected: `other_square_root_instance` gives a second integer square
root of `-1` that does not commute with `J`, so "commutes with J" and "commutes with J'" carve out different
sub-algebras; `commutes_conj` shows that the choice of a square root is a choice of a conjugate of `J`.
Nothing here selects `J`, selects the complex field, or concerns states `sigma = R(rho)/2`, positivity or physics.
-/

namespace RealificationJ

open Matrix

section General

variable {α : Type*} [CommRing α]
variable {m n k : Type*} [Fintype m] [Fintype n] [Fintype k] [DecidableEq m] [DecidableEq n] [DecidableEq k]

/-- A complex matrix `P + i Q` as a pair of real matrices. -/
@[ext]
structure CMat (α : Type*) (m n : Type*) where
  re : Matrix m n α
  im : Matrix m n α

namespace CMat

/-- Complex sum. -/
def add (A B : CMat α m n) : CMat α m n := ⟨A.re + B.re, A.im + B.im⟩

/-- Complex product `(P + iQ)(S + iT) = (PS - QT) + i (PT + QS)`. -/
def mul (A : CMat α m n) (B : CMat α n k) : CMat α m k :=
  ⟨A.re * B.re - A.im * B.im, A.re * B.im + A.im * B.re⟩

/-- Complex identity. -/
def one : CMat α m m := ⟨1, 0⟩

/-- Conjugate transpose `A* = P^T - i Q^T`. -/
def star (A : CMat α m n) : CMat α n m := ⟨A.re.transpose, -A.im.transpose⟩

/-- Multiplication by `i`: `i (P + iQ) = -Q + i P`. -/
def imul (A : CMat α m n) : CMat α m n := ⟨-A.im, A.re⟩

/-- Real scalar multiple. -/
def smul (r : α) (A : CMat α m n) : CMat α m n := ⟨r • A.re, r • A.im⟩

/-- Complex trace, as (real part, imaginary part). -/
def trace (A : CMat α m m) : α × α := (Matrix.trace A.re, Matrix.trace A.im)

end CMat

/-- Realification `R(A) = [[P, -Q], [Q, P]]`. -/
def R (A : CMat α m n) : Matrix (m ⊕ m) (n ⊕ n) α := fromBlocks A.re (-A.im) A.im A.re

/-- The fixed real complex structure `J_m = [[0, -1], [1, 0]]`. -/
def J (m : Type*) [Fintype m] [DecidableEq m] (α : Type*) [CommRing α] : Matrix (m ⊕ m) (m ⊕ m) α :=
  fromBlocks 0 (-1) 1 0

theorem R_add (A B : CMat α m n) : R (A.add B) = R A + R B := by
  simp only [R, CMat.add, fromBlocks_add]
  congr 1 <;> simp [add_comm]

theorem R_smul (r : α) (A : CMat α m n) : R (A.smul r) = r • R A := by
  simp only [R, CMat.smul, fromBlocks_smul]
  congr 1 <;> simp

theorem R_mul (A : CMat α m n) (B : CMat α n k) : R (A.mul B) = R A * R B := by
  simp only [R, CMat.mul, fromBlocks_multiply]
  congr 1 <;> simp [sub_eq_add_neg, add_comm]

theorem R_one : R (CMat.one : CMat α m m) = 1 := by
  simp [R, CMat.one, fromBlocks_one]

theorem R_injective : Function.Injective (R : CMat α m n → Matrix (m ⊕ m) (n ⊕ n) α) := by
  intro A B h
  simp only [R] at h
  obtain ⟨h1, h2, h3, -⟩ := fromBlocks_inj.mp h
  exact CMat.ext h1 h3

theorem J_sq : J m α * J m α = -1 := by
  simp only [J, fromBlocks_multiply]
  have : (-1 : Matrix (m ⊕ m) (m ⊕ m) α) = fromBlocks (-1) 0 0 (-1) := by
    conv_lhs => rw [← fromBlocks_one]
    rw [fromBlocks_neg]; simp
  rw [this]
  congr 1 <;> simp

/-- Intertwining: `J_m R(A) = R(A) J_n` (rectangular). -/
theorem J_R_comm (A : CMat α m n) : J m α * R A = R A * J n α := by
  simp only [J, R, fromBlocks_multiply]
  congr 1 <;> simp

/-- `R(i A) = J_m R(A)`: multiplication by `i` is the declared complex structure. -/
theorem R_imul (A : CMat α m n) : R A.imul = J m α * R A := by
  simp only [J, R, CMat.imul, fromBlocks_multiply]
  congr 1 <;> simp

theorem R_star (A : CMat α m n) : R A.star = (R A).transpose := by
  simp only [R, CMat.star, fromBlocks_transpose]
  congr 1 <;> simp

/-- `A` is Hermitian iff `R(A)` is symmetric (square case). -/
theorem hermitian_iff_symmetric (A : CMat α m m) : A.star = A ↔ (R A).transpose = R A := by
  rw [← R_star]
  exact ⟨fun h => by rw [h], fun h => R_injective h⟩

theorem trace_fromBlocks' (A D : Matrix m m α) (B C : Matrix m m α) :
    Matrix.trace (fromBlocks A B C D) = Matrix.trace A + Matrix.trace D := by
  simp [Matrix.trace, Matrix.diag, Fintype.sum_sum_type]

/-- Trace identity: `Tr R(A) = 2 Tr P`, twice the REAL part of the complex trace. -/
theorem trace_R (A : CMat α m m) : Matrix.trace (R A) = 2 * Matrix.trace A.re := by
  simp only [R, trace_fromBlocks']
  ring

/-- INSTANCE: for `A = 1 + i` (1 x 1 over `Int`) the complex trace is `1 + i` but `Tr R(A) = 2 = 2 Re (1 + i)`:
the real trace sees only the real part, it is not "twice the complex trace". -/
theorem trace_not_twice_complex_trace :
    let A : CMat ℤ (Fin 1) (Fin 1) := ⟨!![1], !![1]⟩
    A.trace = (1, 1) ∧ Matrix.trace (R A) = 2 := by
  intro A
  refine ⟨by simp [A, CMat.trace, Matrix.trace], ?_⟩
  rw [trace_R]; simp [A, Matrix.trace]

/-- Theorem 2, existence and uniqueness: `M` is the realification of exactly one complex matrix iff
`J_m M = M J_n`. -/
theorem image_iff (M : Matrix (m ⊕ m) (n ⊕ n) α) :
    (J m α * M = M * J n α) ↔ ∃! A : CMat α m n, R A = M := by
  constructor
  · intro h
    have hM : M = fromBlocks M.toBlocks₁₁ M.toBlocks₁₂ M.toBlocks₂₁ M.toBlocks₂₂ :=
      (fromBlocks_toBlocks M).symm
    set U := M.toBlocks₁₁
    set V := M.toBlocks₁₂
    set W := M.toBlocks₂₁
    set Z := M.toBlocks₂₂
    rw [hM] at h
    simp only [J, fromBlocks_multiply] at h
    obtain ⟨h1, h2, h3, h4⟩ := fromBlocks_inj.mp h
    simp at h1 h2 h3 h4
    have hW : W = -V := neg_eq_iff_eq_neg.mp h1
    have hZ : Z = U := h2
    refine ⟨⟨U, -V⟩, ?_, fun B hB => ?_⟩
    · simp only [R]
      rw [hM, hW, hZ]; simp
    · apply R_injective
      simp only [R] at hB ⊢
      rw [hB, hM, hW, hZ]; simp
  · rintro ⟨A, hA, -⟩
    subst hA
    exact J_R_comm A

end General

section Commutation

variable {α : Type*} [CommRing α]
variable {n : Type*} [Fintype n] [DecidableEq n]

/-- A choice of square root `J'` of `-1` is a choice of the commutant: conjugation by an invertible `P` with
`P J = J' P` carries "commutes with J" to "commutes with J'". -/
theorem commutes_conj (J J' P Pinv M : Matrix n n α) (hP : P * J = J' * P) (hl : Pinv * P = 1)
    (hr : P * Pinv = 1) :
    (J * (Pinv * M * P) = (Pinv * M * P) * J) ↔ (J' * M = M * J') := by
  have hJ : J = Pinv * J' * P := by
    calc J = (Pinv * P) * J := by rw [hl, one_mul]
      _ = Pinv * (P * J) := by rw [Matrix.mul_assoc]
      _ = Pinv * (J' * P) := by rw [hP]
      _ = Pinv * J' * P := by rw [Matrix.mul_assoc]
  constructor
  · intro h
    have h2 : P * (J * (Pinv * M * P)) * Pinv = P * ((Pinv * M * P) * J) * Pinv := by rw [h]
    have e1 : P * (J * (Pinv * M * P)) * Pinv = J' * M := by
      calc P * (J * (Pinv * M * P)) * Pinv = (P * J) * (Pinv * M * P) * Pinv := by simp only [Matrix.mul_assoc]
        _ = (J' * P) * (Pinv * M * P) * Pinv := by rw [hP]
        _ = J' * ((P * Pinv) * M * (P * Pinv)) := by simp only [Matrix.mul_assoc]
        _ = J' * M := by rw [hr]; simp
    have e2 : P * ((Pinv * M * P) * J) * Pinv = M * J' := by
      calc P * ((Pinv * M * P) * J) * Pinv = (P * Pinv) * M * (P * J) * Pinv := by simp only [Matrix.mul_assoc]
        _ = M * (J' * P) * Pinv := by rw [hr, hP, Matrix.one_mul]
        _ = M * J' * (P * Pinv) := by simp only [Matrix.mul_assoc]
        _ = M * J' := by rw [hr, Matrix.mul_one]
    rw [e1, e2] at h2; exact h2
  · intro h
    rw [hJ]
    have l : Pinv * J' * P * (Pinv * M * P) = Pinv * (J' * ((P * Pinv) * M)) * P := by simp only [Matrix.mul_assoc]
    have r : (Pinv * M * P) * (Pinv * J' * P) = Pinv * (M * ((P * Pinv) * J')) * P := by simp only [Matrix.mul_assoc]
    rw [l, r, hr, Matrix.one_mul, Matrix.one_mul, h]

end Commutation

section Instances

/-- The standard `J` for `n = 1` as an explicit integer matrix. -/
def Jstd : Matrix (Fin 2) (Fin 2) ℤ := !![0, -1; 1, 0]
/-- Another integer square root of `-1`. -/
def Jother : Matrix (Fin 2) (Fin 2) ℤ := !![1, -1; 2, -1]
/-- An integer matrix of determinant 1 with `P J = J' P`. -/
def Pconj : Matrix (Fin 2) (Fin 2) ℤ := !![1, 0; 1, 1]
def PconjInv : Matrix (Fin 2) (Fin 2) ℤ := !![1, 0; -1, 1]

/-- INSTANCE (Fin 2, Int): `J' = [[1,-1],[2,-1]]` squares to `-1`, does not commute with `J`, and is conjugate to
`J` by a unimodular matrix.  Hence "commutes with J" and "commutes with J'" are different conditions: `J` is a
declaration (for `n = 1` the image of `R` is the commutant of the declared `J`), not a consequence. -/
theorem other_square_root_instance :
    Jother * Jother = -1 ∧ Jother * Jstd ≠ Jstd * Jother ∧ Pconj * Jstd = Jother * Pconj ∧
      PconjInv * Pconj = 1 ∧ Pconj * PconjInv = 1 := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · ext i j; fin_cases i <;> fin_cases j <;> simp [Jother, Matrix.mul_apply, Fin.sum_univ_two]
  · intro h
    have := congrFun (congrFun h 0) 0
    simp [Jother, Jstd, Matrix.mul_apply, Fin.sum_univ_two] at this
  · ext i j; fin_cases i <;> fin_cases j <;> simp [Pconj, Jother, Jstd, Matrix.mul_apply, Fin.sum_univ_two]
  · ext i j; fin_cases i <;> fin_cases j <;> simp [Pconj, PconjInv, Matrix.mul_apply, Fin.sum_univ_two]
  · ext i j; fin_cases i <;> fin_cases j <;> simp [Pconj, PconjInv, Matrix.mul_apply, Fin.sum_univ_two]

/-- INSTANCE: `J'` itself commutes with `J'` but is not in the image of `R` (it does not commute with `J`). -/
theorem other_root_not_in_image : ¬ (Jstd * Jother = Jother * Jstd) := fun h =>
  other_square_root_instance.2.1 h.symm

end Instances

end RealificationJ

#print axioms RealificationJ.R_add
#print axioms RealificationJ.R_smul
#print axioms RealificationJ.R_mul
#print axioms RealificationJ.R_one
#print axioms RealificationJ.R_injective
#print axioms RealificationJ.J_sq
#print axioms RealificationJ.J_R_comm
#print axioms RealificationJ.R_imul
#print axioms RealificationJ.R_star
#print axioms RealificationJ.hermitian_iff_symmetric
#print axioms RealificationJ.trace_R
#print axioms RealificationJ.trace_not_twice_complex_trace
#print axioms RealificationJ.image_iff
#print axioms RealificationJ.commutes_conj
#print axioms RealificationJ.other_square_root_instance
#print axioms RealificationJ.other_root_not_in_image
