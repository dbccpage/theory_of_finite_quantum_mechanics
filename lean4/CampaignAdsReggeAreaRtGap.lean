import Mathlib.Data.Rat.Defs
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.FieldSimp
import ReggePachnerWdw
import FrontierHappyMincut

/-!
# Campaign: ADS-REGGE-AREA-RT-GAP (TFQ-2211) — Non-Equivalence Fences Between Repository Regge Areas and Minimal-Surface / HaPPY Bond-Cut Areas

AuthorityEffect: None.

This module narrows the explicit gap node `ADS-REGGE-AREA-RT-GAP` (`TFQ-2211`, stage `ADS_CFT`,
status `OPEN`, audited against `TFQ-0100`, `TFQ-0084`, and `arXiv:hep-th/0603001` eq. (1.5)) to
three exact finite/rational non-equivalence fences between the repository's simplicial Regge
squared-area proxy (`code/rust/src/general_relativity/exact_regge/action.rs` and `sphere.rs`),
the continuum Ryu-Takayanagi minimal-surface area term, and the discrete 6-pentagon HaPPY `{5,4}`
bond-cut count (`FrontierHappyMincut.lean`):

1. **Simplicial Hinge Carrier vs. HaPPY Tensor-Network Cut Spectrum Census**:
   - The 4D `orthogonal_pentatope` simplex of `TFQ-0100` (`sphere.rs`) has `5` vertices, `10` edges,
     `10` triangular hinges partitioned into `6` right-triangle hinges (`A_h^2 = 1/4`) and `4`
     equilateral-triangle hinges (`A_h^2 = 3/4`), and `5` tetrahedral facets, while the
     `closed_s4_cube_boundary` Kuhn triangulation of `∂([0,1]^5)` has `10 * 24 = 240` pentatope
     charts (`simplicial_regge_vs_happy_network_carrier_counts`).
   - On the 20-qubit 6-pentagon HaPPY `{5,4}` network (`FrontierHappyMincut`), across all `380`
     proper nonempty contiguous boundary intervals `(start, len)`, the integer bond-cut count
     `intervalMincut start len` takes only values in `{1, 2, 3, 4, 5}` with exact multiplicity
     distribution `(50, 90, 110, 100, 30)` summing to `380` (`happy_mincut_value_distribution_380`).
   - No single rational conversion constant `alpha : ℚ` can map both hinge squared-area classes
     (`1/4` and `3/4`) of `orthogonal_pentatope` to the HaPPY unit bond weight `1`
     (`no_uniform_hinge_to_bond_unit_dictionary`).

2. **Subdivision Collapse of Squared Hinge Areas vs. Subdivision Invariance of Linear Areas**:
   - If a planar surface element of linear area `A` is subdivided into `m` congruent sub-triangles
     of linear area `A / m` each, the linear area sum `m * (A / m) = A` is invariant for all `m ≠ 0`
     (`linear_area_subdivision_invariant`), whereas the squared-area sum `m * (A / m)^2 = A^2 / m`
     scales as `1 / m` (`sq_area_subdivision_scales_inv_m`).
   - The resulting squared-area subdivision defect `A^2 - m * (A / m)^2 = ((m - 1) / m) * A^2`
     (`sq_area_subdivision_defect_formula`) is strictly positive for every `m > 1` and `A ≠ 0`
     (`sq_area_subdivision_defect_pos`), so minimizing unregularized squared hinge areas under
     refinement collapses toward `0`, unlike linear minimal-surface area or discrete bond counts
     (`midpoint_and_barycentric_subdivision_witnesses`).

3. **Holonomy-Defect Weighting (`κ_h`) Decoupling from Topological Bond Cuts (`TFQ-0084`, `TFQ-0100`)**:
   - Importing `ReggePachnerWdw`, a flat simplicial vertex (`isFlatVertex v`) has zero Wheeler-DeWitt
     defect sum `evaluateH_Wdw v = 0` while any positive bone defect `d > 0` forces `sumDeficits > 0`
     (`regge_wdw_flat_vs_curved_dichotomy`).
   - In the `TFQ-0100` rational Regge proxy `uniformDefectReggeAction totalAreaSq kappa = totalAreaSq * kappa`,
     varying the uniform holonomy defect `kappa` on the fixed `orthogonal_pentatope` geometry
     (`totalAreaSq = 9 / 2`) scales the proxy linearly in `kappa` (`0` at `kappa = 0`, `9 / 2` at
     `kappa = 1`, `9` at `kappa = 2`) without altering the combinatorial complex, whereas on the
     fixed 6-pentagon HaPPY network `intervalMincut 0 len` varies across `(1, 2, 3, 4, 5)` purely
     as a function of the boundary subregion (`regge_curvature_variation_vs_happy_subregion_variation`).
-/

namespace CampaignAdsReggeAreaRtGap

open ReggePachnerWdw
open FrontierHappyMincut

-- ============================================================================
-- 1. Simplicial Hinge Carrier vs. HaPPY Tensor-Network Cut Spectrum Census
-- ============================================================================

/-- Number of vertices, edges, triangular hinges, and tetrahedral facets of a 4-simplex `Δ^4`
(`orthogonal_pentatope` in `code/rust/src/general_relativity/exact_regge/sphere.rs`). -/
def pentatopeVertexCount : Nat := 5
def pentatopeEdgeCount : Nat := 10
def pentatopeHingeCount : Nat := 10
def pentatopeRightHingeCount : Nat := 6
def pentatopeEquilateralHingeCount : Nat := 4
def pentatopeFacetCount : Nat := 5

/-- Number of pentatope charts in `closed_s4_cube_boundary` (`10` hypercube facets × `4! = 24`
Kuhn simplices per facet = `240` charts in `sphere.rs`). -/
def s4CubeBoundaryPentatopeCount : Nat := 10 * 24

/-- Combinatorial counts of the 6-pentagon HaPPY `{5,4}` star patch (`FrontierHappyMincut.lean`):
`6` six-leg perfect tensors (`1` central + `5` outer), `5` internal bulk bonds, `20` boundary legs,
and `380` proper nonempty contiguous boundary intervals. -/
def happyTensorCount : Nat := 6
def happyInternalBondCount : Nat := 5
def happyBoundaryLegCount : Nat := 20
def happyProperIntervalCount : Nat := 380

set_option maxRecDepth 20000 in
/-- Theorem 1: Exact combinatorial carrier counts of the 4D simplicial Regge complex (`TFQ-0100`)
versus the 6-pentagon HaPPY `{5,4}` tensor network (`TFQ-2209`). -/
theorem simplicial_regge_vs_happy_network_carrier_counts :
    pentatopeRightHingeCount + pentatopeEquilateralHingeCount = pentatopeHingeCount ∧
    pentatopeVertexCount + pentatopeHingeCount = pentatopeEdgeCount + pentatopeFacetCount ∧
    s4CubeBoundaryPentatopeCount = 240 ∧
    happyInternalBondCount + happyBoundaryLegCount = 25 ∧
    allIntervals380.length = happyProperIntervalCount := by
  decide

/-- Count how many of the `380` proper contiguous boundary intervals `(start, len)` on the
20-qubit 6-pentagon HaPPY patch have `intervalMincut start len = k`. -/
def countIntervalsWithMincut (k : Nat) : Nat :=
  (allIntervals380.filter fun (s, l) => intervalMincut s l == k).length

set_option maxRecDepth 20000 in
set_option maxHeartbeats 800000 in
/-- Theorem 2: Complete value census of `intervalMincut` across all `380` proper nonempty
contiguous boundary intervals on the 20-qubit 6-pentagon HaPPY patch:
`intervalMincut` takes only values in `{1, 2, 3, 4, 5}`, with exact multiplicities
`(50, 90, 110, 100, 30)` summing to `380`. -/
theorem happy_mincut_value_distribution_380 :
    countIntervalsWithMincut 1 = 50 ∧
    countIntervalsWithMincut 2 = 90 ∧
    countIntervalsWithMincut 3 = 110 ∧
    countIntervalsWithMincut 4 = 100 ∧
    countIntervalsWithMincut 5 = 30 ∧
    countIntervalsWithMincut 1 + countIntervalsWithMincut 2 +
      countIntervalsWithMincut 3 + countIntervalsWithMincut 4 +
      countIntervalsWithMincut 5 = 380 ∧
    (allIntervals380.all fun (s, l) =>
      decide (1 ≤ intervalMincut s l ∧ intervalMincut s l ≤ 5)) = true := by
  decide

/-- Squared hinge areas of the two triangle classes in `orthogonal_pentatope` (`sphere.rs`):
`1 / 4` for the 6 right triangles and `3 / 4` for the 4 equilateral triangles. -/
def rightHingeAreaSq : ℚ := 1 / 4
def equilateralHingeAreaSq : ℚ := 3 / 4
def pentatopeTotalAreaSq : ℚ :=
  6 * rightHingeAreaSq + 4 * equilateralHingeAreaSq

/-- Theorem 3: No single rational dictionary constant `alpha : ℚ` can map both hinge squared-area
classes (`1 / 4` and `3 / 4`) of `orthogonal_pentatope` to the HaPPY unit bond weight `1` (`1` bit
per cut bond), and normalizing `alpha * rightHingeAreaSq = 1` forces `alpha = 4`,
`alpha * equilateralHingeAreaSq = 3`, and `alpha * pentatopeTotalAreaSq = 18`. -/
theorem no_uniform_hinge_to_bond_unit_dictionary :
    (∀ alpha : ℚ, ¬ (alpha * rightHingeAreaSq = 1 ∧ alpha * equilateralHingeAreaSq = 1)) ∧
    (4 : ℚ) * rightHingeAreaSq = 1 ∧
    (4 : ℚ) * equilateralHingeAreaSq = 3 ∧
    (4 : ℚ) * pentatopeTotalAreaSq = 18 := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro alpha ⟨h1, h2⟩
    dsimp [rightHingeAreaSq, equilateralHingeAreaSq] at h1 h2
    linarith
  · dsimp [rightHingeAreaSq]; norm_num
  · dsimp [equilateralHingeAreaSq]; norm_num
  · dsimp [pentatopeTotalAreaSq, rightHingeAreaSq, equilateralHingeAreaSq]; norm_num

-- ============================================================================
-- 2. Subdivision Collapse of Squared Hinge Areas vs. Linear Minimal-Surface Area
-- ============================================================================

/-- Sum of linear areas when a surface of area `A` is subdivided into `m` equal sub-hinges of
area `A / m`. -/
def linearAreaSubdivisionSum (A m : ℚ) : ℚ :=
  m * (A / m)

/-- Sum of squared areas when a surface of area `A` is subdivided into `m` equal sub-hinges of
linear area `A / m` (squared area `(A / m)^2`). -/
def sqAreaSubdivisionSum (A m : ℚ) : ℚ :=
  m * (A / m) ^ 2

/-- Subdivision defect `A^2 - m * (A / m)^2` between the un-subdivided squared area `A^2` and the
sum of squared areas of `m` equal sub-hinges. -/
def sqAreaSubdivisionDefect (A m : ℚ) : ℚ :=
  A ^ 2 - sqAreaSubdivisionSum A m

/-- Theorem 4: Linear surface area is invariant under `m`-fold uniform hinge subdivision for every
`m ≠ 0`. -/
theorem linear_area_subdivision_invariant (A m : ℚ) (hm : m ≠ 0) :
    linearAreaSubdivisionSum A m = A := by
  dsimp [linearAreaSubdivisionSum]
  field_simp [hm]

/-- Theorem 5: The squared-area sum `sqAreaSubdivisionSum A m` scales as `A^2 / m` under `m`-fold
uniform hinge subdivision. -/
theorem sq_area_subdivision_scales_inv_m (A m : ℚ) (hm : m ≠ 0) :
    sqAreaSubdivisionSum A m = A ^ 2 / m := by
  dsimp [sqAreaSubdivisionSum]
  field_simp [hm]

/-- Theorem 6: Exact formula `((m - 1) / m) * A^2` for the squared-area subdivision defect. -/
theorem sq_area_subdivision_defect_formula (A m : ℚ) (hm : m ≠ 0) :
    sqAreaSubdivisionDefect A m = ((m - 1) / m) * A ^ 2 := by
  dsimp [sqAreaSubdivisionDefect, sqAreaSubdivisionSum]
  field_simp [hm]

/-- Theorem 7: For every subdivision multiplicity `m > 1` and nonzero linear area `A ≠ 0`, the
squared-area subdivision defect is strictly positive (`0 < sqAreaSubdivisionDefect A m`), so
`sqAreaSubdivisionSum A m < A ^ 2`. -/
theorem sq_area_subdivision_defect_pos (A m : ℚ) (hm : 1 < m) (hA : A ≠ 0) :
    0 < sqAreaSubdivisionDefect A m ∧ sqAreaSubdivisionSum A m < A ^ 2 := by
  have hm0 : (0 : ℚ) < m := by linarith
  have hm_ne : m ≠ 0 := ne_of_gt hm0
  have hA2 : 0 < A ^ 2 := sq_pos_of_ne_zero hA
  have hfrac : 0 < (m - 1) / m := div_pos (by linarith) hm0
  have hpos : 0 < sqAreaSubdivisionDefect A m := by
    rw [sq_area_subdivision_defect_formula A m hm_ne]
    exact mul_pos hfrac hA2
  refine ⟨hpos, ?_⟩
  dsimp [sqAreaSubdivisionDefect] at hpos
  linarith

/-- Theorem 8: Under recursive `4^k` midpoint triangle refinement of a unit-squared-area hinge
(`A^2 = 1`), the squared-area sum at refinement depth `k = 1, 2, 3` drops to `1/4, 1/16, 1/64`,
and for a right-triangle hinge of `orthogonal_pentatope` (`A = 1/2`, `A^2 = 1/4`) midpoint (`m = 4`)
and barycentric (`m = 6`) subdivision reduce the squared-area sum to `1/16` and `1/24`. -/
theorem midpoint_and_barycentric_subdivision_witnesses :
    sqAreaSubdivisionSum 1 4 = 1 / 4 ∧
    sqAreaSubdivisionSum 1 16 = 1 / 16 ∧
    sqAreaSubdivisionSum 1 64 = 1 / 64 ∧
    sqAreaSubdivisionSum (1 / 2) 4 = 1 / 16 ∧
    sqAreaSubdivisionSum (1 / 2) 6 = 1 / 24 ∧
    sqAreaSubdivisionDefect (1 / 2) 4 = 3 / 16 ∧
    sqAreaSubdivisionDefect (1 / 2) 6 = 5 / 24 := by
  dsimp [sqAreaSubdivisionSum, sqAreaSubdivisionDefect]
  norm_num

-- ============================================================================
-- 3. Holonomy-Defect Weighting (`κ_h`) Decoupling from Topological Bond Cuts
-- ============================================================================

/-- Uniform-defect rational Regge action proxy `(∑_h A_h^2) * κ` on a simplicial complex with total
squared hinge area `totalAreaSq` and uniform holonomy defect `kappa`. -/
def uniformDefectReggeAction (totalAreaSq kappa : ℚ) : ℚ :=
  totalAreaSq * kappa

/-- Theorem 9: Importing `ReggePachnerWdw` (`TFQ-0084`), a flat simplicial vertex (`d = 0` on all
incident bones) has `evaluateH_Wdw v = 0`, whereas any incident bone with positive defect `d > 0`
produces `evaluateH_Wdw v > 0`. -/
theorem regge_wdw_flat_vs_curved_dichotomy :
    evaluateH_Wdw ⟨[0, 0, 0, 0]⟩ = 0 ∧
    0 < evaluateH_Wdw ⟨[0, 2, 0, 0]⟩ ∧
    evaluateH_Wdw ⟨[0, 2, 0, 0]⟩ = 2 := by
  refine ⟨?_, ?_, ?_⟩
  · exact flat_vertex_wdw_closure ⟨[0, 0, 0, 0]⟩ (by intro d hd; simp at hd; exact hd)
  · exact curved_pachner_induces_positive_defect [0, 2, 0, 0] 2 (by decide) (by decide)
  · rfl

/-- Theorem 10: On the fixed `orthogonal_pentatope` geometry (`pentatopeTotalAreaSq = 9 / 2`),
varying the holonomy defect `kappa` scales `uniformDefectReggeAction` linearly with `kappa`
(`0`, `9 / 2`, `9` at `kappa = 0, 1, 2`) and satisfies `uniformDefectReggeAction (9/2) k2 -
uniformDefectReggeAction (9/2) k1 = (9/2) * (k2 - k1)`. -/
theorem regge_action_linear_in_holonomy_defect (k1 k2 : ℚ) :
    uniformDefectReggeAction pentatopeTotalAreaSq 0 = 0 ∧
    uniformDefectReggeAction pentatopeTotalAreaSq 1 = 9 / 2 ∧
    uniformDefectReggeAction pentatopeTotalAreaSq 2 = 9 ∧
    uniformDefectReggeAction pentatopeTotalAreaSq k2 -
      uniformDefectReggeAction pentatopeTotalAreaSq k1 = (9 / 2) * (k2 - k1) := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · dsimp [uniformDefectReggeAction, pentatopeTotalAreaSq, rightHingeAreaSq, equilateralHingeAreaSq]
    norm_num
  · dsimp [uniformDefectReggeAction, pentatopeTotalAreaSq, rightHingeAreaSq, equilateralHingeAreaSq]
    norm_num
  · dsimp [uniformDefectReggeAction, pentatopeTotalAreaSq, rightHingeAreaSq, equilateralHingeAreaSq]
    norm_num
  · dsimp [uniformDefectReggeAction, pentatopeTotalAreaSq, rightHingeAreaSq, equilateralHingeAreaSq]
    ring

/-- Theorem 11: On the fixed 6-pentagon HaPPY `{5,4}` network (`FrontierHappyMincut`), varying the
boundary interval length `len ∈ {1, 2, 3, 4, 8}` at `start = 2` varies the minimal bond cut
`intervalMincut 2 len` across the full integer range `(1, 2, 3, 4, 5)` (with `intervalMincut 0 4 = 1`
vs. `intervalMincut 2 4 = 4` for aligned vs. straddling 4-qubit intervals) without any bulk holonomy
defect parameter, while the flat-chart Regge proxy (`kappa = 0`) remains identically `0`. -/
theorem regge_curvature_variation_vs_happy_subregion_variation :
    intervalMincut 2 1 = 1 ∧
    intervalMincut 2 2 = 2 ∧
    intervalMincut 2 3 = 3 ∧
    intervalMincut 2 4 = 4 ∧
    intervalMincut 2 8 = 5 ∧
    intervalMincut 0 4 = 1 ∧
    uniformDefectReggeAction pentatopeTotalAreaSq 0 = 0 := by
  refine ⟨by decide, by decide, by decide, by decide, by decide, by decide, ?_⟩
  dsimp [uniformDefectReggeAction, pentatopeTotalAreaSq, rightHingeAreaSq, equilateralHingeAreaSq]
  norm_num

/-- Theorem 12: No affine function `kappa ↦ a * kappa + b` of a single bulk holonomy defect `kappa`
on a fixed background (`kappa = 0`) can simultaneously reproduce the distinct HaPPY minimal-cut
values `intervalMincut 2 1 = 1` and `intervalMincut 2 2 = 2` at the same background curvature
`kappa = 0`. -/
theorem no_fixed_background_regge_function_matches_all_subregion_cuts (a b : ℚ) :
    ¬ (a * 0 + b = (intervalMincut 2 1 : ℚ) ∧ a * 0 + b = (intervalMincut 2 2 : ℚ)) := by
  have h1 : intervalMincut 2 1 = 1 := by decide
  have h2 : intervalMincut 2 2 = 2 := by decide
  rw [h1, h2]
  rintro ⟨ha1, ha2⟩
  push_cast at ha1 ha2
  linarith

end CampaignAdsReggeAreaRtGap

#print axioms CampaignAdsReggeAreaRtGap.simplicial_regge_vs_happy_network_carrier_counts
#print axioms CampaignAdsReggeAreaRtGap.happy_mincut_value_distribution_380
#print axioms CampaignAdsReggeAreaRtGap.no_uniform_hinge_to_bond_unit_dictionary
#print axioms CampaignAdsReggeAreaRtGap.linear_area_subdivision_invariant
#print axioms CampaignAdsReggeAreaRtGap.sq_area_subdivision_scales_inv_m
#print axioms CampaignAdsReggeAreaRtGap.sq_area_subdivision_defect_formula
#print axioms CampaignAdsReggeAreaRtGap.sq_area_subdivision_defect_pos
#print axioms CampaignAdsReggeAreaRtGap.midpoint_and_barycentric_subdivision_witnesses
#print axioms CampaignAdsReggeAreaRtGap.regge_wdw_flat_vs_curved_dichotomy
#print axioms CampaignAdsReggeAreaRtGap.regge_action_linear_in_holonomy_defect
#print axioms CampaignAdsReggeAreaRtGap.regge_curvature_variation_vs_happy_subregion_variation
#print axioms CampaignAdsReggeAreaRtGap.no_fixed_background_regge_function_matches_all_subregion_cuts

private def l5aProvenance : String :=
  "Origin: lean4/CampaignAdsReggeAreaRtGap.lean Claim: ADS-REGGE-AREA-RT-GAP AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
