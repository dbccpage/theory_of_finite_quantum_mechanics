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
import BasisExtensionObstruction
/-!
# Wiring the exact interval cover into the **basis-level** MUB(6) no-go

`MUB.FiniteVectorCover` is the Lean consume-target for the vector-level cover: a finite
family of certified patches that covers the candidate **vectors** mechanizes *no fourth
MU vector*. This module is its **basis-level** analog. The candidate is now a full unitary
`U ∈ unitaryGroup (Fin d) ℂ` (a candidate fourth basis), and the Rust engine
(`crates/omega_mub/src/omega_native/mub6_basis_cover.rs`) certifies, per box and in exact
rational arithmetic, a positive lower bound `ε_j ≤ Ψ^sq(T, U)` on the **basis-level squared
curvature mass**

```text
  Ψ^sq(T, U) = ∑_j ∑_i (‖overlap e U i j‖² − target)²
```

over a patch `Uc_j` of candidate bases. A finite family of such patches that **covers** the
candidate-basis set turns into the mechanized conclusion *no unitary is mutually unbiased to
the fixed set `e`* — i.e. `Ψ_basis(e) > 0`, **no fourth MU basis extends the canonical triple**.

The bridge is the already-proved `finite_cover_no_feasible` (ENC-1133), reused verbatim over
`V = unitaryGroup (Fin d) ℂ`, plus the basis-level characterization
`MUB.BasisExtensionObstruction.Psi_basis_pos_iff_no_fourth_basis` (ENC-1142). The basis mass
vanishes *exactly* at fourth MU bases, so a complete certified cover with `Ψ^sq > 0` on every
patch leaves no room for one.

**Per-column note (the reduction the Rust kernel uses).** `Ψ^sq` factorizes over the columns,
`Ψ^sq(T, U) = ∑_j Φ^sq(T, U_j)`, so the basis cover is the sum of six vector covers and a
basis box is excluded as soon as any single column box is vector-excluded. For a *fixed* triple
this makes the basis-level no-go a corollary of the (strictly stronger) vector-level no-go; the
genuinely-open content is the cover over the **moduli of triples** (the dephased Hadamard slice,
`MUB.TripleHadamardDephase`), which the Rust `BoxedTriple` kernel templates.

**Firewall.** This mechanizes the *logic* that assembles a finite certified cover into the
basis-level no-go for a *fixed* triple; producing a cover of the whole compact candidate space
(and, for `MUB(6) ≤ 3`, over all triples) is the finite computation / open frontier. It is not
-/

namespace MUB
namespace FiniteBasisCover

open Matrix
open MUB.ExtensionCurvatureObstruction
open MUB.BasisExtensionObstruction

variable {N d : ℕ}

/-- The basis-level ℓ² curvature mass of a candidate basis `U` against the fixed set `e`
with unbiasedness target `target`:
`Ψ^sq(U) = ∑_j ∑_i (‖overlap e U i j‖² − target)²`. This is exactly the quantity the Rust
`mub6_basis_cover` engine lower-bounds per box (`basis_residual_sq_lower`). -/
noncomputable def basisCurvatureMass (e : Fin N → (Fin d → ℂ)) (target : ℝ)
    (U : Matrix.unitaryGroup (Fin d) ℂ) : ℝ :=
  ∑ j, ∑ i, (‖overlap e U i j‖ ^ 2 - target) ^ 2

theorem basisCurvatureMass_nonneg (e : Fin N → (Fin d → ℂ)) (target : ℝ) (U) :
    0 ≤ basisCurvatureMass e target U :=
  Finset.sum_nonneg fun _ _ => Finset.sum_nonneg fun _ _ => sq_nonneg _

/-- The basis mass vanishes **iff** every column of `U` is mutually unbiased to `e`
(`‖overlap e U i j‖² = target` for all `i, j`) — i.e. iff `U` is a fourth MU basis. -/
theorem basisCurvatureMass_eq_zero_iff (e : Fin N → (Fin d → ℂ)) (target : ℝ) (U) :
    basisCurvatureMass e target U = 0 ↔ ∀ j i, ‖overlap e U i j‖ ^ 2 = target := by
  unfold basisCurvatureMass
  rw [Finset.sum_eq_zero_iff_of_nonneg
        (fun j _ => Finset.sum_nonneg (fun i _ => sq_nonneg _))]
  constructor
  · intro h j i
    have hj := h j (Finset.mem_univ j)
    rw [Finset.sum_eq_zero_iff_of_nonneg (fun i _ => sq_nonneg _)] at hj
    have := hj i (Finset.mem_univ i)
    rwa [sq_eq_zero_iff, sub_eq_zero] at this
  · intro h j _
    refine Finset.sum_eq_zero (fun i _ => ?_)
    rw [sq_eq_zero_iff, sub_eq_zero]; exact h j i

/-- **The cover no-go on a candidate-basis set `K`.** Given a finite family of patches `Uc_j`
(`j ∈ s`) covering `K`, each carrying a certified positive lower bound `ε_j ≤ Ψ^sq` on it, no
member of `K` is a fourth MU basis for `e`. The hypotheses are precisely the output of a
completed Rust basis-cover run. -/
theorem no_fourth_basis_in_cover {ι : Type*}
    (s : Finset ι) (Uc : ι → Set (Matrix.unitaryGroup (Fin d) ℂ))
    (K : Set (Matrix.unitaryGroup (Fin d) ℂ))
    (e : Fin N → (Fin d → ℂ)) (target : ℝ)
    (hcover : ∀ U ∈ K, ∃ j ∈ s, U ∈ Uc j) (ε : ι → ℝ)
    (hbound : ∀ j ∈ s, ∀ U ∈ Uc j, ε j ≤ basisCurvatureMass e target U)
    (hpos : ∀ j ∈ s, 0 < ε j) :
    ∀ U ∈ K, ¬ ∀ j i, ‖overlap e U i j‖ ^ 2 = target := by
  intro U hU hMU
  have hΨ : 0 < basisCurvatureMass e target U :=
    finite_cover_no_feasible s Uc (basisCurvatureMass e target) K hcover ε hbound hpos U hU
  rw [(basisCurvatureMass_eq_zero_iff e target U).mpr hMU] at hΨ
  exact lt_irrefl 0 hΨ

/-- **No fourth MU basis exists at all**, given a certified cover of a candidate-basis set `K`
that contains every fourth MU basis. -/
theorem no_fourth_basis_of_cover {ι : Type*}
    (s : Finset ι) (Uc : ι → Set (Matrix.unitaryGroup (Fin d) ℂ))
    (K : Set (Matrix.unitaryGroup (Fin d) ℂ))
    (e : Fin N → (Fin d → ℂ)) (target : ℝ)
    (hcover : ∀ U ∈ K, ∃ j ∈ s, U ∈ Uc j) (ε : ι → ℝ)
    (hbound : ∀ j ∈ s, ∀ U ∈ Uc j, ε j ≤ basisCurvatureMass e target U)
    (hpos : ∀ j ∈ s, 0 < ε j)
    (hK : ∀ U, (∀ j i, ‖overlap e U i j‖ ^ 2 = target) → U ∈ K) :
    ¬ ∃ U : Matrix.unitaryGroup (Fin d) ℂ, ∀ j i, ‖overlap e U i j‖ ^ 2 = target := by
  rintro ⟨U, hMU⟩
  exact no_fourth_basis_in_cover s Uc K e target hcover ε hbound hpos U (hK U hMU) hMU

/-- **The cover ⟹ `Ψ_basis > 0` bridge.** With `target = 1/d`, a certified cover of a set `K`
containing every fourth MU basis forces the basis-level obstruction strictly positive — exactly
the no-fourth-basis conclusion, via `Psi_basis_pos_iff_no_fourth_basis`. This is the basis-level
counterpart of `FiniteVectorCover.no_fourth_mu_vector_T0_of_cover`, and a completed cover makes
it self-contained (each `ε_j` is an exact bound the cover computes — no external `W`). -/
theorem psi_basis_pos_of_cover {ι : Type*}
    (s : Finset ι) (Uc : ι → Set (Matrix.unitaryGroup (Fin d) ℂ))
    (K : Set (Matrix.unitaryGroup (Fin d) ℂ))
    (e : Fin N → (Fin d → ℂ))
    (hcover : ∀ U ∈ K, ∃ j ∈ s, U ∈ Uc j) (ε : ι → ℝ)
    (hbound : ∀ j ∈ s, ∀ U ∈ Uc j, ε j ≤ basisCurvatureMass e (1 / (d : ℝ)) U)
    (hpos : ∀ j ∈ s, 0 < ε j)
    (hK : ∀ U, (∀ j i, ‖overlap e U i j‖ ^ 2 = 1 / (d : ℝ)) → U ∈ K) :
    0 < (Psi_basis e).phi := by
  rw [Psi_basis_pos_iff_no_fourth_basis]
  exact no_fourth_basis_of_cover s Uc K e (1 / (d : ℝ)) hcover ε hbound hpos hK

/-! ### The d = 6 instance (the canonical-triple problem) -/

/-- **d=6 — the wired basis-level no-go for the canonical triple `T0`.** Given a certified cover
(the Rust basis-cover driver's output: patches `s`/`Uc`, exact per-patch lower bounds
`ε ≤ ∑_j∑_i (‖overlap e U i j‖² − 1/6)²`, covering a set `K` containing every fourth MU basis),
the basis-level obstruction for `T0`'s 18 fixed vectors is strictly positive — no fourth MU
basis extends `T0`. -/
theorem psi_basis_pos_T0_of_cover {ι : Type*}
    (s : Finset ι) (Uc : ι → Set (Matrix.unitaryGroup (Fin 6) ℂ))
    (K : Set (Matrix.unitaryGroup (Fin 6) ℂ))
    (e : Fin 18 → (Fin 6 → ℂ))
    (hcover : ∀ U ∈ K, ∃ j ∈ s, U ∈ Uc j) (ε : ι → ℝ)
    (hbound : ∀ j ∈ s, ∀ U ∈ Uc j, ε j ≤ basisCurvatureMass e (1 / (6 : ℝ)) U)
    (hpos : ∀ j ∈ s, 0 < ε j)
    (hK : ∀ U, (∀ j i, ‖overlap e U i j‖ ^ 2 = 1 / (6 : ℝ)) → U ∈ K) :
    0 < (Psi_basis e).phi :=
  psi_basis_pos_of_cover s Uc K e hcover ε hbound hpos hK

/-- A minimal end-to-end sanity instance: a single patch `Uc = K = univ`, certified with bound
`ε = 1` over a `target = 0` set, rules out the (here vacuous) all-columns condition
`‖overlap e U i j‖² = 0` whenever the basis mass is forced `≥ 1`. Exhibits the basis-level
bridge firing without any external hypothesis. -/
theorem single_patch_basis_cover_fires {d : ℕ} (e : Fin 1 → (Fin d → ℂ))
    (hmass : ∀ U : Matrix.unitaryGroup (Fin d) ℂ, (1 : ℝ) ≤ basisCurvatureMass e 0 U) :
    ¬ ∃ U : Matrix.unitaryGroup (Fin d) ℂ, ∀ j i, ‖overlap e U i j‖ ^ 2 = 0 :=
  no_fourth_basis_of_cover ({0} : Finset (Fin 1)) (fun _ => Set.univ) Set.univ e 0
    (fun U _ => ⟨0, Finset.mem_singleton_self 0, Set.mem_univ U⟩)
    (fun _ => 1) (fun _ _ U _ => hmass U) (fun _ _ => one_pos)
    (fun U _ => Set.mem_univ U)

/-! ### The vector ⟹ basis bridge, and the basis-level no-go over a family of triples -/

/-- **The vector ⟹ basis bridge.** If **no vector** `w` is mutually unbiased to the fixed set
`e` (`‖∑ₖ conj(eᵢ ₖ)·wₖ‖² = target` for all `i`), then **no fourth MU basis** extends `e`: a
candidate unitary's first column would be such a vector. This is the load-bearing fact that
the *weaker* basis-level no-go (`MUB(6) ≤ 3`) follows from the *stronger* vector-level no-go —
exactly the per-column reduction (`Ψ_basis ≥ d·Φ₁`), here at the level of existence. -/
theorem no_fourth_basis_of_no_mu_vector [NeZero d] (e : Fin N → (Fin d → ℂ)) (target : ℝ)
    (hv : ¬ ∃ w : Fin d → ℂ, ∀ i, ‖∑ k, (starRingEnd ℂ) (e i k) * w k‖ ^ 2 = target) :
    ¬ ∃ U : Matrix.unitaryGroup (Fin d) ℂ, ∀ j i, ‖overlap e U i j‖ ^ 2 = target := by
  rintro ⟨U, hU⟩
  exact hv ⟨fun k => (U : Matrix (Fin d) (Fin d) ℂ) k 0, fun i => hU 0 i⟩

/-- **`Ψ_basis > 0` from no MU vector.** With `target = 1/d`, the bridge gives the basis-level
obstruction strictly positive — no fourth MU basis extends `e`. This is what turns the
*vector-level* moduli no-go (`MUB.FiniteVectorCover.no_mu_vector_of_family_cover`) into a
*basis-level* one without any new cover: the cover that already rules out a fourth MU **vector**
a fortiori rules out a fourth MU **basis**. -/
theorem psi_basis_pos_of_no_mu_vector [NeZero d] (e : Fin N → (Fin d → ℂ))
    (hv : ¬ ∃ w : Fin d → ℂ, ∀ i, ‖∑ k, (starRingEnd ℂ) (e i k) * w k‖ ^ 2 = 1 / (d : ℝ)) :
    0 < (Psi_basis e).phi := by
  rw [Psi_basis_pos_iff_no_fourth_basis]
  exact no_fourth_basis_of_no_mu_vector e (1 / (d : ℝ)) hv

/-- **Basis-level no-go over a continuous family of triples (the true all-triples object).**
Given that no vector is mutually unbiased to any configuration `e` in a family `E` (the
conclusion of the `omega_mub` moduli cover, `run_moduli_cover` / ENC-1150), the basis-level
obstruction is strictly positive on **every** `e ∈ E`: no fourth MU **basis** extends any triple
in the family. `MUB(6) ≤ 3` is exactly this basis-level statement, so `Ψ_basis` is the correct
object; the vector route certifies it on the `δ`-neighborhood of `T0` where a fourth MU vector
is already excluded. -/
theorem psi_basis_pos_over_family_of_no_mu_vector [NeZero d] (Efam : Set (Fin N → (Fin d → ℂ)))
    (hv : ∀ e ∈ Efam, ¬ ∃ w : Fin d → ℂ,
        ∀ i, ‖∑ k, (starRingEnd ℂ) (e i k) * w k‖ ^ 2 = 1 / (d : ℝ)) :
    ∀ e ∈ Efam, 0 < (Psi_basis e).phi :=
  fun e he => psi_basis_pos_of_no_mu_vector e (hv e he)

/-- **Direct basis-level family cover.** The basis-level analog of
`MUB.FiniteVectorCover.no_mu_vector_of_family_cover`: a single certified cover of the
candidate-basis space whose per-patch bound `ε_j ≤ Ψ^sq(e, ·)` holds **uniformly over every
`e ∈ E`** forces `Ψ_basis(e) > 0` on the whole family. This is the consume-target for a
*basis-level* moduli cover (`mub6_basis_cover` over a widened `BoxedTriple`). -/
theorem psi_basis_pos_over_family {ι : Type*} (s : Finset ι)
    (Uc : ι → Set (Matrix.unitaryGroup (Fin d) ℂ))
    (K : Set (Matrix.unitaryGroup (Fin d) ℂ))
    (Efam : Set (Fin N → (Fin d → ℂ)))
    (hcover : ∀ U ∈ K, ∃ j ∈ s, U ∈ Uc j) (ε : ι → ℝ)
    (hbound : ∀ e ∈ Efam, ∀ j ∈ s, ∀ U ∈ Uc j, ε j ≤ basisCurvatureMass e (1 / (d : ℝ)) U)
    (hpos : ∀ j ∈ s, 0 < ε j)
    (hK : ∀ e ∈ Efam, ∀ U, (∀ j i, ‖overlap e U i j‖ ^ 2 = 1 / (d : ℝ)) → U ∈ K) :
    ∀ e ∈ Efam, 0 < (Psi_basis e).phi :=
  fun e he => psi_basis_pos_of_cover s Uc K e hcover ε (hbound e he) hpos (hK e he)

end FiniteBasisCover
end MUB

-- Axiom hygiene: the basis-level wiring must rest only on the standard kernel axioms.
#print axioms MUB.FiniteBasisCover.basisCurvatureMass_eq_zero_iff
#print axioms MUB.FiniteBasisCover.no_fourth_basis_in_cover
#print axioms MUB.FiniteBasisCover.no_fourth_basis_of_cover
#print axioms MUB.FiniteBasisCover.psi_basis_pos_of_cover
#print axioms MUB.FiniteBasisCover.psi_basis_pos_T0_of_cover
#print axioms MUB.FiniteBasisCover.single_patch_basis_cover_fires
#print axioms MUB.FiniteBasisCover.no_fourth_basis_of_no_mu_vector
#print axioms MUB.FiniteBasisCover.psi_basis_pos_of_no_mu_vector
#print axioms MUB.FiniteBasisCover.psi_basis_pos_over_family_of_no_mu_vector
#print axioms MUB.FiniteBasisCover.psi_basis_pos_over_family
