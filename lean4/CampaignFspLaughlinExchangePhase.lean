import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Data.Fintype.BigOperators
import Mathlib.Tactic

/-!
# Campaign: FSP-LAUGHLIN-EXCHANGE-PHASE (TFQ-1208) — Laughlin Jastrow Exchange Parity, Cyclotomic Monodromy Matrices, and Holomorphic / Involution Scope Fences

AuthorityEffect: None

This module narrows `FSP-LAUGHLIN-EXCHANGE-PHASE` (`TFQ-1208`, Rank 27 in `FERMION_SIGN`)
by replacing the numeric constants in `FqhLaughlinBraiding.lean` with 10 theorems proved
in Lean 4 without `sorry` or custom axioms:

1. **General-`m` Laughlin Jastrow polynomial exchange parity**:
   - `laughlin_two_body_jastrow_exchange_parity`: `(z2 - z1)^m = (-1)^m * (z1 - z2)^m` for all `m : ℕ`.
   - `laughlin_odd_m_fermionic_and_even_m_bosonic`: odd `m = 2k + 1` gives fermionic antisymmetry
     `-(z1 - z2)^(2k+1)` and even `m = 2k` gives bosonic symmetry `(z1 - z2)^(2k)`.
   - `laughlin_three_body_vandermonde_transposition_flips_sign_for_odd_m`: swapping `z1 ↔ z2`
     in the 3-body Jastrow factor `(z1 - z2)^m (z1 - z3)^m (z2 - z3)^m` negates it for all odd `m = 2k + 1`.
2. **Holomorphic quasihole symmetry fence (why Berry connection / plasma screening is required)**:
   - `laughlin_quasihole_holomorphic_polynomial_symmetric_fence`: the bare holomorphic two-quasihole
     prefactor `∏ j, (z j - η1) * (z j - η2)` is strictly symmetric under `η1 ↔ η2`, demonstrating
     that the fractional statistical phase `θ = π / m` comes from the Arovas–Schrieffer–Wilczek
     adiabatic Berry connection and plasma normalization rather than bare polynomial coordinate swap.
3. **Exact `SL(2, ℤ)` cyclotomic representation of `ν = 1/3` exchange (`π/3`) and monodromy (`2π/3`)**:
   - `laughlin_m3_exchange_companion_cyclotomic_relations`: `R6 = !![0, -1; 1, 1]` satisfies
     `det(R6) = 1`, `Tr(R6) = 1`, `R6^2 - R6 + I_2 = 0`, `R6^3 = -I_2` (`m = 3` exchanges produce
     the fermionic sign `-1`), `R6^6 = I_2`, and `R6 ∉ {I_2, -I_2}`.
   - `laughlin_m3_monodromy_cyclotomic_and_non_involution`: `M3 = R6^2 = !![-1, -1; 1, 0]` satisfies
     `det(M3) = 1`, `Tr(M3) = -1`, `I_2 + M3 + M3^2 = 0`, `M3^3 = I_2`, and `M3^2 ≠ I_2`.
4. **Abelian involution obstruction, general-`m` non-triviality, and thermal weight asymmetry fences**:
   - `no_z2_involution_matches_m3_monodromy_fence`: for every `2 × 2` integer matrix `J` with
     `J * J = 1`, `J ≠ M3` and `J ≠ R6`.
   - `general_m_monodromy_residue_and_odd_coprime`: for all `m ≥ 3`, `2 % m = 2 ≠ 0`, and for all
     `k : ℕ`, `Nat.Coprime 2 (2 * k + 1)`.
   - `abelian_anyon_modular_s_exponent_and_z3_character_sum`: the modular `S`-matrix phase exponent
     combination `a * b + 0 * 0 - a * 0 - 0 * b = a * b`, and `I_2 + M3 + M3^2 = 0`.
   - `unequal_quasihole_quasielectron_weights_prevent_z3_cancellation_fence`: for unequal weights
     `w_qh ≠ w_qe`, `w_qh • I_2 + w_qe • M3 + w_qe • M3^2 = (w_qh - w_qe) • I_2 ≠ 0`.
-/

namespace CampaignFspLaughlinExchangePhase

open Matrix BigOperators

/-- Two-body Laughlin Jastrow factor `(z1 - z2) ^ m`. -/
def jastrowTwoBody {R : Type*} [CommRing R] (m : ℕ) (z1 z2 : R) : R :=
  (z1 - z2) ^ m

/-- Theorem 1: Exchanging `z1 ↔ z2` in the two-body Laughlin Jastrow factor `(z1 - z2)^m`
multiplies it by `(-1)^m` for every `m : ℕ`. -/
theorem laughlin_two_body_jastrow_exchange_parity
    {R : Type*} [CommRing R] (m : ℕ) (z1 z2 : R) :
    jastrowTwoBody m z2 z1 = (-1 : R) ^ m * jastrowTwoBody m z1 z2 := by
  unfold jastrowTwoBody
  have hneg : z2 - z1 = (-1 : R) * (z1 - z2) := by ring
  rw [hneg, mul_pow]

/-- Theorem 2: For odd Laughlin exponent `m = 2 * k + 1`, the two-body Jastrow factor is
antisymmetric (fermionic); for even `m = 2 * k`, it is symmetric (bosonic). -/
theorem laughlin_odd_m_fermionic_and_even_m_bosonic
    {R : Type*} [CommRing R] (k : ℕ) (z1 z2 : R) :
    jastrowTwoBody (2 * k + 1) z2 z1 = -jastrowTwoBody (2 * k + 1) z1 z2 ∧
    jastrowTwoBody (2 * k) z2 z1 = jastrowTwoBody (2 * k) z1 z2 := by
  constructor
  · rw [laughlin_two_body_jastrow_exchange_parity]
    have hodd : (-1 : R) ^ (2 * k + 1) = -1 := Odd.neg_one_pow ⟨k, rfl⟩
    rw [hodd, neg_one_mul]
  · rw [laughlin_two_body_jastrow_exchange_parity]
    have heven : (-1 : R) ^ (2 * k) = 1 := Even.neg_one_pow ⟨k, by omega⟩
    rw [heven, one_mul]

/-- Three-body Laughlin Jastrow factor `(z1 - z2)^m * (z1 - z3)^m * (z2 - z3)^m`. -/
def jastrowThreeBody {R : Type*} [CommRing R] (m : ℕ) (z1 z2 z3 : R) : R :=
  (z1 - z2) ^ m * (z1 - z3) ^ m * (z2 - z3) ^ m

/-- Theorem 3: For every odd Laughlin exponent `m = 2 * k + 1`, transposing `z1 ↔ z2`
in the three-body Laughlin Jastrow factor negates the polynomial, because `(z1 - z2)^m`
flips sign while `(z1 - z3)^m` and `(z2 - z3)^m` swap places. -/
theorem laughlin_three_body_vandermonde_transposition_flips_sign_for_odd_m
    {R : Type*} [CommRing R] (k : ℕ) (z1 z2 z3 : R) :
    jastrowThreeBody (2 * k + 1) z2 z1 z3 = -jastrowThreeBody (2 * k + 1) z1 z2 z3 := by
  unfold jastrowThreeBody
  have h12 : (z2 - z1) ^ (2 * k + 1) = -((z1 - z2) ^ (2 * k + 1)) :=
    (laughlin_odd_m_fermionic_and_even_m_bosonic k z1 z2).1
  rw [h12]
  ring

/-- Bare holomorphic two-quasihole prefactor `∏ j, (z j - η1) * (z j - η2)`. -/
def twoQuasiholePrefactor {ι : Type*} [Fintype ι] {R : Type*} [CommRing R]
    (z : ι → R) (eta1 eta2 : R) : R :=
  ∏ j : ι, ((z j - eta1) * (z j - eta2))

/-- Theorem 4 (Scope Fence — Bare Holomorphic Quasihole Polynomial Symmetry):
The bare holomorphic two-quasihole polynomial `twoQuasiholePrefactor z eta1 eta2` is
strictly symmetric under `eta1 ↔ eta2`. Therefore, the fractional statistical phase
`θ = π / m` does not arise from algebraic substitution `eta1 ↔ eta2` alone; it requires
the Arovas–Schrieffer–Wilczek adiabatic Berry connection / plasma normalization integral. -/
theorem laughlin_quasihole_holomorphic_polynomial_symmetric_fence
    {ι : Type*} [Fintype ι] {R : Type*} [CommRing R]
    (z : ι → R) (eta1 eta2 : R) :
    twoQuasiholePrefactor z eta2 eta1 = twoQuasiholePrefactor z eta1 eta2 := by
  unfold twoQuasiholePrefactor
  refine Finset.prod_congr rfl (fun j _ => ?_)
  ring

/-- `SL(2, ℤ)` companion matrix `R6` of the primitive 6th root of unity `exp(i π / 3)`,
representing the elementary `ν = 1/3` quasihole exchange phase `θ = π / 3`. -/
def exchangeR6 : Matrix (Fin 2) (Fin 2) ℤ :=
  !![0, -1;
     1,  1]

/-- `SL(2, ℤ)` companion matrix `M3 = R6^2` of the primitive 3rd root of unity `exp(i 2π / 3)`,
representing the full `ν = 1/3` braiding monodromy `2θ = 2π / 3`. -/
def monodromyM3 : Matrix (Fin 2) (Fin 2) ℤ :=
  !![-1, -1;
      1,  0]

/-- Theorem 5: The `ν = 1/3` exchange matrix `exchangeR6` has unit determinant, trace `1`
(`2 cos(π/3) = 1`), satisfies the 6th cyclotomic equation `R6^2 - R6 + I_2 = 0`, cubes to
`-I_2` (three `π/3` exchanges yield the fermionic sign `-1`), has sixth power `I_2`, and is
neither `+I_2` nor `-I_2`. -/
theorem laughlin_m3_exchange_companion_cyclotomic_relations :
    exchangeR6.det = 1 ∧
    Matrix.trace exchangeR6 = 1 ∧
    exchangeR6 * exchangeR6 - exchangeR6 + 1 = 0 ∧
    exchangeR6 ^ 3 = -1 ∧
    exchangeR6 ^ 6 = 1 ∧
    exchangeR6 ≠ 1 ∧
    exchangeR6 ≠ -1 := by
  decide

/-- Theorem 6: The `ν = 1/3` monodromy matrix `monodromyM3` equals `exchangeR6^2`, has unit
determinant and trace `-1` (`2 cos(2π/3) = -1`), satisfies the 3rd cyclotomic equation
`I_2 + M3 + M3^2 = 0`, has order `3` (`M3^3 = I_2`), and is not an involution (`M3 * M3 ≠ I_2`). -/
theorem laughlin_m3_monodromy_cyclotomic_and_non_involution :
    monodromyM3 = exchangeR6 * exchangeR6 ∧
    monodromyM3.det = 1 ∧
    Matrix.trace monodromyM3 = -1 ∧
    1 + monodromyM3 + monodromyM3 * monodromyM3 = 0 ∧
    monodromyM3 ^ 3 = 1 ∧
    monodromyM3 * monodromyM3 ≠ 1 := by
  decide

/-- Theorem 7 (Scope Fence — No `Z₂` Involution Matches the `ν = 1/3` Anyonic Phase):
For any `2 × 2` integer matrix `J` satisfying the involution identity `J * J = 1`,
`J` cannot equal `monodromyM3` or `exchangeR6`. -/
theorem no_z2_involution_matches_m3_monodromy_fence
    (J : Matrix (Fin 2) (Fin 2) ℤ) (hJ : J * J = 1) :
    J ≠ monodromyM3 ∧ J ≠ exchangeR6 := by
  constructor
  · intro h_eq
    rw [h_eq] at hJ
    exact laughlin_m3_monodromy_cyclotomic_and_non_involution.2.2.2.2.2 hJ
  · intro h_eq
    rw [h_eq] at hJ
    have hne : exchangeR6 * exchangeR6 ≠ (1 : Matrix (Fin 2) (Fin 2) ℤ) := by decide
    exact hne hJ

/-- Theorem 8: For every integer `m ≥ 3`, the two-exchange monodromy numerator `2` has
nonzero residue `2 % m = 2 ≠ 0` (so the `2π / m` monodromy is non-contractible modulo `2π`),
and for every odd denominator `m = 2 * k + 1`, `gcd(2, 2 * k + 1) = 1`. -/
theorem general_m_monodromy_residue_and_odd_coprime
    (m k : ℕ) (hm : 3 ≤ m) :
    2 % m = 2 ∧ 2 % m ≠ 0 ∧ Nat.gcd 2 (2 * k + 1) = 1 := by
  have hlt : 2 < m := by omega
  have hmod : 2 % m = 2 := Nat.mod_eq_of_lt hlt
  have hcop : Nat.Coprime 2 (2 * k + 1) := by
    rw [Nat.Prime.coprime_iff_not_dvd Nat.prime_two]
    omega
  exact ⟨hmod, by omega, hcop⟩

/-- Unnormalized modular `S`-matrix phase exponent `e(a, b) = a * b` for abelian `Z_m` anyons. -/
def modularSPhaseExponent (a b : ℤ) : ℤ := a * b

/-- Theorem 9: The modular `S`-matrix monodromy exponent combination
`e(a, b) + e(0, 0) - e(a, 0) - e(0, b)` equals `a * b` for all anyon charges `a, b : ℤ`,
and the three `Z_3` monodromy sector matrices `I_2`, `M3`, `M3^2` sum to zero. -/
theorem abelian_anyon_modular_s_exponent_and_z3_character_sum
    (a b : ℤ) :
    modularSPhaseExponent a b + modularSPhaseExponent 0 0 -
      modularSPhaseExponent a 0 - modularSPhaseExponent 0 b = a * b ∧
    (1 : Matrix (Fin 2) (Fin 2) ℤ) + monodromyM3 + monodromyM3 * monodromyM3 = 0 := by
  refine ⟨?_, by decide⟩
  unfold modularSPhaseExponent
  ring

/-- Theorem 10 (Scope Fence — Quasihole/Quasielectron Weight Asymmetry Breaks `Z₃` Cancellation):
While equal weights across `(I_2, M3, M3^2)` cancel to `0`, any unequal quasihole and
quasielectron weights `w_qh ≠ w_qe` leave a residual diagonal matrix
`w_qh • I_2 + w_qe • M3 + w_qe • M3^2 = (w_qh - w_qe) • I_2 ≠ 0`. -/
theorem unequal_quasihole_quasielectron_weights_prevent_z3_cancellation_fence
    (w_qh w_qe : ℤ) (hne : w_qh ≠ w_qe) :
    w_qh • (1 : Matrix (Fin 2) (Fin 2) ℤ) + w_qe • monodromyM3 +
      w_qe • (monodromyM3 * monodromyM3) =
      (w_qh - w_qe) • (1 : Matrix (Fin 2) (Fin 2) ℤ) ∧
    w_qh • (1 : Matrix (Fin 2) (Fin 2) ℤ) + w_qe • monodromyM3 +
      w_qe • (monodromyM3 * monodromyM3) ≠ 0 := by
  have hsum : (1 : Matrix (Fin 2) (Fin 2) ℤ) + monodromyM3 + monodromyM3 * monodromyM3 = 0 := by
    decide
  have hM : monodromyM3 + monodromyM3 * monodromyM3 = -(1 : Matrix (Fin 2) (Fin 2) ℤ) := by
    decide
  have hcomb :
      w_qh • (1 : Matrix (Fin 2) (Fin 2) ℤ) + w_qe • monodromyM3 +
        w_qe • (monodromyM3 * monodromyM3) =
        (w_qh - w_qe) • (1 : Matrix (Fin 2) (Fin 2) ℤ) := by
    calc
      w_qh • (1 : Matrix (Fin 2) (Fin 2) ℤ) + w_qe • monodromyM3 +
          w_qe • (monodromyM3 * monodromyM3)
        = w_qh • (1 : Matrix (Fin 2) (Fin 2) ℤ) +
            w_qe • (monodromyM3 + monodromyM3 * monodromyM3) := by
          rw [smul_add, add_assoc]
      _ = w_qh • (1 : Matrix (Fin 2) (Fin 2) ℤ) +
            w_qe • (-(1 : Matrix (Fin 2) (Fin 2) ℤ)) := by
          rw [hM]
      _ = (w_qh - w_qe) • (1 : Matrix (Fin 2) (Fin 2) ℤ) := by
          rw [smul_neg, sub_smul]
          abel
  refine ⟨hcomb, ?_⟩
  rw [hcomb]
  intro hzero
  have h00 := congr_fun (congr_fun hzero 0) 0
  simp at h00
  omega

#print axioms laughlin_two_body_jastrow_exchange_parity
#print axioms laughlin_odd_m_fermionic_and_even_m_bosonic
#print axioms laughlin_three_body_vandermonde_transposition_flips_sign_for_odd_m
#print axioms laughlin_quasihole_holomorphic_polynomial_symmetric_fence
#print axioms laughlin_m3_exchange_companion_cyclotomic_relations
#print axioms laughlin_m3_monodromy_cyclotomic_and_non_involution
#print axioms no_z2_involution_matches_m3_monodromy_fence
#print axioms general_m_monodromy_residue_and_odd_coprime
#print axioms abelian_anyon_modular_s_exponent_and_z3_character_sum
#print axioms unequal_quasihole_quasielectron_weights_prevent_z3_cancellation_fence

end CampaignFspLaughlinExchangePhase
