import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Analysis.Complex.Basic
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.LinearAlgebra.Matrix.Block
import Mathlib.LinearAlgebra.Matrix.ConjTranspose
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.LinearCombination
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-!
# FermionSignLatticeWessZuminoSusy (`FSP-LATTICE-WESS-ZUMINO-SUSY` / `TFQ-1204`)

AuthorityEffect: None.

Formalizes the finite-dimensional graded linear-algebraic core and lattice subalgebra obstruction
of **FSP-DERIV-040** (`FSP-LATTICE-WESS-ZUMINO-SUSY`, record `TFQ-1204`):

1. **$\mathbb{Z}_2$-Graded Finite Supercharges & the $\{Q_a, Q_b\} = 2 \delta_{ab} H$ Algebra**:
   On a finite $\mathbb{Z}_2$-graded Hilbert space `nB ⊕ nF` with fermion parity involution
   `Γ_F = diag(I_{nB}, -I_{nF})`:
   - Any odd block supercharge `Q(A) = [[0, 0], [A, 0]]` and its adjoint partner
     `Q†(B) = [[0, B], [0, 0]]` satisfy exact nilpotency `Q(A)^2 = 0` and `Q†(B)^2 = 0`,
     and anticommute with `Γ_F`.
   - The supersymmetric Hamiltonian `H(A, B) = Q(A) Q†(B) + Q†(B) Q(A)` is block-diagonal
     `diag(B * A, A * B)`, commutes with `Γ_F`, and commutes with both `Q(A)` and `Q†(B)`.
   - Over `ℂ` with `B = Aᴴ`, the two Hermitian supercharges
     `Q₁(A) = Q(A) + Q(A)ᴴ` and `Q₂(A) = (-I) • (Q(A) - Q(A)ᴴ)` are self-adjoint and satisfy
     the exact Clifford-SUSY relations
     $$Q_1(A)^2 = H(A, A^\dagger), \qquad Q_2(A)^2 = H(A, A^\dagger), \qquad
       Q_1(A) Q_2(A) + Q_2(A) Q_1(A) = 0.$$

2. **Positive Semidefiniteness, Supertrace Cancellation, & Boson–Fermion Partner Pairing**:
   - For any real matrix `A : Matrix nF nB ℝ` and bosonic vector `v : nB → ℝ`, the bosonic
     expectation value of `H_B = Aᵀ * A` equals the sum of squares `∑ x, ((A.mulVec v) x)^2 ≥ 0`,
     and similarly for `H_F = A * Aᵀ` (`∑ i, ((Aᵀ.mulVec w) i)^2 ≥ 0`).
   - The supertrace `Tr(Γ_F H(A, B)) = Tr(B * A) - Tr(A * B) = 0` vanishes identically.
   - If `vB` is a bosonic eigenstate of `B * A` with eigenvalue `E`, then `A.mulVec vB` is a
     fermionic eigenstate of `A * B` with the same eigenvalue `E` (and is nonzero whenever
     `E ≠ 0` and `vB ≠ 0`), and vice versa for `B.mulVec vF`.

3. **Explicit 2-Site Lattice Wess–Zumino Model & Discrete Leibniz Defect Obstruction**:
   - The explicit 2-site lattice Wess–Zumino block `wz2SiteBlock m w = [[m, -w], [w, m]]` yields
     `H_B = H_F = (m^2 + w^2) • I_2` and `det(wz2SiteBlock m w) = m^2 + w^2`.
   - On a 3-site periodic ring `Fin 3`, the discrete cubic Leibniz integral
     `∑ x : Fin 3, (φ x)^2 * (φ (x + 1) - φ (x - 1))` evaluates to `-2 ≠ 0` at `φ = ![0, 1, 2]`,
     showing why naive finite-difference discretizations of nonlinear superpotentials break the
     continuum Leibniz rule and keep at most the nilpotent subalgebra `Q(A)^2 = 0` exact.
-/

namespace FermionSignLatticeWessZuminoSusy

open Matrix Complex
open scoped BigOperators

noncomputable section

/-! ## Part I: $\mathbb{Z}_2$-Graded Supercharges & the $\{Q_a, Q_b\} = 2 \delta_{ab} H$ Algebra -/

/-- Fermion parity involution `Γ_F = diag(I_{nB}, -I_{nF})` on the graded space `nB ⊕ nF`. -/
def fermionParity (nB nF R : Type*) [DecidableEq nB] [DecidableEq nF] [CommRing R] :
    Matrix (nB ⊕ nF) (nB ⊕ nF) R :=
  fromBlocks 1 0 0 (-1)

theorem fermionParity_sq {nB nF R : Type*}
    [Fintype nB] [DecidableEq nB] [Fintype nF] [DecidableEq nF] [CommRing R] :
    fermionParity nB nF R * fermionParity nB nF R = 1 := by
  simp [fermionParity, fromBlocks_multiply, fromBlocks_one]

/-- Nilpotent forward supercharge `Q(A) = [[0, 0], [A, 0]]` mapping bosons (`nB`) to fermions (`nF`). -/
def supercharge {nB nF R : Type*} [Zero R] (A : Matrix nF nB R) :
    Matrix (nB ⊕ nF) (nB ⊕ nF) R :=
  fromBlocks 0 0 A 0

/-- Nilpotent backward/adjoint supercharge `Q†(B) = [[0, B], [0, 0]]` mapping fermions (`nF`) to bosons (`nB`). -/
def superchargeAdj {nB nF R : Type*} [Zero R] (B : Matrix nB nF R) :
    Matrix (nB ⊕ nF) (nB ⊕ nF) R :=
  fromBlocks 0 B 0 0

/-- Exact nilpotency of the forward supercharge: `Q(A)^2 = 0`. -/
theorem supercharge_sq_zero {nB nF R : Type*}
    [Fintype nB] [Fintype nF] [CommRing R] (A : Matrix nF nB R) :
    supercharge A * supercharge A = 0 := by
  simp [supercharge, fromBlocks_multiply, fromBlocks_zero]

/-- Exact nilpotency of the backward supercharge: `Q†(B)^2 = 0`. -/
theorem superchargeAdj_sq_zero {nB nF R : Type*}
    [Fintype nB] [Fintype nF] [CommRing R] (B : Matrix nB nF R) :
    superchargeAdj B * superchargeAdj B = 0 := by
  simp [superchargeAdj, fromBlocks_multiply, fromBlocks_zero]

/-- `Q(A)` is odd under fermion parity: `Γ_F * Q(A) + Q(A) * Γ_F = 0`. -/
theorem supercharge_anticommutes_parity {nB nF R : Type*}
    [Fintype nB] [DecidableEq nB] [Fintype nF] [DecidableEq nF] [CommRing R]
    (A : Matrix nF nB R) :
    fermionParity nB nF R * supercharge A + supercharge A * fermionParity nB nF R = 0 := by
  simp [fermionParity, supercharge, fromBlocks_multiply, fromBlocks_add, fromBlocks_zero]

/-- `Q†(B)` is odd under fermion parity: `Γ_F * Q†(B) + Q†(B) * Γ_F = 0`. -/
theorem superchargeAdj_anticommutes_parity {nB nF R : Type*}
    [Fintype nB] [DecidableEq nB] [Fintype nF] [DecidableEq nF] [CommRing R]
    (B : Matrix nB nF R) :
    fermionParity nB nF R * superchargeAdj B + superchargeAdj B * fermionParity nB nF R = 0 := by
  simp [fermionParity, superchargeAdj, fromBlocks_multiply, fromBlocks_add, fromBlocks_zero]

/-- Supersymmetric Hamiltonian `H(A, B) = {Q(A), Q†(B)} = Q(A) Q†(B) + Q†(B) Q(A)`. -/
def susyHamiltonian {nB nF R : Type*}
    [Fintype nB] [Fintype nF] [CommRing R]
    (A : Matrix nF nB R) (B : Matrix nB nF R) : Matrix (nB ⊕ nF) (nB ⊕ nF) R :=
  supercharge A * superchargeAdj B + superchargeAdj B * supercharge A

/-- Exact block diagonalization of `susyHamiltonian`: `H(A, B) = diag(B * A, A * B)`. -/
theorem susyHamiltonian_eq_fromBlocks {nB nF R : Type*}
    [Fintype nB] [Fintype nF] [CommRing R]
    (A : Matrix nF nB R) (B : Matrix nB nF R) :
    susyHamiltonian A B = fromBlocks (B * A) 0 0 (A * B) := by
  simp [susyHamiltonian, supercharge, superchargeAdj, fromBlocks_multiply, fromBlocks_add]

/-- `H(A, B)` commutes with fermion parity `Γ_F`. -/
theorem susyHamiltonian_commutes_parity {nB nF R : Type*}
    [Fintype nB] [DecidableEq nB] [Fintype nF] [DecidableEq nF] [CommRing R]
    (A : Matrix nF nB R) (B : Matrix nB nF R) :
    fermionParity nB nF R * susyHamiltonian A B = susyHamiltonian A B * fermionParity nB nF R := by
  simp [susyHamiltonian_eq_fromBlocks, fermionParity, fromBlocks_multiply]

/-- Conservation of `Q(A)`: `Q(A) * H(A, B) = H(A, B) * Q(A)`. -/
theorem supercharge_commutes_susyHamiltonian {nB nF R : Type*}
    [Fintype nB] [Fintype nF] [CommRing R]
    (A : Matrix nF nB R) (B : Matrix nB nF R) :
    supercharge A * susyHamiltonian A B = susyHamiltonian A B * supercharge A := by
  simp [susyHamiltonian_eq_fromBlocks, supercharge, fromBlocks_multiply, Matrix.mul_assoc]

/-- Conservation of `Q†(B)`: `Q†(B) * H(A, B) = H(A, B) * Q†(B)`. -/
theorem superchargeAdj_commutes_susyHamiltonian {nB nF R : Type*}
    [Fintype nB] [Fintype nF] [CommRing R]
    (A : Matrix nF nB R) (B : Matrix nB nF R) :
    superchargeAdj B * susyHamiltonian A B = susyHamiltonian A B * superchargeAdj B := by
  simp [susyHamiltonian_eq_fromBlocks, superchargeAdj, fromBlocks_multiply, Matrix.mul_assoc]

/-- Over `ℂ`, `(supercharge A)ᴴ = superchargeAdj Aᴴ`. -/
theorem supercharge_conjTranspose {nB nF : Type*} (A : Matrix nF nB ℂ) :
    (supercharge A)ᴴ = superchargeAdj Aᴴ := by
  simp [supercharge, superchargeAdj, fromBlocks_conjTranspose]

/-- First Hermitian supercharge `Q₁(A) = Q(A) + Q(A)ᴴ`. -/
def hermSupercharge1 {nB nF : Type*} (A : Matrix nF nB ℂ) : Matrix (nB ⊕ nF) (nB ⊕ nF) ℂ :=
  supercharge A + (supercharge A)ᴴ

/-- Second Hermitian supercharge `Q₂(A) = (-I) • (Q(A) - Q(A)ᴴ)`. -/
def hermSupercharge2 {nB nF : Type*} (A : Matrix nF nB ℂ) : Matrix (nB ⊕ nF) (nB ⊕ nF) ℂ :=
  (-I) • (supercharge A - (supercharge A)ᴴ)

theorem hermSupercharge1_hermitian {nB nF : Type*} (A : Matrix nF nB ℂ) :
    (hermSupercharge1 A)ᴴ = hermSupercharge1 A := by
  simp [hermSupercharge1, conjTranspose_add, conjTranspose_conjTranspose, add_comm]

theorem hermSupercharge2_hermitian {nB nF : Type*} (A : Matrix nF nB ℂ) :
    (hermSupercharge2 A)ᴴ = hermSupercharge2 A := by
  simp [hermSupercharge2, conjTranspose_smul, conjTranspose_conjTranspose, sub_eq_add_neg, add_comm]

/-- `Q₁(A)^2 = H(A, Aᴴ)` (i.e. `{Q₁, Q₁} = 2 H`). -/
theorem hermSupercharge1_sq {nB nF : Type*} [Fintype nB] [Fintype nF]
    (A : Matrix nF nB ℂ) :
    hermSupercharge1 A * hermSupercharge1 A = susyHamiltonian A Aᴴ := by
  rw [hermSupercharge1, supercharge_conjTranspose, susyHamiltonian_eq_fromBlocks]
  simp [supercharge, superchargeAdj, fromBlocks_add, fromBlocks_multiply]

/-- `Q₂(A)^2 = H(A, Aᴴ)` (i.e. `{Q₂, Q₂} = 2 H`). -/
theorem hermSupercharge2_sq {nB nF : Type*} [Fintype nB] [Fintype nF]
    (A : Matrix nF nB ℂ) :
    hermSupercharge2 A * hermSupercharge2 A = susyHamiltonian A Aᴴ := by
  rw [hermSupercharge2, supercharge_conjTranspose, susyHamiltonian_eq_fromBlocks]
  simp [supercharge, superchargeAdj, sub_eq_add_neg, fromBlocks_neg, fromBlocks_add,
    fromBlocks_smul, fromBlocks_multiply, Matrix.smul_mul, Matrix.mul_smul, smul_smul, I_mul_I]

/-- Mutual anticommutation of the two Hermitian supercharges: `Q₁(A) Q₂(A) + Q₂(A) Q₁(A) = 0`. -/
theorem hermSupercharge_anticomm {nB nF : Type*} [Fintype nB] [Fintype nF]
    (A : Matrix nF nB ℂ) :
    hermSupercharge1 A * hermSupercharge2 A + hermSupercharge2 A * hermSupercharge1 A = 0 := by
  rw [hermSupercharge1, hermSupercharge2, supercharge_conjTranspose]
  simp [supercharge, superchargeAdj, sub_eq_add_neg, fromBlocks_neg, fromBlocks_add,
    fromBlocks_smul, fromBlocks_multiply, fromBlocks_zero]

/-! ## Part II: Positive Semidefiniteness, Supertrace Cancellation, & Boson–Fermion Pairing -/

/-- For any real operator block `A : Matrix nF nB ℝ` and bosonic vector `v : nB → ℝ`,
the quadratic form `∑ i, v i * ((Aᵀ * A).mulVec v) i` equals the sum of squares
`∑ x, ((A.mulVec v) x)^2`. -/
theorem bosonBlock_quadForm_eq_sum_sq {nB nF : Type*} [Fintype nB] [Fintype nF]
    (A : Matrix nF nB ℝ) (v : nB → ℝ) :
    (∑ i : nB, v i * ((Aᵀ * A).mulVec v) i) = ∑ x : nF, ((A.mulVec v) x) ^ 2 := by
  calc
    (∑ i : nB, v i * ((Aᵀ * A).mulVec v) i)
        = ∑ i : nB, v i * (Aᵀ.mulVec (A.mulVec v)) i := by
          simp only [mulVec_mulVec]
    _ = ∑ i : nB, ∑ x : nF, v i * (A x i * (A.mulVec v) x) := by
          refine Finset.sum_congr rfl (fun i _ => ?_)
          simp only [mulVec, dotProduct, transpose_apply, Finset.mul_sum]
    _ = ∑ x : nF, ∑ i : nB, (A x i * v i) * (A.mulVec v) x := by
          rw [Finset.sum_comm]
          refine Finset.sum_congr rfl (fun x _ => Finset.sum_congr rfl (fun i _ => by ring))
    _ = ∑ x : nF, ((A.mulVec v) x) ^ 2 := by
          refine Finset.sum_congr rfl (fun x _ => ?_)
          rw [← Finset.sum_mul, sq]
          rfl

/-- Nonnegativity of the bosonic Hamiltonian quadratic form `⟨v, (Aᵀ * A) v⟩ ≥ 0`. -/
theorem bosonBlock_quadForm_nonneg {nB nF : Type*} [Fintype nB] [Fintype nF]
    (A : Matrix nF nB ℝ) (v : nB → ℝ) :
    0 ≤ ∑ i : nB, v i * ((Aᵀ * A).mulVec v) i := by
  rw [bosonBlock_quadForm_eq_sum_sq]
  exact Finset.sum_nonneg (fun x _ => sq_nonneg ((A.mulVec v) x))

/-- Nonnegativity of the fermionic Hamiltonian quadratic form `⟨w, (A * Aᵀ) w⟩ ≥ 0`. -/
theorem fermionBlock_quadForm_nonneg {nB nF : Type*} [Fintype nB] [Fintype nF]
    (A : Matrix nF nB ℝ) (w : nF → ℝ) :
    0 ≤ ∑ x : nF, w x * ((A * Aᵀ).mulVec w) x := by
  have h := bosonBlock_quadForm_nonneg Aᵀ w
  simpa only [transpose_transpose] using h

/-- Exact trace equality between the bosonic block `B * A` and fermionic block `A * B`. -/
theorem boson_eq_fermion_trace {nB nF R : Type*}
    [Fintype nB] [Fintype nF] [CommRing R]
    (A : Matrix nF nB R) (B : Matrix nB nF R) :
    (B * A).trace = (A * B).trace :=
  trace_mul_comm B A

/-- Exact vanishing of the supertrace of the supersymmetric Hamiltonian:
`Tr(Γ_F * H(A, B)) = Tr(B * A) - Tr(A * B) = 0`. -/
theorem supertrace_susyHamiltonian_eq_zero {nB nF R : Type*}
    [Fintype nB] [DecidableEq nB] [Fintype nF] [DecidableEq nF] [CommRing R]
    (A : Matrix nF nB R) (B : Matrix nB nF R) :
    (fermionParity nB nF R * susyHamiltonian A B).trace = 0 := by
  have hprod : fermionParity nB nF R * susyHamiltonian A B =
      fromBlocks (B * A) 0 0 (-(A * B)) := by
    simp [susyHamiltonian_eq_fromBlocks, fermionParity, fromBlocks_multiply]
  rw [hprod]
  have htr : (fromBlocks (B * A) 0 0 (-(A * B))).trace = (B * A).trace - (A * B).trace := by
    simp [Matrix.trace, Fintype.sum_sum_type, sub_eq_add_neg]
  rw [htr, trace_mul_comm B A, sub_self]

/-- **Boson-to-Fermion Partner Eigenstate Map**:
If `vB` is an eigenvector of the bosonic block `B * A` with eigenvalue `E`, then `A.mulVec vB`
is an eigenvector of the fermionic block `A * B` with the same eigenvalue `E`. -/
theorem boson_to_fermion_eigenstate {nB nF R : Type*}
    [Fintype nB] [Fintype nF] [CommRing R]
    (A : Matrix nF nB R) (B : Matrix nB nF R) (E : R) (vB : nB → R)
    (h_eig : (B * A).mulVec vB = E • vB) :
    (A * B).mulVec (A.mulVec vB) = E • (A.mulVec vB) := by
  calc
    (A * B).mulVec (A.mulVec vB) = (A * B * A).mulVec vB := mulVec_mulVec vB (A * B) A
    _ = (A * (B * A)).mulVec vB := by rw [Matrix.mul_assoc]
    _ = A.mulVec ((B * A).mulVec vB) := (mulVec_mulVec vB A (B * A)).symm
    _ = E • (A.mulVec vB) := by rw [h_eig, mulVec_smul]

/-- **Fermion-to-Boson Partner Eigenstate Map**:
If `vF` is an eigenvector of the fermionic block `A * B` with eigenvalue `E`, then `B.mulVec vF`
is an eigenvector of the bosonic block `B * A` with the same eigenvalue `E`. -/
theorem fermion_to_boson_eigenstate {nB nF R : Type*}
    [Fintype nB] [Fintype nF] [CommRing R]
    (A : Matrix nF nB R) (B : Matrix nB nF R) (E : R) (vF : nF → R)
    (h_eig : (A * B).mulVec vF = E • vF) :
    (B * A).mulVec (B.mulVec vF) = E • (B.mulVec vF) := by
  calc
    (B * A).mulVec (B.mulVec vF) = (B * A * B).mulVec vF := mulVec_mulVec vF (B * A) B
    _ = (B * (A * B)).mulVec vF := by rw [Matrix.mul_assoc]
    _ = B.mulVec ((A * B).mulVec vF) := (mulVec_mulVec vF B (A * B)).symm
    _ = E • (B.mulVec vF) := by rw [h_eig, mulVec_smul]

/-- **Nonzero-Energy Partner Non-Vanishing**:
Over a field `K`, if `(B * A).mulVec vB = E • vB` with `E ≠ 0` and `vB ≠ 0`, then the fermionic
partner state `A.mulVec vB` is nonzero. -/
theorem boson_partner_ne_zero {nB nF K : Type*}
    [Fintype nB] [Fintype nF] [Field K]
    (A : Matrix nF nB K) (B : Matrix nB nF K) (E : K) (vB : nB → K)
    (h_eig : (B * A).mulVec vB = E • vB) (hE : E ≠ 0) (hvB : vB ≠ 0) :
    A.mulVec vB ≠ 0 := by
  intro hA0
  have h0 : E • vB = 0 := by
    calc
      E • vB = (B * A).mulVec vB := h_eig.symm
      _ = B.mulVec (A.mulVec vB) := by rw [mulVec_mulVec]
      _ = B.mulVec 0 := by rw [hA0]
      _ = 0 := mulVec_zero B
  exact smul_ne_zero hE hvB h0

/-! ## Part III: Explicit 2-Site Lattice Wess–Zumino Model & Discrete Leibniz Defect -/

/-- Explicit 2-site lattice Wess–Zumino Nicolai/superpotential gradient block
`A_WZ(m, w) = [[m, -w], [w, m]]` on `Fin 2`. -/
def wz2SiteBlock (m w : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![m, -w;
     w,  m]

/-- Both the bosonic Hamiltonian `A_WZᵀ * A_WZ` and fermionic Hamiltonian `A_WZ * A_WZᵀ`
equal `(m^2 + w^2) • I_2`, exhibiting exact boson-fermion mass degeneracy. -/
theorem wz2SiteBlock_boson_eq_fermion (m w : ℝ) :
    (wz2SiteBlock m w)ᵀ * wz2SiteBlock m w = (m ^ 2 + w ^ 2) • (1 : Matrix (Fin 2) (Fin 2) ℝ) ∧
    wz2SiteBlock m w * (wz2SiteBlock m w)ᵀ = (m ^ 2 + w ^ 2) • (1 : Matrix (Fin 2) (Fin 2) ℝ) := by
  constructor
  · ext i j; fin_cases i <;> fin_cases j <;>
      simp [wz2SiteBlock, mul_apply, Fin.sum_univ_two, transpose_apply, Matrix.smul_apply, one_apply] <;>
      ring
  · ext i j; fin_cases i <;> fin_cases j <;>
      simp [wz2SiteBlock, mul_apply, Fin.sum_univ_two, transpose_apply, Matrix.smul_apply, one_apply] <;>
      ring

/-- The determinant of `wz2SiteBlock m w` is `m^2 + w^2 ≥ 0`. -/
theorem wz2SiteBlock_det (m w : ℝ) :
    (wz2SiteBlock m w).det = m ^ 2 + w ^ 2 ∧ 0 ≤ (wz2SiteBlock m w).det := by
  have hdet : (wz2SiteBlock m w).det = m ^ 2 + w ^ 2 := by
    simp [wz2SiteBlock, det_fin_two]
    ring
  exact ⟨hdet, hdet.symm ▸ add_nonneg (sq_nonneg m) (sq_nonneg w)⟩

/-- Symmetric lattice difference `(D φ)_x = φ (x + 1) - φ (x - 1)` on the 3-site ring `Fin 3`,
and the discrete cubic Leibniz integral `∑ x : Fin 3, (φ x)^2 * (φ (x + 1) - φ (x - 1))`. -/
def leibnizCubicDefect3 (φ : Fin 3 → ℝ) : ℝ :=
  ∑ x : Fin 3, (φ x) ^ 2 * (φ (x + 1) - φ (x - 1))

/-- **Discrete Cubic Leibniz Defect Witness**:
Unlike the continuum integral `∮ φ(x)^2 ∂_x φ(x) dx = 0`, the discrete lattice sum on `Fin 3`
for `φ = ![0, 1, 2]` equals `-2 ≠ 0`, obstructing full continuum SUSY closure on the lattice. -/
theorem leibnizCubicDefect3_witness :
    leibnizCubicDefect3 ![0, 1, 2] = -2 ∧ leibnizCubicDefect3 ![0, 1, 2] ≠ 0 := by
  constructor
  · simp [leibnizCubicDefect3, Fin.sum_univ_three]
    norm_num
  · simp [leibnizCubicDefect3, Fin.sum_univ_three]
    norm_num

/-- Putative lattice operator mixing both off-diagonal blocks `[[0, I_2], [I_2, 0]]`. -/
def brokenSupercharge2 : Matrix (Fin 2 ⊕ Fin 2) (Fin 2 ⊕ Fin 2) ℝ :=
  fromBlocks 0 1 1 0

/-- **Broken Supercharge Nilpotency Obstruction**:
Adding a non-zero upper-right block `B = 1` to `Q = [[0, 0], [1, 0]]` produces
`brokenSupercharge2 = [[0, 1], [1, 0]]` whose square is `1 ≠ 0`, illustrating that lattice operators
mixing both off-diagonal grading sectors fail `Q^2 = 0` unless `B * A = 0` and `A * B = 0`. -/
theorem brokenSupercharge_sq_ne_zero :
    brokenSupercharge2 * brokenSupercharge2 = 1 ∧
    brokenSupercharge2 * brokenSupercharge2 ≠ 0 := by
  have hsq : brokenSupercharge2 * brokenSupercharge2 = 1 := by
    simp [brokenSupercharge2, fromBlocks_multiply, fromBlocks_one]
  refine ⟨hsq, ?_⟩
  rw [hsq]
  intro h10
  have h00 := congrArg (fun M => M (Sum.inl 0) (Sum.inl 0)) h10
  simp at h00

end

end FermionSignLatticeWessZuminoSusy

#print axioms FermionSignLatticeWessZuminoSusy.fermionParity_sq
#print axioms FermionSignLatticeWessZuminoSusy.supercharge_sq_zero
#print axioms FermionSignLatticeWessZuminoSusy.superchargeAdj_sq_zero
#print axioms FermionSignLatticeWessZuminoSusy.supercharge_anticommutes_parity
#print axioms FermionSignLatticeWessZuminoSusy.superchargeAdj_anticommutes_parity
#print axioms FermionSignLatticeWessZuminoSusy.susyHamiltonian_eq_fromBlocks
#print axioms FermionSignLatticeWessZuminoSusy.susyHamiltonian_commutes_parity
#print axioms FermionSignLatticeWessZuminoSusy.supercharge_commutes_susyHamiltonian
#print axioms FermionSignLatticeWessZuminoSusy.superchargeAdj_commutes_susyHamiltonian
#print axioms FermionSignLatticeWessZuminoSusy.hermSupercharge1_hermitian
#print axioms FermionSignLatticeWessZuminoSusy.hermSupercharge2_hermitian
#print axioms FermionSignLatticeWessZuminoSusy.hermSupercharge1_sq
#print axioms FermionSignLatticeWessZuminoSusy.hermSupercharge2_sq
#print axioms FermionSignLatticeWessZuminoSusy.hermSupercharge_anticomm
#print axioms FermionSignLatticeWessZuminoSusy.bosonBlock_quadForm_eq_sum_sq
#print axioms FermionSignLatticeWessZuminoSusy.bosonBlock_quadForm_nonneg
#print axioms FermionSignLatticeWessZuminoSusy.fermionBlock_quadForm_nonneg
#print axioms FermionSignLatticeWessZuminoSusy.boson_eq_fermion_trace
#print axioms FermionSignLatticeWessZuminoSusy.supertrace_susyHamiltonian_eq_zero
#print axioms FermionSignLatticeWessZuminoSusy.boson_to_fermion_eigenstate
#print axioms FermionSignLatticeWessZuminoSusy.fermion_to_boson_eigenstate
#print axioms FermionSignLatticeWessZuminoSusy.boson_partner_ne_zero
#print axioms FermionSignLatticeWessZuminoSusy.wz2SiteBlock_boson_eq_fermion
#print axioms FermionSignLatticeWessZuminoSusy.wz2SiteBlock_det
#print axioms FermionSignLatticeWessZuminoSusy.leibnizCubicDefect3_witness
#print axioms FermionSignLatticeWessZuminoSusy.brokenSupercharge_sq_ne_zero
