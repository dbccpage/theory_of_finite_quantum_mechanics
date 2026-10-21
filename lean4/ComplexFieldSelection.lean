import BornGaussRat
import Mathlib.Data.Nat.Choose.Basic
import Mathlib.LinearAlgebra.Matrix.Kronecker
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.LinearAlgebra.Matrix.ConjTranspose
import Mathlib.Algebra.Star.SelfAdjoint
import Mathlib.Tactic
import Mathlib.Data.Matrix.Basis

/-! Exact conditional carrier selection. AuthorityEffect: None.
Classification, same-family composites and operational tomography are supplied.
The unrestricted natural-number theorem has the additional solution d = 0.
-/
namespace ComplexFieldSelection
open Matrix
open scoped BigOperators Kronecker

def K (d n : ℕ) : ℕ := n + d * n.choose 2

theorem dimension_formula (d n : ℕ) :
    K d n = n + d * (n * (n - 1) / 2) := by
  simp [K, Nat.choose_two_right]

def Multiplicative (d : ℕ) : Prop :=
  ∀ n m : ℕ, 2 ≤ n → 2 ≤ m → K d (n * m) = K d n * K d m

theorem complex_dimension (n : ℕ) : K 2 n = n * n := by
  induction n with
  | zero => norm_num [K]
  | succ n ih =>
    simp only [K] at ih ⊢
    rw [Nat.choose_succ_succ, Nat.choose_one_right]
    nlinarith

theorem complex_multiplicative : Multiplicative 2 := by
  intro n m _ _
  simp only [complex_dimension]
  ring

theorem zero_multiplicative : Multiplicative 0 := by
  intro n m _ _
  simp [K]

theorem two_pair_selects (d : ℕ) (hd : 0 < d)
    (h : K d 4 = K d 2 * K d 2) : d = 2 := by
  norm_num [K, Nat.choose] at h
  have hlo : 2 ≤ d := by
    by_contra hn
    have : d = 1 := by omega
    subst d
    norm_num at h
  nlinarith

theorem dimension_selection (d : ℕ) (hd : 0 < d) :
    Multiplicative d ↔ d = 2 := by
  constructor
  · intro h
    exact two_pair_selects d hd (h 2 2 (by omega) (by omega))
  · rintro rfl
    exact complex_multiplicative

theorem unrestricted_selection (d : ℕ) : Multiplicative d ↔ d = 0 ∨ d = 2 := by
  by_cases hd : d = 0
  · subst d
    simp [zero_multiplicative]
  · simpa [hd] using dimension_selection d (Nat.pos_of_ne_zero hd)

theorem failing_pair_refutes (d n m : ℕ) (hn : 2 ≤ n) (hm : 2 ≤ m)
    (h : K d (n*m) ≠ K d n * K d m) : ¬ Multiplicative d :=
  fun hmul => h (hmul n m hn hm)

theorem real_count : K 1 2 * K 1 2 = 9 ∧ K 1 4 = 10 := by decide
theorem quaternion_count : K 4 2 * K 4 2 = 36 ∧ K 4 4 = 28 := by decide

theorem real_refuted : ¬ Multiplicative 1 :=
  failing_pair_refutes 1 2 2 (by omega) (by omega) (by decide)
theorem quaternion_refuted : ¬ Multiplicative 4 :=
  failing_pair_refutes 4 2 2 (by omega) (by omega) (by decide)

theorem trivial_factor_passes (d n : ℕ) : K d (1*n) = K d 1 * K d n := by
  simp [K]

inductive Carrier where
  | real | complex | quaternion
  deriving DecidableEq

def scalarDimension : Carrier → ℕ
  | .real => 1
  | .complex => 2
  | .quaternion => 4

theorem conditional_discharge (c : Carrier) (h : Multiplicative (scalarDimension c)) :
    c = .complex := by
  cases c with
  | real => exact (real_refuted h).elim
  | complex => rfl
  | quaternion => exact (quaternion_refuted h).elim

abbrev R2 := Matrix (Fin 2) (Fin 2) ℚ
abbrev R4 := Matrix (Fin 2 × Fin 2) (Fin 2 × Fin 2) ℚ

def Y : R2 := !![0, -1; 1, 0]
def delta : R4 := Y ⊗ₖ Y

def Symmetric {ι : Type*} (A : Matrix ι ι ℚ) : Prop := ∀ i j, A i j = A j i

theorem delta_symmetric : Symmetric delta := by
  intro ⟨i,j⟩ ⟨k,l⟩
  fin_cases i <;> fin_cases j <;> fin_cases k <;> fin_cases l <;> norm_num [delta, Y]

theorem delta_nonzero : delta ≠ 0 := by
  intro h
  have := congrFun (congrFun h (0,0)) (1,1)
  norm_num [delta, Y] at this

theorem skew_trace_zero (A : R2) (hA : Symmetric A) : (Y * A).trace = 0 := by
  have h := hA 0 1
  simp [Matrix.trace, Matrix.mul_apply, Matrix.vecMul, dotProduct, Fin.sum_univ_two, Y]
  linarith

theorem real_product_orthogonality (A B : R2) (hA : Symmetric A) (hB : Symmetric B) :
    (delta * (A ⊗ₖ B)).trace = 0 := by
  rw [delta, ← mul_kronecker_mul, trace_kronecker, skew_trace_zero A hA]
  simp

def rhoPlus : R4 := (1/4 : ℚ) • (1 + delta)
def rhoMinus : R4 := (1/4 : ℚ) • (1 - delta)
def quadratic (A : R4) (x : Fin 2 × Fin 2 → ℚ) : ℚ :=
  ∑ i, ∑ j, x i * A i j * x j

def RationalState (A : R4) : Prop := Symmetric A ∧ A.trace = 1 ∧ ∀ x, 0 ≤ quadratic A x

theorem rho_quadratic (x : Fin 2 × Fin 2 → ℚ) :
    quadratic rhoPlus x = ((x (0,0) + x (1,1))^2 + (x (0,1) - x (1,0))^2)/4 ∧
    quadratic rhoMinus x = ((x (0,0) - x (1,1))^2 + (x (0,1) + x (1,0))^2)/4 := by
  constructor <;>
    simp [quadratic, rhoPlus, rhoMinus, delta, Y, Fintype.sum_prod_type,
      Fin.sum_univ_two, Matrix.one_apply] <;> ring

theorem rho_states : RationalState rhoPlus ∧ RationalState rhoMinus := by
  have hs (s : ℚ) : Symmetric ((1/4 : ℚ) • (1 + s • delta)) := by
    intro i j
    simp only [Matrix.smul_apply, Matrix.add_apply, smul_eq_mul]
    rw [delta_symmetric i j]
    congr 2
    simp [Matrix.one_apply, eq_comm]
  constructor
  · refine ⟨?_, ?_, ?_⟩
    · simpa [rhoPlus] using hs 1
    · norm_num [rhoPlus, delta, Y, Matrix.trace, Fintype.sum_prod_type, Fin.sum_univ_two]
    · intro x
      rw [(rho_quadratic x).1]
      positivity
  · refine ⟨?_, ?_, ?_⟩
    · simpa [rhoMinus, sub_eq_add_neg] using hs (-1)
    · norm_num [rhoMinus, delta, Y, Matrix.trace, Fintype.sum_prod_type, Fin.sum_univ_two]
    · intro x
      rw [(rho_quadratic x).2]
      positivity

theorem rho_distinct : rhoPlus ≠ rhoMinus := by
  intro h
  have := congrFun (congrFun h (0,0)) (1,1)
  norm_num [rhoPlus, rhoMinus, delta, Y, Matrix.one_apply] at this

theorem rho_same_product_statistics (A B : R2) (hA : Symmetric A) (hB : Symmetric B) :
    (rhoPlus * (A ⊗ₖ B)).trace = (rhoMinus * (A ⊗ₖ B)).trace := by
  simp [rhoPlus, rhoMinus, add_mul, sub_mul, real_product_orthogonality A B hA hB]


/- The existing TensorTomography.product_span is over C/R. This exact analogue
uses the already constructed Gaussian-rational field, with Q-linear span. -/
open BornFable
abbrev GMat (n : Type*) := Matrix n n GaussRat

def symPart {n : Type*} (A : GMat n) : GMat n := (1/2 : ℚ) • (A + Aᴴ)
def imagPart {n : Type*} (A : GMat n) : GMat n :=
  fun i j => (1/2 : ℚ) • ((-GaussRat.I) * (A i j - star (A j i)))

theorem symPart_hermitian {n : Type*} (A : GMat n) : (symPart A)ᴴ = symPart A := by
  ext i j <;> simp [symPart, Matrix.conjTranspose_apply] <;> ring

theorem imagPart_hermitian {n : Type*} (A : GMat n) : (imagPart A)ᴴ = imagPart A := by
  ext i j <;> simp [imagPart, Matrix.conjTranspose_apply] <;> ring

theorem symPart_product {n m : Type*} (A : GMat n) (B : GMat m) :
    symPart (A ⊗ₖ B) = symPart A ⊗ₖ symPart B - imagPart A ⊗ₖ imagPart B := by
  ext ⟨i,k⟩ ⟨j,l⟩ <;>
    simp [symPart, imagPart, Matrix.conjTranspose_apply, Matrix.kronecker_apply] <;> ring

/-- Every Gaussian-rational Hermitian joint matrix lies in the Q-linear span
of local Hermitian products, for arbitrary finite index types. -/
theorem gaussian_product_span {n m : Type*} [Fintype n] [Fintype m]
    (H : GMat (n × m)) (hH : Hᴴ = H) :
    H ∈ Submodule.span ℚ {P : GMat (n × m) | ∃ A : GMat n, ∃ B : GMat m,
      Aᴴ = A ∧ Bᴴ = B ∧ P = A ⊗ₖ B} := by
  classical
  let S := Submodule.span ℚ {P : GMat (n × m) | ∃ A : GMat n, ∃ B : GMat m,
      Aᴴ = A ∧ Bᴴ = B ∧ P = A ⊗ₖ B}
  have hp (A : GMat n) (B : GMat m) (ha : Aᴴ = A) (hb : Bᴴ = B) : A ⊗ₖ B ∈ S :=
    Submodule.subset_span ⟨A, B, ha, hb, rfl⟩
  have hr (X : GMat (n × m)) : symPart X ∈ S := by
    refine Matrix.induction_on' X ?_ ?_ ?_
    · simpa [symPart] using S.zero_mem
    · intro X Y hx hy
      have he : symPart (X + Y) = symPart X + symPart Y := by
        ext i j <;> simp [symPart, Matrix.conjTranspose_apply] <;> ring
      rw [he]
      exact S.add_mem hx hy
    · intro i j z
      have he : single i j z = single i.1 j.1 z ⊗ₖ single i.2 j.2 (1 : GaussRat) := by
        simp [single_kronecker_single]
      rw [he, symPart_product]
      exact S.sub_mem (hp _ _ (symPart_hermitian _) (symPart_hermitian _))
        (hp _ _ (imagPart_hermitian _) (imagPart_hermitian _))
  have he : symPart H = H := by
    rw [symPart, hH]
    ext i j <;> simp <;> ring
  simpa only [he] using hr H

#print axioms dimension_formula
#print axioms complex_dimension
#print axioms complex_multiplicative
#print axioms zero_multiplicative
#print axioms real_count
#print axioms quaternion_count
#print axioms rho_quadratic
#print axioms gaussian_product_span
#print axioms dimension_selection
#print axioms unrestricted_selection
#print axioms two_pair_selects
#print axioms failing_pair_refutes
#print axioms real_refuted
#print axioms quaternion_refuted
#print axioms trivial_factor_passes
#print axioms conditional_discharge
#print axioms real_product_orthogonality
#print axioms delta_symmetric
#print axioms delta_nonzero
#print axioms rho_states
#print axioms rho_distinct
#print axioms rho_same_product_statistics
end ComplexFieldSelection
