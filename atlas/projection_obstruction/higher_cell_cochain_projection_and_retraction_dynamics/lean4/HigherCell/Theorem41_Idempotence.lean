import HigherCell.Core

/-!
  # HigherCell.Theorem41_Idempotence — Theorem 4.1 Formalization
  Formal proofs for:
  1. Exact Marginal Preservation: tau_j(P_sigma(Z)) = tau_j(Z) for all j < k
  2. Idempotence: P_sigma(P_sigma(Z)) = P_sigma(Z)
  3. Tangent Annihilation: Q_sigma(P_sigma(Z)) = 0
  AuthorityEffect: None.
-/

namespace HigherCell

open SimplexOperatorSpace

variable (V : SimplexOperatorSpace)

/-- Lemma: Partial trace at site l of sumTangent m Z vanishes when m ≤ l. -/
theorem partial_trace_sumTangent_ge (Z : V.E) :
    ∀ (m l : Nat), m ≤ l → V.tau l (V.sumTangent m Z) = V.zero_Ej l
  | 0, l, _ => by
    dsimp [sumTangent]
    exact V.tau_zero l
  | m + 1, l, h => by
    dsimp [sumTangent]
    rw [V.tau_add]
    have h_ml : m ≤ l := Nat.le_of_succ_le h
    have h_ih := partial_trace_sumTangent_ge Z m l h_ml
    rw [h_ih]
    have h_ne : m ≠ l := Nat.ne_of_lt (Nat.lt_of_succ_le h)
    have h_diff := V.tau_iota_diff m l (V.tau m Z) h_ne
    rw [h_diff]
    exact V.zero_add_Ej l (V.zero_Ej l)

/-- Lemma: Partial trace at site l of sumTangent m Z preserves the marginal tau l Z when l < m. -/
theorem partial_trace_sumTangent_lt (Z : V.E) :
    ∀ (m l : Nat), l < m → V.tau l (V.sumTangent m Z) = V.tau l Z
  | 0, l, h => by
    cases h
  | m + 1, l, h => by
    dsimp [sumTangent]
    rw [V.tau_add]
    cases Nat.eq_or_lt_of_le (Nat.le_of_lt_succ h) with
    | inl h_eq =>
      subst h_eq
      have h_ge := partial_trace_sumTangent_ge V Z l l (Nat.le_refl l)
      rw [h_ge]
      rw [V.tau_iota_same]
      exact V.zero_add_Ej l (V.tau l Z)
    | inr h_lt =>
      have h_ih := partial_trace_sumTangent_lt Z m l h_lt
      rw [h_ih]
      have h_ne : m ≠ l := Nat.ne_of_gt h_lt
      have h_diff := V.tau_iota_diff m l (V.tau m Z) h_ne
      rw [h_diff]
      exact V.add_zero_Ej l (V.tau l Z)

/-- Theorem 4.1 Part 1 (Exact Marginal Preservation):
    The oblique tangent projector P_sigma preserves all single-site reduced marginals exactly:
    tau_j(P_sigma(Z)) = tau_j(Z) for all j < k. -/
theorem theorem41_marginal_preservation (Z : V.E) (j : Nat) (h : j < V.k) :
    V.tau j (V.P_sigma Z) = V.tau j Z := by
  dsimp [P_sigma]
  exact partial_trace_sumTangent_lt V Z V.k j h

/-- Lemma: sumTangent evaluated on P_sigma Z equals sumTangent evaluated on Z for m ≤ k. -/
theorem sumTangent_P_sigma_eq (Z : V.E) :
    ∀ (m : Nat), m ≤ V.k → V.sumTangent m (V.P_sigma Z) = V.sumTangent m Z
  | 0, _ => by
    dsimp [sumTangent]
  | m + 1, h => by
    dsimp [sumTangent]
    have h_m_le : m ≤ V.k := Nat.le_of_succ_le h
    have h_ih := sumTangent_P_sigma_eq Z m h_m_le
    rw [h_ih]
    have h_m_lt : m < V.k := h
    have h_marg := theorem41_marginal_preservation V Z m h_m_lt
    rw [h_marg]

/-- Theorem 4.1 Part 2 (Tangent Projector Idempotence):
    P_sigma is an idempotent oblique projection:
    P_sigma(P_sigma(Z)) = P_sigma(Z). -/
theorem theorem41_idempotence (Z : V.E) :
    V.P_sigma (V.P_sigma Z) = V.P_sigma Z := by
  dsimp [P_sigma]
  exact sumTangent_P_sigma_eq V Z V.k (Nat.le_refl V.k)

/-- Theorem 4.1 Part 3 (Tangent Annihilation):
    The complementary normal projector Q_sigma annihilates the tangent space:
    Q_sigma(P_sigma(Z)) = 0. -/
theorem theorem41_normal_annihilates_tangent (Z : V.E) :
    V.Q_sigma (V.P_sigma Z) = V.zero := by
  dsimp [Q_sigma]
  rw [theorem41_idempotence]
  exact V.sub_self (V.P_sigma Z)

end HigherCell
