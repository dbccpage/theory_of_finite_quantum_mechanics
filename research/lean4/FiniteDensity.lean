-- Finite Quantum Density Matrices in Lean 4
-- AuthorityEffect: None

namespace FromPrimitiveDifferenceToQuantumMechanics.FiniteDensity

/-- A diagonalized 2-state finite density spectrum with non-negative eigenvalues summing to denominator. -/
structure FiniteDensity2 where
  lambda0 : Nat
  lambda1 : Nat
  denominator : Nat
  h_denom_pos : denominator > 0
  h_unit_trace : lambda0 + lambda1 = denominator

def trace (d : FiniteDensity2) : Nat :=
  d.lambda0 + d.lambda1

theorem density_is_positive_unit_trace (d : FiniteDensity2) :
    trace d = d.denominator := by
  dsimp [trace]
  exact d.h_unit_trace

/-- Born probability for a binary projective measurement on finite density states. -/
structure ProjectiveEffect where
  coeff0 : Nat
  coeff1 : Nat
  h_bound0 : coeff0 ≤ 1
  h_bound1 : coeff1 ≤ 1

def born_expected_numerator (d : FiniteDensity2) (e : ProjectiveEffect) : Nat :=
  d.lambda0 * e.coeff0 + d.lambda1 * e.coeff1

theorem born_probability_in_unit_interval (d : FiniteDensity2) (e : ProjectiveEffect) :
    born_expected_numerator d e ≤ d.denominator := by
  dsimp [born_expected_numerator]
  have h0 : d.lambda0 * e.coeff0 ≤ d.lambda0 * 1 := Nat.mul_le_mul_left d.lambda0 e.h_bound0
  have h1 : d.lambda1 * e.coeff1 ≤ d.lambda1 * 1 := Nat.mul_le_mul_left d.lambda1 e.h_bound1
  rw [Nat.mul_one] at h0 h1
  have h_sum := Nat.add_le_add h0 h1
  rw [d.h_unit_trace] at h_sum
  exact h_sum

end FromPrimitiveDifferenceToQuantumMechanics.FiniteDensity

/- ------------------------------------------------------------------
   Merged from derive_genesis_foundational_docs (PR #203).
   Distinct namespace from the block above; both are retained.
   ------------------------------------------------------------------ -/

-- Finite Quantum Density Matrices in Lean 4
-- AuthorityEffect: None

namespace FiniteDensity

/-- A discrete 2-state diagonal density spectrum represented as non-negative integer weights
    `lambda0`, `lambda1` normalized by a common positive integer `denominator`.
    This models a discrete rational probability distribution over 2 orthogonal states. -/
structure FiniteDensity2 where
  lambda0 : Nat
  lambda1 : Nat
  denominator : Nat
  h_denom_pos : denominator > 0
  h_unit_trace : lambda0 + lambda1 = denominator

/-- Trace of the 2-state diagonal density, defined as the sum of its unnormalized eigenvalues. -/
def trace (d : FiniteDensity2) : Nat :=
  d.lambda0 + d.lambda1

/-- Verification of unit trace: the sum of diagonal weights equals the declared denominator. -/
theorem density_is_positive_unit_trace (d : FiniteDensity2) :
    trace d = d.denominator := by
  dsimp [trace]
  exact d.h_unit_trace

/-- A discrete binary measurement effect with rational evaluation coefficients in [0, 1],
    represented as integer numerators `coeff0, coeff1 ≤ 1`. -/
structure ProjectiveEffect where
  coeff0 : Nat
  coeff1 : Nat
  h_bound0 : coeff0 ≤ 1
  h_bound1 : coeff1 ≤ 1

/-- Born rule expected outcome numerator: Tr(E ρ) * denominator = λ0 * c0 + λ1 * c1. -/
def born_expected_numerator (d : FiniteDensity2) (e : ProjectiveEffect) : Nat :=
  d.lambda0 * e.coeff0 + d.lambda1 * e.coeff1

/-- Upper bound: the Born rule expectation numerator never exceeds the denominator,
    ensuring that the associated probability (numerator / denominator) is ≤ 1. -/
theorem born_probability_in_unit_interval (d : FiniteDensity2) (e : ProjectiveEffect) :
    born_expected_numerator d e ≤ d.denominator := by
  dsimp [born_expected_numerator]
  have h0 : d.lambda0 * e.coeff0 ≤ d.lambda0 * 1 := Nat.mul_le_mul_left d.lambda0 e.h_bound0
  have h1 : d.lambda1 * e.coeff1 ≤ d.lambda1 * 1 := Nat.mul_le_mul_left d.lambda1 e.h_bound1
  rw [Nat.mul_one] at h0 h1
  have h_sum := Nat.add_le_add h0 h1
  rw [d.h_unit_trace] at h_sum
  exact h_sum

/-- Lower bound: the Born expectation numerator is non-negative (≥ 0). -/
theorem born_probability_nonneg (d : FiniteDensity2) (e : ProjectiveEffect) :
    born_expected_numerator d e ≥ 0 := by
  dsimp [born_expected_numerator]
  exact Nat.zero_le _

/-- Convex combination of two discrete 2-state densities:
    Given weights wA, wB, the mixture of states dA, dB
    yields an unnormalized spectrum whose trace equals wA * dA.denominator + wB * dB.denominator. -/
def mix_eigenvalues (dA dB : FiniteDensity2) (wA wB : Nat) : Nat × Nat :=
  (wA * dA.lambda0 + wB * dB.lambda0, wA * dA.lambda1 + wB * dB.lambda1)

theorem convex_mixture_trace (dA dB : FiniteDensity2) (wA wB : Nat) :
    (mix_eigenvalues dA dB wA wB).1 + (mix_eigenvalues dA dB wA wB).2 =
    wA * dA.denominator + wB * dB.denominator := by
  dsimp [mix_eigenvalues]
  have h1 : (wA * dA.lambda0 + wB * dB.lambda0) + (wA * dA.lambda1 + wB * dB.lambda1) =
            (wA * dA.lambda0 + wA * dA.lambda1) + (wB * dB.lambda0 + wB * dB.lambda1) := by omega
  rw [h1]
  rw [← Nat.mul_add wA dA.lambda0 dA.lambda1]
  rw [← Nat.mul_add wB dB.lambda0 dB.lambda1]
  rw [dA.h_unit_trace, dB.h_unit_trace]

#print axioms density_is_positive_unit_trace
#print axioms born_probability_in_unit_interval
#print axioms born_probability_nonneg
#print axioms convex_mixture_trace

end FiniteDensity
