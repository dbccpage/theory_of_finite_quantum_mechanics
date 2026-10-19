import Mathlib.Data.Real.Basic
import Mathlib.Data.Complex.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Rat.Defs
import Mathlib.Data.Rat.Lemmas
import Mathlib.Analysis.Real.Sqrt
import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Topology.ContinuousMap.Basic
import Mathlib.Topology.Compactness.Compact
import Mathlib.Topology.Order.MonotoneContinuity
import Mathlib.Topology.MetricSpace.Basic
import Mathlib.Topology.MetricSpace.ProperSpace
import Mathlib.LinearAlgebra.UnitaryGroup
import Mathlib.Analysis.CStarAlgebra.Matrix
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.FinCases
import BasisExtensionObstruction
import ExtensionCurvatureObstruction
import TripleExtensionAssembly
/-!
# D1': the symmetry-reduction principle and per-basis right-phase (dephasing) invariance

Second symmetry-reduction step (D1') of the MUB(d) ≤ 3 attack, built on the ASSEMBLY
(`MUB.TripleExtensionAssembly`) and the gauge reduction (`MUB.TripleGaugeReduction`). It
mechanizes:

* `no_four_mub_of_psiVal_pos_on_orbit_reps` — **the abstract symmetry-reduction
  principle**: for any family of `psiVal`-invariant maps that reaches a set `S` from every
  triple, positivity on `S` rules out four MUBs. This is the reusable backbone every
  symmetry (the U(d) gauge of D1, the dephasing here, and the eventual finite
  Weyl–Heisenberg/Clifford group) plugs into.
* `rightPhase v hv T` — the **per-basis right-phase action**: right-multiply each basis by
  a diagonal phase matrix `diagonal (v a)` with unit-modulus entries.
* `psiVal_rightPhase` — **`psiVal` is invariant under per-basis right-phase (dephasing)**.
  Phases factor out of `|⟨·,·⟩|²`, so the deviation mass is literally unchanged.

The right action is the residual of the Hadamard equivalence that D1's left `U(d)` gauge
did not consume; dephasing collapses the bulk of the Hadamard moduli on the normalized
slice. All declarations are axiom-clean (`[propext, Classical.choice, Quot.sound]`, no
`sorry`).

## Firewall (honest scope)

This is a *symmetry reduction*, not a solution of MUB(6) ≤ 3. It mechanizes the reduction
*principle* and the *phase* generator of the discrete/Hadamard symmetry. The remaining
generators — column **permutations** within a basis, the basis-relabelling group, and the
synthesis into the finite **Cl(2)⊗Cl(3)** fundamental domain — are follow-up work, as is
the cover itself. `psiVal` is a diagnostic; it mints no authority.
-/

open Matrix Metric
open MUB.BasisExtensionObstruction
open MUB.ExtensionCurvatureObstruction
open MUB.TripleExtensionAssembly

namespace MUB.TripleHadamardDephase

variable {d : ℕ}

/-- **Symmetry-reduction principle.** If a family of `psiVal`-invariant maps reaches a set
`S` from every triple, positivity on `S` suffices to rule out four MUBs. The reusable
backbone for every symmetry reduction (gauge, dephasing, the finite Clifford group). -/
theorem no_four_mub_of_psiVal_pos_on_orbit_reps {ι : Type*}
    (act : ι → MUTriple d → MUTriple d) (hinv : ∀ g T, psiVal (act g T) = psiVal T)
    (S : Set (MUTriple d)) (hreach : ∀ T, ∃ g, act g T ∈ S)
    (h : ∀ T ∈ S, 0 < psiVal T) : ¬ FourMUB d := by
  refine no_four_mub_of_psiVal_pos (fun T => ?_)
  obtain ⟨g, hg⟩ := hreach T
  rw [← hinv g T]
  exact h (act g T) hg

/-- A unit-modulus phase has norm one. -/
theorem phase_norm_one {z : ℂ} (hz : (starRingEnd ℂ) z * z = 1) : ‖z‖ = 1 := by
  have h : ‖z‖ * ‖z‖ = 1 := by
    have hc := congrArg norm hz
    rwa [norm_mul, RCLike.norm_conj, norm_one] at hc
  calc ‖z‖ = Real.sqrt (‖z‖ * ‖z‖) := (Real.sqrt_mul_self (norm_nonneg z)).symm
    _ = Real.sqrt 1 := by rw [h]
    _ = 1 := Real.sqrt_one

/-- A diagonal unitary built from a unit-modulus phase vector. -/
def diagU (v : Fin d → ℂ) (hv : ∀ k, (starRingEnd ℂ) (v k) * v k = 1) :
    Matrix.unitaryGroup (Fin d) ℂ :=
  ⟨Matrix.diagonal v, by
    rw [Matrix.mem_unitaryGroup_iff', Matrix.star_eq_conjTranspose, Matrix.diagonal_conjTranspose,
      Matrix.diagonal_mul_diagonal]
    have hv1 : (fun i => star v i * v i) = (1 : Fin d → ℂ) := by
      funext k
      simp only [Pi.star_apply, Pi.one_apply]
      rw [← starRingEnd_apply]; exact hv k
    rw [hv1]; exact Matrix.diagonal_one⟩

/-- Right-multiplying basis `a` by `diagonal v` reads off as a per-column phase. -/
theorem coe_mul_diagU (X : Matrix.unitaryGroup (Fin d) ℂ) (v : Fin d → ℂ) (hv) (k i : Fin d) :
    ((X * diagU v hv : Matrix.unitaryGroup (Fin d) ℂ) : Matrix (Fin d) (Fin d) ℂ) k i
      = (X : Matrix (Fin d) (Fin d) ℂ) k i * v i := by
  show ((X : Matrix (Fin d) (Fin d) ℂ) * Matrix.diagonal v) k i = _
  rw [Matrix.mul_diagonal]

/-- Per-basis right-phase action: right-multiply each basis by a diagonal phase. -/
def rightPhase (v : Fin 3 → Fin d → ℂ) (hv : ∀ a k, (starRingEnd ℂ) (v a k) * v a k = 1)
    (T : MUTriple d) : MUTriple d :=
  ⟨fun a => T.val a * diagU (v a) (hv a), by
    intro a b hab i j
    have hc : ‖(starRingEnd ℂ) (v a i) * v b j‖ = 1 := by
      rw [norm_mul, RCLike.norm_conj, phase_norm_one (hv a i), phase_norm_one (hv b j), one_mul]
    have key :
        (∑ k, (starRingEnd ℂ)
                (((T.val a * diagU (v a) (hv a) : Matrix.unitaryGroup (Fin d) ℂ)
                    : Matrix (Fin d) (Fin d) ℂ) k i)
                * ((T.val b * diagU (v b) (hv b) : Matrix.unitaryGroup (Fin d) ℂ)
                    : Matrix (Fin d) (Fin d) ℂ) k j)
          = ((starRingEnd ℂ) (v a i) * v b j)
              * ∑ k, (starRingEnd ℂ) ((T.val a : Matrix (Fin d) (Fin d) ℂ) k i)
                  * (T.val b : Matrix (Fin d) (Fin d) ℂ) k j := by
      rw [Finset.mul_sum]
      refine Finset.sum_congr rfl (fun k _ => ?_)
      rw [coe_mul_diagU, coe_mul_diagU, map_mul]; ring
    rw [key, norm_mul, hc, one_mul]
    exact T.2 a b hab i j⟩

theorem toFlat_rightPhase (v : Fin 3 → Fin d → ℂ) (hv) (T : MUTriple d) (i k) :
    (rightPhase v hv T).toFlat i k
      = T.toFlat i k * v ((finProdFinEquiv (m := 3) (n := d)).symm i).1
          ((finProdFinEquiv (m := 3) (n := d)).symm i).2 := by
  simp only [MUTriple.toFlat, rightPhase, coe_mul_diagU]

theorem overlap_rightPhase (v : Fin 3 → Fin d → ℂ) (hv) (T : MUTriple d)
    (U : Matrix.unitaryGroup (Fin d) ℂ) (i : Fin (3 * d)) (j : Fin d) :
    overlap (rightPhase v hv T).toFlat U i j
      = (starRingEnd ℂ) (v ((finProdFinEquiv (m := 3) (n := d)).symm i).1
          ((finProdFinEquiv (m := 3) (n := d)).symm i).2) * overlap T.toFlat U i j := by
  simp only [overlap, toFlat_rightPhase, Finset.mul_sum, map_mul]
  refine Finset.sum_congr rfl (fun k _ => ?_); ring

/-- The deviation mass is invariant under per-basis right-phase (dephasing). -/
theorem basisDeviation_rightPhase (v : Fin 3 → Fin d → ℂ) (hv) (T : MUTriple d)
    (U : Matrix.unitaryGroup (Fin d) ℂ) :
    basisDeviation (rightPhase v hv T).toFlat U = basisDeviation T.toFlat U := by
  unfold basisDeviation
  refine Finset.sum_congr rfl (fun j _ => Finset.sum_congr rfl (fun i _ => ?_))
  have hnorm : ‖overlap (rightPhase v hv T).toFlat U i j‖ = ‖overlap T.toFlat U i j‖ := by
    rw [overlap_rightPhase, norm_mul, RCLike.norm_conj, phase_norm_one (hv _ _), one_mul]
  rw [hnorm]

/-- **D1' (right-phase invariance).** `psiVal` is invariant under per-basis
right-multiplication by diagonal phases — the dephasing of the Hadamard slice. -/
theorem psiVal_rightPhase (v : Fin 3 → Fin d → ℂ) (hv) (T : MUTriple d) :
    psiVal (rightPhase v hv T) = psiVal T := by
  rw [psiVal, psiVal, phi_eq_sInf, phi_eq_sInf,
    show (Psi_basis (rightPhase v hv T).toFlat).mass = (Psi_basis T.toFlat).mass from
      funext (fun U => basisDeviation_rightPhase v hv T U)]

end MUB.TripleHadamardDephase

#print axioms MUB.TripleHadamardDephase.no_four_mub_of_psiVal_pos_on_orbit_reps
#print axioms MUB.TripleHadamardDephase.psiVal_rightPhase
