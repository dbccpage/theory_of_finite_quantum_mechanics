import OperationalFilterFamily
import OperationalFieldSelection

/-! Concrete orthant models and semantic boundary witnesses. Admission in these
examples is specified by the positive subnormalized maps; no primitive physical
admission claim or local-tomography derivation is inferred. -/
namespace OperationalBoundaryWitnesses
open OperationalTomography OperationalFilterFamily
open scoped BigOperators

/-- The rational nonnegative orthant with sum normalization. -/
def orthant (I : Type*) [Fintype I] : OrderedModel (I → ℚ) where
  positive := {x | ∀ i, 0 ≤ x i}
  zero_mem := fun _ => le_refl 0
  add_mem := fun x hx y hy i => add_nonneg (hx i) (hy i)
  smul_mem := fun a ha x hx i => mul_nonneg ha (hx i)
  unit := ∑ i, LinearMap.proj i
  unit_nonneg := by
    intro x hx
    simpa only [LinearMap.sum_apply, LinearMap.proj_apply] using
      Finset.sum_nonneg (fun i (_ : i ∈ Finset.univ) => hx i)

/-- A concrete admission model: normalized preparations, bounded effects, and
all positive subnormalized maps. Sequential closure is a proved field. -/
def canonicalAdmission {W : Type*} [AddCommGroup W] [Module ℚ W]
    (O : OrderedModel W) : SequentialAdmission ℚ W where
  preparations := {P | ∃ p : W, p ∈ O.positive ∧ O.unit p = 1 ∧ P = preparation p}
  tests := {e | ∀ x ∈ O.positive, 0 ≤ e x ∧ e x ≤ O.unit x}
  processes := {T | OutcomeFilter O T}
  sequential := by
    rintro P ⟨p,hp,hn,rfl⟩ e he
    rw [← reset_is_sequential]
    exact reset_outcome_filter O p e hp hn he

theorem orthant_basis_normalized (I : Type*) [Fintype I] [DecidableEq I] (i : I) :
    basisVector (K := ℚ) i ∈ (orthant I).positive ∧ (orthant I).unit (basisVector i) = 1 := by
  constructor
  · intro k; unfold basisVector; split_ifs <;> norm_num
  · simp [orthant, basisVector, LinearMap.sum_apply]

theorem orthant_basis_span (I : Type*) [Fintype I] [DecidableEq I] :
    Submodule.span ℚ (Set.range (basisVector (K := ℚ) (I := I))) = ⊤ := by
  apply top_unique
  intro x _
  have h : ∀ i, x i • basisVector (K := ℚ) i ∈
      Submodule.span ℚ (Set.range (basisVector (K := ℚ) (I := I))) := by
    intro i
    exact Submodule.smul_mem _ _ (Submodule.subset_span ⟨i,rfl⟩)
  have hs := Submodule.sum_mem _ (fun i (_ : i ∈ Finset.univ) => h i)
  convert hs using 1
  ext k
  simp [basisVector]

theorem orthant_effect_bounded (I : Type*) [Fintype I] (i : I) (x : I → ℚ)
    (hx : x ∈ (orthant I).positive) :
    0 ≤ (LinearMap.proj i : (I → ℚ) →ₗ[ℚ] ℚ) x ∧
      (LinearMap.proj i : (I → ℚ) →ₗ[ℚ] ℚ) x ≤ (orthant I).unit x := by
  refine ⟨hx i, ?_⟩
  simpa [orthant, LinearMap.sum_apply] using
    Finset.single_le_sum (fun j _ => hx j) (Finset.mem_univ i)

/-- All hypotheses of the finite admitted-reset theorem are discharged in an
actual OrderedModel and SequentialAdmission, including preparation span. -/
theorem orthant_reset_family (I : Type*) [Fintype I] [DecidableEq I] :
    (∀ ij : I × I, reset (basisVector (K := ℚ) ij.1) (LinearMap.proj ij.2) ∈
      (canonicalAdmission (orthant I)).processes ∧
      OutcomeFilter (orthant I) (reset (basisVector ij.1) (LinearMap.proj ij.2))) ∧
    OperationalTomography.Irreducible
      (fun ij : I × I => reset (basisVector (K := ℚ) ij.1) (LinearMap.proj ij.2)) := by
  apply admitted_reset_family (orthant I) (canonicalAdmission (orthant I))
    (basisVector (K := ℚ)) (fun i => LinearMap.proj i)
  · intro i
    have hi := orthant_basis_normalized I i
    exact ⟨hi.1, hi.2, ⟨_, hi.1, hi.2, rfl⟩⟩
  · intro i
    have he := orthant_effect_bounded I i
    exact ⟨he, he⟩
  · exact orthant_basis_span I
  · intro x hx; funext i; exact hx i

def productResetOps (ij : PairIndex × PairIndex) :
    DoubledCoordinates →ₗ[ℚ] DoubledCoordinates := lift doubledProduct (matrixUnit ij.1 ij.2)

/-- The hidden alternatives are positive normalized states, not just vectors. -/
theorem doubled_point_normalized (i : DoubledIndex) :
    pointState i ∈ (orthant DoubledIndex).positive ∧
      (orthant DoubledIndex).unit (pointState i) = 1 :=
  orthant_basis_normalized DoubledIndex i

theorem product_preparation_normalized (i : PairIndex) :
    doubledProduct.prepare (basisVector i) ∈ (orthant DoubledIndex).positive ∧
      (orthant DoubledIndex).unit (doubledProduct.prepare (basisVector i)) = 1 := by
  constructor
  · intro bi
    change 0 ≤ (1/2 : ℚ) * basisVector i bi.2
    exact mul_nonneg (by norm_num) ((orthant_basis_normalized PairIndex i).1 bi.2)
  · rcases i with ⟨i,j⟩
    fin_cases i <;> fin_cases j <;>
      norm_num [orthant, doubledProduct, Fintype.sum_prod_type, Fin.sum_univ_two, basisVector]

theorem product_effect_bounded (j : PairIndex) (x : DoubledCoordinates)
    (hx : x ∈ (orthant DoubledIndex).positive) :
    0 ≤ ((LinearMap.proj j).comp doubledProduct.observe) x ∧
      ((LinearMap.proj j).comp doubledProduct.observe) x ≤ (orthant DoubledIndex).unit x := by
  constructor
  · exact add_nonneg (hx (0,j)) (hx (1,j))
  · have h (b : Fin 2) : x (b,j) ≤ ∑ k : PairIndex, x (b,k) :=
      Finset.single_le_sum (fun k _ => hx (b,k)) (Finset.mem_univ j)
    simpa [orthant, doubledProduct, LinearMap.sum_apply, Fintype.sum_prod_type,
      Fin.sum_univ_two] using add_le_add (h 0) (h 1)

/-- Product-test resets are genuine admitted outcome filters in the doubled
orthant model even though their family is reducible. -/
theorem product_reset_admitted (ij : PairIndex × PairIndex) :
    productResetOps ij ∈ (canonicalAdmission (orthant DoubledIndex)).processes ∧
      OutcomeFilter (orthant DoubledIndex) (productResetOps ij) := by
  have hp := product_preparation_normalized ij.1
  have he := product_effect_bounded ij.2
  have h := reset_outcome_filter (orthant DoubledIndex) _ _ hp.1 hp.2 he
  rw [← product_reset_formula doubledProduct ij.1 ij.2] at h
  exact ⟨h,h⟩

theorem product_reset_boundary :
    (∀ ij x, doubledProduct.observe (productResetOps ij x) =
      matrixUnit ij.1 ij.2 (doubledProduct.observe x)) ∧
    ¬ OperationalTomography.Irreducible productResetOps ∧
    ¬ Function.Injective doubledProduct.observe := by
  refine ⟨fun ij => lift_descent doubledProduct _, ?_, doubled_product_not_injective⟩
  intro h
  exact doubled_product_not_injective ((product_resets_irreducible_iff doubledProduct).mp h)

/-- Product effects on the doubled carrier do not separate, even with all basis
preparations available. The common kernel is exhibited by two different states. -/
theorem product_effects_not_separating :
    ¬ (∀ x : DoubledCoordinates,
      (∀ j : PairIndex, ((LinearMap.proj j).comp doubledProduct.observe) x = 0) → x = 0) := by
  intro h
  apply doubled_product_not_injective
  intro x y he
  have hz := h (x-y) (fun j => by simp [he])
  exact sub_eq_zero.mp hz

def globalResetOps (ij : DoubledIndex × DoubledIndex) :
    DoubledCoordinates →ₗ[ℚ] DoubledCoordinates := reset (basisVector ij.1) (LinearMap.proj ij.2)

theorem global_reset_boundary :
    (∀ ij, globalResetOps ij ∈ (canonicalAdmission (orthant DoubledIndex)).processes ∧
      OutcomeFilter (orthant DoubledIndex) (globalResetOps ij)) ∧
    OperationalTomography.Irreducible globalResetOps ∧
    ¬ (∃ loc : DoubledIndex × DoubledIndex → PairCoordinates →ₗ[ℚ] PairCoordinates,
      ∀ ij x, doubledProduct.observe (globalResetOps ij x) = loc ij (doubledProduct.observe x)) := by
  have h := orthant_reset_family DoubledIndex
  refine ⟨h.1, h.2, ?_⟩
  rintro ⟨loc,descent⟩
  exact doubled_product_not_injective
    (calibrated_tomography doubledProduct globalResetOps loc descent h.2)

/-- Both sides of the reset boundary hold in concrete, nonempty finite models. -/
theorem classical_product_reset_boundary :
    OperationalTomography.Irreducible
      (fun ij : PairIndex × PairIndex => lift (identityCalibration (K := ℚ) (V := PairCoordinates))
        (matrixUnit ij.1 ij.2)) ∧
    Function.Injective (identityCalibration (K := ℚ) (V := PairCoordinates)).observe := by
  have h : Function.Injective (identityCalibration (K := ℚ) (V := PairCoordinates)).observe := fun _ _ h => h
  exact ⟨(product_resets_irreducible_iff _).mpr h,h⟩

end OperationalBoundaryWitnesses

#print axioms OperationalBoundaryWitnesses.orthant
#print axioms OperationalBoundaryWitnesses.canonicalAdmission
#print axioms OperationalBoundaryWitnesses.orthant_reset_family
#print axioms OperationalBoundaryWitnesses.product_reset_boundary
#print axioms OperationalBoundaryWitnesses.product_effects_not_separating
#print axioms OperationalBoundaryWitnesses.global_reset_boundary
#print axioms OperationalBoundaryWitnesses.classical_product_reset_boundary

#print axioms OperationalBoundaryWitnesses.doubled_point_normalized
#print axioms OperationalBoundaryWitnesses.product_reset_admitted
