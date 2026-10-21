import HilbertLiftFiniteTower
import Mathlib.Algebra.BigOperators.Intervals
import Mathlib.Algebra.Order.Archimedean.Basic
import Mathlib.Algebra.Order.Field.Basic
import Mathlib.Algebra.Order.Ring.Abs
import Mathlib.Order.Interval.Finset.Nat
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Ring

/-!
# Rational uniformities on the exact carrier and the harmonic witness

Origin: dag/results/FQ-GAP-CONTINUUM-HILBERT-LIFT/runs/20261020T230000Z_completion
Claim: the ℓ², ℓ¹ and sup Cauchy conditions on sequences of exact vectors are stated with rational
tolerances only; ℓ¹-Cauchy implies ℓ²-Cauchy implies sup-Cauchy; the harmonic sequence
`h_N = Σ_{i<N} (1/(i+1)) e_i` is ℓ²-Cauchy with the explicit modulus `k ↦ k+1`, is not ℓ¹-Cauchy,
and converges to no exact vector.
AuthorityEffect: None
Scope Fence: no real number, no square root and no topology is used; every bound is an exact
rational inequality.  The witness shows that the choice of uniformity is a hypothesis and that the
exact carrier is not complete; it does not construct a limit.
Level: L5
-/

namespace HilbertLift

open Finset

/-- Squared ℓ² distance on the exact carrier. -/
noncomputable def sqdist (f g : Carrier) : ℚ := qinner (f - g) (f - g)

/-- ℓ¹ distance on the exact carrier. -/
noncomputable def l1dist (f g : Carrier) : ℚ := (f - g).sum fun _ a => |a|

theorem sqdist_self (f : Carrier) : sqdist f f = 0 := by
  simp [sqdist, qinner]

theorem sqdist_nonneg (f g : Carrier) : 0 ≤ sqdist f g := qinner_self_nonneg _

theorem sqdist_eq_sum (f g : Carrier) {s : Finset ℕ} (hs : (f - g).support ⊆ s) :
    sqdist f g = ∑ i ∈ s, (f i - g i) ^ 2 := by
  unfold sqdist
  rw [qinner_eq_sum _ _ hs]
  exact Finset.sum_congr rfl fun i _ => by rw [Finsupp.sub_apply, sq]

theorem sqdist_comm (f g : Carrier) : sqdist f g = sqdist g f := by
  classical
  rw [sqdist_eq_sum f g (s := f.support ∪ g.support) Finsupp.support_sub,
    sqdist_eq_sum g f (s := f.support ∪ g.support)
      (by rw [Finset.union_comm]; exact Finsupp.support_sub)]
  exact Finset.sum_congr rfl fun i _ => by ring

theorem sq_sub_apply_le_sqdist (f g : Carrier) (i : ℕ) : (f i - g i) ^ 2 ≤ sqdist f g := by
  have h := mul_self_apply_le_qinner_self (f - g) i
  rwa [Finsupp.sub_apply, ← sq] at h

/-- The doubling triangle inequality for squared distances; no square root is needed. -/
theorem sqdist_le_two_mul (f g h : Carrier) : sqdist f h ≤ 2 * (sqdist f g + sqdist g h) := by
  have key : f - h = (f - g) + (g - h) := by abel
  unfold sqdist
  rw [key, qinner_add_left, qinner_add_right, qinner_add_right, qinner_comm (g - h) (f - g)]
  have h2 := two_mul_qinner_le (f - g) (g - h)
  linarith

theorem l1dist_eq_sum (f g : Carrier) {s : Finset ℕ} (hs : (f - g).support ⊆ s) :
    l1dist f g = ∑ i ∈ s, |f i - g i| := by
  unfold l1dist
  rw [Finsupp.sum_of_support_subset _ hs _ (fun i _ => abs_zero)]
  exact Finset.sum_congr rfl fun i _ => by rw [Finsupp.sub_apply]

theorem l1dist_nonneg (f g : Carrier) : 0 ≤ l1dist f g := by
  rw [l1dist_eq_sum f g (subset_refl _)]
  exact Finset.sum_nonneg fun i _ => abs_nonneg _

/-- ℓ² is dominated by ℓ¹ on the exact carrier. -/
theorem sqdist_le_l1dist_sq (f g : Carrier) : sqdist f g ≤ l1dist f g ^ 2 := by
  classical
  rw [sqdist_eq_sum f g (subset_refl _), l1dist_eq_sum f g (subset_refl _), sq, Finset.sum_mul]
  refine Finset.sum_le_sum fun i hi => ?_
  rw [← sq_abs, sq]
  exact mul_le_mul_of_nonneg_left
    (Finset.single_le_sum (fun j _ => abs_nonneg (f j - g j)) hi) (abs_nonneg _)

/-- ℓ²-Cauchy with rational tolerances. -/
def IsCauchyL2 (x : ℕ → Carrier) : Prop :=
  ∀ ε : ℚ, 0 < ε → ∃ N : ℕ, ∀ m, N ≤ m → ∀ n, N ≤ n → sqdist (x m) (x n) < ε

/-- ℓ¹-Cauchy with rational tolerances. -/
def IsCauchyL1 (x : ℕ → Carrier) : Prop :=
  ∀ ε : ℚ, 0 < ε → ∃ N : ℕ, ∀ m, N ≤ m → ∀ n, N ≤ n → l1dist (x m) (x n) < ε

/-- Coordinatewise-uniform (sup) Cauchy with rational tolerances. -/
def IsCauchySup (x : ℕ → Carrier) : Prop :=
  ∀ ε : ℚ, 0 < ε → ∃ N : ℕ, ∀ m, N ≤ m → ∀ n, N ≤ n → ∀ i, |x m i - x n i| < ε

/-- ℓ² convergence to an exact vector, with rational tolerances. -/
def TendsToL2 (x : ℕ → Carrier) (f : Carrier) : Prop :=
  ∀ ε : ℚ, 0 < ε → ∃ N : ℕ, ∀ n, N ≤ n → sqdist (x n) f < ε

/-- An explicit Cauchy modulus: `μ k` is a stage after which squared distances are below
`1/(k+1)`. -/
def HasModulusL2 (x : ℕ → Carrier) (μ : ℕ → ℕ) : Prop :=
  ∀ k m n, μ k ≤ m → μ k ≤ n → sqdist (x m) (x n) < 1 / ((k : ℚ) + 1)

theorem isCauchyL2_of_hasModulus {x : ℕ → Carrier} {μ : ℕ → ℕ} (h : HasModulusL2 x μ) :
    IsCauchyL2 x := by
  intro ε hε
  obtain ⟨k, hk⟩ := exists_nat_one_div_lt hε
  exact ⟨μ k, fun m hm n hn => (h k m n hm hn).trans hk⟩

theorem exists_hasModulus_of_isCauchyL2 {x : ℕ → Carrier} (h : IsCauchyL2 x) :
    ∃ μ : ℕ → ℕ, HasModulusL2 x μ := by
  have hk : ∀ k : ℕ, ∃ N : ℕ, ∀ m, N ≤ m → ∀ n, N ≤ n →
      sqdist (x m) (x n) < 1 / ((k : ℚ) + 1) :=
    fun k => h _ (by positivity)
  choose μ hμ using hk
  exact ⟨μ, fun k m n hm hn => hμ k m hm n hn⟩

/-- ℓ¹-Cauchy sequences are ℓ²-Cauchy. -/
theorem isCauchyL2_of_isCauchyL1 {x : ℕ → Carrier} (h : IsCauchyL1 x) : IsCauchyL2 x := by
  intro ε hε
  obtain ⟨N, hN⟩ := h (min ε 1) (lt_min hε one_pos)
  refine ⟨N, fun m hm n hn => ?_⟩
  have h1 := hN m hm n hn
  have h0 := l1dist_nonneg (x m) (x n)
  have hmin : min ε 1 ≤ ε := min_le_left _ _
  have hmin1 : min ε 1 ≤ 1 := min_le_right _ _
  have hpos : 0 < min ε 1 := lt_min hε one_pos
  calc sqdist (x m) (x n) ≤ l1dist (x m) (x n) ^ 2 := sqdist_le_l1dist_sq _ _
    _ < min ε 1 ^ 2 := by nlinarith
    _ ≤ min ε 1 := by nlinarith
    _ ≤ ε := hmin

/-- ℓ²-Cauchy sequences are coordinatewise-uniformly Cauchy. -/
theorem isCauchySup_of_isCauchyL2 {x : ℕ → Carrier} (h : IsCauchyL2 x) : IsCauchySup x := by
  intro ε hε
  obtain ⟨N, hN⟩ := h (ε ^ 2) (by positivity)
  refine ⟨N, fun m hm n hn i => ?_⟩
  have h1 := (sq_sub_apply_le_sqdist (x m) (x n) i).trans_lt (hN m hm n hn)
  exact abs_lt_of_sq_lt_sq h1 hε.le

/-- The harmonic coordinate `1/(i+1)`. -/
def harmonicTerm (i : ℕ) : ℚ := 1 / ((i : ℚ) + 1)

theorem harmonicTerm_pos (i : ℕ) : 0 < harmonicTerm i := by
  unfold harmonicTerm
  positivity

/-- The harmonic witness `h_N = Σ_{i<N} (1/(i+1)) e_i`. -/
noncomputable def harmonic (N : ℕ) : Carrier :=
  Finsupp.onFinset (range N) (fun i => if i < N then harmonicTerm i else 0) fun i hi => by
    by_contra h
    exact hi (if_neg fun h' => h (mem_range.mpr h'))

@[simp] theorem harmonic_apply (N i : ℕ) :
    harmonic N i = if i < N then harmonicTerm i else 0 :=
  Finsupp.onFinset_apply

theorem support_harmonic_subset (N : ℕ) : (harmonic N).support ⊆ range N :=
  Finsupp.support_onFinset_subset

theorem harmonic_sub_apply {n m : ℕ} (hnm : n ≤ m) (i : ℕ) :
    (harmonic m - harmonic n) i = if n ≤ i ∧ i < m then harmonicTerm i else 0 := by
  rw [Finsupp.sub_apply, harmonic_apply, harmonic_apply]
  by_cases h1 : i < n
  · have h2 : i < m := lt_of_lt_of_le h1 hnm
    simp [h1, h2, not_le.mpr h1]
  · by_cases h2 : i < m
    · simp [h1, h2, not_lt.mp h1]
    · simp [h1, h2]

theorem support_harmonic_sub_subset {n m : ℕ} (hnm : n ≤ m) :
    (harmonic m - harmonic n).support ⊆ Ico n m := by
  intro i hi
  rw [Finsupp.mem_support_iff, harmonic_sub_apply hnm] at hi
  by_contra h
  exact hi (if_neg fun h' => h (mem_Ico.mpr h'))

theorem sqdist_harmonic {n m : ℕ} (hnm : n ≤ m) :
    sqdist (harmonic m) (harmonic n) = ∑ i ∈ Ico n m, harmonicTerm i ^ 2 := by
  rw [sqdist_eq_sum _ _ (support_harmonic_sub_subset hnm)]
  refine Finset.sum_congr rfl fun i hi => ?_
  have h := harmonic_sub_apply hnm i
  rw [Finsupp.sub_apply] at h
  rw [h, if_pos (mem_Ico.mp hi)]

theorem l1dist_harmonic {n m : ℕ} (hnm : n ≤ m) :
    l1dist (harmonic m) (harmonic n) = ∑ i ∈ Ico n m, harmonicTerm i := by
  rw [l1dist_eq_sum _ _ (support_harmonic_sub_subset hnm)]
  refine Finset.sum_congr rfl fun i hi => ?_
  have h := harmonic_sub_apply hnm i
  rw [Finsupp.sub_apply] at h
  rw [h, if_pos (mem_Ico.mp hi), abs_of_pos (harmonicTerm_pos i)]

/-- The telescoping bound `1/(i+1)^2 ≤ 1/i - 1/(i+1)` for `i ≥ 1`. -/
theorem harmonicTerm_sq_le {i : ℕ} (hi : 1 ≤ i) :
    harmonicTerm i ^ 2 ≤ 1 / (i : ℚ) - 1 / ((i : ℚ) + 1) := by
  have hi' : (0 : ℚ) < i := by exact_mod_cast hi
  have h1 : 1 / (i : ℚ) - 1 / ((i : ℚ) + 1) = 1 / ((i : ℚ) * ((i : ℚ) + 1)) := by
    rw [div_sub_div _ _ (ne_of_gt hi') (by positivity)]
    congr 1
    ring
  rw [h1]
  unfold harmonicTerm
  rw [div_pow, one_pow]
  apply one_div_le_one_div_of_le (by positivity)
  nlinarith

theorem sum_harmonicTerm_sq_le {n : ℕ} (hn : 1 ≤ n) :
    ∀ m, n ≤ m → ∑ i ∈ Ico n m, harmonicTerm i ^ 2 ≤ 1 / (n : ℚ) - 1 / (m : ℚ) := by
  intro m hm
  induction m, hm using Nat.le_induction with
  | base => simp
  | succ m hnm ih =>
    rw [Finset.sum_Ico_succ_top hnm]
    have h := harmonicTerm_sq_le (hn.trans hnm)
    push_cast
    linarith

theorem sqdist_harmonic_lt {n m : ℕ} (hn : 1 ≤ n) (hnm : n ≤ m) :
    sqdist (harmonic m) (harmonic n) < 1 / (n : ℚ) := by
  rw [sqdist_harmonic hnm]
  have h1 := sum_harmonicTerm_sq_le hn m hnm
  have hm : (0 : ℚ) < m := by exact_mod_cast (hn.trans hnm)
  have h2 : (0 : ℚ) < 1 / (m : ℚ) := by positivity
  linarith

/-- The harmonic witness has the explicit ℓ² modulus `k ↦ k + 1`. -/
theorem harmonic_hasModulus : HasModulusL2 harmonic fun k => k + 1 := by
  intro k m n hm hn
  simp only at hm hn
  have hk : (1 : ℚ) / ((k : ℚ) + 1) = 1 / ((k + 1 : ℕ) : ℚ) := by push_cast; rfl
  rw [hk]
  rcases le_total n m with h | h
  · calc sqdist (harmonic m) (harmonic n) < 1 / (n : ℚ) := sqdist_harmonic_lt (by omega) h
      _ ≤ 1 / ((k + 1 : ℕ) : ℚ) :=
        one_div_le_one_div_of_le (by positivity) (Nat.cast_le.mpr hn)
  · rw [sqdist_comm]
    calc sqdist (harmonic n) (harmonic m) < 1 / (m : ℚ) := sqdist_harmonic_lt (by omega) h
      _ ≤ 1 / ((k + 1 : ℕ) : ℚ) :=
        one_div_le_one_div_of_le (by positivity) (Nat.cast_le.mpr hm)

theorem harmonic_isCauchyL2 : IsCauchyL2 harmonic :=
  isCauchyL2_of_hasModulus harmonic_hasModulus

theorem harmonicTerm_ge {n i : ℕ} (hi : i < 2 * n) : 1 / (2 * (n : ℚ)) ≤ harmonicTerm i := by
  unfold harmonicTerm
  apply one_div_le_one_div_of_le (by positivity)
  have h : i + 1 ≤ 2 * n := Nat.succ_le_of_lt hi
  exact_mod_cast h

theorem sum_harmonicTerm_Ico_ge (n : ℕ) (hn : 1 ≤ n) :
    1 / 2 ≤ ∑ i ∈ Ico n (2 * n), harmonicTerm i := by
  have h1 : ∑ i ∈ Ico n (2 * n), (1 / (2 * (n : ℚ))) ≤ ∑ i ∈ Ico n (2 * n), harmonicTerm i :=
    Finset.sum_le_sum fun i hi => harmonicTerm_ge (mem_Ico.mp hi).2
  rw [Finset.sum_const, Nat.card_Ico, nsmul_eq_mul] at h1
  have hn' : (0 : ℚ) < n := by exact_mod_cast hn
  have h2 : ((2 * n - n : ℕ) : ℚ) = n := by
    rw [Nat.cast_sub (by omega)]
    push_cast
    ring
  rw [h2] at h1
  have h3 : (n : ℚ) * (1 / (2 * n)) = 1 / 2 := by
    rw [mul_one_div, div_eq_iff (by positivity)]
    ring
  linarith

/-- The harmonic witness is not ℓ¹-Cauchy: the same exact sequence separates the two
uniformities. -/
theorem harmonic_not_isCauchyL1 : ¬ IsCauchyL1 harmonic := by
  intro h
  obtain ⟨N, hN⟩ := h (1 / 2) (by norm_num)
  have h1 := hN (2 * (N + 1)) (by omega) (N + 1) (by omega)
  rw [l1dist_harmonic (by omega)] at h1
  have h2 := sum_harmonicTerm_Ico_ge (N + 1) (by omega)
  linarith

/-- The harmonic witness converges to no exact vector: the exact carrier is not complete. -/
theorem harmonic_not_tendsTo (f : Carrier) : ¬ TendsToL2 harmonic f := by
  obtain ⟨M, hM⟩ := Finset.exists_nat_subset_range f.support
  intro h
  obtain ⟨N, hN⟩ := h (harmonicTerm M ^ 2) (by have := harmonicTerm_pos M; positivity)
  have h1 := hN (max N (M + 1)) (le_max_left _ _)
  have hfM : f M = 0 := by
    by_contra hne
    exact absurd (mem_range.mp (hM (Finsupp.mem_support_iff.mpr hne))) (lt_irrefl M)
  have h2 : harmonicTerm M ^ 2 ≤ sqdist (harmonic (max N (M + 1))) f := by
    have h3 := sq_sub_apply_le_sqdist (harmonic (max N (M + 1))) f M
    rwa [harmonic_apply, if_pos (by omega), hfM, sub_zero] at h3
  linarith

/-- Summary: the uniformity is a hypothesis (ℓ² and ℓ¹ differ on an exact sequence) and the exact
carrier is not complete. -/
theorem harmonic_separates_uniformities :
    IsCauchyL2 harmonic ∧ ¬ IsCauchyL1 harmonic ∧ ∀ f : Carrier, ¬ TendsToL2 harmonic f :=
  ⟨harmonic_isCauchyL2, harmonic_not_isCauchyL1, harmonic_not_tendsTo⟩

end HilbertLift

#print axioms HilbertLift.sqdist_comm
#print axioms HilbertLift.sqdist_self
#print axioms HilbertLift.sqdist_nonneg
#print axioms HilbertLift.sqdist_eq_sum
#print axioms HilbertLift.sq_sub_apply_le_sqdist
#print axioms HilbertLift.sqdist_le_two_mul
#print axioms HilbertLift.l1dist_eq_sum
#print axioms HilbertLift.l1dist_nonneg
#print axioms HilbertLift.sqdist_le_l1dist_sq
#print axioms HilbertLift.isCauchyL2_of_hasModulus
#print axioms HilbertLift.exists_hasModulus_of_isCauchyL2
#print axioms HilbertLift.isCauchyL2_of_isCauchyL1
#print axioms HilbertLift.isCauchySup_of_isCauchyL2
#print axioms HilbertLift.harmonicTerm_pos
#print axioms HilbertLift.harmonic_sub_apply
#print axioms HilbertLift.support_harmonic_sub_subset
#print axioms HilbertLift.sqdist_harmonic
#print axioms HilbertLift.l1dist_harmonic
#print axioms HilbertLift.harmonicTerm_sq_le
#print axioms HilbertLift.sum_harmonicTerm_sq_le
#print axioms HilbertLift.sqdist_harmonic_lt
#print axioms HilbertLift.harmonic_hasModulus
#print axioms HilbertLift.harmonic_isCauchyL2
#print axioms HilbertLift.harmonicTerm_ge
#print axioms HilbertLift.sum_harmonicTerm_Ico_ge
#print axioms HilbertLift.harmonic_not_isCauchyL1
#print axioms HilbertLift.harmonic_not_tendsTo
#print axioms HilbertLift.harmonic_separates_uniformities
