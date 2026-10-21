import TensorEffectCone

/-! Operational measurement corollaries. `hcone` is exactly the conclusion of
`TensorComposition.quantum_state_cone`. Effect saturation and finite-test
saturation are distinct hypotheses; neither follows from cone equality. -/
open Matrix Module
open scoped BigOperators ComplexOrder MatrixOrder Kronecker
noncomputable section
namespace TensorMeasurements
open TensorTomography TensorComposition TensorEffectOrder TensorEffectCone
variable {V : Type*} [AddCommGroup V] [Module ℝ V] {n m : ℕ}

def effectRepresentation (D : TomographicData (Fin n) (Fin m) V) :
    Module.Dual ℝ V ≃ₗ[ℝ] Herm (Fin n × Fin m) :=
  (representation D).symm.dualMap.trans
    (LinearMap.BilinForm.toDual pairing pairing_nondegenerate).symm

@[simp] theorem effectRepresentation_apply (D : TomographicData (Fin n) (Fin m) V)
    (f : Module.Dual ℝ V) (x : V) :
    pairing (effectRepresentation D f) (representation D x) = f x := by
  change pairing ((LinearMap.BilinForm.toDual pairing pairing_nondegenerate).symm
    ((representation D).symm.dualMap f)) (representation D x) = _
  rw [LinearMap.BilinForm.apply_toDual_symm_apply]
  simp

def unitEffect (D : TomographicData (Fin n) (Fin m) V) : Module.Dual ℝ V := D.test 1 1

theorem effectRepresentation_unit (D : TomographicData (Fin n) (Fin m) V) :
    effectRepresentation D (unitEffect D) = 1 := by
  apply (LinearMap.BilinForm.toDual pairing pairing_nondegenerate).injective
  ext A
  obtain ⟨x, rfl⟩ := (representation D).surjective A
  change pairing (effectRepresentation D (unitEffect D)) (representation D x) =
    pairing 1 (representation D x)
  rw [effectRepresentation_apply, pairing_one]
  exact unit_test_is_trace D x

theorem effectRepresentation_product (D : TomographicData (Fin n) (Fin m) V)
    (E : Herm (Fin n)) (F : Herm (Fin m)) :
    effectRepresentation D (D.test E F) = product E F := by
  apply (LinearMap.BilinForm.toDual pairing pairing_nondegenerate).injective
  ext A
  obtain ⟨x, rfl⟩ := (representation D).surjective A
  change pairing (effectRepresentation D (D.test E F)) (representation D x) =
    pairing (product E F) (representation D x)
  rw [effectRepresentation_apply, representation_test]

def ValidEffect (D : TomographicData (Fin n) (Fin m) V) (K : Set V)
    (f : Module.Dual ℝ V) : Prop := ∀ x ∈ K, 0 ≤ f x ∧ f x ≤ unitEffect D x

/-- No-restriction for individual binary effects, explicitly supplied. -/
def EffectSaturated (D : TomographicData (Fin n) (Fin m) V) (K : Set V)
    (available : Set (Module.Dual ℝ V)) : Prop :=
  ∀ f, ValidEffect D K f → f ∈ available

theorem validEffect_iff_binary (D : TomographicData (Fin n) (Fin m) V) (K : Set V)
    (hcone : (fun x => (representation D x).val) '' K = {A | A.PosSemidef})
    (f : Module.Dual ℝ V) : ValidEffect D K f ↔ Binary (effectRepresentation D f) := by
  rw [binary_iff_bounds]
  constructor
  · intro hf A hA
    have hm : A.val ∈ (fun x => (representation D x).val) '' K := by
      rw [hcone]; exact hA
    obtain ⟨x, hx, he⟩ := hm
    have he' : representation D x = A := Subtype.ext he
    have hp := hf x hx
    rw [← effectRepresentation_apply D f x, unitEffect, unit_test_is_trace] at hp
    simpa only [he'] using hp
  · intro hf x hx
    have hA : Positive (representation D x) := by
      have hm : (representation D x).val ∈ (fun x => (representation D x).val) '' K :=
        ⟨x, hx, rfl⟩
      rw [hcone] at hm
      exact hm
    have hp := hf (representation D x) hA
    simpa only [effectRepresentation_apply, ← unit_test_is_trace, unitEffect] using hp

/-- Equality with the full interval requires the explicit effect-saturation premise. -/
theorem available_effects_eq_interval (D : TomographicData (Fin n) (Fin m) V) (K : Set V)
    (hcone : (fun x => (representation D x).val) '' K = {A | A.PosSemidef})
    (available : Set (Module.Dual ℝ V))
    (hsound : ∀ f ∈ available, ValidEffect D K f)
    (hsaturated : EffectSaturated D K available) :
    effectRepresentation D '' available = {E | 0 ≤ E.val ∧ E.val ≤ 1} := by
  ext E
  constructor
  · rintro ⟨f, hf, rfl⟩
    exact (binary_iff_interval _).mp ((validEffect_iff_binary D K hcone f).mp (hsound f hf))
  · intro hE
    obtain ⟨f, rfl⟩ := (effectRepresentation D).surjective E
    exact ⟨f, hsaturated f ((validEffect_iff_binary D K hcone f).mpr
      ((binary_iff_interval _).mpr hE)), rfl⟩

variable {ι : Type*} [Fintype ι]

/-- A separate operational assumption: compatible available outcomes summing
to the deterministic effect can be implemented jointly as a finite test. -/
def FiniteTestSaturated (D : TomographicData (Fin n) (Fin m) V)
    (available : Set (Module.Dual ℝ V)) (tests : Set (ι → Module.Dual ℝ V)) : Prop :=
  ∀ f, (∀ i, f i ∈ available) → ∑ i, f i = unitEffect D → f ∈ tests

def POVM (E : ι → Herm (Fin n × Fin m)) : Prop :=
  (∀ i, Positive (E i)) ∧ ∑ i, E i = 1

/-- Each outcome of a finite positive resolution of the identity lies in [0,I]. -/
theorem povm_binary (E : ι → Herm (Fin n × Fin m)) (hE : POVM E) (i : ι) :
    Binary (E i) := by
  classical
  apply (binary_iff_bounds _).mpr
  intro A hA
  have hs : (∑ j, pairing (E j) A) = A.val.trace.re := by
    rw [← LinearMap.sum_apply, ← map_sum, hE.2, pairing_one]
  refine ⟨pairing_nonneg (hE.1 i) hA, ?_⟩
  rw [← hs]
  exact Finset.single_le_sum (fun j _ => pairing_nonneg (hE.1 j) hA) (Finset.mem_univ i)

/-- Available tests are POVMs from soundness alone, without saturation. -/
theorem test_povm_of_sound (D : TomographicData (Fin n) (Fin m) V) (K : Set V)
    (hcone : (fun x => (representation D x).val) '' K = {A | A.PosSemidef})
    (available : Set (Module.Dual ℝ V)) (tests : Set (ι → Module.Dual ℝ V))
    (hsound : ∀ f ∈ available, ValidEffect D K f)
    (htest : ∀ f ∈ tests, (∀ i, f i ∈ available) ∧ ∑ i, f i = unitEffect D)
    (f : ι → Module.Dual ℝ V) (hf : f ∈ tests) :
    POVM (fun i => effectRepresentation D (f i)) := by
  obtain ⟨hav, hsum⟩ := htest f hf
  constructor
  · intro i
    exact ((validEffect_iff_binary D K hcone (f i)).mp (hsound (f i) (hav i))).1
  · rw [← map_sum, hsum, effectRepresentation_unit]

/-- POVM availability needs both saturation assumptions. This theorem applies
to every finite outcome type. -/
theorem test_iff_povm (D : TomographicData (Fin n) (Fin m) V) (K : Set V)
    (hcone : (fun x => (representation D x).val) '' K = {A | A.PosSemidef})
    (available : Set (Module.Dual ℝ V)) (tests : Set (ι → Module.Dual ℝ V))
    (hsound : ∀ f ∈ available, ValidEffect D K f)
    (hsaturated : EffectSaturated D K available)
    (htest : ∀ f ∈ tests, (∀ i, f i ∈ available) ∧ ∑ i, f i = unitEffect D)
    (htestSaturated : FiniteTestSaturated D available tests)
    (f : ι → Module.Dual ℝ V) :
    f ∈ tests ↔ POVM (fun i => effectRepresentation D (f i)) := by
  constructor
  · exact test_povm_of_sound D K hcone available tests hsound htest f
  · intro hE
    apply htestSaturated f
    · intro i
      apply hsaturated (f i)
      exact (validEffect_iff_binary D K hcone (f i)).mpr (povm_binary _ hE i)
    · apply (effectRepresentation D).injective
      rw [map_sum, effectRepresentation_unit]
      exact hE.2

/-- The generated operational effect cone needs soundness, local products and
calibrated pullbacks, but neither of the two saturation assumptions. -/
theorem operational_effect_cone [NeZero m] (hnm : n ≤ m)
    (D : TomographicData (Fin n) (Fin m) V) (K : Set V)
    (hcone : (fun x => (representation D x).val) '' K = {A | A.PosSemidef})
    (available : Set (Module.Dual ℝ V))
    (hsound : ∀ f ∈ available, ValidEffect D K f)
    (hproduct : ∀ E F, Binary E → Binary F → D.test E F ∈ available)
    (hlocal : ∀ (U : Matrix.unitaryGroup (Fin n) ℂ) (W : Matrix.unitaryGroup (Fin m) ℂ),
      PullbackClosed (effectRepresentation D '' available) (U.val ⊗ₖ W.val))
    (hshift : PullbackClosed (effectRepresentation D '' available)
      (TensorReachability.controlledShift hnm).val) :
    (effectCone (effectRepresentation D '' available) :
      Set (Matrix (Fin n × Fin m) (Fin n × Fin m) ℂ)) = {A | A.PosSemidef} := by
  apply effect_cone_eq_positive hnm _ _ _ hlocal hshift
  · rintro E ⟨f, hf, rfl⟩
    exact ((validEffect_iff_binary D K hcone f).mp (hsound f hf)).1
  · intro E F hE hF
    exact ⟨D.test E F, hproduct E F hE hF, effectRepresentation_product D E F⟩

/-- End-to-end application of the state-cone theorem. The primitive operational
premises remain explicit, alongside the two separate measurement saturations. -/
theorem quantum_measurements [NeZero m] (hnm : n ≤ m)
    (D : TomographicData (Fin n) (Fin m) V) (K : Set V)
    (hz : 0 ∈ K) (ha : ∀ x ∈ K, ∀ y ∈ K, x + y ∈ K)
    (hprep : ∀ a b, D.prepare (hermRankOne a) (hermRankOne b) ∈ K)
    (hprob : ∀ x ∈ K, ∀ a b, 0 ≤ D.test (hermRankOne a) (hermRankOne b) x)
    (hlocalState : ∀ (U : Matrix.unitaryGroup (Fin n) ℂ) (W : Matrix.unitaryGroup (Fin m) ℂ),
      Preserves D K (U.val ⊗ₖ W.val))
    (hshiftState : Preserves D K (TensorReachability.controlledShift hnm).val)
    (hunshiftState : Preserves D K (TensorReachability.controlledShift hnm).valᴴ)
    (available : Set (Module.Dual ℝ V)) (tests : Set (ι → Module.Dual ℝ V))
    (hsound : ∀ f ∈ available, ValidEffect D K f)
    (hproduct : ∀ E F, Binary E → Binary F → D.test E F ∈ available)
    (hlocalEffect : ∀ (U : Matrix.unitaryGroup (Fin n) ℂ) (W : Matrix.unitaryGroup (Fin m) ℂ),
      PullbackClosed (effectRepresentation D '' available) (U.val ⊗ₖ W.val))
    (hshiftEffect : PullbackClosed (effectRepresentation D '' available)
      (TensorReachability.controlledShift hnm).val)
    (hsaturated : EffectSaturated D K available)
    (htest : ∀ f ∈ tests, (∀ i, f i ∈ available) ∧ ∑ i, f i = unitEffect D)
    (htestSaturated : FiniteTestSaturated D available tests) :
    ((effectCone (effectRepresentation D '' available) :
      Set (Matrix (Fin n × Fin m) (Fin n × Fin m) ℂ)) = {A | A.PosSemidef}) ∧
    (effectRepresentation D '' available = {E | 0 ≤ E.val ∧ E.val ≤ 1}) ∧
    (∀ f, f ∈ tests ↔ POVM (fun i => effectRepresentation D (f i))) := by
  have hcone := quantum_state_cone hnm D K hz ha hprep hprob
    hlocalState hshiftState hunshiftState
  exact ⟨operational_effect_cone hnm D K hcone available hsound hproduct hlocalEffect hshiftEffect,
    available_effects_eq_interval D K hcone available hsound hsaturated,
    test_iff_povm D K hcone available tests hsound hsaturated htest htestSaturated⟩

#print axioms effectRepresentation_apply
#print axioms validEffect_iff_binary
#print axioms available_effects_eq_interval
#print axioms test_povm_of_sound
#print axioms test_iff_povm
#print axioms operational_effect_cone
#print axioms quantum_measurements
end TensorMeasurements
