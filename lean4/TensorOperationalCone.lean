import TensorConeReconstruction
import TensorReachability

open Matrix
open scoped BigOperators Kronecker ComplexOrder
noncomputable section
namespace TensorOperationalCone
open TensorConeReconstruction TensorReachability

def conjugate {d : Type*} [Fintype d] (U A : Matrix d d ℂ) : Matrix d d ℂ := U * A * Uᴴ

theorem conjugate_rankOne {d : Type*} [Fintype d] (U : Matrix d d ℂ) (s : d → ℂ) :
    conjugate U (rankOne s) = rankOne (U *ᵥ s) := by
  simp only [conjugate, rankOne, mul_vecMulVec, vecMulVec_mul, star_mulVec]

theorem quadratic_transport {d : Type*} [Fintype d] (U A : Matrix d d ℂ) (s : d → ℂ) :
    quadratic (conjugate Uᴴ A) s = quadratic A (U *ᵥ s) := by
  simp only [conjugate, quadratic, conjTranspose_conjTranspose, ← mulVec_mulVec,
    star_mulVec, dotProduct_mulVec]

theorem conjugate_mul {d : Type*} [Fintype d] (U V A : Matrix d d ℂ) :
    conjugate (U * V) A = conjugate U (conjugate V A) := by
  simp only [conjugate, conjTranspose_mul, Matrix.mul_assoc]

/-- Only local unitary conjugations and the controlled shift (in both directions)
are required. The seed-orbit hypothesis of the cone kernel is now a theorem. -/
theorem controlled_shift_selects_positive {n m : ℕ} [NeZero m] (hnm : n ≤ m)
    (K : Set (Matrix (Fin n × Fin m) (Fin n × Fin m) ℂ))
    (hz : 0 ∈ K) (ha : ∀ A ∈ K, ∀ B ∈ K, A + B ∈ K)
    (hh : ∀ A ∈ K, A.IsHermitian)
    (hseed : ∀ a b, rankOne (productVector a b) ∈ K)
    (htest : ∀ A ∈ K, ∀ a b, 0 ≤ quadratic A (productVector a b))
    (hlocal : ∀ (U : Matrix.unitaryGroup (Fin n) ℂ) (V : Matrix.unitaryGroup (Fin m) ℂ),
      ∀ A ∈ K, conjugate (U.val ⊗ₖ V.val) A ∈ K)
    (hshift : ∀ A ∈ K, conjugate (controlledShift hnm).val A ∈ K)
    (hunshift : ∀ A ∈ K, conjugate (controlledShift hnm).valᴴ A ∈ K) :
    K = {A | A.PosSemidef} := by
  let R (g : Matrix.unitaryGroup (Fin n) ℂ × Matrix.unitaryGroup (Fin m) ℂ) :=
    (g.1.val ⊗ₖ g.2.val) * (controlledShift hnm).val
  apply operational_orbit_selects_positive K hz ha hh (G :=
    Matrix.unitaryGroup (Fin n) ℂ × Matrix.unitaryGroup (Fin m) ℂ)
  refine {
    seeds := Set.range (fun p : (Fin n → ℂ) × (Fin m → ℂ) => productVector p.1 p.2)
    vector := fun g s => R g *ᵥ s
    forward := fun g A => conjugate (R g) A
    backward := fun g A => conjugate (R g)ᴴ A
    seed_preparation := ?_
    seed_positive := ?_
    forward_preserves := ?_
    backward_preserves := ?_
    preparation_transport := fun g s => conjugate_rankOne (R g) s
    test_transport := fun g A s => quadratic_transport (R g) A s
    reachability := ?_ }
  · rintro s ⟨⟨a,b⟩,rfl⟩; exact hseed a b
  · rintro A hA s ⟨⟨a,b⟩,rfl⟩; exact htest A hA a b
  · intro g A hA
    rw [show R g = (g.1.val ⊗ₖ g.2.val) * (controlledShift hnm).val from rfl,
      conjugate_mul]
    exact hlocal g.1 g.2 _ (hshift A hA)
  · intro g A hA
    change conjugate (((g.1.val ⊗ₖ g.2.val) * (controlledShift hnm).val)ᴴ) A ∈ K
    rw [conjTranspose_mul, conjugate_mul, conjTranspose_kronecker]
    exact hunshift _ (hlocal (star g.1) (star g.2) A hA)
  · intro ψ
    obtain ⟨U,V,s,h⟩ := schmidt_reachability hnm ψ
    exact ⟨(U,V),productVector s (Pi.single 0 1),⟨(s,Pi.single 0 1),rfl⟩,h⟩

#print axioms controlled_shift_selects_positive
end TensorOperationalCone
