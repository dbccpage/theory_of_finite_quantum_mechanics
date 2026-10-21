import QcConcatenation
import QcRepairQueue
import QcEntropySink

/-!
# Conditional viability of reliable computation: the assembled finite statement

Origin: dag/research/quantum_computation_self_obstruction.md (QCV-Q5)
Claim: inside the declared finite model, reliable depth-`T` computation is certified exactly when
four named conditions hold together: (1) a fresh-ancilla supply `r` of at least
`lam / ((1 - g) * kappa)` (so the repair step's own residual `g` is outweighed), (2) the level
overhead's weighted geometric means stay bounded (`AmpBounded`), (3) the physical error rate lies
below the resulting threshold, and (4) the noise obeys the recurrence `p_{k+1} <= c_k p_k^2`.
Then the logical failure probability of any circuit with `L` locations is at most
`L * (D p_0)^(2^k) / D` at concatenation level `k`, which an explicit level makes at most any
`epsilon`.  When (1) fails the backlog grows linearly and, in the global depolarizing model, the
distance between two computation histories decays as `(1 - p)^t`; when (2) fails in the exact
`double exponential` form no positive `p_0` lies below threshold.
AuthorityEffect: None
Scope Fence: (4) is a hypothesis about the noise, not a derived property of any hardware.  The
theorems say what follows from the hypotheses and which hypotheses cannot be dropped; they do not
say that any physical computer meets them or fails them.
-/

namespace QcSelfObstruction

/-! ## Comparison of an actual error profile with the recurrence -/

/-- If the true level errors obey the declared inequality `p_{k+1} <= c_k p_k^2` with `c_k <= C`,
they stay below the constant-overhead closed form with `D = max C 1`. -/
theorem level_error_le {c : ℕ → ℚ} {C : ℚ} (hC : ∀ k, c k ≤ C)
    (p : ℕ → ℚ) (hp : ∀ k, 0 ≤ p k) (hrec : ∀ k, p (k + 1) ≤ c k * p k ^ 2) (k : ℕ) :
    p k ≤ conc (max C 1) (p 0) k := by
  induction k with
  | zero => simp
  | succ k ih =>
    rw [conc_succ]
    calc p (k + 1) ≤ c k * p k ^ 2 := hrec k
      _ ≤ max C 1 * p k ^ 2 :=
          mul_le_mul_of_nonneg_right (le_trans (hC k) (le_max_left _ _)) (sq_nonneg _)
      _ ≤ max C 1 * conc (max C 1) (p 0) k ^ 2 :=
          mul_le_mul_of_nonneg_left (pow_le_pow_left₀ (hp k) ih 2)
            (le_trans zero_le_one (le_max_right _ _))

/-- Conversely, if the recurrence is an exact lower bound `p_{k+1} >= c_k p_k^2` (a tight model),
the errors stay above `concv c p_0`: the overhead criterion is then also necessary. -/
theorem level_error_ge {c : ℕ → ℚ} (hc : ∀ k, 0 ≤ c k) (p : ℕ → ℚ) (hp0 : 0 ≤ p 0)
    (hrec : ∀ k, c k * p k ^ 2 ≤ p (k + 1)) (k : ℕ) : concv c (p 0) k ≤ p k := by
  induction k with
  | zero => simp [concv]
  | succ k ih =>
    rw [concv]
    have h0 := concv_nonneg hc hp0 k
    calc c k * concv c (p 0) k ^ 2 ≤ c k * p k ^ 2 :=
          mul_le_mul_of_nonneg_left (pow_le_pow_left₀ h0 ih 2) (hc k)
      _ ≤ p (k + 1) := hrec k

/-- Explicit level: with `D p_0 <= 1/2`, a circuit of `L` locations fails with probability at most
`epsilon` as soon as `L <= epsilon * D * 2 ^ (2 ^ k)`. -/
theorem explicit_level {D p0 : ℚ} (hD : 0 < D) (hp0 : 0 ≤ p0) (hr : D * p0 ≤ 1 / 2) (L ε : ℚ)
    (hL : 0 ≤ L) (k : ℕ) (hk : L ≤ ε * D * 2 ^ (2 ^ k)) :
    L * conc D p0 k ≤ ε := by
  have h1 : conc D p0 k ≤ (1 / 2) ^ (2 ^ k) / D := sub_half_bound hD (by positivity) hr k
  have h2 : (0 : ℚ) < 2 ^ (2 ^ k) := by positivity
  have h3 : (1 / 2 : ℚ) ^ (2 ^ k) = 1 / 2 ^ (2 ^ k) := by rw [one_div_pow]
  calc L * conc D p0 k ≤ L * ((1 / 2) ^ (2 ^ k) / D) := mul_le_mul_of_nonneg_left h1 hL
    _ = L / (2 ^ (2 ^ k) * D) := by rw [h3]; field_simp
    _ ≤ ε := by
        rw [div_le_iff₀ (by positivity)]
        nlinarith

/-- Q5 (positive half): the conditional certificate.  Fresh supply large enough, repair efficient
(`g < 1`), level-bounded overhead, physical rate below `1 / D`, and true noise obeying the
recurrence *whenever the repair backlog is bounded* (the recurrence is hypothesised only in the
regime where repair keeps up): the backlog is bounded and, for every `epsilon > 0` and every circuit
size `L`, some concatenation level makes the union-bound failure probability `L * p_k` at most
`epsilon`. -/
theorem conditional_viability {lam g kappa r q0 : ℚ} {c : ℕ → ℚ} {C : ℚ}
    (hq : 0 ≤ q0) (hg : g < 1) (hkap : 0 < kappa)
    (hsupply : lam / ((1 - g) * kappa) ≤ r)
    (hC : ∀ k, c k ≤ C)
    (p : ℕ → ℚ) (hp : ∀ k, 0 ≤ p k)
    (hrec : BacklogBounded lam g (kappa * r) q0 → ∀ k, p (k + 1) ≤ c k * p k ^ 2)
    (hth : max C 1 * p 0 < 1) :
    BacklogBounded lam g (kappa * r) q0 ∧
      ∀ (L ε : ℚ), 0 ≤ L → 0 < ε → ∃ k : ℕ, L * p k ≤ ε := by
  have hD : 0 < max C 1 := lt_of_lt_of_le one_pos (le_max_right _ _)
  have hbb : BacklogBounded lam g (kappa * r) q0 := (fresh_supply_threshold hq hg hkap).2 hsupply
  refine ⟨hbb, fun L ε hL hε => ?_⟩
  have hz := sub_goesToZero hD (hp 0) hth
  obtain ⟨K, hK⟩ := hz (ε / (L + 1)) (by positivity)
  refine ⟨K, ?_⟩
  have h1 := level_error_le hC p hp (hrec hbb) K
  have h2 := hK K le_rfl
  rw [abs_of_nonneg (conc_nonneg hD.le (hp 0) K)] at h2
  have h3 : p K < ε / (L + 1) := lt_of_le_of_lt h1 h2
  rw [lt_div_iff₀ (by positivity)] at h3
  nlinarith [hp K]

/-- The same certificate with an explicit level when `D p_0 <= 1/2`: any `k` with
`L <= epsilon * D * 2 ^ (2 ^ k)` works. -/
theorem conditional_viability_explicit {c : ℕ → ℚ} {C : ℚ} (hC : ∀ k, c k ≤ C)
    (p : ℕ → ℚ) (hp : ∀ k, 0 ≤ p k) (hrec : ∀ k, p (k + 1) ≤ c k * p k ^ 2)
    (hth : max C 1 * p 0 ≤ 1 / 2) (L ε : ℚ) (hL : 0 ≤ L) (k : ℕ)
    (hk : L ≤ ε * max C 1 * 2 ^ (2 ^ k)) : L * p k ≤ ε := by
  have hD : 0 < max C 1 := lt_of_lt_of_le one_pos (le_max_right _ _)
  exact le_trans (mul_le_mul_of_nonneg_left (level_error_le hC p hp hrec k) hL)
    (explicit_level hD (hp 0) hth L ε hL k hk)

/-- Q5 (negative half) for the model: viability requires both conditions.  In the model with exact
overhead sequence `c` (positive) and the repair queue, "backlog bounded and some positive physical
rate has `p_k -> 0`" holds exactly when the fresh supply reaches `lam / ((1 - g) kappa)` and the
overhead means are bounded. -/
theorem model_viable_iff {lam g kappa r q0 : ℚ} {c : ℕ → ℚ} (hq : 0 ≤ q0) (hg : g < 1)
    (hkap : 0 < kappa) (hc : ∀ k, 0 ≤ c k) :
    (BacklogBounded lam g (kappa * r) q0 ∧ ThresholdRegionNonempty c) ↔
      (lam / ((1 - g) * kappa) ≤ r ∧ AmpBounded c) := by
  rw [fresh_supply_threshold hq hg hkap, threshold_region_iff hc]

/-- No fresh supply and positive generation: not viable, in the repair queue (backlog grows) ... -/
theorem not_viable_without_supply {lam g kappa q0 : ℚ} (hq : 0 ≤ q0) (hg : g < 1) (hkap : 0 < kappa)
    (hlam : 0 < lam) : ¬ BacklogBounded lam g (kappa * 0) q0 := by
  rw [fresh_supply_threshold hq hg hkap]
  have : 0 < lam / ((1 - g) * kappa) := by
    apply div_pos hlam; nlinarith
  intro h; linarith

/-- ... and not viable under unit-gain repair, whatever the supply. -/
theorem not_viable_unit_gain {lam g q0 : ℚ} (hq : 0 ≤ q0) (hlam : 0 < lam) (hg : 1 ≤ g)
    (kappa r : ℚ) (hkr : 0 ≤ kappa * r) : ¬ BacklogBounded lam g (kappa * r) q0 :=
  no_bounded_backlog_if_unit_gain hq hlam hg _ hkr

/-- ... and not viable when the overhead grows as a double exponential: the exact model has no
positive physical rate with `p_k -> 0`; a tight lower-bound noise profile cannot tend to zero
either. -/
theorem not_viable_dexp_profile {c : ℕ → ℚ} {a b : ℚ} (ha : 0 < a) (hb : 1 < b)
    (hge : ∀ k, a * b ^ (2 ^ k) ≤ c k) (p : ℕ → ℚ) (hp0 : 0 < p 0)
    (hrec : ∀ k, c k * p k ^ 2 ≤ p (k + 1)) : ¬ GoesToZero p := by
  have hc : ∀ k, 0 ≤ c k := fun k => le_trans (by positivity) (hge k)
  intro hz
  have hno := dexp_region_empty ha hb hge (p 0) hp0
  apply hno
  intro ε hε
  obtain ⟨K, hK⟩ := hz ε hε
  refine ⟨K, fun k hk => ?_⟩
  have h1 := level_error_ge hc p hp0.le hrec k
  have h2 := concv_nonneg hc hp0.le k
  rw [abs_of_nonneg h2]
  exact lt_of_le_of_lt h1 (lt_of_le_of_lt (le_abs_self _) (hK k hk))

/-- The hypotheses of `conditional_viability` are jointly satisfiable (declared toy numbers, not a
device): `lam = 1`, `g = 1/2`, `kappa = 1`, `r = 2`, constant overhead `c = 4`, `p_0 = 1/10`, so
`D * p_0 = 2/5 < 1`.  The conclusion then holds for that instance. -/
theorem conditional_viability_instance :
    BacklogBounded 1 (1 / 2) (1 * 2) 0 ∧
      ∀ (L ε : ℚ), 0 ≤ L → 0 < ε → ∃ k : ℕ, L * conc 4 (1 / 10) k ≤ ε := by
  have hth : max (4 : ℚ) 1 * conc 4 (1 / 10) 0 < 1 := by norm_num [conc, max_def]
  exact conditional_viability (c := fun _ => 4) (C := 4) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (fun _ => le_rfl) (conc 4 (1 / 10))
    (fun k => conc_nonneg (by norm_num) (by norm_num) k)
    (fun _ k => by rw [conc_succ]) hth

end QcSelfObstruction

/-! ## Axiom audit for the cited declarations -/

open QcSelfObstruction in
#print axioms backlog
open QcSelfObstruction in
#print axioms drift
open QcSelfObstruction in
#print axioms pairCount
open QcSelfObstruction in
#print axioms backlog_bounded_iff
open QcSelfObstruction in
#print axioms no_bounded_backlog_if_unit_gain
open QcSelfObstruction in
#print axioms fresh_supply_threshold
open QcSelfObstruction in
#print axioms no_supply_linear_growth
open QcSelfObstruction in
#print axioms backlog_linear
open QcSelfObstruction in
#print axioms backlog_le_initial
open QcSelfObstruction in
#print axioms lin_not_goesToZero
open QcSelfObstruction in
#print axioms lin_closed
open QcSelfObstruction in
#print axioms pairCount_mono
open QcSelfObstruction in
#print axioms threshold_decreases_with_repair
open QcSelfObstruction in
#print axioms conc_closed
open QcSelfObstruction in
#print axioms conc_eq_div
open QcSelfObstruction in
#print axioms threshold_trichotomy
open QcSelfObstruction in
#print axioms goesToZero_iff_below_threshold
open QcSelfObstruction in
#print axioms sub_bound
open QcSelfObstruction in
#print axioms sub_half_bound
open QcSelfObstruction in
#print axioms super_bound
open QcSelfObstruction in
#print axioms super_diverges
open QcSelfObstruction in
#print axioms fixed_point
open QcSelfObstruction in
#print axioms concv_eq_amp
open QcSelfObstruction in
#print axioms threshold_region_iff
open QcSelfObstruction in
#print axioms region_empty_iff
open QcSelfObstruction in
#print axioms ampBounded_of_bounded
open QcSelfObstruction in
#print axioms bounded_overhead_goesToZero
open QcSelfObstruction in
#print axioms ampBounded_of_geom
open QcSelfObstruction in
#print axioms ampBounded_poly
open QcSelfObstruction in
#print axioms ampBounded_of_sizes
open QcSelfObstruction in
#print axioms blockExp_le
open QcSelfObstruction in
#print axioms dexp_not_ampBounded
open QcSelfObstruction in
#print axioms dexp_region_empty
open QcSelfObstruction in
#print axioms sizes_not_ampBounded
open QcSelfObstruction in
#print axioms amp_dexp_sq
open QcSelfObstruction in
#print axioms tn
open QcSelfObstruction in
#print axioms tn_smul
open QcSelfObstruction in
#print axioms tn_conj
open QcSelfObstruction in
#print axioms pairingSet_bddAbove
open QcSelfObstruction in
#print axioms depol_dist
open QcSelfObstruction in
#print axioms noisyStep_dist
open QcSelfObstruction in
#print axioms run_dist
open QcSelfObstruction in
#print axioms run_dist_le
open QcSelfObstruction in
#print axioms decay_le_inv
open QcSelfObstruction in
#print axioms decay_below
open QcSelfObstruction in
#print axioms sqDist_runB
open QcSelfObstruction in
#print axioms sqDist_runB_le
open QcSelfObstruction in
#print axioms sqDist_stepB
open QcSelfObstruction in
#print axioms rot_dot
open QcSelfObstruction in
#print axioms blochMat_sq
open QcSelfObstruction in
#print axioms conditional_viability
open QcSelfObstruction in
#print axioms conditional_viability_explicit
open QcSelfObstruction in
#print axioms conditional_viability_instance
open QcSelfObstruction in
#print axioms level_error_le
open QcSelfObstruction in
#print axioms explicit_level
open QcSelfObstruction in
#print axioms model_viable_iff
open QcSelfObstruction in
#print axioms not_viable_without_supply
open QcSelfObstruction in
#print axioms not_viable_unit_gain
open QcSelfObstruction in
#print axioms not_viable_dexp_profile
open QcSelfObstruction in
#print axioms level_error_ge
open QcSelfObstruction in
#print axioms rounds_le_budget
open QcSelfObstruction in
#print axioms budget_exhausted
