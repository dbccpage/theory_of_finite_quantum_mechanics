import TensorPartialTranspose

/-! Full separable, block-positive and partially transposed quantum cones.
All local quantum spaces and matrix-coordinate conventions are supplied.
No calibrated entangling interaction is assumed to preserve SEP or BP. -/
open Matrix Module
open scoped BigOperators Kronecker ComplexOrder MatrixOrder Matrix.Norms.L2Operator
noncomputable section
namespace TensorCountermodelCones
open TensorTomography TensorComposition TensorEffectOrder TensorPartialTranspose
variable {n m : Type*} [Fintype n] [Fintype m] [DecidableEq n] [DecidableEq m]

def sep : PointedCone ℝ (Herm (n × m)) := PointedCone.hull ℝ
  {H | ∃ (A : Herm n) (B : Herm m), Positive A ∧ Positive B ∧ H = product A B}

def BlockPositive (H : Herm (n × m)) : Prop :=
  ∀ (A : Herm n) (B : Herm m), Positive A → Positive B → 0 ≤ pairing (product A B) H

def bp : PointedCone ℝ (Herm (n × m)) where
  carrier := {H | BlockPositive H}
  zero_mem' := by intro A B hA hB; simp
  add_mem' := by
    intro X Y hX hY A B hA hB
    simpa only [map_add] using add_nonneg (hX A B hA hB) (hY A B hA hB)
  smul_mem' := by
    intro r X hX A B hA hB
    change 0 ≤ pairing (product A B) ((r : ℝ) • X)
    simpa only [map_smul, smul_eq_mul] using mul_nonneg r.property (hX A B hA hB)

def twisted : PointedCone ℝ (Herm (n × m)) where
  carrier := {H | Positive (gamma H)}
  zero_mem' := by change Positive (gamma 0); simpa [Positive] using Matrix.PosSemidef.zero
  add_mem' := by
    intro X Y hX hY
    change Positive (gamma (X + Y))
    rw [map_add]
    exact hX.add hY
  smul_mem' := by
    intro r X hX
    change Positive (gamma ((r : ℝ) • X))
    rw [map_smul]
    exact hX.smul r.property

theorem product_mem_sep {A : Herm n} {B : Herm m} (hA : Positive A) (hB : Positive B) :
    product A B ∈ sep := PointedCone.subset_hull ⟨A, B, hA, hB, rfl⟩

theorem sep_positive {H : Herm (n × m)} (hH : H ∈ sep) : Positive H := by
  induction hH using Submodule.span_induction with
  | mem X hX => obtain ⟨A, B, hA, hB, rfl⟩ := hX; exact hA.kronecker hB
  | zero => exact Matrix.PosSemidef.zero
  | add X Y hX hY ihX ihY => exact ihX.add ihY
  | smul r X hX ih => exact ih.smul r.property

theorem positive_blockPositive {H : Herm (n × m)} (hH : Positive H) : BlockPositive H :=
  fun A B hA hB => pairing_nonneg (hA.kronecker hB) hH

/-- BP is the trace dual of the entire conic hull SEP, not a finite test sample. -/
theorem blockPositive_iff_dual_sep (H : Herm (n × m)) :
    BlockPositive H ↔ ∀ E ∈ sep, 0 ≤ pairing E H := by
  constructor
  · intro h E hE
    induction hE using Submodule.span_induction with
    | mem X hX => obtain ⟨A, B, hA, hB, rfl⟩ := hX; exact h A B hA hB
    | zero => simp
    | add X Y hX hY ihX ihY =>
      simpa only [map_add, LinearMap.add_apply] using add_nonneg ihX ihY
    | smul r X hX ih =>
      change 0 ≤ pairing ((r : ℝ) • X) H
      simpa only [map_smul, LinearMap.smul_apply, smul_eq_mul] using mul_nonneg r.property ih
  · intro h A B hA hB
    exact h _ (product_mem_sep hA hB)

theorem gamma_sep {H : Herm (n × m)} (hH : H ∈ sep) : gamma H ∈ sep := by
  induction hH using Submodule.span_induction with
  | mem X hX =>
    obtain ⟨A, B, hA, hB, rfl⟩ := hX
    rw [gamma_product]
    exact product_mem_sep hA.transpose hB
  | zero => simpa only [map_zero] using sep.zero_mem
  | add X Y hX hY ihX ihY => simpa only [map_add] using sep.add_mem ihX ihY
  | smul r X hX ih =>
    change gamma ((r : ℝ) • X) ∈ sep
    simpa only [map_smul] using PointedCone.smul_mem sep r.property ih

theorem sep_ppt {H : Herm (n × m)} (hH : H ∈ sep) : Positive (gamma H) :=
  sep_positive (gamma_sep hH)

theorem twisted_product {A : Herm n} {B : Herm m} (hA : Positive A) (hB : Positive B) :
    product A B ∈ twisted := hA.transpose.kronecker hB

theorem twisted_blockPositive {H : Herm (n × m)} (hH : H ∈ twisted) : BlockPositive H := by
  intro A B hA hB
  rw [← pairing_gamma_gamma, gamma_product]
  exact pairing_nonneg (hA.transpose.kronecker hB) hH

/-- Partial transpose gives an explicit cone isomorphism with PSD. -/
theorem twisted_eq_image : (twisted (n := n) (m := m) : Set (Herm (n × m))) =
    gamma '' {A | Positive A} := by
  ext H
  constructor
  · intro h; exact ⟨gamma H, h, gamma_gamma H⟩
  · rintro ⟨A, hA, rfl⟩; change Positive (gamma (gamma A)); simpa using hA

theorem twisted_self_dual (H : Herm (n × m)) :
    H ∈ twisted ↔ ∀ A ∈ twisted, 0 ≤ pairing H A := by
  constructor
  · intro hH A hA
    rw [← pairing_gamma_gamma]
    exact pairing_nonneg hH hA
  · intro h
    apply (positive_iff_pairing (gamma H)).mpr
    intro A hA
    rw [pairing_gamma]
    exact h (gamma A) (by change Positive (gamma (gamma A)); simpa using hA)

theorem sep_local (U : Matrix n n ℂ) (W : Matrix m m ℂ)
    {H : Herm (n × m)} (hH : H ∈ sep) : conjMap (U ⊗ₖ W) H ∈ sep := by
  induction hH using Submodule.span_induction with
  | mem X hX =>
    obtain ⟨A, B, hA, hB, rfl⟩ := hX
    rw [conjMap_product]
    exact product_mem_sep (conjMap_positive U hA) (conjMap_positive W hB)
  | zero => simpa only [map_zero] using sep.zero_mem
  | add X Y hX hY ihX ihY => simpa only [map_add] using sep.add_mem ihX ihY
  | smul r X hX ih =>
    change conjMap (U ⊗ₖ W) ((r : ℝ) • X) ∈ sep
    simpa only [map_smul] using PointedCone.smul_mem sep r.property ih

theorem pairing_conjMap {d : Type*} [Fintype d] (U : Matrix d d ℂ) (E A : Herm d) :
    pairing E (conjMap U A) = pairing (conjMap Uᴴ E) A := by
  simp only [pairing_apply, conjMap_val, conjTranspose_conjTranspose]
  congr 1
  calc
    (E.val * (U * A.val * Uᴴ)).trace = ((E.val * U * A.val) * Uᴴ).trace := by
      simp only [Matrix.mul_assoc]
    _ = (Uᴴ * (E.val * U * A.val)).trace := Matrix.trace_mul_comm _ _
    _ = (Uᴴ * E.val * U * A.val).trace := by simp only [Matrix.mul_assoc]

theorem bp_local (U : Matrix n n ℂ) (W : Matrix m m ℂ)
    {H : Herm (n × m)} (hH : BlockPositive H) : BlockPositive (conjMap (U ⊗ₖ W) H) := by
  intro A B hA hB
  rw [pairing_conjMap, conjTranspose_kronecker, conjMap_product]
  exact hH _ _ (conjMap_positive Uᴴ hA) (conjMap_positive Wᴴ hB)

theorem twisted_local (U : Matrix n n ℂ) (W : Matrix m m ℂ)
    {H : Herm (n × m)} (hH : H ∈ twisted) : conjMap (U ⊗ₖ W) H ∈ twisted := by
  change Positive (gamma (conjMap (U ⊗ₖ W) H))
  rw [gamma_conjMap_product]
  exact conjMap_positive _ hH

def twist (U : Matrix (n × m) (n × m) ℂ) : Herm (n × m) →ₗ[ℝ] Herm (n × m) :=
  gamma.toLinearMap.comp ((conjMap U).comp gamma.toLinearMap)

theorem twist_preserves (U : Matrix (n × m) (n × m) ℂ)
    {H : Herm (n × m)} (hH : H ∈ twisted) : twist U H ∈ twisted := by
  change Positive (gamma (gamma (conjMap U (gamma H))))
  rw [gamma_gamma]
  exact conjMap_positive U hH

theorem twist_reversible (U : Matrix.unitaryGroup (n × m) ℂ) (H : Herm (n × m)) :
    twist U.valᴴ (twist U.val H) = H := by
  change gamma (conjMap U.valᴴ (gamma (gamma (conjMap U.val (gamma H))))) = H
  rw [gamma_gamma, conjMap_inverse, gamma_gamma]

theorem conjMap_trace {d : Type*} [Fintype d] [DecidableEq d]
    (U : Matrix.unitaryGroup d ℂ) (H : Herm d) : (conjMap U.val H).val.trace = H.val.trace := by
  change (U.val * H.val * U.valᴴ).trace = _
  have hu : U.valᴴ * U.val = 1 := Matrix.mem_unitaryGroup_iff'.mp U.property
  rw [Matrix.trace_mul_cycle, hu, Matrix.one_mul]

theorem twist_trace (U : Matrix.unitaryGroup (n × m) ℂ) (H : Herm (n × m)) :
    (twist U.val H).val.trace = H.val.trace := by
  change (gamma (conjMap U.val (gamma H))).val.trace = _
  rw [gamma_trace, conjMap_trace, gamma_trace]

/-- A supplied continuous unitary path transports to a continuous twisted path.
The path and its physical availability are not derived from primitive data. -/
theorem twist_path_continuous {T : Type*} [TopologicalSpace T]
    (R : T → Matrix (n × m) (n × m) ℂ) (hR : Continuous R) (H : Herm (n × m)) :
    Continuous (fun t => twist (R t) H) := by
  have hc : Continuous (fun t => conjMap (R t) (gamma H)) :=
    ((hR.mul continuous_const).mul hR.star).subtype_mk _
  exact gamma.toLinearMap.continuous_of_finiteDimensional.comp hc

theorem product_statistics_separate (X Y : Herm (n × m))
    (h : ∀ E F, pairing (product E F) X = pairing (product E F) Y) : X = Y := by
  have hz : ∀ A : Herm (n × m), pairing A (X - Y) = 0 := by
    intro A
    have ha : A ∈ Submodule.span ℝ (Set.range (fun p : Herm n × Herm m => product p.1 p.2)) := by
      rw [product_span]; trivial
    induction ha using Submodule.span_induction with
    | mem A ha => obtain ⟨⟨E,F⟩,rfl⟩ := ha; simp only [map_sub, h E F, sub_self]
    | zero => simp
    | add A B hA hB ihA ihB => simp only [map_add, LinearMap.add_apply, ihA, ihB, add_zero]
    | smul r A hA ih => simp only [map_smul, LinearMap.smul_apply, ih, smul_zero]
  exact sub_eq_zero.mp (pairing_nondegenerate.2 _ hz)

theorem hermitian_difference_positive {d : Type*} [Fintype d] [DecidableEq d] (A : Herm d) :
    ∃ P Q : Herm d, Positive P ∧ Positive Q ∧ A = P - Q := by
  let Q : Herm d := ‖A.val‖ • 1
  have hQ : Positive Q := Matrix.PosSemidef.one.smul (norm_nonneg A.val)
  have hbound : -Q.val ≤ A.val := by
    simpa [Q, Algebra.algebraMap_eq_smul_one] using
      (show IsSelfAdjoint A.val from A.property).neg_algebraMap_norm_le_self
  have hP : Positive (A + Q) := by
    change (A.val + Q.val).PosSemidef
    simpa only [sub_neg_eq_add] using (sub_nonneg.mpr hbound).posSemidef
  exact ⟨A + Q, Q, hP, hQ, by abel⟩

/-- Tomography uses genuine local positive tests, not unphysical extra probes. -/
theorem positive_product_statistics_separate (X Y : Herm (n × m))
    (h : ∀ E F, Positive E → Positive F → pairing (product E F) X = pairing (product E F) Y) :
    X = Y := by
  apply product_statistics_separate
  intro E F
  obtain ⟨P,Q,hP,hQ,rfl⟩ := hermitian_difference_positive E
  obtain ⟨R,S,hR,hS,rfl⟩ := hermitian_difference_positive F
  change pairing (productMap (P-Q) (R-S)) X = pairing (productMap (P-Q) (R-S)) Y
  simp only [map_sub, LinearMap.sub_apply]
  change (pairing (product P R) X - pairing (product Q R) X) -
    (pairing (product P S) X - pairing (product Q S) X) = _
  rw [h P R hP hR, h P S hP hS, h Q R hQ hR, h Q S hQ hS]
  rfl

theorem binary_product_statistics_separate (X Y : Herm (n × m))
    (h : ∀ E F, Binary E → Binary F → pairing (product E F) X = pairing (product E F) Y) :
    X = Y := by
  apply positive_product_statistics_separate
  intro E F hE hF
  obtain ⟨r,A,_,hA,rfl⟩ := positive_ray_binary E hE
  obtain ⟨s,B,_,hB,rfl⟩ := positive_ray_binary F hF
  simp only [product_smul_left, product_smul_right, map_smul, LinearMap.smul_apply, h A B hA hB]

theorem bp_salient {H : Herm (n × m)} (hp : BlockPositive H) (hn : BlockPositive (-H)) : H = 0 := by
  apply positive_product_statistics_separate
  intro E F hE hF
  have hlo := hp E F hE hF
  have hhi := hn E F hE hF
  rw [map_neg] at hhi
  simpa only [map_zero] using le_antisymm (neg_nonneg.mp hhi) hlo

#print axioms blockPositive_iff_dual_sep
#print axioms sep_ppt
#print axioms twisted_self_dual
#print axioms sep_local
#print axioms bp_local
#print axioms twisted_local
#print axioms twist_reversible
#print axioms twist_trace
#print axioms twist_path_continuous
#print axioms product_statistics_separate
#print axioms binary_product_statistics_separate
#print axioms bp_salient
end TensorCountermodelCones
