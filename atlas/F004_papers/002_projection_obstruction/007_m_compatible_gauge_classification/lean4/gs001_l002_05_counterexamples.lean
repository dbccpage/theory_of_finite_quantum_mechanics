/-
Paper 002, Target 5 / ENC-0523: independence witnesses.

These finite witnesses mechanize the four counterexample rows behind PL-002-2:
dropping P1, P2, P3, or edge-uniformity leaves the target scalar unweighted
l1 endpoint underdetermined.
-/

import Mathlib.Data.Real.Basic
import Mathlib.Tactic

namespace Enc0523

abbrev TwoEdgeCochain := Fin 2 → ℝ

def leftUnit : TwoEdgeCochain := fun e => if e = 0 then 1 else 0
def rightUnit : TwoEdgeCochain := fun e => if e = 1 then 1 else 0

/-! ## Dropping P1: max aggregation is not edge-additive. -/

def maxDiagnostic (x : TwoEdgeCochain) : ℝ :=
  max |x 0| |x 1|

theorem maxDiagnostic_faithful (x : TwoEdgeCochain) :
    maxDiagnostic x = 0 ↔ x = 0 := by
  constructor
  · intro h
    have hmax : max |x 0| |x 1| = 0 := by
      simpa [maxDiagnostic] using h
    funext e
    fin_cases e
    · have hle : |x 0| ≤ 0 := by
        rw [← hmax]
        exact le_max_left |x 0| |x 1|
      exact abs_eq_zero.mp (le_antisymm hle (abs_nonneg (x 0)))
    · have hle : |x 1| ≤ 0 := by
        rw [← hmax]
        exact le_max_right |x 0| |x 1|
      exact abs_eq_zero.mp (le_antisymm hle (abs_nonneg (x 1)))
  · intro h
    subst h
    simp [maxDiagnostic]

theorem maxDiagnostic_contracts {x y : TwoEdgeCochain}
    (h0 : |y 0| ≤ |x 0|)
    (h1 : |y 1| ≤ |x 1|) :
    maxDiagnostic y ≤ maxDiagnostic x := by
  unfold maxDiagnostic
  exact max_le (h0.trans (le_max_left |x 0| |x 1|))
    (h1.trans (le_max_right |x 0| |x 1|))

theorem max_not_additive :
    maxDiagnostic (leftUnit + rightUnit) ≠
      maxDiagnostic leftUnit + maxDiagnostic rightUnit := by
  norm_num [maxDiagnostic, leftUnit, rightUnit]

/-! ## Dropping P2: the zero diagnostic is additive but not faithful. -/

def zeroDiagnostic (_x : TwoEdgeCochain) : ℝ := 0

theorem zeroDiagnostic_additive (x y : TwoEdgeCochain) :
    zeroDiagnostic (x + y) = zeroDiagnostic x + zeroDiagnostic y := by
  simp [zeroDiagnostic]

theorem zeroDiagnostic_functorial (opNorm : ℝ) (_hop : 0 ≤ opNorm)
    (x y : TwoEdgeCochain) :
    zeroDiagnostic y ≤ opNorm * zeroDiagnostic x := by
  simp [zeroDiagnostic]

theorem leftUnit_ne_zero : leftUnit ≠ 0 := by
  intro h
  have h0 := congrFun h (0 : Fin 2)
  norm_num [leftUnit] at h0

theorem zero_not_faithful :
    ¬ (∀ x : TwoEdgeCochain, zeroDiagnostic x = 0 ↔ x = 0) := by
  intro h
  exact leftUnit_ne_zero ((h leftUnit).mp (by simp [zeroDiagnostic]))

/-! ## Dropping P3: anisotropic local gauge breaks unit-direction constancy. -/

def sqEuclideanNorm (x : TwoEdgeCochain) : ℝ :=
  x 0 ^ 2 + x 1 ^ 2

def anisotropicGauge (x : TwoEdgeCochain) : ℝ :=
  |x 0| + 2 * |x 1|

theorem leftUnit_sqEuclideanNorm :
    sqEuclideanNorm leftUnit = 1 := by
  norm_num [sqEuclideanNorm, leftUnit]

theorem rightUnit_sqEuclideanNorm :
    sqEuclideanNorm rightUnit = 1 := by
  norm_num [sqEuclideanNorm, rightUnit]

theorem anisotropic_leftUnit :
    anisotropicGauge leftUnit = 1 := by
  norm_num [anisotropicGauge, leftUnit]

theorem anisotropic_rightUnit :
    anisotropicGauge rightUnit = 2 := by
  norm_num [anisotropicGauge, rightUnit]

theorem anisotropic_not_p3 :
    ∃ u v : TwoEdgeCochain,
      sqEuclideanNorm u = 1 ∧ sqEuclideanNorm v = 1 ∧
        anisotropicGauge u ≠ anisotropicGauge v := by
  refine ⟨leftUnit, rightUnit, leftUnit_sqEuclideanNorm,
    rightUnit_sqEuclideanNorm, ?_⟩
  intro h
  rw [anisotropic_leftUnit, anisotropic_rightUnit] at h
  norm_num at h

/-! ## Dropping edge-uniformity: unequal weights are not one scalar l1. -/

def unequalWeights (e : Fin 2) : ℝ :=
  if e = 0 then 1 else 2

def unweightedL1 (x : TwoEdgeCochain) : ℝ :=
  |x 0| + |x 1|

def unequalWeightedDiagnostic (x : TwoEdgeCochain) : ℝ :=
  unequalWeights 0 * |x 0| + unequalWeights 1 * |x 1|

theorem unequalWeights_positive (e : Fin 2) :
    0 < unequalWeights e := by
  fin_cases e <;> norm_num [unequalWeights]

theorem unequalWeights_not_uniform :
    ¬ ∃ α : ℝ, ∀ e : Fin 2, unequalWeights e = α := by
  rintro ⟨α, hα⟩
  have h0 : α = 1 := by
    have h := hα 0
    norm_num [unequalWeights] at h
    linarith
  have h1 : α = 2 := by
    have h := hα 1
    norm_num [unequalWeights] at h
    linarith
  linarith

theorem weighted_not_uniform :
    ¬ ∃ α : ℝ, ∀ x : TwoEdgeCochain,
      unequalWeightedDiagnostic x = α * unweightedL1 x := by
  rintro ⟨α, hα⟩
  have hleft : α = 1 := by
    have h := hα leftUnit
    norm_num [unequalWeightedDiagnostic, unweightedL1, unequalWeights,
      leftUnit] at h
    linarith
  have hright : α = 2 := by
    have h := hα rightUnit
    norm_num [unequalWeightedDiagnostic, unweightedL1, unequalWeights,
      rightUnit] at h
    linarith
  linarith

theorem maxDiagnostic_homog (a : ℝ) (x : TwoEdgeCochain) :
    maxDiagnostic (a • x) = |a| * maxDiagnostic x := by
  unfold maxDiagnostic
  dsimp
  rw [abs_mul, abs_mul, ← mul_max_of_nonneg _ _ (abs_nonneg a)]

theorem maxDiagnostic_subadditive (x y : TwoEdgeCochain) :
    maxDiagnostic (x + y) ≤ maxDiagnostic x + maxDiagnostic y := by
  unfold maxDiagnostic
  dsimp
  have h0 : |x 0 + y 0| ≤ |x 0| + |y 0| := abs_add_le (x 0) (y 0)
  have h1 : |x 1 + y 1| ≤ |x 1| + |y 1| := abs_add_le (x 1) (y 1)
  have h0_le : |x 0| + |y 0| ≤ max |x 0| |x 1| + max |y 0| |y 1| :=
    add_le_add (le_max_left _ _) (le_max_left _ _)
  have h1_le : |x 1| + |y 1| ≤ max |x 0| |x 1| + max |y 0| |y 1| :=
    add_le_add (le_max_right _ _) (le_max_right _ _)
  exact max_le (h0.trans h0_le) (h1.trans h1_le)

theorem anisotropicGauge_faithful (x : TwoEdgeCochain) :
    anisotropicGauge x = 0 ↔ x = 0 := by
  unfold anisotropicGauge
  constructor
  · intro h
    have h0_nonneg : 0 ≤ |x 0| := abs_nonneg (x 0)
    have h1_nonneg : 0 ≤ 2 * |x 1| := by positivity
    have h0_zero : |x 0| = 0 := by linarith
    have h1_zero : |x 1| = 0 := by linarith
    funext e
    fin_cases e
    · exact abs_eq_zero.mp h0_zero
    · exact abs_eq_zero.mp h1_zero
  · intro h
    subst h
    simp

theorem anisotropicGauge_homog (a : ℝ) (x : TwoEdgeCochain) :
    anisotropicGauge (a • x) = |a| * anisotropicGauge x := by
  unfold anisotropicGauge
  dsimp
  rw [abs_mul, abs_mul]
  ring

theorem anisotropicGauge_subadditive (x y : TwoEdgeCochain) :
    anisotropicGauge (x + y) ≤ anisotropicGauge x + anisotropicGauge y := by
  unfold anisotropicGauge
  dsimp
  have h0 := abs_add_le (x 0) (y 0)
  have h1 := abs_add_le (x 1) (y 1)
  linarith

theorem unequalWeightedDiagnostic_faithful (x : TwoEdgeCochain) :
    unequalWeightedDiagnostic x = 0 ↔ x = 0 := by
  unfold unequalWeightedDiagnostic unequalWeights
  dsimp
  constructor
  · intro h
    have h0_nonneg : 0 ≤ 1 * |x 0| := by positivity
    have h1_nonneg : 0 ≤ 2 * |x 1| := by positivity
    have h0 : |x 0| = 0 := by linarith
    have h1 : |x 1| = 0 := by linarith
    funext e
    fin_cases e
    · exact abs_eq_zero.mp h0
    · exact abs_eq_zero.mp h1
  · intro h
    subst h
    simp

theorem unequalWeightedDiagnostic_homog (a : ℝ) (x : TwoEdgeCochain) :
    unequalWeightedDiagnostic (a • x) = |a| * unequalWeightedDiagnostic x := by
  unfold unequalWeightedDiagnostic
  dsimp
  rw [abs_mul, abs_mul]
  ring

theorem unequalWeightedDiagnostic_subadditive (x y : TwoEdgeCochain) :
    unequalWeightedDiagnostic (x + y) ≤ unequalWeightedDiagnostic x + unequalWeightedDiagnostic y := by
  unfold unequalWeightedDiagnostic unequalWeights
  dsimp
  have h0 := abs_add_le (x 0) (y 0)
  have h1 := abs_add_le (x 1) (y 1)
  linarith

#print axioms Enc0523.max_not_additive
#print axioms Enc0523.zero_not_faithful
#print axioms Enc0523.anisotropic_not_p3
#print axioms Enc0523.weighted_not_uniform
#print axioms Enc0523.maxDiagnostic_homog
#print axioms Enc0523.maxDiagnostic_subadditive
#print axioms Enc0523.anisotropicGauge_faithful
#print axioms Enc0523.anisotropicGauge_homog
#print axioms Enc0523.anisotropicGauge_subadditive
#print axioms Enc0523.unequalWeightedDiagnostic_faithful
#print axioms Enc0523.unequalWeightedDiagnostic_homog
#print axioms Enc0523.unequalWeightedDiagnostic_subadditive

end Enc0523

