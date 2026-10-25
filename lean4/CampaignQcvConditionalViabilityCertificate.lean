-- Campaign: QCV-CONDITIONAL-VIABILITY-CERTIFICATE. Not a default target.
-- Nonnegative initial backlog, then the explicit level bound.
import QcSelfObstruction

open QcSelfObstruction

theorem viability_nonneg_initial
    {lam g kappa r q0 : ℚ} {c : ℕ → ℚ} {C : ℚ}
    (hq : 0 ≤ q0) (hg : g < 1) (hkap : 0 < kappa)
    (hsupply : lam / ((1 - g) * kappa) ≤ r)
    (hC : ∀ k, c k ≤ C)
    (p : ℕ → ℚ) (hp : ∀ k, 0 ≤ p k)
    (hrec : BacklogBounded lam g (kappa * r) q0 → ∀ k, p (k + 1) ≤ c k * p k ^ 2)
    (hth : max C 1 * p 0 < 1) :
    BacklogBounded lam g (kappa * r) q0 ∧
      ∀ (L ε : ℚ), 0 ≤ L → 0 < ε → ∃ k : ℕ, L * p k ≤ ε :=
  conditional_viability hq hg hkap hsupply hC p hp hrec hth

theorem viability_explicit_level
    {lam g kappa r q0 : ℚ} {c : ℕ → ℚ} {C : ℚ}
    (hq : 0 ≤ q0) (hg : g < 1) (hkap : 0 < kappa)
    (hsupply : lam / ((1 - g) * kappa) ≤ r)
    (hC : ∀ k, c k ≤ C)
    (p : ℕ → ℚ) (hp : ∀ k, 0 ≤ p k)
    (hrec : BacklogBounded lam g (kappa * r) q0 → ∀ k, p (k + 1) ≤ c k * p k ^ 2)
    (hth : max C 1 * p 0 ≤ 1 / 2)
    (L ε : ℚ) (hL : 0 ≤ L) (k : ℕ)
    (hk : L ≤ ε * max C 1 * 2 ^ (2 ^ k)) :
    L * p k ≤ ε := by
  have hlt : max C 1 * p 0 < 1 := lt_of_le_of_lt hth (by norm_num)
  have hbb : BacklogBounded lam g (kappa * r) q0 :=
    (viability_nonneg_initial hq hg hkap hsupply hC p hp hrec hlt).1
  exact conditional_viability_explicit hC p hp (hrec hbb) hth L ε hL k hk

#print axioms viability_nonneg_initial
#print axioms viability_explicit_level
#print axioms conditional_viability
#print axioms conditional_viability_explicit
