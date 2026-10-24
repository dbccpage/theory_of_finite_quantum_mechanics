/-
Exact algebraic model; AuthorityEffect: None.
Jastrow exchange identities hold in commutative rings. A supplied 2x2 integer companion matrix and its square satisfy cyclotomic identities and fail involution tests. The quasihole polynomial is symmetric. The matrix model is not identified with a physical Berry holonomy, and symmetry alone does not derive a Berry phase or its physical origin.
Historical names are labels; their physical or operational interpretations require separate evidence.
-/

import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Data.Fintype.BigOperators
import Mathlib.Tactic



namespace CampaignFspLaughlinExchangePhase

open Matrix BigOperators


def jastrowTwoBody {R : Type*} [CommRing R] (m : ℕ) (z1 z2 : R) : R :=
  (z1 - z2) ^ m


theorem laughlin_two_body_jastrow_exchange_parity
    {R : Type*} [CommRing R] (m : ℕ) (z1 z2 : R) :
    jastrowTwoBody m z2 z1 = (-1 : R) ^ m * jastrowTwoBody m z1 z2 := by
  unfold jastrowTwoBody
  have hneg : z2 - z1 = (-1 : R) * (z1 - z2) := by ring
  rw [hneg, mul_pow]


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


def jastrowThreeBody {R : Type*} [CommRing R] (m : ℕ) (z1 z2 z3 : R) : R :=
  (z1 - z2) ^ m * (z1 - z3) ^ m * (z2 - z3) ^ m


theorem laughlin_three_body_vandermonde_transposition_flips_sign_for_odd_m
    {R : Type*} [CommRing R] (k : ℕ) (z1 z2 z3 : R) :
    jastrowThreeBody (2 * k + 1) z2 z1 z3 = -jastrowThreeBody (2 * k + 1) z1 z2 z3 := by
  unfold jastrowThreeBody
  have h12 : (z2 - z1) ^ (2 * k + 1) = -((z1 - z2) ^ (2 * k + 1)) :=
    (laughlin_odd_m_fermionic_and_even_m_bosonic k z1 z2).1
  rw [h12]
  ring


def twoQuasiholePrefactor {ι : Type*} [Fintype ι] {R : Type*} [CommRing R]
    (z : ι → R) (eta1 eta2 : R) : R :=
  ∏ j : ι, ((z j - eta1) * (z j - eta2))


theorem laughlin_quasihole_holomorphic_polynomial_symmetric_fence
    {ι : Type*} [Fintype ι] {R : Type*} [CommRing R]
    (z : ι → R) (eta1 eta2 : R) :
    twoQuasiholePrefactor z eta2 eta1 = twoQuasiholePrefactor z eta1 eta2 := by
  unfold twoQuasiholePrefactor
  refine Finset.prod_congr rfl (fun j _ => ?_)
  ring


def exchangeR6 : Matrix (Fin 2) (Fin 2) ℤ :=
  !![0, -1;
     1,  1]


def monodromyM3 : Matrix (Fin 2) (Fin 2) ℤ :=
  !![-1, -1;
      1,  0]


theorem laughlin_m3_exchange_companion_cyclotomic_relations :
    exchangeR6.det = 1 ∧
    Matrix.trace exchangeR6 = 1 ∧
    exchangeR6 * exchangeR6 - exchangeR6 + 1 = 0 ∧
    exchangeR6 ^ 3 = -1 ∧
    exchangeR6 ^ 6 = 1 ∧
    exchangeR6 ≠ 1 ∧
    exchangeR6 ≠ -1 := by
  decide


theorem laughlin_m3_monodromy_cyclotomic_and_non_involution :
    monodromyM3 = exchangeR6 * exchangeR6 ∧
    monodromyM3.det = 1 ∧
    Matrix.trace monodromyM3 = -1 ∧
    1 + monodromyM3 + monodromyM3 * monodromyM3 = 0 ∧
    monodromyM3 ^ 3 = 1 ∧
    monodromyM3 * monodromyM3 ≠ 1 := by
  decide


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


theorem general_m_monodromy_residue_and_odd_coprime
    (m k : ℕ) (hm : 3 ≤ m) :
    2 % m = 2 ∧ 2 % m ≠ 0 ∧ Nat.gcd 2 (2 * k + 1) = 1 := by
  have hlt : 2 < m := by omega
  have hmod : 2 % m = 2 := Nat.mod_eq_of_lt hlt
  have hcop : Nat.Coprime 2 (2 * k + 1) := by
    rw [Nat.Prime.coprime_iff_not_dvd Nat.prime_two]
    omega
  exact ⟨hmod, by omega, hcop⟩


def modularSPhaseExponent (a b : ℤ) : ℤ := a * b


theorem abelian_anyon_modular_s_exponent_and_z3_character_sum
    (a b : ℤ) :
    modularSPhaseExponent a b + modularSPhaseExponent 0 0 -
      modularSPhaseExponent a 0 - modularSPhaseExponent 0 b = a * b ∧
    (1 : Matrix (Fin 2) (Fin 2) ℤ) + monodromyM3 + monodromyM3 * monodromyM3 = 0 := by
  refine ⟨?_, by decide⟩
  unfold modularSPhaseExponent
  ring


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
