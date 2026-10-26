import WitnessedDifference.FiniteStateEffectReadout

/-!
# Finite process composition on Gram-factor states

A Gaussian-rational operator `K` acts on the density presented by a factor
`B` through the new factor `B K†`.  Complete families satisfy
`Σ K†K = I`; the binary case is formalized here.  The resulting branch masses
sum exactly to the input mass, sequential branch factors compose in the
operator order, and a unitary factor is reversible.

This is a finite algebraic process model.  It does not select which process is
physical, identify outcome labels, prove complete positivity over an analytic
completion, or establish universal quantum computation.
-/

namespace WitnessedDifference.FiniteProcessComposition

open WitnessedDifference.FiniteHermitianization
open WitnessedDifference.FiniteStateEffectReadout

set_option linter.checkUnivs false
set_option linter.unusedSimpArgs false

theorem mdagger_involutive (A : GMatrix2) : mdagger (mdagger A) = A := by
  cases A
  apply matrix_ext <;>
    simp only [mdagger, gconj_involutive]

theorem mdagger_mmul (A B : GMatrix2) :
    mdagger (mmul A B) = mmul (mdagger B) (mdagger A) := by
  cases A
  cases B
  apply matrix_ext <;>
    apply gaussian_ext <;>
      simp only [mdagger, mmul, gconj, gadd, gmul, Rat.neg_add,
        Rat.neg_mul, Rat.mul_neg, Rat.neg_neg, Rat.sub_eq_add_neg,
        Rat.add_mul, Rat.mul_add, Rat.mul_assoc] <;> grind

theorem mmul_assoc (A B C : GMatrix2) :
    mmul (mmul A B) C = mmul A (mmul B C) := by
  cases A
  cases B
  cases C
  apply matrix_ext <;>
    apply gaussian_ext <;>
      simp only [mmul, gadd, gmul, Rat.sub_eq_add_neg, Rat.neg_add,
        Rat.neg_mul, Rat.mul_neg, Rat.neg_neg, Rat.add_mul, Rat.mul_add,
        Rat.mul_assoc] <;> grind

theorem frobenius_dagger (A : GMatrix2) :
    frobeniusSquare (mdagger A) = frobeniusSquare A := by
  cases A
  simp only [frobeniusSquare, mdagger, gnorm, gconj]
  grind

theorem gram_zero : gram mzero = mzero := by
  apply matrix_ext <;>
    apply gaussian_ext <;>
      simp only [gram, mzero, mmul, mdagger, gadd, gmul, gconj, gzero] <;>
        grind

theorem madd_zero_right (A : GMatrix2) : madd A mzero = A := by
  cases A
  apply matrix_ext <;>
    apply gaussian_ext <;>
      simp only [madd, mzero, gadd, gzero] <;> grind

/-- Applying branch operator `K` to a state factor `B`. -/
def postFactor (B K : GMatrix2) : GMatrix2 := mmul B (mdagger K)

/-- The mass of the output factor is the readout numerator of the branch. -/
theorem post_mass_eq_readout_numerator (B K : GMatrix2) :
    frobeniusSquare (postFactor B K) =
      frobeniusSquare (mmul K (mdagger B)) := by
  calc
    frobeniusSquare (postFactor B K) =
        frobeniusSquare (mdagger (postFactor B K)) :=
      (frobenius_dagger (postFactor B K)).symm
    _ = frobeniusSquare (mmul K (mdagger B)) := by
      rw [postFactor, mdagger_mmul, mdagger_involutive]

/-- A complete binary process preserves total unnormalized state mass. -/
theorem post_mass_partition (B K L : GMatrix2)
    (complete : madd (gram K) (gram L) = midentity) :
    frobeniusSquare (postFactor B K) + frobeniusSquare (postFactor B L) =
      frobeniusSquare B := by
  rw [post_mass_eq_readout_numerator, post_mass_eq_readout_numerator]
  exact frame_partition B K L complete

/-- Sequential branch factors compose in the physical operator order. -/
theorem postFactor_compose (B K L : GMatrix2) :
    postFactor (postFactor B K) L = postFactor B (mmul L K) := by
  unfold postFactor
  rw [mdagger_mmul]
  exact mmul_assoc B (mdagger K) (mdagger L)

structure UnitaryFactor where
  op : GMatrix2
  complete : gram op = midentity

theorem unitary_mass_preserving (B : GMatrix2) (U : UnitaryFactor) :
    frobeniusSquare (postFactor B U.op) = frobeniusSquare B := by
  have complete : madd (gram U.op) (gram mzero) = midentity := by
    rw [U.complete, gram_zero, madd_zero_right]
  have partition := post_mass_partition B U.op mzero complete
  have zeroMass : frobeniusSquare (postFactor B mzero) = 0 := by
    simp only [postFactor, mzero, mdagger, mmul, gadd, gmul, gconj,
      frobeniusSquare, gnorm, gzero]
    grind
  grind

/-- Applying the declared adjoint after a unitary branch recovers the factor. -/
theorem unitary_reversible (B : GMatrix2) (U : UnitaryFactor) :
    postFactor (postFactor B U.op) (mdagger U.op) = B := by
  unfold postFactor
  rw [mdagger_involutive, mmul_assoc]
  change mmul B (gram U.op) = B
  rw [U.complete, mmul_identity_right]

/-! ## Exact bit-flip fixture -/

def xGate : GMatrix2 := ⟨gzero, gone, gone, gzero⟩

theorem x_gate_unitary : gram xGate = midentity := by
  apply matrix_ext <;>
    apply gaussian_ext <;>
      simp only [gram, xGate, midentity, mmul, mdagger, gadd, gmul,
        gconj, gone, gzero] <;> grind

def xUnitary : UnitaryFactor := ⟨xGate, x_gate_unitary⟩

def basisOneFactor : GMatrix2 := ⟨gzero, gone, gzero, gzero⟩

theorem x_gate_transports_basis_factor :
    postFactor basisStateFactor xGate = basisOneFactor := by
  apply matrix_ext <;>
    apply gaussian_ext <;>
      simp only [postFactor, basisStateFactor, basisOneFactor, xGate, mmul,
        mdagger, gadd, gmul, gconj, gone, gzero] <;> grind

theorem x_gate_round_trip :
    postFactor (postFactor basisStateFactor xGate) (mdagger xGate) =
      basisStateFactor := unitary_reversible basisStateFactor xUnitary

end WitnessedDifference.FiniteProcessComposition

#print axioms WitnessedDifference.FiniteProcessComposition.mdagger_involutive
#print axioms WitnessedDifference.FiniteProcessComposition.mdagger_mmul
#print axioms WitnessedDifference.FiniteProcessComposition.mmul_assoc
#print axioms WitnessedDifference.FiniteProcessComposition.frobenius_dagger
#print axioms WitnessedDifference.FiniteProcessComposition.post_mass_eq_readout_numerator
#print axioms WitnessedDifference.FiniteProcessComposition.post_mass_partition
#print axioms WitnessedDifference.FiniteProcessComposition.postFactor_compose
#print axioms WitnessedDifference.FiniteProcessComposition.unitary_mass_preserving
#print axioms WitnessedDifference.FiniteProcessComposition.unitary_reversible
#print axioms WitnessedDifference.FiniteProcessComposition.x_gate_unitary
#print axioms WitnessedDifference.FiniteProcessComposition.x_gate_transports_basis_factor
#print axioms WitnessedDifference.FiniteProcessComposition.x_gate_round_trip
