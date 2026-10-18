import CharacterOrthogonality
import Mathlib.Analysis.SpecificLimits.Basic


namespace FiniteToContinuum

set_option autoImplicit false

open scoped BigOperators Topology
open MeasureTheory Filter

instance : Fact (0 < (1 : ℝ)) := ⟨zero_lt_one⟩

theorem cyclic_embedding_injective (N : ℕ) [NeZero N] :
    Function.Injective (ZMod.toAddCircle : ZMod N → UnitAddCircle) :=
  ZMod.toAddCircle_injective N

noncomputable def circleCharacter (N : ℕ) [NeZero N] (k : ℤ) :
    AdditiveChar (ZMod N) ℂ where
  toFun x := (AddCircle.toCircle (ZMod.toAddCircle ((k : ZMod N) * x)) : ℂ)
  map_zero' := by simp [AddCircle.toCircle_zero]
  map_add' x y := by
    simp only [mul_add, map_add, AddCircle.toCircle_add, Circle.coe_mul]

theorem circleCharacter_restriction (N : ℕ) [NeZero N] (k : ℤ) (x : ZMod N) :
    circleCharacter N k x = fourier k (ZMod.toAddCircle x) := by
  simp [circleCharacter, fourier_apply, ← map_zsmul, zsmul_eq_mul]

theorem circleCharacter_trivial_iff (N : ℕ) [NeZero N] (k : ℤ) :
    (∀ x, circleCharacter N k x = 1) ↔ (N : ℤ) ∣ k := by
  rw [← ZMod.intCast_zmod_eq_zero_iff_dvd]
  constructor
  · intro h
    have hcircle : AddCircle.toCircle (ZMod.toAddCircle (k : ZMod N)) = 1 := by
      apply Subtype.ext
      simpa [circleCharacter] using h 1
    have hzero : ZMod.toAddCircle (k : ZMod N) = 0 := by
      apply AddCircle.injective_toCircle one_ne_zero
      simpa [AddCircle.toCircle_zero] using hcircle
    exact ZMod.toAddCircle_eq_zero.mp hzero
  · intro h x
    simp [circleCharacter, h, AddCircle.toCircle_zero]

noncomputable def finiteCircleAverage (N : ℕ) [NeZero N] (k : ℤ) : ℂ :=
  (N : ℂ)⁻¹ * ∑ x : ZMod N, circleCharacter N k x

theorem finiteCircleAverage_eq (N : ℕ) [NeZero N] (k : ℤ) :
    finiteCircleAverage N k = if (N : ℤ) ∣ k then 1 else 0 := by
  have h := normalized_character_sum (circleCharacter N k)
    (by simpa using (Nat.cast_ne_zero.mpr (NeZero.ne N) : (N : ℂ) ≠ 0))
  simpa [finiteCircleAverage, ZMod.card, circleCharacter_trivial_iff] using h

noncomputable def circleHaar (k : ℤ) : ℂ :=
  ∫ x : UnitAddCircle, fourier k x ∂AddCircle.haarAddCircle

theorem circleHaar_eq (k : ℤ) : circleHaar k = if k = 0 then 1 else 0 := by
  have h := congrFun (fourierCoeff_fourier (T := 1) k) 0
  simpa [circleHaar, fourierCoeff, fourier_zero,
    Pi.single_apply, eq_comm] using h

theorem finiteCircleAverage_eq_haar (N : ℕ) [NeZero N] (k : ℤ)
    (hbound : k.natAbs < N) : finiteCircleAverage N k = circleHaar k := by
  rw [finiteCircleAverage_eq, circleHaar_eq]
  by_cases hk : k = 0
  · simp [hk]
  · have hnot : ¬ (N : ℤ) ∣ k := by
      intro hdvd
      exact hk (Int.eq_zero_of_dvd_of_natAbs_lt_natAbs hdvd (by simpa using hbound))
    simp [hk, hnot]

theorem dyadic_character_haar_limit (k : ℤ) :
    Tendsto (fun n : ℕ => finiteCircleAverage (2 ^ n) k) atTop (𝓝 (circleHaar k)) := by
  apply tendsto_const_nhds.congr'
  filter_upwards [eventually_ge_atTop k.natAbs] with n hn
  exact (finiteCircleAverage_eq_haar (2 ^ n) k
    (lt_of_le_of_lt hn Nat.lt_two_pow_self)).symm

theorem polynomial_haar_limit (s : Finset ℤ) (c : ℤ → ℂ) :
    Tendsto (fun n : ℕ => ∑ k ∈ s, c k * finiteCircleAverage (2 ^ n) k)
      atTop (𝓝 (∑ k ∈ s, c k * circleHaar k)) := by
  exact tendsto_finsetSum s (fun k _ => tendsto_const_nhds.mul (dyadic_character_haar_limit k))

theorem polynomial_haar_integral (s : Finset ℤ) (c : ℤ → ℂ) :
    (∫ x : UnitAddCircle, ∑ k ∈ s, c k * fourier k x ∂AddCircle.haarAddCircle) =
      ∑ k ∈ s, c k * circleHaar k := by
  have hint : ∀ k ∈ s, Integrable (fun x : UnitAddCircle => c k * fourier k x)
      AddCircle.haarAddCircle := by
    intro k _
    exact (continuous_const.mul (map_continuous (fourier k))).integrable_of_hasCompactSupport
      (HasCompactSupport.of_compactSpace _)
  rw [integral_finsetSum s hint]
  apply Finset.sum_congr rfl
  intro k _
  exact integral_const_mul (c k) (fun x => fourier k x)

theorem polynomial_continuous_haar_limit (s : Finset ℤ) (c : ℤ → ℂ) :
    Tendsto (fun n : ℕ => ∑ k ∈ s, c k * finiteCircleAverage (2 ^ n) k) atTop
      (𝓝 (∫ x : UnitAddCircle, ∑ k ∈ s, c k * fourier k x ∂AddCircle.haarAddCircle)) := by
  rw [polynomial_haar_integral]
  exact polynomial_haar_limit s c

end FiniteToContinuum
