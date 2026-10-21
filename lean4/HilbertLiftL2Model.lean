import HilbertLiftCompletion
import Mathlib.Analysis.InnerProductSpace.l2Space

/-!
# The sequence model: the Hilbert lift is `ℓ²(ℕ, 𝕜)`

Origin: dag/results/FQ-GAP-CONTINUUM-HILBERT-LIFT/runs/20261021T003000Z_lift_steps
Claim: the coordinate map `f ↦ (f i)_i` is a linear isometry from the pre-Hilbert carrier
`ℕ →₀ 𝕜` into `lp (fun _ : ℕ => 𝕜) 2` with dense range, and it extends to a linear isometric
equivalence `HilbertLiftSpace 𝕜 ≃ₗᵢ[𝕜] ℓ²(ℕ, 𝕜)` under which an exact vector `lift 𝕜 f` is its
own coordinate sequence.
AuthorityEffect: None
Scope Fence: `ℓ²` is Mathlib's `lp` space with its own completeness; the identification uses
the universal property of the Hausdorff completion and the density of finitely supported
sequences in `ℓ²` (`lp.hasSum_single`).  No basis is chosen beyond the coordinate functions.
Level: L5
-/

namespace HilbertLift

open Filter Topology UniformSpace

section Model

variable (𝕜 : Type*) [RCLike 𝕜]

/-- The sequence model `ℓ²(ℕ, 𝕜)`. -/
abbrev L2 : Type _ := lp (fun _ : ℕ => 𝕜) 2

theorem memℓp_coe (f : PreH 𝕜) : Memℓp (fun i => f i) 2 := by
  refine memℓp_gen (summable_of_ne_finset_zero (s := f.support) fun i hi => ?_)
  simp [Finsupp.notMem_support_iff.mp hi]

/-- The sequence model of a finitely supported vector. -/
noncomputable def toL2 (f : PreH 𝕜) : L2 𝕜 := ⟨fun i => f i, memℓp_coe 𝕜 f⟩

@[simp] theorem toL2_apply (f : PreH 𝕜) (i : ℕ) : (toL2 𝕜 f : ℕ → 𝕜) i = f i := rfl

theorem toL2_add (f g : PreH 𝕜) : toL2 𝕜 (f + g) = toL2 𝕜 f + toL2 𝕜 g :=
  lp.ext (by
    ext i
    simp)

theorem toL2_smul (c : 𝕜) (f : PreH 𝕜) : toL2 𝕜 (c • f) = c • toL2 𝕜 f :=
  lp.ext (by
    ext i
    simp [lp.coeFn_smul])

theorem inner_toL2 (f g : PreH 𝕜) : inner 𝕜 (toL2 𝕜 f) (toL2 𝕜 g) = inner 𝕜 f g := by
  rw [lp.inner_eq_tsum,
    tsum_eq_sum (s := f.support) (fun i hi => by simp [Finsupp.notMem_support_iff.mp hi]),
    inner_def]
  unfold preInner Finsupp.sum
  exact Finset.sum_congr rfl fun i _ => by rw [toL2_apply, toL2_apply, RCLike.inner_apply, mul_comm]

theorem norm_toL2 (f : PreH 𝕜) : ‖toL2 𝕜 f‖ = ‖f‖ := by
  have h : ‖toL2 𝕜 f‖ ^ 2 = ‖f‖ ^ 2 := by
    rw [norm_sq_eq_re_inner (𝕜 := 𝕜), inner_toL2, ← norm_sq_eq_re_inner (𝕜 := 𝕜)]
  exact (pow_left_inj₀ (norm_nonneg _) (norm_nonneg _) two_ne_zero).mp h

/-- The sequence model as a linear isometry on the pre-Hilbert carrier. -/
noncomputable def toL2ₗᵢ : PreH 𝕜 →ₗᵢ[𝕜] L2 𝕜 :=
  { toFun := toL2 𝕜
    map_add' := toL2_add 𝕜
    map_smul' := toL2_smul 𝕜
    norm_map' := norm_toL2 𝕜 }

theorem toL2ₗᵢ_apply (f : PreH 𝕜) : toL2ₗᵢ 𝕜 f = toL2 𝕜 f := rfl

/-- Finitely supported sequences are dense in `ℓ²`. -/
theorem denseRange_toL2 : DenseRange (toL2 𝕜) := by
  classical
  intro g
  have h := (lp.hasSum_single (E := fun _ : ℕ => 𝕜) (p := 2) ENNReal.ofNat_ne_top g).tendsto_sum_nat
  refine mem_closure_of_tendsto h (Eventually.of_forall fun n => ?_)
  refine ⟨∑ i ∈ Finset.range n, Finsupp.single i ((g : ℕ → 𝕜) i), ?_⟩
  apply lp.ext
  ext j
  rw [toL2_apply, lp.coeFn_sum, Finset.sum_apply, Finsupp.finsetSum_apply]
  simp [Finsupp.single_apply, lp.single_apply, Pi.single_apply]

theorem uniformContinuous_toL2 : UniformContinuous (toL2 𝕜) :=
  (toL2ₗᵢ 𝕜).isometry.uniformContinuous

theorem isUniformInducing_toL2 : IsUniformInducing (toL2 𝕜) :=
  (toL2ₗᵢ 𝕜).isometry.isUniformInducing

/-- The extension of the sequence model to the Hilbert lift. -/
noncomputable def liftToL2 : HilbertLiftSpace 𝕜 → L2 𝕜 := Completion.extension (toL2 𝕜)

theorem liftToL2_coe (f : PreH 𝕜) : liftToL2 𝕜 (f : Completion (PreH 𝕜)) = toL2 𝕜 f :=
  Completion.extension_coe (uniformContinuous_toL2 𝕜) f

theorem liftToL2_lift (f : Carrier) : liftToL2 𝕜 (lift 𝕜 f) = toL2 𝕜 (castSeq 𝕜 f) :=
  liftToL2_coe 𝕜 _

/-- An exact vector is its own coordinate sequence in the model. -/
theorem liftToL2_lift_apply (f : Carrier) (i : ℕ) :
    (liftToL2 𝕜 (lift 𝕜 f) : ℕ → 𝕜) i = (f i : 𝕜) := by
  rw [liftToL2_lift, toL2_apply, castSeq_apply]

theorem continuous_liftToL2 : Continuous (liftToL2 𝕜) := Completion.continuous_extension

theorem norm_liftToL2 (x : HilbertLiftSpace 𝕜) : ‖liftToL2 𝕜 x‖ = ‖x‖ := by
  refine Completion.induction_on x (isClosed_eq (continuous_liftToL2 𝕜).norm continuous_norm)
    fun f => ?_
  rw [liftToL2_coe, norm_toL2, Completion.norm_coe]

theorem liftToL2_add (x y : HilbertLiftSpace 𝕜) :
    liftToL2 𝕜 (x + y) = liftToL2 𝕜 x + liftToL2 𝕜 y := by
  refine Completion.induction_on₂ x y (isClosed_eq ((continuous_liftToL2 𝕜).comp continuous_add)
    (((continuous_liftToL2 𝕜).comp continuous_fst).add
      ((continuous_liftToL2 𝕜).comp continuous_snd))) fun f g => ?_
  rw [← Completion.coe_add, liftToL2_coe, liftToL2_coe, liftToL2_coe, toL2_add]

theorem liftToL2_smul (c : 𝕜) (x : HilbertLiftSpace 𝕜) :
    liftToL2 𝕜 (c • x) = c • liftToL2 𝕜 x := by
  refine Completion.induction_on x
    (isClosed_eq ((continuous_liftToL2 𝕜).comp (continuous_const_smul c))
      ((continuous_liftToL2 𝕜).const_smul c)) fun f => ?_
  rw [← Completion.coe_smul, liftToL2_coe, liftToL2_coe, toL2_smul]

theorem range_liftToL2 : Set.range (liftToL2 𝕜) = Set.univ := by
  have hclosed : IsClosed (Set.range (liftToL2 𝕜)) :=
    (Completion.isUniformInducing_extension (isUniformInducing_toL2 𝕜)).isComplete_range.isClosed
  have hdense : Dense (Set.range (liftToL2 𝕜)) :=
    (denseRange_toL2 𝕜).mono (by
      rintro _ ⟨f, rfl⟩
      exact ⟨f, liftToL2_coe 𝕜 f⟩)
  rw [← hclosed.closure_eq, hdense.closure_eq]

theorem liftToL2_surjective : Function.Surjective (liftToL2 𝕜) := by
  intro g
  have hmem : g ∈ Set.range (liftToL2 𝕜) := by
    rw [range_liftToL2]
    trivial
  obtain ⟨x, hx⟩ := hmem
  exact ⟨x, hx⟩

/-- The Hilbert lift is linearly isometrically isomorphic to `ℓ²(ℕ, 𝕜)`. -/
noncomputable def liftEquivL2 : HilbertLiftSpace 𝕜 ≃ₗᵢ[𝕜] L2 𝕜 :=
  LinearIsometryEquiv.ofSurjective
    { toFun := liftToL2 𝕜
      map_add' := liftToL2_add 𝕜
      map_smul' := liftToL2_smul 𝕜
      norm_map' := norm_liftToL2 𝕜 }
    (liftToL2_surjective 𝕜)

theorem liftEquivL2_apply (x : HilbertLiftSpace 𝕜) : liftEquivL2 𝕜 x = liftToL2 𝕜 x := rfl

theorem liftEquivL2_lift_apply (f : Carrier) (i : ℕ) :
    (liftEquivL2 𝕜 (lift 𝕜 f) : ℕ → 𝕜) i = (f i : 𝕜) :=
  liftToL2_lift_apply 𝕜 f i

/-- Summary: the lift is `ℓ²(ℕ, 𝕜)`, with exact vectors as their coordinate sequences. -/
theorem l2_model_summary :
    (∀ x : HilbertLiftSpace 𝕜, ‖liftEquivL2 𝕜 x‖ = ‖x‖) ∧
    Function.Surjective (liftEquivL2 𝕜) ∧
    (∀ (f : Carrier) (i : ℕ), (liftEquivL2 𝕜 (lift 𝕜 f) : ℕ → 𝕜) i = (f i : 𝕜)) :=
  ⟨(liftEquivL2 𝕜).norm_map, (liftEquivL2 𝕜).surjective, liftEquivL2_lift_apply 𝕜⟩

end Model

end HilbertLift

#print axioms HilbertLift.memℓp_coe
#print axioms HilbertLift.toL2_add
#print axioms HilbertLift.toL2_smul
#print axioms HilbertLift.inner_toL2
#print axioms HilbertLift.norm_toL2
#print axioms HilbertLift.denseRange_toL2
#print axioms HilbertLift.liftToL2_coe
#print axioms HilbertLift.liftToL2_lift_apply
#print axioms HilbertLift.norm_liftToL2
#print axioms HilbertLift.liftToL2_add
#print axioms HilbertLift.liftToL2_smul
#print axioms HilbertLift.range_liftToL2
#print axioms HilbertLift.liftToL2_surjective
#print axioms HilbertLift.liftEquivL2_lift_apply
#print axioms HilbertLift.l2_model_summary
