import Mathlib.Algebra.Order.Archimedean.Basic
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Data.Rat.Cast.Order
import Mathlib.Tactic.IntervalCases
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

/-!
# Concatenated repair: the exact threshold dichotomy and its level-dependent form

Origin: dag/research/quantum_computation_self_obstruction.md (QCV-Q2, QCV-Q3)
Claim: the recurrence `p_{k+1} = c * p_k ^ 2` over `ℚ` has the closed form `c * p_k = (c * p_0) ^ (2 ^ k)`,
and for `0 < c`, `0 ≤ p_0` it splits exactly into three cases on `c * p_0` (below one: doubly
exponential decay; equal to one: fixed point; above one: divergence).  For a level-dependent overhead
`c_k` the same recurrence has the closed form `p_k = p_0 ^ (2 ^ k) * amp c k`, a threshold region
exists if and only if `amp c k ≤ M ^ (2 ^ k)` for some `M`, bounded and at-most-exponential overheads
satisfy it, and an overhead of at least `a * b ^ (2 ^ k)` with `b > 1` violates it.
AuthorityEffect: None
Scope Fence: this is the recurrence only.  It does not derive that any physical noise model obeys the
recurrence, does not compute a constant `c` for any code, and does not say that any device is below
threshold.  The threshold theorem for concatenated codes is cited, not re-proved.
-/

namespace QcSelfObstruction

/-! ## Q2: the constant-overhead recurrence -/

/-- `conc c p k` is the level-`k` error of `p_{k+1} = c * p_k ^ 2` started at `p_0 = p`. -/
def conc (c p : ℚ) : ℕ → ℚ
  | 0 => p
  | k + 1 => c * (conc c p k) ^ 2

@[simp] theorem conc_zero (c p : ℚ) : conc c p 0 = p := rfl

theorem conc_succ (c p : ℚ) (k : ℕ) : conc c p (k + 1) = c * (conc c p k) ^ 2 := rfl

/-- Exact closed form: `c * p_k = (c * p_0) ^ (2 ^ k)`; no sign or size assumption on `c`, `p`. -/
theorem conc_closed (c p : ℚ) (k : ℕ) : c * conc c p k = (c * p) ^ (2 ^ k) := by
  induction k with
  | zero => simp
  | succ k ih =>
    rw [conc_succ, pow_succ 2 k, pow_mul, ← ih]
    ring

/-- `p_k = (c * p_0) ^ (2 ^ k) / c` for `c ≠ 0`. -/
theorem conc_eq_div (c p : ℚ) (hc : c ≠ 0) (k : ℕ) : conc c p k = (c * p) ^ (2 ^ k) / c := by
  rw [eq_div_iff hc, mul_comm]
  exact conc_closed c p k

theorem conc_nonneg {c p : ℚ} (hc : 0 ≤ c) (hp : 0 ≤ p) (k : ℕ) : 0 ≤ conc c p k := by
  induction k with
  | zero => simpa using hp
  | succ k ih => rw [conc_succ]; positivity

/-- A sequence tends to zero (epsilon form over `ℚ`). -/
def GoesToZero (f : ℕ → ℚ) : Prop := ∀ ε : ℚ, 0 < ε → ∃ K : ℕ, ∀ k, K ≤ k → |f k| < ε

/-- A sequence is unbounded above and eventually above every bound. -/
def Diverges (f : ℕ → ℚ) : Prop := ∀ M : ℚ, ∃ K : ℕ, ∀ k, K ≤ k → M < f k

theorem two_pow_ge_succ (k : ℕ) : k + 1 ≤ 2 ^ k := Nat.succ_le_of_lt Nat.lt_two_pow_self

/-- Below threshold: the doubly exponential bound `c * p_k = r ^ (2 ^ k) ≤ r ^ (k + 1)`, `r = c * p_0`. -/
theorem sub_bound {c p : ℚ} (hr0 : 0 ≤ c * p) (hr1 : c * p < 1) (k : ℕ) :
    c * conc c p k ≤ (c * p) ^ (k + 1) := by
  rw [conc_closed]
  exact pow_le_pow_of_le_one hr0 hr1.le (two_pow_ge_succ k)

/-- Below threshold with `r ≤ 1/2`: the explicit doubly exponential rate `p_k ≤ (1/2)^(2^k) / c`. -/
theorem sub_half_bound {c p : ℚ} (hc : 0 < c) (hr0 : 0 ≤ c * p) (hr : c * p ≤ 1 / 2) (k : ℕ) :
    conc c p k ≤ (1 / 2) ^ (2 ^ k) / c := by
  rw [conc_eq_div c p hc.ne']
  exact div_le_div_of_nonneg_right (pow_le_pow_left₀ hr0 hr _) hc.le

/-- Below threshold: `p_k` tends to zero. -/
theorem sub_goesToZero {c p : ℚ} (hc : 0 < c) (hp : 0 ≤ p) (hr : c * p < 1) :
    GoesToZero (conc c p) := by
  intro ε hε
  have hr0 : 0 ≤ c * p := by positivity
  obtain ⟨n, hn⟩ := exists_pow_lt_of_lt_one (mul_pos hc hε) hr
  refine ⟨n, fun k hk => ?_⟩
  have hnn : 0 ≤ conc c p k := conc_nonneg hc.le hp k
  rw [abs_of_nonneg hnn]
  have h1 := sub_bound hr0 hr k
  have h2 : (c * p) ^ (k + 1) ≤ (c * p) ^ n :=
    pow_le_pow_of_le_one hr0 hr.le (by omega)
  have : c * conc c p k < c * ε := by linarith
  exact lt_of_mul_lt_mul_left this hc.le

/-- Below threshold the error strictly decreases while positive. -/
theorem sub_strictAnti_step {c p : ℚ} (hc : 0 < c) (hp : 0 < p) (hr : c * p < 1) (k : ℕ) :
    conc c p (k + 1) < conc c p k := by
  have hr0 : 0 ≤ c * p := by positivity
  have hpos : 0 < conc c p k := by
    rw [conc_eq_div c p hc.ne']; positivity
  have h1 : c * conc c p k ≤ c * p := by
    have := sub_bound hr0 hr k
    calc c * conc c p k ≤ (c * p) ^ (k + 1) := this
      _ ≤ (c * p) ^ 1 := pow_le_pow_of_le_one hr0 hr.le (by omega)
      _ = c * p := pow_one _
  have : c * conc c p k < 1 := lt_of_le_of_lt h1 hr
  rw [conc_succ]
  nlinarith

/-- The fixed point: `c * p_0 = 1` gives the constant sequence `1 / c`. -/
theorem fixed_point {c p : ℚ} (hc : 0 < c) (hr : c * p = 1) (k : ℕ) : conc c p k = 1 / c := by
  rw [conc_eq_div c p hc.ne', hr, one_pow]

theorem fixed_not_goesToZero {c p : ℚ} (hc : 0 < c) (hr : c * p = 1) :
    ¬ GoesToZero (conc c p) := by
  intro h
  obtain ⟨K, hK⟩ := h (1 / c) (by positivity)
  have := hK K le_rfl
  rw [fixed_point hc hr, abs_of_pos (by positivity)] at this
  exact lt_irrefl _ this

/-- Above threshold: `c * p_k ≥ 1 + 2^k (r - 1)` (Bernoulli) with `r = c * p_0`. -/
theorem super_bound {c p : ℚ} (hr : 1 < c * p) (k : ℕ) :
    1 + (2 ^ k : ℕ) * (c * p - 1) ≤ c * conc c p k := by
  rw [conc_closed]
  have := one_add_mul_le_pow (a := c * p - 1) (by linarith) (2 ^ k)
  simpa using this

/-- Above threshold: `p_k` diverges (leaves every bound; in particular leaves `[0, 1]`). -/
theorem super_diverges {c p : ℚ} (hc : 0 < c) (hr : 1 < c * p) : Diverges (conc c p) := by
  intro M
  obtain ⟨K, hK⟩ := exists_nat_gt (M * c / (c * p - 1))
  refine ⟨K, fun k hk => ?_⟩
  have hd : 0 < c * p - 1 := by linarith
  have h1 := super_bound hr k
  have h2 : (K : ℚ) ≤ ((2 ^ k : ℕ) : ℚ) := by
    have : K ≤ 2 ^ k := le_trans hk (le_trans (Nat.le_succ k) (two_pow_ge_succ k))
    exact_mod_cast this
  have h3 : M * c < K * (c * p - 1) := by
    rwa [div_lt_iff₀ hd] at hK
  have h4 : (K : ℚ) * (c * p - 1) ≤ ((2 ^ k : ℕ) : ℚ) * (c * p - 1) :=
    mul_le_mul_of_nonneg_right h2 hd.le
  have : M * c < c * conc c p k := by linarith
  nlinarith

/-- The three-way split on `r = c * p_0` (for `0 < c`, `0 ≤ p_0`), with the exact closed form in each case. -/
theorem threshold_trichotomy {c p : ℚ} (hc : 0 < c) (hp : 0 ≤ p) :
    (c * p < 1 ∧ GoesToZero (conc c p) ∧ ∀ k, c * conc c p k = (c * p) ^ (2 ^ k)) ∨
    (c * p = 1 ∧ (∀ k, conc c p k = 1 / c) ∧ ¬ GoesToZero (conc c p)) ∨
    (1 < c * p ∧ Diverges (conc c p)) := by
  rcases lt_trichotomy (c * p) 1 with h | h | h
  · exact Or.inl ⟨h, sub_goesToZero hc hp h, conc_closed c p⟩
  · exact Or.inr (Or.inl ⟨h, fixed_point hc h, fixed_not_goesToZero hc h⟩)
  · exact Or.inr (Or.inr ⟨h, super_diverges hc h⟩)

/-- Diverging sequences do not tend to zero. -/
theorem diverges_not_goesToZero {f : ℕ → ℚ} (h : Diverges f) : ¬ GoesToZero f := by
  intro hz
  obtain ⟨K, hK⟩ := h 1
  obtain ⟨K', hK'⟩ := hz 1 one_pos
  have a := hK (max K K') (le_max_left _ _)
  have b := hK' (max K K') (le_max_right _ _)
  have := le_abs_self (f (max K K'))
  linarith

/-- The threshold exists and is exactly `1 / c`: `p_k -> 0` iff `c * p_0 < 1` (for `0 <= p_0`, `0 < c`). -/
theorem goesToZero_iff_below_threshold {c p : ℚ} (hc : 0 < c) (hp : 0 ≤ p) :
    GoesToZero (conc c p) ↔ c * p < 1 := by
  rcases threshold_trichotomy hc hp with ⟨h, h2, _⟩ | ⟨h, _, h3⟩ | ⟨h, h2⟩
  · exact ⟨fun _ => h, fun _ => h2⟩
  · exact ⟨fun h' => absurd h' h3, fun h' => by linarith⟩
  · exact ⟨fun h' => absurd h' (diverges_not_goesToZero h2), fun h' => by linarith⟩

/-! ## Without repair the recurrence is linear and cannot contract -/

/-- A level with no syndrome-and-repair step fails whenever any of its `a` locations fails: a union
bound `p_{k+1} = a * p_k`. -/
def lin (a p : ℚ) : ℕ → ℚ
  | 0 => p
  | k + 1 => a * lin a p k

theorem lin_closed (a p : ℚ) (k : ℕ) : lin a p k = a ^ k * p := by
  induction k with
  | zero => simp [lin]
  | succ k ih => rw [lin, ih, pow_succ]; ring

/-- With at least one location per level (`1 ≤ a`) and `p_0 > 0`, the unrepaired recurrence never
tends to zero. -/
theorem lin_not_goesToZero {a p : ℚ} (ha : 1 ≤ a) (hp : 0 < p) : ¬ GoesToZero (lin a p) := by
  intro h
  obtain ⟨K, hK⟩ := h p hp
  have h1 := hK K le_rfl
  rw [lin_closed, abs_of_nonneg (by positivity)] at h1
  have : 1 ≤ a ^ K := one_le_pow₀ ha
  nlinarith

/-! ## The size of a level grows with its repair: pair counting -/

/-- Number of unordered pairs among `a` locations: the constant `c` of a distance-three level whose
extended gadget has `a` fault locations (declared model; the locations of the repair circuit itself
are among the `a`). -/
def pairCount (a : ℕ) : ℚ := (a : ℚ) * ((a : ℚ) - 1) / 2

theorem pairCount_mono {a b : ℕ} (hab : a ≤ b) (ha : 1 ≤ a) : pairCount a ≤ pairCount b := by
  unfold pairCount
  have h1 : (1 : ℚ) ≤ a := by exact_mod_cast ha
  have h2 : (a : ℚ) ≤ b := by exact_mod_cast hab
  nlinarith

theorem pairCount_pos {a : ℕ} (ha : 2 ≤ a) : 0 < pairCount a := by
  unfold pairCount
  have h : (2 : ℚ) ≤ a := by exact_mod_cast ha
  nlinarith

/-- Adding repair locations lowers the certified threshold `1 / c`. -/
theorem threshold_decreases_with_repair {a b : ℕ} (hab : a ≤ b) (ha : 2 ≤ a) :
    1 / pairCount b ≤ 1 / pairCount a := by
  have h1 := pairCount_pos ha
  exact one_div_le_one_div_of_le h1 (pairCount_mono hab (by omega))

/-! ## Q3: level-dependent overhead -/

/-- `concv c p k` is the level-`k` error of `p_{k+1} = c k * p_k ^ 2`. -/
def concv (c : ℕ → ℚ) (p : ℚ) : ℕ → ℚ
  | 0 => p
  | k + 1 => c k * (concv c p k) ^ 2

/-- The overhead amplification `amp c`: `amp 0 = 1`, `amp (k + 1) = c k * amp k ^ 2`, equal to the
product of `c j ^ (2 ^ (k - 1 - j))` over `j < k`. -/
def amp (c : ℕ → ℚ) : ℕ → ℚ
  | 0 => 1
  | k + 1 => c k * (amp c k) ^ 2

theorem concv_eq_amp (c : ℕ → ℚ) (p : ℚ) (k : ℕ) : concv c p k = p ^ (2 ^ k) * amp c k := by
  induction k with
  | zero => simp [concv, amp]
  | succ k ih =>
    rw [concv, amp, ih, pow_succ 2 k, pow_mul]
    ring

theorem concv_const (c : ℚ) (p : ℚ) (k : ℕ) : concv (fun _ => c) p k = conc c p k := by
  induction k with
  | zero => rfl
  | succ k ih => simp only [concv, conc, ih]

theorem amp_nonneg {c : ℕ → ℚ} (hc : ∀ k, 0 ≤ c k) (k : ℕ) : 0 ≤ amp c k := by
  induction k with
  | zero => simp [amp]
  | succ k ih => rw [amp]; exact mul_nonneg (hc k) (sq_nonneg _)

theorem concv_nonneg {c : ℕ → ℚ} (hc : ∀ k, 0 ≤ c k) {p : ℚ} (hp : 0 ≤ p) (k : ℕ) :
    0 ≤ concv c p k := by
  rw [concv_eq_amp]; exact mul_nonneg (pow_nonneg hp _) (amp_nonneg hc k)

/-- Comparison: a pointwise larger overhead gives a pointwise larger error. -/
theorem concv_mono {c d : ℕ → ℚ} (hc : ∀ k, 0 ≤ c k) (hcd : ∀ k, c k ≤ d k) {p : ℚ} (hp : 0 ≤ p)
    (k : ℕ) : concv c p k ≤ concv d p k := by
  induction k with
  | zero => simp [concv]
  | succ k ih =>
    rw [concv, concv]
    have h0 := concv_nonneg hc hp k
    calc c k * concv c p k ^ 2 ≤ c k * concv d p k ^ 2 :=
          mul_le_mul_of_nonneg_left (pow_le_pow_left₀ h0 ih 2) (hc k)
      _ ≤ d k * concv d p k ^ 2 := mul_le_mul_of_nonneg_right (hcd k) (sq_nonneg _)

/-- The exact criterion on the overhead sequence: the weighted geometric means
`amp c k ^ (1 / 2 ^ k) = prod_{j<k} (c j) ^ (1 / 2 ^ (j + 1))` stay bounded (stated without roots). -/
def AmpBounded (c : ℕ → ℚ) : Prop := ∃ M : ℚ, 0 < M ∧ ∀ k, amp c k ≤ M ^ (2 ^ k)

/-- The threshold region for `c`: some positive physical error rate with `p_k -> 0`. -/
def ThresholdRegionNonempty (c : ℕ → ℚ) : Prop := ∃ p : ℚ, 0 < p ∧ GoesToZero (concv c p)

/-- Weaker: some positive `p_0` with `p_k < 1` for all large `k`. -/
def EventuallyBelowOne (c : ℕ → ℚ) : Prop :=
  ∃ p : ℚ, 0 < p ∧ ∃ K : ℕ, ∀ k, K ≤ k → concv c p k < 1

theorem ampBounded_goesToZero {c : ℕ → ℚ} (hc : ∀ k, 0 ≤ c k) (h : AmpBounded c) :
    ThresholdRegionNonempty c := by
  obtain ⟨M, hM, hb⟩ := h
  refine ⟨1 / (2 * M), by positivity, ?_⟩
  intro ε hε
  have hh : (1 / 2 : ℚ) < 1 := by norm_num
  obtain ⟨n, hn⟩ := exists_pow_lt_of_lt_one hε hh
  refine ⟨n, fun k hk => ?_⟩
  rw [abs_of_nonneg (concv_nonneg hc (by positivity) k), concv_eq_amp]
  have hp0 : 0 ≤ (1 / (2 * M)) ^ (2 ^ k) := by positivity
  calc (1 / (2 * M)) ^ (2 ^ k) * amp c k ≤ (1 / (2 * M)) ^ (2 ^ k) * M ^ (2 ^ k) :=
        mul_le_mul_of_nonneg_left (hb k) hp0
    _ = (1 / 2) ^ (2 ^ k) := by
        rw [← mul_pow]; congr 1; field_simp
    _ ≤ (1 / 2) ^ n := pow_le_pow_of_le_one (by norm_num) hh.le (by
        have := two_pow_ge_succ k; omega)
    _ < ε := hn

theorem eventuallyBelowOne_ampBounded {c : ℕ → ℚ} (hc : ∀ k, 0 ≤ c k) (h : EventuallyBelowOne c) :
    AmpBounded c := by
  obtain ⟨p, hp, K, hK⟩ := h
  -- the finite head is bounded by one number
  set S : ℚ := 1 + ∑ k ∈ Finset.range K, amp c k with hS
  have hS1 : 1 ≤ S := by
    have : 0 ≤ ∑ k ∈ Finset.range K, amp c k := Finset.sum_nonneg (fun k _ => amp_nonneg hc k)
    linarith
  refine ⟨max (1 / p) S, lt_of_lt_of_le one_pos (le_trans hS1 (le_max_right _ _)), fun k => ?_⟩
  have hM1 : 1 ≤ max (1 / p) S := le_trans hS1 (le_max_right _ _)
  by_cases hk : K ≤ k
  · have h1 := hK k hk
    rw [concv_eq_amp] at h1
    have hpk : 0 < p ^ (2 ^ k) := by positivity
    have h2 : amp c k < 1 / p ^ (2 ^ k) := (lt_div_iff₀ hpk).2 (by linarith [mul_comm (amp c k) (p ^ (2 ^ k))])
    rw [one_div, ← inv_pow, ← one_div] at h2
    exact le_trans h2.le (pow_le_pow_left₀ (by positivity) (le_max_left _ _) _)
  · have hk' : k < K := not_le.1 hk
    have h1 : amp c k ≤ ∑ j ∈ Finset.range K, amp c j :=
      Finset.single_le_sum (f := fun j => amp c j) (fun j _ => amp_nonneg hc j) (Finset.mem_range.2 hk')
    calc amp c k ≤ S := by linarith
      _ ≤ max (1 / p) S := le_max_right _ _
      _ ≤ (max (1 / p) S) ^ (2 ^ k) := le_self_pow₀ hM1 (by positivity)

/-- Exact criterion (Q3): for positive overheads, a positive physical error rate with `p_k -> 0`
exists if and only if the weighted geometric means of `c` stay bounded, i.e.
`amp c k <= M ^ (2 ^ k)` for some `M` and all `k`.  Equivalently some `p_0 > 0` has `p_k < 1`
eventually.  The threshold region is empty exactly when `AmpBounded c` fails. -/
theorem threshold_region_iff {c : ℕ → ℚ} (hc : ∀ k, 0 ≤ c k) :
    ThresholdRegionNonempty c ↔ AmpBounded c := by
  constructor
  · rintro ⟨p, hp, hz⟩
    apply eventuallyBelowOne_ampBounded hc
    obtain ⟨K, hK⟩ := hz 1 one_pos
    refine ⟨p, hp, K, fun k hk => ?_⟩
    exact lt_of_le_of_lt (le_abs_self _) (hK k hk)
  · exact ampBounded_goesToZero hc

/-- Empty region: when `AmpBounded c` fails, every positive `p_0` has some arbitrarily late level
with `p_k >= 1`; in particular `p_k` does not tend to zero. -/
theorem region_empty_iff {c : ℕ → ℚ} (hc : ∀ k, 0 ≤ c k) :
    (∀ p : ℚ, 0 < p → ¬ GoesToZero (concv c p)) ↔ ¬ AmpBounded c := by
  constructor
  · intro h hb
    obtain ⟨p, hp, hz⟩ := (threshold_region_iff hc).2 hb
    exact h p hp hz
  · intro hb p hp hz
    exact hb ((threshold_region_iff hc).1 ⟨p, hp, hz⟩)

/-- A level-bounded overhead `c k <= C` keeps the region nonempty, with `amp c k <= C' ^ (2 ^ k)`,
`C' = max C 1`. -/
theorem amp_le_of_bounded {c : ℕ → ℚ} {C : ℚ} (hc : ∀ k, 0 ≤ c k) (hC : ∀ k, c k ≤ C) (k : ℕ) :
    amp c k * max C 1 ≤ (max C 1) ^ (2 ^ k) := by
  have hD : 1 ≤ max C 1 := le_max_right _ _
  have hD0 : 0 ≤ max C 1 := by linarith
  induction k with
  | zero => simp [amp]
  | succ k ih =>
    rw [amp, pow_succ 2 k, pow_mul]
    have h0 := amp_nonneg hc k
    have hck : c k ≤ max C 1 := le_trans (hC k) (le_max_left _ _)
    calc c k * amp c k ^ 2 * max C 1 ≤ max C 1 * amp c k ^ 2 * max C 1 :=
          mul_le_mul_of_nonneg_right (mul_le_mul_of_nonneg_right hck (sq_nonneg _)) hD0
      _ = (amp c k * max C 1) ^ 2 := by ring
      _ ≤ ((max C 1) ^ (2 ^ k)) ^ 2 := pow_le_pow_left₀ (mul_nonneg h0 hD0) ih 2

theorem ampBounded_of_bounded {c : ℕ → ℚ} {C : ℚ} (hc : ∀ k, 0 ≤ c k) (hC : ∀ k, c k ≤ C) :
    AmpBounded c := by
  refine ⟨max C 1, by positivity, fun k => ?_⟩
  have h := amp_le_of_bounded hc hC k
  have hD : 1 ≤ max C 1 := le_max_right _ _
  have h0 := amp_nonneg hc k
  nlinarith

/-- Level-bounded overhead: below `1 / C'` the error tends to zero, with the explicit bound
`p_k <= (C' * p_0) ^ (2 ^ k) / C'` (the constant-overhead closed form). -/
theorem concv_le_conc_of_bounded {c : ℕ → ℚ} {C : ℚ} (hc : ∀ k, 0 ≤ c k) (hC : ∀ k, c k ≤ C)
    {p : ℚ} (hp : 0 ≤ p) (k : ℕ) :
    concv c p k ≤ (max C 1 * p) ^ (2 ^ k) / max C 1 := by
  have hD : 0 < max C 1 := lt_of_lt_of_le one_pos (le_max_right _ _)
  have hcd : ∀ k, c k ≤ max C 1 := fun k => le_trans (hC k) (le_max_left _ _)
  have := concv_mono (d := fun _ => max C 1) hc hcd hp k
  rw [concv_const] at this
  rwa [conc_eq_div _ _ hD.ne'] at this

theorem bounded_overhead_goesToZero {c : ℕ → ℚ} {C : ℚ} (hc : ∀ k, 0 ≤ c k) (hC : ∀ k, c k ≤ C)
    {p : ℚ} (hp : 0 ≤ p) (hth : max C 1 * p < 1) : GoesToZero (concv c p) := by
  have hD : 0 < max C 1 := lt_of_lt_of_le one_pos (le_max_right _ _)
  have hz := sub_goesToZero hD hp hth
  intro ε hε
  obtain ⟨K, hK⟩ := hz ε hε
  refine ⟨K, fun k hk => ?_⟩
  have h0 := concv_nonneg hc hp k
  have h1 := concv_mono (d := fun _ => max C 1) hc
    (fun k => le_trans (hC k) (le_max_left _ _)) hp k
  rw [concv_const] at h1
  rw [abs_of_nonneg h0]
  exact lt_of_le_of_lt h1 (by simpa [abs_of_nonneg (conc_nonneg hD.le hp k)] using hK k hk)

/-- Geometric growth of the overhead, `c k <= A * B ^ (k + 1)` with `1 <= A`, `1 <= B`, keeps the
region nonempty: `amp c k * (A * B ^ (k + 2)) <= (A * B ^ 2) ^ (2 ^ k)`. -/
theorem amp_le_of_geom {c : ℕ → ℚ} {A B : ℚ} (hc : ∀ k, 0 ≤ c k) (hA : 1 ≤ A) (hB : 1 ≤ B)
    (hC : ∀ k, c k ≤ A * B ^ (k + 1)) (k : ℕ) :
    amp c k * (A * B ^ (k + 2)) ≤ (A * B ^ 2) ^ (2 ^ k) := by
  induction k with
  | zero => simp [amp]
  | succ k ih =>
    rw [amp, pow_succ 2 k, pow_mul]
    have h0 := amp_nonneg hc k
    have hA0 : 0 < A := by linarith
    have hB0 : 0 < B := by linarith
    calc c k * amp c k ^ 2 * (A * B ^ (k + 1 + 2))
        ≤ (A * B ^ (k + 1)) * amp c k ^ 2 * (A * B ^ (k + 1 + 2)) := by
          apply mul_le_mul_of_nonneg_right
          · exact mul_le_mul_of_nonneg_right (hC k) (sq_nonneg _)
          · positivity
      _ = (amp c k * (A * B ^ (k + 2))) ^ 2 := by ring
      _ ≤ ((A * B ^ 2) ^ (2 ^ k)) ^ 2 :=
          pow_le_pow_left₀ (mul_nonneg h0 (by positivity)) ih 2

theorem ampBounded_of_geom {c : ℕ → ℚ} {A B : ℚ} (hc : ∀ k, 0 ≤ c k) (hA : 1 ≤ A) (hB : 1 ≤ B)
    (hC : ∀ k, c k ≤ A * B ^ (k + 1)) : AmpBounded c := by
  have hB0 : 0 < B := by linarith
  refine ⟨A * B ^ 2, by positivity, fun k => ?_⟩
  have h := amp_le_of_geom hc hA hB hC k
  have h0 := amp_nonneg hc k
  have hf : (1 : ℚ) ≤ A * B ^ (k + 2) := by
    have : (1 : ℚ) ≤ B ^ (k + 2) := one_le_pow₀ hB
    nlinarith
  nlinarith

/-- `(k + 1) ^ 2 <= 2 ^ (k + 2)` for all `k`. -/
theorem sq_succ_le_two_pow (k : ℕ) : (k + 1) ^ 2 ≤ 2 ^ (k + 2) := by
  have key : ∀ n : ℕ, 2 ≤ n → (n + 1) ^ 2 ≤ 2 ^ (n + 2) := by
    intro n hn
    induction n, hn using Nat.le_induction with
    | base => norm_num
    | succ n hn ih =>
      calc (n + 1 + 1) ^ 2 ≤ 2 * (n + 1) ^ 2 := by nlinarith
        _ ≤ 2 * 2 ^ (n + 2) := by omega
        _ = 2 ^ (n + 1 + 2) := by ring
  rcases Nat.lt_or_ge k 2 with h | h
  · interval_cases k <;> norm_num
  · exact key k h

theorem ampBounded_poly : AmpBounded (fun k => ((k : ℚ) + 1) ^ 2) := by
  apply ampBounded_of_geom (A := 2) (B := 2) (fun k => by positivity) (by norm_num) (by norm_num)
  intro k
  have h : (k + 1) ^ 2 ≤ 2 ^ (k + 2) := sq_succ_le_two_pow k
  have h' : ((k : ℚ) + 1) ^ 2 ≤ 2 ^ (k + 2) := by exact_mod_cast h
  calc ((k : ℚ) + 1) ^ 2 ≤ 2 ^ (k + 2) := h'
    _ = 2 * 2 ^ (k + 1) := by ring

/-- The double-exponential family `d k = a * b ^ (2 ^ k)`:
`(amp d k * a) ^ 2 = (a ^ 2 * b ^ k) ^ (2 ^ k)`. -/
theorem amp_dexp_sq (a b : ℚ) (k : ℕ) :
    (amp (fun j => a * b ^ (2 ^ j)) k * a) ^ 2 = (a ^ 2 * b ^ k) ^ (2 ^ k) := by
  induction k with
  | zero => simp [amp]
  | succ k ih =>
    have h : ((a * b ^ 2 ^ k) * amp (fun j => a * b ^ (2 ^ j)) k ^ 2 * a) =
        b ^ (2 ^ k) * (amp (fun j => a * b ^ (2 ^ j)) k * a) ^ 2 := by ring
    have h2 : b ^ (2 ^ k) * (a ^ 2 * b ^ k) ^ (2 ^ k) = (a ^ 2 * b ^ (k + 1)) ^ (2 ^ k) := by
      rw [← mul_pow]; congr 1; ring
    simp only [amp]
    calc ((a * b ^ 2 ^ k) * amp (fun j => a * b ^ (2 ^ j)) k ^ 2 * a) ^ 2
        = (b ^ (2 ^ k) * (amp (fun j => a * b ^ (2 ^ j)) k * a) ^ 2) ^ 2 := by rw [h]
      _ = (b ^ (2 ^ k) * (a ^ 2 * b ^ k) ^ (2 ^ k)) ^ 2 := by rw [ih]
      _ = ((a ^ 2 * b ^ (k + 1)) ^ (2 ^ k)) ^ 2 := by rw [h2]
      _ = (a ^ 2 * b ^ (k + 1)) ^ (2 ^ (k + 1)) := by rw [← pow_mul, ← pow_succ]

theorem amp_eq_concv_one (c : ℕ → ℚ) (k : ℕ) : amp c k = concv c 1 k := by
  rw [concv_eq_amp]; simp

theorem amp_mono {c d : ℕ → ℚ} (hd : ∀ k, 0 ≤ d k) (hcd : ∀ k, d k ≤ c k) (k : ℕ) :
    amp d k ≤ amp c k := by
  rw [amp_eq_concv_one, amp_eq_concv_one]
  exact concv_mono hd hcd zero_le_one k

/-- Self-limitation (Q3): if the level overhead is at least `a * b ^ (2 ^ k)` with `a > 0`, `b > 1`
(syndrome-circuit growth of any positive double-exponential rate, `b` as close to one as desired),
the weighted means are unbounded, so by `region_empty_iff` no positive `p_0` has `p_k -> 0`. -/
theorem dexp_not_ampBounded {c : ℕ → ℚ} {a b : ℚ} (ha : 0 < a) (hb : 1 < b)
    (hge : ∀ k, a * b ^ (2 ^ k) ≤ c k) : ¬ AmpBounded c := by
  rintro ⟨M, hM, hbd⟩
  have hd : ∀ k, 0 ≤ a * b ^ (2 ^ k) := fun k => by positivity
  set m : ℚ := max 1 (a ^ 2) with hm
  have hm1 : 1 ≤ m := le_max_left _ _
  have ha2 : a ^ 2 ≤ m := le_max_right _ _
  have hN : 0 < M ^ 2 * m := by positivity
  obtain ⟨k, hk⟩ := pow_unbounded_of_one_lt (M ^ 2 * m / a ^ 2) hb
  have hk2 : M ^ 2 * m < a ^ 2 * b ^ k := by
    rw [div_lt_iff₀ (by positivity)] at hk
    linarith
  have h1 : amp (fun j => a * b ^ (2 ^ j)) k ≤ M ^ (2 ^ k) :=
    le_trans (amp_mono hd hge k) (hbd k)
  have h2 : (amp (fun j => a * b ^ (2 ^ j)) k * a) ^ 2 ≤ (M ^ (2 ^ k) * a) ^ 2 :=
    pow_le_pow_left₀ (mul_nonneg (amp_nonneg hd k) ha.le) (mul_le_mul_of_nonneg_right h1 ha.le) 2
  rw [amp_dexp_sq] at h2
  have h3 : (M ^ 2 * m) ^ (2 ^ k) < (a ^ 2 * b ^ k) ^ (2 ^ k) :=
    pow_lt_pow_left₀ hk2 hN.le (by positivity)
  have h4 : m ≤ m ^ (2 ^ k) := le_self_pow₀ hm1 (by positivity)
  have h5 : (M ^ (2 ^ k) * a) ^ 2 = (M ^ 2) ^ (2 ^ k) * a ^ 2 := by
    rw [mul_pow, ← pow_mul, ← pow_mul, mul_comm (2 ^ k) 2]
  have h6 : (M ^ 2 * m) ^ (2 ^ k) = (M ^ 2) ^ (2 ^ k) * m ^ (2 ^ k) := mul_pow _ _ _
  have h7 : 0 < (M ^ 2) ^ (2 ^ k) := by positivity
  nlinarith

theorem dexp_region_empty {c : ℕ → ℚ} {a b : ℚ} (ha : 0 < a) (hb : 1 < b)
    (hge : ∀ k, a * b ^ (2 ^ k) ≤ c k) (p : ℚ) (hp : 0 < p) : ¬ GoesToZero (concv c p) := by
  have hc : ∀ k, 0 ≤ c k := fun k => le_trans (by positivity) (hge k)
  exact (region_empty_iff hc).2 (dexp_not_ampBounded ha hb hge) p hp

/-! ## Overhead exponential in a block size that grows by a fixed factor per level -/

/-- `blockExp N`: `E 0 = 0`, `E (k + 1) = 2 E k + N k`; the exponent of `b` in `amp` when
`c k = a * b ^ N k`. -/
def blockExp (N : ℕ → ℕ) : ℕ → ℕ
  | 0 => 0
  | k + 1 => 2 * blockExp N k + N k

/-- If the block size `N k` grows at most by the factor `s < 2` per level, then
`E k + N k / (2 - s) <= 2 ^ k * N 0 / (2 - s)`. -/
theorem blockExp_le {N : ℕ → ℕ} {s : ℚ} (hs : s < 2) (hN : ∀ k, (N (k + 1) : ℚ) ≤ s * N k)
    (k : ℕ) : (blockExp N k : ℚ) + N k / (2 - s) ≤ 2 ^ k * (N 0 / (2 - s)) := by
  have h2 : 0 < 2 - s := by linarith
  induction k with
  | zero => simp [blockExp]
  | succ k ih =>
    have e : (blockExp N (k + 1) : ℚ) = 2 * blockExp N k + N k := by
      simp [blockExp]
    have h3 : (N (k + 1) : ℚ) / (2 - s) ≤ s * N k / (2 - s) :=
      div_le_div_of_nonneg_right (hN k) h2.le
    have h4 : (N k : ℚ) = (2 - s) * (N k / (2 - s)) := by field_simp
    have h5 : s * N k / (2 - s) = s * (N k / (2 - s)) := by ring
    rw [e, pow_succ]
    nlinarith

/-- Self-consistent growth (Q3, positive side): with `c k <= a * b ^ N k`, `1 <= a`, `1 <= b`, and a
block size growing by at most a factor `s < 2` per level, the weighted means stay bounded, so the
threshold region is nonempty. -/
theorem ampBounded_of_sizes {c : ℕ → ℚ} {a b s : ℚ} {N : ℕ → ℕ} (hc : ∀ k, 0 ≤ c k) (ha : 1 ≤ a)
    (hb : 1 ≤ b) (hs : s < 2) (hN : ∀ k, (N (k + 1) : ℚ) ≤ s * N k)
    (hC : ∀ k, c k ≤ a * b ^ N k) : AmpBounded c := by
  have h2 : 0 < 2 - s := by linarith
  have ha0 : 0 < a := by linarith
  have hb0 : 0 < b := by linarith
  obtain ⟨L, hL⟩ := exists_nat_ge ((N 0 : ℚ) / (2 - s))
  -- invariant: amp k * a <= a ^ (2 ^ k) * b ^ (blockExp N k)
  have inv : ∀ k, amp c k * a ≤ a ^ (2 ^ k) * b ^ (blockExp N k) := by
    intro k
    induction k with
    | zero => simp [amp, blockExp]
    | succ k ih =>
      have h0 := amp_nonneg hc k
      calc amp c (k + 1) * a = c k * amp c k ^ 2 * a := rfl
        _ ≤ (a * b ^ N k) * amp c k ^ 2 * a := by
            apply mul_le_mul_of_nonneg_right
            · exact mul_le_mul_of_nonneg_right (hC k) (sq_nonneg _)
            · exact ha0.le
        _ = b ^ N k * (amp c k * a) ^ 2 := by ring
        _ ≤ b ^ N k * (a ^ (2 ^ k) * b ^ (blockExp N k)) ^ 2 :=
            mul_le_mul_of_nonneg_left (pow_le_pow_left₀ (mul_nonneg h0 ha0.le) ih 2) (by positivity)
        _ = a ^ (2 ^ (k + 1)) * b ^ (blockExp N (k + 1)) := by
            simp only [blockExp]
            rw [pow_succ 2 k, pow_mul, mul_pow, ← pow_mul, pow_add]
            ring
  have hE : ∀ k, blockExp N k ≤ L * 2 ^ k := by
    intro k
    have h := blockExp_le hs hN k
    have h1 : (blockExp N k : ℚ) ≤ 2 ^ k * (N 0 / (2 - s)) := by
      have : 0 ≤ (N k : ℚ) / (2 - s) := by positivity
      linarith
    have h3 : (blockExp N k : ℚ) ≤ (L * 2 ^ k : ℕ) := by
      push_cast
      calc (blockExp N k : ℚ) ≤ 2 ^ k * (N 0 / (2 - s)) := h1
        _ ≤ 2 ^ k * L := mul_le_mul_of_nonneg_left hL (by positivity)
        _ = L * 2 ^ k := by ring
    exact_mod_cast h3
  refine ⟨a * b ^ L, by positivity, fun k => ?_⟩
  have h0 := amp_nonneg hc k
  have hk := inv k
  have h5 : b ^ (blockExp N k) ≤ (b ^ L) ^ (2 ^ k) := by
    rw [← pow_mul]
    exact pow_le_pow_right₀ hb (hE k)
  calc amp c k ≤ amp c k * a := by nlinarith
    _ ≤ a ^ (2 ^ k) * b ^ (blockExp N k) := hk
    _ ≤ a ^ (2 ^ k) * (b ^ L) ^ (2 ^ k) :=
        mul_le_mul_of_nonneg_left h5 (by positivity)
    _ = (a * b ^ L) ^ (2 ^ k) := (mul_pow _ _ _).symm

/-- Self-consistent growth (Q3, negative side): if the block size at least doubles per level,
`2 ^ k <= N k`, and `c k >= a * b ^ N k` with `a > 0`, `b > 1`, the weighted means are unbounded and
no positive physical rate lies below threshold. -/
theorem sizes_not_ampBounded {c : ℕ → ℚ} {a b : ℚ} {N : ℕ → ℕ} (ha : 0 < a) (hb : 1 < b)
    (hN : ∀ k, 2 ^ k ≤ N k) (hC : ∀ k, a * b ^ N k ≤ c k) : ¬ AmpBounded c := by
  apply dexp_not_ampBounded ha hb
  intro k
  exact le_trans (mul_le_mul_of_nonneg_left (pow_le_pow_right₀ hb.le (hN k)) ha.le) (hC k)

end QcSelfObstruction
