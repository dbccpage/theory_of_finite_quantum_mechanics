import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-!
Counting gap for the CKM physics fence.

`cycleCount` and `cpCount` are rational expressions. Their difference identity
is arithmetic. It does not build a graph, a tree, a unitary matrix, or a
measured angle. Two declared quartets in `Q(i)` have imaginary parts 0 and 1.
-/

namespace CampaignDfmCkmPhysicsFence

def cycleCount (n : ℚ) : ℚ := (n - 1) * (n - 1)

def constraintCount (n : ℚ) : ℚ := n * (n - 1) / 2

def cpCount (n : ℚ) : ℚ := (n - 1) * (n - 2) / 2

theorem cpCount_from_difference (n : ℚ) :
    cycleCount n - constraintCount n = cpCount n := by
  simp only [cycleCount, constraintCount, cpCount, div_eq_mul_inv]
  ring

theorem constraintCount_sum (n : ℚ) :
    cpCount n + (n - 1) = constraintCount n := by
  simp only [cpCount, constraintCount, div_eq_mul_inv]
  ring

theorem count_table :
    cycleCount 1 = 0 ∧ cpCount 1 = 0 ∧
    cycleCount 2 = 1 ∧ cpCount 2 = 0 ∧
    cycleCount 3 = 4 ∧ cpCount 3 = 1 ∧
    cycleCount 4 = 9 ∧ cpCount 4 = 3 ∧
    cycleCount 1 = cpCount 1 ∧
    cycleCount 2 ≠ cpCount 2 ∧
    cycleCount 3 ≠ cpCount 3 ∧
    cycleCount 4 ≠ cpCount 4 := by
  simp only [cycleCount, cpCount]
  norm_num

theorem three_generation_split :
    cycleCount 3 = 4 ∧
    constraintCount 3 = 3 ∧
    cpCount 3 = 1 ∧
    cycleCount 3 - constraintCount 3 = cpCount 3 := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · simp only [cycleCount]; norm_num
  · simp only [constraintCount]; norm_num
  · simp only [cpCount]; norm_num
  · rw [cpCount_from_difference]

@[ext]
structure GR where
  re : ℚ
  im : ℚ
  deriving DecidableEq, Repr

namespace GR

def conj (z : GR) : GR := ⟨z.re, -z.im⟩

def mul (z w : GR) : GR :=
  ⟨z.re * w.re - z.im * w.im, z.re * w.im + z.im * w.re⟩

end GR

def quartet (a b c d : GR) : GR :=
  GR.mul (GR.mul a b) (GR.mul (GR.conj c) (GR.conj d))

def oneGR : GR := ⟨1, 0⟩
def iGR : GR := ⟨0, 1⟩

def quartetReal : GR := quartet oneGR oneGR oneGR oneGR
def quartetImag : GR := quartet oneGR iGR oneGR oneGR

theorem quartet_real_value : quartetReal = ⟨1, 0⟩ := by
  simp only [quartetReal, quartet, oneGR, GR.mul, GR.conj]
  apply GR.ext <;> norm_num

theorem quartet_imag_value : quartetImag = ⟨0, 1⟩ := by
  simp only [quartetImag, quartet, oneGR, iGR, GR.mul, GR.conj]
  apply GR.ext <;> norm_num

theorem quartets_differ : quartetReal ≠ quartetImag := by
  intro h
  have hr := congrArg GR.im h
  simp only [quartet_real_value, quartet_imag_value] at hr
  norm_num at hr

theorem count_misses_one_quartet :
    cpCount 3 = 1 ∧
    quartetReal.im = 0 ∧
    quartetImag.im = 1 ∧
    quartetReal.im ≠ cpCount 3 ∧
    quartetImag.im = cpCount 3 := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · simp only [cpCount]; norm_num
  · rw [quartet_real_value]
  · rw [quartet_imag_value]
  · rw [quartet_real_value]
    simp only [cpCount]
    norm_num
  · rw [quartet_imag_value]
    simp only [cpCount]
    norm_num

#print axioms CampaignDfmCkmPhysicsFence.cpCount_from_difference
#print axioms CampaignDfmCkmPhysicsFence.constraintCount_sum
#print axioms CampaignDfmCkmPhysicsFence.count_table
#print axioms CampaignDfmCkmPhysicsFence.three_generation_split
#print axioms CampaignDfmCkmPhysicsFence.quartet_real_value
#print axioms CampaignDfmCkmPhysicsFence.quartet_imag_value
#print axioms CampaignDfmCkmPhysicsFence.quartets_differ
#print axioms CampaignDfmCkmPhysicsFence.count_misses_one_quartet

end CampaignDfmCkmPhysicsFence
