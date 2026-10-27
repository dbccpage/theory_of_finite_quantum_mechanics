import Mathlib.Probability.ProductMeasure
import Mathlib.Topology.Compactness.Compact
import Mathlib.Topology.Instances.Discrete

/-! A projective probability limit for supplied finite-alphabet label laws.
AuthorityEffect: None. No LQG amplitudes, triangulation refinement or manifold is
selected. Positivity, normalization and compatibility are explicit hypotheses.
-/
namespace LqgProjectiveLimit
open MeasureTheory Filter Set Finset
open scoped ENNReal Topology

variable {A : Type*} [Fintype A]
  [TopologicalSpace A] [DiscreteTopology A]
  [MeasurableSpace A]

abbrev Config (A : Type*) := ℕ → A

/-- Every finite-coordinate cylinder is closed in the compact label product. -/
theorem cylinder_closed {s : Set (Config A)}
    (hs : s ∈ measurableCylinders (fun _ : ℕ => A)) : IsClosed s := by
  obtain ⟨I, S, _, rfl⟩ := (mem_measurableCylinders s).mp hs
  exact (Set.toFinite S).isClosed.preimage (continuous_pi fun i => continuous_apply i.val)

/-- Nested empty-intersection cylinders become empty at a finite stage. -/
theorem empty_stage (s : ℕ → Set (Config A))
    (hs : ∀ n, s n ∈ measurableCylinders (fun _ : ℕ => A))
    (hanti : Antitone s) (hempty : ⋂ n, s n = ∅) : ∃ n, s n = ∅ := by
  by_contra h
  have hn : ∀ n, (s n).Nonempty := by
    intro n
    exact Set.nonempty_iff_ne_empty.mpr (fun he => h ⟨n, he⟩)
  have hi := IsCompact.nonempty_iInter_of_sequence_nonempty_isCompact_isClosed s
    (fun n => hanti (Nat.le_succ n)) hn (cylinder_closed (hs 0)).isCompact
    (fun n => cylinder_closed (hs n))
  rw [hempty] at hi
  exact Set.not_nonempty_empty hi

variable (P : (I : Finset ℕ) → Measure (I → A))
  [∀ I, IsProbabilityMeasure (P I)]
  (hP : IsProjectiveMeasureFamily (α := fun _ : ℕ => A) P)
include hP

omit [∀ I, IsProbabilityMeasure (P I)] in
theorem content_tendsto_zero (s : ℕ → Set (Config A))
    (hs : ∀ n, s n ∈ measurableCylinders (fun _ : ℕ => A))
    (hanti : Antitone s) (hempty : ⋂ n, s n = ∅) :
    Tendsto (fun n => projectiveFamilyContent hP (s n)) atTop (𝓝 0) := by
  obtain ⟨n, hn⟩ := empty_stage s hs hanti hempty
  apply tendsto_const_nhds.congr'
  filter_upwards [eventually_ge_atTop n] with m hm
  have he : s m = ∅ := Set.eq_empty_of_subset_empty (hn ▸ hanti hm)
  simp [he]

theorem content_sigma_subadditive : (projectiveFamilyContent hP).IsSigmaSubadditive := by
  refine isSigmaSubadditive_of_addContent_iUnion_eq_tsum
    isSetRing_measurableCylinders (fun f hf hfUnion hf' => ?_)
  exact addContent_iUnion_eq_sum_of_tendsto_zero isSetRing_measurableCylinders
    (projectiveFamilyContent hP) (fun _ _ => projectiveFamilyContent_ne_top hP)
    (fun _ hs => content_tendsto_zero P hP _ hs) hf hfUnion hf'

noncomputable def limitMeasure : Measure (Config A) :=
  (projectiveFamilyContent hP).measure isSetSemiring_measurableCylinders
    generateFrom_measurableCylinders.ge (content_sigma_subadditive P hP)

theorem limit_marginals : IsProjectiveLimit (limitMeasure P hP) P := by
  intro I
  ext s hs
  rw [Measure.map_apply (Finset.measurable_restrict I) hs, limitMeasure, AddContent.measure_eq,
    ← cylinder, projectiveFamilyContent_cylinder hP hs]
  · exact generateFrom_measurableCylinders.symm
  · exact cylinder_mem_measurableCylinders _ _ hs

instance limit_probability : IsProbabilityMeasure (limitMeasure P hP) :=
  (limit_marginals P hP).isProbabilityMeasure

theorem limit_unique (μ : Measure (Config A)) (hμ : IsProjectiveLimit μ P) :
    μ = limitMeasure P hP := hμ.unique (limit_marginals P hP)

theorem exists_unique_limit : ∃! μ : Measure (Config A), IsProjectiveLimit μ P :=
  ⟨limitMeasure P hP, limit_marginals P hP, fun μ hμ => limit_unique P hP μ hμ⟩

/-- Probability-one finite constraints hold simultaneously for the countable family. -/
theorem countable_constraints (I : ℕ → Finset ℕ) (S : ∀ n, Set (I n → A))
    (hS : ∀ n, MeasurableSet (S n)) (hprob : ∀ n, P (I n) (S n) = 1) :
    ∀ᵐ ω ∂limitMeasure P hP, ∀ n, Finset.restrict (π := fun _ : ℕ => A) (I n) ω ∈ S n := by
  apply ae_all_iff.mpr
  intro n
  change cylinder (I n) (S n) ∈ ae (limitMeasure P hP)
  apply (mem_ae_iff_prob_eq_one (MeasurableSet.of_mem_measurableCylinders
    (cylinder_mem_measurableCylinders _ _ (hS n)))).mpr
  rw [(limit_marginals P hP).measure_cylinder (I n) (hS n), hprob n]

theorem constraints_have_configuration (I : ℕ → Finset ℕ) (S : ∀ n, Set (I n → A))
    (hS : ∀ n, MeasurableSet (S n)) (hprob : ∀ n, P (I n) (S n) = 1) :
    ∃ ω : Config A, ∀ n, Finset.restrict (π := fun _ : ℕ => A) (I n) ω ∈ S n :=
  (countable_constraints P hP I S hS hprob).exists

omit hP [Fintype A] [TopologicalSpace A] [DiscreteTopology A]
     [∀ I, IsProbabilityMeasure (P I)] in
/-- Compatibility is necessary; normalization alone cannot replace it. -/
theorem projective_of_limit (μ : Measure (Config A)) (hμ : IsProjectiveLimit μ P) :
    IsProjectiveMeasureFamily (α := fun _ : ℕ => A) P := by
  intro I J hJI
  rw [← hμ J, ← hμ I, Measure.map_map (Finset.measurable_restrict₂ hJI) (Finset.measurable_restrict I),
    Finset.restrict₂_comp_restrict]

omit hP in
theorem exists_limit_iff_projective :
    (∃ μ : Measure (Config A), IsProjectiveLimit μ P) ↔
      IsProjectiveMeasureFamily (α := fun _ : ℕ => A) P := by
  constructor
  · rintro ⟨μ, hμ⟩
    exact projective_of_limit P μ hμ
  · intro h
    exact ⟨limitMeasure P h, limit_marginals P h⟩

omit hP P in
/-- The three level-two spin labels are a concrete instance of the extension theorem. -/
theorem spin_labels_extension
    (laws : (I : Finset ℕ) → Measure (I → Fin 3))
    [∀ I, IsProbabilityMeasure (laws I)]
    (consistent : IsProjectiveMeasureFamily (α := fun _ : ℕ => Fin 3) laws) :
    ∃! μ : Measure (ℕ → Fin 3), IsProjectiveLimit μ laws :=
  exists_unique_limit laws consistent

omit hP P in
/-- Every predicate on a finite spin window is measurable; full-mass local laws pass to the limit. -/
theorem spin_constraints_ae
    (laws : (I : Finset ℕ) → Measure (I → Fin 3))
    [∀ I, IsProbabilityMeasure (laws I)]
    (consistent : IsProjectiveMeasureFamily (α := fun _ : ℕ => Fin 3) laws)
    (windows : ℕ → Finset ℕ) (allowed : ∀ n, Set (windows n → Fin 3))
    (full_mass : ∀ n, laws (windows n) (allowed n) = 1) :
    ∀ᵐ ω ∂limitMeasure laws consistent, ∀ n,
      Finset.restrict (π := fun _ : ℕ => Fin 3) (windows n) ω ∈ allowed n :=
  countable_constraints laws consistent windows allowed
    (fun n => (Set.toFinite (allowed n)).countable.measurableSet) full_mass

#print axioms spin_constraints_ae
#print axioms spin_labels_extension
#print axioms countable_constraints
#print axioms constraints_have_configuration
#print axioms projective_of_limit
#print axioms exists_limit_iff_projective

#print axioms empty_stage
#print axioms content_sigma_subadditive
#print axioms limit_marginals
#print axioms limit_unique
end LqgProjectiveLimit
