import HigherCell.Core
import HigherCell.Theorem41_Idempotence

/-!
  # HigherCell.Theorem42_Isolation — Conditional One-Site and Tangent Isolation
  Formal proofs for:
  1. 1-Local Tangent Isolation: Q_sigma(iota_v u) = 0 for any single-site variation v < k
  2. Conditional Tangent Isolation: A perturbation assumed to lie in im(P_sigma)
     is annihilated by Q_sigma. Proper support alone does not establish this premise.
  AuthorityEffect: None.
-/

namespace HigherCell

open SimplexOperatorSpace

variable (V : SimplexOperatorSpace)

/-- Lemma: sumTangent m on an elementary 1-local operator iota v u vanishes when m ≤ v. -/
theorem sumTangent_iota_ge (v : Nat) (u : V.Ej v) :
    ∀ (m : Nat), m ≤ v → V.sumTangent m (V.iota v u) = V.zero
  | 0, _ => by
    dsimp [sumTangent]
  | m + 1, h => by
    dsimp [sumTangent]
    have h_m_le : m ≤ v := Nat.le_of_succ_le h
    have h_ih := sumTangent_iota_ge v u m h_m_le
    rw [h_ih]
    have h_ne : v ≠ m := Nat.ne_of_gt (Nat.lt_of_succ_le h)
    have h_diff := V.tau_iota_diff v m u h_ne
    rw [h_diff, V.iota_zero]
    exact V.zero_add V.zero

/-- Lemma: sumTangent m on an elementary 1-local operator iota v u recovers iota v u when v < m. -/
theorem sumTangent_iota_lt (v : Nat) (u : V.Ej v) :
    ∀ (m : Nat), v < m → V.sumTangent m (V.iota v u) = V.iota v u
  | 0, h => by
    cases h
  | m + 1, h => by
    dsimp [sumTangent]
    cases Nat.eq_or_lt_of_le (Nat.le_of_lt_succ h) with
    | inl h_eq =>
      subst h_eq
      have h_ge := sumTangent_iota_ge V v u v (Nat.le_refl v)
      rw [h_ge]
      rw [V.tau_iota_same]
      exact V.zero_add (V.iota v u)
    | inr h_lt =>
      have h_ih := sumTangent_iota_lt v u m h_lt
      rw [h_ih]
      have h_ne : v ≠ m := Nat.ne_of_lt h_lt
      have h_diff := V.tau_iota_diff v m u h_ne
      rw [h_diff, V.iota_zero]
      exact V.add_zero (V.iota v u)

/-- Theorem 4.2 Part 1 (1-Local Projector Identification):
    P_sigma acts as the identity on any single-site variation iota v u (v < k). -/
theorem theorem42_P_sigma_one_local (v : Nat) (hv : v < V.k) (u : V.Ej v) :
    V.P_sigma (V.iota v u) = V.iota v u := by
  dsimp [P_sigma]
  exact sumTangent_iota_lt V v u V.k hv

/-- Theorem 4.2 Part 2 (1-Local Tangent Isolation):
    Every single-site Hamiltonian variation is annihilated by Q_sigma:
    Q_sigma(iota_v u) = 0 for all v < k. -/
theorem theorem42_one_local_isolation (v : Nat) (hv : v < V.k) (u : V.Ej v) :
    V.Q_sigma (V.iota v u) = V.zero := by
  dsimp [Q_sigma]
  rw [theorem42_P_sigma_one_local V v hv u]
  exact V.sub_self (V.iota v u)

/-- Definition: A perturbation Z is Tangent-Decomposable if it lies in im(P_sigma). -/
def IsTangentVector (Z : V.E) : Prop :=
  ∃ Y : V.E, Z = V.P_sigma Y

/-- Theorem 4.2 Part 3 (Generalized Tangent Isolation):
    Every perturbation Z assumed to be tangent
    satisfies P_sigma(Z) = Z and is annihilated by Q_sigma: Q_sigma(Z) = 0. -/
theorem theorem42_tangent_isolation (Z : V.E) (hZ : IsTangentVector V Z) :
    V.Q_sigma Z = V.zero := by
  rcases hZ with ⟨Y, rfl⟩
  exact theorem41_normal_annihilates_tangent V Y

/-- Theorem 4.2 Part 4 (Tangent Vector Identity): -/
theorem theorem42_tangent_fixed (Z : V.E) (hZ : IsTangentVector V Z) :
    V.P_sigma Z = Z := by
  rcases hZ with ⟨Y, rfl⟩
  exact theorem41_idempotence V Y

end HigherCell
