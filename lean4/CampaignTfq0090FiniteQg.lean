import Mathlib.Data.Rat.Defs
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.FieldSimp

/-!
# Campaign Formalization: `TFQ-0090` (`FINITE_QG`)
## `OBL-R03` Cochain Curvature vs. Regge Deficit Split and `OBL-R01` Continuum Scaling Fence

This module formalizes the exact finite/algebraic counterpart and non-equivalence scope fences for
DAG node `TFQ-0090` (`GAP: OBL-R03 leaves Regge deficit uncoupled from cochain curvature; OBL-R01
leaves the continuum scaling gap open`):

1. **Finite Comparison Complex & Gauge-Invariant Cochain Curvature (`d_1 = ∂_2^T`, `d_1 ∘ d_0 = 0`)**:
   - On the 4-vertex tetrahedral comparison 2-complex `K_4^{(2)}` (`4` vertices, `6` oriented edges
     `e01, e02, e03, e12, e13, e23`, and `4` oriented faces `f012, f013, f023, f123`), a 0-cochain
     `(p0, p1, p2, p3)` induces the coboundary 1-cochain `d_0` and a 1-cochain induces the face
     holonomy / cochain curvature 2-cochain `d_1`.
   - Proves exactness `d_1 (d_0 φ) = (0, 0, 0, 0)` (`cochain_curvature_of_coboundary_zero`), gauge
     invariance `d_1 (ω + d_0 φ) = d_1 ω` (`cochain_curvature_gauge_invariant`), linearity
     `d_1 (c • ω) = c • d_1 ω` (`cochain_curvature_linear_scaling`), and the discrete Bianchi
     identity `F012 - F013 + F023 - F123 = 0` on the closed 2-cycle (`tetrahedral_bianchi_identity`).

2. **`OBL-R03` Split Between Cochain Curvature (`d_1 ω`) and Regge Metric Deficit (`ε_v`)**:
   - Defines the Regge hinge deficit `reggeVertexDeficit fullTurn angleSum = fullTurn - angleSum`
     and the equilateral `k`-sector vertex deficit `equilateralVertexDeficit fullTurn k = fullTurn - k * (fullTurn / 6)`.
   - Proves that under uniform edge-length rescaling, the metric sector angles and Regge deficit
     are scale-invariant whereas cochain curvature scales linearly with the 1-cochain amplitude
     (`obl_r03_scaling_dichotomy_cochain_vs_regge`).
   - Proves bidirectional uncoupling (`obl_r03_flat_hinge_with_arbitrary_cochain_curvature` and
     `obl_r03_zero_cochain_curvature_with_positive_regge_deficit`): a flat 6-equilateral-triangle
     hinge (`ε_v = 0`) admits 1-cochains with any prescribed face curvature `q ≠ 0`, whereas the
     zero/pure-gauge 1-cochain (`d_1 ω = 0`) on the 4-face equilateral tetrahedron has strictly
     positive Regge deficit `fullTurn / 2` at every vertex and total Gauss-Bonnet sum `2 * fullTurn`,
     contrasting with the identically zero oriented Bianchi sum of cochain curvatures
     (`obl_r03_gauss_bonnet_vs_bianchi_sum_contrast`).

3. **`OBL-R01` Continuum Light-Cone Scaling Gap & Lattice-Spacing Underdetermination Fence**:
   - Defines the effective lattice signal speed `effectiveLightSpeed ax at = ax / at` from external
     spatial and temporal lattice spacings `(ax, at)`.
   - Proves that for any nonzero temporal spacing `at ≠ 0` and any target slope `cTarget ≠ 0`,
     choosing `ax = cTarget * at` reproduces `effectiveLightSpeed ax at = cTarget` (`obl_r01_any_light_cone_slope_by_spacing_calibration`),
     and distinct spatial calibrations `ax1 ≠ ax2` yield distinct effective light-cone slopes
     (`obl_r01_spacing_calibration_injective`).
   - Proves the discrete Manhattan vs. Euclidean light-cone anisotropy fence on `(3, 4)` vs. `(5, 0)`:
     both displacements have identical Euclidean squared radius `3^2 + 4^2 = 5^2 + 0^2 = 25`,
     whereas their combinatorial graph step counts `3 + 4 = 7` and `5 + 0 = 5` differ
     (`obl_r01_manhattan_vs_euclidean_light_cone_anisotropy`).
-/

namespace CampaignTfq0090FiniteQg

-- ============================================================================
-- 1. Finite Tetrahedral Comparison Complex & Cochain Curvature (`d_1 ∘ d_0 = 0`)
-- ============================================================================

/-- 0-cochain on the 4 vertices `(0, 1, 2, 3)` of `K_4^{(2)}`. -/
structure Cochain0 where
  p0 : ℚ
  p1 : ℚ
  p2 : ℚ
  p3 : ℚ
  deriving DecidableEq, Repr

/-- 1-cochain on the 6 oriented edges `(01, 02, 03, 12, 13, 23)` of `K_4^{(2)}`. -/
structure Cochain1 where
  e01 : ℚ
  e02 : ℚ
  e03 : ℚ
  e12 : ℚ
  e13 : ℚ
  e23 : ℚ
  deriving DecidableEq, Repr

/-- 2-cochain on the 4 oriented triangular faces `(012, 013, 023, 123)` of `K_4^{(2)}`. -/
@[ext]
structure Cochain2 where
  f012 : ℚ
  f013 : ℚ
  f023 : ℚ
  f123 : ℚ
  deriving DecidableEq, Repr

/-- Coboundary operator `d_0 : C^0 → C^1` sending `φ` to `(d_0 φ)(u,v) = φ(v) - φ(u)`. -/
def d0 (φ : Cochain0) : Cochain1 :=
  { e01 := φ.p1 - φ.p0
    e02 := φ.p2 - φ.p0
    e03 := φ.p3 - φ.p0
    e12 := φ.p2 - φ.p1
    e13 := φ.p3 - φ.p1
    e23 := φ.p3 - φ.p2 }

/-- Pointwise addition of 1-cochains. -/
def add1 (ω η : Cochain1) : Cochain1 :=
  { e01 := ω.e01 + η.e01
    e02 := ω.e02 + η.e02
    e03 := ω.e03 + η.e03
    e12 := ω.e12 + η.e12
    e13 := ω.e13 + η.e13
    e23 := ω.e23 + η.e23 }

/-- Scalar multiplication of a 1-cochain by `c : ℚ`. -/
def smul1 (c : ℚ) (ω : Cochain1) : Cochain1 :=
  { e01 := c * ω.e01
    e02 := c * ω.e02
    e03 := c * ω.e03
    e12 := c * ω.e12
    e13 := c * ω.e13
    e23 := c * ω.e23 }

/-- Scalar multiplication of a 2-cochain by `c : ℚ`. -/
def smul2 (c : ℚ) (F : Cochain2) : Cochain2 :=
  { f012 := c * F.f012
    f013 := c * F.f013
    f023 := c * F.f023
    f123 := c * F.f123 }

/-- Cochain curvature / face holonomy operator `d_1 : C^1 → C^2` on `K_4^{(2)}`:
`(d_1 ω)(u,v,w) = ω(u,v) + ω(v,w) - ω(u,w)`. -/
def d1 (ω : Cochain1) : Cochain2 :=
  { f012 := ω.e01 + ω.e12 - ω.e02
    f013 := ω.e01 + ω.e13 - ω.e03
    f023 := ω.e02 + ω.e23 - ω.e03
    f123 := ω.e12 + ω.e23 - ω.e13 }

/-- Oriented 2-cycle boundary sum `d_2 : C^2 → ℚ` on the closed tetrahedron `∂(0123)`:
`F(012) - F(013) + F(023) - F(123)`. -/
def bianchiCycleSum (F : Cochain2) : ℚ :=
  F.f012 - F.f013 + F.f023 - F.f123

/-- Zero 1-cochain on `K_4^{(2)}`. -/
def zeroCochain1 : Cochain1 :=
  { e01 := 0, e02 := 0, e03 := 0, e12 := 0, e13 := 0, e23 := 0 }

/-- Zero 2-cochain on `K_4^{(2)}`. -/
def zeroCochain2 : Cochain2 :=
  { f012 := 0, f013 := 0, f023 := 0, f123 := 0 }

/-- Theorem 1: Every exact 1-cochain `d_0 φ` has identically vanishing cochain curvature
`d_1 (d_0 φ) = 0` on all 4 faces of `K_4^{(2)}`. -/
theorem cochain_curvature_of_coboundary_zero (φ : Cochain0) :
    d1 (d0 φ) = zeroCochain2 := by
  ext <;> dsimp [d1, d0, zeroCochain2] <;> ring

/-- Theorem 2: Face holonomy / cochain curvature is invariant under any vertex gauge transformation
`ω ↦ ω + d_0 φ`. -/
theorem cochain_curvature_gauge_invariant (ω : Cochain1) (φ : Cochain0) :
    d1 (add1 ω (d0 φ)) = d1 ω := by
  ext <;> dsimp [d1, add1, d0] <;> ring

/-- Theorem 3: Cochain curvature scales linearly under amplitude rescaling `ω ↦ c • ω`:
`d_1 (smul1 c ω) = smul2 c (d_1 ω)`. -/
theorem cochain_curvature_linear_scaling (c : ℚ) (ω : Cochain1) :
    d1 (smul1 c ω) = smul2 c (d1 ω) := by
  ext <;> dsimp [d1, smul1, smul2] <;> ring

/-- Theorem 4: Discrete Bianchi identity on `K_4^{(2)}`: for every 1-cochain `ω`, the oriented sum
of face curvatures around the closed tetrahedral 2-cycle vanishes (`d_2 (d_1 ω) = 0`). -/
theorem tetrahedral_bianchi_identity (ω : Cochain1) :
    bianchiCycleSum (d1 ω) = 0 := by
  dsimp [bianchiCycleSum, d1]
  ring

-- ============================================================================
-- 2. `OBL-R03` Split Between Cochain Curvature and Regge Metric Deficit
-- ============================================================================

/-- Regge vertex/hinge angle deficit `fullTurn - angleSum` in exact rational turn units. -/
def reggeVertexDeficit (fullTurn angleSum : ℚ) : ℚ :=
  fullTurn - angleSum

/-- Regge deficit at a vertex where `k` equilateral triangles meet (each interior angle is
`fullTurn / 6`, since 3 angles of an equilateral triangle sum to `fullTurn / 2`). -/
def equilateralVertexDeficit (fullTurn k : ℚ) : ℚ :=
  reggeVertexDeficit fullTurn (k * (fullTurn / 6))

/-- Single-edge 1-cochain carrying comparison weight `q` on edge `e12` and `0` elsewhere. -/
def singleEdgeCochain1 (q : ℚ) : Cochain1 :=
  { e01 := 0, e02 := 0, e03 := 0, e12 := q, e13 := 0, e23 := 0 }

/-- Theorem 5 (`OBL-R03` Scaling Dichotomy): Under uniform edge-length rescaling `L ↦ s * L`
(`s ≠ 0`), equilateral sector angles `(s * L) / (6 * (s * L)) * fullTurn = fullTurn / 6` and the
Regge deficit are strictly scale-invariant, whereas rescaling the 1-cochain by `s` scales the
cochain curvature linearly by `s`. -/
theorem obl_r03_scaling_dichotomy_cochain_vs_regge
    (fullTurn k L s q : ℚ) (hL : L ≠ 0) (hs : s ≠ 0) :
    reggeVertexDeficit fullTurn (k * (((s * L) / (6 * (s * L))) * fullTurn)) =
      equilateralVertexDeficit fullTurn k ∧
    (d1 (smul1 s (singleEdgeCochain1 q))).f012 = s * q := by
  refine ⟨?_, ?_⟩
  · dsimp [reggeVertexDeficit, equilateralVertexDeficit]
    field_simp [hL, hs]
  · dsimp [d1, smul1, singleEdgeCochain1]
    ring

/-- Theorem 6 (`OBL-R03` Uncoupling Direction 1): A metrically flat 6-equilateral-triangle hinge
has vanishing Regge deficit `equilateralVertexDeficit fullTurn 6 = 0`, yet for any nonzero rational
`q ≠ 0`, `singleEdgeCochain1 q` has nonzero cochain curvature `f012 = q ≠ 0` and `f123 = q ≠ 0`. -/
theorem obl_r03_flat_hinge_with_arbitrary_cochain_curvature
    (fullTurn q : ℚ) (hq : q ≠ 0) :
    equilateralVertexDeficit fullTurn 6 = 0 ∧
    (d1 (singleEdgeCochain1 q)).f012 = q ∧
    (d1 (singleEdgeCochain1 q)).f123 = q ∧
    (d1 (singleEdgeCochain1 q)).f012 ≠ 0 := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · dsimp [equilateralVertexDeficit, reggeVertexDeficit]; ring
  · dsimp [d1, singleEdgeCochain1]; ring
  · dsimp [d1, singleEdgeCochain1]; ring
  · dsimp [d1, singleEdgeCochain1]
    intro h0
    apply hq
    linarith

/-- Theorem 7 (`OBL-R03` Uncoupling Direction 2): For any pure-gauge 1-cochain `d_0 φ`, the cochain
curvature vanishes on every face (`d_1 (d_0 φ) = 0`), whereas the 3-equilateral-triangle tetrahedral
vertex has strictly positive Regge deficit `equilateralVertexDeficit fullTurn 3 = fullTurn / 2 > 0`
whenever `fullTurn > 0`. -/
theorem obl_r03_zero_cochain_curvature_with_positive_regge_deficit
    (φ : Cochain0) (fullTurn : ℚ) (hTurn : 0 < fullTurn) :
    d1 (d0 φ) = zeroCochain2 ∧
    equilateralVertexDeficit fullTurn 3 = fullTurn / 2 ∧
    0 < equilateralVertexDeficit fullTurn 3 := by
  refine ⟨cochain_curvature_of_coboundary_zero φ, ?_, ?_⟩
  · dsimp [equilateralVertexDeficit, reggeVertexDeficit]; ring
  · dsimp [equilateralVertexDeficit, reggeVertexDeficit]; linarith

/-- Theorem 8 (`OBL-R03` Global Gauss-Bonnet vs. Bianchi Sum Contrast): On the 4-vertex equilateral
tetrahedron (`V = 4`, each vertex degree `k = 3`), the sum of the 4 Regge vertex deficits equals
`2 * fullTurn ≠ 0` (discrete Gauss-Bonnet `χ(S^2) * fullTurn`), whereas for every 1-cochain `ω` the
oriented Bianchi cycle sum of cochain curvatures equals `0`. -/
theorem obl_r03_gauss_bonnet_vs_bianchi_sum_contrast
    (ω : Cochain1) (fullTurn : ℚ) (hTurn : fullTurn ≠ 0) :
    4 * equilateralVertexDeficit fullTurn 3 = 2 * fullTurn ∧
    4 * equilateralVertexDeficit fullTurn 3 ≠ 0 ∧
    bianchiCycleSum (d1 ω) = 0 := by
  refine ⟨?_, ?_, tetrahedral_bianchi_identity ω⟩
  · dsimp [equilateralVertexDeficit, reggeVertexDeficit]; ring
  · dsimp [equilateralVertexDeficit, reggeVertexDeficit]
    intro h0
    apply hTurn
    linarith

-- ============================================================================
-- 3. `OBL-R01` Continuum Light-Cone Scaling Gap & Lattice-Spacing Fence
-- ============================================================================

/-- Effective lattice light-cone speed `ax / at` from external spatial spacing `ax` and temporal
spacing `at`. -/
def effectiveLightSpeed (ax at_ : ℚ) : ℚ :=
  ax / at_

/-- Physical Minkowskian interval `(c * N_t * at)^2 - (N_x * ax)^2` of a discrete displacement
`(N_t, N_x)` under spacings `(at, ax)` and speed parameter `c`. -/
def discreteMinkowskiInterval (c at_ ax Nt Nx : ℚ) : ℚ :=
  (c * Nt * at_) ^ 2 - (Nx * ax) ^ 2

/-- Theorem 9 (`OBL-R01` Light-Cone Slope Underdetermination): Without an intrinsic scale-fixing law
relating `ax` and `at`, any nonzero target light-cone speed `cTarget ≠ 0` is reproduced from any
nonzero temporal spacing `at ≠ 0` by choosing `ax = cTarget * at`. -/
theorem obl_r01_any_light_cone_slope_by_spacing_calibration
    (at_ cTarget : ℚ) (hat : at_ ≠ 0) (hc : cTarget ≠ 0) :
    effectiveLightSpeed (cTarget * at_) at_ = cTarget ∧
    (cTarget * at_) ≠ 0 := by
  refine ⟨?_, mul_ne_zero hc hat⟩
  dsimp [effectiveLightSpeed]
  field_simp [hat]

/-- Theorem 10 (`OBL-R01` Spacing Calibration Injectivity): For any fixed nonzero temporal spacing
`at ≠ 0`, distinct spatial lattice spacings `ax1 ≠ ax2` yield distinct effective light-cone slopes. -/
theorem obl_r01_spacing_calibration_injective
    (at_ ax1 ax2 : ℚ) (hat : at_ ≠ 0)
    (heq : effectiveLightSpeed ax1 at_ = effectiveLightSpeed ax2 at_) :
    ax1 = ax2 := by
  dsimp [effectiveLightSpeed] at heq
  field_simp [hat] at heq
  linarith

/-- Theorem 11 (`OBL-R01` Causal Classification Reversal Under Spacing Choice): For the fixed
combinatorial displacement `(N_t, N_x) = (2, 3)` with `c = 1` and `at = 1`, choosing spatial spacing
`ax = 1/2` makes the Minkowskian interval strictly timelike (`> 0`), choosing `ax = 2/3` makes it
null (`= 0`), and choosing `ax = 1` makes it strictly spacelike (`< 0`). -/
theorem obl_r01_causal_character_depends_on_uncalibrated_spacing :
    discreteMinkowskiInterval 1 1 (1 / 2) 2 3 = 7 / 4 ∧
    0 < discreteMinkowskiInterval 1 1 (1 / 2) 2 3 ∧
    discreteMinkowskiInterval 1 1 (2 / 3) 2 3 = 0 ∧
    discreteMinkowskiInterval 1 1 1 2 3 = -5 ∧
    discreteMinkowskiInterval 1 1 1 2 3 < 0 := by
  dsimp [discreteMinkowskiInterval]
  norm_num

/-- Manhattan (`ℓ_1`) graph step count `dx + dy` and Euclidean (`ℓ_2^2`) squared radius
`dx^2 + dy^2` for nonnegative grid displacements `(dx, dy)`. -/
def manhattanSteps (dx dy : Nat) : Nat :=
  dx + dy

def euclideanSqRadius (dx dy : Nat) : Nat :=
  dx * dx + dy * dy

/-- Theorem 12 (`OBL-R01` Manhattan vs. Euclidean Light-Cone Anisotropy Fence): On a 2D square
comparison lattice, the displacements `(3, 4)` and `(5, 0)` lie on the same Euclidean circle
(`euclideanSqRadius 3 4 = euclideanSqRadius 5 0 = 25`), but require distinct combinatorial step
counts (`manhattanSteps 3 4 = 7 ≠ 5 = manhattanSteps 5 0`). -/
theorem obl_r01_manhattan_vs_euclidean_light_cone_anisotropy :
    euclideanSqRadius 3 4 = 25 ∧
    euclideanSqRadius 5 0 = 25 ∧
    euclideanSqRadius 3 4 = euclideanSqRadius 5 0 ∧
    manhattanSteps 3 4 = 7 ∧
    manhattanSteps 5 0 = 5 ∧
    manhattanSteps 3 4 ≠ manhattanSteps 5 0 := by
  decide

end CampaignTfq0090FiniteQg

#print axioms CampaignTfq0090FiniteQg.cochain_curvature_of_coboundary_zero
#print axioms CampaignTfq0090FiniteQg.cochain_curvature_gauge_invariant
#print axioms CampaignTfq0090FiniteQg.cochain_curvature_linear_scaling
#print axioms CampaignTfq0090FiniteQg.tetrahedral_bianchi_identity
#print axioms CampaignTfq0090FiniteQg.obl_r03_scaling_dichotomy_cochain_vs_regge
#print axioms CampaignTfq0090FiniteQg.obl_r03_flat_hinge_with_arbitrary_cochain_curvature
#print axioms CampaignTfq0090FiniteQg.obl_r03_zero_cochain_curvature_with_positive_regge_deficit
#print axioms CampaignTfq0090FiniteQg.obl_r03_gauss_bonnet_vs_bianchi_sum_contrast
#print axioms CampaignTfq0090FiniteQg.obl_r01_any_light_cone_slope_by_spacing_calibration
#print axioms CampaignTfq0090FiniteQg.obl_r01_spacing_calibration_injective
#print axioms CampaignTfq0090FiniteQg.obl_r01_causal_character_depends_on_uncalibrated_spacing
#print axioms CampaignTfq0090FiniteQg.obl_r01_manhattan_vs_euclidean_light_cone_anisotropy

private def l5aProvenance : String :=
  "Origin: lean4/CampaignTfq0090FiniteQg.lean Claim: TFQ-0090 AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
