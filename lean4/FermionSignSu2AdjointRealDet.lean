import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Analysis.Complex.Basic
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.LinearAlgebra.Matrix.Block
import Mathlib.LinearAlgebra.Matrix.ConjTranspose
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.LinearCombination
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-!
# FSP-SU2-ADJOINT-REAL-DET (TFQ-1200)

AuthorityEffect: None.
Origin: lean4/FermionSignSu2AdjointRealDet.lean

Scope:
1. Explicit 3x3 real adjoint representation `su2AdjointMatrix a b c d` of a quaternion / SU(2)
   tuple `(a, b, c, d)` on `Fin 3`, proving `Z_2` center blindness (`R(-q) = R(q)`),
   orthogonality (`R^T R = I_3` and `R R^T = I_3` when `a^2 + b^2 + c^2 + d^2 = 1`),
   determinant formula `det R = (a^2 + b^2 + c^2 + d^2)^3 = 1`, and invariance under complex
   conjugation when lifted to `ℂ`.
2. General antiunitary intertwiner reality theorem (`antiunitary_intertwiner_det_conj`,
   `antiunitary_intertwiner_det_im_zero`): for any complex matrix `D` and invertible
   intertwiner `C` (`C.det ≠ 0`) satisfying `C * matConj D = D * C`, `star D.det = D.det`
   and `(D.det).im = 0`, with nonnegative two-flavor square `0 ≤ ((fromBlocks D 0 0 D).det).re`.
3. Explicit 4D Euclidean charge-conjugation intertwiner `chargeConj4` (`chargeConj4^2 = -1`,
   `chargeConj4.det = 1`) intertwining the 4D Euclidean Clifford generators `gamma4d μ` and
   `gamma5Four`, lifted to `fullIntertwiner4` on `Spin4 × (Site × Fin 3)` to establish that
   the 4D lattice adjoint Wilson-Dirac operator `wilsonDiracAdjoint4` has a real determinant
   for every finite site type, real mass, Wilson parameter, and real adjoint link configuration.
4. Explicit witnesses separating determinant reality from positivity (`reality_not_positivity_witness`,
   where `star D.det = D.det` and `(D.det).re = -1 < 0`) and proving the 2x2 and 4x4 skew-symmetric
   Majorana Pfaffian identity `det M = (Pf M)^2` together with explicit Pfaffian sign-flip pairs
   (`Pf = +1` vs `Pf = -1` at identical positive determinant `det = 1`).
-/

open scoped BigOperators
open Matrix Complex

namespace FermionSignSu2AdjointRealDet

noncomputable section

/-! ## Part I: Explicit SU(2) -> SO(3) Real Adjoint Representation -/

/-- The 3x3 real adjoint matrix associated with quaternion parameters `(a, b, c, d)`.
For a unit quaternion `a^2 + b^2 + c^2 + d^2 = 1` representing `U ∈ SU(2)`, this is the
exact `SO(3)` matrix of the adjoint action `X ↦ U X U†` on traceless Hermitian 2x2 matrices. -/
def su2AdjointMatrix (a b c d : ℝ) : Matrix (Fin 3) (Fin 3) ℝ :=
  !![a ^ 2 + b ^ 2 - c ^ 2 - d ^ 2, 2 * (b * c - a * d), 2 * (b * d + a * c);
     2 * (b * c + a * d), a ^ 2 - b ^ 2 + c ^ 2 - d ^ 2, 2 * (c * d - a * b);
     2 * (b * d - a * c), 2 * (c * d + a * b), a ^ 2 - b ^ 2 - c ^ 2 + d ^ 2]

/-- At the identity `q = (1, 0, 0, 0)`, the adjoint matrix is the 3x3 identity matrix. -/
theorem su2AdjointMatrix_one : su2AdjointMatrix 1 0 0 0 = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [su2AdjointMatrix, one_apply]

/-- Zero N-ality / Z_2 center blindness: negating `(a, b, c, d) ↦ (-a, -b, -c, -d)` (the
nontrivial center element `-I_2 ∈ SU(2)`) leaves every entry of `su2AdjointMatrix` unchanged. -/
theorem su2AdjointMatrix_center_blind (a b c d : ℝ) :
    su2AdjointMatrix (-a) (-b) (-c) (-d) = su2AdjointMatrix a b c d := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [su2AdjointMatrix]

/-- Quaternion conjugation `(a, b, c, d) ↦ (a, -b, -c, -d)` maps `su2AdjointMatrix` to its transpose. -/
theorem su2AdjointMatrix_conj_eq_transpose (a b c d : ℝ) :
    su2AdjointMatrix a (-b) (-c) (-d) = (su2AdjointMatrix a b c d).transpose := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [su2AdjointMatrix, transpose_apply] <;> ring

/-- For unit parameters `a^2 + b^2 + c^2 + d^2 = 1`, `su2AdjointMatrix` is orthogonal: `R^T R = I_3`. -/
theorem su2AdjointMatrix_transpose_mul_self {a b c d : ℝ}
    (h : a ^ 2 + b ^ 2 + c ^ 2 + d ^ 2 = 1) :
    (su2AdjointMatrix a b c d).transpose * su2AdjointMatrix a b c d = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [su2AdjointMatrix, mul_apply, Fin.sum_univ_three, transpose_apply, one_apply]
  · linear_combination (a ^ 2 + b ^ 2 + c ^ 2 + d ^ 2 + 1) * h
  · ring
  · ring
  · ring
  · linear_combination (a ^ 2 + b ^ 2 + c ^ 2 + d ^ 2 + 1) * h
  · ring
  · ring
  · ring
  · linear_combination (a ^ 2 + b ^ 2 + c ^ 2 + d ^ 2 + 1) * h

/-- For unit parameters `a^2 + b^2 + c^2 + d^2 = 1`, `R R^T = I_3`. -/
theorem su2AdjointMatrix_mul_transpose_self {a b c d : ℝ}
    (h : a ^ 2 + b ^ 2 + c ^ 2 + d ^ 2 = 1) :
    su2AdjointMatrix a b c d * (su2AdjointMatrix a b c d).transpose = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [su2AdjointMatrix, mul_apply, Fin.sum_univ_three, transpose_apply, one_apply]
  · linear_combination (a ^ 2 + b ^ 2 + c ^ 2 + d ^ 2 + 1) * h
  · ring
  · ring
  · ring
  · linear_combination (a ^ 2 + b ^ 2 + c ^ 2 + d ^ 2 + 1) * h
  · ring
  · ring
  · ring
  · linear_combination (a ^ 2 + b ^ 2 + c ^ 2 + d ^ 2 + 1) * h

/-- Exact polynomial identity for the 3x3 adjoint determinant:
`det(su2AdjointMatrix a b c d) = (a^2 + b^2 + c^2 + d^2)^3`. -/
theorem su2AdjointMatrix_det_eq_norm_cube (a b c d : ℝ) :
    (su2AdjointMatrix a b c d).det = (a ^ 2 + b ^ 2 + c ^ 2 + d ^ 2) ^ 3 := by
  simp [su2AdjointMatrix, det_fin_three]
  ring

/-- For unit parameters `a^2 + b^2 + c^2 + d^2 = 1`, `det(su2AdjointMatrix a b c d) = 1`,
so `su2AdjointMatrix a b c d ∈ SO(3)`. -/
theorem su2AdjointMatrix_det_one {a b c d : ℝ}
    (h : a ^ 2 + b ^ 2 + c ^ 2 + d ^ 2 = 1) :
    (su2AdjointMatrix a b c d).det = 1 := by
  rw [su2AdjointMatrix_det_eq_norm_cube, h, one_pow]

/-! ## Part II: Complex Conjugation & General Antiunitary Intertwiner Reality Theorem -/

/-- Entrywise complex conjugation of a complex matrix (`M^*`). -/
def matConj {m n : Type*} (M : Matrix m n ℂ) : Matrix m n ℂ :=
  M.map (starRingEnd ℂ)

/-- Embedding of a real matrix into a complex matrix. -/
def realToComplexMat {m n : Type*} (K : Matrix m n ℝ) : Matrix m n ℂ :=
  K.map Complex.ofReal

@[simp]
lemma matConj_apply {m n : Type*} (M : Matrix m n ℂ) (i : m) (j : n) :
    matConj M i j = star (M i j) := rfl

@[simp]
lemma realToComplexMat_apply {m n : Type*} (K : Matrix m n ℝ) (i : m) (j : n) :
    realToComplexMat K i j = (K i j : ℂ) := rfl

/-- Every real matrix embedded into `ℂ` is fixed by entrywise complex conjugation `matConj`. -/
theorem matConj_realToComplexMat {m n : Type*} (K : Matrix m n ℝ) :
    matConj (realToComplexMat K) = realToComplexMat K := by
  ext i j
  simp [matConj, realToComplexMat]

/-- Every SU(2) adjoint matrix embedded into `ℂ` is fixed by entrywise complex conjugation. -/
theorem matConj_su2AdjointMatrix (a b c d : ℝ) :
    matConj (realToComplexMat (su2AdjointMatrix a b c d)) =
      realToComplexMat (su2AdjointMatrix a b c d) :=
  matConj_realToComplexMat (su2AdjointMatrix a b c d)

/-- The determinant of the entrywise complex conjugate of `D` is the complex conjugate of `D.det`. -/
theorem matConj_det {n : Type*} [Fintype n] [DecidableEq n] (D : Matrix n n ℂ) :
    (matConj D).det = star D.det := by
  simpa [matConj] using (RingHom.map_det (starRingEnd ℂ) D).symm

/-- **Antiunitary Intertwiner Determinant Reality (Conjugation Form)**:
If an invertible complex matrix `C` (`C.det ≠ 0`) intertwines `matConj D` with `D` via
`C * matConj D = D * C`, then `D.det` is fixed by complex conjugation (`star D.det = D.det`). -/
theorem antiunitary_intertwiner_det_conj {n : Type*} [Fintype n] [DecidableEq n]
    (D C : Matrix n n ℂ) (hC : C.det ≠ 0) (h_int : C * matConj D = D * C) :
    star D.det = D.det := by
  have hdet : (C * matConj D).det = (D * C).det := congrArg Matrix.det h_int
  rw [det_mul, det_mul, matConj_det, mul_comm C.det (star D.det)] at hdet
  exact mul_right_cancel₀ hC hdet

/-- **Antiunitary Intertwiner Determinant Reality (Zero Imaginary Part)**:
If `C.det ≠ 0` and `C * matConj D = D * C`, then `(D.det).im = 0`. -/
theorem antiunitary_intertwiner_det_im_zero {n : Type*} [Fintype n] [DecidableEq n]
    (D C : Matrix n n ℂ) (hC : C.det ≠ 0) (h_int : C * matConj D = D * C) :
    (D.det).im = 0 := by
  have hconj := antiunitary_intertwiner_det_conj D C hC h_int
  exact conj_eq_iff_im.mp (by simpa only [star_def] using hconj)

/-- For two degenerate flavors `fromBlocks D 0 0 D` of an antiunitarily intertwined operator `D`,
the two-flavor determinant equals `D.det ^ 2`, has zero imaginary part, and has nonnegative
real part `0 ≤ ((fromBlocks D 0 0 D).det).re`. -/
theorem antiunitary_intertwiner_two_flavor_nonneg {n : Type*} [Fintype n] [DecidableEq n]
    (D C : Matrix n n ℂ) (hC : C.det ≠ 0) (h_int : C * matConj D = D * C) :
    ((fromBlocks D 0 0 D).det).im = 0 ∧ 0 ≤ ((fromBlocks D 0 0 D).det).re := by
  have hconj := antiunitary_intertwiner_det_conj D C hC h_int
  have hre : ((D.det).re : ℂ) = D.det :=
    conj_eq_iff_re.mp (by simpa only [star_def] using hconj)
  have hsq : D.det ^ 2 = (((D.det).re ^ 2 : ℝ) : ℂ) := by
    calc
      D.det ^ 2 = ((D.det).re : ℂ) ^ 2 := by rw [hre]
      _ = (((D.det).re ^ 2 : ℝ) : ℂ) := (ofReal_pow (D.det).re 2).symm
  have hdet2 : (fromBlocks D 0 0 D).det = (((D.det).re ^ 2 : ℝ) : ℂ) := by
    rw [det_fromBlocks_zero₂₁, ← pow_two, hsq]
  rw [hdet2, ofReal_im, ofReal_re]
  exact ⟨rfl, sq_nonneg (D.det).re⟩

/-! ## Part III: 4D Euclidean Charge-Conjugation Intertwiner & Lattice Adjoint Wilson-Dirac Operator -/

/-- Four-component spinor index type in chiral 2+2 block form. -/
abbrev Spin4 := Fin 2 ⊕ Fin 2

def pauli1 : Matrix (Fin 2) (Fin 2) ℂ := !![0, 1; 1, 0]
def pauli2 : Matrix (Fin 2) (Fin 2) ℂ := !![0, -I; I, 0]
def pauli3 : Matrix (Fin 2) (Fin 2) ℂ := !![1, 0; 0, -1]

/-- The 2x2 real symplectic spinor block `ε = i σ_2 = [[0, 1], [-1, 0]]`. -/
def eps2 : Matrix (Fin 2) (Fin 2) ℂ := !![0, 1; -1, 0]

lemma eps2_sq : eps2 * eps2 = -1 := by
  ext i j; fin_cases i <;> fin_cases j <;>
    simp [eps2, mul_apply, Fin.sum_univ_two, one_apply]

lemma eps2_det : eps2.det = 1 := by
  simp [eps2, det_fin_two]

def offDirac (B C : Matrix (Fin 2) (Fin 2) ℂ) : Matrix Spin4 Spin4 ℂ :=
  fromBlocks 0 B C 0

/-- 4D Euclidean gamma matrices in the chiral block basis. -/
def gamma4d : Fin 4 → Matrix Spin4 Spin4 ℂ
  | 0 => offDirac ((-I) • pauli1) (I • pauli1)
  | 1 => offDirac ((-I) • pauli2) (I • pauli2)
  | 2 => offDirac ((-I) • pauli3) (I • pauli3)
  | 3 => offDirac 1 1

/-- 4D chirality matrix `γ_5 = diag(I_2, -I_2)`. -/
def gamma5Four : Matrix Spin4 Spin4 ℂ :=
  fromBlocks 1 0 0 (-1)

/-- The 4D Euclidean charge-conjugation / reality intertwiner `C_4 = diag(ε, ε)`. -/
def chargeConj4 : Matrix Spin4 Spin4 ℂ :=
  fromBlocks eps2 0 0 eps2

/-- Quaternionic / Kramers structure: `chargeConj4 ^ 2 = -I_4`. -/
theorem chargeConj4_sq : chargeConj4 * chargeConj4 = -1 := by
  calc
    chargeConj4 * chargeConj4 = fromBlocks (-1) 0 0 (-1) := by
      simp [chargeConj4, fromBlocks_multiply, eps2_sq]
    _ = fromBlocks (-1) (-0) (-0) (-1) := by simp
    _ = -fromBlocks 1 0 0 1 := (fromBlocks_neg 1 0 0 1).symm
    _ = -1 := by rw [fromBlocks_one]

/-- `det(chargeConj4) = 1`. -/
theorem chargeConj4_det : chargeConj4.det = 1 := by
  simp [chargeConj4, det_fromBlocks_zero₂₁, eps2_det]

lemma eps2_intertwines_neg_I_pauli1 :
    eps2 * matConj ((-I) • pauli1) = ((-I) • pauli1) * eps2 := by
  ext i j; fin_cases i <;> fin_cases j <;>
    simp [eps2, pauli1, matConj, mul_apply, Fin.sum_univ_two]

lemma eps2_intertwines_I_pauli1 :
    eps2 * matConj (I • pauli1) = (I • pauli1) * eps2 := by
  ext i j; fin_cases i <;> fin_cases j <;>
    simp [eps2, pauli1, matConj, mul_apply, Fin.sum_univ_two]

lemma eps2_intertwines_neg_I_pauli2 :
    eps2 * matConj ((-I) • pauli2) = ((-I) • pauli2) * eps2 := by
  ext i j; fin_cases i <;> fin_cases j <;>
    simp [eps2, pauli2, matConj, mul_apply, Fin.sum_univ_two, I_mul_I]

lemma eps2_intertwines_I_pauli2 :
    eps2 * matConj (I • pauli2) = (I • pauli2) * eps2 := by
  ext i j; fin_cases i <;> fin_cases j <;>
    simp [eps2, pauli2, matConj, mul_apply, Fin.sum_univ_two, I_mul_I]

lemma eps2_intertwines_neg_I_pauli3 :
    eps2 * matConj ((-I) • pauli3) = ((-I) • pauli3) * eps2 := by
  ext i j; fin_cases i <;> fin_cases j <;>
    simp [eps2, pauli3, matConj, mul_apply, Fin.sum_univ_two]

lemma eps2_intertwines_I_pauli3 :
    eps2 * matConj (I • pauli3) = (I • pauli3) * eps2 := by
  ext i j; fin_cases i <;> fin_cases j <;>
    simp [eps2, pauli3, matConj, mul_apply, Fin.sum_univ_two]

lemma eps2_intertwines_one :
    eps2 * matConj (1 : Matrix (Fin 2) (Fin 2) ℂ) = (1 : Matrix (Fin 2) (Fin 2) ℂ) * eps2 := by
  ext i j; fin_cases i <;> fin_cases j <;>
    simp [eps2, matConj, mul_apply, one_apply]

lemma matConj_fromBlocks {m n : Type*} (A B C D : Matrix m n ℂ) :
    matConj (fromBlocks A B C D) = fromBlocks (matConj A) (matConj B) (matConj C) (matConj D) := by
  ext i j
  cases i <;> cases j <;> rfl

@[simp]
lemma matConj_zero {m n : Type*} : matConj (0 : Matrix m n ℂ) = 0 := by
  ext i j
  simp [matConj]

@[simp]
lemma matConj_one {n : Type*} [DecidableEq n] : matConj (1 : Matrix n n ℂ) = 1 := by
  ext i j
  by_cases h : i = j <;> simp [matConj, one_apply, h]

@[simp]
lemma matConj_neg {m n : Type*} (M : Matrix m n ℂ) : matConj (-M) = -matConj M := by
  ext i j
  simp [matConj]

/-- `chargeConj4` intertwines complex conjugation on all four 4D Euclidean gamma matrices:
`chargeConj4 * matConj (gamma4d μ) = gamma4d μ * chargeConj4`. -/
theorem chargeConj4_intertwines_gamma4d (μ : Fin 4) :
    chargeConj4 * matConj (gamma4d μ) = gamma4d μ * chargeConj4 := by
  fin_cases μ <;>
    simp only [gamma4d, offDirac, chargeConj4, matConj_fromBlocks, matConj_zero,
      fromBlocks_multiply, mul_zero, zero_mul, add_zero, zero_add]
  · rw [eps2_intertwines_neg_I_pauli1, eps2_intertwines_I_pauli1]
  · rw [eps2_intertwines_neg_I_pauli2, eps2_intertwines_I_pauli2]
  · rw [eps2_intertwines_neg_I_pauli3, eps2_intertwines_I_pauli3]
  · rw [eps2_intertwines_one]

/-- `chargeConj4` also intertwines `gamma5Four`. -/
theorem chargeConj4_intertwines_gamma5Four :
    chargeConj4 * matConj gamma5Four = gamma5Four * chargeConj4 := by
  simp [chargeConj4, gamma5Four, matConj_fromBlocks, fromBlocks_multiply]

/-- Tensor product of a complex spin matrix `S` and a real site-color kernel `K`. -/
def tensorSpinReal {Spin SiteColor : Type*}
    (S : Matrix Spin Spin ℂ) (K : Matrix SiteColor SiteColor ℝ) :
    Matrix (Spin × SiteColor) (Spin × SiteColor) ℂ :=
  fun sx ty => S sx.1 ty.1 * (K sx.2 ty.2 : ℂ)

lemma tensorSpinReal_mul {Spin SiteColor : Type*}
    [Fintype Spin] [Fintype SiteColor]
    (S₁ S₂ : Matrix Spin Spin ℂ) (K₁ K₂ : Matrix SiteColor SiteColor ℝ) :
    tensorSpinReal S₁ K₁ * tensorSpinReal S₂ K₂ = tensorSpinReal (S₁ * S₂) (K₁ * K₂) := by
  ext ⟨s, x⟩ ⟨t, y⟩
  simp only [tensorSpinReal, mul_apply, ofReal_sum, ofReal_mul, Fintype.sum_prod_type]
  rw [Finset.sum_mul]
  refine Finset.sum_congr rfl fun u _ => ?_
  rw [Finset.mul_sum]
  refine Finset.sum_congr rfl fun z _ => ?_
  ring

lemma tensorSpinReal_one {Spin SiteColor : Type*}
    [DecidableEq Spin] [DecidableEq SiteColor] :
    tensorSpinReal (1 : Matrix Spin Spin ℂ) (1 : Matrix SiteColor SiteColor ℝ) = 1 := by
  ext ⟨s, x⟩ ⟨t, y⟩
  by_cases hs : s = t <;> by_cases hx : x = y <;>
    simp [tensorSpinReal, one_apply, Prod.ext_iff, hs, hx]

lemma tensorSpinReal_neg_left {Spin SiteColor : Type*}
    (S : Matrix Spin Spin ℂ) (K : Matrix SiteColor SiteColor ℝ) :
    tensorSpinReal (-S) K = -tensorSpinReal S K := by
  ext sx ty
  simp [tensorSpinReal]

lemma matConj_tensorSpinReal {Spin SiteColor : Type*}
    (S : Matrix Spin Spin ℂ) (K : Matrix SiteColor SiteColor ℝ) :
    matConj (tensorSpinReal S K) = tensorSpinReal (matConj S) K := by
  ext sx ty
  simp [matConj, tensorSpinReal]

/-- The full lattice antiunitary intertwiner `C_full = C_4 ⊗ I_{SiteColor}`. -/
def fullIntertwiner4 (SiteColor : Type*) [DecidableEq SiteColor] :
    Matrix (Spin4 × SiteColor) (Spin4 × SiteColor) ℂ :=
  tensorSpinReal chargeConj4 (1 : Matrix SiteColor SiteColor ℝ)

/-- `fullIntertwiner4` satisfies the Kramers identity `C_full ^ 2 = -1` on `Spin4 × SiteColor`. -/
theorem fullIntertwiner4_sq (SiteColor : Type*) [Fintype SiteColor] [DecidableEq SiteColor] :
    fullIntertwiner4 SiteColor * fullIntertwiner4 SiteColor = -1 := by
  unfold fullIntertwiner4
  rw [tensorSpinReal_mul, chargeConj4_sq, mul_one, tensorSpinReal_neg_left, tensorSpinReal_one]

/-- Because `fullIntertwiner4 ^ 2 = -1`, its determinant is nonzero for every finite `SiteColor`. -/
theorem fullIntertwiner4_det_ne_zero (SiteColor : Type*) [Fintype SiteColor] [DecidableEq SiteColor] :
    (fullIntertwiner4 SiteColor).det ≠ 0 := by
  intro hzero
  have hsq := congrArg Matrix.det (fullIntertwiner4_sq SiteColor)
  rw [det_mul, hzero, zero_mul] at hsq
  have hneg1 : ((-1 : Matrix (Spin4 × SiteColor) (Spin4 × SiteColor) ℂ) * (-1)).det = (1 : ℂ) := by
    simp
  rw [det_mul, ← hsq, zero_mul] at hneg1
  exact zero_ne_one hneg1

lemma fullIntertwiner4_intertwines_channel {SiteColor : Type*}
    [Fintype SiteColor] [DecidableEq SiteColor]
    (S : Matrix Spin4 Spin4 ℂ) (K : Matrix SiteColor SiteColor ℝ)
    (hS : chargeConj4 * matConj S = S * chargeConj4) :
    fullIntertwiner4 SiteColor * matConj (tensorSpinReal S K) =
      tensorSpinReal S K * fullIntertwiner4 SiteColor := by
  unfold fullIntertwiner4
  rw [matConj_tensorSpinReal, tensorSpinReal_mul, tensorSpinReal_mul, hS, one_mul, mul_one]

lemma chargeConj4_intertwines_wilson_proj_pos (r : ℝ) (μ : Fin 4) :
    chargeConj4 * matConj ((r : ℂ) • (1 : Matrix Spin4 Spin4 ℂ) + gamma4d μ) =
      ((r : ℂ) • (1 : Matrix Spin4 Spin4 ℂ) + gamma4d μ) * chargeConj4 := by
  have hmap : matConj ((r : ℂ) • (1 : Matrix Spin4 Spin4 ℂ) + gamma4d μ) =
      (r : ℂ) • (1 : Matrix Spin4 Spin4 ℂ) + matConj (gamma4d μ) := by
    ext i j
    by_cases hij : i = j <;> simp [matConj, one_apply, hij]
  rw [hmap, mul_add, add_mul, chargeConj4_intertwines_gamma4d]
  simp

lemma chargeConj4_intertwines_wilson_proj_neg (r : ℝ) (μ : Fin 4) :
    chargeConj4 * matConj ((r : ℂ) • (1 : Matrix Spin4 Spin4 ℂ) - gamma4d μ) =
      ((r : ℂ) • (1 : Matrix Spin4 Spin4 ℂ) - gamma4d μ) * chargeConj4 := by
  have hmap : matConj ((r : ℂ) • (1 : Matrix Spin4 Spin4 ℂ) - gamma4d μ) =
      (r : ℂ) • (1 : Matrix Spin4 Spin4 ℂ) - matConj (gamma4d μ) := by
    ext i j
    by_cases hij : i = j <;> simp [matConj, one_apply, hij]
  rw [hmap, mul_sub, sub_mul, chargeConj4_intertwines_gamma4d]
  simp

/-- The 4D lattice Wilson-Dirac operator coupled to any real adjoint gauge link kernels
`Upos, Uneg : Fin 4 → Matrix (Site × Fin 3) (Site × Fin 3) ℝ`, real mass term `m0`,
and real Wilson parameter `r`:
`D_adj = I_4 ⊗ (m0 I) - (1/2) Σ_{μ=0}^3 [ (r I - γ_μ) ⊗ U^+_μ + (r I + γ_μ) ⊗ U^-_μ ]`. -/
def wilsonDiracAdjoint4 {Site : Type*} [Fintype Site] [DecidableEq Site]
    (m0 r : ℝ) (Upos Uneg : Fin 4 → Matrix (Site × Fin 3) (Site × Fin 3) ℝ) :
    Matrix (Spin4 × (Site × Fin 3)) (Spin4 × (Site × Fin 3)) ℂ :=
  tensorSpinReal 1 (m0 • 1) -
    (1 / 2 : ℂ) • ∑ μ : Fin 4,
      (tensorSpinReal ((r : ℂ) • 1 - gamma4d μ) (Upos μ) +
       tensorSpinReal ((r : ℂ) • 1 + gamma4d μ) (Uneg μ))

lemma matConj_add {m n : Type*} (A B : Matrix m n ℂ) :
    matConj (A + B) = matConj A + matConj B := by
  ext i j; simp [matConj]

lemma matConj_sub {m n : Type*} (A B : Matrix m n ℂ) :
    matConj (A - B) = matConj A - matConj B := by
  ext i j; simp [matConj]

lemma matConj_sum {m n ι : Type*} (s : Finset ι) (f : ι → Matrix m n ℂ) :
    matConj (∑ k ∈ s, f k) = ∑ k ∈ s, matConj (f k) := by
  ext i j
  simp [matConj, Matrix.sum_apply]

lemma matConj_half_smul {m n : Type*} (A : Matrix m n ℂ) :
    matConj ((1 / 2 : ℂ) • A) = (1 / 2 : ℂ) • matConj A := by
  ext i j
  change star (((1 / 2 : ℂ) • A) i j) = ((1 / 2 : ℂ) • matConj A) i j
  simp

/-- **4D Lattice Adjoint Wilson-Dirac Antiunitary Intertwining Theorem**:
For every finite site set `Site`, real mass `m0`, Wilson parameter `r`, and real adjoint
hopping kernels `Upos, Uneg`, `fullIntertwiner4` intertwines `matConj D_adj` with `D_adj`. -/
theorem wilsonDiracAdjoint4_intertwined {Site : Type*} [Fintype Site] [DecidableEq Site]
    (m0 r : ℝ) (Upos Uneg : Fin 4 → Matrix (Site × Fin 3) (Site × Fin 3) ℝ) :
    fullIntertwiner4 (Site × Fin 3) * matConj (wilsonDiracAdjoint4 m0 r Upos Uneg) =
      wilsonDiracAdjoint4 m0 r Upos Uneg * fullIntertwiner4 (Site × Fin 3) := by
  unfold wilsonDiracAdjoint4
  rw [matConj_sub, matConj_half_smul, matConj_sum, mul_sub, sub_mul,
    Matrix.mul_smul, Matrix.smul_mul, Finset.mul_sum, Finset.sum_mul]
  congr 1
  · apply fullIntertwiner4_intertwines_channel
    rw [matConj_one, mul_one, one_mul]
  · congr 1
    refine Finset.sum_congr rfl fun μ _ => ?_
    rw [matConj_add, mul_add, add_mul]
    rw [fullIntertwiner4_intertwines_channel _ _ (chargeConj4_intertwines_wilson_proj_neg r μ)]
    rw [fullIntertwiner4_intertwines_channel _ _ (chargeConj4_intertwines_wilson_proj_pos r μ)]

/-- **4D Lattice Adjoint Wilson-Dirac Determinant Reality (Conjugation Form)**:
`star (det D_adj) = det D_adj` for every gauge configuration of real adjoint links. -/
theorem wilsonDiracAdjoint4_det_conj {Site : Type*} [Fintype Site] [DecidableEq Site]
    (m0 r : ℝ) (Upos Uneg : Fin 4 → Matrix (Site × Fin 3) (Site × Fin 3) ℝ) :
    star (wilsonDiracAdjoint4 m0 r Upos Uneg).det =
      (wilsonDiracAdjoint4 m0 r Upos Uneg).det :=
  antiunitary_intertwiner_det_conj
    (wilsonDiracAdjoint4 m0 r Upos Uneg)
    (fullIntertwiner4 (Site × Fin 3))
    (fullIntertwiner4_det_ne_zero (Site × Fin 3))
    (wilsonDiracAdjoint4_intertwined m0 r Upos Uneg)

/-- **4D Lattice Adjoint Wilson-Dirac Determinant Reality (Zero Imaginary Part)**:
`((wilsonDiracAdjoint4 m0 r Upos Uneg).det).im = 0` for every gauge configuration of real
adjoint links. -/
theorem wilsonDiracAdjoint4_det_im_zero {Site : Type*} [Fintype Site] [DecidableEq Site]
    (m0 r : ℝ) (Upos Uneg : Fin 4 → Matrix (Site × Fin 3) (Site × Fin 3) ℝ) :
    ((wilsonDiracAdjoint4 m0 r Upos Uneg).det).im = 0 :=
  antiunitary_intertwiner_det_im_zero
    (wilsonDiracAdjoint4 m0 r Upos Uneg)
    (fullIntertwiner4 (Site × Fin 3))
    (fullIntertwiner4_det_ne_zero (Site × Fin 3))
    (wilsonDiracAdjoint4_intertwined m0 r Upos Uneg)

/-! ## Part IV: Reality Is Not Positivity & Majorana Pfaffian Sign-Flip Witnesses -/

/-- Witness that antiunitary reality of `det D` does NOT imply positivity:
on `Fin 3` (the 3-dimensional adjoint color space), `D = -1` intertwined by `C = 1`
satisfies `C * matConj D = D * C` and `(D.det).im = 0`, yet `(D.det).re = -1 < 0`. -/
theorem reality_not_positivity_witness :
    ∃ D C : Matrix (Fin 3) (Fin 3) ℂ,
      C.det ≠ 0 ∧
      C * matConj D = D * C ∧
      (D.det).im = 0 ∧
      (D.det).re < 0 := by
  refine ⟨(-1 : Matrix (Fin 3) (Fin 3) ℂ), (1 : Matrix (Fin 3) (Fin 3) ℂ), ?_, ?_, ?_, ?_⟩
  · simp
  · simp [matConj_neg, matConj_one]
  · simp [det_fin_three]
  · simp [det_fin_three]

/-- General 2x2 skew-symmetric Majorana matrix `[[0, p], [-p, 0]]`. -/
def skew2 {R : Type*} [CommRing R] (p : R) : Matrix (Fin 2) (Fin 2) R :=
  !![0, p; -p, 0]

/-- Pfaffian of a 2x2 skew-symmetric matrix: `Pf(A) = A_{0,1}`. -/
def pfaffian2 {R : Type*} (A : Matrix (Fin 2) (Fin 2) R) : R :=
  A 0 1

theorem skew2_transpose {R : Type*} [CommRing R] (p : R) :
    (skew2 p).transpose = -skew2 p := by
  ext i j; fin_cases i <;> fin_cases j <;> simp [skew2]

/-- 2x2 Pfaffian square identity: `det(skew2 p) = (pfaffian2 (skew2 p))^2`. -/
theorem skew2_det_eq_pfaffian2_sq {R : Type*} [CommRing R] (p : R) :
    (skew2 p).det = (pfaffian2 (skew2 p)) ^ 2 := by
  simp [skew2, pfaffian2, det_fin_two]
  ring

/-- Two 2x2 Majorana configurations `skew2 1` and `skew2 (-1)` have the same positive
determinant `det = 1`, while their Pfaffians have opposite signs (`+1` vs `-1`). -/
theorem majorana_pfaffian2_sign_flip :
    pfaffian2 (skew2 (1 : ℝ)) = 1 ∧
    pfaffian2 (skew2 (-1 : ℝ)) = -1 ∧
    (skew2 (1 : ℝ)).det = (skew2 (-1 : ℝ)).det ∧
    (skew2 (1 : ℝ)).det = 1 := by
  refine ⟨rfl, rfl, ?_, ?_⟩
  · simp [skew2, det_fin_two]
  · simp [skew2, det_fin_two]

/-- General 4x4 skew-symmetric Majorana matrix parameterized by its 6 upper-triangular entries. -/
def skew4 {R : Type*} [CommRing R] (a b c d e f : R) : Matrix (Fin 4) (Fin 4) R :=
  !![0, a, b, c;
     -a, 0, d, e;
     -b, -d, 0, f;
     -c, -e, -f, 0]

/-- Pfaffian of a 4x4 skew-symmetric matrix:
`Pf(M) = M_{0,1} M_{2,3} - M_{0,2} M_{1,3} + M_{0,3} M_{1,2}`. -/
def pfaffian4 {R : Type*} [CommRing R] (M : Matrix (Fin 4) (Fin 4) R) : R :=
  M 0 1 * M 2 3 - M 0 2 * M 1 3 + M 0 3 * M 1 2

theorem skew4_transpose {R : Type*} [CommRing R] (a b c d e f : R) :
    (skew4 a b c d e f).transpose = -skew4 a b c d e f := by
  ext i j; fin_cases i <;> fin_cases j <;> simp [skew4]

/-- **Exact 4x4 Cayley Pfaffian Identity**:
For every 4x4 skew-symmetric matrix `M = skew4 a b c d e f` over any commutative ring `R`,
`det M = (Pf M)^2 = (a f - b e + c d)^2`. -/
theorem skew4_det_eq_pfaffian4_sq {R : Type*} [CommRing R] (a b c d e f : R) :
    (skew4 a b c d e f).det = (pfaffian4 (skew4 a b c d e f)) ^ 2 := by
  simp [skew4, pfaffian4, det_succ_row_zero, Fin.sum_univ_four, Fin.sum_univ_three,
    submatrix, Fin.succAbove]
  ring

/-- Explicit 4x4 Majorana Pfaffian sign-flip witness: `skew4 1 0 0 0 0 1` and
`skew4 1 0 0 0 0 (-1)` both have `det = 1 > 0`, while their Pfaffians are `+1` and `-1`. -/
theorem majorana_pfaffian4_sign_flip :
    pfaffian4 (skew4 (1 : ℝ) 0 0 0 0 1) = 1 ∧
    pfaffian4 (skew4 (1 : ℝ) 0 0 0 0 (-1)) = -1 ∧
    (skew4 (1 : ℝ) 0 0 0 0 1).det = (skew4 (1 : ℝ) 0 0 0 0 (-1)).det ∧
    (skew4 (1 : ℝ) 0 0 0 0 1).det = 1 := by
  have h1 : pfaffian4 (skew4 (1 : ℝ) 0 0 0 0 1) = 1 := by
    simp [pfaffian4, skew4]
  have h2 : pfaffian4 (skew4 (1 : ℝ) 0 0 0 0 (-1)) = -1 := by
    simp [pfaffian4, skew4]
  have hd1 : (skew4 (1 : ℝ) 0 0 0 0 1).det = 1 := by
    rw [skew4_det_eq_pfaffian4_sq, h1, one_pow]
  have hd2 : (skew4 (1 : ℝ) 0 0 0 0 (-1)).det = 1 := by
    rw [skew4_det_eq_pfaffian4_sq, h2]
    norm_num
  exact ⟨h1, h2, hd1.trans hd2.symm, hd1⟩

end

end FermionSignSu2AdjointRealDet

#print axioms FermionSignSu2AdjointRealDet.su2AdjointMatrix_center_blind
#print axioms FermionSignSu2AdjointRealDet.su2AdjointMatrix_transpose_mul_self
#print axioms FermionSignSu2AdjointRealDet.su2AdjointMatrix_det_eq_norm_cube
#print axioms FermionSignSu2AdjointRealDet.su2AdjointMatrix_det_one
#print axioms FermionSignSu2AdjointRealDet.antiunitary_intertwiner_det_conj
#print axioms FermionSignSu2AdjointRealDet.antiunitary_intertwiner_det_im_zero
#print axioms FermionSignSu2AdjointRealDet.antiunitary_intertwiner_two_flavor_nonneg
#print axioms FermionSignSu2AdjointRealDet.chargeConj4_intertwines_gamma4d
#print axioms FermionSignSu2AdjointRealDet.wilsonDiracAdjoint4_intertwined
#print axioms FermionSignSu2AdjointRealDet.wilsonDiracAdjoint4_det_conj
#print axioms FermionSignSu2AdjointRealDet.wilsonDiracAdjoint4_det_im_zero
#print axioms FermionSignSu2AdjointRealDet.reality_not_positivity_witness
#print axioms FermionSignSu2AdjointRealDet.skew2_det_eq_pfaffian2_sq
#print axioms FermionSignSu2AdjointRealDet.majorana_pfaffian2_sign_flip
#print axioms FermionSignSu2AdjointRealDet.skew4_det_eq_pfaffian4_sq
#print axioms FermionSignSu2AdjointRealDet.majorana_pfaffian4_sign_flip
