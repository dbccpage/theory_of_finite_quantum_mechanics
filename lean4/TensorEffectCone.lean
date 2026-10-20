import TensorEffectOrder

/-! The conic hull of available effects is the full PSD cone. Local binary
effects and calibrated reversible pullbacks suffice; effect saturation and
finite-test saturation are deliberately absent from this theorem. -/
open Matrix Module
open scoped BigOperators Kronecker ComplexOrder MatrixOrder
noncomputable section
namespace TensorEffectCone
open TensorTomography TensorComposition TensorConeReconstruction
open TensorEffectOrder TensorOperationalCone TensorReachability
variable {d : Type*} [Fintype d] [DecidableEq d]

def effectCone (available : Set (Herm d)) : PointedCone ℝ (Matrix d d ℂ) :=
  PointedCone.hull ℝ (Subtype.val '' available)

def PullbackClosed (available : Set (Herm d)) (U : Matrix d d ℂ) : Prop :=
  ∀ E ∈ available, ∃ F ∈ available, F.val = conjugate U E.val

theorem cone_positive (available : Set (Herm d))
    (hvalid : ∀ E ∈ available, Positive E) {A : Matrix d d ℂ}
    (hA : A ∈ effectCone available) : A.PosSemidef := by
  induction hA using Submodule.span_induction with
  | mem E hE => obtain ⟨F, hF, rfl⟩ := hE; exact hvalid F hF
  | zero => exact Matrix.PosSemidef.zero
  | add A B hA hB ihA ihB => exact ihA.add ihB
  | smul r A hA ih => exact ih.smul r.property

theorem cone_pullback (available : Set (Herm d)) (U : Matrix d d ℂ)
    (hU : PullbackClosed available U) {A : Matrix d d ℂ}
    (hA : A ∈ effectCone available) : conjugate U A ∈ effectCone available := by
  induction hA using Submodule.span_induction with
  | mem E hE =>
    obtain ⟨F, hF, rfl⟩ := hE
    obtain ⟨G, hG, he⟩ := hU F hF
    rw [← he]
    exact PointedCone.subset_hull ⟨G, hG, rfl⟩
  | zero => simpa [conjugate] using (effectCone available).zero_mem
  | add A B hA hB ihA ihB =>
    simpa [conjugate, Matrix.mul_add, Matrix.add_mul] using
      (effectCone available).add_mem ihA ihB
  | smul r A hA ih =>
    change conjugate U ((r : ℝ) • A) ∈ effectCone available
    simpa [conjugate] using PointedCone.smul_mem (effectCone available) r.property ih

/-- Schmidt reachability transports local effect rays onto every rank-one ray.
The pullback for `C` is provided operationally by the inverse controlled shift. -/
theorem effect_cone_eq_positive {n m : ℕ} [NeZero m] (hnm : n ≤ m)
    (available : Set (Herm (Fin n × Fin m)))
    (hvalid : ∀ E ∈ available, Positive E)
    (hproduct : ∀ (E : Herm (Fin n)) (F : Herm (Fin m)),
      Binary E → Binary F → product E F ∈ available)
    (hlocal : ∀ (U : Matrix.unitaryGroup (Fin n) ℂ) (W : Matrix.unitaryGroup (Fin m) ℂ),
      PullbackClosed available (U.val ⊗ₖ W.val))
    (hshift : PullbackClosed available (controlledShift hnm).val) :
    (effectCone available : Set (Matrix (Fin n × Fin m) (Fin n × Fin m) ℂ)) =
      {A | A.PosSemidef} := by
  have hseed (a : Fin n → ℂ) (b : Fin m → ℂ) :
      rankOne (productVector a b) ∈ effectCone available := by
    obtain ⟨r, E, hr, hE, he⟩ := positive_ray_binary (hermRankOne a)
      (Matrix.posSemidef_vecMulVec_self_star a)
    obtain ⟨s, F, hs, hF, hf⟩ := positive_ray_binary (hermRankOne b)
      (Matrix.posSemidef_vecMulVec_self_star b)
    have hp : (product E F).val ∈ effectCone available :=
      PointedCone.subset_hull ⟨product E F, hproduct E F hE hF, rfl⟩
    have hid : rankOne (productVector a b) = (r * s) • (product E F).val := by
      change (hermRankOne (productVector a b)).val = _
      rw [← product_rankOne, he, hf, product_smul_left, product_smul_right]
      simp [smul_smul]
    rw [hid]
    exact PointedCone.smul_mem (effectCone available) (mul_nonneg hr hs) hp
  have hrank (v : Fin n × Fin m → ℂ) : rankOne v ∈ effectCone available := by
    obtain ⟨U, W, s, hv⟩ := schmidt_reachability hnm v
    rw [← hv, ← conjugate_rankOne, conjugate_mul]
    exact cone_pullback available _ (hlocal U W)
      (cone_pullback available _ hshift (hseed s (Pi.single 0 1)))
  ext A
  constructor
  · exact cone_positive available hvalid
  · intro hA
    exact positive_mem_of_rankOne
      (effectCone available : Set (Matrix (Fin n × Fin m) (Fin n × Fin m) ℂ))
      (effectCone available).zero_mem
      (fun A hA B hB => (effectCone available).add_mem hA hB) hrank hA

#print axioms effect_cone_eq_positive
end TensorEffectCone
