import Po000JordanLie
import Mathlib.Analysis.InnerProductSpace.StarOrder
import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Range

/-! Finite-dimensional closed image and reverse positive-cone inclusion for E.1.
All spectral input is supplied by Mathlib's proved continuous functional calculus.
No square-root-closure hypothesis or custom kernel axiom is used. -/

namespace Po000JordanLie.Data

open Complex

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℂ E]
  [StarAddMonoid E] [StarModule ℂ E] [FiniteDimensional ℂ E]

local instance : CompleteSpace E := FiniteDimensional.complete ℂ E

noncomputable def continuousLeft (d : Data E) (a : E) : E →L[ℂ] E :=
  (d.left a).toContinuousLinearMap

variable (d : Data E)

@[simp] theorem continuousLeft_apply (a b : E) : d.continuousLeft a b = d.product a b := rfl

@[simp] theorem continuousLeft_add (a b : E) :
    d.continuousLeft (a + b) = d.continuousLeft a + d.continuousLeft b := by
  ext c
  simp [product, smul_add, add_assoc, add_left_comm]

@[simp] theorem continuousLeft_smul (r : ℂ) (a : E) :
    d.continuousLeft (r • a) = r • d.continuousLeft a := by
  ext b
  simp [product, smul_add, smul_smul, mul_comm]

@[simp] theorem continuousLeft_one : d.continuousLeft d.one = 1 := by
  ext a
  simp

theorem continuousLeft_product (a b : E) :
    d.continuousLeft (d.product a b) = d.continuousLeft a * d.continuousLeft b := by
  ext c
  exact d.product_associative a b c

theorem continuousLeft_star (a : E) :
    d.continuousLeft (star a) = star (d.continuousLeft a) := by
  apply (ContinuousLinearMap.eq_adjoint_iff _ _).2
  intro b c
  simpa only [continuousLeft_apply, left_apply, star_star] using d.left_adjoint (star a) b c

theorem continuousLeft_faithful : Function.Injective d.continuousLeft := by
  intro a b h
  have h' := congrArg (fun f : E →L[ℂ] E => f d.one) h
  simpa using h'

noncomputable def leftLinear : E →ₗ[ℂ] (E →L[ℂ] E) where
  toFun := d.continuousLeft
  map_add' := d.continuousLeft_add
  map_smul' := d.continuousLeft_smul

noncomputable def image : StarSubalgebra ℂ (E →L[ℂ] E) where
  carrier := Set.range d.continuousLeft
  zero_mem' := ⟨0, by ext b; simp [product]⟩
  add_mem' := by rintro _ _ ⟨a, rfl⟩ ⟨b, rfl⟩; exact ⟨a + b, d.continuousLeft_add a b⟩
  one_mem' := ⟨d.one, d.continuousLeft_one⟩
  mul_mem' := by rintro _ _ ⟨a, rfl⟩ ⟨b, rfl⟩; exact ⟨d.product a b, d.continuousLeft_product a b⟩
  algebraMap_mem' := by
    intro r
    refine ⟨r • d.one, ?_⟩
    simp [Algebra.algebraMap_eq_smul_one]
  star_mem' := by rintro _ ⟨a, rfl⟩; exact ⟨star a, d.continuousLeft_star a⟩

theorem image_closed : IsClosed (d.image : Set (E →L[ℂ] E)) :=
  (d.leftLinear.range).closed_of_finiteDimensional

@[instance_reducible]
noncomputable def imageCStarAlgebra : CStarAlgebra d.image := by
  letI : IsClosed (d.image : Set (E →L[ℂ] E)) := d.image_closed
  infer_instance

theorem image_finite : FiniteDimensional ℂ d.image := by
  change FiniteDimensional ℂ d.leftLinear.range
  infer_instance

theorem image_self_adjoint_iff (a : E) :
    IsSelfAdjoint (d.continuousLeft a) ↔ star a = a := by
  change star (d.continuousLeft a) = d.continuousLeft a ↔ star a = a
  rw [← d.continuousLeft_star]
  exact d.continuousLeft_faithful.eq_iff

omit [FiniteDimensional ℂ E] in
theorem jordan_self (a : E) : d.product a a = d.j a a := by
  have hz : d.l a a = 0 := by
    have h := d.l_anti a a
    have hh : (2 : ℂ) • d.l a a = 0 := by
      calc
        _ = d.l a a + d.l a a := by module
        _ = 0 := (congrArg (fun x => x + d.l a a) h).trans (neg_add_cancel _)
    exact (smul_eq_zero.mp hh).resolve_left (by norm_num)
  simp [product, hz]

theorem positive_iff_jordan_square (a : E) :
    0 ≤ d.continuousLeft a ↔ ∃ b, star b = b ∧ d.j b b = a := by
  constructor
  · intro ha
    let : IsClosed (d.image : Set (E →L[ℂ] E)) := d.image_closed
    let t := cfcₙ Real.sqrt (d.continuousLeft a)
    have ht : t ∈ d.image := cfcₙ_mem _ (show d.continuousLeft a ∈ d.image from ⟨a, rfl⟩)
    obtain ⟨b, hb⟩ := ht
    have hs : IsSelfAdjoint t := by dsimp [t]; cfc_tac
    have hsq : t * t = d.continuousLeft a := by
      dsimp [t]
      rw [← cfcₙ_mul ..]
      convert cfcₙ_id' ℝ (d.continuousLeft a) using 1
      exact cfcₙ_congr fun r hr => by grind [Real.mul_self_sqrt]
    refine ⟨b, ?_, ?_⟩
    · apply d.continuousLeft_faithful
      rw [d.continuousLeft_star, hb, hs.star_eq]
    · apply d.continuousLeft_faithful
      rw [← d.jordan_self, d.continuousLeft_product, hb, hsq]
  · rintro ⟨b, hb, rfl⟩
    rw [← d.jordan_self, d.continuousLeft_product]
    have hstar : star (d.continuousLeft b) = d.continuousLeft b := by
      rw [← d.continuousLeft_star, hb]
    simpa only [hstar] using star_mul_self_nonneg (d.continuousLeft b)

/-- Additive closure is exactly the set of finite sums of real Jordan squares,
including the empty sum. -/
def positiveCone : AddSubmonoid E :=
  AddSubmonoid.closure {a | ∃ b, star b = b ∧ d.j b b = a}

theorem mem_positiveCone_iff (a : E) : a ∈ d.positiveCone ↔ 0 ≤ d.continuousLeft a := by
  constructor
  · intro ha
    induction ha using AddSubmonoid.closure_induction with
    | mem x hx => exact (d.positive_iff_jordan_square x).2 hx
    | zero => simp [continuousLeft, left]
    | add x y _ _ hx hy => simpa only [d.continuousLeft_add] using add_nonneg hx hy
  · intro ha
    exact AddSubmonoid.subset_closure ((d.positive_iff_jordan_square a).1 ha)

end Po000JordanLie.Data

#print axioms Po000JordanLie.Data.continuousLeft_faithful
#print axioms Po000JordanLie.Data.image_closed
#print axioms Po000JordanLie.Data.imageCStarAlgebra
#print axioms Po000JordanLie.Data.image_finite
#print axioms Po000JordanLie.Data.image_self_adjoint_iff
#print axioms Po000JordanLie.Data.positive_iff_jordan_square
#print axioms Po000JordanLie.Data.mem_positiveCone_iff
