import Mathlib
import ExtensionCurvatureObstruction
import FiniteVectorCover

/-!
# Pilot Certificate Verification for MUB(6) Narrow Torus Cell

AuthorityEffect: None.

## Stated-Region Pilot Verification
This module is the Lean consume target for the Rust exact interval pilot artifact
`omega_engine/crates_rs/omega_mub/artifacts/kernel_reflection_pilot_dita_0_8_narrow_cell.json`
(schema version `omega.mub.kernel-reflection-pilot.v1`).

The Rust engine certifies, in exact rational interval arithmetic, a positive lower bound
`min_gap > 0` on the squared curvature mass
`Φ(v) = ∑_i (‖⟪e_i, v⟫‖² − 1/6)²`
over the stated narrow torus cell patch `K_narrow` against the Dita seed `(0, 8)` triple.

Here, Lean 4:
1. Formalizes the pilot certificate metadata and exact rational lower bound.
2. Formally evaluates in exact rational arithmetic that `min_gap > 0`.
3. Wires the certified bound into `MUB.FiniteVectorCover.no_mu_vector_in_cover` and
   `MUB.ExtensionCurvatureObstruction.finite_cover_no_feasible` to establish that no
   vector in the certified narrow torus cell patch is mutually unbiased to the seed triple.

## Scope and Firewall
* **Demonstration on stated region only**: This pilot verifies a single leaf patch (the narrow torus cell).
  It is NOT a check of the full 5-torus moduli space.
  unbiased bases in dimension 6 is 3 or bounded by 3.
* **AuthorityEffect**: None. Mints no authority.
-/

namespace MUB
namespace KernelReflectionPilot

open scoped InnerProductSpace
open MUB.ExtensionCurvatureObstruction
open MUB.FiniteVectorCover

/-- Schema version tag matching `kernel_reflection_pilot_dita_0_8_narrow_cell.json`. -/
def pilot_schema_version : String := "omega.mub.kernel-reflection-pilot.v1"

/-- Dita seed index dx = 0. -/
def seed_dx : ℤ := 0

/-- Dita seed index dy = 8. -/
def seed_dy : ℤ := 8

/-- Stated region description from the pilot JSON artifact. -/
def pilot_region_desc : String := "narrow_torus_cell (stated region; not full 5-torus)"

/-- Exact integer numerator of the certified minimum gap. -/
def pilot_min_gap_num : ℤ := 1767254173955314751271193592806205971432363044041390940254075465254451

/-- Exact natural number denominator of the certified minimum gap. -/
def pilot_min_gap_den : ℕ := 2711707949687046089977061030825711891756217552008462909571072000000000

/-- The exact certified minimum gap as a rational number `ℚ`. -/
def pilot_min_gap_rat : ℚ :=
  (1767254173955314751271193592806205971432363044041390940254075465254451 : ℚ) /
  (2711707949687046089977061030825711891756217552008462909571072000000000 : ℚ)

/-- The certified minimum gap coerced to `ℝ`. -/
noncomputable def pilot_min_gap_real : ℝ := (pilot_min_gap_rat : ℝ)

/-- Exact rational arithmetic verification: the certified minimum gap is strictly positive in `ℚ`. -/
theorem pilot_min_gap_rat_pos : 0 < pilot_min_gap_rat := by
  unfold pilot_min_gap_rat
  norm_num

/-- The certified minimum gap is strictly positive in `ℝ`. -/
theorem pilot_min_gap_real_pos : 0 < pilot_min_gap_real := by
  unfold pilot_min_gap_real pilot_min_gap_rat
  norm_num

/-- Formal Lean 4 reflection of the Rust `KernelReflectionPilot` certificate schema
    `omega.mub.kernel-reflection-pilot.v1` for the stated narrow torus cell region. -/
structure NarrowCellPilotCertificate {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℂ E]
    (e : Fin 18 → E) (K_narrow : Set E) where
  schema_version : String := pilot_schema_version
  seed_dx : ℤ := seed_dx
  seed_dy : ℤ := seed_dy
  region_desc : String := pilot_region_desc
  certified_count : ℕ := 1
  off_torus_count : ℕ := 0
  uncertified_count : ℕ := 0
  complete_flag : Bool := true
  bound_certified : ∀ v ∈ K_narrow, pilot_min_gap_real ≤ curvatureMass e (1 / 6) v

/-- **Obstruction positivity on the narrow cell patch.**
    Witnessed via `MUB.ExtensionCurvatureObstruction.finite_cover_no_feasible`:
    the certified positive lower bound forces the curvature mass `Φ` to be strictly positive
    on all vectors in the narrow torus cell patch `K_narrow`. -/
theorem narrow_cell_pilot_curvature_mass_pos {E : Type*} [NormedAddCommGroup E]
    [InnerProductSpace ℂ E] (e : Fin 18 → E) (K_narrow : Set E)
    (cert : NarrowCellPilotCertificate e K_narrow) :
    ∀ v ∈ K_narrow, 0 < curvatureMass e (1 / 6) v := by
  intro v hv
  have hcover : ∀ w ∈ K_narrow, ∃ j ∈ ({0} : Finset (Fin 1)), w ∈ (fun _ => K_narrow) j :=
    fun w hw => ⟨0, Finset.mem_singleton_self 0, hw⟩
  have hbound : ∀ j ∈ ({0} : Finset (Fin 1)), ∀ w ∈ (fun _ => K_narrow) j,
      (fun _ => pilot_min_gap_real) j ≤ curvatureMass e (1 / 6) w :=
    fun j _ w hw => cert.bound_certified w hw
  have hpos : ∀ j ∈ ({0} : Finset (Fin 1)), 0 < (fun _ => pilot_min_gap_real) j :=
    fun _ _ => pilot_min_gap_real_pos
  exact finite_cover_no_feasible ({0} : Finset (Fin 1)) (fun _ => K_narrow)
    (curvatureMass e (1 / 6)) K_narrow hcover (fun _ => pilot_min_gap_real) hbound hpos v hv

/-- **Narrow cell pilot no-go for candidate vectors.**
    Witnessed via `MUB.FiniteVectorCover.no_mu_vector_in_cover`:
    no vector in the certified narrow torus cell patch is mutually unbiased to the seed triple `e`.
    This is the primary consumption target for `kernel_reflection_pilot_dita_0_8_narrow_cell.json`. -/
theorem narrow_cell_pilot_no_mu_vector {E : Type*} [NormedAddCommGroup E]
    [InnerProductSpace ℂ E] (e : Fin 18 → E) (K_narrow : Set E)
    (cert : NarrowCellPilotCertificate e K_narrow) :
    ∀ v ∈ K_narrow, ¬ ∀ i, ‖⟪e i, v⟫_ℂ‖ ^ 2 = 1 / 6 := by
  have hcover : ∀ w ∈ K_narrow, ∃ j ∈ ({0} : Finset (Fin 1)), w ∈ (fun _ => K_narrow) j :=
    fun w hw => ⟨0, Finset.mem_singleton_self 0, hw⟩
  have hbound : ∀ j ∈ ({0} : Finset (Fin 1)), ∀ w ∈ (fun _ => K_narrow) j,
      (fun _ => pilot_min_gap_real) j ≤ curvatureMass e (1 / 6) w :=
    fun j _ w hw => cert.bound_certified w hw
  have hpos : ∀ j ∈ ({0} : Finset (Fin 1)), 0 < (fun _ => pilot_min_gap_real) j :=
    fun _ _ => pilot_min_gap_real_pos
  exact no_mu_vector_in_cover ({0} : Finset (Fin 1)) (fun _ => K_narrow)
    K_narrow e (1 / 6) hcover (fun _ => pilot_min_gap_real) hbound hpos

/-- Direct derivation of the pilot vector no-go combining
    `narrow_cell_pilot_curvature_mass_pos` and `curvatureMass_eq_zero_iff`. -/
theorem narrow_cell_pilot_no_mu_vector_alt {E : Type*} [NormedAddCommGroup E]
    [InnerProductSpace ℂ E] (e : Fin 18 → E) (K_narrow : Set E)
    (cert : NarrowCellPilotCertificate e K_narrow) :
    ∀ v ∈ K_narrow, ¬ ∀ i, ‖⟪e i, v⟫_ℂ‖ ^ 2 = 1 / 6 := by
  intro v hv hMU
  have hpos : 0 < curvatureMass e (1 / 6) v :=
    narrow_cell_pilot_curvature_mass_pos e K_narrow cert v hv
  rw [(curvatureMass_eq_zero_iff e (1 / 6) v).mpr hMU] at hpos
  exact lt_irrefl 0 hpos

end KernelReflectionPilot
end MUB

#print axioms MUB.KernelReflectionPilot.pilot_min_gap_rat_pos
#print axioms MUB.KernelReflectionPilot.pilot_min_gap_real_pos
#print axioms MUB.KernelReflectionPilot.narrow_cell_pilot_curvature_mass_pos
#print axioms MUB.KernelReflectionPilot.narrow_cell_pilot_no_mu_vector
#print axioms MUB.KernelReflectionPilot.narrow_cell_pilot_no_mu_vector_alt
