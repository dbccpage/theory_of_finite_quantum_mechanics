import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.RingTheory.Algebraic.Integral
import Mathlib.LinearAlgebra.LinearIndependent.Lemmas
import Mathlib.LinearAlgebra.Finsupp.LinearCombination
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Positivity

open scoped BigOperators

namespace C750B01

structure AlgebraicSpectrum (d : ℕ) where
  p : Fin d → ℝ
  nonneg : ∀ i, 0 ≤ p i
  normalized : ∑ i, p i = 1
  algebraic : ∀ i, IsAlgebraic ℚ (p i)

noncomputable def entropy {d : ℕ} (s : AlgebraicSpectrum d) : ℝ :=
  ∑ i, -(s.p i) * Real.log (s.p i)

def Pure {d : ℕ} (s : AlgebraicSpectrum d) : Prop :=
  ∃ j, s.p j = 1 ∧ ∀ i, i ≠ j → s.p i = 0

noncomputable def logArgument {d : ℕ} (s : AlgebraicSpectrum d) (i : Fin d) : ℝ :=
  if s.p i = 0 then 1 else s.p i

theorem probability_le_one {d : ℕ} (s : AlgebraicSpectrum d) (i : Fin d) :
    s.p i ≤ 1 := by
  rw [← s.normalized]
  exact Finset.single_le_sum (fun j _ => s.nonneg j) (Finset.mem_univ i)

theorem entropy_term_nonneg {x : ℝ} (h0 : 0 ≤ x) (h1 : x ≤ 1) :
    0 ≤ -x * Real.log x := by
  exact mul_nonneg_of_nonpos_of_nonpos (neg_nonpos.mpr h0) (Real.log_nonpos h0 h1)

theorem entropy_term_zero_iff {x : ℝ} (h0 : 0 ≤ x) (h1 : x ≤ 1) :
    -x * Real.log x = 0 ↔ x = 0 ∨ x = 1 := by
  constructor
  · intro hz
    rcases mul_eq_zero.mp hz with hx | hl
    · exact Or.inl (neg_eq_zero.mp hx)
    · by_cases hx : x = 0
      · exact Or.inl hx
      · exact Or.inr (Real.eq_one_of_pos_of_log_eq_zero (lt_of_le_of_ne h0 (Ne.symm hx)) hl)
  · rintro (rfl | rfl) <;> simp

theorem entropy_zero_iff_pure {d : ℕ} (s : AlgebraicSpectrum d) :
    entropy s = 0 ↔ Pure s := by
  classical
  constructor
  · intro hz
    have ht : ∀ i, s.p i = 0 ∨ s.p i = 1 := by
      intro i
      apply (entropy_term_zero_iff (s.nonneg i) (probability_le_one s i)).mp
      exact (Finset.sum_eq_zero_iff_of_nonneg
        (fun j _ => entropy_term_nonneg (s.nonneg j) (probability_le_one s j))).mp hz i
        (Finset.mem_univ i)
    have hn : ∃ j, s.p j ≠ 0 := by
      by_contra h
      push Not at h
      have : (∑ j, s.p j) = 0 := by simp [h]
      linarith [s.normalized]
    obtain ⟨j, hj⟩ := hn
    have hj1 := (ht j).resolve_left hj
    refine ⟨j, hj1, ?_⟩
    intro i hij
    have he : (∑ k ∈ Finset.univ.erase j, s.p k) = 0 := by
      have h := Finset.sum_erase_add (s := Finset.univ) (f := s.p) (Finset.mem_univ j)
      rw [s.normalized, hj1] at h
      linarith
    exact (Finset.sum_eq_zero_iff_of_nonneg (fun k _ => s.nonneg k)).mp he i
      (Finset.mem_erase.mpr ⟨hij, Finset.mem_univ i⟩)
  · rintro ⟨j, hj, hrest⟩
    apply Finset.sum_eq_zero
    intro i _
    by_cases hi : i = j
    · simp [hi, hj]
    · simp [hrest i hi]

theorem entropy_nonnegative {d : ℕ} (s : AlgebraicSpectrum d) : 0 ≤ entropy s := by
  exact Finset.sum_nonneg (fun i _ => entropy_term_nonneg (s.nonneg i) (probability_le_one s i))

theorem mixed_entropy_positive {d : ℕ} (s : AlgebraicSpectrum d) (hm : ¬ Pure s) :
    0 < entropy s := by
  have hn : entropy s ≠ 0 := fun h => hm ((entropy_zero_iff_pure s).mp h)
  exact lt_of_le_of_ne (entropy_nonnegative s) (Ne.symm hn)

theorem logArgument_positive {d : ℕ} (s : AlgebraicSpectrum d) (i : Fin d) :
    0 < logArgument s i := by
  unfold logArgument
  split_ifs with h
  · exact zero_lt_one
  · exact lt_of_le_of_ne (s.nonneg i) (Ne.symm h)

theorem logArgument_algebraic {d : ℕ} (s : AlgebraicSpectrum d) (i : Fin d) :
    IsAlgebraic ℚ (logArgument s i) := by
  unfold logArgument
  split_ifs
  · exact isAlgebraic_one
  · exact s.algebraic i

theorem entropy_linear_form {d : ℕ} (s : AlgebraicSpectrum d) :
    entropy s = ∑ i, -(s.p i) * Real.log (logArgument s i) := by
  apply Finset.sum_congr rfl
  intro i _
  unfold logArgument
  split_ifs with h
  · simp [h]
  · rfl

theorem rational_log_basis_exists {d : ℕ} (q : Fin d → ℝ) :
    ∃ (κ : Type) (_ : Fintype κ) (a : κ → Fin d) (coordinates : Fin d → κ → ℚ),
      LinearIndependent ℚ (fun k => Real.log (q (a k))) ∧
      ∀ i, Real.log (q i) = ∑ k, (coordinates i k : ℝ) * Real.log (q (a k)) := by
  classical
  obtain ⟨κ, a, ha, hspan, hli⟩ :=
    exists_linearIndependent' ℚ (fun i => Real.log (q i))
  let : Finite κ := Finite.of_injective a ha
  let : Fintype κ := Fintype.ofFinite κ
  have hmem (i : Fin d) : Real.log (q i) ∈
      Submodule.span ℚ (Set.range (fun k => Real.log (q (a k)))) := by
    change Real.log (q i) ∈ Submodule.span ℚ
      (Set.range ((fun j => Real.log (q j)) ∘ a))
    rw [hspan]
    exact Submodule.subset_span ⟨i, rfl⟩
  have hc (i : Fin d) : ∃ c : κ → ℚ,
      ∑ k, (c k : ℝ) * Real.log (q (a k)) = Real.log (q i) := by
    simpa only [Rat.smul_def] using
      (Submodule.mem_span_range_iff_exists_fun ℚ).mp (hmem i)
  choose c hc using hc
  exact ⟨κ, inferInstance, a, c, hli, fun i => (hc i).symm⟩

theorem algebraic_finite_sum {ι : Type} (t : Finset ι) (f : ι → ℝ)
    (hf : ∀ i ∈ t, IsAlgebraic ℚ (f i)) : IsAlgebraic ℚ (∑ i ∈ t, f i) := by
  classical
  induction t using Finset.induction_on with
  | empty => simpa using (isAlgebraic_zero : IsAlgebraic ℚ (0 : ℝ))
  | @insert i t hi ih =>
    rw [Finset.sum_insert hi]
    exact (hf i (Finset.mem_insert_self i t)).add
      (ih (fun j hj => hf j (Finset.mem_insert_of_mem hj)))

theorem dependence_transport {d : ℕ} {κ : Type} [Fintype κ]
    (p q : Fin d → ℝ) (a : κ → Fin d) (c : Fin d → κ → ℚ)
    (hc : ∀ i, Real.log (q i) = ∑ k, (c i k : ℝ) * Real.log (q (a k))) :
    (∑ i, -(p i) * Real.log (q i)) =
      ∑ k, (∑ i, -(p i) * (c i k : ℝ)) * Real.log (q (a k)) := by
  calc
    (∑ i, -(p i) * Real.log (q i)) =
        ∑ i, ∑ k, -(p i) * ((c i k : ℝ) * Real.log (q (a k))) := by
      apply Finset.sum_congr rfl
      intro i _
      rw [hc i, Finset.mul_sum]
    _ = ∑ k, (∑ i, -(p i) * (c i k : ℝ)) * Real.log (q (a k)) := by
      rw [Finset.sum_comm]
      apply Finset.sum_congr rfl
      intro k _
      rw [Finset.sum_mul]
      apply Finset.sum_congr rfl
      intro i _
      ring

def BakerCitedInput : Prop :=
  ∀ (ι : Type) [Fintype ι] (q c : ι → ℝ),
    (∀ i, 0 < q i) → (∀ i, IsAlgebraic ℚ (q i)) →
    (∀ i, IsAlgebraic ℚ (c i)) →
    (∑ i, c i * Real.log (q i)) ≠ 0 →
    Transcendental ℚ (∑ i, c i * Real.log (q i))

theorem entropy_dichotomy_general_dimension (baker : BakerCitedInput)
    {d : ℕ} (s : AlgebraicSpectrum d) :
    entropy s = 0 ∨ Transcendental ℚ (entropy s) := by
  classical
  by_cases hz : entropy s = 0
  · exact Or.inl hz
  · right
    obtain ⟨κ, inst, a, c, _hli, hc⟩ := rational_log_basis_exists (logArgument s)
    let : Fintype κ := inst
    let beta (k : κ) : ℝ := ∑ i, -(s.p i) * (c i k : ℝ)
    have heq : entropy s = ∑ k, beta k * Real.log (logArgument s (a k)) := by
      rw [entropy_linear_form s]
      exact dependence_transport s.p (logArgument s) a c hc
    have hb (k : κ) : IsAlgebraic ℚ (beta k) := by
      apply algebraic_finite_sum
      intro i _
      exact (s.algebraic i).neg.mul (isAlgebraic_ratCast ℚ (c i k))
    rw [heq]
    exact baker κ (fun k => logArgument s (a k)) beta
      (fun k => logArgument_positive s (a k))
      (fun k => logArgument_algebraic s (a k)) hb (heq ▸ hz)

theorem mixed_entropy_transcendental (baker : BakerCitedInput)
    {d : ℕ} (s : AlgebraicSpectrum d) (hm : ¬ Pure s) :
    Transcendental ℚ (entropy s) := by
  rcases entropy_dichotomy_general_dimension baker s with hz | ht
  · exact False.elim (hm ((entropy_zero_iff_pure s).mp hz))
  · exact ht

theorem entropy_algebraic_iff_pure (baker : BakerCitedInput)
    {d : ℕ} (s : AlgebraicSpectrum d) : IsAlgebraic ℚ (entropy s) ↔ Pure s := by
  constructor
  · intro ha
    by_contra hm
    exact mixed_entropy_transcendental baker s hm ha
  · intro hp
    rw [(entropy_zero_iff_pure s).mpr hp]
    exact isAlgebraic_zero

theorem carrier_membership_iff_pure (baker : BakerCitedInput)
    (K : Set ℝ) (hzero : 0 ∈ K) (halg : ∀ x ∈ K, IsAlgebraic ℚ x)
    {d : ℕ} (s : AlgebraicSpectrum d) : entropy s ∈ K ↔ Pure s := by
  constructor
  · intro h
    exact (entropy_algebraic_iff_pure baker s).mp (halg _ h)
  · intro h
    rw [(entropy_zero_iff_pure s).mpr h]
    exact hzero

theorem vanishing_log_control : Real.log 4 - 2 * Real.log 2 = 0 := by
  have h := Real.log_pow (2 : ℝ) 2
  norm_num at h
  linarith

#print axioms AlgebraicSpectrum
#print axioms entropy
#print axioms Pure
#print axioms logArgument
#print axioms BakerCitedInput
#print axioms probability_le_one
#print axioms entropy_term_nonneg
#print axioms entropy_term_zero_iff
#print axioms entropy_zero_iff_pure
#print axioms entropy_nonnegative
#print axioms mixed_entropy_positive
#print axioms logArgument_positive
#print axioms logArgument_algebraic
#print axioms entropy_linear_form
#print axioms rational_log_basis_exists
#print axioms algebraic_finite_sum
#print axioms dependence_transport
#print axioms entropy_dichotomy_general_dimension
#print axioms mixed_entropy_transcendental
#print axioms entropy_algebraic_iff_pure
#print axioms carrier_membership_iff_pure
#print axioms vanishing_log_control

end C750B01

private def l5aProvenance : String :=
  "Origin: lean4/EntropyDichotomy.lean Claim: probability_le_one AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
