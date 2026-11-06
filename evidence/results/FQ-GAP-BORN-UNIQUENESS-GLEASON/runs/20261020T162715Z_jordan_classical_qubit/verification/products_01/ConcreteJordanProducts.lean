import ReconstructionArithmetic
import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Analysis.Convex.StdSimplex
import Mathlib.Tactic

/-! Explicit real products for the supported state models. Identities and square positivity are
proved directly. No complex Hermitian-matrix isomorphism or full global EJA classification is
claimed. The classical positive cone and spin Lorentz cone are stated explicitly. -/
noncomputable section
namespace FiniteQM.ConcreteJordanProducts

def classicalMul {r : ℕ} (a b : Fin r → ℝ) : Fin r → ℝ := fun i => a i * b i
def classicalUnit (r : ℕ) : Fin r → ℝ := fun _ => 1
def classicalTrace {r : ℕ} (a : Fin r → ℝ) : ℝ := ∑ i, a i
def classicalPositive {r : ℕ} (a : Fin r → ℝ) : Prop := ∀ i, 0 ≤ a i

theorem classical_comm {r : ℕ} (a b : Fin r → ℝ) : classicalMul a b = classicalMul b a := by
  funext i; exact mul_comm _ _
theorem classical_unit {r : ℕ} (a : Fin r → ℝ) : classicalMul (classicalUnit r) a = a := by
  funext i; simp [classicalMul, classicalUnit]
theorem classical_jordan_identity {r : ℕ} (a b : Fin r → ℝ) :
    classicalMul a (classicalMul (classicalMul a a) b) =
      classicalMul (classicalMul a a) (classicalMul a b) := by
  funext i; simp only [classicalMul]; ring

theorem classical_square_positive {r : ℕ} (a : Fin r → ℝ) :
    classicalPositive (classicalMul a a) := fun i => mul_self_nonneg (a i)

theorem classical_normalized {r : ℕ} (a : Fin r → ℝ) :
    classicalPositive a ∧ classicalTrace a = 1 ↔ a ∈ stdSimplex ℝ (Fin r) := Iff.rfl

abbrev Spin3 := ℝ × EuclideanSpace ℝ (Fin 3)
def spinMul (a b : Spin3) : Spin3 :=
  (a.1*b.1 + inner ℝ a.2 b.2, a.1 • b.2 + b.1 • a.2)
def spinUnit : Spin3 := (1, 0)
def spinTrace (a : Spin3) : ℝ := 2*a.1
def spinPositive (a : Spin3) : Prop := ‖a.2‖ ≤ a.1

theorem spin_comm (a b : Spin3) : spinMul a b = spinMul b a := by
  apply Prod.ext
  · simp only [spinMul, real_inner_comm b.2 a.2]; ring
  · simp [spinMul, add_comm]

theorem spin_unit (a : Spin3) : spinMul spinUnit a = a := by
  ext <;> simp [spinMul, spinUnit]

theorem spin_jordan_identity (a b : Spin3) :
    spinMul a (spinMul (spinMul a a) b) = spinMul (spinMul a a) (spinMul a b) := by
  apply Prod.ext
  · simp only [spinMul, inner_add_left, inner_add_right,
      real_inner_smul_left, real_inner_smul_right, real_inner_comm b.2 a.2]
    ring
  · simp only [spinMul, inner_add_left, inner_add_right,
      real_inner_smul_left, real_inner_smul_right, real_inner_comm b.2 a.2]
    module

theorem spin_square_positive (a : Spin3) : spinPositive (spinMul a a) := by
  have hvec : a.1 • a.2 + a.1 • a.2 = (2*a.1) • a.2 := by module
  change ‖a.1 • a.2 + a.1 • a.2‖ ≤ a.1*a.1 + inner ℝ a.2 a.2
  rw [hvec, norm_smul, real_inner_self_eq_norm_sq]
  simp only [Real.norm_eq_abs, abs_mul, abs_ofNat]
  nlinarith [sq_nonneg (|a.1| - ‖a.2‖), sq_abs a.1]

/-- A normalized spin state has scalar part 1/2 and Bloch vector scaled by 1/2. -/
def blochState (x : EuclideanSpace ℝ (Fin 3)) : Spin3 := (1/2, (1/2 : ℝ) • x)

theorem bloch_trace (x : EuclideanSpace ℝ (Fin 3)) : spinTrace (blochState x) = 1 := by
  norm_num [spinTrace, blochState]

theorem bloch_positive_iff (x : EuclideanSpace ℝ (Fin 3)) :
    spinPositive (blochState x) ↔ ‖x‖ ≤ 1 := by
  unfold spinPositive blochState
  simp only [norm_smul, Real.norm_eq_abs]
  norm_num
  constructor <;> intro h <;> linarith

#print axioms classical_comm
#print axioms classical_unit
#print axioms classical_jordan_identity
#print axioms classical_square_positive
#print axioms classical_normalized
#print axioms spin_comm
#print axioms spin_unit
#print axioms spin_jordan_identity
#print axioms spin_square_positive
#print axioms bloch_trace
#print axioms bloch_positive_iff
end FiniteQM.ConcreteJordanProducts