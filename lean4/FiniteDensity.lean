

namespace FromPrimitiveDifferenceToQuantumMechanics.FiniteDensity

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



namespace FiniteDensity

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

theorem born_probability_nonneg (d : FiniteDensity2) (e : ProjectiveEffect) :
    born_expected_numerator d e ≥ 0 := by
  dsimp [born_expected_numerator]
  exact Nat.zero_le _

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

private def l5aProvenance : String :=
  "Origin: lean4/FiniteDensity.lean Claim: density_is_positive_unit_trace AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
