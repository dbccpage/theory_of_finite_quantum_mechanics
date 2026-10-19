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
# Wiring the exact interval cover into the MUB(6) no-go

This module is the **Lean consume-target** for the `omega_mub` exact interval
finite-cover engine (`crates/omega_mub/src/omega_native/mub6_cover.rs`,
`mub6_cyclotomic_enclosure.rs`, `mub6_interval_cover.rs`). The Rust side certifies,
*per box and in exact rational arithmetic*, a positive lower bound
`ε_j ≤ ∑_i (‖⟪e_i, v⟫‖² − target)²` over a patch `U_j` of candidate vectors. This
module turns a finite family of such certified patches that **covers** the
candidate set into the mechanized conclusion *no vector is mutually unbiased to the
fixed set `e`* — hence no fourth MU basis extends the canonical triple `T0`.

The bridge is the already-proved `finite_cover_no_feasible` (ENC-1133): a finite
cover with per-patch certified positive lower bounds forces the obstruction to be
positive on the whole set. The obstruction here is the ℓ² curvature mass
`Φ(v) = ∑_i (‖⟪e_i, v⟫‖² − target)²`, which vanishes *exactly* at mutually-unbiased
vectors. So a complete certified cover with `Φ > 0` on every patch leaves no room
for a mutually-unbiased vector.

**Independent of the friend's wall.** Unlike `no_fourth_mu_vector_T0` (conditional
on the cited Invariant-Systems bound `max f = W`), this route supplies its *own*
positivity: each `ε_j` is an exact lower bound the cover computes. A completed cover
is therefore a self-contained, machine-checkable proof of the vector-level no-go.

**What remains the computation (the "run it on big compute" part).** The two data
inputs — the finite patch family `(s, U)` and the per-patch exact bounds `ε` with
`ε_j ≤ Φ` on `U_j` (`hbound`), plus that the patches *cover* the candidate set
(`hcover`) — are exactly what a completed run of the Rust driver produces. This
module mechanizes the *logic* that assembles them into the theorem; producing a
cover of the entire (compact) candidate torus is the finite computation. Firewall:
this proves a *vector-level* no-go for a *fixed* triple; it is not `MUB(6) ≤ 3`.
-/

namespace MUB
namespace FiniteVectorCover

open scoped InnerProductSpace
open MUB.ExtensionCurvatureObstruction

variable {N : ℕ} {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℂ E]

/-- The ℓ² curvature mass against a fixed set `e` with unbiasedness target `target`:
`Φ(v) = ∑_i (‖⟪e_i, v⟫‖² − target)²`. This is exactly the quantity the Rust cover
lower-bounds per box (`EnclosedTriple::residual_sq_lower`). -/
noncomputable def curvatureMass (e : Fin N → E) (target : ℝ) (v : E) : ℝ :=
  ∑ i, (‖⟪e i, v⟫_ℂ‖ ^ 2 - target) ^ 2

theorem curvatureMass_nonneg (e : Fin N → E) (target : ℝ) (v : E) :
    0 ≤ curvatureMass e target v :=
  Finset.sum_nonneg fun _ _ => sq_nonneg _

/-- The curvature mass vanishes **iff** `v` is mutually unbiased to `e`
(`‖⟪e_i, v⟫‖² = target` for every `i`). This is the definiteness that turns
`Φ > 0` into "no MU vector". -/
theorem curvatureMass_eq_zero_iff (e : Fin N → E) (target : ℝ) (v : E) :
    curvatureMass e target v = 0 ↔ ∀ i, ‖⟪e i, v⟫_ℂ‖ ^ 2 = target := by
  unfold curvatureMass
  rw [Finset.sum_eq_zero_iff_of_nonneg fun i _ => sq_nonneg _]
  constructor
  · intro h i
    have hz : ‖⟪e i, v⟫_ℂ‖ ^ 2 - target = 0 :=
      sq_eq_zero_iff.mp (h i (Finset.mem_univ i))
    exact sub_eq_zero.mp hz
  · intro h i _
    simp [h i]

/-- **The cover no-go on the candidate set `K`.** Given a finite family of patches
`U_j` (`j ∈ s`) that covers `K`, each carrying a certified positive lower bound
`ε_j ≤ Φ` on it, no member of `K` is mutually unbiased to `e`. The hypotheses are
precisely the output of a completed Rust cover run. -/
theorem no_mu_vector_in_cover {ι : Type*} (s : Finset ι) (U : ι → Set E)
    (K : Set E) (e : Fin N → E) (target : ℝ)
    (hcover : ∀ v ∈ K, ∃ j ∈ s, v ∈ U j) (ε : ι → ℝ)
    (hbound : ∀ j ∈ s, ∀ v ∈ U j, ε j ≤ curvatureMass e target v)
    (hpos : ∀ j ∈ s, 0 < ε j) :
    ∀ v ∈ K, ¬ ∀ i, ‖⟪e i, v⟫_ℂ‖ ^ 2 = target := by
  intro v hv hMU
  have hPhi : 0 < curvatureMass e target v :=
    finite_cover_no_feasible s U (curvatureMass e target) K hcover ε hbound hpos v hv
  rw [(curvatureMass_eq_zero_iff e target v).mpr hMU] at hPhi
  exact lt_irrefl 0 hPhi

/-- **No mutually-unbiased vector exists at all**, given a certified cover of a
candidate set `K` that contains every mutually-unbiased vector. The containment
`hK` is the B1-unbiased reduction: any vector MU to `e` is in particular unbiased
to the standard basis among `e`, so it lies on the torus `K` the cover tiles. -/
theorem no_mu_vector_of_cover {ι : Type*} (s : Finset ι) (U : ι → Set E)
    (K : Set E) (e : Fin N → E) (target : ℝ)
    (hcover : ∀ v ∈ K, ∃ j ∈ s, v ∈ U j) (ε : ι → ℝ)
    (hbound : ∀ j ∈ s, ∀ v ∈ U j, ε j ≤ curvatureMass e target v)
    (hpos : ∀ j ∈ s, 0 < ε j)
    (hK : ∀ v, (∀ i, ‖⟪e i, v⟫_ℂ‖ ^ 2 = target) → v ∈ K) :
    ¬ ∃ v : E, ∀ i, ‖⟪e i, v⟫_ℂ‖ ^ 2 = target := by
  rintro ⟨v, hMU⟩
  exact no_mu_vector_in_cover s U K e target hcover ε hbound hpos v (hK v hMU) hMU

/-- **d=6 instance — the wired no-go for the canonical triple `T0`.** Given a
certified cover (the Rust driver's output: patches `s`/`U`, exact per-patch lower
bounds `ε ≤ ∑_i(‖⟪e_i,v⟫‖² − 1/6)²`, covering the B1-unbiased candidate set `K`),
no unit vector is mutually unbiased to `T0`'s 18 vectors `e`. A fourth MU basis's
first column would be such a vector, so none extends `T0`. **No `W` is used** — the
cover provides its own positivity. -/
theorem no_fourth_mu_vector_T0_of_cover {ι : Type*} (s : Finset ι) (U : ι → Set E)
    (K : Set E) (e : Fin 18 → E)
    (hcover : ∀ v ∈ K, ∃ j ∈ s, v ∈ U j) (ε : ι → ℝ)
    (hbound : ∀ j ∈ s, ∀ v ∈ U j, ε j ≤ curvatureMass e (1 / 6) v)
    (hpos : ∀ j ∈ s, 0 < ε j)
    (hK : ∀ v, (∀ i, ‖⟪e i, v⟫_ℂ‖ ^ 2 = 1 / 6) → v ∈ K) :
    ¬ ∃ v : E, ∀ i, ‖⟪e i, v⟫_ℂ‖ ^ 2 = 1 / 6 :=
  no_mu_vector_of_cover s U K e (1 / 6) hcover ε hbound hpos hK

/-- A minimal end-to-end sanity instance: a single patch `U = K = univ` certified
with bound `ε = 1` (standing in for the Rust certificate `Φ ≥ 1` on the patch) over
a `target = 0` set rules out the (here vacuous) "MU" condition `‖⟪e_i,v⟫‖² = 0`
whenever some coordinate mass is forced to be ≥ 1. Exhibits the bridge firing
without any external hypothesis. -/
theorem single_patch_cover_fires {E : Type*} [NormedAddCommGroup E]
    [InnerProductSpace ℂ E] (e : Fin 1 → E)
    (hmass : ∀ v : E, (1 : ℝ) ≤ curvatureMass e 0 v) :
    ¬ ∃ v : E, ∀ i, ‖⟪e i, v⟫_ℂ‖ ^ 2 = 0 :=
  no_mu_vector_of_cover ({0} : Finset (Fin 1)) (fun _ => Set.univ) Set.univ e 0
    (fun v _ => ⟨0, Finset.mem_singleton_self 0, Set.mem_univ v⟩)
    (fun _ => 1) (fun _ _ v _ => hmass v) (fun _ _ => one_pos)
    (fun v _ => Set.mem_univ v)

/-! ### The moduli family no-go (cover over a continuous family of triples) -/

/-- **The family cover no-go.** Let `Efam` be a *family* of fixed-vector configurations
(a continuous neighborhood of `T0` in the moduli of triples). If a single finite patch
family covers the candidate set `K` and each patch carries a certified positive lower
bound `ε_j ≤ Φ(e, ·)` that holds **uniformly over every `e ∈ Efam`** (`hbound`), then no
configuration in the family admits a mutually-unbiased vector in `K`. This is the Lean
consume-target for the `omega_mub` **moduli** cover (`run_moduli_cover`): widening the
fixed vectors by `δ` makes the per-box interval bound hold for every triple in the
`δ`-box at once, which is exactly the uniform `hbound`. -/
theorem no_mu_vector_in_family_cover {ι : Type*} (s : Finset ι) (U : ι → Set E)
    (K : Set E) (Efam : Set (Fin N → E)) (target : ℝ)
    (hcover : ∀ v ∈ K, ∃ j ∈ s, v ∈ U j) (ε : ι → ℝ)
    (hbound : ∀ e ∈ Efam, ∀ j ∈ s, ∀ v ∈ U j, ε j ≤ curvatureMass e target v)
    (hpos : ∀ j ∈ s, 0 < ε j) :
    ∀ e ∈ Efam, ∀ v ∈ K, ¬ ∀ i, ‖⟪e i, v⟫_ℂ‖ ^ 2 = target :=
  fun e he => no_mu_vector_in_cover s U K e target hcover ε (hbound e he) hpos

/-- **No mutually-unbiased vector for any configuration in the family**, given that `K`
contains every MU vector of every `e ∈ Efam`. A *single* certified cover (uniform over the
family) thus rules out a fourth MU vector for an entire continuous neighborhood of `T0`,
not just the point `T0`. -/
theorem no_mu_vector_of_family_cover {ι : Type*} (s : Finset ι) (U : ι → Set E)
    (K : Set E) (Efam : Set (Fin N → E)) (target : ℝ)
    (hcover : ∀ v ∈ K, ∃ j ∈ s, v ∈ U j) (ε : ι → ℝ)
    (hbound : ∀ e ∈ Efam, ∀ j ∈ s, ∀ v ∈ U j, ε j ≤ curvatureMass e target v)
    (hpos : ∀ j ∈ s, 0 < ε j)
    (hK : ∀ e ∈ Efam, ∀ v, (∀ i, ‖⟪e i, v⟫_ℂ‖ ^ 2 = target) → v ∈ K) :
    ∀ e ∈ Efam, ¬ ∃ v : E, ∀ i, ‖⟪e i, v⟫_ℂ‖ ^ 2 = target :=
  fun e he => no_mu_vector_of_cover s U K e target hcover ε (hbound e he) hpos (hK e he)

end FiniteVectorCover
end MUB

-- Axiom hygiene: the wiring must rest only on the standard kernel axioms.
#print axioms MUB.FiniteVectorCover.curvatureMass_eq_zero_iff
#print axioms MUB.FiniteVectorCover.no_mu_vector_in_cover
#print axioms MUB.FiniteVectorCover.no_mu_vector_of_cover
#print axioms MUB.FiniteVectorCover.no_fourth_mu_vector_T0_of_cover
#print axioms MUB.FiniteVectorCover.single_patch_cover_fires
#print axioms MUB.FiniteVectorCover.no_mu_vector_in_family_cover
#print axioms MUB.FiniteVectorCover.no_mu_vector_of_family_cover
