import Mathlib.Data.Complex.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.ConjTranspose
import Mathlib.Algebra.BigOperators.Group.Finset.Defs
import Mathlib.Tactic.Ring

/-!
# Concrete Matrix Semantics and Dephasing Normalization for Order-Six Complex Hadamard Matrices

This module implements the concrete semantics of 6x6 complex Hadamard matrices over `ℂ`,
establishing the standard Hadamard equivalence relation (row/column permutations and diagonal
unitary phases), proving equivalence relation properties (reflexivity, symmetry, transitivity),
invariance of the complex Hadamard property under equivalence, and the existence of a dephased
equivalent representative via explicit algebraic conjugation factors without transcendental inverse.

AuthorityEffect: None.
-/

namespace MUB.ConcreteSemantics

/-- Every entry of `H` lies on the complex unit circle. -/
def EntrywiseUnit (H : Matrix (Fin 6) (Fin 6) ℂ) : Prop :=
  ∀ i j, Complex.normSq (H i j) = 1

/-- The concrete complex Hadamard matrix condition in dimension 6 over `ℂ`. -/
def IsCH6 (H : Matrix (Fin 6) (Fin 6) ℂ) : Prop :=
  EntrywiseUnit H ∧ H * Matrix.conjTranspose H = (6 : ℂ) • 1

/-- A 6x6 complex matrix is dephased if its first row and first column are identically 1. -/
def Dephased (H : Matrix (Fin 6) (Fin 6) ℂ) : Prop :=
  (∀ j, H 0 j = 1) ∧ (∀ i, H i 0 = 1)

/-- Standard Hadamard equivalence: permutation of rows and columns together with
multiplication of rows and columns by complex unit phases. -/
def HadamardEquivalent (H K : Matrix (Fin 6) (Fin 6) ℂ) : Prop :=
  ∃ (σ τ : Equiv.Perm (Fin 6)) (r c : Fin 6 → ℂ),
    (∀ i, Complex.normSq (r i) = 1) ∧
    (∀ j, Complex.normSq (c j) = 1) ∧
    ∀ i j, K i j = r i * H (σ i) (τ j) * c j

/-!
### Auxiliary Algebraic Lemmas on Complex Unit Circle Entries
-/

theorem star_mul_self_of_normSq_one {z : ℂ}
    (hz : Complex.normSq z = 1) : star z * z = 1 := by
  simpa [Complex.star_def, Complex.normSq_eq_conj_mul_self] using
    congrArg (fun a : ℝ ↦ (a : ℂ)) hz

theorem mul_star_self_of_normSq_one {z : ℂ}
    (hz : Complex.normSq z = 1) : z * star z = 1 := by
  rw [mul_comm]
  exact star_mul_self_of_normSq_one hz

/-!
### Equivalence Relation Theorems
-/

theorem hadamard_equiv_refl (H : Matrix (Fin 6) (Fin 6) ℂ) :
    HadamardEquivalent H H := by
  refine ⟨Equiv.refl (Fin 6), Equiv.refl (Fin 6), (fun _ ↦ 1), (fun _ ↦ 1), ?_, ?_, ?_⟩
  · intro i
    simp
  · intro j
    simp
  · intro i j
    simp

theorem hadamard_equiv_trans {H K L : Matrix (Fin 6) (Fin 6) ℂ}
    (hHK : HadamardEquivalent H K) (hKL : HadamardEquivalent K L) :
    HadamardEquivalent H L := by
  rcases hHK with ⟨σ₁, τ₁, r₁, c₁, hr₁, hc₁, hHK⟩
  rcases hKL with ⟨σ₂, τ₂, r₂, c₂, hr₂, hc₂, hKL⟩
  refine ⟨σ₂.trans σ₁, τ₂.trans τ₁,
    (fun i ↦ r₂ i * r₁ (σ₂ i)),
    (fun j ↦ c₁ (τ₂ j) * c₂ j), ?_, ?_, ?_⟩
  · intro i
    simp [Complex.normSq_mul, hr₂ i, hr₁ (σ₂ i)]
  · intro j
    simp [Complex.normSq_mul, hc₁ (τ₂ j), hc₂ j]
  · intro i j
    rw [hKL, hHK]
    simp only [Equiv.trans_apply]
    ring

theorem hadamard_equiv_symm {H K : Matrix (Fin 6) (Fin 6) ℂ}
    (hHK : HadamardEquivalent H K) : HadamardEquivalent K H := by
  rcases hHK with ⟨σ, τ, r, c, hr, hc, hHK⟩
  refine ⟨σ.symm, τ.symm,
    (fun i ↦ star (r (σ.symm i))),
    (fun j ↦ star (c (τ.symm j))), ?_, ?_, ?_⟩
  · intro i
    simpa [Complex.star_def, Complex.normSq_conj] using hr (σ.symm i)
  · intro j
    simpa [Complex.star_def, Complex.normSq_conj] using hc (τ.symm j)
  · intro i j
    have h := hHK (σ.symm i) (τ.symm j)
    simp only [Equiv.apply_symm_apply] at h ⊢
    have hri : star (r (σ.symm i)) * r (σ.symm i) = 1 :=
      star_mul_self_of_normSq_one (hr (σ.symm i))
    have hcj : c (τ.symm j) * star (c (τ.symm j)) = 1 :=
      mul_star_self_of_normSq_one (hc (τ.symm j))
    rw [h]
    symm
    calc
      star (r (σ.symm i)) *
          (r (σ.symm i) * H i j * c (τ.symm j)) *
          star (c (τ.symm j)) =
        (star (r (σ.symm i)) * r (σ.symm i)) * H i j *
          (c (τ.symm j) * star (c (τ.symm j))) := by ring
      _ = H i j := by rw [hri, hcj]; simp

theorem hadamard_equiv_equivalence : Equivalence HadamardEquivalent :=
  ⟨hadamard_equiv_refl, hadamard_equiv_symm, hadamard_equiv_trans⟩

/-!
### Transport of CH6 along Equivalence
-/

def reindexMatrix (σ τ : Equiv.Perm (Fin 6)) (H : Matrix (Fin 6) (Fin 6) ℂ) :
    Matrix (Fin 6) (Fin 6) ℂ :=
  fun i j ↦ H (σ i) (τ j)

theorem reindexMatrix_isCH6 {σ τ : Equiv.Perm (Fin 6)} {H : Matrix (Fin 6) (Fin 6) ℂ}
    (hH : IsCH6 H) : IsCH6 (reindexMatrix σ τ H) := by
  constructor
  · intro i j
    exact hH.1 (σ i) (τ j)
  · ext i j
    change (∑ k, H (σ i) (τ k) * star (H (σ j) (τ k))) = _
    rw [τ.sum_comp Finset.univ (fun k ↦ H (σ i) k * star (H (σ j) k)) (by simp)]
    have hentry := congrArg (fun M : Matrix (Fin 6) (Fin 6) ℂ ↦ M (σ i) (σ j)) hH.2
    simp only [Matrix.mul_apply, Matrix.conjTranspose_apply,
      Matrix.smul_apply, Matrix.one_apply] at hentry ⊢
    by_cases hij : i = j
    · subst j
      simpa using hentry
    · have hsij : σ i ≠ σ j := fun h ↦ hij (σ.injective h)
      simpa [hij, hsij] using hentry

def phaseTransform (r c : Fin 6 → ℂ) (H : Matrix (Fin 6) (Fin 6) ℂ) :
    Matrix (Fin 6) (Fin 6) ℂ :=
  fun i j ↦ r i * H i j * c j

theorem phaseTransform_entrywiseUnit {r c : Fin 6 → ℂ} {H : Matrix (Fin 6) (Fin 6) ℂ}
    (hr : ∀ i, Complex.normSq (r i) = 1)
    (hc : ∀ j, Complex.normSq (c j) = 1)
    (hH : EntrywiseUnit H) :
    EntrywiseUnit (phaseTransform r c H) := by
  intro i j
  simp [phaseTransform, Complex.normSq_mul, hr i, hc j, hH i j]

theorem phaseTransform_rowGram {r c : Fin 6 → ℂ} {H : Matrix (Fin 6) (Fin 6) ℂ}
    (hc : ∀ j, Complex.normSq (c j) = 1) :
    phaseTransform r c H * Matrix.conjTranspose (phaseTransform r c H) =
      fun i j ↦ r i * (H * Matrix.conjTranspose H) i j * star (r j) := by
  ext i j
  simp only [Matrix.mul_apply, Matrix.conjTranspose_apply, phaseTransform, star_mul]
  change
    (∑ k, (r i * H i k * c k) *
      (star (c k) * (star (H j k) * star (r j)))) =
      r i * (∑ k, H i k * star (H j k)) * star (r j)
  calc
    ∑ k, (r i * H i k * c k) *
        (star (c k) * (star (H j k) * star (r j))) =
      ∑ k, r i * (H i k * star (H j k)) * star (r j) := by
        apply Finset.sum_congr rfl
        intro k _
        have hck : c k * star (c k) = 1 := mul_star_self_of_normSq_one (hc k)
        calc
          (r i * H i k * c k) *
              (star (c k) * (star (H j k) * star (r j))) =
            r i * H i k * (c k * star (c k)) *
              star (H j k) * star (r j) := by ring
          _ = r i * (H i k * star (H j k)) * star (r j) := by
            rw [hck]
            ring
    _ = r i * (∑ k, H i k * star (H j k)) * star (r j) := by
      rw [Finset.mul_sum, Finset.sum_mul]

theorem phaseTransform_isCH6 {r c : Fin 6 → ℂ} {H : Matrix (Fin 6) (Fin 6) ℂ}
    (hr : ∀ i, Complex.normSq (r i) = 1)
    (hc : ∀ j, Complex.normSq (c j) = 1)
    (hH : IsCH6 H) : IsCH6 (phaseTransform r c H) := by
  refine ⟨phaseTransform_entrywiseUnit hr hc hH.1, ?_⟩
  rw [phaseTransform_rowGram hc, hH.2]
  ext i j
  simp only [Matrix.smul_apply, Matrix.one_apply]
  by_cases hij : i = j
  · subst j
    have hri : r i * star (r i) = 1 := mul_star_self_of_normSq_one (hr i)
    simp only [if_pos, smul_eq_mul, mul_one]
    calc
      r i * (6 : ℂ) * star (r i) = 6 * (r i * star (r i)) := by ring
      _ = (6 : ℂ) := by rw [hri]; ring
  · simp [hij]

theorem isCH6_of_equivalent {H K : Matrix (Fin 6) (Fin 6) ℂ}
    (hHK : HadamardEquivalent H K) (hH : IsCH6 H) : IsCH6 K := by
  rcases hHK with ⟨σ, τ, r, c, hr, hc, hHK⟩
  have hperm : IsCH6 (reindexMatrix σ τ H) := reindexMatrix_isCH6 hH
  have hphase : K = phaseTransform r c (reindexMatrix σ τ H) := by
    ext i j
    simp [phaseTransform, reindexMatrix, hHK]
  rw [hphase]
  exact phaseTransform_isCH6 hr hc hperm

theorem equivalent_isCH6_iff {H K : Matrix (Fin 6) (Fin 6) ℂ}
    (hHK : HadamardEquivalent H K) : IsCH6 H ↔ IsCH6 K :=
  ⟨isCH6_of_equivalent hHK, isCH6_of_equivalent (hadamard_equiv_symm hHK)⟩

/-!
### Exact Algebraic Dephasing Normalization
-/

/-- Left phase factor for row dephasing: conjugate of entry in the first column. -/
def dephaseRowFactor (H : Matrix (Fin 6) (Fin 6) ℂ) (i : Fin 6) : ℂ :=
  star (H i 0)

/-- Right phase factor for column dephasing: conjugate of entry in the first row times (0,0) entry. -/
def dephaseColumnFactor (H : Matrix (Fin 6) (Fin 6) ℂ) (j : Fin 6) : ℂ :=
  star (H 0 j) * H 0 0

/-- Concrete algebraic dephasing transformation. -/
def dephase (H : Matrix (Fin 6) (Fin 6) ℂ) : Matrix (Fin 6) (Fin 6) ℂ :=
  fun i j ↦ dephaseRowFactor H i * H i j * dephaseColumnFactor H j

theorem dephaseRowFactor_unit (H : Matrix (Fin 6) (Fin 6) ℂ)
    (hH : EntrywiseUnit H) (i : Fin 6) :
    Complex.normSq (dephaseRowFactor H i) = 1 := by
  simpa [dephaseRowFactor, Complex.star_def, Complex.normSq_conj] using hH i 0

theorem dephaseColumnFactor_unit (H : Matrix (Fin 6) (Fin 6) ℂ)
    (hH : EntrywiseUnit H) (j : Fin 6) :
    Complex.normSq (dephaseColumnFactor H j) = 1 := by
  simp [dephaseColumnFactor, Complex.normSq_mul, Complex.star_def,
    Complex.normSq_conj, hH 0 j, hH 0 0]

theorem dephase_isDephased (H : Matrix (Fin 6) (Fin 6) ℂ)
    (hH : EntrywiseUnit H) : Dephased (dephase H) := by
  have h00 := star_mul_self_of_normSq_one (hH 0 0)
  constructor
  · intro j
    simp only [dephase, dephaseRowFactor, dephaseColumnFactor]
    calc
      star (H 0 0) * H 0 j * (star (H 0 j) * H 0 0) =
        (star (H 0 j) * H 0 j) * (star (H 0 0) * H 0 0) := by ring
      _ = 1 := by
        rw [star_mul_self_of_normSq_one (hH 0 j), h00]
        norm_num
  · intro i
    simp only [dephase, dephaseRowFactor, dephaseColumnFactor]
    calc
      star (H i 0) * H i 0 * (star (H 0 0) * H 0 0) =
        (star (H i 0) * H i 0) * (star (H 0 0) * H 0 0) := by ring
      _ = 1 := by
        rw [star_mul_self_of_normSq_one (hH i 0), h00]
        norm_num

theorem dephase_isCH6 (H : Matrix (Fin 6) (Fin 6) ℂ)
    (hH : IsCH6 H) : IsCH6 (dephase H) :=
  phaseTransform_isCH6
    (fun i ↦ dephaseRowFactor_unit H hH.1 i)
    (fun j ↦ dephaseColumnFactor_unit H hH.1 j) hH

theorem equivalent_dephase (H : Matrix (Fin 6) (Fin 6) ℂ)
    (hH : EntrywiseUnit H) : HadamardEquivalent H (dephase H) := by
  refine ⟨Equiv.refl (Fin 6), Equiv.refl (Fin 6),
    dephaseRowFactor H, dephaseColumnFactor H,
    dephaseRowFactor_unit H hH,
    dephaseColumnFactor_unit H hH,
    fun i j ↦ rfl⟩

/-- Main existence theorem: Every order-six complex Hadamard matrix has an
algebraically equivalent dephased complex Hadamard representative. -/
theorem dephase_exists (H : Matrix (Fin 6) (Fin 6) ℂ) (hH : IsCH6 H) :
    ∃ D, IsCH6 D ∧ Dephased D ∧ HadamardEquivalent H D :=
  ⟨dephase H, dephase_isCH6 H hH, dephase_isDephased H hH.1, equivalent_dephase H hH.1⟩

#print axioms dephase_exists
#print axioms isCH6_of_equivalent
#print axioms hadamard_equiv_equivalence

end MUB.ConcreteSemantics
