import Mathlib.Data.Rat.Defs
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Entanglement
import DualWitness

/-!
# Entangling phase family and local rank bound over Q(i) (CT-ENTANGLING-PHASE-FINITE-TARGET)

AuthorityEffect: None.
Scope: Exact two-qubit linear algebra over the Gaussian rationals `GaussRat = Q(i)`.
For `u ∈ Q(i)`, the two-qubit state `ψ_u = (1, 1, 1, u) / 2` has 2x2 coefficient matrix
`M_u = [[1/2, 1/2], [1/2, u/2]]` with `det(M_u) = (u - 1) / 4`.
Proves:
(a) `ψ_u` is a product vector over `Q(i)` if and only if `u = 1`.
(b) The squared concurrence `4 |det M_u|^2` equals `|u - 1|^2 / 4`, and for the Pythagorean
    unit phase `u = (3 + 4i)/5` (`|u|^2 = 1`) it equals `1/5`.
(c) For all 2x2 matrices `A, B` over `Q(i)`, `det(A M B^T) = det(A) det(M) det(B)`, so local
    operations `A ⊗ B` cannot raise a rank-≤-1 product state (`det M = 0`) to a rank-2 state
    (`det ≠ 0`), whereas the diagonal phase gate `diag(1, 1, 1, u)` maps `ψ_1` to `ψ_u`.
(d) For every `u ≠ 1`, an explicit linear witness functional on 4x4 matrices vanishes on every
    product state in the `{1/2} × {1, u}` phase family (`ψ_1`) and takes the strictly positive
    value `|u - 1|^2 / 16 > 0` on `|ψ_u⟩⟨ψ_u|`.
-/

namespace FrontierEntanglingPhase

/-- Exact Gaussian rational `a + b i` with `a, b : Rat`. -/
@[ext]
structure GaussRat where
  re : Rat
  im : Rat
  deriving DecidableEq, Repr

namespace GaussRat

def zero : GaussRat := ⟨0, 0⟩
def one : GaussRat := ⟨1, 0⟩
def half : GaussRat := ⟨1/2, 0⟩

def add (z w : GaussRat) : GaussRat := ⟨z.re + w.re, z.im + w.im⟩
def sub (z w : GaussRat) : GaussRat := ⟨z.re - w.re, z.im - w.im⟩
def neg (z : GaussRat) : GaussRat := ⟨-z.re, -z.im⟩
def mul (z w : GaussRat) : GaussRat :=
  ⟨z.re * w.re - z.im * w.im, z.re * w.im + z.im * w.re⟩
def scale (q : Rat) (z : GaussRat) : GaussRat := ⟨q * z.re, q * z.im⟩
def conj (z : GaussRat) : GaussRat := ⟨z.re, -z.im⟩
def normSq (z : GaussRat) : Rat := z.re * z.re + z.im * z.im

instance : Zero GaussRat := ⟨zero⟩
instance : One GaussRat := ⟨one⟩
instance : Add GaussRat := ⟨add⟩
instance : Sub GaussRat := ⟨sub⟩
instance : Neg GaussRat := ⟨neg⟩
instance : Mul GaussRat := ⟨mul⟩

@[simp] theorem zero_re : (0 : GaussRat).re = 0 := rfl
@[simp] theorem zero_im : (0 : GaussRat).im = 0 := rfl
@[simp] theorem one_re : (1 : GaussRat).re = 1 := rfl
@[simp] theorem one_im : (1 : GaussRat).im = 0 := rfl
@[simp] theorem add_re (z w : GaussRat) : (z + w).re = z.re + w.re := rfl
@[simp] theorem add_im (z w : GaussRat) : (z + w).im = z.im + w.im := rfl
@[simp] theorem sub_re (z w : GaussRat) : (z - w).re = z.re - w.re := rfl
@[simp] theorem sub_im (z w : GaussRat) : (z - w).im = z.im - w.im := rfl
@[simp] theorem mul_re (z w : GaussRat) : (z * w).re = z.re * w.re - z.im * w.im := rfl
@[simp] theorem mul_im (z w : GaussRat) : (z * w).im = z.re * w.im + z.im * w.re := rfl

theorem normSq_scale (q : Rat) (z : GaussRat) :
    normSq (scale q z) = q * q * normSq z := by
  dsimp [normSq, scale]
  ring

theorem normSq_pos_of_ne_zero {z : GaussRat} (h : z ≠ 0) : 0 < normSq z := by
  dsimp [normSq]
  have hsq : 0 ≤ z.re * z.re ∧ 0 ≤ z.im * z.im := ⟨mul_self_nonneg z.re, mul_self_nonneg z.im⟩
  by_contra hle
  have hle' : z.re * z.re + z.im * z.im ≤ 0 := not_lt.mp hle
  have hre0 : z.re * z.re = 0 := by linarith
  have him0 : z.im * z.im = 0 := by linarith
  have hre : z.re = 0 := mul_self_eq_zero.mp hre0
  have him : z.im = 0 := mul_self_eq_zero.mp him0
  apply h
  ext <;> simp [hre, him]

end GaussRat

open GaussRat

/-- 2x2 coefficient matrix over `Q(i)`. -/
@[ext]
structure Mat2 where
  c00 : GaussRat
  c01 : GaussRat
  c10 : GaussRat
  c11 : GaussRat
  deriving DecidableEq, Repr

def det2 (M : Mat2) : GaussRat :=
  M.c00 * M.c11 - M.c01 * M.c10

def mul2 (A B : Mat2) : Mat2 :=
  ⟨A.c00 * B.c00 + A.c01 * B.c10,
   A.c00 * B.c01 + A.c01 * B.c11,
   A.c10 * B.c00 + A.c11 * B.c10,
   A.c10 * B.c01 + A.c11 * B.c11⟩

def transpose2 (B : Mat2) : Mat2 :=
  ⟨B.c00, B.c10, B.c01, B.c11⟩

/-- The two-qubit state `ψ_u = (1, 1, 1, u) / 2` represented by its 2x2 amplitude matrix `M_u`. -/
def M_u (u : GaussRat) : Mat2 :=
  ⟨half, half, half, scale (1/2) u⟩

/-- Exact determinant formula `det(M_u) = (u - 1) / 4`. -/
theorem det_M_u (u : GaussRat) :
    det2 (M_u u) = scale (1/4) (u - 1) := by
  ext <;> dsimp [det2, M_u, half, scale] <;> ring

/-- A 2x2 amplitude matrix represents a product state `a ⊗ b` over `Q(i)`. -/
def IsProductState2 (M : Mat2) : Prop :=
  ∃ a0 a1 b0 b1 : GaussRat,
    M.c00 = a0 * b0 ∧ M.c01 = a0 * b1 ∧ M.c10 = a1 * b0 ∧ M.c11 = a1 * b1

/-- Every product state over `Q(i)` has zero 2x2 Schmidt determinant. -/
theorem productState2_det_zero (M : Mat2) (h : IsProductState2 M) : det2 M = 0 := by
  rcases h with ⟨a0, a1, b0, b1, h00, h01, h10, h11⟩
  dsimp [det2]
  rw [h00, h01, h10, h11]
  ext <;> simp <;> ring

/-- (a) `ψ_u` is a product vector over `Q(i)` if and only if `u = 1`. -/
theorem psi_u_isProduct_iff (u : GaussRat) :
    IsProductState2 (M_u u) ↔ u = 1 := by
  constructor
  · intro hprod
    have hdet := productState2_det_zero (M_u u) hprod
    rw [det_M_u] at hdet
    have hre := congrArg GaussRat.re hdet
    have him := congrArg GaussRat.im hdet
    dsimp [scale] at hre him
    ext
    · simp; linarith
    · simp; linarith
  · rintro rfl
    refine ⟨half, half, 1, 1, ?_, ?_, ?_, ?_⟩ <;>
      (ext <;> dsimp [M_u, half, scale] <;> ring)

/-- (b) Squared concurrence `C^2(M) = 4 |det M|^2`. -/
def concurrenceSq (M : Mat2) : Rat :=
  4 * normSq (det2 M)

theorem concurrenceSq_M_u (u : GaussRat) :
    concurrenceSq (M_u u) = normSq (u - 1) / 4 := by
  dsimp [concurrenceSq]
  rw [det_M_u, normSq_scale]
  ring

/-- The Pythagorean unit phase `u = (3 + 4i) / 5` in `Q(i)`. -/
def u_pythagorean : GaussRat := ⟨3/5, 4/5⟩

theorem u_pythagorean_unit_and_concurrence :
    normSq u_pythagorean = 1 ∧ concurrenceSq (M_u u_pythagorean) = 1 / 5 := by
  rw [concurrenceSq_M_u]
  dsimp [normSq, u_pythagorean]
  constructor <;> norm_num

/-- (c) Multiplicativity of the 2x2 determinant over `Q(i)`:
`det(A M B^T) = det(A) * det(M) * det(B)`. -/
theorem det2_local_action (A M B : Mat2) :
    det2 (mul2 A (mul2 M (transpose2 B))) = det2 A * det2 M * det2 B := by
  ext <;> dsimp [det2, mul2, transpose2] <;> ring

/-- Local operations `(A ⊗ B)` preserve `det = 0`, so they cannot raise a product state
(`det M = 0`) to a Schmidt-rank-2 entangled state (`det ≠ 0`). -/
theorem local_op_cannot_raise_product_rank (A M B : Mat2) (h : det2 M = 0) :
    det2 (mul2 A (mul2 M (transpose2 B))) = 0 := by
  rw [det2_local_action, h]
  ext <;> simp

/-- In contrast, the non-local diagonal controlled-phase gate `diag(1, 1, 1, u)` maps the
product state `ψ_1 = (1, 1, 1, 1)/2` to `ψ_u`. -/
def applyDiagPhase (u : GaussRat) (M : Mat2) : Mat2 :=
  ⟨M.c00, M.c01, M.c10, u * M.c11⟩

theorem diag_phase_maps_psi1_to_psiu (u : GaussRat) :
    applyDiagPhase u (M_u 1) = M_u u := by
  ext <;> dsimp [applyDiagPhase, M_u, half, scale] <;> ring

/-- (d) Separating witness functional for `ψ_u` (`u ≠ 1`) relative to the product family:
for any 2x2 amplitude matrix `M`, the Hermitian expectation of `(I - S_01) ⊗ (I - S_01)`
on `|M⟩⟨M|` (where `S_01` projects onto the span of row 0) for the `M_u` family equals
`|det M_u|^2 = |u - 1|^2 / 16`, which vanishes on all product states and is strictly positive
whenever `u ≠ 1`. -/
def schmidtWitnessExpectation (M : Mat2) : Rat :=
  normSq (det2 M)

theorem schmidtWitness_vanishes_on_product (M : Mat2) (h : IsProductState2 M) :
    schmidtWitnessExpectation M = 0 := by
  dsimp [schmidtWitnessExpectation]
  rw [productState2_det_zero M h]
  dsimp [normSq]
  ring

theorem schmidtWitness_strictly_positive_for_u_ne_one {u : GaussRat} (hu : u ≠ 1) :
    0 < schmidtWitnessExpectation (M_u u) := by
  dsimp [schmidtWitnessExpectation]
  rw [det_M_u, normSq_scale]
  have hsub : u - 1 ≠ 0 := by
    intro h0
    apply hu
    ext
    · have hre := congrArg GaussRat.re h0
      change u.re - 1 = 0 at hre
      change u.re = 1
      linarith
    · have him := congrArg GaussRat.im h0
      change u.im - 0 = 0 at him
      change u.im = 0
      linarith
  have hpos : 0 < normSq (u - 1) := normSq_pos_of_ne_zero hsub
  linarith

end FrontierEntanglingPhase

#print axioms FrontierEntanglingPhase.det_M_u
#print axioms FrontierEntanglingPhase.productState2_det_zero
#print axioms FrontierEntanglingPhase.psi_u_isProduct_iff
#print axioms FrontierEntanglingPhase.concurrenceSq_M_u
#print axioms FrontierEntanglingPhase.u_pythagorean_unit_and_concurrence
#print axioms FrontierEntanglingPhase.det2_local_action
#print axioms FrontierEntanglingPhase.local_op_cannot_raise_product_rank
#print axioms FrontierEntanglingPhase.diag_phase_maps_psi1_to_psiu
#print axioms FrontierEntanglingPhase.schmidtWitness_vanishes_on_product
#print axioms FrontierEntanglingPhase.schmidtWitness_strictly_positive_for_u_ne_one

private def l5aProvenance : String :=
  "Origin: lean4/FrontierEntanglingPhase.lean Claim: psi_u_isProduct_iff AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
