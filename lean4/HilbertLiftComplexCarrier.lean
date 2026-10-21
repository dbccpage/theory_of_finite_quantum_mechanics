import HilbertLiftCompletion
import Mathlib.Analysis.Complex.Basic

/-!
# The Gaussian-rational carrier in the complex Hilbert lift

Origin: dag/results/FQ-GAP-CONTINUUM-HILBERT-LIFT/runs/20261020T230000Z_completion
Claim: pairs `(a, b)` of exact rational sequences, read as `a + i b`, embed into the complex
pre-Hilbert carrier `PreH ℂ` with the exact inner-product identity
`⟪a + ib, c + id⟫ = (⟨a,c⟩ + ⟨b,d⟩) + i (⟨a,d⟩ − ⟨b,c⟩)`; they are dense in `PreH ℂ`, hence in
the complex Hilbert lift; and the complex lift is strictly larger than the Gaussian-rational
carrier (the harmonic witness has no Gaussian-rational limit).
AuthorityEffect: None
Scope Fence: the complex field `ℂ` is the supplied scalar field (so `ℚ(i) → ℂ` is a completion
hypothesis, exactly as `ℚ → ℝ` is in the real case); nothing selects it.  No Gaussian-rational
field structure is formalised: a pair of rational sequences is the carrier, and the complex
multiplication enters only through the inner product identity.
Level: L5
-/

namespace HilbertLift

open Finset Filter Topology UniformSpace

/-- The Gaussian-rational carrier element `a + i b` inside the complex pre-Hilbert carrier. -/
noncomputable def castPair (a b : Carrier) : PreH ℂ := castSeq ℂ a + Complex.I • castSeq ℂ b

theorem castPair_apply (a b : Carrier) (i : ℕ) :
    castPair a b i = (a i : ℂ) + Complex.I * (b i : ℂ) := by
  simp [castPair, Finsupp.add_apply, Finsupp.smul_apply, castSeq_apply, smul_eq_mul]

theorem castPair_re (a b : Carrier) (i : ℕ) : (castPair a b i).re = a i := by
  rw [castPair_apply]
  simp

theorem castPair_im (a b : Carrier) (i : ℕ) : (castPair a b i).im = b i := by
  rw [castPair_apply]
  simp

theorem support_castPair_subset (a b : Carrier) :
    (castPair a b).support ⊆ a.support ∪ b.support := by
  classical
  refine Finsupp.support_add.trans (Finset.union_subset_union (support_castSeq_subset a) ?_)
  exact Finsupp.support_smul.trans (support_castSeq_subset b)

theorem castPair_sub (a b c d : Carrier) :
    castPair a b - castPair c d = castPair (a - c) (b - d) :=
  Finsupp.ext fun i => by
    rw [Finsupp.sub_apply, castPair_apply, castPair_apply, castPair_apply, Finsupp.sub_apply,
      Finsupp.sub_apply]
    push_cast
    ring

theorem castPair_zero_right (a : Carrier) : castPair a 0 = castSeq ℂ a := by
  simp [castPair, castSeq]

/-- The exact inner-product identity for Gaussian-rational pairs. -/
theorem inner_castPair (a b c d : Carrier) :
    inner ℂ (castPair a b) (castPair c d) =
      ((qinner a c + qinner b d : ℚ) : ℂ) + Complex.I * ((qinner a d - qinner b c : ℚ) : ℂ) := by
  classical
  have ha : a.support ⊆ a.support ∪ b.support ∪ (c.support ∪ d.support) :=
    subset_union_left.trans subset_union_left
  have hb : b.support ⊆ a.support ∪ b.support ∪ (c.support ∪ d.support) :=
    subset_union_right.trans subset_union_left
  rw [inner_def, preInner_eq_sum _ _ ((support_castPair_subset a b).trans subset_union_left),
    qinner_eq_sum a c ha, qinner_eq_sum b d hb, qinner_eq_sum a d ha, qinner_eq_sum b c hb]
  push_cast
  rw [← Finset.sum_add_distrib, ← Finset.sum_sub_distrib, Finset.mul_sum, ← Finset.sum_add_distrib]
  refine Finset.sum_congr rfl fun i _ => ?_
  rw [castPair_apply, castPair_apply]
  apply Complex.ext <;> simp
  ring

theorem norm_castPair_sq (a b : Carrier) :
    ‖castPair a b‖ ^ 2 = ((qinner a a + qinner b b : ℚ) : ℝ) := by
  rw [norm_sq_eq_re_inner (𝕜 := ℂ), inner_castPair]
  simp

theorem norm_sq_apply_complex (z : ℂ) : ‖z‖ ^ 2 = z.re ^ 2 + z.im ^ 2 := by
  rw [Complex.sq_norm, Complex.normSq_apply]
  ring

theorem norm_sq_eq_sum_complex (g : PreH ℂ) {s : Finset ℕ} (hs : g.support ⊆ s) :
    ‖g‖ ^ 2 = ∑ i ∈ s, ‖g i‖ ^ 2 := by
  rw [norm_sq_eq_re_inner (𝕜 := ℂ), inner_def, re_preInner_self g hs]

/-- Density of the Gaussian-rational carrier in the complex pre-Hilbert carrier. -/
theorem denseRange_castPair : DenseRange (fun p : Carrier × Carrier => castPair p.1 p.2) := by
  classical
  rw [Metric.denseRange_iff]
  intro f r hr
  set s := f.support with hs
  have hδpos : 0 < r / (2 * ((s.card : ℝ) + 1)) := by positivity
  choose pf hpf using fun i => exists_rat_near (f i).re hδpos
  choose qf hqf using fun i => exists_rat_near (f i).im hδpos
  set p : Carrier := Finsupp.onFinset s (fun i => if i ∈ s then pf i else 0) fun i hi => by
    by_contra h
    exact hi (if_neg h) with hpdef
  set q : Carrier := Finsupp.onFinset s (fun i => if i ∈ s then qf i else 0) fun i hi => by
    by_contra h
    exact hi (if_neg h) with hqdef
  refine ⟨(p, q), ?_⟩
  show dist f (castPair p q) < r
  have hsupp : (f - castPair p q).support ⊆ s := by
    refine Finsupp.support_sub.trans (Finset.union_subset (subset_refl _) ?_)
    exact (support_castPair_subset p q).trans
      (Finset.union_subset Finsupp.support_onFinset_subset Finsupp.support_onFinset_subset)
  have hterm : ∀ i ∈ s,
      ‖(f - castPair p q) i‖ ^ 2 < 2 * (r / (2 * ((s.card : ℝ) + 1))) ^ 2 := by
    intro i hi
    rw [norm_sq_apply_complex, Finsupp.sub_apply, Complex.sub_re, Complex.sub_im, castPair_re,
      castPair_im, hpdef, hqdef, Finsupp.onFinset_apply, Finsupp.onFinset_apply, if_pos hi,
      if_pos hi]
    have h1 := abs_lt.mp (hpf i)
    have h2 := abs_lt.mp (hqf i)
    have h3 := sq_lt_sq' h1.1 h1.2
    have h4 := sq_lt_sq' h2.1 h2.2
    linarith
  have h2δ : 2 * (r / (2 * ((s.card : ℝ) + 1))) ^ 2 = r ^ 2 / (2 * ((s.card : ℝ) + 1) ^ 2) := by
    rw [div_pow, mul_pow, ← mul_div_assoc, div_eq_div_iff (by positivity) (by positivity)]
    ring
  have hsq : ‖f - castPair p q‖ ^ 2 < r ^ 2 := by
    rw [norm_sq_eq_sum_complex _ hsupp]
    rcases s.eq_empty_or_nonempty with he | hne
    · rw [he, Finset.sum_empty]
      positivity
    · have hk : (0 : ℝ) < 2 * (s.card : ℝ) ^ 2 + 3 * s.card + 2 := by positivity
      calc ∑ i ∈ s, ‖(f - castPair p q) i‖ ^ 2
          < ∑ _i ∈ s, 2 * (r / (2 * ((s.card : ℝ) + 1))) ^ 2 :=
            Finset.sum_lt_sum_of_nonempty hne hterm
        _ = (s.card : ℝ) * (r ^ 2 / (2 * ((s.card : ℝ) + 1) ^ 2)) := by
          rw [Finset.sum_const, nsmul_eq_mul, h2δ]
        _ < r ^ 2 := by
          rw [mul_div_assoc', div_lt_iff₀ (by positivity)]
          nlinarith [mul_pos (pow_pos hr 2) hk]
  rw [dist_eq_norm]
  exact lt_of_sq_lt (norm_nonneg _) hr.le hsq

/-- The explicit embedding of Gaussian-rational pairs into the complex Hilbert lift. -/
noncomputable def liftPair (p : Carrier × Carrier) : HilbertLiftSpace ℂ :=
  ((castPair p.1 p.2 : PreH ℂ) : Completion (PreH ℂ))

theorem liftPair_real (a : Carrier) : liftPair (a, 0) = lift ℂ a := by
  unfold liftPair lift
  rw [castPair_zero_right]

theorem inner_liftPair (a b c d : Carrier) :
    inner ℂ (liftPair (a, b)) (liftPair (c, d)) =
      ((qinner a c + qinner b d : ℚ) : ℂ) + Complex.I * ((qinner a d - qinner b c : ℚ) : ℂ) := by
  unfold liftPair
  rw [Completion.inner_coe]
  exact inner_castPair a b c d

theorem liftPair_sub (a b c d : Carrier) :
    liftPair (a, b) - liftPair (c, d) = liftPair (a - c, b - d) := by
  unfold liftPair
  rw [← Completion.coe_sub, castPair_sub]

theorem norm_liftPair_sq (a b : Carrier) :
    ‖liftPair (a, b)‖ ^ 2 = ((qinner a a + qinner b b : ℚ) : ℝ) := by
  unfold liftPair
  rw [Completion.norm_coe, norm_castPair_sq]

/-- Density of the Gaussian-rational carrier in the complex Hilbert lift. -/
theorem denseRange_liftPair : DenseRange liftPair :=
  Completion.denseRange_coe.comp denseRange_castPair (Completion.continuous_coe _)

/-- Strictness: the limit of the harmonic witness is not a Gaussian-rational pair. -/
theorem exists_not_mem_range_liftPair : ∃ h : HilbertLiftSpace ℂ, h ∉ Set.range liftPair := by
  obtain ⟨h, hh⟩ := exists_limit_of_isCauchyL2 (𝕜 := ℂ) harmonic harmonic_isCauchyL2
  refine ⟨h, ?_⟩
  rintro ⟨⟨p, q⟩, rfl⟩
  obtain ⟨M, hM⟩ := Finset.exists_nat_subset_range p.support
  rw [Metric.tendsto_atTop] at hh
  obtain ⟨N, hN⟩ := hh (harmonicTerm M) (by exact_mod_cast harmonicTerm_pos M)
  have h1 := hN (max N (M + 1)) (le_max_left _ _)
  have hpM : p M = 0 := by
    by_contra hne
    exact absurd (mem_range.mp (hM (Finsupp.mem_support_iff.mpr hne))) (lt_irrefl M)
  have hsq : dist (lift ℂ (harmonic (max N (M + 1)))) (liftPair (p, q)) ^ 2
      = ((sqdist (harmonic (max N (M + 1))) p + qinner (0 - q) (0 - q) : ℚ) : ℝ) := by
    rw [dist_eq_norm, ← liftPair_real, liftPair_sub, norm_liftPair_sq]
    rfl
  have hlow : harmonicTerm M ^ 2 ≤ sqdist (harmonic (max N (M + 1))) p := by
    have h3 := sq_sub_apply_le_sqdist (harmonic (max N (M + 1))) p M
    rwa [harmonic_apply, if_pos (by omega), hpM, sub_zero] at h3
  have hq0 : 0 ≤ qinner (0 - q) (0 - q) := qinner_self_nonneg _
  have h2 : (harmonicTerm M : ℝ) ^ 2 ≤
      dist (lift ℂ (harmonic (max N (M + 1)))) (liftPair (p, q)) ^ 2 := by
    rw [hsq]
    have : harmonicTerm M ^ 2 ≤ sqdist (harmonic (max N (M + 1))) p + qinner (0 - q) (0 - q) := by
      linarith
    exact_mod_cast this
  have h3 : dist (lift ℂ (harmonic (max N (M + 1)))) (liftPair (p, q)) ^ 2
      < (harmonicTerm M : ℝ) ^ 2 :=
    pow_lt_pow_left₀ h1 dist_nonneg two_ne_zero
  linarith

theorem liftPair_not_surjective : ¬ Function.Surjective liftPair := by
  intro hs
  obtain ⟨h, hh⟩ := exists_not_mem_range_liftPair
  exact hh (hs h)

/-- The controlled completion over `ℂ`, packaged: the Gaussian-rational pairs embed with the exact
inner-product identity, are dense, their Cauchy sequences are characterised by the rational ℓ²
condition on both components (through `cauchySeq_lift_iff` on each), and the lift is strictly
larger than the Gaussian-rational carrier. -/
theorem controlled_completion_complex :
    (∀ a b c d : Carrier, inner ℂ (liftPair (a, b)) (liftPair (c, d)) =
      ((qinner a c + qinner b d : ℚ) : ℂ) + Complex.I * ((qinner a d - qinner b c : ℚ) : ℂ)) ∧
    DenseRange liftPair ∧
    (∀ x : ℕ → Carrier, CauchySeq (fun n => lift ℂ (x n)) ↔ IsCauchyL2 x) ∧
    ¬ Function.Surjective liftPair :=
  ⟨inner_liftPair, denseRange_liftPair, cauchySeq_lift_iff, liftPair_not_surjective⟩

end HilbertLift

#print axioms HilbertLift.castPair_re
#print axioms HilbertLift.castPair_im
#print axioms HilbertLift.support_castPair_subset
#print axioms HilbertLift.castPair_sub
#print axioms HilbertLift.castPair_zero_right
#print axioms HilbertLift.inner_castPair
#print axioms HilbertLift.norm_castPair_sq
#print axioms HilbertLift.norm_sq_eq_sum_complex
#print axioms HilbertLift.denseRange_castPair
#print axioms HilbertLift.liftPair_real
#print axioms HilbertLift.inner_liftPair
#print axioms HilbertLift.liftPair_sub
#print axioms HilbertLift.norm_liftPair_sq
#print axioms HilbertLift.denseRange_liftPair
#print axioms HilbertLift.exists_not_mem_range_liftPair
#print axioms HilbertLift.liftPair_not_surjective
#print axioms HilbertLift.controlled_completion_complex
