import WitnessedDifference.FiniteHermitianization

/-!
# Certified finite states, effects and a trace readout

This module starts from the exact Gaussian-rational carrier constructed by
`FiniteHermitianization`.  In dimension two, a nonzero factor `B` presents the
normalized positive state `B†B / ‖B‖²_F`.  Two factors `C,D` present a binary
effect exactly when `C†C + D†D = I`.

The accepted probability is computed from the submitted factors as

`‖C B†‖²_F / ‖B‖²_F`.

The file proves exact positivity, normalization and the upper bound.  The
choice of this state/effect certificate language and readout is supplied; it
is not derived from primitive difference, dagger or Hermitianization alone.
Lean core only.
-/

namespace WitnessedDifference.FiniteStateEffectReadout

open WitnessedDifference.FiniteHermitianization

set_option linter.checkUnivs false
set_option linter.unusedSimpArgs false

/-! ## Exact two-by-two Gaussian-rational matrices -/

structure GMatrix2 where
  a00 : GaussianRat
  a01 : GaussianRat
  a10 : GaussianRat
  a11 : GaussianRat
  deriving DecidableEq

theorem matrix_ext {A B : GMatrix2}
    (h00 : A.a00 = B.a00) (h01 : A.a01 = B.a01)
    (h10 : A.a10 = B.a10) (h11 : A.a11 = B.a11) : A = B := by
  cases A
  cases B
  simp only [GMatrix2.mk.injEq] at h00 h01 h10 h11 ⊢
  exact ⟨h00, h01, h10, h11⟩

def mzero : GMatrix2 := ⟨gzero, gzero, gzero, gzero⟩
def midentity : GMatrix2 := ⟨gone, gzero, gzero, gone⟩
def madd (A B : GMatrix2) : GMatrix2 :=
  ⟨gadd A.a00 B.a00, gadd A.a01 B.a01,
    gadd A.a10 B.a10, gadd A.a11 B.a11⟩
def mscale (r : Rat) (A : GMatrix2) : GMatrix2 :=
  ⟨⟨r * A.a00.re, r * A.a00.im⟩,
   ⟨r * A.a01.re, r * A.a01.im⟩,
   ⟨r * A.a10.re, r * A.a10.im⟩,
   ⟨r * A.a11.re, r * A.a11.im⟩⟩
def mdagger (A : GMatrix2) : GMatrix2 :=
  ⟨gconj A.a00, gconj A.a10, gconj A.a01, gconj A.a11⟩
def mmul (A B : GMatrix2) : GMatrix2 :=
  ⟨gadd (gmul A.a00 B.a00) (gmul A.a01 B.a10),
   gadd (gmul A.a00 B.a01) (gmul A.a01 B.a11),
   gadd (gmul A.a10 B.a00) (gmul A.a11 B.a10),
   gadd (gmul A.a10 B.a01) (gmul A.a11 B.a11)⟩
def gram (A : GMatrix2) : GMatrix2 := mmul (mdagger A) A
def mtrace (A : GMatrix2) : GaussianRat := gadd A.a00 A.a11
def frobeniusSquare (A : GMatrix2) : Rat :=
  gnorm A.a00 + gnorm A.a01 + gnorm A.a10 + gnorm A.a11

theorem mmul_identity_right (A : GMatrix2) : mmul A midentity = A := by
  cases A
  apply matrix_ext <;>
    apply gaussian_ext <;>
      simp only [mmul, midentity, gmul, gadd, gone, gzero] <;> grind

theorem trace_mul_add_right (A E F : GMatrix2) :
    mtrace (mmul A (madd E F)) =
      gadd (mtrace (mmul A E)) (mtrace (mmul A F)) := by
  cases A
  cases E
  cases F
  apply gaussian_ext <;>
    simp only [mtrace, mmul, madd, gadd, gmul, Rat.add_mul,
      Rat.mul_add, Rat.sub_eq_add_neg, Rat.neg_add] <;> grind

theorem trace_gram (A : GMatrix2) :
    mtrace (gram A) = ⟨frobeniusSquare A, 0⟩ := by
  cases A
  apply gaussian_ext <;>
    simp only [mtrace, gram, mmul, mdagger, frobeniusSquare, gadd, gmul,
      gconj, gnorm, Rat.neg_mul, Rat.mul_neg, Rat.sub_eq_add_neg,
      Rat.neg_add, Rat.neg_neg] <;> grind

theorem frobenius_nonnegative (A : GMatrix2) : 0 ≤ frobeniusSquare A := by
  unfold frobeniusSquare
  have h00 := gnorm_nonnegative A.a00
  have h01 := gnorm_nonnegative A.a01
  have h10 := gnorm_nonnegative A.a10
  have h11 := gnorm_nonnegative A.a11
  grind

/-- The trace numerator for two Gram factors is an exact sum of squares. -/
theorem born_numerator_identity (B C : GMatrix2) :
    mtrace (mmul (gram B) (gram C)) =
      ⟨frobeniusSquare (mmul C (mdagger B)), 0⟩ := by
  cases B
  cases C
  apply gaussian_ext <;>
    simp only [mtrace, gram, mmul, mdagger, frobeniusSquare, gadd, gmul,
      gconj, gnorm, Rat.neg_mul, Rat.mul_neg, Rat.sub_eq_add_neg,
      Rat.neg_add, Rat.neg_neg, Rat.add_mul, Rat.mul_add, Rat.mul_assoc] <;>
        grind

/-- A complete binary factor pair partitions every state's Frobenius mass. -/
theorem frame_partition (B C D : GMatrix2)
    (complete : madd (gram C) (gram D) = midentity) :
    frobeniusSquare (mmul C (mdagger B)) +
      frobeniusSquare (mmul D (mdagger B)) = frobeniusSquare B := by
  have hc := born_numerator_identity B C
  have hd := born_numerator_identity B D
  have hadd := trace_mul_add_right (gram B) (gram C) (gram D)
  have hid := mmul_identity_right (gram B)
  have hg := trace_gram B
  have chain :
      gadd
          ⟨frobeniusSquare (mmul C (mdagger B)), 0⟩
          ⟨frobeniusSquare (mmul D (mdagger B)), 0⟩ =
        ⟨frobeniusSquare B, 0⟩ := by
    calc
      gadd
          ⟨frobeniusSquare (mmul C (mdagger B)), 0⟩
          ⟨frobeniusSquare (mmul D (mdagger B)), 0⟩ =
        gadd (mtrace (mmul (gram B) (gram C)))
          (mtrace (mmul (gram B) (gram D))) := by rw [hc, hd]
      _ = mtrace (mmul (gram B) (madd (gram C) (gram D))) := hadd.symm
      _ = mtrace (mmul (gram B) midentity) := by rw [complete]
      _ = mtrace (gram B) := by rw [hid]
      _ = ⟨frobeniusSquare B, 0⟩ := hg
  exact congrArg GaussianRat.re chain

/-! ## Certified states, effects and probabilities -/

structure StateFactor where
  factor : GMatrix2
  positiveTrace : 0 < frobeniusSquare factor

structure BinaryEffectFactor where
  accept : GMatrix2
  reject : GMatrix2
  complete : madd (gram accept) (gram reject) = midentity

def probability (state : StateFactor) (effect : BinaryEffectFactor) : Rat :=
  frobeniusSquare (mmul effect.accept (mdagger state.factor)) /
    frobeniusSquare state.factor

def complementProbability (state : StateFactor) (effect : BinaryEffectFactor) : Rat :=
  frobeniusSquare (mmul effect.reject (mdagger state.factor)) /
    frobeniusSquare state.factor

theorem divide_nonnegative (a t : Rat) (ha : 0 ≤ a) (ht : 0 < t) :
    0 ≤ a / t := by
  apply Rat.le_of_mul_le_mul_right (c := t)
  · rw [Rat.div_mul_cancel (Rat.ne_of_gt ht)]
    grind
  · exact ht

theorem divide_sum_one (a b t : Rat) (sum : a + b = t) (ht : 0 < t) :
    a / t + b / t = 1 := by
  have hn : t ≠ 0 := Rat.ne_of_gt ht
  have ha := Rat.div_mul_cancel (a := a) hn
  have hb := Rat.div_mul_cancel (a := b) hn
  have htself := Rat.div_mul_cancel (a := t) hn
  grind

theorem probability_nonnegative (state : StateFactor) (effect : BinaryEffectFactor) :
    0 ≤ probability state effect :=
  divide_nonnegative _ _ (frobenius_nonnegative _) state.positiveTrace

theorem complement_probability_nonnegative
    (state : StateFactor) (effect : BinaryEffectFactor) :
    0 ≤ complementProbability state effect :=
  divide_nonnegative _ _ (frobenius_nonnegative _) state.positiveTrace

theorem probability_normalized (state : StateFactor) (effect : BinaryEffectFactor) :
    probability state effect + complementProbability state effect = 1 := by
  apply divide_sum_one
  · exact frame_partition state.factor effect.accept effect.reject effect.complete
  · exact state.positiveTrace

theorem probability_at_most_one (state : StateFactor) (effect : BinaryEffectFactor) :
    probability state effect ≤ 1 := by
  have hn := complement_probability_nonnegative state effect
  have hs := probability_normalized state effect
  grind

theorem probability_interval (state : StateFactor) (effect : BinaryEffectFactor) :
    0 ≤ probability state effect ∧ probability state effect ≤ 1 :=
  ⟨probability_nonnegative state effect, probability_at_most_one state effect⟩

/-! ## A concrete sharp qubit fixture -/

def basisStateFactor : GMatrix2 :=
  ⟨gone, gzero, gzero, gzero⟩

def acceptZeroFactor : GMatrix2 :=
  ⟨gone, gzero, gzero, gzero⟩

def rejectZeroFactor : GMatrix2 :=
  ⟨gzero, gzero, gzero, gone⟩

theorem basis_state_positive : 0 < frobeniusSquare basisStateFactor := by
  simp only [frobeniusSquare, basisStateFactor, gnorm, gone, gzero]
  grind

theorem basis_effect_complete :
    madd (gram acceptZeroFactor) (gram rejectZeroFactor) = midentity := by
  apply matrix_ext <;>
    apply gaussian_ext <;>
      simp only [madd, gram, mmul, mdagger, acceptZeroFactor,
        rejectZeroFactor, midentity, gadd, gmul, gconj, gone, gzero] <;> grind

def basisState : StateFactor := ⟨basisStateFactor, basis_state_positive⟩
def basisEffect : BinaryEffectFactor :=
  ⟨acceptZeroFactor, rejectZeroFactor, basis_effect_complete⟩

theorem basis_readout_is_sharp :
    probability basisState basisEffect = 1 ∧
      complementProbability basisState basisEffect = 0 := by
  constructor <;>
    simp only [probability, complementProbability, basisState, basisEffect,
      frobeniusSquare, mmul, mdagger, basisStateFactor, acceptZeroFactor,
      rejectZeroFactor, gadd, gmul, gconj, gnorm, gone, gzero] <;> grind

end WitnessedDifference.FiniteStateEffectReadout

#print axioms WitnessedDifference.FiniteStateEffectReadout.trace_gram
#print axioms WitnessedDifference.FiniteStateEffectReadout.frobenius_nonnegative
#print axioms WitnessedDifference.FiniteStateEffectReadout.born_numerator_identity
#print axioms WitnessedDifference.FiniteStateEffectReadout.frame_partition
#print axioms WitnessedDifference.FiniteStateEffectReadout.divide_nonnegative
#print axioms WitnessedDifference.FiniteStateEffectReadout.divide_sum_one
#print axioms WitnessedDifference.FiniteStateEffectReadout.probability_nonnegative
#print axioms WitnessedDifference.FiniteStateEffectReadout.complement_probability_nonnegative
#print axioms WitnessedDifference.FiniteStateEffectReadout.probability_normalized
#print axioms WitnessedDifference.FiniteStateEffectReadout.probability_at_most_one
#print axioms WitnessedDifference.FiniteStateEffectReadout.probability_interval
#print axioms WitnessedDifference.FiniteStateEffectReadout.basis_effect_complete
#print axioms WitnessedDifference.FiniteStateEffectReadout.basis_readout_is_sharp
