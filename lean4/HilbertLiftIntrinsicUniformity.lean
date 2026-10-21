import HilbertLiftCompletion
import Mathlib.Topology.UniformSpace.UniformEmbedding

/-!
# The intrinsic uniformity of the exact carrier and its completion

Origin: dag/results/FQ-GAP-CONTINUUM-HILBERT-LIFT/runs/20261021T003000Z_lift_steps
Claim: the exact carrier `ℕ →₀ ℚ` carries the uniformity whose entourages are the rational
squared-distance balls `{(f, g) | sqdist f g < ε}`, `ε : ℚ`, `ε > 0` (the uniformity filter is
proved equal to the infimum of these principal filters); under it a sequence is Cauchy exactly
when it is `IsCauchyL2`; and the Hausdorff completion of the exact carrier under this uniformity
is uniformly isomorphic to the real Hilbert lift, the isomorphism restricting to `lift ℝ` on
exact vectors.
AuthorityEffect: None
Scope Fence: the uniform structure is declared on the abbreviation `ℕ →₀ ℚ` as the pullback of
the real pre-Hilbert metric and then characterised intrinsically (`uniformity_eq_iInf_sqdist`);
since a uniform structure is determined by its uniformity filter, the characterisation is the
intrinsic definition.  The scalar field `ℝ` still enters the target of the isomorphism; the
domain carries no real number.
Level: L5
-/

namespace HilbertLift

open Filter Topology UniformSpace Uniformity

/-- The uniformity of the exact carrier: the pullback of the real pre-Hilbert metric along the
scalar lift.  `uniformity_eq_iInf_sqdist` identifies it with the intrinsic rational-ball
uniformity. -/
noncomputable instance instUniformSpaceCarrier : UniformSpace Carrier :=
  UniformSpace.comap (castSeq ℝ) inferInstance

theorem isUniformInducing_castSeq_real : IsUniformInducing (castSeq ℝ) :=
  isUniformInducing_iff_uniformSpace.mpr rfl

theorem dist_castSeq_sq (f g : Carrier) : dist (castSeq ℝ f) (castSeq ℝ g) ^ 2 = (sqdist f g : ℝ) := by
  rw [dist_eq_norm, ← castSeq_sub, norm_castSeq_sq]
  rfl

/-- The intrinsic description: rational squared-distance balls form a basis of the uniformity. -/
theorem uniformity_hasBasis_sqdist :
    (𝓤 Carrier).HasBasis (fun ε : ℚ => 0 < ε)
      (fun ε => {p : Carrier × Carrier | sqdist p.1 p.2 < ε}) := by
  have h := (Metric.uniformity_basis_dist (α := PreH ℝ)).comap (Prod.map (castSeq ℝ) (castSeq ℝ))
  rw [← uniformity_comap (castSeq ℝ)] at h
  refine h.to_hasBasis ?_ ?_
  · intro ε hε
    obtain ⟨δ, hδ0, hδ⟩ := exists_rat_btwn (pow_pos hε 2)
    refine ⟨δ, by exact_mod_cast hδ0, ?_⟩
    intro p hp
    have h1 : (sqdist p.1 p.2 : ℝ) < δ := by exact_mod_cast hp
    have h2 : dist (castSeq ℝ p.1) (castSeq ℝ p.2) ^ 2 < ε ^ 2 := by
      rw [dist_castSeq_sq]
      linarith
    exact lt_of_sq_lt dist_nonneg hε.le h2
  · intro ε hε
    have hε' : (0 : ℝ) < ε := by exact_mod_cast hε
    refine ⟨Real.sqrt ε, Real.sqrt_pos.mpr hε', ?_⟩
    intro p hp
    have h1 : dist (castSeq ℝ p.1) (castSeq ℝ p.2) < Real.sqrt ε := hp
    have h2 := (Real.lt_sqrt dist_nonneg).mp h1
    rw [dist_castSeq_sq] at h2
    exact_mod_cast h2

/-- The uniformity filter is the infimum of the rational-ball principal filters: no real number
occurs in this description. -/
theorem uniformity_eq_iInf_sqdist :
    𝓤 Carrier = ⨅ ε : ℚ, ⨅ (_ : 0 < ε), 𝓟 {p : Carrier × Carrier | sqdist p.1 p.2 < ε} :=
  uniformity_hasBasis_sqdist.eq_biInf

/-- Cauchy sequences of the intrinsic uniformity are exactly the rational ℓ²-Cauchy sequences. -/
theorem cauchySeq_iff_isCauchyL2 (x : ℕ → Carrier) : CauchySeq x ↔ IsCauchyL2 x := by
  rw [uniformity_hasBasis_sqdist.cauchySeq_iff]
  constructor
  · intro h ε hε
    obtain ⟨N, hN⟩ := h ε hε
    exact ⟨N, fun m hm n hn => hN m hm n hn⟩
  · intro h ε hε
    obtain ⟨N, hN⟩ := h ε hε
    exact ⟨N, fun m hm n hn => hN m hm n hn⟩

theorem uniformContinuous_lift_real : UniformContinuous (lift ℝ) :=
  (Completion.isUniformInducing_coe _).uniformContinuous.comp
    isUniformInducing_castSeq_real.uniformContinuous

theorem isUniformInducing_lift_real : IsUniformInducing (lift ℝ) :=
  (Completion.isUniformInducing_coe _).comp isUniformInducing_castSeq_real

/-- Every rational ℓ²-Cauchy sequence converges in the completion of the exact carrier. -/
theorem exists_limit_in_completion (x : ℕ → Carrier) (hx : IsCauchyL2 x) :
    ∃ c : Completion Carrier, Tendsto (fun n => (x n : Completion Carrier)) atTop (𝓝 c) :=
  cauchySeq_tendsto_of_complete
    (((cauchySeq_iff_isCauchyL2 x).mpr hx).map (Completion.isUniformInducing_coe _).uniformContinuous)

/-- The canonical map from the completion of the exact carrier to the real Hilbert lift. -/
noncomputable def completionToLift : Completion Carrier → HilbertLiftSpace ℝ :=
  Completion.extension (lift ℝ)

theorem completionToLift_coe (f : Carrier) :
    completionToLift (f : Completion Carrier) = lift ℝ f :=
  Completion.extension_coe uniformContinuous_lift_real f

theorem isUniformInducing_completionToLift : IsUniformInducing completionToLift :=
  Completion.isUniformInducing_extension isUniformInducing_lift_real

theorem completionToLift_injective : Function.Injective completionToLift :=
  isUniformInducing_completionToLift.injective

theorem range_completionToLift : Set.range completionToLift = Set.univ := by
  have hclosed : IsClosed (Set.range completionToLift) :=
    isUniformInducing_completionToLift.isComplete_range.isClosed
  have hdense : Dense (Set.range completionToLift) :=
    denseRange_lift_real.mono (by
      rintro _ ⟨f, rfl⟩
      exact ⟨f, completionToLift_coe f⟩)
  rw [← hclosed.closure_eq, hdense.closure_eq]

theorem completionToLift_surjective : Function.Surjective completionToLift := by
  intro h
  have hmem : h ∈ Set.range completionToLift := by
    rw [range_completionToLift]
    trivial
  obtain ⟨c, hc⟩ := hmem
  exact ⟨c, hc⟩

/-- The completion of the exact carrier under its intrinsic rational uniformity is uniformly
isomorphic to the real Hilbert lift. -/
noncomputable def completionEquivLift : Completion Carrier ≃ᵤ HilbertLiftSpace ℝ :=
  (Equiv.ofBijective completionToLift
    ⟨completionToLift_injective, completionToLift_surjective⟩).toUniformEquivOfIsUniformInducing
    isUniformInducing_completionToLift

theorem completionEquivLift_coe (f : Carrier) :
    completionEquivLift (f : Completion Carrier) = lift ℝ f :=
  completionToLift_coe f

theorem completionEquivLift_symm_lift (f : Carrier) :
    completionEquivLift.symm (lift ℝ f) = (f : Completion Carrier) := by
  rw [← completionEquivLift_coe]
  exact completionEquivLift.symm_apply_apply _

/-- Summary: the intrinsic uniformity is the rational-ball uniformity, its Cauchy sequences are
the rational ℓ²-Cauchy sequences, and its completion is the real Hilbert lift. -/
theorem intrinsic_completion :
    (𝓤 Carrier = ⨅ ε : ℚ, ⨅ (_ : 0 < ε), 𝓟 {p : Carrier × Carrier | sqdist p.1 p.2 < ε}) ∧
    (∀ x : ℕ → Carrier, CauchySeq x ↔ IsCauchyL2 x) ∧
    (∀ f : Carrier, completionEquivLift (f : Completion Carrier) = lift ℝ f) :=
  ⟨uniformity_eq_iInf_sqdist, cauchySeq_iff_isCauchyL2, completionEquivLift_coe⟩

end HilbertLift

#print axioms HilbertLift.isUniformInducing_castSeq_real
#print axioms HilbertLift.dist_castSeq_sq
#print axioms HilbertLift.uniformity_hasBasis_sqdist
#print axioms HilbertLift.uniformity_eq_iInf_sqdist
#print axioms HilbertLift.cauchySeq_iff_isCauchyL2
#print axioms HilbertLift.uniformContinuous_lift_real
#print axioms HilbertLift.isUniformInducing_lift_real
#print axioms HilbertLift.exists_limit_in_completion
#print axioms HilbertLift.completionToLift_coe
#print axioms HilbertLift.isUniformInducing_completionToLift
#print axioms HilbertLift.completionToLift_injective
#print axioms HilbertLift.range_completionToLift
#print axioms HilbertLift.completionToLift_surjective
#print axioms HilbertLift.completionEquivLift_coe
#print axioms HilbertLift.completionEquivLift_symm_lift
#print axioms HilbertLift.intrinsic_completion
