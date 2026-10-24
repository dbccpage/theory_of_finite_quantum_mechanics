import Mathlib.Data.Matrix.Basic
import Mathlib.Data.ZMod.Basic
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Tactic

/-!
# Campaign: FSP-COBORDISM-INTRINSIC-SIGN (TFQ-1211 / FSP-DERIV-047)

Formalizes the finite algebraic prototypes of spectral asymmetry (`η`-jump), Arf quadratic
refinements, Atiyah-Hirzebruch / Postnikov-Arf-Rokhlin mod-2 cobordism pairings, and the
class-specific representation no-go and scope fences for `FSP-COBORDISM-INTRINSIC-SIGN`
(`TFQ-1211`, `GIN-C22`):

1. **Discrete Spectral Asymmetry and Level-Crossing `Δη = ±2` Jump**:
   - `spectralSign` is odd (`spectralSign (-λ) = -spectralSign λ`), vanishes on paired
     particle-hole symmetric spectra `(λ, -λ)`, and jumps by `+2` (`Δ(η/2) = 1`) when a
     single mode crosses zero from `-λ < 0` to `+λ > 0` (`λ > 0`), flipping `(-1)^k`.
2. **Finite Mapping-Torus Fermion Determinant Sign Reversal**:
   - The `2 × 2` mapping-torus Dirac block `diracMappingBlock m s = !![m, s; 1, m]` has
     determinant `m² - s`; at `m = 0`, the antiperiodic untwisted sector (`s = -1`) has
     `det = +1 > 0` whereas the `ℤ₂`-twisted periodic sector (`s = +1`) has `det = -1 < 0`.
3. **Arf Quadratic Refinement Gaussian Sign Sums on `(ZMod 2)²` and Mod-2 AHSS Pairing**:
   - The even Arf-0 quadratic form `q₀(x, y) = x * y` on `{0, 1}²` has Gaussian sign sum
     `+2` (`(1/2) ∑ (-1)^{q₀} = +1`), whereas the odd Arf-1 quadratic form
     `q₁(x, y) = x * y + x + y` has Gaussian sign sum `-2` (`(1/2) ∑ (-1)^{q₁} = -1`).
   - The mod-2 5D cobordism pairing `nu5Pairing a3 arf w1 sigmaDiv16 = a3 * arf + w1 * sigmaDiv16`
     vanishes on `T⁴` (`arf = 0, sigmaDiv16 = 0`) and evaluates to `1 ≠ 0` on both the
     `K3` gauge-gravitational sector (`w1 = 1, sigmaDiv16 = 1, a3 = 0`) and the Postnikov-Arf
     sector (`a3 = 1, arf = 1, w1 = 0`).
4. **Class-Specific Representation No-Go and 5D Bulk Inflow Cancellation**:
   - In any representation class whose partition sum `Z = w₀ + w₁` is required to satisfy
     both nonnegativity (`w₀ ≥ 0, w₁ ≥ 0`) and the anomalous Ward identity `Z = -Z`, every
     representation has `w₀ = 0 ∧ w₁ = 0`, ruling out any positive partition sum `Z > 0`
     within that symmetry-preserving class.
   - Coupling the 4D boundary class `ν₅ ∈ ZMod 2` to a 5D bulk counterterm `-ν₅` cancels the
     total class (`ν₅ + (-ν₅) = 0`) and squares the integer sign `(-1)^{ν₅} * (-1)^{ν₅} = +1`.
5. **Class-Specificity, `Pin⁻` `ℤ₁₆`, and Thermal Asymmetry Scope Fences (`GIN-C22`)**:
   - Outside the symmetry-constrained representation class, a basis change can remove
     off-diagonal sign problems (e.g. `H = !![1, -1; -1, 1]` vs its diagonalized spectrum
     `D = !![0, 0; 0, 2]` with identical trace `2` and determinant `0`).
   - In `ZMod 16` (`Ω₅^{Pin⁻}`), the generator `1` is not annihilated by doubling (`2 * 1 ≠ 0`),
     and thermal weight asymmetry `w₊ ≠ w₋` leaves `w₊ - w₋ ≠ 0` even when `ν₅ = 0`.
-/

namespace CampaignFspCobordismIntrinsicSign

open Matrix

/-- Discrete spectral sign `sgn(λ) ∈ {-1, 0, +1}` for integer eigenvalues `λ ∈ ℤ`. -/
def spectralSign (lam : ℤ) : ℤ :=
  if 0 < lam then 1 else if lam < 0 then -1 else 0

/-- Theorem 1 (Spectral Sign Oddness and Symmetric Doublet Cancellation):
`spectralSign` is odd (`spectralSign (-λ) = -spectralSign λ`) and any particle-hole
symmetric eigenvalue pair `(λ, -λ)` contributes zero net spectral asymmetry. -/
theorem spectralSign_odd_and_symmetric_pair_zero (lam : ℤ) :
    spectralSign (-lam) = -spectralSign lam ∧
    spectralSign lam + spectralSign (-lam) = 0 := by
  unfold spectralSign
  split_ifs <;> omega

/-- Theorem 2 (Single-Mode Zero Crossing Jumps Spectral Asymmetry by `+2` and Flips Parity):
For any positive eigenvalue `lam > 0`, crossing from `-lam < 0` to `+lam > 0` changes
`spectralSign` by `+2` (`Δ(η/2) = 1`) and flips the parity factor `(-1)^(k + 1) = -((-1)^k)`. -/
theorem single_eigenvalue_crossing_eta_jump_by_two (lam : ℤ) (hpos : 0 < lam) (k : ℕ) :
    spectralSign lam = 1 ∧
    spectralSign (-lam) = -1 ∧
    spectralSign lam - spectralSign (-lam) = 2 ∧
    (-1 : ℤ) ^ (k + 1) = -((-1 : ℤ) ^ k) := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · rw [spectralSign, if_pos hpos]
  · unfold spectralSign
    split_ifs <;> omega
  · unfold spectralSign
    split_ifs <;> omega
  · rw [pow_succ]
    ring

/-- Finite `2 × 2` mapping-torus Dirac block with mass `m` and `S¹` holonomy twist `s`. -/
def diracMappingBlock (m s : ℤ) : Matrix (Fin 2) (Fin 2) ℤ :=
  !![m, s;
     1, m]

/-- Theorem 3 (Mapping-Torus Fermion Determinant Sign Reversal at `m = 0`):
`det (diracMappingBlock m s) = m² - s`; at the massless point `m = 0`, the untwisted
antiperiodic sector (`s = -1`) has positive determinant `+1`, whereas the `ℤ₂`-twisted
periodic sector (`s = +1`) has negative determinant `-1`, so their equal-weight sum vanishes. -/
theorem mapping_torus_fermion_det_sign_reversal (m s : ℤ) :
    Matrix.det (diracMappingBlock m s) = m ^ 2 - s ∧
    Matrix.det (diracMappingBlock 0 (-1)) = 1 ∧
    Matrix.det (diracMappingBlock 0 1) = -1 ∧
    Matrix.det (diracMappingBlock 0 (-1)) + Matrix.det (diracMappingBlock 0 1) = 0 := by
  refine ⟨?_, by decide, by decide, by decide⟩
  simp [diracMappingBlock, Matrix.det_fin_two]
  ring

/-- Arf-0 quadratic form `q₀(x, y) = x * y` on `{0, 1}²` (evaluated in `ℕ`). -/
def arf0Form (x y : Fin 2) : ℕ := x.val * y.val

/-- Arf-1 quadratic form `q₁(x, y) = x * y + x + y` on `{0, 1}²` (evaluated in `ℕ`). -/
def arf1Form (x y : Fin 2) : ℕ := x.val * y.val + x.val + y.val

/-- Gaussian sign sum `∑_{x,y ∈ Fin 2} (-1)^{q(x,y)}` for a quadratic form `q` on `(Fin 2)²`. -/
def arfGaussianSum (q : Fin 2 → Fin 2 → ℕ) : ℤ :=
  ((-1 : ℤ) ^ q 0 0) + ((-1 : ℤ) ^ q 0 1) + ((-1 : ℤ) ^ q 1 0) + ((-1 : ℤ) ^ q 1 1)

/-- Theorem 4 (Arf Invariant Gaussian Sign Sum Dichotomy on `(Fin 2)²`):
The even Arf-0 quadratic form `arf0Form` has Gaussian sign sum `+2` (`+2 / 2 = +1 = (-1)^0`),
whereas the odd Arf-1 quadratic form `arf1Form` has Gaussian sign sum `-2` (`-2 / 2 = -1 = (-1)^1`). -/
theorem arf_gaussian_sign_sum_dichotomy :
    arfGaussianSum arf0Form = 2 ∧
    arfGaussianSum arf1Form = -2 ∧
    arfGaussianSum arf0Form + arfGaussianSum arf1Form = 0 := by
  decide

/-- Mod-2 5D Spin cobordism pairing `ν₅ = a₃ · Arf + w₁ · (σ/16)` in `ZMod 2`. -/
def nu5Pairing (a3 arf w1 sigmaDiv16 : ZMod 2) : ZMod 2 :=
  a3 * arf + w1 * sigmaDiv16

/-- Theorem 5 (Mod-2 5D Cobordism Pairing on `T⁴`, `K3`, and Postnikov-Arf Sectors):
`nu5Pairing` vanishes on the anomaly-free `T⁴` sector (`arf = 0, sigmaDiv16 = 0`) for all
`a3, w1`, and evaluates to `1 ≠ 0` on both the `K3` gauge-gravitational sector
(`a3 = 0, w1 = 1, sigmaDiv16 = 1`) and the Postnikov-Arf sector (`a3 = 1, arf = 1, w1 = 0`). -/
theorem ahss_5d_spin_cobordism_pairing_sectors (a3 arf w1 sigmaDiv16 : ZMod 2) :
    nu5Pairing a3 0 w1 0 = 0 ∧
    nu5Pairing 0 arf 1 1 = 1 ∧
    nu5Pairing 1 1 0 sigmaDiv16 = 1 ∧
    (1 : ZMod 2) ≠ 0 := by
  refine ⟨?_, ?_, ?_, by decide⟩
  · simp [nu5Pairing]
  · simp [nu5Pairing]
  · simp [nu5Pairing]

/-- Theorem 6 (Class-Specific Intrinsic Sign No-Go Under Odd Anomaly Ward Identity):
In any symmetry-preserving representation class where configuration weights `w₀, w₁ : ℤ`
are nonnegative (`0 ≤ w₀`, `0 ≤ w₁`) and the partition sum `Z = w₀ + w₁` satisfies the odd
anomalous Ward identity `w₀ + w₁ = -(w₀ + w₁)` (`U(f) Z = -Z`), both weights must vanish
(`w₀ = 0 ∧ w₁ = 0`), ruling out any positive partition sum `w₀ + w₁ > 0` in that class. -/
theorem anomaly_odd_ward_identity_rules_out_positive_weights_in_class
    (w0 w1 : ℤ) (hw0 : 0 ≤ w0) (hw1 : 0 ≤ w1) :
    (w0 + w1 = -(w0 + w1) → w0 = 0 ∧ w1 = 0) ∧
    (0 < w0 + w1 → w0 + w1 ≠ -(w0 + w1)) := by
  refine ⟨?_, ?_⟩
  · intro hward
    omega
  · intro hpos hward
    omega

/-- Theorem 7 (5D Bulk Topological Inflow Cancels 4D Boundary Anomaly Sign):
Coupling a 4D boundary cobordism class `nu5 : ZMod 2` to its 5D bulk inflow partner
`-nu5 : ZMod 2` yields total class `nu5 + (-nu5) = 0` in `ZMod 2` and positive product sign
`((-1 : ℤ) ^ nu5.val) * ((-1 : ℤ) ^ nu5.val) = 1`. -/
theorem five_d_bulk_inflow_cancels_boundary_anomaly_sign (nu5 : ZMod 2) :
    nu5 + (-nu5) = 0 ∧
    ((-1 : ℤ) ^ nu5.val) * ((-1 : ℤ) ^ nu5.val) = 1 := by
  refine ⟨add_neg_cancel nu5, ?_⟩
  fin_cases nu5 <;> decide

/-- Theorem 8 (`Ω₅^{Pin⁻} ≅ ℤ₁₆` Non-Involution Fence on `ℝP⁴`):
In `ZMod 16`, the generator `1` is not annihilated by 2-fold pairing (`2 * (1 : ZMod 16) ≠ 0`)
or 8-fold pairing (`8 * (1 : ZMod 16) ≠ 0`), requiring 16 copies (`16 * (1 : ZMod 16) = 0`). -/
theorem pin_minus_z16_order_sixteen_fence :
    (1 : ZMod 16) ≠ 0 ∧
    (2 : ZMod 16) * (1 : ZMod 16) ≠ 0 ∧
    (8 : ZMod 16) * (1 : ZMod 16) ≠ 0 ∧
    (16 : ZMod 16) * (1 : ZMod 16) = 0 := by
  decide

/-- Off-diagonal signed matrix `H = !![1, -1; -1, 1]` and its nonnegative diagonalized partner
`D = !![0, 0; 0, 2]`. -/
def offDiagSignedMat : Matrix (Fin 2) (Fin 2) ℤ :=
  !![1, -1;
     -1, 1]

/-- Nonnegative diagonalized partner `D = !![0, 0; 0, 2]`. -/
def diagNonnegMat : Matrix (Fin 2) (Fin 2) ℤ :=
  !![0, 0;
     0, 2]

/-- Change-of-basis matrix `P = !![1, 1; 1, -1]` (unnormalized Hadamard). -/
def hadamardBasisMat : Matrix (Fin 2) (Fin 2) ℤ :=
  !![1, 1;
     1, -1]

/-- Theorem 9 (Class-Specificity Scope Fence: Basis Change Outside Constrained Class):
While `offDiagSignedMat` has negative off-diagonal entries `-1 < 0`, conjugating by
`hadamardBasisMat` diagonalizes it to `2 • diagNonnegMat = !![0, 0; 0, 4]` with nonnegative
entries, preserving `trace = 2` and `det = 0`, illustrating that sign obstructions depend
on the symmetry/locality constraints of the representation class (`TFQ-1211` bottleneck). -/
theorem basis_change_removes_sign_outside_constrained_class_fence :
    offDiagSignedMat 0 1 = -1 ∧
    Matrix.trace offDiagSignedMat = Matrix.trace diagNonnegMat ∧
    Matrix.det offDiagSignedMat = Matrix.det diagNonnegMat ∧
    hadamardBasisMat * offDiagSignedMat * hadamardBasisMat =
      (2 : ℤ) • diagNonnegMat := by
  refine ⟨rfl, by decide, by decide, ?_⟩
  ext i j; fin_cases i <;> fin_cases j <;> decide

/-- Theorem 10 (Thermal Orientation Weight Asymmetry Fence, `GIN-C22`):
Even when the topological cobordism class is trivial (`nu5 = 0`, sign `+1`), unequal
orientation weights `w_pos ≠ w_neg` leave a nonzero residual `w_pos - w_neg ≠ 0`. -/
theorem thermal_orientation_weight_asymmetry_fence (w_pos w_neg : ℤ) :
    (w_pos = w_neg → w_pos - w_neg = 0) ∧
    (w_pos ≠ w_neg → w_pos - w_neg ≠ 0) := by
  refine ⟨by omega, by omega⟩

end CampaignFspCobordismIntrinsicSign
