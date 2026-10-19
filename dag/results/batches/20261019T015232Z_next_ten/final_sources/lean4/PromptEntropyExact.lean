import EntropyDichotomy
import Mathlib.Analysis.SpecialFunctions.Log.Deriv

/- BakerCitedInput is an explicit argument, not proved or supplied by a flag.
   Entropy uses natural logarithms. AuthorityEffect: None. -/
namespace QuantumMechanics.PromptEntropyExact
theorem zero_iff_pure {d : ℕ} (s : C750B01.AlgebraicSpectrum d) :
    C750B01.entropy s = 0 ↔ C750B01.Pure s := C750B01.entropy_zero_iff_pure s
theorem mixed_positive {d : ℕ} (s : C750B01.AlgebraicSpectrum d) (h : ¬ C750B01.Pure s) :
    0 < C750B01.entropy s := C750B01.mixed_entropy_positive s h
theorem mixed_transcendental_requires_Baker (baker : C750B01.BakerCitedInput)
    {d : ℕ} (s : C750B01.AlgebraicSpectrum d) (h : ¬ C750B01.Pure s) :
    Transcendental ℚ (C750B01.entropy s) := C750B01.mixed_entropy_transcendental baker s h
theorem general_dichotomy_requires_Baker (baker : C750B01.BakerCitedInput)
    {d : ℕ} (s : C750B01.AlgebraicSpectrum d) :
    C750B01.entropy s = 0 ∨ Transcendental ℚ (C750B01.entropy s) :=
  C750B01.entropy_dichotomy_general_dimension baker s
theorem nonzero_coefficients_can_cancel : Real.log 4 - 2 * Real.log 2 = 0 :=
  C750B01.vanishing_log_control
theorem actual_log_series {x : ℝ} (h : |x| < 1) :
    HasSum (fun k : ℕ => (2 : ℝ) * (1 / (2 * k + 1)) * x ^ (2 * k + 1))
      (Real.log (1 + x) - Real.log (1 - x)) :=
  Real.hasSum_log_sub_log_of_abs_lt_one h
end QuantumMechanics.PromptEntropyExact
#print axioms QuantumMechanics.PromptEntropyExact.zero_iff_pure
#print axioms QuantumMechanics.PromptEntropyExact.mixed_positive
#print axioms QuantumMechanics.PromptEntropyExact.mixed_transcendental_requires_Baker
#print axioms QuantumMechanics.PromptEntropyExact.general_dichotomy_requires_Baker
#print axioms QuantumMechanics.PromptEntropyExact.nonzero_coefficients_can_cancel
#print axioms QuantumMechanics.PromptEntropyExact.actual_log_series
