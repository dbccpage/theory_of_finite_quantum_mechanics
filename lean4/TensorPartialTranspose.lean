import TensorMeasurements

/-! Partial transpose on the first tensor factor. These are finite-dimensional
coordinate identities, not assumptions selecting a physical composite cone. -/
open Matrix Module
open scoped BigOperators Kronecker ComplexOrder MatrixOrder
noncomputable section
namespace TensorPartialTranspose
open TensorTomography TensorComposition TensorOperationalCone TensorEffectOrder
variable {n m : Type*} [Fintype n] [Fintype m]

def pt (A : Matrix (n × m) (n × m) ℂ) : Matrix (n × m) (n × m) ℂ :=
  fun i j => A (j.1, i.2) (i.1, j.2)

@[simp] theorem pt_pt (A : Matrix (n × m) (n × m) ℂ) : pt (pt A) = A := rfl

def gamma : Herm (n × m) ≃ₗ[ℝ] Herm (n × m) where
  toFun A := ⟨pt A.val, by
    change (pt A.val)ᴴ = pt A.val
    ext i j
    exact congrFun (congrFun A.property (j.1, i.2)) (i.1, j.2)⟩
  invFun A := ⟨pt A.val, by
    change (pt A.val)ᴴ = pt A.val
    ext i j
    exact congrFun (congrFun A.property (j.1, i.2)) (i.1, j.2)⟩
  left_inv A := Subtype.ext (pt_pt A.val)
  right_inv A := Subtype.ext (pt_pt A.val)
  map_add' A B := rfl
  map_smul' r A := rfl

@[simp] theorem gamma_val (A : Herm (n × m)) : (gamma A).val = pt A.val := rfl
@[simp] theorem gamma_gamma (A : Herm (n × m)) : gamma (gamma A) = A := rfl

def trans (A : Herm n) : Herm n := ⟨A.valᵀ, by
  change (A.valᵀ)ᴴ = A.valᵀ
  rw [conjTranspose_transpose_eq_transpose_conjTranspose,
    (show A.valᴴ = A.val from A.property)]⟩

@[simp] theorem gamma_product (A : Herm n) (B : Herm m) :
    gamma (product A B) = product (trans A) B := rfl

@[simp] theorem gamma_trace (A : Herm (n × m)) : (gamma A).val.trace = A.val.trace := rfl

/-- Partial transpose is self-adjoint for the real trace pairing. -/
theorem pairing_gamma (A B : Herm (n × m)) : pairing (gamma A) B = pairing A (gamma B) := by
  simp only [pairing_apply, gamma_val, Matrix.trace, Matrix.diag_apply, Matrix.mul_apply,
    Fintype.sum_prod_type, pt]
  congr 1
  conv_lhs =>
    rw [Finset.sum_comm]
    arg 2
    ext j
    rw [Finset.sum_comm]
  rw [Finset.sum_comm]

theorem pairing_gamma_gamma (A B : Herm (n × m)) :
    pairing (gamma A) (gamma B) = pairing A B := by rw [pairing_gamma, gamma_gamma]

def conjMap {a b : Type*} [Fintype a] [Fintype b]
    (U : Matrix b a ℂ) : Herm a →ₗ[ℝ] Herm b where
  toFun A := ⟨U * A.val * Uᴴ, by
    change (U * A.val * Uᴴ)ᴴ = _
    simp only [conjTranspose_mul, conjTranspose_conjTranspose,
      (show A.valᴴ = A.val from A.property), Matrix.mul_assoc]⟩
  map_add' A B := Subtype.ext (by simp [Matrix.mul_add, Matrix.add_mul])
  map_smul' r A := Subtype.ext (by simp)

@[simp] theorem conjMap_val {a b : Type*} [Fintype a] [Fintype b]
    (U : Matrix b a ℂ) (A : Herm a) : (conjMap U A).val = U * A.val * Uᴴ := rfl

theorem conjMap_positive {a b : Type*} [Fintype a] [Fintype b]
    (U : Matrix b a ℂ) {A : Herm a} (hA : Positive A) : Positive (conjMap U A) :=
  hA.mul_mul_conjTranspose_same U

theorem conjMap_product {a b : Type*} [Fintype a] [Fintype b]
    (U : Matrix a n ℂ) (W : Matrix b m ℂ) (A : Herm n) (B : Herm m) :
    conjMap (U ⊗ₖ W) (product A B) = product (conjMap U A) (conjMap W B) := by
  apply Subtype.ext
  simp only [conjMap_val, product, conjTranspose_kronecker, mul_kronecker_mul]

theorem trans_conjMap {a : Type*} [Fintype a] (U : Matrix a n ℂ) (A : Herm n) :
    trans (conjMap U A) = conjMap (U.map star) (trans A) := by
  apply Subtype.ext
  have hs : (U.map star)ᴴ = Uᵀ := by ext i j; simp [Matrix.conjTranspose, Matrix.map_apply]
  change (U * A.val * Uᴴ)ᵀ = U.map star * A.valᵀ * (U.map star)ᴴ
  rw [hs, Matrix.transpose_mul, Matrix.transpose_mul, Matrix.conjTranspose_transpose]
  simp only [Matrix.mul_assoc]

/-- The covariance formula applies also to rectangular embeddings. -/
theorem gamma_conjMap_product {a b : Type*} [Fintype a] [Fintype b]
    (U : Matrix a n ℂ) (W : Matrix b m ℂ) (A : Herm (n × m)) :
    gamma (conjMap (U ⊗ₖ W) A) = conjMap (U.map star ⊗ₖ W) (gamma A) := by
  have h : gamma.toLinearMap.comp (conjMap (U ⊗ₖ W)) =
      (conjMap (U.map star ⊗ₖ W)).comp gamma.toLinearMap := by
    apply product_calibration
    intro E F
    simp only [LinearMap.comp_apply, LinearEquiv.coe_coe,
      conjMap_product, gamma_product, trans_conjMap]
  exact LinearMap.congr_fun h A

theorem conjMap_inverse [DecidableEq n] (U : Matrix.unitaryGroup n ℂ) (A : Herm n) :
    conjMap U.valᴴ (conjMap U.val A) = A := by
  apply Subtype.ext
  simp only [conjMap_val, conjTranspose_conjTranspose, ← Matrix.mul_assoc]
  have hu : U.valᴴ * U.val = 1 := Matrix.mem_unitaryGroup_iff'.mp U.property
  rw [hu, Matrix.one_mul]
  rw [Matrix.mul_assoc, hu, Matrix.mul_one]

#print axioms pairing_gamma_gamma
#print axioms gamma_conjMap_product
#print axioms conjMap_inverse
end TensorPartialTranspose
