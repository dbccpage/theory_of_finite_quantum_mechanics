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
import ExtensionCurvatureObstruction
/-!
# Basis-level MUB extension obstruction `Ψ_basis`

The vector-level obstruction `Φ₁` of `MUB.ExtensionCurvatureObstruction` certifies
*no fourth MU **vector*** for a fixed set — strictly stronger than MUB(d) needs
(*no fourth MU **basis***). This module gives the **basis-level** obstruction by
modeling a candidate fourth basis as a **unitary matrix** `U ∈ unitaryGroup`: its
columns are *automatically orthonormal*, so `Ψ_basis = 0 ⟺ a fourth MU basis
extends the fixed set` — closing the vector-vs-basis strength gap. The space of
candidate bases (`unitaryGroup (Fin d) ℂ`) is compact, so attainment is free and we
reuse `ExtensionObstruction.ofCompact` + `phi_eq_zero_iff` verbatim.

`Ψ_basis` is a diagnostic obstruction; nothing here claims MUB(6) ≤ 3.
-/

open Matrix Metric
open MUB.ExtensionCurvatureObstruction

namespace MUB
namespace BasisExtensionObstruction

/-- **The candidate-basis space is compact.** `unitaryGroup (Fin d) ℂ` is a closed
(`U ↦ star U * U` continuous, preimage of `{1}`) and bounded (entries `≤ 1`) subset
of a finite product of compact ℂ-closedballs. -/
instance unitaryGroup_compactSpace {d : ℕ} :
    CompactSpace (Matrix.unitaryGroup (Fin d) ℂ) := by
  have hcont : Continuous (fun U : Matrix (Fin d) (Fin d) ℂ => star U * U) := by
    refine continuous_matrix (fun i j => ?_)
    simp only [Matrix.mul_apply, Matrix.star_apply]
    refine continuous_finsetSum _ (fun k _ => ?_)
    exact (continuous_star.comp (continuous_id.matrix_elem k i)).mul
      (continuous_id.matrix_elem k j)
  have hclosed : IsClosed
      (Matrix.unitaryGroup (Fin d) ℂ : Set (Matrix (Fin d) (Fin d) ℂ)) := by
    have hpre : (Matrix.unitaryGroup (Fin d) ℂ : Set (Matrix (Fin d) (Fin d) ℂ))
        = (fun U => star U * U) ⁻¹' {1} := by
      ext U
      simp only [Set.mem_preimage, Set.mem_singleton_iff, SetLike.mem_coe,
        Matrix.mem_unitaryGroup_iff']
    rw [hpre]; exact isClosed_singleton.preimage hcont
  have hcompact : IsCompact
      (Matrix.unitaryGroup (Fin d) ℂ : Set (Matrix (Fin d) (Fin d) ℂ)) := by
    refine (isCompact_univ_pi (fun _ : Fin d =>
              isCompact_univ_pi (fun _ : Fin d =>
                isCompact_closedBall (0 : ℂ) 1))).of_isClosed_subset hclosed ?_
    intro U hU i _ j _
    rw [mem_closedBall, dist_zero_right]; exact entry_norm_bound_of_unitary hU i j
  exact isCompact_iff_compactSpace.mp hcompact

/-- Overlap of fixed vector `e i` with column `j` of candidate basis `U`
(`∑ₖ conj(eᵢ ₖ) · U ₖ ⱼ`). -/
noncomputable def overlap {N d : ℕ} (e : Fin N → (Fin d → ℂ))
    (U : Matrix.unitaryGroup (Fin d) ℂ) (i : Fin N) (j : Fin d) : ℂ :=
  ∑ k, (starRingEnd ℂ) (e i k) * (U : Matrix (Fin d) (Fin d) ℂ) k j

/-- Basis-level deviation: ℓ¹ mass of how far the columns of `U` are from being
mutually unbiased (`|overlap|² = 1/d`) to the fixed set `e`. -/
noncomputable def basisDeviation {N d : ℕ} (e : Fin N → (Fin d → ℂ))
    (U : Matrix.unitaryGroup (Fin d) ℂ) : ℝ :=
  ∑ j, ∑ i, |‖overlap e U i j‖ ^ 2 - 1 / (d : ℝ)|

theorem basisDeviation_nonneg {N d : ℕ} (e : Fin N → (Fin d → ℂ)) (U) :
    0 ≤ basisDeviation e U :=
  Finset.sum_nonneg (fun _ _ => Finset.sum_nonneg (fun _ _ => abs_nonneg _))

theorem continuous_basisDeviation {N d : ℕ} (e : Fin N → (Fin d → ℂ)) :
    Continuous (basisDeviation e) := by
  refine continuous_finsetSum _ (fun j _ => continuous_finsetSum _ (fun i _ => ?_))
  refine (Continuous.sub ?_ continuous_const).abs
  refine (Continuous.norm ?_).pow 2
  refine continuous_finsetSum _ (fun k _ => ?_)
  exact continuous_const.mul (continuous_subtype_val.matrix_elem k j)

/-- The basis-level obstruction mass — `min` over the compact candidate-basis space,
attainment discharged by `ExtensionObstruction.ofCompact`. -/
noncomputable def Psi_basis {N d : ℕ} (e : Fin N → (Fin d → ℂ)) :
    ExtensionObstruction (Matrix.unitaryGroup (Fin d) ℂ) :=
  ExtensionObstruction.ofCompact (basisDeviation e) (basisDeviation_nonneg e)
    (continuous_basisDeviation e)

theorem basisDeviation_eq_zero_iff {N d : ℕ} (e : Fin N → (Fin d → ℂ)) (U) :
    basisDeviation e U = 0 ↔ ∀ j i, ‖overlap e U i j‖ ^ 2 = 1 / (d : ℝ) := by
  unfold basisDeviation
  rw [Finset.sum_eq_zero_iff_of_nonneg
        (fun j _ => Finset.sum_nonneg (fun i _ => abs_nonneg _))]
  constructor
  · intro h j i
    have hj := h j (Finset.mem_univ j)
    rw [Finset.sum_eq_zero_iff_of_nonneg (fun i _ => abs_nonneg _)] at hj
    have := hj i (Finset.mem_univ i)
    rwa [abs_eq_zero, sub_eq_zero] at this
  · intro h j _
    refine Finset.sum_eq_zero (fun i _ => ?_)
    rw [abs_eq_zero, sub_eq_zero]; exact h j i

/-- **The basis-level characterization (Step 2 closing artifact).** `Ψ_basis = 0`
iff there is a unitary `U` whose every column is mutually unbiased to the fixed set
`e` — i.e. **a fourth MU basis (the orthonormal columns of `U`, orthonormal by
unitarity) extends `e`**. Unlike the vector-level `Φ₁`, this is exactly what
"no fourth MU basis" requires (the vector-vs-basis strength gap is closed). -/
theorem Psi_basis_zero_iff_fourth_basis {N d : ℕ} (e : Fin N → (Fin d → ℂ)) :
    (Psi_basis e).phi = 0 ↔
      ∃ U : Matrix.unitaryGroup (Fin d) ℂ, ∀ j i, ‖overlap e U i j‖ ^ 2 = 1 / (d : ℝ) := by
  rw [Psi_basis, ExtensionObstruction.phi_eq_zero_iff]
  constructor
  · rintro ⟨U, hU⟩; exact ⟨U, (basisDeviation_eq_zero_iff e U).mp hU⟩
  · rintro ⟨U, hU⟩; exact ⟨U, (basisDeviation_eq_zero_iff e U).mpr hU⟩

/-- **No-go form: `Ψ_basis > 0 ⟺ no fourth MU basis`.** The contrapositive of the
characterization, using `Ψ_basis ≥ 0`: a strictly positive basis-level obstruction
means no unitary is mutually unbiased to the fixed set — no fourth MU basis extends
it. (This names + checks the positive direction the prose relies on.) -/
theorem Psi_basis_pos_iff_no_fourth_basis {N d : ℕ} (e : Fin N → (Fin d → ℂ)) :
    0 < (Psi_basis e).phi ↔
      ¬ ∃ U : Matrix.unitaryGroup (Fin d) ℂ, ∀ j i, ‖overlap e U i j‖ ^ 2 = 1 / (d : ℝ) := by
  rw [← Psi_basis_zero_iff_fourth_basis]
  exact ⟨fun h => h.ne', fun h => lt_of_le_of_ne (Psi_basis e).phi_nonneg (Ne.symm h)⟩

/-- d=6 instance: the basis-level characterization for the canonical-triple problem
(`N = 18` fixed vectors of `ℂ⁶`, target `1/6`). Conditional on nothing — it is the
exact statement "a fourth MU basis extends the 18 fixed vectors". -/
theorem psi_basis_zero_iff_fourth_basis_d6 (e : Fin 18 → (Fin 6 → ℂ)) :
    (Psi_basis e).phi = 0 ↔
      ∃ U : Matrix.unitaryGroup (Fin 6) ℂ, ∀ j i, ‖overlap e U i j‖ ^ 2 = 1 / (6 : ℝ) :=
  Psi_basis_zero_iff_fourth_basis e

end BasisExtensionObstruction
end MUB

-- Axiom hygiene.
#print axioms MUB.BasisExtensionObstruction.unitaryGroup_compactSpace
#print axioms MUB.BasisExtensionObstruction.continuous_basisDeviation
#print axioms MUB.BasisExtensionObstruction.basisDeviation_eq_zero_iff
#print axioms MUB.BasisExtensionObstruction.Psi_basis_zero_iff_fourth_basis
#print axioms MUB.BasisExtensionObstruction.Psi_basis_pos_iff_no_fourth_basis
#print axioms MUB.BasisExtensionObstruction.psi_basis_zero_iff_fourth_basis_d6
