import Mathlib.Data.Complex.Basic
import Mathlib.Data.Complex.BigOperators
import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.ConjTranspose
import Mathlib.Algebra.BigOperators.Group.Finset.Defs
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import ConcreteSemantics

namespace MUB.PolynomialEncoding

open MUB.ConcreteSemantics
open scoped BigOperators

structure Point where
  x : Fin 5 → Fin 5 → ℝ
  y : Fin 5 → Fin 5 → ℝ

def fullX (z : Point) (i j : Fin 6) : ℝ :=
  Fin.cases (fun _ ↦ 1) (fun i' ↦ Fin.cases 1 (fun j' ↦ z.x i' j')) i j

def fullY (z : Point) (i j : Fin 6) : ℝ :=
  Fin.cases (fun _ ↦ 0) (fun i' ↦ Fin.cases 0 (fun j' ↦ z.y i' j')) i j

@[simp] theorem fullX_zero_left (z : Point) (j : Fin 6) : fullX z 0 j = 1 := rfl

@[simp] theorem fullX_zero_right (z : Point) (i : Fin 6) : fullX z i 0 = 1 := by
  cases i using Fin.cases <;> rfl

@[simp] theorem fullX_succ_succ (z : Point) (i j : Fin 5) : fullX z i.succ j.succ = z.x i j := rfl

@[simp] theorem fullY_zero_left (z : Point) (j : Fin 6) : fullY z 0 j = 0 := rfl

@[simp] theorem fullY_zero_right (z : Point) (i : Fin 6) : fullY z i 0 = 0 := by
  cases i using Fin.cases <;> rfl

@[simp] theorem fullY_succ_succ (z : Point) (i j : Fin 5) : fullY z i.succ j.succ = z.y i j := rfl

def encode (H : Matrix (Fin 6) (Fin 6) ℂ) : Point :=
  ⟨fun i j ↦ (H i.succ j.succ).re, fun i j ↦ (H i.succ j.succ).im⟩

def decode (z : Point) : Matrix (Fin 6) (Fin 6) ℂ :=
  fun i j ↦ Complex.mk (fullX z i j) (fullY z i j)

theorem decode_isDephased (z : Point) : Dephased (decode z) := by
  constructor
  · intro j
    simp only [decode, fullX_zero_left, fullY_zero_left]
    exact Complex.ext rfl rfl
  · intro i
    simp only [decode, fullX_zero_right, fullY_zero_right]
    exact Complex.ext rfl rfl

theorem decode_encode (H : Matrix (Fin 6) (Fin 6) ℂ) (hH : Dephased H) :
    decode (encode H) = H := by
  ext i j
  cases i using Fin.cases with
  | zero =>
    have h0j : H 0 j = 1 := hH.1 j
    simp only [decode, fullX_zero_left, fullY_zero_left, h0j]
    exact Complex.ext rfl rfl
  | succ i' =>
    cases j using Fin.cases with
    | zero =>
      have hi0 : H i'.succ 0 = 1 := hH.2 i'.succ
      simp only [decode, fullX_zero_right, fullY_zero_right, hi0]
      exact Complex.ext rfl rfl
    | succ j' =>
      apply Complex.ext <;> rfl

theorem mul_star_decode_entry (z : Point) (i k j : Fin 6) :
    decode z i j * star (decode z k j) =
      Complex.mk (fullX z i j * fullX z k j + fullY z i j * fullY z k j)
                 (fullY z i j * fullX z k j - fullX z i j * fullY z k j) := by
  apply Complex.ext
  · simp only [decode, Complex.mul_re, Complex.star_def, Complex.conj_re, Complex.conj_im]
    ring
  · simp only [decode, Complex.mul_im, Complex.star_def, Complex.conj_re, Complex.conj_im]
    ring

/-- The 25 circle equations on the free entries: x_{i+1, j+1}^2 + y_{i+1, j+1}^2 - 1 = 0. -/
def circleResidue (z : Point) (i j : Fin 5) : ℝ :=
  (z.x i j) ^ 2 + (z.y i j) ^ 2 - 1

/-- The 15 real row-orthogonality equations for pairs 0 ≤ i < k < 6:
∑_{j=0}^5 (x_{i,j} x_{k,j} + y_{i,j} y_{k,j}) = 0. -/
def realRowOrthResidue (z : Point) (i k : Fin 6) : ℝ :=
  ∑ j : Fin 6, (fullX z i j * fullX z k j + fullY z i j * fullY z k j)

/-- The 15 imaginary row-orthogonality equations for pairs 0 ≤ i < k < 6:
∑_{j=0}^5 (y_{i,j} x_{k,j} - x_{i,j} y_{k,j}) = 0. -/
def imagRowOrthResidue (z : Point) (i k : Fin 6) : ℝ :=
  ∑ j : Fin 6, (fullY z i j * fullX z k j - fullX z i j * fullY z k j)

/-- The system of 55 real polynomial equations governing dephased 6x6 complex Hadamard matrices. -/
def Satisfies55 (z : Point) : Prop :=
  (∀ i j : Fin 5, circleResidue z i j = 0) ∧
  (∀ i k : Fin 6, i < k → realRowOrthResidue z i k = 0) ∧
  (∀ i k : Fin 6, i < k → imagRowOrthResidue z i k = 0)

theorem mul_conjTranspose_apply (z : Point) (i k : Fin 6) :
    (decode z * Matrix.conjTranspose (decode z)) i k =
      Complex.mk (realRowOrthResidue z i k) (imagRowOrthResidue z i k) := by
  apply Complex.ext
  · simp only [Matrix.mul_apply, Matrix.conjTranspose_apply, mul_star_decode_entry, Complex.re_sum]
    rfl
  · simp only [Matrix.mul_apply, Matrix.conjTranspose_apply, mul_star_decode_entry, Complex.im_sum]
    rfl

theorem mul_conjTranspose_re (z : Point) (i k : Fin 6) :
    ((decode z * Matrix.conjTranspose (decode z)) i k).re = realRowOrthResidue z i k := by
  rw [mul_conjTranspose_apply]

theorem mul_conjTranspose_im (z : Point) (i k : Fin 6) :
    ((decode z * Matrix.conjTranspose (decode z)) i k).im = imagRowOrthResidue z i k := by
  rw [mul_conjTranspose_apply]

theorem normSq_decode (z : Point) (i j : Fin 6) :
    Complex.normSq (decode z i j) = (fullX z i j) ^ 2 + (fullY z i j) ^ 2 := by
  rw [Complex.normSq_apply]
  dsimp [decode]
  ring

theorem normSq_full_one (z : Point) (h_circ : ∀ i j : Fin 5, circleResidue z i j = 0) (i j : Fin 6) :
    Complex.normSq (decode z i j) = 1 := by
  cases i using Fin.cases with
  | zero =>
    simp only [normSq_decode, fullX_zero_left, fullY_zero_left]
    ring
  | succ i' =>
    cases j using Fin.cases with
    | zero =>
      simp only [normSq_decode, fullX_zero_right, fullY_zero_right]
      ring
    | succ j' =>
      have hc := h_circ i' j'
      simp only [circleResidue] at hc
      simp only [normSq_decode, fullX_succ_succ, fullY_succ_succ]
      linarith

theorem circle_of_entrywiseUnit (z : Point) (h : EntrywiseUnit (decode z)) (i j : Fin 5) :
    circleResidue z i j = 0 := by
  have hij := h i.succ j.succ
  simp only [normSq_decode, fullX_succ_succ, fullY_succ_succ] at hij
  simp only [circleResidue]
  linarith

theorem entrywiseUnit_decode_iff (z : Point) :
    EntrywiseUnit (decode z) ↔ ∀ i j : Fin 5, circleResidue z i j = 0 :=
  ⟨circle_of_entrywiseUnit z, fun h i j ↦ normSq_full_one z h i j⟩

theorem diagonal_gram_of_circle (z : Point) (h_circle : ∀ i j : Fin 5, circleResidue z i j = 0) (i : Fin 6) :
    (∑ j : Fin 6, ((fullX z i j) ^ 2 + (fullY z i j) ^ 2)) = 6 := by
  have hj : ∀ j : Fin 6, (fullX z i j) ^ 2 + (fullY z i j) ^ 2 = 1 := by
    intro j
    have h_norm := normSq_full_one z h_circle i j
    rw [normSq_decode] at h_norm
    exact h_norm
  calc
    ∑ j : Fin 6, ((fullX z i j) ^ 2 + (fullY z i j) ^ 2) =
      ∑ j : Fin 6, (1 : ℝ) := by
        apply Finset.sum_congr rfl
        intro j _
        exact hj j
    _ = 6 := by
      simp

theorem realRowOrthResidue_self (z : Point)
    (h_circle : ∀ i j : Fin 5, circleResidue z i j = 0) (i : Fin 6) :
    realRowOrthResidue z i i = 6 := by
  simp only [realRowOrthResidue]
  calc
    ∑ j : Fin 6, (fullX z i j * fullX z i j + fullY z i j * fullY z i j) =
      ∑ j : Fin 6, ((fullX z i j) ^ 2 + (fullY z i j) ^ 2) := by
        apply Finset.sum_congr rfl
        intro j _
        ring
    _ = 6 := diagonal_gram_of_circle z h_circle i

theorem imagRowOrthResidue_self (z : Point) (i : Fin 6) :
    imagRowOrthResidue z i i = 0 := by
  simp only [imagRowOrthResidue]
  have h : ∀ j : Fin 6, fullY z i j * fullX z i j - fullX z i j * fullY z i j = 0 := by
    intro j; ring
  calc
    ∑ j : Fin 6, (fullY z i j * fullX z i j - fullX z i j * fullY z i j) =
      ∑ j : Fin 6, (0 : ℝ) := by
        apply Finset.sum_congr rfl
        intro j _
        exact h j
    _ = 0 := by simp

theorem realRowOrthResidue_comm (z : Point) (i k : Fin 6) :
    realRowOrthResidue z i k = realRowOrthResidue z k i := by
  simp only [realRowOrthResidue]
  apply Finset.sum_congr rfl
  intro j _
  ring

theorem imagRowOrthResidue_skew (z : Point) (i k : Fin 6) :
    imagRowOrthResidue z k i = - imagRowOrthResidue z i k := by
  simp only [imagRowOrthResidue]
  rw [← Finset.sum_neg_distrib]
  apply Finset.sum_congr rfl
  intro j _
  ring

theorem mul_conjTranspose_eq_six_smul_one (z : Point) (h : Satisfies55 z) :
    decode z * Matrix.conjTranspose (decode z) = (6 : ℂ) • 1 := by
  ext i k
  simp only [Matrix.smul_apply, Matrix.one_apply]
  rw [mul_conjTranspose_apply]
  rcases lt_trichotomy i k with hik | rfl | hki
  · have h_re := h.2.1 i k hik
    have h_im := h.2.2 i k hik
    rw [h_re, h_im]
    have h_ne : i ≠ k := ne_of_lt hik
    simp [h_ne]
    exact Complex.ext rfl rfl
  · have h_re := realRowOrthResidue_self z h.1 i
    have h_im := imagRowOrthResidue_self z i
    rw [h_re, h_im]
    simp
    exact Complex.ext rfl rfl
  · have h_re := h.2.1 k i hki
    have h_im := h.2.2 k i hki
    rw [realRowOrthResidue_comm z i k, h_re]
    rw [imagRowOrthResidue_skew z k i, h_im, neg_zero]
    have h_ne : i ≠ k := ne_of_gt hki
    simp [h_ne]
    exact Complex.ext rfl rfl

theorem isCH6_decode_of_satisfies55 (z : Point) (h : Satisfies55 z) : IsCH6 (decode z) :=
  ⟨(entrywiseUnit_decode_iff z).2 h.1, mul_conjTranspose_eq_six_smul_one z h⟩

theorem satisfies55_of_isCH6_decode (z : Point) (h : IsCH6 (decode z)) : Satisfies55 z := by
  refine ⟨(entrywiseUnit_decode_iff z).1 h.1, ?_, ?_⟩
  · intro i k hik
    have h_entry := congrArg (fun M : Matrix (Fin 6) (Fin 6) ℂ ↦ M i k) h.2
    simp only [Matrix.smul_apply, Matrix.one_apply, if_neg (ne_of_lt hik)] at h_entry
    rw [mul_conjTranspose_apply] at h_entry
    have h_re := congrArg Complex.re h_entry
    simpa using h_re
  · intro i k hik
    have h_entry := congrArg (fun M : Matrix (Fin 6) (Fin 6) ℂ ↦ M i k) h.2
    simp only [Matrix.smul_apply, Matrix.one_apply, if_neg (ne_of_lt hik)] at h_entry
    rw [mul_conjTranspose_apply] at h_entry
    have h_im := congrArg Complex.im h_entry
    simpa using h_im

/-- Master bidirectional equivalence theorem: A real point satisfies the 55 polynomial equations
if and only if its decoded complex matrix is a dephased order-six complex Hadamard matrix. -/
theorem bidirectional_equivalence (z : Point) :
    Satisfies55 z ↔ (IsCH6 (decode z) ∧ Dephased (decode z)) := by
  constructor
  · intro h
    exact ⟨isCH6_decode_of_satisfies55 z h, decode_isDephased z⟩
  · intro h
    exact satisfies55_of_isCH6_decode z h.1

/-- Completeness theorem: Every dephased order-six complex Hadamard matrix encodes to a
real point satisfying the 55 polynomial equations. -/
theorem completeness (H : Matrix (Fin 6) (Fin 6) ℂ) (hCH : IsCH6 H) (hDeph : Dephased H) :
    Satisfies55 (encode H) := by
  have heq : decode (encode H) = H := decode_encode H hDeph
  have hCH_dec : IsCH6 (decode (encode H)) := by rw [heq]; exact hCH
  exact satisfies55_of_isCH6_decode (encode H) hCH_dec

/-- Connection to Prompt 03's `dephase_exists`: Every order-six complex Hadamard matrix has an
equivalent representative decoded from a real point satisfying the 55 polynomial equations. -/
theorem exists_real_solution_of_isCH6 (H : Matrix (Fin 6) (Fin 6) ℂ) (hH : IsCH6 H) :
    ∃ z, Satisfies55 z ∧ HadamardEquivalent H (decode z) := by
  rcases dephase_exists H hH with ⟨D, hD_CH, hD_Deph, hHD⟩
  refine ⟨encode D, completeness D hD_CH hD_Deph, ?_⟩
  rw [decode_encode D hD_Deph]
  exact hHD

#print axioms decode_isDephased
#print axioms decode_encode
#print axioms entrywiseUnit_decode_iff
#print axioms diagonal_gram_of_circle
#print axioms mul_conjTranspose_eq_six_smul_one
#print axioms isCH6_decode_of_satisfies55
#print axioms satisfies55_of_isCH6_decode
#print axioms bidirectional_equivalence
#print axioms completeness
#print axioms exists_real_solution_of_isCH6

end MUB.PolynomialEncoding
