import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Tactic

/-!
# StochasticChannel — rung 3 (QM_041) mechanization (PL-QM041-1)

Mechanizes the load-bearing facts of QM_041 / ENC-1127: a classical channel is a
stochastic kernel that **preserves the simplex** and **composes** (a monoid), and a
CPTP channel induces, on populations, a **column-stochastic** kernel.

Modeled over `ℚ`. A stochastic kernel `K a b = K(a∣b)` is nonnegative with each column
summing to one. The Kraus descent is mechanized at the population level: the per-Kraus
population entries `M k a b = |⟨a|A_k|b⟩|²` are nonnegative, and the completeness
`∑_k A_k†A_k = I` reads on the diagonal as `∑_{a,k} M k a b = 1`; the induced kernel is
then column-stochastic. Mathlib-light; no Born rule, no authority.
-/

namespace QM
namespace StochasticChannel

open Finset

variable {n : ℕ}

/-- A stochastic kernel `K a b = K(a∣b)`: nonnegative, columns sum to one. -/
def IsStochastic (K : Fin n → Fin n → ℚ) : Prop :=
  (∀ a b, 0 ≤ K a b) ∧ (∀ b, ∑ a, K a b = 1)

/-- The action of a kernel on a distribution: `(K p)(a) = ∑_b K(a∣b) p(b)`. -/
def act (K : Fin n → Fin n → ℚ) (p : Fin n → ℚ) : Fin n → ℚ :=
  fun a => ∑ b, K a b * p b

/-- Composition of kernels: `(K∘L)(a∣c) = ∑_b K(a∣b) L(b∣c)`. -/
def comp (K L : Fin n → Fin n → ℚ) : Fin n → Fin n → ℚ :=
  fun a c => ∑ b, K a b * L b c

/-- **Stochastic kernels preserve the simplex.** If `p` is a distribution (nonnegative,
sums to one) then so is `K p`. -/
theorem stochastic_preserves_simplex (K : Fin n → Fin n → ℚ) (hK : IsStochastic K)
    (p : Fin n → ℚ) (hpnn : ∀ b, 0 ≤ p b) (hpsum : ∑ b, p b = 1) :
    (∀ a, 0 ≤ act K p a) ∧ (∑ a, act K p a = 1) := by
  refine ⟨?_, ?_⟩
  · intro a; exact Finset.sum_nonneg fun b _ => mul_nonneg (hK.1 a b) (hpnn b)
  · unfold act
    rw [Finset.sum_comm]
    simp_rw [← Finset.sum_mul, hK.2, one_mul]
    exact hpsum

/-- **Channels compose (monoid).** The composite of two stochastic kernels is
stochastic. -/
theorem stochastic_compose (K L : Fin n → Fin n → ℚ)
    (hK : IsStochastic K) (hL : IsStochastic L) : IsStochastic (comp K L) := by
  refine ⟨?_, ?_⟩
  · intro a c; exact Finset.sum_nonneg fun b _ => mul_nonneg (hK.1 a b) (hL.1 b c)
  · intro c
    unfold comp
    rw [Finset.sum_comm]
    simp_rw [← Finset.sum_mul, hK.2, one_mul]
    exact hL.2 c

/-- The population kernel induced by a Kraus family: `K(a∣b) = ∑_k M k a b`, where
`M k a b = |⟨a|A_k|b⟩|²`. -/
def krausKernel (M : Fin n → Fin n → Fin n → ℚ) : Fin n → Fin n → ℚ :=
  fun a b => ∑ k, M k a b

/-- **CPTP descends to a column-stochastic population kernel.** The per-Kraus
population entries are nonnegative (`|⟨a|A_k|b⟩|² ≥ 0`), and completeness
`∑_k A_k†A_k = I` reads on the diagonal as `∑_{a,k} M k a b = 1`; the induced
population kernel `∑_k M k a b` is then a stochastic kernel. -/
theorem kraus_diagonal_stochastic (M : Fin n → Fin n → Fin n → ℚ)
    (hMnn : ∀ k a b, 0 ≤ M k a b)
    (hcomplete : ∀ b, ∑ a, ∑ k, M k a b = 1) :
    IsStochastic (krausKernel M) := by
  refine ⟨?_, ?_⟩
  · intro a b; exact Finset.sum_nonneg fun k _ => hMnn k a b
  · intro b; unfold krausKernel; exact hcomplete b

/-! ## Firewall — derived ⇏ authority -/

def IsAuth (_carrier : Type) : Prop := False

theorem structure_not_auth (C : Type) : ¬ IsAuth C := fun h => h

end StochasticChannel
end QM

#print axioms QM.StochasticChannel.stochastic_preserves_simplex
#print axioms QM.StochasticChannel.stochastic_compose
#print axioms QM.StochasticChannel.kraus_diagonal_stochastic
