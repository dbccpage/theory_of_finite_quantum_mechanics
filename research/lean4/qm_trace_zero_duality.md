/-
  Trace-zero ℓ¹ / diameter duality — the combinatorial core of Paper 005's S1 / Theorem 5.

  Paper: research/published/005_CPTP-Invariant Obstruction Theory ... .md
         (Theorem 5 "Trace-zero dual ball" lemma; Support Ledger S1/S7).

  The quantum trace-zero dual-ball lemma reduces, via the spectral theorem (unitary
  invariance), to a statement about the eigenvalue vector. This file machine-checks that
  eigenvalue-level core, quantum-free:

    for a sum-zero  x : Fin n → ℝ,   (1/2) * ∑ |x i|  =  max { ⟨m, x⟩ : diam(m) ≤ 1 },

  where the diameter constraint `diam(m) ≤ 1` is encoded as `∃ c, ∀ i, |m i - c| ≤ 1/2`
  (the center `c` is the spectral midpoint; this is exactly `max_i m_i − min_i m_i ≤ 1`).
  The maximizer is `m i = (1/2)·sign(x i)`.

  This is the centered-representative argument of the paper's lemma, at the eigenvalue level:
  the upper bound is discrete Hölder after subtracting the (free, since ∑ x = 0) center;
  attainment is the explicit sign witness. The lift to the Hermitian-matrix statement uses
  only `Matrix.IsHermitian.spectral_theorem` (unitary invariance ⇒ reduce to eigenvalues),
  which is left to the paper's prose. The maximizer is NOT unique when some `x i = 0`
  (sign(0) is free), so the result is stated with an ∃-witness, not uniqueness.
-/
import Mathlib

namespace TraceZeroDuality

open Finset

variable {n : ℕ}

/-- The sign witness `m i = (1/2)·sign(x i)` (with `sign 0 := 1`). Noncomputable because the
real comparison `0 ≤ x i` uses classical decidability; it is a proof artifact, never run. -/
noncomputable def signWitness (x : Fin n → ℝ) : Fin n → ℝ :=
  fun i => (1/2) * (if 0 ≤ x i then 1 else -1)

/-- The witness has diameter ≤ 1, with center `c = 0` (i.e. `‖·‖_∞ ≤ 1/2`). -/
theorem signWitness_feasible (x : Fin n → ℝ) (i : Fin n) :
    |signWitness x i - 0| ≤ 1/2 := by
  unfold signWitness
  rw [sub_zero, abs_le]
  by_cases h : 0 ≤ x i
  · rw [if_pos h]
    constructor <;> linarith
  · rw [if_neg h]
    constructor <;> linarith

/-- The witness attains `(1/2) ∑ |x i|`. -/
theorem signWitness_value (x : Fin n → ℝ) :
    ∑ i, signWitness x i * x i = (1/2) * ∑ i, |x i| := by
  have step : ∀ i, signWitness x i * x i = (1/2) * |x i| := by
    intro i
    unfold signWitness
    by_cases h : 0 ≤ x i
    · rw [if_pos h, abs_of_nonneg h]
      ring
    · have h2 : x i < 0 := not_le.mp h
      rw [if_neg h, abs_of_neg h2]
      ring
  have sum_eq : ∑ i, signWitness x i * x i = ∑ i, (1/2) * |x i| := Finset.sum_congr rfl (fun i _ => step i)
  rw [sum_eq, ← Finset.mul_sum]

/-- **Upper bound (dual feasibility ⇒ ≤ ½‖x‖₁).** For a sum-zero vector `x`, any `m` of
diameter ≤ 1 (witnessed by a center `c` with `|m i − c| ≤ 1/2`) pairs against `x` below
`(1/2) ∑ |x i|`. Pure discrete Hölder after subtracting the center, which is free because
`∑ x = 0`. -/
theorem pairing_le (x m : Fin n → ℝ) (hx : ∑ i, x i = 0)
    (c : ℝ) (hc : ∀ i, |m i - c| ≤ 1/2) :
    ∑ i, m i * x i ≤ (1/2) * ∑ i, |x i| := by
  have hshift : ∑ i, m i * x i = ∑ i, (m i - c) * x i := by
    have h1 : ∀ i, (m i - c) * x i = m i * x i - c * x i := fun i => sub_mul (m i) c (x i)
    have h2 : ∑ i, (m i - c) * x i = ∑ i, (m i * x i - c * x i) := Finset.sum_congr rfl (fun i _ => h1 i)
    rw [h2, Finset.sum_sub_distrib, ← Finset.mul_sum]
    rw [hx, mul_zero, sub_zero]
  rw [hshift, Finset.mul_sum]
  refine Finset.sum_le_sum (fun i _ => ?_)
  calc (m i - c) * x i
      ≤ |(m i - c) * x i| := le_abs_self _
    _ = |m i - c| * |x i| := abs_mul _ _
    _ ≤ (1/2) * |x i| := mul_le_mul_of_nonneg_right (hc i) (abs_nonneg _)

/-- **The duality value (the eigenvalue-level core of S1).** For a sum-zero `x`,
`(1/2) ∑ |x i|` is the GREATEST value of `⟨m, x⟩` over the diameter-≤1 ball
`{ m : ∃ c, ∀ i, |m i − c| ≤ 1/2 }`. -/
theorem half_l1_isGreatest (x : Fin n → ℝ) (hx : ∑ i, x i = 0) :
    IsGreatest
      { v : ℝ | ∃ m : Fin n → ℝ, (∃ c, ∀ i, |m i - c| ≤ 1/2) ∧ v = ∑ i, m i * x i }
      ((1/2) * ∑ i, |x i|) := by
  constructor
  · exact ⟨signWitness x, ⟨0, signWitness_feasible x⟩, (signWitness_value x).symm⟩
  · rintro v ⟨m, ⟨c, hc⟩, rfl⟩
    exact pairing_le x m hx c hc

end TraceZeroDuality

-- Axiom audit: expected exactly the standard trio (propext, Classical.choice, Quot.sound).
#print axioms TraceZeroDuality.half_l1_isGreatest
